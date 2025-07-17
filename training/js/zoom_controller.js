/**
 * 手動ズーム・縮小機構
 * スピーキング練習時の視認性向上のため、スロット空間全体を縦横比を保ったまま縮小
 * 
 * 機能:
 * - スライダーによるリアルタイムズーム調整（50% - 150%）
 * - 上位スロット・サブスロット全体に適用
 * - 縦横比保持（transform: scale）
 * - 設定の永続化（localStorage）
 * - リセット機能
 */

class ZoomController {
  constructor() {
    this.zoomSlider = null;
    this.zoomValue = null;
    this.zoomResetButton = null;
    this.targetContainers = []; // ズーム対象のコンテナ
    this.currentZoom = 1.0;
    this.storageKey = 'rephrase_zoom_level';
    
    this.init();
  }

  init() {
    // DOM要素の取得
    this.zoomSlider = document.getElementById('zoomSlider');
    this.zoomValue = document.getElementById('zoomValue');
    this.zoomResetButton = document.getElementById('zoomResetButton');
    
    if (!this.zoomSlider || !this.zoomValue || !this.zoomResetButton) {
      console.warn('⚠️ ズームコントロール要素が見つかりません');
      return;
    }

    // ズーム対象コンテナの特定
    this.identifyTargetContainers();
    
    // 保存されたズーム値を読み込み
    this.loadZoomLevel();
    
    // イベントリスナーの設定
    this.setupEventListeners();
    
    // スクロールヒント要素を作成
    this.createScrollHint();
    
    console.log('🔍 ズームコントローラーが初期化されました');
  }

  /**
   * ズーム対象となるコンテナを特定
   * 上位スロット・サブスロット全体を含む領域
   */
  identifyTargetContainers() {
    // メインスロットエリア（上位スロット群）
    const mainSlotWrapper = document.querySelector('.slot-wrapper');
    if (mainSlotWrapper) {
      this.targetContainers.push({
        element: mainSlotWrapper,
        type: 'main',
        id: 'main-slots'
      });
    }

    // サブスロットエリア群
    const subSlotWrappers = document.querySelectorAll('.slot-wrapper[id$="-sub"]');
    subSlotWrappers.forEach((wrapper, index) => {
      this.targetContainers.push({
        element: wrapper,
        type: 'sub',
        id: wrapper.id || `sub-slots-${index}`
      });
    });

    console.log(`🎯 ズーム対象コンテナ: ${this.targetContainers.length}個を特定`);
  }

  /**
   * イベントリスナーの設定
   */
  setupEventListeners() {
    // スライダー変更時のリアルタイムズーム
    this.zoomSlider.addEventListener('input', (e) => {
      const zoomLevel = parseFloat(e.target.value);
      this.applyZoom(zoomLevel);
      this.updateZoomDisplay(zoomLevel);
    });

    // スライダー操作完了時の保存
    this.zoomSlider.addEventListener('change', (e) => {
      const zoomLevel = parseFloat(e.target.value);
      this.saveZoomLevel(zoomLevel);
    });

    // リセットボタン
    this.zoomResetButton.addEventListener('click', () => {
      this.resetZoom();
    });

    // サブスロット展開時の動的対応
    this.setupDynamicSubslotObserver();
  }

  /**
   * ズームレベルの適用
   * @param {number} zoomLevel - ズーム倍率 (0.5 - 1.5)
   */
  applyZoom(zoomLevel) {
    this.currentZoom = zoomLevel;
    
    this.targetContainers.forEach(container => {
      if (container.element) {
        // transform: scale で縦横比を保ったまま縮小・拡大
        container.element.style.transform = `scale(${zoomLevel})`;
        container.element.style.transformOrigin = 'top left';
        
        // スケール適用時の位置調整
        if (zoomLevel !== 1.0) {
          container.element.style.marginBottom = `${(1 - zoomLevel) * 100}px`;
        } else {
          container.element.style.marginBottom = '';
        }
      }
    });

    // ズーム倍率が高い場合のスクロールヒント表示
    if (zoomLevel > 1.2) {
      this.showScrollHint(true);
    }

    console.log(`🔍 ズーム適用: ${Math.round(zoomLevel * 100)}%`);
  }

  /**
   * ズーム表示の更新
   * @param {number} zoomLevel - ズーム倍率
   */
  updateZoomDisplay(zoomLevel) {
    const percentage = Math.round(zoomLevel * 100);
    this.zoomValue.textContent = `${percentage}%`;
    
    // パーセンテージに応じた色変更
    if (zoomLevel < 0.8) {
      this.zoomValue.style.color = '#FF5722'; // 縮小時は赤
    } else if (zoomLevel > 1.2) {
      this.zoomValue.style.color = '#4CAF50'; // 拡大時は緑
    } else {
      this.zoomValue.style.color = '#666'; // 通常時はグレー
    }
  }

  /**
   * ズームレベルのlocalStorageへの保存
   * @param {number} zoomLevel - 保存するズーム倍率
   */
  saveZoomLevel(zoomLevel) {
    try {
      localStorage.setItem(this.storageKey, zoomLevel.toString());
      console.log(`💾 ズームレベル保存: ${Math.round(zoomLevel * 100)}%`);
    } catch (error) {
      console.warn('⚠️ ズームレベルの保存に失敗:', error);
    }
  }

  /**
   * 保存されたズームレベルの読み込み
   */
  loadZoomLevel() {
    try {
      const savedZoom = localStorage.getItem(this.storageKey);
      if (savedZoom) {
        const zoomLevel = parseFloat(savedZoom);
        if (zoomLevel >= 0.5 && zoomLevel <= 1.5) {
          this.zoomSlider.value = zoomLevel;
          this.applyZoom(zoomLevel);
          this.updateZoomDisplay(zoomLevel);
          console.log(`📚 保存されたズームレベル復元: ${Math.round(zoomLevel * 100)}%`);
        }
      }
    } catch (error) {
      console.warn('⚠️ ズームレベルの読み込みに失敗:', error);
    }
  }

  /**
   * ズームリセット（100%に戻す）
   */
  resetZoom() {
    const defaultZoom = 1.0;
    this.zoomSlider.value = defaultZoom;
    this.applyZoom(defaultZoom);
    this.updateZoomDisplay(defaultZoom);
    this.saveZoomLevel(defaultZoom);
    
    console.log('🔄 ズームレベルをリセットしました');
  }

  /**
   * 動的なサブスロット展開に対応
   * MutationObserverでサブスロットの表示変更を監視
   */
  setupDynamicSubslotObserver() {
    const observer = new MutationObserver((mutations) => {
      let needsUpdate = false;

      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
          const target = mutation.target;
          if (target.classList.contains('slot-wrapper') && target.id && target.id.endsWith('-sub')) {
            needsUpdate = true;
          }
        }
      });

      if (needsUpdate) {
        // 新たに表示されたサブスロットにもズームを適用
        setTimeout(() => {
          this.identifyTargetContainers();
          this.applyZoom(this.currentZoom);
        }, 100);
      }
    });

    // body全体を監視（サブスロット表示の変更を捕捉）
    observer.observe(document.body, {
      attributes: true,
      subtree: true,
      attributeFilter: ['style']
    });

    console.log('👁️ サブスロット動的監視を開始');
  }

  /**
   * 外部からのズーム調整API
   * @param {number} zoomLevel - 設定するズーム倍率
   */
  setZoom(zoomLevel) {
    if (zoomLevel >= 0.5 && zoomLevel <= 1.5) {
      this.zoomSlider.value = zoomLevel;
      this.applyZoom(zoomLevel);
      this.updateZoomDisplay(zoomLevel);
      this.saveZoomLevel(zoomLevel);
    }
  }

  /**
   * 現在のズームレベルを取得
   * @returns {number} 現在のズーム倍率
   */
  getCurrentZoom() {
    return this.currentZoom;
  }

  /**
   * スクロールヒント要素の作成
   * 高ズーム時のスクロール案内
   */
  createScrollHint() {
    const hint = document.createElement('div');
    hint.id = 'zoomScrollHint';
    hint.className = 'zoom-scroll-hint';
    hint.innerHTML = '🔍 ズーム中：横スクロールで全体を確認';
    document.body.appendChild(hint);
    this.scrollHint = hint;
  }

  /**
   * スクロールヒントの表示制御
   * @param {boolean} show - 表示するかどうか
   */
  showScrollHint(show) {
    if (this.scrollHint) {
      if (show) {
        this.scrollHint.classList.add('show');
        // 3秒後に自動非表示
        setTimeout(() => {
          if (this.scrollHint) {
            this.scrollHint.classList.remove('show');
          }
        }, 3000);
      } else {
        this.scrollHint.classList.remove('show');
      }
    }
  }
}

// グローバル変数として公開
let zoomController = null;

// DOMContentLoaded時の初期化
document.addEventListener('DOMContentLoaded', () => {
  // 他のシステムの初期化を待って実行
  setTimeout(() => {
    zoomController = new ZoomController();
    
    // グローバルAPIとして公開
    window.zoomController = zoomController;
    window.setZoom = (level) => zoomController.setZoom(level);
    window.resetZoom = () => zoomController.resetZoom();
    window.getCurrentZoom = () => zoomController.getCurrentZoom();
    
  }, 500);
});

// デバッグ用関数
window.debugZoomController = () => {
  if (zoomController) {
    console.log('🔍 ズームコントローラー状態:');
    console.log('- 現在のズーム:', zoomController.getCurrentZoom());
    console.log('- 対象コンテナ数:', zoomController.targetContainers.length);
    console.log('- 対象コンテナ詳細:', zoomController.targetContainers);
  } else {
    console.log('❌ ズームコントローラーが初期化されていません');
  }
};
