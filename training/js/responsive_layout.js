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
        
        // 🎯 実際の要素サイズを動的に取得
        const slotContainers = document.querySelectorAll('.slot-container:not(.hidden-empty)');
        const slotCount = slotContainers.length;
        
        if (slotCount === 0) return;
        
        // 🎯 固定値を使用（スケール適用の影響を受けないように）
        // CSSで定義された基本サイズを使用
        const baseSlotWidth = 180; // CSSのmin-width基準
        const baseGap = 12; // CSSのgap値
        
        // 実際のコンテナ幅とウィンドウ幅を取得
        const containerWidth = this.slotWrapper.offsetWidth;
        const windowWidth = window.innerWidth;
        
        // 🎯 実際の利用可能幅を正確に計算
        // containerWidthとwindowWidthの大きい方を基準にする（十分な余裕を持たせる）
        const availableWidth = Math.max(containerWidth, windowWidth * 0.9); // ウィンドウ幅の90%を利用可能とする
        
        console.log(`🔍 デバッグ: 固定値使用 - baseSlotWidth=${baseSlotWidth}px, baseGap=${baseGap}px`);
        console.log(`📐 レイアウト調整詳細:`);
        console.log(`   ウィンドウ幅: ${windowWidth}px`);
        console.log(`   コンテナ幅: ${containerWidth}px`);
        console.log(`   基本スロット幅: ${baseSlotWidth}px`);
        console.log(`   利用可能幅: ${availableWidth}px (ウィンドウ幅の90%基準)`);
        console.log(`   スロット数: ${slotCount}`);
        
        // 🎯 全体スケール調整方式：横一列を維持して全体を縮小
        const { globalScale } = this.calculateOptimalScale(availableWidth, slotCount, baseSlotWidth, baseGap);
        
        // CSS変数を更新
        this.slotWrapper.style.setProperty('--global-scale', globalScale);
        this.slotWrapper.style.setProperty('--overflow-x', globalScale < 1 ? 'visible' : 'visible');
        
        // 🔍 設定確認ログ
        const setScale = this.slotWrapper.style.getPropertyValue('--global-scale');
        console.log(`🔍 CSS変数設定確認: --global-scale = ${setScale}`);
        console.log(`🔍 .slot-wrapper element:`, this.slotWrapper);
        
        console.log(`🎯 調整結果: 全体スケール${globalScale}`);
    }
    
    /**
     * 最適なスケールを計算
     */
    calculateOptimalScale(availableWidth, slotCount, baseSlotWidth = 180, baseGap = 12) {
        // 理想的な必要幅を固定値で計算（スケール適用前のサイズ）
        const idealTotalWidth = (baseSlotWidth * slotCount) + (baseGap * (slotCount - 1));
        
        console.log(`🧮 スケール計算:`);
        console.log(`   基本スロット幅: ${baseSlotWidth}px`);
        console.log(`   基本ギャップ: ${baseGap}px`);
        console.log(`   理想的な必要幅: ${idealTotalWidth}px`);
        console.log(`   利用可能幅: ${availableWidth}px`);
        
        // スケール計算
        let globalScale = 1;
        
        // 🎯 より寛容な閾値：利用可能幅の95%を超える場合のみ縮小
        const threshold = availableWidth * 0.95;
        
        if (idealTotalWidth > threshold) {
            // コンテンツが閾値を超える場合のみ縮小
            globalScale = Math.max(0.3, threshold / idealTotalWidth); // 最小スケールを0.3に上げる
            console.log(`🔍 縮小が必要: ${idealTotalWidth}px > ${threshold.toFixed(0)}px (閾値95%) → スケール${globalScale.toFixed(3)}`);
        } else {
            // 閾値内に収まる場合は通常サイズ（1.0）を維持
            globalScale = 1.0;
            console.log(`✅ 通常サイズで表示: ${idealTotalWidth}px ≤ ${threshold.toFixed(0)}px (閾値95%)`);
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
