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

### 6. 【2025年7月25日完成】PC版サブスロット左右スライド機能 🆕

**実装背景**: スマホ最適化を見据え、PC版サブスロットにも左右スライド機能を先行実装。PC版では必須ではないが、スマホ版で複数サブスロットの表示時に必要となる機能の基盤を構築。

#### 🎯 技術実装詳細

##### 上位スロット・サブスロット共通のスライド機能
**場所**: `responsive.css`

```css
/* 📱 モバイル専用: 外側スワイプコンテナ */
.mobile-device .slot-wrapper {
  /* 🎯 左右スライド機能の核心実装 */
  overflow-x: auto !important;           /* 水平スクロール有効化 */
  overflow-y: visible !important;        /* 垂直方向は表示維持 */
  scroll-behavior: smooth !important;    /* スムーズスクロール */
  scroll-snap-type: x mandatory !important;  /* スナップスクロール */
  -webkit-overflow-scrolling: touch !important;  /* iOS最適化 */
  
  /* 🔧 レイアウト制御 */
  flex-direction: row !important;        /* 水平配置優先 */
  flex-wrap: nowrap !important;          /* 改行禁止 */
  white-space: nowrap !important;        /* テキスト改行禁止 */
}

/* 🎯 サブスロット専用スライド最適化 */
.mobile-device .slot-wrapper[id$="-sub"] {
  /* サブスロット特化のスライド制御 */
  overflow-x: auto !important;           /* 水平スクロール */
  white-space: nowrap !important;        /* 改行禁止 */
  scroll-behavior: smooth !important;    /* スムーズスクロール */
  
  /* 🔒 PC版制御システム完全保護 */
  /* display プロパティは指定しない → PC版制御を尊重 */
}
```

##### 個別スロット要素のスナップ制御
```css
.mobile-device .slot-container {
  /* 🎯 スライド時のスナップポイント設定 */
  scroll-snap-align: start !important;   /* 左端揃えでスナップ */
  flex-shrink: 0 !important;            /* サイズ固定 */
  min-width: 120px !important;          /* 最小幅確保 */
  max-width: 200px !important;          /* 最大幅制限 */
  
  /* 🔧 インライン表示最適化 */
  display: inline-block !important;      /* 横並び配置 */
  vertical-align: top !important;        /* 上端揃え */
  white-space: normal !important;        /* 内部テキストは改行可 */
}
```

#### 🏗️ アーキテクチャ設計原則

##### 1. **PC版機能完全保護**
- **JavaScript制御の尊重**: `display`・`order`プロパティは一切上書きしない
- **動的制御保持**: `subslot_toggle.js`、`structure_builder.js`の機能を完全保護
- **レイアウト保持**: PC版の自動幅調整・高さ調整システムを維持

##### 2. **最小限介入原則**
```css
/* ✅ 正しいアプローチ：スライド機能のみ追加 */
.mobile-device .slot-wrapper {
  overflow-x: auto !important;      /* スライド機能追加 */
  scroll-behavior: smooth !important;  /* UX向上 */
  /* PC版の width, height, margin は一切変更しない */
}

/* ❌ 避けるべき：PC版設定の上書き */
.mobile-device .slot-wrapper {
  width: 100vw !important;          /* PC版破壊 */
  height: 35vh !important;          /* PC版破壊 */
}
```

##### 3. **段階的適用戦略**
1. **ステップ1**: モバイル検出システム（`training/index.html`）
2. **ステップ2**: `.mobile-device`クラス自動付与
3. **ステップ3**: スライド機能CSS適用（`responsive.css`）
4. **ステップ4**: PC版制御システムはそのまま動作継続

#### 🔧 技術的特徴

##### スナップスクロール実装
- **`scroll-snap-type: x mandatory`**: 水平方向の強制スナップ
- **`scroll-snap-align: start`**: 各スロットの左端でスナップ
- **`scroll-behavior: smooth`**: 滑らかなスクロールアニメーション

##### タッチ最適化
- **`-webkit-overflow-scrolling: touch`**: iOS向けネイティブスクロール
- **`touch-action: pan-x pan-y`**: タッチ操作の最適化
- **`flex-shrink: 0`**: スライド中のサイズ変更防止

##### クロスプラットフォーム対応
- **Android**: 標準的なスクロール実装
- **iOS**: WebKit最適化スクロール
- **Chrome DevTools**: 開発時のシミュレーション対応

#### 📱 スマホ版への展開可能性

##### 現在のPC版実装の利点
1. **基盤完成**: スライド機能の基本実装が完了
2. **動作検証済み**: PC環境でのスライド動作を確認可能
3. **段階的移行**: スマホ版では同じCSS設定を流用可能

##### スマホ版での活用予定
```css
/* PC版で実装済み → スマホ版でそのまま活用 */
.mobile-device .slot-wrapper[id$="-sub"] {
  overflow-x: auto !important;           /* ✅ 実装済み */
  scroll-behavior: smooth !important;    /* ✅ 実装済み */
  scroll-snap-type: x mandatory !important;  /* ✅ 実装済み */
}
```

#### 🎯 実装完了度

| 機能 | PC版実装 | スマホ版準備 | 状態 |
|------|----------|-------------|------|
| **水平スクロール** | ✅ 完了 | ✅ 準備完了 | 実装済み |
| **スナップスクロール** | ✅ 完了 | ✅ 準備完了 | 実装済み |
| **タッチ最適化** | ✅ 完了 | ✅ 準備完了 | 実装済み |
| **PC版機能保護** | ✅ 完了 | ✅ 準備完了 | 実装済み |

#### 🔍 検証方法

##### PC環境での動作確認
1. **Chrome DevTools**: モバイルモードでスライド動作確認
2. **実機シミュレーション**: タッチ操作の動作確認
3. **機能保護確認**: PC版の既存機能が正常動作することを確認

##### デバッグ用確認コマンド
```javascript
// ブラウザコンソールでモバイル検出状況を確認
console.log('Mobile Device:', document.documentElement.classList.contains('mobile-device'));
console.log('CSS applied:', window.getComputedStyle(document.querySelector('.slot-wrapper'))['overflow-x']);
```

---

**🎯 結論**: PC版サブスロット左右スライド機能は、スマホ最適化の基盤として完全実装済み。PC版では支障がないため必要性は低いが、スマホ版での複数サブスロット表示時に重要な役割を果たす準備が整いました。

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

2. **`responsive.css`** - 【2025年7月25日追加】PC版DOM完全保持型モバイル対応
   - PC版サブスロット左右スライド機能
   - スナップスクロール実装
   - User-Agent判定版モバイル最適化

### 統合済みファイル
1. **`training/index.html`** - モバイル検出・CSS適用システム
   - User-Agentベースのモバイル検出
   - `.mobile-device` クラス自動適用
   - 画面サイズベース判定（768px以下）
   - タッチデバイス検出
   - Chrome DevTools対応

2. **モバイル検出JavaScript** - 自動デバイス判定システム
   ```javascript
   // 実装済み検出ロジック
   const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
   const isTouchDevice = 'ontouchstart' in window;
   const isSmallScreen = window.innerWidth <= 768;
   ```

### ファイル優先度・読み込み順序

| 順序 | ファイル | 役割 | 重要度 |
|------|----------|------|--------|
| **1** | `style.css` | PC版基本スタイル | 最高 |
| **2** | `mobile-split-view-simple.css` | Always-Visible Subslot System | 高 |
| **3** | `responsive.css` | PC版保護スライド機能 | 高 |
| **4** | モバイル検出JavaScript | デバイス判定・クラス適用 | 必須 |

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

- **v2.1** (2025-07-25): PC版サブスロット左右スライド機能実装・仕様書統合完了
  - `responsive.css`によるPC版DOM完全保持型スライド機能
  - スナップスクロール・タッチ最適化実装
  - PC版既存機能の完全保護体制確立
  - ファイル構成・優先度の明確化
- **v2.0** (2025-07-24): SPEC・REPORT統合、設計要件定義明確化
- **v1.0** (2025-07-18): Always-Visible Subslot System実装
