# Rephraseアプリケーション リファクタリング設計仕様書

## 1. プロジェクト概要

### 1.1 現状認識
- **教育的価値**: パターンプラクティスのデジタル化による語学教育の革新
- **技術的課題**: 継ぎ接ぎ開発による技術債務の蓄積
- **商用化目標**: スマホ最適化完了後の商用展開

### 1.2 リファクタリング目標
- 機能を維持しながらコード品質を向上
- 保守性・拡張性の確保
- パフォーマンス最適化

## 2. 現状分析と問題特定

### 2.1 主要問題領域
```
Priority 1: CSS混沌 (2000行超、!important乱用)
Priority 2: JavaScript状態管理分散
Priority 3: ファイル構造の無秩序
Priority 4: 命名規則不統一
```

### 2.2 技術債務マップ
```
高リスク：
- mobile-split-view-simple.css (複雑な条件分岐)
- visibility_control.js (状態管理分散)
- index.html (HTMLとCSSの混在)

中リスク：
- subslot_visibility_control.js (重複ロジック)
- style.css (スタイル定義の重複)
```

## 3. 段階的リファクタリング戦略

### 3.1 フェーズ1: CSS整理統合 (期間: 1-2週間)

#### 3.1.1 CSS分割戦略
```css
/* 新しいファイル構造 */
styles/
├── base.css          /* リセット、基本設定 */
├── layout.css        /* レイアウト、グリッド */
├── components.css    /* ボタン、パネル等 */
├── slots.css         /* スロット専用スタイル */
├── responsive.css    /* レスポンシブ設定 */
└── themes.css        /* 色彩、テーマ設定 */
```

#### 3.1.2 重要度削減戦略
```css
/* !important削除ルール */
1. 詳細度を正しく設定してimportant削除
2. カスケード順序の見直し
3. CSS変数による統一的管理

/* 例: Before */
.slot-control-group label {
  background: #e8f5e8 !important;
}

/* 例: After */
:root {
  --control-bg-active: #e8f5e8;
}
.visibility-panel .slot-control-group label.active {
  background: var(--control-bg-active);
}
```

#### 3.1.3 レスポンシブ統合
```css
/* モバイル・PC統合方針 */
/* 基本: モバイルファースト */
.slot-wrapper {
  /* モバイル基本設定 */
}

@media (min-width: 768px) {
  .slot-wrapper {
    /* PC拡張設定 */
  }
}

/* デバイス判定クラス廃止 */
/* .mobile-device プレフィックス → メディアクエリに統合 */
```

### 3.2 フェーズ2: JavaScript状態管理統合 (期間: 2-3週間)

#### 3.2.1 状態管理一元化
```javascript
// 新しい状態管理構造
class RephraseStateManager {
  constructor() {
    this.state = {
      visibility: {},      // 表示状態管理
      audio: {},          // 音声関連状態
      ui: {},             // UI状態
      slots: {}           // スロットデータ
    };
    this.listeners = [];  // 状態変更リスナー
  }
  
  // 状態更新
  setState(path, value) {
    // 深いオブジェクト更新
    // localStorage自動同期
    // リスナー通知
  }
  
  // 状態取得
  getState(path) {
    // 深いオブジェクト取得
  }
}

// グローバル状態管理インスタンス
window.RephraseState = new RephraseStateManager();
```

#### 3.2.2 モジュール分割戦略
```javascript
// ファイル構造
js/
├── core/
│   ├── state-manager.js    /* 状態管理 */
│   ├── event-manager.js    /* イベント管理 */
│   └── config.js          /* 設定定数 */
├── modules/
│   ├── visibility.js      /* 表示制御 */
│   ├── audio.js           /* 音声機能 */
│   ├── slots.js           /* スロット管理 */
│   └── ui-controls.js     /* UI制御 */
└── main.js                /* メインエントリ */
```

#### 3.2.3 命名規則統一
```javascript
// 統一命名規則
const NAMING_CONVENTIONS = {
  // 定数: UPPER_SNAKE_CASE
  SLOT_TYPES: ['s', 'aux', 'v', 'm1', 'm2', 'c1', 'o1', 'o2', 'c2', 'm3'],
  
  // 関数: camelCase (動詞から開始)
  toggleSlotVisibility: function() {},
  updateAudioState: function() {},
  
  // クラス: PascalCase
  SlotController: class {},
  AudioManager: class {},
  
  // DOM要素: kebab-case
  'slot-wrapper', 'visibility-control-panel'
};
```

### 3.3 フェーズ3: コンポーネント化 (期間: 2-3週間)

#### 3.3.1 共通コンポーネント抽出
```javascript
// スロット制御パネルの統一
class ControlPanel {
  constructor(options) {
    this.slotId = options.slotId;
    this.elementTypes = options.elementTypes;
    this.isSubslot = options.isSubslot || false;
  }
  
  render() {
    // 統一されたパネルHTML生成
    // サブスロットと上位スロットで共通ロジック
  }
  
  bindEvents() {
    // イベントハンドラーの統一
  }
}
```

#### 3.3.2 設定外部化
```javascript
// config/app-config.js
export const APP_CONFIG = {
  SLOTS: {
    TYPES: ['s', 'aux', 'v', 'm1', 'm2', 'c1', 'o1', 'o2', 'c2', 'm3'],
    ELEMENT_TYPES: ['auxtext', 'text'],
    COLORS: {
      S: '#4CAF50',
      V: '#2196F3',
      O: '#FF9800',
      // ...
    }
  },
  
  UI: {
    MOBILE_BREAKPOINT: 768,
    ANIMATION_DURATION: 200,
    CONTROL_PANEL: {
      PADDING: '4px',
      BORDER_RADIUS: '3px',
      ACTIVE_COLOR: '#e8f5e8'
    }
  },
  
  AUDIO: {
    SUPPORTED_FORMATS: ['mp3', 'wav'],
    DEFAULT_VOLUME: 0.8
  }
};
```

## 4. 実装ガイドライン

### 4.1 安全なリファクタリング手順
```bash
# 1. バックアップ作成
git branch backup-before-refactor

# 2. 小さな単位でのコミット
git commit -m "CSS: Extract slot styles to slots.css"

# 3. 機能テスト後のマージ
# 各フェーズ完了時に動作確認

# 4. ロールバック準備
# 問題発生時はいつでも戻せる状態を維持
```

### 4.2 テスト戦略
```javascript
// 基本機能テストリスト
const CORE_FUNCTIONS = [
  'スロット表示・非表示制御',
  'サブスロット切り替え',
  '音声再生',
  'ランダマイズ機能',
  'モバイル・PC表示切替'
];

// 各リファクタリング後にこれらの動作確認を実施
```

### 4.3 パフォーマンス指標
```javascript
// 改善目標
const PERFORMANCE_TARGETS = {
  CSS_SIZE: 'current 2000+ lines → target <1000 lines',
  JS_EXECUTION: 'DOM操作の最適化',
  MOBILE_RESPONSIVENESS: '60fps維持',
  LOAD_TIME: '初期表示3秒以内'
};
```

## 5. 商用化準備項目

### 5.1 コード品質チェックリスト
- [ ] CSS !important削除率 > 90%
- [ ] JavaScript重複コード削除
- [ ] 命名規則統一完了
- [ ] モバイル最適化完了
- [ ] エラーハンドリング強化

### 5.2 ドキュメント整備
- [ ] API仕様書作成
- [ ] 設定変更マニュアル
- [ ] デプロイメント手順書
- [ ] 保守・運用ガイド

### 5.3 商用展開考慮事項
- スケーラビリティ設計
- セキュリティ強化
- ログ・監視システム
- ユーザーデータ管理

## 6. リスク管理

### 6.1 技術的リスク
- **機能破綻リスク**: 段階的実装とテストで軽減
- **互換性問題**: ブラウザテスト強化
- **パフォーマンス劣化**: 最適化と計測の並行実施

### 6.2 スケジュールリスク
- **想定外の複雑性**: バッファ時間確保
- **テスト時間不足**: 自動テスト導入検討

## 7. 追加考慮事項

### 7.1 教育効果最大化
- **学習者体験の向上**: UIの直感性向上
- **学習進捗管理**: 進捗追跡機能の強化
- **個人化対応**: 学習者レベル別カスタマイズ

### 7.2 技術的拡張性
- **多言語対応**: 国際化対応の基盤整備
- **モバイルアプリ化**: PWA対応の検討
- **AI機能統合**: 自動構文分析機能の追加検討

---

この設計仕様書に基づいて、段階的かつ安全にリファクタリングを進めることで、商用化に向けた堅牢なアプリケーションに改善できます。
