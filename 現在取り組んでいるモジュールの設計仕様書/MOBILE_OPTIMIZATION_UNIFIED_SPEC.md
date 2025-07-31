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

### 2. スワイプエリア最適化【2025年7月25日調整】
- **上位スロットエリア**: 45vh（上位スロット重要性を反映した拡大）
- **サブスロットエリア**: 12vh（適切な補助表示サイズに縮小）
- **スワイプ操作**: 快適なタッチ操作を維持
- **バランス改善**: 上位スロットを主体とした適切な画面配分を実現

### 3. Transform Scale Content Optimization【2025年7月25日バランス調整】
- **上位スロット内容**: `transform: scale(0.8)` で80%縮小（重要性を反映）
- **サブスロット内容**: `transform: scale(0.55)` で55%縮小（補助表示に適切化）
- **重要**: スワイプエリア自体のサイズは維持、内部コンテンツのみ縮小
- **階層バランス**: 上位スロット > サブスロットの明確な視覚的階層を確立

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

## 🎯 【2025年7月28日更新】音声システム統合完了報告

### 完全分離型Android/PC音声認識システム実装完了 🎉

#### 🚀 重大な技術的進歩
- **プラットフォーム完全分離**: Android用 `this.recognition` と PC用 `recordingRecognition` の独立システム
- **設定完全分離**: `localStorage` キーに `_Android` / `_PC` サフィックス追加による独立管理
- **音声認識安定化**: PC版連続認識と Android版単発認識の最適化
- **発話時間計算精度向上**: タイムスタンプベース vs 推定時間計算の適切な使い分け

#### 📱 プラットフォーム別音声認識アーキテクチャ

##### Android システム
```javascript
// Android専用音声認識（this.recognition使用）
startAndroidVoiceRecognition() {
  this.recognition = new SpeechRecognition();
  this.recognition.continuous = false;  // 単発認識
  this.recognition.lang = this.getLocalStorageItem('speechLang_Android', 'en-US');
  // リトライ機能・透過化・専用設定管理
}
```

##### PC システム
```javascript
// PC専用音声認識（recordingRecognition使用）
async initPCSpeechRecognition() {
  this.recordingRecognition = new SpeechRecognition();
  this.recordingRecognition.continuous = true;  // 連続認識
  this.recordingRecognition.lang = this.getLocalStorageItem('speechLang_PC', 'en-US');
  // 累積テキスト処理・PC専用最適化
}
```

#### 🔧 設定管理の完全分離
```javascript
// プラットフォーム別独立設定
getLocalStorageItem(key, defaultValue) {
  const platformKey = this.isAndroid ? `${key}_Android` : `${key}_PC`;
  return localStorage.getItem(platformKey) || defaultValue;
}

setLocalStorageItem(key, value) {
  const platformKey = this.isAndroid ? `${key}_Android` : `${key}_PC`;
  localStorage.setItem(platformKey, value);
}
```

#### 🎯 発話時間計算システムの精密化

##### Android: タイムスタンプベース計算
```javascript
// 実際の発話タイミングを正確に計測
finishAndroidVoiceRecognition() {
  // speechTimestamps配列から無音期間を除外した実発話時間を計算
  let adjustedSpeechTime = 0;
  for (let i = 1; i < this.speechTimestamps.length; i++) {
    const gap = this.speechTimestamps[i] - this.speechTimestamps[i - 1];
    const adjustedGap = gap > 1.5 ? 0.3 : gap; // 長い無音は0.3秒に正規化
    adjustedSpeechTime += adjustedGap;
  }
}
```

##### PC: 推定時間計算
```javascript
// 文字数ベースの推定計算（連続認識対応）
const estimatedSpeechDuration = recognizedText ? recognizedText.split(/\s+/).length * 0.6 : 1;
```

#### 🛡️ 認識システムの安定性向上

##### 重複検出・除去システム
```javascript
// サブスロット展開時の重複を高精度で検出・除去
isDuplicateText(newText, existingTexts) {
  return existingTexts.some(existing => {
    const similarity = this.calculateTextSimilarity(newText, existing);
    return similarity > 0.8; // 80%以上の類似度で重複と判定
  });
}
```

##### プラットフォーム別エラーハンドリング
- **Android**: 認識失敗時の自動リトライ、透過化復旧
- **PC**: 連続認識の安定性管理、録音終了時処理

### 🎉 現在の実装完成度

| 機能領域 | Android | PC | 統合度 |
|---------|---------|----|----|
| **音声認識** | ✅ 完成 | ✅ 完成 | 完全分離 |
| **設定管理** | ✅ 完成 | ✅ 完成 | 独立システム |
| **発話時間計算** | ✅ 完成 | ✅ 完成 | 高精度実装 |
| **エラーハンドリング** | ✅ 完成 | ✅ 完成 | プラットフォーム最適化 |
| **UI統合** | ✅ 完成 | ✅ 完成 | 透過的操作 |

### モバイル最適化への統合効果

#### 音声システムとモバイルUIの相乗効果
1. **プラットフォーム検出の一元化**: モバイル検出システムと音声システムの連携
2. **透過化パネルシステム**: 音声認識中のUI透過とモバイルタッチ操作の両立
3. **設定管理の統一**: モバイル/PC設定とAndroid/PC音声設定の協調

#### 次期統合予定項目
1. **音声パネルのモバイル最適化**: Always-Visible Subslot Systemとの統合
2. **タッチジェスチャーとの協調**: スワイプ操作と音声操作の両立
3. **設定UI統合**: モバイル向け音声設定パネルの実装

---

## 🔍 【2025年7月26日発見】重要な技術的知見・デバッグ手法

### 横向きモード上部スワイプエリア拡張の技術的課題と解決

#### 🚨 発見した根本問題：**外側容器制約の見落とし**

##### 問題の症状
- 上部スワイプエリア（`.slot-wrapper`）の`width: 120vw`設定が無効
- いくら内側要素の幅を拡張しても1mmも変化しない
- CSS設定は正しいが視覚的効果が全く現れない

##### 根本原因の発見
```css
/* 🚨 問題の構造 */
.mobile-device body {
  zoom: 0.7 !important; /* 70%に縮小された外側容器 */
  /* width指定なし → デフォルト100vw */
}

.mobile-device .slot-wrapper:not([id$="-sub"]) {
  width: 120vw !important; /* 内側で120%指定しても... */
  /* ↑ 親容器が100vwなので、実質的に100vw以下に制限される */
}
```

#### 🎯 解決アプローチ：**階層的幅制御**

##### 正しい実装手順
1. **外側容器（body）の拡張**
2. **内側要素（slot-wrapper）の拡張**
3. **両方の連携による効果実現**

```css
/* ✅ 解決策：外側と内側の連携拡張 */
@media screen and (orientation: landscape) {
  /* 🎯 ステップ1: 外側容器を拡張 */
  .mobile-device body {
    zoom: 0.7 !important;
    width: 140vw !important; /* 外側容器を140%に拡張 */
    overflow-x: auto !important; /* 横スクロール有効 */
  }
  
  /* 🎯 ステップ2: 内側要素も拡張 */
  .mobile-device .slot-wrapper:not([id$="-sub"]) {
    width: 140vw !important; /* 内側も140%に拡張 */
    min-width: 140vw !important;
    max-width: 140vw !important;
  }
}
```

#### 📚 学んだデバッグ手法

##### 1. **階層構造の見極め**
- 単一要素の問題と思い込まず、**親子関係の制約**を疑う
- `Developer Tools`でDOM階層を確認し、制約元を特定

##### 2. **段階的検証アプローチ**
```css
/* デバッグ用：段階的に幅を確認 */
.mobile-device body { background: red; } /* 外側容器の範囲確認 */
.mobile-device .slot-wrapper { background: blue; } /* 内側要素の範囲確認 */
```

##### 3. **仮説検証の重要性**
- **仮説**: 「上部スワイプエリアを包んでいるさらなる入れ物があるのでは？」
- **検証**: DOM構造とCSS階層の詳細調査
- **発見**: `body`要素の幅制約が真の原因

#### 🏗️ アーキテクチャ設計への影響

##### 新しい設計原則：**外側制約優先の法則**
1. **外側から内側へ**: 制約は外側容器から順番に解除する
2. **階層的デバッグ**: 問題は最も外側の容器から疑う
3. **連携設計**: 幅拡張は全階層で連携して設定する

#### 🔧 実装完了後の技術仕様

##### 横向きモード専用拡張システム
```css
/* 🎯 完成形：140%横幅拡張システム */
@media screen and (orientation: landscape) {
  .mobile-device body {
    zoom: 0.7 !important;
    width: 140vw !important; /* 画面幅の140% */
    overflow-x: auto !important;
  }
  
  .mobile-device .slot-wrapper:not([id$="-sub"]) {
    height: 100vh !important;
    width: 140vw !important; /* bodyと連携した140% */
    min-width: 140vw !important;
    max-width: 140vw !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    touch-action: pan-x manipulation !important;
    margin: 0 !important;
    padding-top: 8px !important;
  }
}
```

##### 効果と利点
- **横向きモード**: 上部スワイプエリアが画面幅の140%に拡張
- **横スクロール**: 拡張部分へのスムーズなナビゲーション
- **PC版保護**: 既存機能を完全保持
- **段階的調整**: 120% → 140%のような柔軟な調整が可能

#### 🎓 今後のデバッグ指針

##### CSS幅問題のチェックリスト
1. **親容器の制約確認**: `body`, `section`, `main`等の外側要素
2. **CSS継承確認**: `width`, `max-width`, `overflow`プロパティの継承
3. **メディアクエリ優先度**: `@media`ルールの適用順序
4. **!important競合**: 複数の`!important`宣言の衝突

##### 効率的デバッグ手順
1. **最外側から調査**: `body` → `section` → `div` → `.slot-wrapper`
2. **視覚的境界確認**: `background`色でエリア範囲を明確化
3. **段階的変更**: 一つずつ要素を変更して効果を確認
4. **仮説駆動**: 「なぜ効果がないのか」の仮説を立てて検証

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

- **v2.3** (2025-07-28): **音声システム統合完了** 🎉
  - **プラットフォーム完全分離**: Android/PC音声認識システムの独立実装完了
  - **設定管理統合**: localStorage分離管理（_Android/_PCサフィックス）
  - **発話時間計算精密化**: タイムスタンプベース vs 推定計算の適切な使い分け
  - **認識システム安定化**: 重複検出・除去、プラットフォーム別エラーハンドリング実装
  - **モバイル最適化統合**: 音声システムとモバイルUIの相乗効果実現
- **v2.2** (2025-07-26): **横向きモード上部スワイプエリア140%拡張完成** 🎉
  - **重要発見**: 外側容器制約の技術的課題と解決手法を文書化
  - **階層的幅制御**: body(140vw) + slot-wrapper(140vw) の連携拡張システム実装
  - **デバッグ手法確立**: 外側制約優先の法則、段階的検証アプローチ
  - **技術仕様完成**: 横向きモード専用140%拡張システムの完全実装
  - **レイアウト最適化完了**: スマホ最適化のレイアウト面が完成段階に到達
- **v2.1** (2025-07-25): PC版サブスロット左右スライド機能実装・仕様書統合完了
  - `responsive.css`によるPC版DOM完全保持型スライド機能
  - スナップスクロール・タッチ最適化実装
  - PC版既存機能の完全保護体制確立
  - ファイル構成・優先度の明確化
- **v2.0** (2025-07-24): SPEC・REPORT統合、設計要件定義明確化
- **v1.0** (2025-07-18): Always-Visible Subslot System実装
