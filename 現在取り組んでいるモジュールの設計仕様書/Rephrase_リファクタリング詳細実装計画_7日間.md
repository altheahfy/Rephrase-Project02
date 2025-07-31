# Rephraseアプリケーション リファクタリング詳細実装計画
## 🚀 7日間高速完了プラン (1日10時間集中作業)

### 📊 全体概要
- **総作業時間**: 70時間 (1日10時間 × 7日)
- **現在進捗**: フェーズ1 30%完了 (CSS変数化 Phase2完了)
- **目標**: 全3フェーズ完了 + 商用化準備
- **品質方針**: 機能保持 + 段階的テスト + 即座ロールバック対応

---

## 📅 日別詳細作業計画

### **【1日目】フェーズ1完了 - CSS整理統合 (10時間)**

#### **午前 (5時間): CSS変数化完了**
- **Phase 3: 高さ・幅値変数化** (2時間)
- **Phase 4: カラー値変数化** (2時間)  
- **Phase 5: アニメーション値変数化** (1時間)

#### **午後 (5時間): !important削除**
- **mobile-split-view-simple.css !important削除** (3時間)
- **style.css !important削除** (2時間)

### **【2日目】CSS分割・統合 (10時間)**

#### **午前 (5時間): ファイル構造設計**
- **新ファイル構造作成** (2時間)
- **既存CSS分析・分割準備** (3時間)

#### **午後 (5時間): CSS分割実行**
- **base.css, layout.css作成** (2時間)
- **components.css, slots.css作成** (3時間)

### **【3-4日目】フェーズ2 - JavaScript状態管理統合 (20時間)**

#### **3日目: 状態管理基盤構築** (10時間)
- **RephraseStateManager設計・実装** (6時間)
- **既存状態管理分析** (4時間)

#### **4日目: モジュール分割・統合** (10時間)
- **core/modules分離** (6時間)
- **命名規則統一・テスト** (4時間)

### **【5-6日目】フェーズ3 - コンポーネント化 (20時間)**

#### **5日目: 共通コンポーネント抽出** (10時間)
- **ControlPanel統一化** (6時間)
- **SlotRenderer統一化** (4時間)

#### **6日目: 設定外部化・統合** (10時間)
- **config外部化** (4時間)
- **全体統合テスト** (6時間)

### **【7日目】商用化準備・最終調整 (10時間)**

#### **午前 (5時間): 品質確保**
- **パフォーマンス最適化** (3時間)
- **セキュリティ強化** (2時間)

#### **午後 (5時間): 完成化**
- **ドキュメント整備** (2時間)
- **最終テスト・デプロイ準備** (3時間)

---

## 🎯 詳細実装仕様

### **CSS変数化完全ロードマップ**

#### **Phase 3: 高さ・幅値変数化** (2時間)
```css
/* 新規追加変数 */
:root {
  /* 高さ系 */
  --mobile-height-small: 12px;
  --mobile-height-medium: 16px;
  --mobile-height-large: 20px;
  --mobile-height-control: 22px;
  
  /* 幅系 */
  --mobile-width-small: 40px;
  --mobile-width-medium: 60px;
  --mobile-width-button: 15px;
}
```

**置換対象箇所** (約15箇所):
- `height: 16px` → `height: var(--mobile-height-medium)`
- `height: 20px` → `height: var(--mobile-height-large)`
- `width: 40px` → `width: var(--mobile-width-small)`
- `width: 60px` → `width: var(--mobile-width-medium)`

#### **Phase 4: カラー値変数化** (2時間)
```css
/* カラーシステム変数 */
:root {
  /* プライマリカラー */
  --mobile-color-primary: #007bff;
  --mobile-color-secondary: #28a745;
  --mobile-color-accent: #ff9800;
  
  /* 背景系 */
  --mobile-bg-primary: rgba(240, 248, 255, 0.9);
  --mobile-bg-secondary: rgba(248, 255, 248, 0.9);
  --mobile-bg-control: #e8f5e8;
  
  /* ボーダー系 */
  --mobile-border-primary: #4CAF50;
  --mobile-border-secondary: #f44336;
}
```

**置換対象箇所** (約25箇所):
- `background: rgba(240, 248, 255, 0.9)` → `background: var(--mobile-bg-primary)`
- `border-color: #4CAF50` → `border-color: var(--mobile-border-primary)`

#### **Phase 5: アニメーション値変数化** (1時間)
```css
/* アニメーション・トランジション変数 */
:root {
  --mobile-transition-fast: 0.2s;
  --mobile-transition-normal: 0.3s;
  --mobile-animation-duration: 1.5s;
}
```

### **!important削除戦略**

#### **削除対象分析** (mobile-split-view-simple.css):
```
現在の!important数: 約180箇所
削除可能: 約150箇所 (83%)
詳細度調整必要: 約30箇所
```

**削除手順**:
1. **セレクタ詳細度計算**: `.mobile-device`プレフィックス活用
2. **カスケード順序調整**: CSS読み込み順序最適化
3. **変数置換連携**: 変数化と同時に!important削除

### **CSS分割詳細設計**

#### **新ファイル構造**:
```
styles/
├── base.css (300行)          /* リセット、CSS変数、基本設定 */
├── layout.css (400行)        /* レイアウト、グリッド、フレックス */
├── components.css (500行)    /* ボタン、パネル、制御要素 */
├── slots.css (600行)         /* スロット専用スタイル */
├── mobile.css (400行)        /* モバイル専用スタイル */
└── animations.css (100行)    /* アニメーション、トランジション */
```

#### **分割マッピング**:
```css
/* base.css */
- CSS変数定義 (全Phase)
- リセットCSS
- 基本フォント・カラー設定

/* layout.css */
- .slot-wrapper レイアウト
- グリッド・フレックス定義
- レスポンシブ基本構造

/* components.css */
- ボタンスタイル
- 制御パネルスタイル
- ナビゲーション要素

/* slots.css */
- スロット表示システム
- サブスロット制御
- 画像表示システム

/* mobile.css */
- .mobile-device 専用スタイル
- モバイル最適化
- タッチ操作対応

/* animations.css */
- トランジション定義
- キーフレームアニメーション
- ホバー効果
```

### **JavaScript状態管理詳細設計**

#### **RephraseStateManager API仕様**:
```javascript
class RephraseStateManager {
  constructor() {
    this.state = {
      visibility: {
        slots: {},      // スロット表示状態
        subslots: {},   // サブスロット表示状態
        panels: {}      // パネル表示状態
      },
      audio: {
        currentTrack: null,
        volume: 0.8,
        isPlaying: false
      },
      ui: {
        activeSlot: null,
        zoom: 1.0,
        theme: 'default'
      },
      slots: {
        data: {},       // スロットデータ
        randomState: {} // ランダム化状態
      }
    };
    this.listeners = new Map();
    this.history = [];
  }

  // 状態更新 (深いオブジェクト対応)
  setState(path, value, options = {}) {
    const oldValue = this.getState(path);
    this._setDeepPath(this.state, path, value);
    
    if (!options.silent) {
      this._notifyListeners(path, value, oldValue);
    }
    
    if (options.persist) {
      this._saveToLocalStorage();
    }
    
    this._addHistory(path, oldValue, value);
  }

  // 状態取得
  getState(path) {
    return this._getDeepPath(this.state, path);
  }

  // リスナー登録
  subscribe(path, callback) {
    if (!this.listeners.has(path)) {
      this.listeners.set(path, new Set());
    }
    this.listeners.get(path).add(callback);
    
    return () => this.listeners.get(path).delete(callback);
  }

  // 状態リセット
  reset(preserve = []) {
    // preserve配列のパス以外をリセット
  }

  // 履歴機能
  undo() {
    // 最後の変更を取り消し
  }
}
```

#### **モジュール分割構造**:
```
js/
├── core/
│   ├── state-manager.js      /* RephraseStateManager */
│   ├── event-manager.js      /* イベント統合管理 */
│   ├── config.js            /* 設定定数 */
│   └── utils.js             /* 共通ユーティリティ */
├── modules/
│   ├── visibility/
│   │   ├── slot-visibility.js      /* スロット表示制御 */
│   │   ├── subslot-visibility.js   /* サブスロット表示制御 */
│   │   └── panel-visibility.js     /* パネル表示制御 */
│   ├── audio/
│   │   ├── audio-manager.js        /* 音声機能統合 */
│   │   └── voice-controls.js       /* 音声制御UI */
│   ├── slots/
│   │   ├── slot-manager.js         /* スロット管理 */
│   │   ├── randomizer.js           /* ランダム化機能 */
│   │   └── renderer.js             /* 描画機能 */
│   └── ui/
│       ├── controls.js             /* UI制御 */
│       ├── navigation.js           /* ナビゲーション */
│       └── responsive.js           /* レスポンシブ対応 */
└── main.js                         /* メインエントリーポイント */
```

#### **既存ファイル移行計画**:
```
visibility_control.js → modules/visibility/slot-visibility.js
subslot_visibility_control.js → modules/visibility/subslot-visibility.js
universal_image_system.js → modules/slots/renderer.js
randomizer_*.js → modules/slots/randomizer.js
```

### **コンポーネント化詳細設計**

#### **ControlPanel統一化**:
```javascript
class UnifiedControlPanel {
  constructor(options) {
    this.slotId = options.slotId;
    this.elementTypes = options.elementTypes || ['auxtext', 'text'];
    this.isSubslot = options.isSubslot || false;
    this.state = window.RephraseState;
  }

  render() {
    return `
      <div class="control-panel ${this.isSubslot ? 'subslot' : 'main'}-panel">
        <div class="panel-header">
          <span class="panel-title">${this.getTitle()}</span>
          <button class="panel-toggle">▼</button>
        </div>
        <div class="panel-content">
          ${this.renderControls()}
        </div>
      </div>
    `;
  }

  renderControls() {
    return this.elementTypes.map(type => 
      this.renderElementControl(type)
    ).join('');
  }

  renderElementControl(elementType) {
    const isVisible = this.state.getState(
      `visibility.${this.isSubslot ? 'subslots' : 'slots'}.${this.slotId}.${elementType}`
    );
    
    return `
      <label class="control-item ${isVisible ? 'active' : 'inactive'}">
        <input type="checkbox" ${isVisible ? 'checked' : ''} 
               data-slot="${this.slotId}" 
               data-element="${elementType}">
        <span class="control-label">${this.getElementLabel(elementType)}</span>
      </label>
    `;
  }

  bindEvents() {
    // 統一されたイベントハンドリング
    this.element.addEventListener('change', this.handleToggle.bind(this));
  }

  handleToggle(event) {
    if (event.target.matches('input[type="checkbox"]')) {
      const { slot, element } = event.target.dataset;
      const isChecked = event.target.checked;
      
      this.state.setState(
        `visibility.${this.isSubslot ? 'subslots' : 'slots'}.${slot}.${element}`,
        isChecked,
        { persist: true }
      );
    }
  }
}
```

### **設定外部化詳細**:
```javascript
// config/app-config.js
export const APP_CONFIG = {
  SLOTS: {
    TYPES: ['s', 'aux', 'v', 'm1', 'm2', 'c1', 'o1', 'o2', 'c2', 'm3'],
    ELEMENT_TYPES: {
      DEFAULT: ['auxtext', 'text'],
      EXTENDED: ['auxtext', 'text', 'image', 'audio']
    },
    COLORS: {
      S: { primary: '#4CAF50', secondary: '#e8f5e8' },
      V: { primary: '#2196F3', secondary: '#e3f2fd' },
      O: { primary: '#FF9800', secondary: '#fff3e0' },
      M: { primary: '#9C27B0', secondary: '#f3e5f5' },
      C: { primary: '#607D8B', secondary: '#eceff1' },
      AUX: { primary: '#795548', secondary: '#efebe9' }
    }
  },
  
  UI: {
    MOBILE_BREAKPOINT: 768,
    ANIMATION_DURATION: 200,
    DEBOUNCE_DELAY: 300,
    CONTROL_PANEL: {
      PADDING: 'var(--mobile-padding-medium)',
      BORDER_RADIUS: 'var(--mobile-border-radius)',
      ACTIVE_COLOR: 'var(--mobile-bg-control)'
    }
  },
  
  AUDIO: {
    SUPPORTED_FORMATS: ['mp3', 'wav', 'ogg'],
    DEFAULT_VOLUME: 0.8,
    PRELOAD: 'metadata'
  },
  
  PERFORMANCE: {
    IMAGE_LAZY_LOADING: true,
    VIRTUAL_SCROLLING: false,
    CHUNK_SIZE: 50
  }
};
```

---

## 🔧 品質保証・テスト戦略

### **段階的テスト項目**:
```
□ CSS変数化テスト (各Phase後)
  - 視覚的変化なし確認
  - 全デバイス表示確認
  - 変数値変更でのスタイル反映確認

□ JavaScript統合テスト
  - 既存機能完全動作確認
  - 状態管理正常動作確認
  - エラーハンドリング確認

□ パフォーマンステスト
  - ページ読み込み時間
  - メモリ使用量
  - CPU使用率

□ 商用化品質確認
  - セキュリティ脆弱性チェック
  - アクセシビリティ確認
  - SEO最適化確認
```

### **リスク対応戦略**:
```
High: 機能破綻 → 即座ロールバック (git stash/reset)
Medium: パフォーマンス劣化 → 最適化調整
Low: 視覚的微調整 → 後回し対応可能
```

---

## 📈 成果指標

### **定量的目標**:
- **CSS行数**: 2000+ → 1200行 (40%削減)
- **!important使用**: 180+ → 20個 (90%削減)  
- **ファイル数**: 統合済み構造
- **JavaScript重複**: 統合によるDRY化
- **ページ読み込み**: 3秒以内維持

### **定性的目標**:
- **保守性**: 変更容易性向上
- **拡張性**: 新機能追加容易性
- **可読性**: コード理解容易性
- **商用化準備**: 品質基準達成

---

この詳細計画により、7日間で確実にリファクタリング完了できます。開始しますか？
