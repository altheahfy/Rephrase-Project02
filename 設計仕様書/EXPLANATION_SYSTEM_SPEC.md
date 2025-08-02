# 例文解説システム設計仕様書
**Rephrase English Learning System**  
**作成日:** 2025年8月2日  
**バージョン:** v1.0  
**ステータス:** Production Ready

## 📋 概要

例文解説システムは、Rephraseトレーニング画面で動詞の文法解説を提供するモーダルベースのシステムです。V_group_keyに基づいて対応する文法解説を表示し、学習者の理解を深めます。

## 🎯 主要機能

### 1. 動的解説ボタン配置
- 例文シャッフルボタン（`randomize-all`）付近に自動配置
- ボタンテキスト: "📚 解説"
- 初期化時に`addExplanationButtons()`で設置

### 2. V_group_key検出システム
- 現在表示中の例文から動詞のV_group_keyを自動検出
- `getCurrentVGroupKey()`メソッドで実装
- Vスロット内の`data-v-group-key`属性から取得

### 3. 解説データ管理
- JSONファイル: `training/data/V自動詞第1文型.json`
- 対象フィールド: `explanation_title`, `explanation_content`
- フィルタリング: 両フィールドが空でないアイテムのみ抽出

### 4. モーダル表示システム
- レスポンシブ対応のモーダルウィンドウ
- オーバーレイクリック・閉じるボタンで閉じる機能
- 動的コンテンツ表示

## 🏗️ アーキテクチャ

### クラス構造
```javascript
class ExplanationSystem {
  constructor() {
    this.stateManager = window.RephraseState;
    this.modal = null;
    this.isInitialized = false;
  }
}
```

### 状態管理（state-manager.js統合）
| 状態パス | 説明 | 型 |
|---------|------|-----|
| `explanation.modal.visible` | モーダル表示状態 | Boolean |
| `explanation.data.explanationData` | 解説データ配列 | Array |
| `explanation.ui.buttons.explanation` | 解説ボタン表示状態 | Boolean |
| `explanation.context.currentVGroupKey` | 現在のV_group_key | String |
| `explanation.system.isInitialized` | 初期化ステータス | Boolean |

## 📊 データ構造

### JSONデータ形式
```json
{
  "V_group_key": "recover",
  "Slot": "EXPLANATION",
  "explanation_title": "recoverの使い方",
  "explanation_content": "recoverは「治る」なら自動詞で「from his illness」などを置いて情報を付加するが、「回復する」なら他動詞で、まずは「his health」などの目的語が直接来る。このように、同じ単語でどちらにも成り得るものは、使う場合に区別して注意しなければならない。"
}
```

### データ読み込み処理
```javascript
async loadExplanationData() {
  // V自動詞第1文型.jsonを読み込み
  const response = await fetch('data/V自動詞第1文型.json');
  const allData = await response.json();
  
  // 解説データのみフィルタリング
  const explanationData = allData.filter(item => 
    item.explanation_title && item.explanation_title.trim() !== "" && 
    item.explanation_content && item.explanation_content.trim() !== ""
  );
  
  // state-managerに保存
  this.stateManager.setState(this.STATE_PATHS.EXPLANATION_DATA, explanationData);
}
```

## 🔄 処理フロー

### 1. 初期化
```
1. ExplanationSystem インスタンス作成
2. RephraseState 接続確認
3. JSONデータ読み込み (loadExplanationData)
4. モーダル要素作成 (createModal)
5. 解説ボタン配置 (addExplanationButtons)
```

### 2. 解説表示
```
1. 解説ボタンクリック
2. V_group_key検出 (getCurrentVGroupKey)
3. 対応解説データ検索 (findExplanationByVGroupKey)
4. モーダル表示 (showExplanation → openModal)
```

### 3. エラーハンドリング
```
- 解説データなし → デバッグ情報付きエラーメッセージ
- V_group_key検出失敗 → 「解説情報なし」メッセージ
- JSON読み込みエラー → 空配列設定、ログ出力
```

## 🎨 UI仕様

### 解説ボタン
- **配置**: `randomize-all`ボタンの後
- **スタイル**: 
  ```css
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
  ```

### モーダルウィンドウ
- **背景**: rgba(0, 0, 0, 0.5) オーバーレイ
- **コンテンツ**: 
  - 最大幅: 600px
  - 背景: white
  - 角丸: 10px
  - パディング: 30px
- **閉じるボタン**: 右上に ❌ 表示

## 🔧 設定・カスタマイズ

### データソース変更
```javascript
// loadExplanationData()内のfetch URLを変更
const response = await fetch('data/新しいデータファイル.json');
```

### V_group_key検出ロジック拡張
```javascript
getCurrentVGroupKey() {
  // 追加の検出方法を実装
  const customDetection = this.detectFromCustomSource();
  return customDetection || this.detectFromVSlot();
}
```

## 🚀 将来拡張計画

### Phase 2: 複数文型対応
- 第2文型、第3文型などの解説データ対応
- 文型別データファイル管理
- 動的データソース切り替え

### Phase 3: 解説コンテンツ拡張
- 例文サンプル表示
- 関連文法項目リンク
- 音声解説対応

### Phase 4: 学習履歴統合
- 解説閲覧履歴の記録
- 復習推奨システム
- 理解度測定機能

## 🧪 テスト仕様

### 動作確認項目
1. ✅ 解説ボタンが適切に表示される
2. ✅ V_group_key検出が正常動作する
3. ✅ 対応する解説が正しく表示される
4. ✅ モーダルの開閉が正常動作する
5. ✅ 解説データが見つからない場合の処理
6. ✅ レスポンシブ表示対応

### デバッグ方法
```javascript
// 解説データ確認
console.log('解説データ:', window.RephraseState.getState('explanation.data.explanationData'));

// V_group_key確認
console.log('現在のV_group_key:', window.explanationSystem.getCurrentVGroupKey());

// 解説システム状態確認
console.log('解説システム:', window.explanationSystem);
```

## 📝 更新履歴

| 日付 | バージョン | 更新内容 |
|------|------------|----------|
| 2025-08-02 | v1.0 | 初版作成、基本機能実装完了 |

---
**開発チーム**: Rephrase Development Team  
**文書管理**: 設計仕様書フォルダー  
**関連ファイル**: `training/js/explanation_system.js`, `training/data/V自動詞第1文型.json`
