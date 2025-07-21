/**
 * Rephraseプロジェクト スマホ最適化JavaScript
 * 2025年7月21日作成
 * タッチ操作、パフォーマンス、UX最適化
 */

// スマホ最適化システム初期化
class MobileOptimizer {
    constructor() {
        this.isMobile = this.detectMobile();
        this.touchStartTime = 0;
        this.isInitialized = false;
        
        this.init();
    }

    /**
     * モバイルデバイス判定
     */
    detectMobile() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        const mobilePatterns = [
            /Android/i,
            /webOS/i,
            /iPhone/i,
            /iPad/i,
            /iPod/i,
            /BlackBerry/i,
            /Windows Phone/i
        ];
        
        return mobilePatterns.some(pattern => pattern.test(userAgent)) || 
               (window.innerWidth <= 768);
    }

    /**
     * 初期化処理
     */
    init() {
        if (this.isInitialized) return;
        
        console.log('📱 Mobile Optimizer initializing...', { isMobile: this.isMobile });
        
        // DOM読み込み完了後に実行
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
        
        this.isInitialized = true;
    }

    /**
     * セットアップ処理
     */
    setup() {
        if (this.isMobile) {
            this.optimizeForMobile();
        }
        
        this.setupGlobalOptimizations();
        this.setupTouchOptimizations();
        this.setupKeyboardOptimizations();
        this.setupVoiceSystemOptimizations();
        this.setupOrientationHandling();
        
        console.log('✅ Mobile Optimizer setup complete');
    }

    /**
     * モバイル専用最適化
     */
    optimizeForMobile() {
        // bodyにモバイルクラス追加
        document.body.classList.add('mobile-optimized');
        
        // ビューポート設定の調整
        this.adjustViewport();
        
        // スクロール最適化
        this.optimizeScrolling();
        
        // ズーム無効化（必要に応じて）
        this.preventUnwantedZoom();
        
        console.log('📱 Mobile-specific optimizations applied');
    }

    /**
     * ビューポート調整
     */
    adjustViewport() {
        let viewport = document.querySelector('meta[name=viewport]');
        if (!viewport) {
            viewport = document.createElement('meta');
            viewport.name = 'viewport';
            document.head.appendChild(viewport);
        }
        
        // iOS Safari の 100vh 問題対策
        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover';
        
        // CSS カスタムプロパティで実際の高さを設定
        this.setViewportHeight();
        window.addEventListener('resize', () => this.setViewportHeight());
    }

    /**
     * ビューポート高さの設定
     */
    setViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }

    /**
     * スクロール最適化
     */
    optimizeScrolling() {
        // スムーズスクロール
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // オーバースクロール防止
        document.body.style.overscrollBehavior = 'contain';
        
        // iOS Safari のバウンス防止
        document.addEventListener('touchmove', (e) => {
            if (e.target.closest('.scrollable')) return;
            e.preventDefault();
        }, { passive: false });
    }

    /**
     * 意図しないズームの防止
     */
    preventUnwantedZoom() {
        // ダブルタップズーム防止
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, { passive: false });
        
        // ピンチズーム防止
        document.addEventListener('gesturestart', (e) => {
            e.preventDefault();
        });
    }

    /**
     * 全体的な最適化
     */
    setupGlobalOptimizations() {
        // 画像遅延読み込み
        this.setupLazyLoading();
        
        // クリックイベントの最適化
        this.optimizeClickEvents();
        
        // フォーカス管理
        this.setupFocusManagement();
    }

    /**
     * 画像遅延読み込み
     */
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * クリックイベント最適化
     */
    optimizeClickEvents() {
        // 300ms遅延の除去
        if (this.isMobile) {
            document.addEventListener('touchstart', () => {}, { passive: true });
        }
        
        // ボタンのタッチフィードバック改善
        document.addEventListener('touchstart', (e) => {
            if (e.target.matches('button, .button, input[type="button"], input[type="submit"]')) {
                e.target.style.transform = 'scale(0.95)';
            }
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            if (e.target.matches('button, .button, input[type="button"], input[type="submit"]')) {
                setTimeout(() => {
                    e.target.style.transform = '';
                }, 100);
            }
        }, { passive: true });
    }

    /**
     * フォーカス管理
     */
    setupFocusManagement() {
        // タッチデバイスでのアウトライン制御
        document.addEventListener('mousedown', () => {
            document.body.classList.add('using-mouse');
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.remove('using-mouse');
            }
        });
    }

    /**
     * タッチ操作最適化
     */
    setupTouchOptimizations() {
        // スロット要素のタッチ最適化
        this.optimizeSlotTouchEvents();
        
        // 制御パネルのタッチ最適化
        this.optimizeControlPanelTouch();
        
        // ボタンのタッチ領域拡大
        this.expandTouchTargets();
    }

    /**
     * スロット要素のタッチ最適化
     */
    optimizeSlotTouchEvents() {
        document.addEventListener('touchstart', (e) => {
            if (e.target.closest('.slot, [class*="slot-"]')) {
                const slot = e.target.closest('.slot, [class*="slot-"]');
                slot.classList.add('touch-active');
                this.touchStartTime = Date.now();
            }
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            const touchDuration = Date.now() - this.touchStartTime;
            const slot = e.target.closest('.slot, [class*="slot-"]');
            
            if (slot) {
                slot.classList.remove('touch-active');
                
                // 長押し検出（600ms以上）
                if (touchDuration > 600) {
                    this.handleLongPress(slot);
                }
            }
        }, { passive: true });
    }

    /**
     * 長押し処理
     */
    handleLongPress(element) {
        // 詳細ボタンがある場合は自動クリック
        const detailButton = element.querySelector('button[onclick*="toggle"], .detail-button');
        if (detailButton) {
            detailButton.click();
        }
        
        // 視覚的フィードバック
        element.style.animation = 'longPressEffect 0.3s ease';
        setTimeout(() => {
            element.style.animation = '';
        }, 300);
    }

    /**
     * 制御パネルのタッチ最適化
     */
    optimizeControlPanelTouch() {
        // 制御パネルのスワイプ操作
        let startY = 0;
        let currentY = 0;
        
        document.addEventListener('touchstart', (e) => {
            if (e.target.closest('.control-panel, .subslot-control-panel')) {
                startY = e.touches[0].clientY;
            }
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            if (e.target.closest('.control-panel, .subslot-control-panel')) {
                currentY = e.touches[0].clientY;
                const diff = startY - currentY;
                
                // 上スワイプで表示、下スワイプで非表示
                if (Math.abs(diff) > 50) {
                    const panel = e.target.closest('.control-panel, .subslot-control-panel');
                    if (diff > 0) {
                        panel.style.transform = 'translateY(-10px)';
                    } else {
                        panel.style.transform = 'translateY(10px)';
                    }
                }
            }
        }, { passive: true });
    }

    /**
     * タッチ領域拡大
     */
    expandTouchTargets() {
        const smallButtons = document.querySelectorAll('button:not(.touch-optimized)');
        smallButtons.forEach(button => {
            const rect = button.getBoundingClientRect();
            if (rect.width < 44 || rect.height < 44) {
                button.classList.add('touch-optimized');
                button.style.minHeight = '44px';
                button.style.minWidth = '44px';
                button.style.padding = '12px';
            }
        });
    }

    /**
     * キーボード最適化
     */
    setupKeyboardOptimizations() {
        // ソフトキーボード表示時の対応
        if (this.isMobile) {
            window.addEventListener('resize', () => {
                this.handleSoftKeyboard();
            });
        }
        
        // Enterキーでの操作改善
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.matches('button, .button')) {
                e.target.click();
            }
        });
    }

    /**
     * ソフトキーボード処理
     */
    handleSoftKeyboard() {
        const initialHeight = window.innerHeight;
        const currentHeight = window.innerHeight;
        const heightDifference = initialHeight - currentHeight;
        
        if (heightDifference > 150) {
            // キーボードが表示されている
            document.body.classList.add('keyboard-visible');
            
            // フォーカス要素を画面中央に
            const focusedElement = document.activeElement;
            if (focusedElement && focusedElement.scrollIntoView) {
                setTimeout(() => {
                    focusedElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 300);
            }
        } else {
            document.body.classList.remove('keyboard-visible');
        }
    }

    /**
     * 音声システム最適化
     */
    setupVoiceSystemOptimizations() {
        // 音声ボタンのタッチ最適化
        document.addEventListener('DOMContentLoaded', () => {
            const voiceButtons = document.querySelectorAll('.voice-button, .record-button, .play-button');
            voiceButtons.forEach(button => {
                // タッチ開始で視覚的フィードバック
                button.addEventListener('touchstart', () => {
                    button.style.transform = 'scale(1.1)';
                    button.style.filter = 'brightness(1.2)';
                }, { passive: true });
                
                button.addEventListener('touchend', () => {
                    setTimeout(() => {
                        button.style.transform = '';
                        button.style.filter = '';
                    }, 100);
                }, { passive: true });
            });
        });
        
        // 長押し録音機能
        this.setupLongPressRecording();
    }

    /**
     * 長押し録音機能
     */
    setupLongPressRecording() {
        let recordingTimeout;
        
        document.addEventListener('touchstart', (e) => {
            if (e.target.matches('.record-button, .voice-button[data-action="record"]')) {
                recordingTimeout = setTimeout(() => {
                    // 長押し録音開始
                    console.log('🎤 Long press recording started');
                    e.target.classList.add('long-press-recording');
                }, 500);
            }
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            if (recordingTimeout) {
                clearTimeout(recordingTimeout);
            }
            
            if (e.target.matches('.record-button, .voice-button[data-action="record"]')) {
                e.target.classList.remove('long-press-recording');
            }
        }, { passive: true });
    }

    /**
     * 画面向き変更処理
     */
    setupOrientationHandling() {
        window.addEventListener('orientationchange', () => {
            // 向き変更時の処理
            setTimeout(() => {
                this.setViewportHeight();
                this.adjustLayoutForOrientation();
            }, 100);
        });
    }

    /**
     * 画面向きに応じたレイアウト調整
     */
    adjustLayoutForOrientation() {
        const isLandscape = window.innerWidth > window.innerHeight;
        
        if (isLandscape) {
            document.body.classList.add('landscape');
            document.body.classList.remove('portrait');
        } else {
            document.body.classList.add('portrait');
            document.body.classList.remove('landscape');
        }
        
        // 音声コントロールパネルの位置調整
        const voicePanel = document.querySelector('.voice-control-panel');
        if (voicePanel && this.isMobile) {
            if (isLandscape) {
                voicePanel.style.position = 'relative';
                voicePanel.style.bottom = 'auto';
            } else {
                voicePanel.style.position = 'fixed';
                voicePanel.style.bottom = '0';
            }
        }
    }

    /**
     * パフォーマンス監視
     */
    monitorPerformance() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.entryType === 'measure' && entry.duration > 100) {
                        console.warn(`⚠️ Slow operation detected: ${entry.name} (${entry.duration}ms)`);
                    }
                });
            });
            
            observer.observe({ entryTypes: ['measure'] });
        }
    }
}

// CSS アニメーション追加
const mobileAnimationCSS = `
<style>
@keyframes longPressEffect {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.touch-active {
    transform: scale(0.98);
    transition: transform 0.1s ease;
}

.long-press-recording {
    animation: pulse 1s infinite;
    box-shadow: 0 0 20px rgba(244, 67, 54, 0.5);
}

.mobile-optimized .keyboard-visible {
    padding-bottom: 0;
}

.mobile-optimized .landscape .voice-control-panel {
    border-radius: 8px;
    margin: 16px 8px;
    position: relative !important;
}

.mobile-optimized .portrait .voice-control-panel {
    border-radius: 16px 16px 0 0;
    margin: 0;
    position: fixed !important;
    bottom: 0 !important;
}

/* タッチフィードバック改善 */
.using-mouse button:focus {
    outline: none;
}

button:not(.using-mouse):focus {
    outline: 2px solid #4CAF50;
    outline-offset: 2px;
}
</style>
`;

// CSS をヘッドに追加
document.head.insertAdjacentHTML('beforeend', mobileAnimationCSS);

// グローバルに公開
window.MobileOptimizer = MobileOptimizer;

// 自動初期化
window.mobileOptimizer = new MobileOptimizer();

// エクスポート（ES6モジュール対応）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileOptimizer;
}

console.log('📱 Mobile Optimization System loaded successfully');
