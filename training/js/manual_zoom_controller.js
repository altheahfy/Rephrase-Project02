/**
 * Rephraseプロジェクト 手動ズーム調整システム
 * 作成日: 2025年7月17日
 * 目的: ユーザーが手動でコンテンツサイズを調整できる機能
 */

class ManualZoomController {
    constructor() {
        this.currentZoom = 0.8; // 縮小をデフォルトに
        this.minZoom = 0.4;
        this.maxZoom = 1.5;
        this.zoomStep = 0.1;
        this.targetSelector = '#main-content';
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
        const toolbar = document.querySelector('div[style*="position: fixed"][style*="top: 10px"][style*="left: 10px"]');
        console.log('🔍 main-content要素:', mainContent);
        console.log('🔍 ツールバー要素:', toolbar);
        
        if (!mainContent) {
            console.warn('⚠️ main-content要素が見つかりません。1秒後に再試行します');
            setTimeout(() => this.initialize(), 1000);
            return;
        }
        
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
                <span class="zoom-label">🔍</span>
                <input type="range" 
                       id="zoom-slider" 
                       min="${this.minZoom}" 
                       max="${this.maxZoom}" 
                       step="${this.zoomStep}" 
                       value="${this.currentZoom}"
                       title="表示サイズ調整">
                <span id="zoom-percentage">${Math.round(this.currentZoom * 100)}%</span>
            </div>
        `;
        
        // ツールバーの正確な位置に追加
        const toolbar = document.querySelector('div[style*="position: fixed"][style*="top: 10px"][style*="left: 10px"]');
        if (toolbar) {
            // 区切り線を追加
            const separator = document.createElement('span');
            separator.style.cssText = 'color: #ccc;';
            separator.textContent = '|';
            toolbar.appendChild(separator);
            
            // パネルを直接ツールバーに追加
            toolbar.appendChild(this.controlPanel);
        } else {
            // フォールバック: bodyに追加
            document.body.appendChild(this.controlPanel);
        }
        
        // スタイルを設定
        this.controlPanel.style.cssText = `
            display: inline-flex;
            align-items: center;
            margin-left: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;
            font-size: 10px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        `;
        
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
                align-items: center;
                gap: 6px;
            }
            
            .zoom-label {
                font-size: 12px;
                margin-right: 2px;
            }
            
            #zoom-percentage {
                font-weight: bold;
                font-size: 10px;
                min-width: 35px;
                text-align: center;
            }
            
            #zoom-slider {
                width: 80px;
                height: 3px;
                background: rgba(255,255,255,0.3);
                border-radius: 2px;
                outline: none;
                cursor: pointer;
                margin: 0 4px;
            }
            
            #zoom-slider::-webkit-slider-thumb {
                appearance: none;
                width: 12px;
                height: 12px;
                background: white;
                border-radius: 50%;
                cursor: pointer;
                box-shadow: 0 1px 3px rgba(0,0,0,0.3);
            }
            
            #zoom-slider::-moz-range-thumb {
                width: 12px;
                height: 12px;
                background: white;
                border-radius: 50%;
                cursor: pointer;
                border: none;
                box-shadow: 0 1px 3px rgba(0,0,0,0.3);
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
        const slider = this.controlPanel.querySelector('#zoom-slider');
        
        // デバッグ: 要素の存在確認
        console.log('🔧 スライダー:', slider);
        
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
                this.setZoom(0.8); // 縮小デフォルトに
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
                
                // main-content全体にスケール適用（スロット間隔も含めて）
                element.style.transform = `scale(${this.currentZoom})`;
                element.style.transformOrigin = 'top left'; // 左上を基準点に
                element.style.transition = 'transform 0.3s ease';
                
                // スケール後の高さ調整
                element.style.minHeight = `${100 * this.currentZoom}vh`;
                
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
            } else {
                // 初回時は縮小デフォルト
                this.currentZoom = 0.8;
                console.log(`🔍 初回起動 - デフォルト縮小レベル: ${Math.round(this.currentZoom * 100)}%`);
            }
        } catch (error) {
            console.warn('ズームレベルの読み込みに失敗:', error);
            this.currentZoom = 0.8; // エラー時も縮小デフォルト
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
        this.setZoom(0.8); // 縮小デフォルトに
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
