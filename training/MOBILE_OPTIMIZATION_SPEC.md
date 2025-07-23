# 📱 Rephraseモバイル最適化仕様書 v1.0

## 🎯 概要
PC版の機能を**完全に保持**しながら、スマホで使いやすい**上下2分割スワイプシステム**を実装。

---

## 🚀 実装済み機能

### 1. モバイル検出システム
- **画面サイズベース検出**: 768px以下を自動的にモバイル扱い
- **User-Agent検出**: Android, iPhone, iPad等をサポート
- **タッチデバイス検出**: タッチインターフェース対応
- **Chrome DevTools対応**: 開発時のシミュレーション可能

```javascript
// 実装済み検出ロジック
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
const isTouchDevice = 'ontouchstart' in window;
const isSmallScreen = window.innerWidth <= 768;
```

### 2. 上下2分割レイアウト
- **上エリア**: 上位スロット（画面の40%）
- **下エリア**: サブスロット（画面の40%）
- **自動表示**: サブスロットを強制表示（PC版では非表示）

```css
.mobile-device .slot-wrapper:not([id$="-sub"]) {
  height: 40vh !important;
}
.mobile-device .slot-wrapper[id$="-sub"] {
  height: 40vh !important;
  display: block !important;
}
```

### 3. タッチ操作最適化
- **横スワイプ**: スロット内でのスクロール操作
- **ピンチ操作**: 画面全体の拡大縮小
- **縦ドラッグ**: 画面全体のスクロール

```css
.mobile-device body {
  touch-action: manipulation; /* 画面全体でピンチ可能 */
}
.mobile-device .slot-wrapper {
  touch-action: pan-x; /* 横スワイプのみ、他は画面全体に委譲 */
}
```

### 4. UI要素サイズ調整
- **タイトル**: フォントサイズ16px、狭い帯幅
- **ボタン**: 12px、適切なパディング
- **スロット**: 幅40%、高さ120px制限
- **画像**: 40px×40px
- **テキスト**: 8px、行間1.1

### 5. フロートメニュー対応
- **タイトル位置調整**: `margin-top: 50px`でメニュー下に配置
- **スロット位置調整**: `margin-top: 60px`で適切な配置

---

## 🔧 技術仕様

### ファイル構成
```
training/
├── index.html              # モバイル検出JavaScript含む
├── mobile-split-view-simple.css  # モバイル専用CSS
└── style.css               # PC版CSS（変更なし）
```

### CSS優先度戦略
- **!important使用**: PC版CSSをオーバーライド
- **詳細セレクタ**: `.mobile-device`クラスで分岐
- **属性セレクタ**: タイトル帯の正確な指定

### モバイル検出フロー
1. **画面サイズチェック** → 768px以下
2. **User-Agentチェック** → モバイルデバイス
3. **タッチ対応チェック** → タッチイベント
4. **mobile-deviceクラス追加** → CSS適用

---

## ✅ 動作確認済み環境
- **Chrome DevTools**: モバイルシミュレーション
- **実機テスト**: 準備中
- **画面サイズ**: 375px〜768px対応

---

## 🚧 未完成・課題

### 残存問題
1. **JSONデータ読み込み後のテスト**: スロット表示確認
2. **実機での動作確認**: タッチ操作の最終検証
3. **GitHubホスティング遅延**: 反映タイミングの改善
4. **サイズ調整の微調整**: ユーザビリティ向上

### 今後の改善予定
- [ ] 詳細ボタンのタップ範囲拡大
- [ ] スワイプアニメーションの追加
- [ ] ローディング状態の表示改善
- [ ] エラーハンドリングの強化

---

## 📋 制約・原則

### 絶対禁止事項
- ❌ PC版の機能削除・変更
- ❌ PC版のスタイル破壊
- ❌ display:flex/grid の使用（制約による）
- ❌ position の使用（制約による）
- ❌ フロートメニューの変更

### 許可事項
- ✅ height, width, overflow の調整
- ✅ touch-action の設定
- ✅ display:block の使用
- ✅ font-size, padding, margin の調整

---

## 🎯 実装方針
「PC版をそのまま保持し、モバイルでは**サイズとレイアウトのみ調整**」

これにより、既存の全機能（ボタン動作、データ処理、UI制御）がモバイルでも完全に動作する。

---

**更新日**: 2025年7月23日  
**バージョン**: v1.0  
**ステータス**: 開発中（基本機能実装完了）
