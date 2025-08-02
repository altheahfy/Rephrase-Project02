# 手動ズーム・縮小機構 設計仕様書

## 概要

Rephraseトレーニングシステムにおけるスピーキング練習時の視認性向上のため、スロット空間全体を縦横比を保ったまま拡大・縮小する機構。

**実装状況**: ✅ 完了（2025年8月2日）
- **実装ファイル**: `training/js/modules/zoom-controller-manager.js`
- **統合システム**: RephraseStateManager連携
- **テストファイル**: `training/js/modules/zoom-controller-manager-test.js`

## 機能要件

### 主要機能
- **リアルタイムズーム調整**: スライダーによる50%〜150%の範囲でのズーム制御 ✅
- **縦横比保持**: CSS `transform: scale()` を使用した比率保持ズーム ✅
- **位置関係維持**: 上位スロットとサブスロットの相対位置を完全保持 ✅
- **設定永続化**: ローカルストレージによるズームレベル保存 ✅
- **動的対応**: サブスロット展開時の自動ズーム適用 ✅
- **S/C1特別処理**: 垂直位置補正機能 ✅
- **RephraseStateManager統合**: 状態管理統一 ✅

### 対象要素
- **スロット領域全体**: 例文シャッフルボタンとスロットコンテナを含む `<section>` 要素 ✅
- **上位スロット**: M1, S, AUX, M2, O1等のメインスロット ✅
- **サブスロット**: 各スロットの詳細展開エリア（`[id$="-sub"]`） ✅

## 技術仕様

### クラス構造（ZoomControllerManager）

```javascript
class ZoomControllerManager {
  constructor()                    // RephraseStateManager統合
  initializeState()               // 状態初期化
  init()                          // メイン初期化
  acquireDOMElements()            // DOM要素取得
  scheduleDelayedInit()           // 遅延初期化
  identifyTargetContainers()      // ズーム対象特定
  saveOriginalMarginValue()       // margin値保存
  setupEventListeners()           // イベント設定
  applyZoom(zoomLevel)           // ズーム適用（S/C1特別処理含む）
  updateZoomDisplay(zoomLevel)    // 表示更新
  saveZoomLevel(zoomLevel)       // 設定保存
  loadZoomLevel()                // 設定読み込み
  forceDefaultZoom()             // 強制100%設定
  resetZoom()                    // リセット
  setupDynamicSubslotObserver()  // 動的監視
  setZoom(zoomLevel)             // 外部API
  getCurrentZoom()               // 現在値取得
  forceSubslotDetection()        // 強制検出
  createScrollHint()             // ヒント作成
  showScrollHint(show)           // ヒント表示
  debugInfo()                    // デバッグ情報
  debugVerticalPosition()        // 位置診断
  resetSettings()                // 設定リセット
  destroy()                      // 破棄
}
```

### 主要プロパティ

| プロパティ | 型 | 説明 |
|------------|-----|------|
| `stateManager` | RephraseStateManager | 状態管理インスタンス |
| `zoomSlider` | HTMLElement | ズームスライダー要素 |
| `zoomValue` | HTMLElement | ズーム値表示要素 |
| `zoomResetButton` | HTMLElement | リセットボタン要素 |
| `targetContainers` | Array | ズーム対象コンテナ配列 |
| `currentZoom` | Number | 現在のズーム倍率 (0.5-1.5) |
| `storageKey` | String | ローカルストレージキー |

## DOM要素の特定アルゴリズム

### 1. スロット領域の自動検出

```javascript
// 例文シャッフルボタンとslot-wrapperを含むsection要素を特定
const sections = document.querySelectorAll('section');
sections.forEach(section => {
  const hasShuffleButton = section.querySelector('#randomize-all');
  const hasSlotWrapper = section.querySelector('.slot-wrapper');
  
  if (hasShuffleButton && hasSlotWrapper) {
    // このsection要素をズーム対象とする
  }
});
```

### 2. フォールバック機能

メインsection要素が見つからない場合：
```javascript
const mainSlotWrapper = document.querySelector('.slot-wrapper:not([id$="-sub"])');
```

## ズーム適用メカニズム

### CSS Transform適用

```css
transform: scale(zoomLevel) !important;
transform-origin: top left !important;
```

### 空白調整（縮小時）

```javascript
if (zoomLevel < 1.0) {
  const spaceReduction = (1 - zoomLevel) * 50;
  element.style.marginBottom = `-${spaceReduction}px`;
}
```

## 動的監視システム

### MutationObserver設定

```javascript
observer.observe(document.body, {
  attributes: true,
  childList: true,
  subtree: true,
  attributeFilter: ['style', 'class']
});
```

### サブスロット変更検出

- **スタイル変更**: `display: none` ↔ `display: flex` の監視
- **DOM変更**: サブスロット要素の追加・削除監視
- **遅延適用**: サブスロット変更時は300ms遅延で再適用

## ユーザーインターフェース

### HTMLコントロール

```html
<div style="display: flex; align-items: center; gap: 4px;">
  <label>🔍 ズーム</label>
  <input type="range" id="zoomSlider" min="0.5" max="1.5" step="0.1" value="1.0">
  <span id="zoomValue">100%</span>
  <button id="zoomResetButton">リセット</button>
</div>
```

### 視覚的フィードバック

| ズーム範囲 | 色 | 説明 |
|------------|-----|------|
| < 80% | 赤色 (#FF5722) | 縮小状態 |
| 80-120% | グレー (#666) | 通常状態 |
| > 120% | 緑色 (#4CAF50) | 拡大状態 |

## データ永続化

### ローカルストレージ仕様

- **キー**: `rephrase_zoom_level`
- **値**: ズーム倍率の文字列表現
- **デフォルト値**: `"1.0"` (100%)
- **有効範囲**: 0.5 ≤ value ≤ 1.5

### 起動時の動作

```javascript
// 保存値が1.0の場合のみ復元、それ以外は強制的に100%にリセット
if (zoomLevel === 1.0) {
  // 復元
} else {
  forceDefaultZoom(); // 100%に強制設定
}
```

## パフォーマンス最適化

### 効率的な要素特定

- **一回の検索**: 初期化時に対象要素を特定し、配列に保存
- **キャッシュ利用**: 再検索は動的変更時のみ実行
- **フォールバック**: メイン検索失敗時の代替手段

### 最小限のDOM操作

- **単一ズーム適用**: 親要素への `scale()` のみで子要素も自動スケール
- **不要な調整削除**: 二重ズーム適用や複雑な配置調整を排除

## グローバルAPI

### 公開メソッド

```javascript
// ズーム設定
window.setZoom(level)           // 指定倍率に設定
window.resetZoom()              // 100%にリセット
window.getCurrentZoom()         // 現在の倍率取得

// デバッグ・メンテナンス
window.forceSubslotDetection()  // サブスロット強制検出
window.debugZoomController()    // 状態デバッグ出力
window.resetZoomSettings()      // 設定完全リセット
```

## エラーハンドリング

### 初期化エラー対応

```javascript
if (!this.zoomSlider || !this.zoomValue || !this.zoomResetButton) {
  console.warn('⚠️ ズームコントロール要素が見つかりません');
  return; // 処理を中断
}
```

### ストレージエラー対応

```javascript
try {
  localStorage.setItem(this.storageKey, zoomLevel.toString());
} catch (error) {
  console.warn('⚠️ ズームレベルの保存に失敗:', error);
}
```

## ブラウザ互換性

### 必要な機能

- **CSS Transform**: `scale()`, `transform-origin`
- **MutationObserver**: DOM変更監視
- **localStorage**: 設定永続化
- **ES6**: クラス構文、アロー関数

### 対応ブラウザ

- Chrome 26+
- Firefox 14+
- Safari 6.1+
- Edge 12+

## 今後の拡張可能性

### 機能拡張候補

1. **キーボードショートカット**: Ctrl+マウスホイールでのズーム
2. **プリセット機能**: よく使用するズーム倍率のワンクリック設定
3. **アニメーション**: ズーム変更時のスムーズな移行効果
4. **フォーカス追従**: ズーム時の表示領域自動調整

### パフォーマンス改善

1. **仮想化**: 大量スロット時の描画最適化
2. **レスポンシブ対応**: デバイスサイズに応じた自動ズーム
3. **メモリ最適化**: 不要なイベントリスナーの解放

## 保守・運用

### ログ出力レベル

- **🔍**: 基本動作（初期化、ズーム適用）
- **🎯**: 対象要素特定
- **📱**: サブスロット変更検出
- **💾**: データ保存・読み込み
- **⚠️**: 警告・エラー

### デバッグ支援

```javascript
// ズームコントローラー状態確認
debugZoomController();

// サブスロット強制再検出
forceSubslotDetection();

// 垂直位置診断（位置ズレ調査用）
debugVerticalPosition();

// 設定完全リセット
resetZoomSettings();
```

## サブスロット個別対応手法

### 問題の背景
スロット種別（S, C1等）によってズーム適用時の挙動が異なり、以下の問題が発生：
1. **S, C1サブスロット**: section全体のscaleが効かず、縮小されない + 垂直位置が下にズレる
2. **その他サブスロット**: section全体のscaleのみで縮小されすぎる

### 解決手法

#### 1. スロット種別による個別処理
```javascript
// S, C1のみ: 個別スケール適用 + 垂直位置補正
if (container.type === 'subslot' && (container.id === 'slot-s-sub' || container.id === 'slot-c1-sub')) {
  // 個別スケール適用
  container.element.style.setProperty('transform', `scale(${zoomLevel})`, 'important');
  container.element.style.setProperty('transform-origin', 'top left', 'important');
  
  // 垂直位置補正（下に離れる問題を解決）
  if (zoomLevel < 1.0) {
    const verticalCorrection = (1 - zoomLevel) * 600;
    container.element.style.setProperty('margin-top', `-${verticalCorrection}px`, 'important');
  } else {
    container.element.style.removeProperty('margin-top');
  }
}
```

#### 2. その他サブスロット: スケール補正
```javascript
// その他のサブスロット: section全体のscaleに加えて補正適用
else if (container.type === 'subslot') {
  const scaleCorrection = Math.min(1.2, 1 + (1 - zoomLevel) * 0.3); // 最大20%まで補正
  container.element.style.setProperty('transform', `scale(${scaleCorrection})`, 'important');
  container.element.style.setProperty('transform-origin', 'top left', 'important');
}
```

### 補正計算式

#### 垂直位置補正（S, C1専用）
- **式**: `verticalCorrection = (1 - zoomLevel) * 600`
- **例**: 60%ズーム時 → `(1 - 0.6) * 600 = 240px` 上方向補正

#### スケール補正（その他サブスロット）
- **式**: `scaleCorrection = Math.min(1.2, 1 + (1 - zoomLevel) * 0.3)`
- **例**: 
  - 60%ズーム時 → `1 + (1 - 0.6) * 0.3 = 1.12` (112%補正)
  - 80%ズーム時 → `1 + (1 - 0.8) * 0.3 = 1.06` (106%補正)
  - 100%ズーム時 → `1.0` (補正なし)

### 診断ツール
```javascript
// 垂直位置問題の診断
window.debugVerticalPosition = () => {
  const subslots = document.querySelectorAll('.slot-wrapper[id$="-sub"]:not([style*="display: none"])');
  subslots.forEach(subslot => {
    const computed = getComputedStyle(subslot);
    const rect = subslot.getBoundingClientRect();
    console.log(`${subslot.id}: top=${rect.top}px, transform="${computed.transform}"`);
  });
};
```

## 変更履歴

| バージョン | 日付 | 変更内容 |
|------------|------|----------|
| 1.0 | 2025年7月 | 初版作成 |
| 1.1 | 2025年8月2日 | **実装完了・モジュール化対応** |

## 実装完了状況（2025年8月2日）

### ✅ 完了機能
- **ZoomControllerManager**: 完全実装（770行）
- **RephraseStateManager統合**: 状態管理統一
- **S/C1垂直位置補正**: 垂直補正計算式 `(1 - zoomLevel) * 600` 適用
- **動的サブスロット対応**: MutationObserver実装
- **設定永続化**: localStorage連携
- **無限ループ対策**: デバウンス機能付きMutationObserver
- **テストシステム**: 包括的テストスイート（500行）

### 🎯 動作確認済み
- ズームスライダー操作: 50%〜150%のリアルタイムズーム
- S/C1特別処理: 垂直位置補正が正確に機能
- サブスロット動的対応: 開閉時の自動ズーム適用
- 状態管理統合: RephraseStateManagerとの連携

### 📁 関連ファイル
- **実装**: `training/js/modules/zoom-controller-manager.js`
- **テスト**: `training/js/modules/zoom-controller-manager-test.js`  
- **統合**: `training/js/core/state-manager.js`
- **HTML統合**: `training/index.html`

### 🔗 API
```javascript
// グローバルAPI
window.zoomController          // ZoomControllerManagerインスタンス
window.setZoom(1.2)           // ズーム設定
window.resetZoom()            // リセット
window.getCurrentZoom()       // 現在値取得
window.forceSubslotDetection() // 強制検出
window.debugZoomController()   // デバッグ情報
window.debugVerticalPosition() // 位置診断
```

**設計仕様書に基づく正確な実装が完了しました。** 🎉
|------------|------|----------|
| v1.0 | 2025-07-18 | 初期実装完了 |
| | | - 正確なsection要素特定機能 |
| | | - 位置関係保持機能 |
| | | - 動的サブスロット対応 |
| v1.1 | 2025-07-18 | サブスロット個別対応実装 |
| | | - S, C1の垂直位置補正機能追加 |
| | | - その他サブスロットのスケール補正追加 |
| | | - スロット種別による個別処理分岐実装 |

---

**作成日**: 2025年7月18日  
**対象システム**: Rephrase トレーニングUI  
**実装ファイル**: `js/zoom_controller.js`
