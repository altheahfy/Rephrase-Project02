/**
 * Rephraseプロジェクト 手動ズーム調整システム
 * 作成日: 2025年7月17日
 * 目的: ユーザーが手動でコンテンツサイズを調整できる機能
 */

class ManualZoomController {
    constructor() {
        this.currentZoom = 1.0;
        this.minZoom = 0.5;
        this.maxZoom = 2.0;
        this.zoomStep = 0.1;
        this.targetSelector = '#main-content, #dynamic-slot-area';
        this.storageKey = 'rephrase_zoom_level';
        
        this.isInitialized = false;
        this.controlPanel = null;
    }
    
    /**
     * システム初期化
     */
    initialize() {
        if (this.isInitialized) {
            console.log('⚠️ 手動ズーム調整システム既に初期化済み');
            return;
        }
        
        console.log('🔍 手動ズーム調整システム初期化開始');
        
        // DOM要素の存在確認
        const mainContent = document.getElementById('main-content');
        const dynamicArea = document.getElementById('dynamic-slot-area');
        console.log('🔍 main-content要素:', mainContent);
        console.log('🔍 dynamic-slot-area要素:', dynamicArea);
        
        // 保存されたズームレベルを読み込み
        this.loadZoomLevel();
        
        // コントロールパネルを作成
        this.createControlPanel();
        
        // 初期ズームを適用
        this.applyZoom();
        
        // キーボードショートカットを設定
        this.setupKeyboardShortcuts();
        
        this.isInitialized = true;
        console.log('✅ 手動ズーム調整システム初期化完了');
        
        // 状態をログ出力
        console.log('📊 システム状態:', this.getStatus());
    }
    
    /**
     * ズームコントロールパネルを作成
     */
    createControlPanel() {
        // 既存のパネルを削除
        const existing = document.getElementById('zoom-control-panel');
        if (existing) {
            existing.remove();
        }
        
        // パネル要素を作成
        this.controlPanel = document.createElement('div');
        this.controlPanel.id = 'zoom-control-panel';
        this.controlPanel.innerHTML = `
            <div class="zoom-panel-content">
                <div class="zoom-title">🔍 表示サイズ調整</div>
                <div class="zoom-controls">
                    <button class="zoom-btn zoom-out" id="zoom-out-btn" title="縮小 (Ctrl + -)">➖</button>
                    <div class="zoom-display">
                        <span id="zoom-percentage">${Math.round(this.currentZoom * 100)}%</span>
                        <input type="range" 
                               id="zoom-slider" 
                               min="${this.minZoom}" 
                               max="${this.maxZoom}" 
                               step="${this.zoomStep}" 
                               value="${this.currentZoom}"
                               title="ドラッグでサイズ調整">
                    </div>
                    <button class="zoom-btn zoom-in" id="zoom-in-btn" title="拡大 (Ctrl + +)">➕</button>
                </div>
                <div class="zoom-presets">
                    <button class="preset-btn" data-zoom="0.7" title="コンパクト表示">📱</button>
                    <button class="preset-btn" data-zoom="1.0" title="標準サイズ">💻</button>
                    <button class="preset-btn" data-zoom="1.3" title="大きく表示">🖥️</button>
                </div>
                <button class="zoom-toggle" id="zoom-panel-toggle" title="パネルを折りたたみ">📐</button>
            </div>
        `;
        
        // スタイルを設定
        this.controlPanel.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 16000;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            font-family: Arial, sans-serif;
            font-size: 12px;
            min-width: 200px;
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.2);
        `;
        
        // パネルをDOMに追加
        document.body.appendChild(this.controlPanel);
        
        // イベントリスナーを設定
        this.setupPanelEvents();
        
        // パネルのスタイルを追加
        this.injectPanelStyles();
    }
    
    /**
     * パネル用CSSスタイルを注入
     */
    injectPanelStyles() {
        const style = document.createElement('style');
        style.id = 'zoom-panel-styles';
        style.innerHTML = `
            .zoom-panel-content {
                display: flex;
                flex-direction: column;
                gap: 8px;
                align-items: center;
            }
            
            .zoom-title {
                font-weight: bold;
                font-size: 13px;
                text-align: center;
                margin-bottom: 4px;
            }
            
            .zoom-controls {
                display: flex;
                align-items: center;
                gap: 8px;
                background: rgba(255,255,255,0.1);
                padding: 8px;
                border-radius: 8px;
            }
            
            .zoom-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
            }
            
            .zoom-btn:hover {
                background: rgba(255,255,255,0.3);
                transform: scale(1.1);
            }
            
            .zoom-btn:active {
                transform: scale(0.95);
            }
            
            .zoom-display {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
                min-width: 80px;
            }
            
            #zoom-percentage {
                font-weight: bold;
                font-size: 14px;
                text-align: center;
                min-width: 45px;
            }
            
            #zoom-slider {
                width: 100px;
                height: 4px;
                background: rgba(255,255,255,0.3);
                border-radius: 2px;
                outline: none;
                cursor: pointer;
            }
            
            #zoom-slider::-webkit-slider-thumb {
                appearance: none;
                width: 16px;
                height: 16px;
                background: white;
                border-radius: 50%;
                cursor: pointer;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            }
            
            #zoom-slider::-moz-range-thumb {
                width: 16px;
                height: 16px;
                background: white;
                border-radius: 50%;
                cursor: pointer;
                border: none;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            }
            
            .zoom-presets {
                display: flex;
                gap: 6px;
                margin-top: 4px;
            }
            
            .preset-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 32px;
                height: 24px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s ease;
            }
            
            .preset-btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-1px);
            }
            
            .preset-btn.active {
                background: rgba(255,255,255,0.4);
                box-shadow: 0 0 8px rgba(255,255,255,0.3);
            }
            
            .zoom-toggle {
                background: rgba(255,255,255,0.15);
                border: none;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 10px;
                margin-top: 4px;
                transition: all 0.2s ease;
            }
            
            .zoom-toggle:hover {
                background: rgba(255,255,255,0.25);
            }
            
            /* 折りたたみ状態 */
            #zoom-control-panel.collapsed {
                width: 40px;
                height: 40px;
                padding: 8px;
                overflow: hidden;
            }
            
            #zoom-control-panel.collapsed .zoom-panel-content {
                transform: scale(0);
                opacity: 0;
            }
            
            #zoom-control-panel.collapsed::after {
                content: "🔍";
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 16px;
                cursor: pointer;
            }
        `;
        
        document.head.appendChild(style);
    }
    
    /**
     * パネルイベントリスナーを設定
     */
    setupPanelEvents() {
        console.log('🔧 パネルイベントリスナー設定開始');
        
        // DOM要素を取得
        const zoomInBtn = this.controlPanel.querySelector('#zoom-in-btn');
        const zoomOutBtn = this.controlPanel.querySelector('#zoom-out-btn');
        const slider = this.controlPanel.querySelector('#zoom-slider');
        const presetBtns = this.controlPanel.querySelectorAll('.preset-btn');
        const toggleBtn = this.controlPanel.querySelector('#zoom-panel-toggle');
        
        // デバッグ: 要素の存在確認
        console.log('🔧 ズームインボタン:', zoomInBtn);
        console.log('🔧 ズームアウトボタン:', zoomOutBtn);
        console.log('🔧 スライダー:', slider);
        console.log('🔧 プリセットボタン数:', presetBtns.length);
        console.log('🔧 トグルボタン:', toggleBtn);
        
        // ズームイン・アウトボタン
        if (zoomInBtn) {
            zoomInBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('➕ ズームインボタンクリック');
                this.zoomIn();
            });
        }
        
        if (zoomOutBtn) {
            zoomOutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('➖ ズームアウトボタンクリック');
                this.zoomOut();
            });
        }
        
        // スライダー
        if (slider) {
            slider.addEventListener('input', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const zoom = parseFloat(e.target.value);
                console.log('🎚️ スライダー変更:', zoom);
                this.setZoom(zoom);
            });
        }
        
        // プリセットボタン
        presetBtns.forEach((btn, index) => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const zoom = parseFloat(btn.dataset.zoom);
                console.log(`📱 プリセットボタン${index + 1}クリック:`, zoom);
                this.setZoom(zoom);
            });
        });
        
        // 折りたたみボタン
        if (toggleBtn) {
            toggleBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('📐 トグルボタンクリック');
                this.togglePanel();
            });
        }
        
        // パネルの折りたたみ状態をクリックで展開
        this.controlPanel.addEventListener('click', (e) => {
            if (this.controlPanel.classList.contains('collapsed')) {
                console.log('📐 折りたたみパネルクリック - 展開');
                this.togglePanel();
                e.stopPropagation();
            }
        });
        
        console.log('✅ パネルイベントリスナー設定完了');
    }
    
    /**
     * キーボードショートカットを設定
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + Plus (拡大)
            if (e.ctrlKey && (e.key === '+' || e.key === '=')) {
                e.preventDefault();
                this.zoomIn();
            }
            
            // Ctrl + Minus (縮小)
            if (e.ctrlKey && e.key === '-') {
                e.preventDefault();
                this.zoomOut();
            }
            
            // Ctrl + 0 (リセット)
            if (e.ctrlKey && e.key === '0') {
                e.preventDefault();
                this.setZoom(1.0);
            }
        });
    }
    
    /**
     * ズームイン
     */
    zoomIn() {
        const newZoom = Math.min(this.maxZoom, this.currentZoom + this.zoomStep);
        this.setZoom(newZoom);
    }
    
    /**
     * ズームアウト
     */
    zoomOut() {
        const newZoom = Math.max(this.minZoom, this.currentZoom - this.zoomStep);
        this.setZoom(newZoom);
    }
    
    /**
     * ズームレベルを設定
     */
    setZoom(zoom) {
        this.currentZoom = Math.max(this.minZoom, Math.min(this.maxZoom, zoom));
        this.applyZoom();
        this.updateUI();
        this.saveZoomLevel();
        
        console.log(`🔍 ズームレベル設定: ${Math.round(this.currentZoom * 100)}%`);
    }
    
    /**
     * ズームを適用
     */
    applyZoom() {
        console.log(`🔍 ズーム適用開始: ${Math.round(this.currentZoom * 100)}%`);
        
        const targetElements = document.querySelectorAll(this.targetSelector);
        console.log(`🔍 対象要素数: ${targetElements.length}`);
        console.log(`🔍 セレクター: ${this.targetSelector}`);
        
        let appliedCount = 0;
        targetElements.forEach((element, index) => {
            if (element) {
                console.log(`🔍 要素${index + 1}にズーム適用:`, element.id || element.className);
                element.style.transform = `scale(${this.currentZoom})`;
                element.style.transformOrigin = 'top center';
                element.style.transition = 'transform 0.3s ease';
                
                // スケール変更に伴うレイアウト調整
                const scaledHeight = element.scrollHeight * this.currentZoom;
                element.style.marginBottom = `${scaledHeight * 0.1}px`;
                appliedCount++;
            }
        });
        
        console.log(`✅ ズーム適用完了: ${appliedCount}個の要素に適用`);
    }
    
    /**
     * UIを更新
     */
    updateUI() {
        if (!this.controlPanel) return;
        
        // パーセンテージ表示を更新
        const percentageSpan = this.controlPanel.querySelector('#zoom-percentage');
        if (percentageSpan) {
            percentageSpan.textContent = `${Math.round(this.currentZoom * 100)}%`;
        }
        
        // スライダーを更新
        const slider = this.controlPanel.querySelector('#zoom-slider');
        if (slider) {
            slider.value = this.currentZoom;
        }
        
        // プリセットボタンのアクティブ状態を更新
        const presetBtns = this.controlPanel.querySelectorAll('.preset-btn');
        presetBtns.forEach(btn => {
            const presetZoom = parseFloat(btn.dataset.zoom);
            if (Math.abs(presetZoom - this.currentZoom) < 0.05) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }
    
    /**
     * パネルの折りたたみ切り替え
     */
    togglePanel() {
        this.controlPanel.classList.toggle('collapsed');
        
        const toggleBtn = this.controlPanel.querySelector('#zoom-panel-toggle');
        if (this.controlPanel.classList.contains('collapsed')) {
            toggleBtn.textContent = '📐';
        } else {
            toggleBtn.textContent = '📐';
        }
    }
    
    /**
     * ズームレベルを保存
     */
    saveZoomLevel() {
        try {
            localStorage.setItem(this.storageKey, this.currentZoom.toString());
        } catch (error) {
            console.warn('ズームレベルの保存に失敗:', error);
        }
    }
    
    /**
     * ズームレベルを読み込み
     */
    loadZoomLevel() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (saved) {
                this.currentZoom = parseFloat(saved);
                console.log(`💾 保存されたズームレベルを読み込み: ${Math.round(this.currentZoom * 100)}%`);
            }
        } catch (error) {
            console.warn('ズームレベルの読み込みに失敗:', error);
        }
    }
    
    /**
     * システム状態を取得
     */
    getStatus() {
        return {
            isInitialized: this.isInitialized,
            currentZoom: this.currentZoom,
            zoomPercentage: Math.round(this.currentZoom * 100),
            minZoom: this.minZoom,
            maxZoom: this.maxZoom,
            targetSelector: this.targetSelector
        };
    }
    
    /**
     * パネルの表示/非表示
     */
    toggleVisibility() {
        if (this.controlPanel) {
            this.controlPanel.style.display = 
                this.controlPanel.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    /**
     * システムリセット
     */
    reset() {
        this.setZoom(1.0);
        this.controlPanel?.classList.remove('collapsed');
    }
}

// グローバルインスタンス作成
window.manualZoomController = new ManualZoomController();

// DOM読み込み完了時に初期化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            window.manualZoomController.initialize();
        }, 1000); // 他のシステムの初期化を待つ
    });
} else {
    setTimeout(() => {
        window.manualZoomController.initialize();
    }, 1000);
}

// デバッグ用グローバル関数
window.debugZoom = {
    status: () => {
        console.log('📊 ズームシステム状態:', window.manualZoomController.getStatus());
        return window.manualZoomController.getStatus();
    },
    setZoom: (zoom) => {
        console.log(`🔧 手動ズーム設定: ${zoom}`);
        window.manualZoomController.setZoom(zoom);
    },
    reset: () => {
        console.log('🔄 ズームリセット');
        window.manualZoomController.reset();
    },
    toggle: () => {
        console.log('👁️ パネル表示切り替え');
        window.manualZoomController.toggleVisibility();
    },
    reinitialize: () => {
        console.log('🔄 システム再初期化');
        window.manualZoomController.isInitialized = false;
        window.manualZoomController.initialize();
    },
    testButtons: () => {
        console.log('🧪 ボタンテスト実行');
        const panel = document.getElementById('zoom-control-panel');
        if (panel) {
            const buttons = panel.querySelectorAll('button');
            console.log(`🧪 パネル内ボタン数: ${buttons.length}`);
            buttons.forEach((btn, i) => {
                console.log(`🧪 ボタン${i + 1}:`, btn.id || btn.className, btn);
            });
        } else {
            console.log('❌ ズームパネルが見つかりません');
        }
    }
};

console.log('🔍 手動ズーム調整システム読み込み完了');
console.log('💡 使用方法:');
console.log('  - Ctrl + + : 拡大');
console.log('  - Ctrl + - : 縮小');
console.log('  - Ctrl + 0 : リセット');
console.log('  - 右上のパネルでマウス操作');
console.log('🛠️ デバッグコマンド:');
console.log('  - debugZoom.status() : 状態確認');
console.log('  - debugZoom.setZoom(1.2) : ズーム設定');
console.log('  - debugZoom.testButtons() : ボタン動作確認');
console.log('  - debugZoom.reinitialize() : 再初期化');
