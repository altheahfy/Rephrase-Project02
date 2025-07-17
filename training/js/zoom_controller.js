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
    // 既存のコンテナリストをクリア
    this.targetContainers = [];

    // メインスロットエリア（上位スロット群）
    const mainSlotWrapper = document.querySelector('.slot-wrapper:not([id$="-sub"])');
    if (mainSlotWrapper) {
      this.targetContainers.push({
        element: mainSlotWrapper,
        type: 'main',
        id: 'main-slots'
      });
    }

    // サブスロットエリア群（より確実な検出）
    const subSlotWrappers = document.querySelectorAll('.slot-wrapper[id$="-sub"]');
    subSlotWrappers.forEach((wrapper, index) => {
      // 表示されているサブスロットのみを対象
      const isVisible = wrapper.style.display !== 'none' && 
                       getComputedStyle(wrapper).display !== 'none';
      
      if (isVisible) {
        this.targetContainers.push({
          element: wrapper,
          type: 'sub',
          id: wrapper.id || `sub-slots-${index}`
        });
      }
    });

    console.log(`🎯 ズーム対象コンテナ: ${this.targetContainers.length}個を特定`);
    this.targetContainers.forEach(container => {
      console.log(`  - ${container.type}: ${container.id}`);
    });
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
    
    console.log(`🔍 ズーム適用開始: ${Math.round(zoomLevel * 100)}% - 対象コンテナ数: ${this.targetContainers.length}`);
    
    this.targetContainers.forEach((container, index) => {
      if (container.element) {
        console.log(`  [${index}] ${container.type}(${container.id}): 適用前transform = ${container.element.style.transform}`);
        
        // transform: scale で縦横比を保ったまま縮小・拡大
        container.element.style.setProperty('transform', `scale(${zoomLevel})`, 'important');
        container.element.style.setProperty('transform-origin', 'top left', 'important');
        
        // 🔍 ズーム時の幅・オーバーフロー制御
        container.element.style.setProperty('max-width', 'none', 'important');
        container.element.style.setProperty('width', '100%', 'important');
        container.element.style.setProperty('overflow-x', 'visible', 'important');
        container.element.style.setProperty('overflow-y', 'visible', 'important');
        
        // 🎯 サブスロット専用：内部要素にもズーム適用 + 配置間隔調整
        if (container.type === 'sub') {
          const subContainers = container.element.querySelectorAll('.subslot-container');
          console.log(`    サブスロット内のコンテナ数: ${subContainers.length}`);
          
          // サブスロット全体の配置間隔を調整
          const originalGap = 8; // 元のgap値
          const scaledGap = originalGap * zoomLevel;
          container.element.style.setProperty('gap', `${scaledGap}px`, 'important');
          
          // サブスロットコンテナごとにズームと配置調整を適用
          subContainers.forEach((subContainer, subIndex) => {
            // ズーム適用
            subContainer.style.setProperty('transform', `scale(${zoomLevel})`, 'important');
            subContainer.style.setProperty('transform-origin', 'top left', 'important');
            
            // 🚀 配置間隔をズームレベルに応じて調整
            const originalMargin = 4; // 元のmargin値
            const originalPadding = 10; // 元のpadding値
            const scaledMargin = originalMargin * zoomLevel;
            const scaledPadding = originalPadding * zoomLevel;
            
            subContainer.style.setProperty('margin', `${scaledMargin}px`, 'important');
            subContainer.style.setProperty('padding', `${scaledPadding}px`, 'important');
            
            console.log(`      [${subIndex}] ズーム適用 + 配置調整: margin=${scaledMargin}px, padding=${scaledPadding}px`);
          });
          
          console.log(`    サブスロット全体のgap調整: ${scaledGap}px`);
        }
        
        console.log(`  [${index}] ${container.type}(${container.id}): 適用後transform = ${container.element.style.transform}`);
        console.log(`  [${index}] 実際のDOM要素:`, container.element);
        
        // スケール適用時の位置調整（縮小時の空白削減）
        if (container.type === 'sub') {
          // サブスロット専用：上位スロットとの間隔調整
          if (zoomLevel < 1.0) {
            // 縮小時は上位スロットとの間隔を詰める
            container.element.style.marginTop = `${(zoomLevel - 1) * 30}px`;
          } else {
            container.element.style.marginTop = '';
          }
        } else {
          // 上位スロット用の通常の位置調整
          if (zoomLevel < 1.0) {
            // 縮小時は上下のマージンを削減
            container.element.style.marginTop = `${(zoomLevel - 1) * 50}px`;
            container.element.style.marginBottom = `${(zoomLevel - 1) * 50}px`;
          } else if (zoomLevel > 1.0) {
            // 拡大時は下のマージンを削減
            container.element.style.marginBottom = `${(1 - zoomLevel) * 100}px`;
            container.element.style.marginTop = '';
          } else {
            // ズーム100%時はマージンリセット
            container.element.style.marginBottom = '';
            container.element.style.marginTop = '';
          }
        }
      } else {
        console.warn(`  [${index}] ${container.type}(${container.id}): 要素が存在しません`);
      }
    });

    // ズーム倍率が高い場合のスクロールヒント表示（縮小時はスクロール不要）
    if (zoomLevel > 1.3) {
      this.showScrollHint(true);
    }

    console.log(`🔍 ズーム適用完了: ${Math.round(zoomLevel * 100)}%`);
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
        // 🚨 デフォルト1.0を強制：保存値が1.0以外の場合はリセット
        if (zoomLevel >= 0.5 && zoomLevel <= 1.5 && zoomLevel === 1.0) {
          this.zoomSlider.value = zoomLevel;
          this.applyZoom(zoomLevel);
          this.updateZoomDisplay(zoomLevel);
          console.log(`📚 保存されたズームレベル復元: ${Math.round(zoomLevel * 100)}%`);
        } else {
          // 1.0以外の値が保存されている場合は強制リセット
          this.forceDefaultZoom();
        }
      } else {
        // 保存値がない場合はデフォルトを適用
        this.forceDefaultZoom();
      }
    } catch (error) {
      console.warn('⚠️ ズームレベルの読み込みに失敗:', error);
      this.forceDefaultZoom();
    }
  }

  /**
   * 強制的にデフォルト100%を設定
   */
  forceDefaultZoom() {
    const defaultZoom = 1.0;
    this.zoomSlider.value = defaultZoom;
    this.applyZoom(defaultZoom);
    this.updateZoomDisplay(defaultZoom);
    this.saveZoomLevel(defaultZoom);
    console.log('🔄 ズームレベルを強制的に100%に設定');
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
      let subslotChange = false;

      mutations.forEach((mutation) => {
        // 1. スタイル変更の監視（display: none ↔ block）
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
          const target = mutation.target;
          if (target.classList.contains('slot-wrapper') && target.id && target.id.endsWith('-sub')) {
            console.log(`📱 サブスロット表示変更検出: ${target.id}`);
            needsUpdate = true;
            subslotChange = true;
          }
        }
        
        // 2. DOM追加・削除の監視
        if (mutation.type === 'childList') {
          mutation.addedNodes.forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
              // サブスロット要素の追加
              if (node.classList && node.classList.contains('slot-wrapper') && 
                  node.id && node.id.endsWith('-sub')) {
                console.log(`➕ サブスロット要素追加: ${node.id}`);
                needsUpdate = true;
                subslotChange = true;
              }
              
              // サブスロット内の子要素追加
              const subWrappers = node.querySelectorAll && node.querySelectorAll('.slot-wrapper[id$="-sub"]');
              if (subWrappers && subWrappers.length > 0) {
                console.log(`➕ サブスロット子要素追加: ${subWrappers.length}個`);
                needsUpdate = true;
                subslotChange = true;
              }
            }
          });
        }
      });

      if (needsUpdate) {
        // サブスロット変更時は少し遅延させて確実に適用
        const delay = subslotChange ? 300 : 100;
        setTimeout(() => {
          console.log('🔄 サブスロット変更によるズーム再適用');
          this.identifyTargetContainers();
          this.applyZoom(this.currentZoom);
        }, delay);
      }
    });

    // より広範囲を監視
    observer.observe(document.body, {
      attributes: true,
      childList: true,
      subtree: true,
      attributeFilter: ['style', 'class']
    });

    console.log('👁️ 強化されたサブスロット動的監視を開始');
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
   * サブスロット検出を強制実行
   * サブスロット展開後に手動で呼び出し可能
   */
  forceSubslotDetection() {
    console.log('🔍 サブスロット強制検出を実行');
    
    // より詳細な検出情報
    const allSubSlotWrappers = document.querySelectorAll('.slot-wrapper[id$="-sub"]');
    console.log(`📊 発見されたサブスロット要素総数: ${allSubSlotWrappers.length}`);
    
    allSubSlotWrappers.forEach((wrapper, index) => {
      const computedStyle = getComputedStyle(wrapper);
      const isVisible = wrapper.style.display !== 'none' && computedStyle.display !== 'none';
      console.log(`  [${index}] ${wrapper.id}:`);
      console.log(`    - style.display: "${wrapper.style.display}"`);
      console.log(`    - computed.display: "${computedStyle.display}"`);
      console.log(`    - isVisible: ${isVisible}`);
      console.log(`    - 現在のtransform: "${wrapper.style.transform}"`);
    });
    
    this.identifyTargetContainers();
    this.applyZoom(this.currentZoom);
    
    // 検出結果をログ出力
    const subslots = this.targetContainers.filter(c => c.type === 'sub');
    console.log(`📱 最終的に対象となったサブスロット: ${subslots.length}個`);
    subslots.forEach(sub => {
      console.log(`  - ${sub.id}: 表示=${sub.element.style.display !== 'none'}`);
    });
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
    window.forceSubslotDetection = () => zoomController.forceSubslotDetection();
    
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

// ズーム設定リセット用関数
window.resetZoomSettings = () => {
  try {
    localStorage.removeItem('rephrase_zoom_level');
    if (zoomController) {
      zoomController.forceDefaultZoom();
    }
    console.log('🔄 ズーム設定を完全リセットしました');
  } catch (error) {
    console.error('❌ ズーム設定リセットに失敗:', error);
  }
};
