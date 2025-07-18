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
   * スロット領域全体（上位スロット・サブスロット）を含むsection要素を対象
   */
  identifyTargetContainers() {
    // 既存のコンテナリストをクリア
    this.targetContainers = [];

    // スロット領域全体を含むsection要素を特定
    const sections = document.querySelectorAll('section');
    let slotSection = null;
    
    sections.forEach(section => {
      // 例文シャッフルボタンとslot-wrapperを含むsectionを探す
      const hasShuffleButton = section.querySelector('#randomize-all');
      const hasSlotWrapper = section.querySelector('.slot-wrapper');
      
      if (hasShuffleButton && hasSlotWrapper) {
        slotSection = section;
      }
    });

    if (slotSection) {
      this.targetContainers.push({
        element: slotSection,
        type: 'slot-section',
        id: 'slot-section'
      });
      console.log('🎯 ズーム対象: スロット領域全体（section要素）');
      
      // 🆕 追加：展開中のサブスロットも個別に追加して確実性を向上
      const visibleSubslots = document.querySelectorAll('.slot-wrapper[id$="-sub"]:not([style*="display: none"])');
      console.log(`📱 展開中のサブスロット: ${visibleSubslots.length}個`);
      
      visibleSubslots.forEach(subslot => {
        this.targetContainers.push({
          element: subslot,
          type: 'subslot',
          id: subslot.id
        });
        console.log(`🎯 サブスロット追加: ${subslot.id}`);
      });
    } else {
      console.warn('⚠️ スロット領域のsection要素が見つかりません');
      
      // フォールバック：個別にslot-wrapperを対象とする
      const mainSlotWrapper = document.querySelector('.slot-wrapper:not([id$="-sub"])');
      if (mainSlotWrapper) {
        this.targetContainers.push({
          element: mainSlotWrapper,
          type: 'main',
          id: 'main-slots'
        });
        console.log('🎯 フォールバック: メインスロットのみ対象');
      }
      
      // フォールバック時も展開中のサブスロットを追加
      const visibleSubslots = document.querySelectorAll('.slot-wrapper[id$="-sub"]:not([style*="display: none"])');
      visibleSubslots.forEach(subslot => {
        this.targetContainers.push({
          element: subslot,
          type: 'subslot',
          id: subslot.id
        });
        console.log(`🎯 フォールバック時サブスロット追加: ${subslot.id}`);
      });
    }

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
    
    console.log(`🔍 ズーム適用開始: ${Math.round(zoomLevel * 100)}% - 対象コンテナ数: ${this.targetContainers.length}`);
    
    // 🔎 ROOT CAUSE ANALYSIS: スロットSの詳細調査
    console.log('🔬=== スロットS根本原因分析開始 ===');
    
    const slotS = document.getElementById('slot-s');
    if (slotS) {
      const computedStyle = getComputedStyle(slotS);
      const parentElement = slotS.parentElement;
      
      console.log('📊 スロットS詳細情報:');
      console.log(`  - ID: ${slotS.id}`);
      console.log(`  - クラス: ${slotS.className}`);
      console.log(`  - 親要素ID: ${parentElement ? parentElement.id : 'なし'}`);
      console.log(`  - 親要素クラス: ${parentElement ? parentElement.className : 'なし'}`);
      console.log(`  - 現在のtransform: "${slotS.style.transform}"`);
      console.log(`  - 計算されたtransform: "${computedStyle.transform}"`);
      console.log(`  - position: "${computedStyle.position}"`);
      console.log(`  - top: "${computedStyle.top}"`);
      console.log(`  - left: "${computedStyle.left}"`);
      console.log(`  - width: "${computedStyle.width}"`);
      console.log(`  - height: "${computedStyle.height}"`);
      console.log(`  - z-index: "${computedStyle.zIndex}"`);
      
      // 他のスロットとの比較
      const slotM1 = document.getElementById('slot-m1');
      if (slotM1) {
        const m1Style = getComputedStyle(slotM1);
        console.log('📊 比較用スロットM1:');
        console.log(`  - 計算されたtransform: "${m1Style.transform}"`);
        console.log(`  - position: "${m1Style.position}"`);
        console.log(`  - width: "${m1Style.width}"`);
        console.log(`  - height: "${m1Style.height}"`);
      }
      
      // スロットS特有のCSS継承チェック
      console.log('🎨 スロットS CSS継承チェック:');
      const relevantProps = ['transform', 'transform-origin', 'scale', 'zoom', 'display', 'visibility'];
      relevantProps.forEach(prop => {
        console.log(`  - ${prop}: "${computedStyle.getPropertyValue(prop)}"`);
      });
    }
    
    // 🆕 直接的アプローチ: すべての.slot-containerに強制的にズーム適用
    const allSlotContainers = document.querySelectorAll('.slot-container');
    console.log(`🎯 検出された全スロットコンテナ数: ${allSlotContainers.length}`);
    
    allSlotContainers.forEach((container, index) => {
      const slotId = container.id || `container-${index}`;
      console.log(`  [${index}] スロット直接適用: ${slotId}`);
      
      // ズーム適用前の状態を記録
      const beforeTransform = container.style.transform;
      const beforeComputed = getComputedStyle(container).transform;
      
      // 全スロットコンテナに強制的にズーム適用
      container.style.setProperty('transform', `scale(${zoomLevel})`, 'important');
      container.style.setProperty('transform-origin', 'top left', 'important');
      
      // ズーム適用後の状態を記録
      const afterTransform = container.style.transform;
      const afterComputed = getComputedStyle(container).transform;
      
      // スロットSの特別処理：完全リセット＋強制適用
      if (slotId === 'slot-s') {
        console.log(`🎯 スロットS変更詳細:`);
        console.log(`  - 適用前style: "${beforeTransform}"`);
        console.log(`  - 適用前computed: "${beforeComputed}"`);
        console.log(`  - 適用後style: "${afterTransform}"`);
        console.log(`  - 適用後computed: "${afterComputed}"`);
        console.log(`  - 変更成功: ${beforeComputed !== afterComputed}`);
        
        // 🔧 ROOT CAUSE FIX: スロットSの完全リセット＋強制適用
        console.log(`🔧 スロットS専用修正処理開始...`);
        
        // 1. 全transformプロパティを完全リセット
        container.style.removeProperty('transform');
        container.style.removeProperty('transform-origin');
        container.style.removeProperty('scale');
        container.style.removeProperty('zoom');
        
        // 2. 強制的に再計算させる
        container.offsetHeight; // reflow trigger
        
        // 3. 新しい値を強制適用
        container.style.setProperty('transform', `scale(${zoomLevel})`, 'important');
        container.style.setProperty('transform-origin', 'top left', 'important');
        
        // 4. 結果確認
        const finalComputed = getComputedStyle(container).transform;
        console.log(`🔧 スロットS修正後: "${finalComputed}"`);
        console.log(`🔧 修正成功: ${finalComputed.includes(zoomLevel.toString())}`);
        
        // 追加：親要素のtransformも確認
        const parent = container.parentElement;
        if (parent) {
          console.log(`  - 親要素transform: "${getComputedStyle(parent).transform}"`);
        }
      }
    });
    
    // 既存のターゲットコンテナ処理も継続
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
        
        console.log(`  [${index}] ${container.type}(${container.id}): 適用後transform = ${container.element.style.transform}`);
        
        // スケール適用時の位置調整（縮小時の空白削減）
        if (zoomLevel < 1.0) {
          // 縮小時は要素間の空白を削減
          const spaceReduction = (1 - zoomLevel) * 50;
          container.element.style.marginBottom = `-${spaceReduction}px`;
        } else {
          // 100%以上の場合はマージンリセット
          container.element.style.marginBottom = '';
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
   * 設計仕様：100%(1.0)の値のみ復元、それ以外は強制的に100%にリセット
   */
  loadZoomLevel() {
    try {
      const savedZoom = localStorage.getItem(this.storageKey);
      if (savedZoom) {
        const zoomLevel = parseFloat(savedZoom);
        // 設計仕様に従い、1.0(100%)の値のみ復元、それ以外は強制リセット
        if (zoomLevel === 1.0) {
          this.zoomSlider.value = zoomLevel;
          this.applyZoom(zoomLevel);
          this.updateZoomDisplay(zoomLevel);
          console.log(`📚 100%ズームレベル復元完了`);
        } else {
          // 1.0以外の値は強制的に100%にリセット
          console.log(`🔄 非100%ズームレベル検出 (${Math.round(zoomLevel * 100)}%) → 100%にリセット`);
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
    
    // 🔧 修正：対象コンテナの再検出と現在のズーム値の取得を確実に実行
    this.identifyTargetContainers();
    
    // 現在のズーム値を取得（スライダーから直接取得して確実性を向上）
    const currentZoomFromSlider = parseFloat(this.zoomSlider.value) || 1.0;
    this.currentZoom = currentZoomFromSlider;
    
    console.log(`🔍 強制検出時のズーム値: スライダー=${currentZoomFromSlider}, currentZoom=${this.currentZoom}`);
    
    // ズーム適用
    this.applyZoom(this.currentZoom);
    
    // 検出結果をログ出力
    const subslots = this.targetContainers.filter(c => c.type === 'sub');
    console.log(`📱 最終的に対象となったサブスロット: ${subslots.length}個`);
    subslots.forEach(sub => {
      console.log(`  - ${sub.id}: 表示=${sub.element.style.display !== 'none'}`);
    });
    
    // 🆕 追加：サブスロット展開直後の追加確認処理
    setTimeout(() => {
      console.log('🔄 サブスロット展開後の追加確認処理');
      const visibleSubslots = document.querySelectorAll('.slot-wrapper[id$="-sub"]:not([style*="display: none"])');
      console.log(`👁️ 表示中のサブスロット数: ${visibleSubslots.length}`);
      
      visibleSubslots.forEach(subslot => {
        const currentTransform = subslot.style.transform;
        console.log(`  - ${subslot.id}: transform="${currentTransform}"`);
        
        // もしズームが適用されていない場合は再適用
        if (!currentTransform.includes('scale')) {
          console.log(`🔧 ${subslot.id} にズームを再適用`);
          subslot.style.setProperty('transform', `scale(${this.currentZoom})`, 'important');
          subslot.style.setProperty('transform-origin', 'top left', 'important');
        }
      });
    }, 200);
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
