# 例文解説システム設計仕様書
**Rephrase English Learning System**  
**作成日:** 2025年8月2日  
**更新日:** 2025年8月6日  
**バージョン:** v2.0  
**ステータス:** Production Ready

## 📋 概要

例文解説システムは、Rephraseトレーニング画面で動詞の文法解説を提供するモーダルベースのシステムです。**V_group_keyベースの検出システム**により、現在表示中の例文に対応する文法解説を自動表示し、動詞の活用形や派生形にも対応します。

## 🎯 主要機能

### 1. データ駆動型V_group_key検出
- **リアルタイム検出**: `window.lastSelectedSlots`から現在表示中のV_group_keyを取得
- **ランダマイズ対応**: 全体ランダマイズ後も正確な解説を表示
- **活用形対応**: `recovered2` → `recover`の基本形解説を表示

### 2. RephraseStateManager統合
- **統合状態管理**: RephraseStateManagerとの完全統合
- **キャッシュ最適化**: リアルタイムデータ優先、キャッシュはフォールバック
- **グローバル共有**: 他のマネージャーとのインスタンス共有

### 3. 解説ボタン自動配置
- 例文シャッフルボタン（`randomize-all`）の右横に自動配置
- ボタンテキスト: "� 例文解説"
- 初期化時に`addExplanationButtons()`で設置

### 4. 基本形フォールバック検索
- 完全一致検索を最優先
- 数字サフィックス除去による基本形検索
- 例: `recovered2` → `recover`の解説を表示

## 🏗️ アーキテクチャ

### クラス構造
```javascript
class ExplanationManager {
  constructor() {
    this.stateManager = window.stateManager || new window.RephraseStateManager();
    this.modal = null;
    this.isInitialized = false;
    this.STATE_PATHS = {
      MODAL_VISIBLE: 'explanation.modal.visible',
      EXPLANATION_DATA: 'explanation.data.explanationData',
      BUTTON_VISIBLE: 'explanation.ui.buttons.explanation',
      CURRENT_V_GROUP_KEY: 'explanation.context.currentVGroupKey',
      INITIALIZATION_STATUS: 'explanation.system.isInitialized'
    };
  }
}
```

### V_group_key検出システム（v2.0改良版）
```javascript
getCurrentVGroupKey() {
  // 最優先: window.lastSelectedSlotsからリアルタイム取得
  if (window.lastSelectedSlots && window.lastSelectedSlots.length > 0) {
    const slotWithVGroupKey = window.lastSelectedSlots.find(slot => slot.V_group_key);
    if (slotWithVGroupKey && slotWithVGroupKey.V_group_key) {
      // 状態管理にキャッシュ更新
      this.stateManager.setState(this.STATE_PATHS.CURRENT_V_GROUP_KEY, slotWithVGroupKey.V_group_key);
      return slotWithVGroupKey.V_group_key;
    }
  }
  
  // フォールバック: window.currentRandomizedStateから取得
  if (window.currentRandomizedState && window.currentRandomizedState.vGroupKey) {
    return window.currentRandomizedState.vGroupKey;
  }
  
  // 最後の手段: 状態管理キャッシュ（古い可能性あり）
  return this.stateManager.getState(this.STATE_PATHS.CURRENT_V_GROUP_KEY);
}
```

### 基本形フォールバック検索
```javascript
findExplanationByVGroupKey(vGroupKey) {
  const explanationData = this.stateManager.getState(this.STATE_PATHS.EXPLANATION_DATA) || [];
  
  // 完全一致を最優先で検索
  let explanation = explanationData.find(item => item.V_group_key === vGroupKey);
  
  if (explanation) return explanation;
  
  // 基本形検索（数字サフィックス除去）
  const baseVGroupKey = vGroupKey.replace(/\d+$/, '');
  if (baseVGroupKey !== vGroupKey) {
    explanation = explanationData.find(item => item.V_group_key === baseVGroupKey);
    if (explanation) return explanation;
  }
  
  return null;
}
```

### 状態管理（RephraseStateManager統合）
| 状態パス | 説明 | 型 | 優先度 |
|---------|------|-----|--------|
| `explanation.modal.visible` | モーダル表示状態 | Boolean | - |
| `explanation.data.explanationData` | 解説データ配列 | Array | - |
| `explanation.ui.buttons.explanation` | 解説ボタン表示状態 | Boolean | - |
| `explanation.context.currentVGroupKey` | 現在のV_group_key | String | 低（キャッシュ用） |
| `explanation.system.isInitialized` | 初期化ステータス | Boolean | - |

**注意**: `currentVGroupKey`は最後の手段として使用。リアルタイムデータを優先。

## 📊 データ構造

### V_group_key例（活用形対応）
```
recover    → recoverの使い方 （完全一致）
recovered2 → recoverの使い方 （基本形フォールバック）
go         → goの使い方      （完全一致）
went2      → goの使い方      （基本形検索失敗例）
```

### JSONデータ形式
```json
{
  "V_group_key": "recover",
  "Slot": "EXPLANATION", 
  "explanation_title": "recoverの使い方",
  "explanation_content": "recoverは「治る」なら自動詞で「from his illness」などを置いて情報を付加しますが、「回復する」なら他動詞で、まずは「his health」などの目的語が直接来ます。このように、同じ単語でどちらにも成り得るものは、使う場合に区別して注意する必要があります。"
}
```

### データ読み込み処理
```javascript
async loadExplanationData() {
  const response = await fetch('data/V自動詞第1文型.json');
  const allData = await response.json();
  
  // 解説データのみフィルタリング
  const explanationData = allData.filter(item => item.explanation_title);
  
  // RephraseStateManagerに保存
  this.stateManager.setState(this.STATE_PATHS.EXPLANATION_DATA, explanationData);
}
```

## 🔄 処理フロー

### 1. 初期化
```
1. ExplanationManager インスタンス作成
2. RephraseStateManager 統合確認
3. 初期状態設定 (initializeState)
4. JSONデータ読み込み (loadExplanationData)
5. モーダルイベント設定 (setupModalEvents)
6. 解説ボタン配置 (addExplanationButtons)
```

### 2. 解説表示（ランダマイズ対応）
```
1. 解説ボタンクリック
2. リアルタイムV_group_key検出 (getCurrentVGroupKey)
   - window.lastSelectedSlots優先
   - window.currentRandomizedState フォールバック
   - 状態管理キャッシュは最後
3. 基本形フォールバック検索 (findExplanationByVGroupKey)
4. モーダル表示 (showExplanation → openModal)
```

### 3. エラーハンドリング & フォールバック
```
- V_group_key未検出 → デバッグ情報付きエラーメッセージ
- 完全一致解説なし → 基本形検索実行
- 基本形解説なし → デバッグ情報付きエラーメッセージ
- JSON読み込みエラー → 空配列設定、ログ出力
```

## 🎨 UI仕様

### 解説ボタン
- **配置**: `randomize-all`ボタンの右横（insertAdjacentElement）
- **テキスト**: "💡 例文解説"
- **スタイル**: 
  ```css
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all 0.2s ease;
  margin-left: 10px;
  ```

### モーダルウィンドウ
- **背景**: rgba(0, 0, 0, 0.5) オーバーレイ
- **コンテンツ**: 
  - HTMLフォーマット対応
  - ESCキー・背景クリック・閉じるボタンで閉じる
  - アニメーション付き表示/非表示

## 🔧 重要な技術的変更点（v2.0）

### 1. 状態管理キャッシュ問題の解決
**問題**: 状態管理のキャッシュが最優先だったため、ランダマイズ後も古いV_group_keyを返していた
**解決**: リアルタイムデータ（`window.lastSelectedSlots`）を最優先に変更

### 2. 活用形対応の実装
**問題**: `recovered2`のようなV_group_keyで解説が表示されない
**解決**: 数字サフィックス除去による基本形フォールバック検索を追加

### 3. ランダマイズアルゴリズム連携
**統合**: RephraseのランダマイズシステムとExplanationManagerが完全連携
- `randomizeAllWithStateManagement` → `window.lastSelectedSlots` 更新
- ExplanationManager → リアルタイム検出 → 正しい解説表示

## 🧪 テスト仕様

### 動作確認項目（v2.0）
1. ✅ 解説ボタンが例文シャッフルボタンの右横に表示される
2. ✅ V_group_key検出がリアルタイムで正常動作する
3. ✅ 全体ランダマイズ後も正しい解説が表示される
4. ✅ 活用形V_group_key（`recovered2`）で基本形解説が表示される
5. ✅ モーダルの開閉・ESCキー・背景クリックが正常動作する
6. ✅ RephraseStateManager統合が正常動作する
7. ✅ 解説データが見つからない場合のフォールバック処理
8. ✅ レスポンシブ表示対応

### 重点テスト項目（v2.0新機能）
```javascript
// 1. ランダマイズ後のV_group_key検出テスト
// 全体ランダマイズ実行 → 解説ボタンクリック → 正しい解説表示確認

// 2. 活用形フォールバックテスト
// recovered2のV_group_keyが選択 → recoverの解説が表示されることを確認

// 3. リアルタイム検出テスト
// window.lastSelectedSlotsの内容変更 → 解説システムが即座に対応することを確認
```

### デバッグ方法
```javascript
// 解説システム状態確認
console.log('ExplanationManager状態:', window.explanationManager.getDebugState());

// V_group_key検出確認
console.log('現在のV_group_key:', window.explanationManager.getCurrentVGroupKey());

// リアルタイムデータ確認
console.log('lastSelectedSlots:', window.lastSelectedSlots);
console.log('currentRandomizedState:', window.currentRandomizedState);

// 解説データ確認
console.log('解説データ:', window.explanationManager.stateManager.getState('explanation.data.explanationData'));
```

## 🚀 将来拡張計画

### Phase 2.1: マルチ文型対応
- 第2文型、第3文型などの解説データ統合
- 文型別解説自動選択システム
- 動的データソース切り替え

### Phase 2.2: 解説コンテンツ拡張
- `explanation_examples`, `explanation_notes`フィールド対応
- 関連文法項目リンク機能
- 音声解説対応

### Phase 3: 学習効果測定
- 解説閲覧履歴の記録
- 理解度測定・復習推奨システム
- 学習パフォーマンス分析

## 📝 更新履歴

| 日付 | バージョン | 更新内容 |
|------|------------|----------|
| 2025-08-02 | v1.0 | 初版作成、基本機能実装完了 |
| 2025-08-06 | v2.0 | **重要な設計変更**: V_group_key検出システム改良、RephraseStateManager統合、活用形フォールバック対応、ランダマイズアルゴリズム連携 |

## 🔧 トラブルシューティング

### よくある問題と解決方法

**問題**: ランダマイズ後に古い解説が表示される
**原因**: 状態管理キャッシュが優先されている
**解決**: v2.0で修正済み（リアルタイムデータ優先）

**問題**: `recovered2`などの活用形で解説が表示されない
**原因**: 完全一致検索のみ実装されている
**解決**: v2.0で基本形フォールバック検索を追加

**問題**: RephraseStateManagerとの競合
**原因**: インスタンス管理の問題
**解決**: v2.0でグローバルインスタンス共有を実装

---
**開発チーム**: Rephrase Development Team  
**文書管理**: 設計仕様書フォルダー  
**関連ファイル**: `training/js/modules/explanation-manager.js`, `training/data/V自動詞第1文型.json`
