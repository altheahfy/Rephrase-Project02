/**
 * Rephraseプロジェクト 手動ズーム調整システム
 * 作成日: 2025年7月17日
 * 目的: ユーザーが手動でコンテンツサイズを調整できる機能
 */

console.log('🚀 manual_zoom_controller.js ファイル読み込み開始');

class ManualZoomController {
    constructor() {
        this.currentZoom = 1.0; // デフォルトは中央（100%）
        this.minZoom = 0.5; // 縮小範囲
        this.maxZoom = 1.5; // 拡大範囲
        this.zoomStep = 0.1;
        this.targetSelector = '.slot-container'; // 上位・サブスロットのみ対象
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
        const toolbar = document.querySelector('div[style*="position: fixed"][style*="top: 10px"][style*="left: 10px"]');
        console.log('🔍 ツールバー要素:', toolbar);
        
        if (!toolbar) {
            console.warn('⚠️ ツールバー要素が見つかりません。1秒後に再試行します');
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
        console.log('📊 パネル要素:', this.controlPanel);
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
        
        // パネル要素を作成（シンプルなスライダーのみ）
        this.controlPanel = document.createElement('div');
        this.controlPanel.id = 'zoom-control-panel';
        this.controlPanel.innerHTML = `
            <span class="zoom-label">🔍</span>
            <input type="range" 
                   id="zoom-slider" 
                   min="${this.minZoom}" 
                   max="${this.maxZoom}" 
                   step="${this.zoomStep}" 
                   value="${this.currentZoom}"
                   title="表示サイズ調整">
            <span id="zoom-percentage">${Math.round(this.currentZoom * 100)}%</span>
        `;
        
        // ツールバーに追加
        const toolbar = document.querySelector('div[style*="position: fixed"][style*="top: 10px"][style*="left: 10px"]');
        if (toolbar) {
            // 区切り線を追加
            const separator = document.createElement('span');
            separator.style.cssText = 'color: #ccc; margin: 0 8px;';
            separator.textContent = '|';
            toolbar.appendChild(separator);
            
            // パネルを追加
            toolbar.appendChild(this.controlPanel);
        } else {
            // フォールバック: bodyに追加
            document.body.appendChild(this.controlPanel);
        }
        
        // スタイルを設定（インライン要素として）
        this.controlPanel.style.cssText = `
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: Arial, sans-serif;
            font-size: 10px;
            border: 1px solid rgba(255,255,255,0.2);
        `;
        
        // イベントリスナーを設定
        this.setupPanelEvents();
        
        // シンプルなスライダー用CSS
        this.injectSimpleStyles();
    }
    
    /**
     * シンプルなスライダー用スタイルを注入
     */
    injectSimpleStyles() {
        const style = document.createElement('style');
        style.id = 'zoom-panel-styles';
        style.innerHTML = `
            .zoom-label {
                font-size: 12px;
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
        // スライダーのみ
        const slider = this.controlPanel.querySelector('#zoom-slider');
        if (slider) {
            slider.addEventListener('input', (e) => {
                this.setZoom(parseFloat(e.target.value));
            });
        }
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
                this.setZoom(1.0); // 中央（100%）にリセット
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
        const targetElements = document.querySelectorAll(this.targetSelector);
        
        targetElements.forEach(element => {
            if (element) {
                // 左右位置関係を保つため、左上基準でスケール
                element.style.transform = `scale(${this.currentZoom})`;
                element.style.transformOrigin = 'top left';
                element.style.transition = 'transform 0.3s ease';
            }
        });
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
                const savedZoom = parseFloat(saved);
                // 古い範囲の値（0.3-1.2）をリセット
                if (savedZoom < this.minZoom || savedZoom > this.maxZoom) {
                    console.log(`⚠️ 古いズーム値 ${savedZoom} をリセットします`);
                    this.currentZoom = 1.0; // デフォルトに戻す
                    localStorage.removeItem(this.storageKey); // 古い値を削除
                } else {
                    this.currentZoom = savedZoom;
                    console.log(`💾 保存されたズームレベルを読み込み: ${Math.round(this.currentZoom * 100)}%`);
                }
            } else {
                this.currentZoom = 1.0; // デフォルト値
            }
        } catch (error) {
            console.warn('ズームレベルの読み込みに失敗:', error);
            this.currentZoom = 1.0; // エラー時はデフォルト
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
        this.setZoom(1.0); // 中央（100%）にリセット
    }
}

// グローバルインスタンス作成
window.manualZoomController = new ManualZoomController();

// 古いLocalStorageをクリア（一度だけ実行）
const migrationKey = 'rephrase_zoom_migration_v2';
if (!localStorage.getItem(migrationKey)) {
    localStorage.removeItem('rephrase_zoom_level');
    localStorage.setItem(migrationKey, 'true');
    console.log('🔄 古いズーム設定をリセットしました');
}

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
    status: () => window.manualZoomController.getStatus(),
    setZoom: (zoom) => window.manualZoomController.setZoom(zoom),
    reset: () => window.manualZoomController.reset(),
    toggle: () => window.manualZoomController.toggleVisibility()
};

console.log('🔍 手動ズーム調整システム読み込み完了');
console.log('💡 使用方法:');
console.log('  - Ctrl + + : 拡大');
console.log('  - Ctrl + - : 縮小');
console.log('  - Ctrl + 0 : リセット');
console.log('  - 右上のパネルでマウス操作');
console.log('🛠️ デバッグ: window.debugZoom.status(), .setZoom(1.2), .reset()');
