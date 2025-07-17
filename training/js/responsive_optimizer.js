/**
 * Rephraseプロジェクト レスポンシブ自動最適化システム
 * 作成日: 2025年7月17日
 * 目的: 画面サイズに応じたコンテンツの自動最適化
 */

class ResponsiveOptimizer {
    constructor() {
        this.viewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };
        this.contentElements = new Map();
        this.isInitialized = false;
        
        // デバウンス用のタイマー
        this.resizeTimeout = null;
        this.RESIZE_DEBOUNCE_MS = 150;
        
        // 最適化設定
        this.settings = {
            minSlotSize: { width: 100, height: 80 },
            maxSlotSize: { width: 300, height: 350 },
            preferredAspectRatio: 1.2, // 幅:高さ = 1.2:1
            gridGap: { min: 8, max: 20 },
            fontSize: { min: 10, max: 18 }
        };
    }
    
    /**
     * システム初期化
     */
    initialize() {
        if (this.isInitialized) return;
        
        console.log('🎯 レスポンシブ最適化システム初期化開始');
        
        // DOM要素をキャッシュ
        this.cacheElements();
        
        // 初回最適化実行
        this.optimizeLayout();
        
        // イベントリスナー設定
        this.setupEventListeners();
        
        // CSS変数を更新
        this.updateCSSVariables();
        
        this.isInitialized = true;
        console.log('✅ レスポンシブ最適化システム初期化完了');
    }
    
    /**
     * DOM要素をキャッシュ
     */
    cacheElements() {
        this.contentElements.set('mainContainer', document.querySelector('.main-container') || document.body);
        this.contentElements.set('sentenceArea', document.querySelector('.sentence-display-area') || document.querySelector('#static-slot-area'));
        this.contentElements.set('slotContainers', document.querySelectorAll('.slot-container, [id^="slot-"]'));
        this.contentElements.set('navigationArea', document.querySelector('.navigation-area'));
        this.contentElements.set('controlPanel', document.querySelector('.control-panel'));
    }
    
    /**
     * イベントリスナー設定
     */
    setupEventListeners() {
        // ウィンドウリサイズイベント（デバウンス処理）
        window.addEventListener('resize', () => {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, this.RESIZE_DEBOUNCE_MS);
        });
        
        // オリエンテーション変更イベント
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleResize();
            }, 300); // オリエンテーション変更の完了を待つ
        });
        
        // DOM変更監視（新しいスロットが追加された場合）
        if (this.contentElements.get('sentenceArea')) {
            const observer = new MutationObserver(() => {
                this.cacheElements();
                this.optimizeLayout();
            });
            
            observer.observe(this.contentElements.get('sentenceArea'), {
                childList: true,
                subtree: true
            });
        }
    }
    
    /**
     * ウィンドウリサイズ処理
     */
    handleResize() {
        const newViewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };
        
        // サイズ変更が十分大きい場合のみ最適化実行
        const widthChange = Math.abs(newViewport.width - this.viewport.width);
        const heightChange = Math.abs(newViewport.height - this.viewport.height);
        
        if (widthChange > 50 || heightChange > 50) {
            console.log(`🔄 画面サイズ変更検出: ${this.viewport.width}x${this.viewport.height} → ${newViewport.width}x${newViewport.height}`);
            
            this.viewport = newViewport;
            this.optimizeLayout();
            this.updateCSSVariables();
        }
    }
    
    /**
     * レイアウト最適化メイン処理
     */
    optimizeLayout() {
        try {
            // 1. 画面サイズカテゴリを判定
            const screenCategory = this.categorizeScreen();
            console.log(`📱 画面カテゴリ: ${screenCategory}`);
            
            // 2. スロット数を取得
            const slotCount = this.getSlotCount();
            console.log(`🎯 スロット数: ${slotCount}`);
            
            // 3. 最適なグリッド設定を計算
            const gridConfig = this.calculateOptimalGrid(slotCount, screenCategory);
            console.log(`⚙️ グリッド設定:`, gridConfig);
            
            // 4. スロットサイズを計算
            const slotConfig = this.calculateSlotSizes(gridConfig, screenCategory);
            console.log(`📏 スロットサイズ:`, slotConfig);
            
            // 5. CSSを動的に適用
            this.applyCSSConfig(gridConfig, slotConfig, screenCategory);
            
            // 6. 画像の最適化
            this.optimizeImages();
            
            console.log('✨ レイアウト最適化完了');
            
        } catch (error) {
            console.error('❌ レイアウト最適化エラー:', error);
        }
    }
    
    /**
     * 画面サイズカテゴリを判定
     */
    categorizeScreen() {
        const { width, height } = this.viewport;
        
        if (width >= 1200) return 'desktop-large';
        if (width >= 992) return 'desktop';
        if (width >= 768) return 'tablet';
        if (width >= 480) return 'mobile-large';
        return 'mobile-small';
    }
    
    /**
     * スロット数を取得
     */
    getSlotCount() {
        const slots = this.contentElements.get('slotContainers');
        return slots ? slots.length : 10; // デフォルト10個
    }
    
    /**
     * 最適なグリッド設定を計算
     */
    calculateOptimalGrid(slotCount, screenCategory) {
        const configs = {
            'desktop-large': { cols: Math.min(5, Math.ceil(slotCount / 2)), gap: 20 },
            'desktop': { cols: Math.min(4, Math.ceil(slotCount / 2)), gap: 16 },
            'tablet': { cols: Math.min(3, Math.ceil(slotCount / 3)), gap: 12 },
            'mobile-large': { cols: 2, gap: 10 },
            'mobile-small': { cols: 1, gap: 8 }
        };
        
        return configs[screenCategory] || configs['desktop'];
    }
    
    /**
     * スロットサイズを計算
     */
    calculateSlotSizes(gridConfig, screenCategory) {
        const { width, height } = this.viewport;
        const availableWidth = width - (2 * 20); // パディング分を除く
        const availableHeight = height - 120; // ナビ・コントロール分を除く
        
        // グリッドベースの幅計算
        const slotWidth = Math.floor(
            (availableWidth - (gridConfig.gap * (gridConfig.cols - 1))) / gridConfig.cols
        );
        
        // アスペクト比ベースの高さ計算
        const preferredHeight = Math.floor(slotWidth / this.settings.preferredAspectRatio);
        
        // 制約内でのサイズ調整
        const finalWidth = Math.max(
            this.settings.minSlotSize.width,
            Math.min(this.settings.maxSlotSize.width, slotWidth)
        );
        
        const finalHeight = Math.max(
            this.settings.minSlotSize.height,
            Math.min(this.settings.maxSlotSize.height, preferredHeight)
        );
        
        return {
            width: finalWidth,
            height: finalHeight,
            fontSize: this.calculateFontSize(finalWidth, screenCategory)
        };
    }
    
    /**
     * フォントサイズを計算
     */
    calculateFontSize(slotWidth, screenCategory) {
        const baseSizes = {
            'desktop-large': { main: 16, sub: 13 },
            'desktop': { main: 15, sub: 12 },
            'tablet': { main: 14, sub: 11 },
            'mobile-large': { main: 13, sub: 10 },
            'mobile-small': { main: 12, sub: 9 }
        };
        
        const base = baseSizes[screenCategory] || baseSizes['desktop'];
        
        // スロット幅に応じてスケーリング
        const scale = Math.max(0.7, Math.min(1.3, slotWidth / 150));
        
        return {
            main: Math.round(base.main * scale),
            sub: Math.round(base.sub * scale)
        };
    }
    
    /**
     * CSS設定を動的に適用
     */
    applyCSSConfig(gridConfig, slotConfig, screenCategory) {
        const style = document.createElement('style');
        style.id = 'responsive-optimizer-styles';
        
        // 既存の動的スタイルを削除
        const existing = document.getElementById('responsive-optimizer-styles');
        if (existing) {
            existing.remove();
        }
        
        style.innerHTML = `
            /* 🎯 動的レスポンシブ最適化スタイル */
            .sentence-display-area,
            #static-slot-area {
                display: grid !important;
                grid-template-columns: repeat(${gridConfig.cols}, 1fr) !important;
                gap: ${gridConfig.gap}px !important;
                justify-items: center !important;
                max-height: calc(100vh - 140px) !important;
                overflow-y: auto !important;
                padding: ${Math.max(8, gridConfig.gap)}px !important;
            }
            
            .slot-container,
            [id^="slot-"] {
                width: ${slotConfig.width}px !important;
                height: ${slotConfig.height}px !important;
                min-width: ${slotConfig.width}px !important;
                min-height: ${slotConfig.height}px !important;
                max-width: ${slotConfig.width}px !important;
                max-height: ${slotConfig.height}px !important;
                display: flex !important;
                flex-direction: column !important;
                padding: ${Math.max(6, Math.floor(slotConfig.width * 0.05))}px !important;
                box-sizing: border-box !important;
            }
            
            .slot-text,
            .slot-phrase {
                font-size: ${slotConfig.fontSize.main}px !important;
                line-height: 1.3 !important;
                word-wrap: break-word !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }
            
            .slot-phrase {
                font-size: ${slotConfig.fontSize.sub}px !important;
            }
            
            .slot-image,
            .slot-multi-image {
                max-width: 100% !important;
                height: ${Math.floor(slotConfig.height * 0.4)}px !important;
                object-fit: cover !important;
            }
            
            /* 画面カテゴリ別追加調整 */
            ${this.getScreenCategoryStyles(screenCategory)}
        `;
        
        document.head.appendChild(style);
    }
    
    /**
     * 画面カテゴリ別の追加スタイル
     */
    getScreenCategoryStyles(category) {
        const styles = {
            'mobile-small': `
                .control-panel { flex-direction: column !important; }
                .voice-btn { font-size: 10px !important; padding: 4px 6px !important; }
                .slot-label { font-size: 11px !important; }
            `,
            'mobile-large': `
                .control-panel { flex-wrap: wrap !important; }
                .voice-btn { font-size: 11px !important; }
            `,
            'tablet': `
                .control-panel { gap: 8px !important; }
            `
        };
        
        return styles[category] || '';
    }
    
    /**
     * CSS変数を更新
     */
    updateCSSVariables() {
        const root = document.documentElement;
        const slotCount = this.getSlotCount();
        
        root.style.setProperty('--viewport-width', `${this.viewport.width}px`);
        root.style.setProperty('--viewport-height', `${this.viewport.height}px`);
        root.style.setProperty('--slot-count', slotCount.toString());
        
        // 画像数の設定（複数画像表示用）
        const imageContainers = document.querySelectorAll('.multi-image-container');
        imageContainers.forEach(container => {
            const images = container.querySelectorAll('.slot-multi-image');
            container.style.setProperty('--image-count', images.length.toString());
        });
    }
    
    /**
     * 画像最適化
     */
    optimizeImages() {
        const images = document.querySelectorAll('.slot-image, .slot-multi-image');
        
        images.forEach(img => {
            // 遅延読み込み対応
            if ('loading' in HTMLImageElement.prototype) {
                img.loading = 'lazy';
            }
            
            // 画像の最適サイズ計算
            const container = img.closest('.slot-container, [id^="slot-"]');
            if (container) {
                const containerWidth = container.offsetWidth;
                const containerHeight = container.offsetHeight;
                
                // コンテナサイズに基づいて画像サイズを調整
                img.style.maxWidth = `${containerWidth - 12}px`;
                img.style.maxHeight = `${Math.floor(containerHeight * 0.5)}px`;
            }
        });
    }
    
    /**
     * レスポンシブ設定の動的変更
     */
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        this.optimizeLayout();
    }
    
    /**
     * システム状態の取得（デバッグ用）
     */
    getSystemStatus() {
        return {
            isInitialized: this.isInitialized,
            viewport: this.viewport,
            screenCategory: this.categorizeScreen(),
            slotCount: this.getSlotCount(),
            settings: this.settings
        };
    }
    
    /**
     * 手動最適化トリガー
     */
    forceOptimization() {
        console.log('🔄 手動最適化実行');
        this.cacheElements();
        this.optimizeLayout();
        this.updateCSSVariables();
    }
}

// グローバルインスタンス作成
window.responsiveOptimizer = new ResponsiveOptimizer();

// DOM読み込み完了時に初期化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            window.responsiveOptimizer.initialize();
        }, 500); // 他のスクリプトの初期化を待つ
    });
} else {
    // すでにDOMが読み込まれている場合
    setTimeout(() => {
        window.responsiveOptimizer.initialize();
    }, 500);
}

// デバッグ用の関数をグローバルに公開
window.debugResponsive = {
    status: () => window.responsiveOptimizer.getSystemStatus(),
    force: () => window.responsiveOptimizer.forceOptimization(),
    settings: (newSettings) => window.responsiveOptimizer.updateSettings(newSettings)
};

console.log('📱 レスポンシブ最適化システム読み込み完了');
console.log('💡 デバッグコマンド: window.debugResponsive.status(), .force(), .settings({})');
