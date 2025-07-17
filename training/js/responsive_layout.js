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
        const slotContainers = document.querySelectorAll('.slot-container:not(.hidden-empty)');
        const slotCount = slotContainers.length;
        
        if (slotCount === 0) return;
        
        console.log(`📐 レイアウト調整: 幅${containerWidth}px, スロット数${slotCount}`);
        
        // 🎯 全体スケール調整方式：横一列を維持して全体を縮小
        const { globalScale } = this.calculateOptimalScale(containerWidth, slotCount);
        
        // CSS変数を更新
        this.slotWrapper.style.setProperty('--global-scale', globalScale);
        this.slotWrapper.style.setProperty('--overflow-x', globalScale < 1 ? 'visible' : 'visible');
        
        console.log(`🎯 調整結果: 全体スケール${globalScale}`);
    }
    
    /**
     * 最適なスケールを計算
     */
    calculateOptimalScale(containerWidth, slotCount) {
        const baseSlotWidth = 180; // 基本スロット幅
        const gap = 12; // スロット間のギャップ
        
        // 理想的な必要幅を計算
        const idealTotalWidth = (baseSlotWidth * slotCount) + (gap * (slotCount - 1));
        
        // スケール計算
        let globalScale = 1;
        
        if (idealTotalWidth > containerWidth) {
            // 必要な縮小率を計算
            globalScale = Math.max(0.3, containerWidth / idealTotalWidth);
            
            // より細かい調整
            if (containerWidth < 600) {
                globalScale = Math.min(globalScale, 0.5);
            } else if (containerWidth < 900) {
                globalScale = Math.min(globalScale, 0.7);
            } else if (containerWidth < 1200) {
                globalScale = Math.min(globalScale, 0.85);
            }
        }
        
        return {
            globalScale: globalScale.toFixed(3)
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
