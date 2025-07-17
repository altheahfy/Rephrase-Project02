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
        
        // ウィンドウリサイズイベント（複数の方法で監視）
        window.addEventListener('resize', () => {
            this.debounceAdjustLayout();
        });
        
        // オリエンテーション変更対応（モバイル端末用）
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.adjustLayout();
            }, 500); // オリエンテーション変更後少し待つ
        });
        
        // ビューポート変更監視（より細かい制御）
        let lastWindowWidth = window.innerWidth;
        setInterval(() => {
            const currentWidth = window.innerWidth;
            if (Math.abs(currentWidth - lastWindowWidth) > 10) {
                lastWindowWidth = currentWidth;
                this.adjustLayout();
            }
        }, 1000); // 1秒ごとにチェック
        
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
        }, 50); // より高速な反応
    }
    
    /**
     * レイアウト調整メイン処理
     */
    adjustLayout() {
        if (!this.slotWrapper) return;
        
        // 🎯 ウィンドウ幅も考慮した幅計算
        const windowWidth = window.innerWidth;
        const containerWidth = Math.min(this.slotWrapper.offsetWidth, windowWidth - 40); // 余白を考慮
        const slotContainers = document.querySelectorAll('.slot-container:not(.hidden-empty)');
        const slotCount = slotContainers.length;
        
        if (slotCount === 0) return;
        
        console.log(`📐 レイアウト調整: ウィンドウ幅${windowWidth}px, コンテナ幅${containerWidth}px, スロット数${slotCount}`);
        
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
            globalScale = Math.max(0.2, containerWidth / idealTotalWidth); // 最小スケールを0.2に
            
            // 🎯 より細かい調整 - HD解像度対応
            if (containerWidth < 400) {
                globalScale = Math.min(globalScale, 0.3); // 非常に小さい画面
            } else if (containerWidth < 600) {
                globalScale = Math.min(globalScale, 0.5); // スマートフォン
            } else if (containerWidth < 800) {
                globalScale = Math.min(globalScale, 0.6); // 小型タブレット
            } else if (containerWidth < 1000) {
                globalScale = Math.min(globalScale, 0.7); // 中型タブレット・小型PC
            } else if (containerWidth < 1200) {
                globalScale = Math.min(globalScale, 0.85); // 中型PC
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
