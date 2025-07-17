/**
 * Rephraseプロジェクト レスポンシブ統合システム
 * 作成日: 2025年7月17日
 * 目的: 既存のスロット要素をレスポンシブクラスに統合
 */

class ResponsiveIntegration {
    constructor() {
        this.isIntegrated = false;
        this.integrationTimeout = null;
    }
    
    /**
     * 既存の要素をレスポンシブ対応に統合
     */
    integrateExistingElements() {
        if (this.isIntegrated) return;
        
        console.log('🔗 既存要素のレスポンシブ統合開始');
        
        try {
            // メインコンテナの統合
            this.integrateMainContainer();
            
            // スロット要素の統合
            this.integrateSlotElements();
            
            // 画像要素の統合
            this.integrateImageElements();
            
            // コントロール要素の統合
            this.integrateControlElements();
            
            // ナビゲーション要素の統合
            this.integrateNavigationElements();
            
            this.isIntegrated = true;
            console.log('✅ レスポンシブ統合完了');
            
            // 統合後に最適化を実行
            if (window.responsiveOptimizer) {
                setTimeout(() => {
                    window.responsiveOptimizer.forceOptimization();
                }, 200);
            }
            
        } catch (error) {
            console.error('❌ レスポンシブ統合エラー:', error);
        }
    }
    
    /**
     * メインコンテナの統合
     */
    integrateMainContainer() {
        const body = document.body;
        
        // メインコンテナが存在しない場合は作成
        let mainContainer = document.querySelector('.main-container');
        if (!mainContainer) {
            mainContainer = document.createElement('div');
            mainContainer.className = 'main-container';
            
            // 既存のコンテンツを移動
            const existingContent = document.querySelector('#main-content');
            if (existingContent) {
                mainContainer.appendChild(existingContent);
            } else {
                // main-contentが無い場合、body内の主要コンテンツを移動
                const children = Array.from(body.children).filter(child => 
                    !child.id?.includes('loading') && 
                    !child.tagName?.toLowerCase() === 'script' &&
                    !child.tagName?.toLowerCase() === 'style'
                );
                
                children.forEach(child => {
                    if (child !== mainContainer) {
                        mainContainer.appendChild(child);
                    }
                });
            }
            
            body.appendChild(mainContainer);
        }
        
        console.log('📦 メインコンテナ統合完了');
    }
    
    /**
     * スロット要素の統合
     */
    integrateSlotElements() {
        // 既存のスロット要素を特定
        const slotElements = document.querySelectorAll('[id^="slot-"], .slot');
        const sentenceArea = document.querySelector('#static-slot-area, .sentence-display-area');
        
        if (sentenceArea && !sentenceArea.classList.contains('sentence-display-area')) {
            sentenceArea.classList.add('sentence-display-area');
        }
        
        slotElements.forEach(slot => {
            if (!slot.classList.contains('slot-container')) {
                slot.classList.add('slot-container');
            }
            
            // スロット内の要素を整理
            this.organizeSlotContent(slot);
        });
        
        console.log(`🎯 スロット要素統合完了: ${slotElements.length}個`);
    }
    
    /**
     * スロット内コンテンツの整理
     */
    organizeSlotContent(slotElement) {
        // ラベル要素の整理
        const labels = slotElement.querySelectorAll('label, .slot-label');
        labels.forEach(label => {
            if (!label.classList.contains('slot-label')) {
                label.classList.add('slot-label');
            }
        });
        
        // テキスト要素の整理
        const textElements = slotElement.querySelectorAll('.slot-text, .dynamic-text, [class*="text"]');
        textElements.forEach(text => {
            if (!text.classList.contains('slot-text') && 
                !text.classList.contains('slot-phrase')) {
                // 内容に基づいて判定
                if (text.textContent?.length > 20) {
                    text.classList.add('slot-phrase');
                } else {
                    text.classList.add('slot-text');
                }
            }
        });
        
        // 画像要素の整理
        const images = slotElement.querySelectorAll('img');
        images.forEach(img => {
            if (!img.classList.contains('slot-image') && 
                !img.classList.contains('slot-multi-image')) {
                img.classList.add('slot-image');
            }
        });
        
        // 音声制御要素の整理
        const voiceElements = slotElement.querySelectorAll('[class*="voice"], [data-voice]');
        voiceElements.forEach(voice => {
            if (!voice.closest('.voice-control-area')) {
                let voiceArea = slotElement.querySelector('.voice-control-area');
                if (!voiceArea) {
                    voiceArea = document.createElement('div');
                    voiceArea.className = 'voice-control-area';
                    slotElement.appendChild(voiceArea);
                }
                voiceArea.appendChild(voice);
            }
        });
    }
    
    /**
     * 画像要素の統合
     */
    integrateImageElements() {
        // 複数画像コンテナの処理
        const imageGroups = document.querySelectorAll('[class*="multi-image"], [class*="images"]');
        imageGroups.forEach(group => {
            if (!group.classList.contains('multi-image-container')) {
                group.classList.add('multi-image-container');
            }
            
            const images = group.querySelectorAll('img');
            images.forEach(img => {
                if (!img.classList.contains('slot-multi-image')) {
                    img.classList.add('slot-multi-image');
                }
            });
        });
        
        // 単独画像の処理
        const singleImages = document.querySelectorAll('img:not(.slot-multi-image)');
        singleImages.forEach(img => {
            if (!img.classList.contains('slot-image')) {
                img.classList.add('slot-image');
            }
        });
        
        console.log('🖼️ 画像要素統合完了');
    }
    
    /**
     * コントロール要素の統合
     */
    integrateControlElements() {
        // コントロールパネルエリアの作成・統合
        const controlElements = document.querySelectorAll('button, .control, [class*="control"]');
        const existingPanels = document.querySelectorAll('[class*="control-panel"], [id*="control"]');
        
        existingPanels.forEach(panel => {
            if (!panel.classList.contains('control-panel')) {
                panel.classList.add('control-panel');
            }
        });
        
        // ボタン要素のクラス統合
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            if (button.textContent?.includes('音声') || button.id?.includes('voice')) {
                if (!button.classList.contains('voice-btn')) {
                    button.classList.add('voice-btn');
                }
            } else if (!button.classList.contains('control-btn') && 
                      !button.classList.contains('voice-btn')) {
                button.classList.add('control-btn');
            }
        });
        
        console.log('🎛️ コントロール要素統合完了');
    }
    
    /**
     * ナビゲーション要素の統合
     */
    integrateNavigationElements() {
        // ナビゲーションエリアの特定・作成
        const navElements = document.querySelectorAll('nav, .navigation, [class*="nav"]');
        const topFixedElements = document.querySelectorAll('[style*="fixed"], [style*="top"]');
        
        topFixedElements.forEach(element => {
            if (element.style.position === 'fixed' && 
                parseInt(element.style.top) < 100) {
                if (!element.classList.contains('navigation-area')) {
                    element.classList.add('navigation-area');
                }
            }
        });
        
        console.log('🧭 ナビゲーション要素統合完了');
    }
    
    /**
     * 動的要素の監視と統合
     */
    setupDynamicIntegration() {
        const observer = new MutationObserver((mutations) => {
            let needsReintegration = false;
            
            mutations.forEach(mutation => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // 新しいスロット要素が追加された
                            if (node.id?.startsWith('slot-') || node.classList?.contains('slot')) {
                                needsReintegration = true;
                            }
                            
                            // 新しい画像要素が追加された
                            if (node.tagName === 'IMG' || node.querySelector('img')) {
                                needsReintegration = true;
                            }
                        }
                    });
                }
            });
            
            if (needsReintegration) {
                clearTimeout(this.integrationTimeout);
                this.integrationTimeout = setTimeout(() => {
                    console.log('🔄 動的要素の再統合実行');
                    this.integrateSlotElements();
                    this.integrateImageElements();
                    
                    if (window.responsiveOptimizer) {
                        window.responsiveOptimizer.forceOptimization();
                    }
                }, 300);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'id', 'style']
        });
        
        console.log('👁️ 動的要素監視開始');
    }
    
    /**
     * 手動統合トリガー
     */
    forceIntegration() {
        this.isIntegrated = false;
        this.integrateExistingElements();
    }
    
    /**
     * 統合状態の確認
     */
    getIntegrationStatus() {
        return {
            isIntegrated: this.isIntegrated,
            mainContainers: document.querySelectorAll('.main-container').length,
            slotContainers: document.querySelectorAll('.slot-container').length,
            sentenceAreas: document.querySelectorAll('.sentence-display-area').length,
            imageElements: document.querySelectorAll('.slot-image, .slot-multi-image').length,
            controlPanels: document.querySelectorAll('.control-panel').length
        };
    }
}

// グローバルインスタンス作成
window.responsiveIntegration = new ResponsiveIntegration();

// DOM読み込み後に統合を実行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            window.responsiveIntegration.integrateExistingElements();
            window.responsiveIntegration.setupDynamicIntegration();
        }, 100);
    });
} else {
    setTimeout(() => {
        window.responsiveIntegration.integrateExistingElements();
        window.responsiveIntegration.setupDynamicIntegration();
    }, 100);
}

// デバッグ用関数
window.debugIntegration = {
    status: () => window.responsiveIntegration.getIntegrationStatus(),
    force: () => window.responsiveIntegration.forceIntegration()
};

console.log('🔗 レスポンシブ統合システム読み込み完了');
console.log('💡 デバッグコマンド: window.debugIntegration.status(), .force()');
