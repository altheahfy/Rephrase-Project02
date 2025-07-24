# 📱 Rephraseモバイル最適化統合仕様書 v2.0

**最終更新**: 2025年7月24日  
**対象**: Rephrase英語学習プラットフォーム モバイル最適化  

## 🚨 重要：設計要件定義（絶対遵守）

### 基本方針
1. **スマホ画面分割**: 画面を上下に分割（上部パネル・ボタンを考慮した分割比率）
2. **スワイプエリア化**: 各エリアは「スワイプエリア」として機能
   - 左右スワイプ操作可能
   - 画面全体でのピンチ拡大・縮小対応
3. **PC版完全保持**: PC版の上位スロット・サブスロットをそのまま表示
4. **機能変更禁止**: デザイン・各種機能は一切変更禁止
   - ランダマイズ機能
   - イラスト表示機能  
   - 順序制御機能
   - 分離疑問詞表示機能
   - その他全ての既存機能
5. **調整許可範囲**: 位置・大きさの調整のみ許可（スワイプエリア内での適切な表示のため）
6. **PC版機能保持**: 自動幅調整・高さ調整・レイアウト等のPC版機能を完全保持

### 実装原則
- PC版のスタイルを一切上書きしない
- `.mobile-device`クラスでスワイプ機能のみ追加
- `!important`による強制上書きは最小限に抑制
- PC版の動的機能（自動リサイズ等）は保持

---

## 🎯 実装アプローチ

**Always-Visible Subslot System + Transform Scale Architecture**

PC版の機能を**完全に保持**しながら、スマホで使いやすい**上下2分割スワイプシステム**を実装。

---

## ✅ 完全実装済み機能

### 1. Always-Visible Subslot System（革新的アプローチ）
- **概要**: サブスロットエリアを常時表示し、コンテンツのみ切り替える方式
- **解決した問題**: 
  - 詳細ボタン2回タップ問題 → **1回タップで正常動作**
  - 動的記載エリアの位置ずれ → **最初から適切な位置に表示**
- **技術実装**: `mobile-split-view-simple.css`による専用システム

### 2. スワイプエリア最適化
- **上位スロットエリア**: 35vh（元の7割サイズ）でジャストフィット実現
- **サブスロットエリア**: 17.5vh（元の7割サイズ）で理想的なバランス
- **スワイプ操作**: 快適なタッチ操作を維持

### 3. Transform Scale Content Optimization
- **上位スロット内容**: `transform: scale(0.75)` で75%縮小
- **サブスロット内容**: `transform: scale(0.65)` で65%縮小
- **重要**: スワイプエリア自体のサイズは維持、内部コンテンツのみ縮小

### 4. モバイル検出システム
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

### 5. タッチ操作最適化
- **横スワイプ**: スロット内でのスクロール操作
- **ピンチ操作**: 画面全体の拡大縮小
- **縦ドラッグ**: 画面全体のスクロール

```css
.mobile-device body {
  touch-action: manipulation; /* 画面全体でピンチ可能 */
}
.mobile-device .slot-wrapper {
  touch-action: pan-x pan-y; /* スワイプ操作有効 */
}
```

---

## 🔧 革新的技術実装

### Always-Visible Subslot System
```css
/* 🟢 サブスロット表示エリア：常時表示 */
.mobile-device #subslot-display-area {
  height: 17.5vh !important;
  display: block !important; /* 常時表示 */
  position: relative !important;
}

/* ✅ 選択されたサブスロットのみ表示 */
.mobile-device .slot-wrapper[id$="-sub"].active-subslot {
  display: block !important;
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
}
```

### Transform Scale Architecture
```css
/* 🎯 上位スロット内部コンテンツのみ縮小 */
.mobile-device .slot-wrapper:not([id$="-sub"]) > * {
  transform: scale(0.75) !important;
  transform-origin: top left !important;
}

/* 🎯 サブスロット内部コンテンツのみ縮小 */
.mobile-device .slot-wrapper[id$="-sub"].active-subslot > * {
  transform: scale(0.65) !important;
  transform-origin: top left !important;
}
```

---

## 📁 実装ファイル構成

### メインファイル
1. **`mobile-split-view-simple.css`** - モバイル最適化の核心実装
   - Always-Visible Subslot System
   - Transform Scale Content Optimization
   - 上部エリア超圧縮システム

### 統合済みファイル
1. **`training/index.html`** - モバイル検出・CSS適用システム
2. **モバイル検出JavaScript** - `.mobile-device` クラス自動適用

### CSS優先度戦略
```css
/* 🎯 正しいアプローチ：PC版保持 + スワイプ機能追加のみ */
.mobile-device .slot-wrapper:not([id$="-sub"]) {
  overflow-x: auto !important; /* スワイプ機能追加 */
  overflow-y: auto !important; /* スワイプ機能追加 */
  touch-action: pan-x pan-y !important; /* スワイプ機能追加 */
  /* PC版の width, height, margin, border, background はそのまま */
}
```

---

## 🚨 現在の問題と修正が必要な事項

### 1. 設計要件違反の修正が必要
現在の`mobile-split-view-simple.css`は設計要件に違反：

#### 問題点
- **大量の`!important`宣言**でPC版スタイルを強制上書き
- **PC版機能の破壊**（自動幅調整、高さ調整等）
- **新しいレイアウトシステムの構築**（要件違反）

#### 正しい実装方針
```css
/* ❌ 間違い：PC版を上書き */
.mobile-device .slot-wrapper:not([id$="-sub"]) {
  width: calc(100vw - 4px) !important; /* PC版の幅設定を破壊 */
  height: 35vh !important; /* PC版の高さ設定を破壊 */
}

/* ✅ 正しい：スワイプ機能のみ追加 */
.mobile-device .slot-wrapper:not([id$="-sub"]) {
  overflow-x: auto !important; /* スワイプ機能追加 */
  touch-action: pan-x pan-y !important; /* タッチ操作追加 */
  /* PC版の設定はそのまま保持 */
}
```

### 2. 優先修正事項
1. **PC版機能の完全復元**
2. **最小限のスワイプ機能追加**のみ実装
3. **要件定義準拠**の確認

---

## 🎯 次のステップ

### 即座に必要な作業
1. **現在のCSS全面見直し**：設計要件準拠への修正
2. **PC版機能復元確認**：自動幅調整・レイアウト等
3. **最小限実装**：スワイプ機能のみ追加

### 長期目標
1. 設計要件完全準拠の実装
2. PC版機能100%保持
3. モバイルでの快適なスワイプ操作

---

## 📝 変更履歴

- **v2.0** (2025-07-24): SPEC・REPORT統合、設計要件定義明確化
- **v1.0** (2025-07-18): Always-Visible Subslot System実装
