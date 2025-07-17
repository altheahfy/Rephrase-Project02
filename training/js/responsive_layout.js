/**
 * レスポンシブ自動サイズ調整システム
 * 画面幅に応じてスロットサイズとフォントサイズを動的調整
 */
class ResponsiveLayoutManager {
    constructor() {
        this.initialized = false;
        this.slotWrapper = null;
        this.resizeObserver = null;
        this.lastWidth = 0;
        
        console.log('📐 レスポンシブレイアウトマネージャー初期化');
    }
    
    /**
     * 初期化
     */
    init() {
        if (this.initialized) return;
        
        this.slotWrapper = document.querySelector('.slot-wrapper');
        if (!this.slotWrapper) {
            console.warn('⚠️ .slot-wrapperが見つかりません');
            return;
        }
        
        // 初回調整
        this.adjustLayout();
        
        // リサイズ監視
        this.setupResizeObserver();
        
        // ウィンドウリサイズイベント
        window.addEventListener('resize', () => {
            this.debounceAdjustLayout();
        });
        
        this.initialized = true;
        console.log('✅ レスポンシブレイアウトマネージャー開始');
    }
    
    /**
     * ResizeObserverを設定
     */
    setupResizeObserver() {
        if ('ResizeObserver' in window) {
            this.resizeObserver = new ResizeObserver(entries => {
                for (let entry of entries) {
                    const width = entry.contentRect.width;
                    if (Math.abs(width - this.lastWidth) > 50) { // 50px以上の変化で調整
                        this.lastWidth = width;
                        this.adjustLayout();
                    }
                }
            });
            
            this.resizeObserver.observe(this.slotWrapper);
        }
    }
    
    /**
     * デバウンス付きレイアウト調整
     */
    debounceAdjustLayout() {
        clearTimeout(this.adjustTimeout);
        this.adjustTimeout = setTimeout(() => {
            this.adjustLayout();
        }, 100);
    }
    
    /**
     * レイアウト調整メイン処理
     */
    adjustLayout() {
        if (!this.slotWrapper) return;
        
        const containerWidth = this.slotWrapper.offsetWidth;
        const slotContainers = document.querySelectorAll('.slot-container');
        const slotCount = slotContainers.length;
        
        if (slotCount === 0) return;
        
        console.log(`📐 レイアウト調整: 幅${containerWidth}px, スロット数${slotCount}`);
        
        // 最適なスロット幅を計算
        const { slotWidth, fontScale, imageScale } = this.calculateOptimalSizes(containerWidth, slotCount);
        
        // CSS変数を更新
        this.slotWrapper.style.setProperty('--slot-min-width', `${slotWidth}px`);
        this.slotWrapper.style.setProperty('--font-scale', fontScale);
        this.slotWrapper.style.setProperty('--image-scale', imageScale);
        
        console.log(`🎯 調整結果: スロット幅${slotWidth}px, フォント倍率${fontScale}, 画像倍率${imageScale}`);
        
        // グリッドレイアウトの再計算を促す
        this.slotWrapper.style.gridTemplateColumns = `repeat(auto-fit, minmax(${slotWidth}px, 1fr))`;
    }
    
    /**
     * 最適なサイズを計算
     */
    calculateOptimalSizes(containerWidth, slotCount) {
        const minSlotWidth = 100; // 最小スロット幅
        const maxSlotWidth = 250; // 最大スロット幅
        const gap = 20; // グリッドギャップ
        
        // 理想的なスロット幅を計算
        const availableWidth = containerWidth - (gap * (slotCount - 1));
        let idealSlotWidth = availableWidth / slotCount;
        
        // 範囲内に調整
        let slotWidth = Math.max(minSlotWidth, Math.min(maxSlotWidth, idealSlotWidth));
        
        // スケール計算
        let fontScale = 1;
        let imageScale = 1;
        
        if (containerWidth < 600) {
            fontScale = 0.7;
            imageScale = 0.6;
            slotWidth = Math.max(90, slotWidth);
        } else if (containerWidth < 900) {
            fontScale = 0.8;
            imageScale = 0.7;
            slotWidth = Math.max(110, slotWidth);
        } else if (containerWidth < 1200) {
            fontScale = 0.9;
            imageScale = 0.8;
            slotWidth = Math.max(130, slotWidth);
        } else if (containerWidth < 1600) {
            fontScale = 1.0;
            imageScale = 0.9;
            slotWidth = Math.max(150, slotWidth);
        } else {
            // 4K等の大画面
            fontScale = 1.1;
            imageScale = 1.0;
            slotWidth = Math.max(180, slotWidth);
        }
        
        return {
            slotWidth: Math.round(slotWidth),
            fontScale: fontScale.toFixed(2),
            imageScale: imageScale.toFixed(2)
        };
    }
    
    /**
     * 手動再調整
     */
    recalculate() {
        console.log('🔄 手動レイアウト再計算');
        this.adjustLayout();
    }
    
    /**
     * 破棄
     */
    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        window.removeEventListener('resize', this.debounceAdjustLayout);
        clearTimeout(this.adjustTimeout);
        this.initialized = false;
        console.log('🗑️ レスポンシブレイアウトマネージャー破棄');
    }
}

// グローバルインスタンス作成
window.responsiveLayoutManager = new ResponsiveLayoutManager();

// DOM読み込み完了後に自動初期化
document.addEventListener('DOMContentLoaded', () => {
    // 少し遅延して初期化（他のスクリプトの完了を待つ）
    setTimeout(() => {
        window.responsiveLayoutManager.init();
    }, 500);
});

// データ読み込み後にも再調整
document.addEventListener('dataLoaded', () => {
    setTimeout(() => {
        window.responsiveLayoutManager.recalculate();
    }, 100);
});
