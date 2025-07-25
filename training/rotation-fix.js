/* =================================================================== */
/* 📱 画面回転ずれ問題解決用JavaScript                                */
/* =================================================================== */

(function() {
    'use strict';
    
    // 画面回転検知と自動修正
    function fixLayoutAfterRotation() {
        console.log('画面回転検知：レイアウト修正を実行');
        
        // 短時間遅延後にスタイルを強制再適用
        setTimeout(() => {
            const slotWrappers = document.querySelectorAll('.mobile-device .slot-wrapper:not([id$="-sub"])');
            const subslotArea = document.querySelector('.mobile-device #subslot-display-area');
            
            slotWrappers.forEach(wrapper => {
                // スタイルを一旦リセットして強制再適用
                wrapper.style.cssText = '';
                
                // 基本スタイルを強制再適用
                setTimeout(() => {
                    wrapper.style.height = '40vh';
                    wrapper.style.paddingTop = '8px';
                    wrapper.style.alignItems = 'flex-start';
                    wrapper.style.display = 'flex';
                    wrapper.style.justifyContent = 'flex-start';
                    wrapper.style.width = 'calc(100vw - 4px)';
                    wrapper.style.minWidth = 'calc(100vw - 4px)';
                    wrapper.style.maxWidth = 'calc(100vw - 4px)';
                    wrapper.style.margin = '2px';
                    wrapper.style.border = '2px solid #007bff';
                    wrapper.style.borderRadius = '4px';
                    wrapper.style.background = 'rgba(240, 248, 255, 0.9)';
                    wrapper.style.overflowX = 'auto';
                    wrapper.style.overflowY = 'auto';
                    wrapper.style.touchAction = 'pan-x pan-y';
                }, 50);
            });
            
            if (subslotArea) {
                // サブスロットエリアも同様に修正
                subslotArea.style.cssText = '';
                setTimeout(() => {
                    subslotArea.style.height = '12vh';
                    subslotArea.style.width = 'calc(100vw - 4px)';
                    subslotArea.style.maxWidth = 'calc(100vw - 4px)';
                    subslotArea.style.minWidth = 'calc(100vw - 4px)';
                }, 50);
            }
            
            console.log('レイアウト修正完了');
        }, 100);
    }
    
    // 画面回転イベントリスナー
    window.addEventListener('orientationchange', fixLayoutAfterRotation);
    
    // リサイズイベントでも対応
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(fixLayoutAfterRotation, 300);
    });
    
    // ページ読み込み時に初期設定
    document.addEventListener('DOMContentLoaded', () => {
        console.log('画面回転ずれ問題解決用JavaScript初期化完了');
    });
    
})();
