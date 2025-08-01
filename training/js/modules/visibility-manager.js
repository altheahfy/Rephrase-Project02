/**
 * Visibility Manager - RephraseStateManager統合版
 * Phase2リファクタリング: visibility_control.js の完全統合
 * 
 * 変更点:
 * - グローバル変数visibilityStateをRephraseStateManagerに統合
 * - localStorage管理をRephraseStateManagerに委譲
 * - 既存APIとの完全互換性維持
 */

class VisibilityManager {
  constructor() {
    // RephraseStateManagerインスタンスを取得
    this.stateManager = window.RephraseState;
    if (!this.stateManager) {
      throw new Error('[VisibilityManager] RephraseStateManagerが初期化されていません');
    }
    
    // スロット定義（既存コードと同一）
    this.ALL_SLOTS = ['s', 'aux', 'v', 'm1', 'm2', 'c1', 'o1', 'o2', 'c2', 'm3'];
    this.ELEMENT_TYPES = ['auxtext', 'text'];
    
    this.init();
  }
  
  /**
   * 初期化処理
   */
  init() {
    // 既存のグローバル変数との互換性チェック
    if (window.visibilityState) {
      console.log('[VisibilityManager] 既存のvisibilityStateを統合中...');
      this.migrateExistingState();
    } else {
      this.initializeVisibilityState();
    }
    
    // 既存の関数をグローバルに公開（完全互換性維持）
    this.setupGlobalCompatibility();
    
    console.log('[VisibilityManager] 初期化完了 - RephraseStateManager統合版');
  }
  
  /**
   * 既存グローバル変数の統合
   */
  migrateExistingState() {
    const existingState = window.visibilityState;
    
    this.ALL_SLOTS.forEach(slot => {
      this.ELEMENT_TYPES.forEach(type => {
        const existingValue = existingState[slot]?.[type];
        if (existingValue !== undefined) {
          this.stateManager.setState(`visibility.slots.${slot}.${type}`, existingValue, false);
        }
      });
    });
    
    console.log('[VisibilityManager] 既存状態を統合完了');
  }
  
  /**
   * 表示状態の初期化（既存ロジックと同一）
   */
  initializeVisibilityState() {
    this.ALL_SLOTS.forEach(slot => {
      this.ELEMENT_TYPES.forEach(type => {
        // 既存の状態がない場合のみ初期化（true = 表示）
        const currentValue = this.stateManager.getState(`visibility.slots.${slot}.${type}`);
        if (currentValue === undefined) {
          this.stateManager.setState(`visibility.slots.${slot}.${type}`, true, false);
        }
      });
    });
    
    console.log("[VisibilityManager] 表示状態を初期化しました");
  }
  
  /**
   * 個別スロット・要素の表示制御（既存APIと完全互換）
   * @param {string} slotKey - スロットキー
   * @param {string} elementType - 要素タイプ
   * @param {boolean} isVisible - 表示状態
   */
  toggleSlotElementVisibility(slotKey, elementType, isVisible) {
    if (!this.ALL_SLOTS.includes(slotKey)) {
      console.error(`❌ 無効なスロットキー: ${slotKey}`);
      return;
    }
    
    if (!this.ELEMENT_TYPES.includes(elementType)) {
      console.error(`❌ 無効な要素タイプ: ${elementType}`);
      return;
    }

    // RephraseStateManagerで状態更新（localStorage自動同期）
    this.stateManager.setState(`visibility.slots.${slotKey}.${elementType}`, isVisible);
    
    // DOM操作（既存ロジックと同一）
    this.updateDOMVisibility(slotKey, elementType, isVisible);
    
    console.log(`🔄 ${slotKey}スロットの${elementType}表示状態を${isVisible ? '表示' : '非表示'}に更新`);
  }
  
  /**
   * DOM要素の表示状態更新（既存ロジックから抽出）
   * @param {string} slotKey - スロットキー
   * @param {string} elementType - 要素タイプ
   * @param {boolean} isVisible - 表示状態
   */
  updateDOMVisibility(slotKey, elementType, isVisible) {
    // DOM要素を取得
    const slotElement = document.getElementById(`slot-${slotKey}`);
    const className = `hidden-${elementType}`;
    
    if (slotElement) {
      if (isVisible) {
        slotElement.classList.remove(className);
        console.log(`✅ ${slotKey}スロットの${elementType}を表示しました`);
      } else {
        slotElement.classList.add(className);
        console.log(`🙈 ${slotKey}スロットの${elementType}を非表示にしました`);
      }
      
      // 英語例文（text要素）の直接制御
      if (elementType === 'text') {
        const textElement = slotElement.querySelector('.slot-phrase');
        if (textElement) {
          if (isVisible) {
            textElement.style.opacity = '1';
            textElement.style.visibility = 'visible';
            console.log(`✅ ${slotKey}スロットの英語例文を表示しました`);
          } else {
            textElement.style.opacity = '0';
            textElement.style.visibility = 'hidden';
            console.log(`🙈 ${slotKey}スロットの英語例文を非表示にしました`);
          }
        }
      }
      
      // サブスロットも同様に制御
      const subSlots = document.querySelectorAll(`[id^="slot-${slotKey}-sub-"]`);
      subSlots.forEach(subSlot => {
        if (isVisible) {
          subSlot.classList.remove(className);
        } else {
          subSlot.classList.add(className);
        }
        
        // サブスロットの英語例文（text要素）も直接制御
        if (elementType === 'text') {
          const subTextElement = subSlot.querySelector('.slot-phrase');
          if (subTextElement) {
            if (isVisible) {
              subTextElement.style.opacity = '1';
              subTextElement.style.visibility = 'visible';
            } else {
              subTextElement.style.opacity = '0';
              subTextElement.style.visibility = 'hidden';
            }
          }
        }
      });
      
      console.log(`🔄 ${slotKey}スロットのサブスロット${subSlots.length}個も更新しました`);
    } else {
      console.warn(`⚠ スロット要素が見つかりません: slot-${slotKey}`);
    }
  }
  
  /**
   * 現在の表示状態をDOMに適用（既存ロジックと同一）
   */
  applyVisibilityState() {
    this.ALL_SLOTS.forEach(slotKey => {
      this.ELEMENT_TYPES.forEach(elementType => {
        const isVisible = this.stateManager.getState(`visibility.slots.${slotKey}.${elementType}`) ?? true;
        this.updateDOMVisibility(slotKey, elementType, isVisible);
      });
    });
    
    console.log("[VisibilityManager] DOM表示状態を適用完了");
  }
  
  /**
   * 表示状態の取得（既存APIとの互換性）
   * @param {string} slotKey - スロットキー
   * @param {string} elementType - 要素タイプ
   * @returns {boolean} 表示状態
   */
  getVisibilityState(slotKey, elementType) {
    return this.stateManager.getState(`visibility.slots.${slotKey}.${elementType}`) ?? true;
  }
  
  /**
   * 全スロットの一括表示制御
   * @param {string} elementType - 要素タイプ
   * @param {boolean} isVisible - 表示状態
   */
  toggleAllSlots(elementType, isVisible) {
    this.ALL_SLOTS.forEach(slotKey => {
      this.toggleSlotElementVisibility(slotKey, elementType, isVisible);
    });
    
    console.log(`🔄 全スロットの${elementType}を${isVisible ? '表示' : '非表示'}に設定`);
  }
  
  /**
   * 既存グローバル関数との完全互換性維持
   */
  setupGlobalCompatibility() {
    // 既存の関数をグローバルスコープに公開
    window.toggleSlotElementVisibility = (slotKey, elementType, isVisible) => {
      this.toggleSlotElementVisibility(slotKey, elementType, isVisible);
    };
    
    window.initializeVisibilityState = () => {
      this.initializeVisibilityState();
    };
    
    window.applyVisibilityState = () => {
      this.applyVisibilityState();
    };
    
    // 既存のlocalStorage関数は不要（RephraseStateManagerが自動処理）
    window.saveVisibilityState = () => {
      console.log('[VisibilityManager] saveVisibilityState呼び出し - RephraseStateManagerが自動保存済み');
    };
    
    window.loadVisibilityState = () => {
      console.log('[VisibilityManager] loadVisibilityState呼び出し - RephraseStateManagerが自動読み込み済み');
      this.applyVisibilityState();
    };
    
    // グローバル変数との互換性（getter/setterで動的参照）
    Object.defineProperty(window, 'visibilityState', {
      get: () => {
        // RephraseStateManagerから動的に構築
        const state = {};
        this.ALL_SLOTS.forEach(slot => {
          state[slot] = {};
          this.ELEMENT_TYPES.forEach(type => {
            state[slot][type] = this.stateManager.getState(`visibility.slots.${slot}.${type}`) ?? true;
          });
        });
        return state;
      },
      set: (newState) => {
        console.warn('[VisibilityManager] visibilityState直接設定は非推奨 - toggleSlotElementVisibilityを使用してください');
        // 互換性のため設定は受け入れる
        if (typeof newState === 'object') {
          Object.keys(newState).forEach(slot => {
            if (this.ALL_SLOTS.includes(slot)) {
              Object.keys(newState[slot]).forEach(type => {
                if (this.ELEMENT_TYPES.includes(type)) {
                  this.stateManager.setState(`visibility.slots.${slot}.${type}`, newState[slot][type]);
                }
              });
            }
          });
        }
      },
      configurable: true
    });
    
    console.log('[VisibilityManager] グローバル互換性API設定完了');
  }
}

// インスタンス作成とグローバル公開
window.VisibilityManager = new VisibilityManager();

console.log('[VisibilityManager] RephraseStateManager統合版初期化完了');
