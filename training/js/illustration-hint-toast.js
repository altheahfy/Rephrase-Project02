// 💡 イラストヒントトーストシステム
// 英語OFFボタンを押した際に、イラストをハイライトしてヒントを表示

(function() {
  'use strict';
  
  /**
   * トーストを表示してイラストをハイライト
   * @param {HTMLElement} triggerButton - クリックされたボタン要素
   */
  function showIllustrationHintToast(triggerButton) {
    // localStorage で「今後表示しない」設定を確認
    const dismissed = localStorage.getItem('illustration_hint_dismissed');
    if (dismissed === 'true') {
      console.log('💡 イラストヒント: ユーザーが非表示設定済み');
      return;
    }
    
    console.log('💡 イラストヒントトーストを表示', triggerButton);
    
    // トリガーボタンから親スロットを探す
    let targetSlot = null;
    if (triggerButton) {
      targetSlot = triggerButton.closest('.slot-container') || 
                   triggerButton.closest('.subslot-container') ||
                   triggerButton.closest('#display-top-question-word');
    }
    
    // ターゲットスロット内のイラストを取得
    let targetImage = null;
    if (targetSlot) {
      targetImage = targetSlot.querySelector('.slot-image');
      console.log('🎯 ターゲットスロット:', targetSlot.id || targetSlot.className);
      console.log('🎯 ターゲットイラスト:', targetImage);
    }
    
    // イラストがない場合は全スロットのイラストをハイライト
    const images = targetImage ? [targetImage] : Array.from(document.querySelectorAll('.slot-image'));
    const highlightedImages = [];
    
    images.forEach(img => {
      const hasImage = img.style.backgroundImage && img.style.backgroundImage !== 'none' && img.style.backgroundImage !== '';
      console.log('🔍 イラスト要素:', img.id || img.className, 'backgroundImage:', img.style.backgroundImage, 'hasImage:', hasImage);
      if (hasImage) {
        img.classList.add('slot-image-highlight');
        highlightedImages.push(img);
      }
    });
    
    console.log(`✅ ${highlightedImages.length}個のイラストをハイライト`);
    
    if (highlightedImages.length === 0) {
      console.warn('⚠ ハイライトするイラストが見つかりません');
      return;
    }
    
    // 吹き出しの位置を計算（最初のハイライトされたイラストを基準）
    const firstImage = highlightedImages[0];
    const imageRect = firstImage.getBoundingClientRect();
    
    // 吹き出しトースト（イラストの右側に配置）
    const toast = document.createElement('div');
    toast.id = 'illustration-hint-toast';
    
    // イラストの右側に配置（画面外に出る場合は左側）
    const toastWidth = 280;
    const spaceOnRight = window.innerWidth - imageRect.right;
    const positionOnRight = spaceOnRight > toastWidth + 40;
    
    let toastLeft, arrowPosition;
    if (positionOnRight) {
      toastLeft = imageRect.right + 20;
      arrowPosition = 'left'; // 矢印は左側
    } else {
      toastLeft = imageRect.left - toastWidth - 20;
      arrowPosition = 'right'; // 矢印は右側
    }
    
    const toastTop = imageRect.top + (imageRect.height / 2);
    
    toast.style.cssText = `
      position: fixed;
      left: ${toastLeft}px;
      top: ${toastTop}px;
      transform: translateY(-50%);
      background: white;
      border: 2px solid #333;
      border-radius: 12px;
      padding: 16px 20px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
      z-index: 10001;
      text-align: center;
      animation: fadeIn 0.3s ease-out;
      pointer-events: auto;
      width: ${toastWidth}px;
    `;
    
    // 矢印（CSS triangle）
    const arrow = document.createElement('div');
    arrow.className = 'toast-arrow';
    if (arrowPosition === 'left') {
      arrow.style.cssText = `
        position: absolute;
        left: -12px;
        top: 50%;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
        border-right: 12px solid #333;
      `;
    } else {
      arrow.style.cssText = `
        position: absolute;
        right: -12px;
        top: 50%;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
        border-left: 12px solid #333;
      `;
    }
    
    toast.innerHTML = `
      <div style="font-size: 16px; font-weight: bold; color: #333; margin-bottom: 10px; line-height: 1.4;">
        イラストをヒントに<br>英語を考えましょう
      </div>
      <label style="display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 10px; cursor: pointer;">
        <input type="checkbox" id="dismiss-illustration-hint" style="width: 16px; height: 16px; cursor: pointer;">
        <span style="font-size: 12px; color: #555;">今後表示しない</span>
      </label>
      <button id="close-illustration-hint" style="
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-size: 13px;
        cursor: pointer;
        font-weight: bold;
      ">OK</button>
    `;
    
    toast.appendChild(arrow);
    
    // アニメーションCSS
    const style = document.createElement('style');
    style.id = 'illustration-hint-style';
    style.textContent = `
      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(-50%) scale(0.9);
        }
        to {
          opacity: 1;
          transform: translateY(-50%) scale(1);
        }
      }
      
      .slot-image-highlight {
        position: relative;
        z-index: 10000 !important;
        animation: imageGlow 1s infinite alternate !important;
        border-radius: 8px !important;
      }
      
      @keyframes imageGlow {
        0% {
          box-shadow: 0 0 10px 4px rgba(255, 193, 7, 0.8), 
                      0 0 20px 8px rgba(255, 193, 7, 0.4) !important;
          border: 3px solid rgba(255, 193, 7, 0.9) !important;
        }
        100% {
          box-shadow: 0 0 20px 8px rgba(255, 193, 7, 1), 
                      0 0 40px 12px rgba(255, 193, 7, 0.6) !important;
          border: 3px solid rgba(255, 193, 7, 1) !important;
        }
      }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(toast);
    
    // OKボタンクリック
    const closeBtn = document.getElementById('close-illustration-hint');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        console.log('💡 OKボタンクリック');
        
        const checkbox = document.getElementById('dismiss-illustration-hint');
        if (checkbox && checkbox.checked) {
          localStorage.setItem('illustration_hint_dismissed', 'true');
          console.log('💡 イラストヒント: 今後表示しない設定を保存');
        }
        
        // トーストを削除
        if (toast.parentNode) {
          toast.remove();
        }
        if (style.parentNode) {
          style.remove();
        }
        
        // ハイライトを解除
        highlightedImages.forEach(img => img.classList.remove('slot-image-highlight'));
        
        console.log('💡 イラストヒントトーストを閉じました');
      });
    } else {
      console.error('❌ OKボタンが見つかりません');
    }
  }
  
  /**
   * 「今後表示しない」設定をリセット（デバッグ用）
   */
  function resetIllustrationHint() {
    localStorage.removeItem('illustration_hint_dismissed');
    console.log('💡 イラストヒント設定をリセットしました');
  }
  
  // グローバルにエクスポート
  window.showIllustrationHintToast = showIllustrationHintToast;
  window.resetIllustrationHint = resetIllustrationHint;
  
  console.log('✅ illustration-hint-toast.js が読み込まれました');
})();
