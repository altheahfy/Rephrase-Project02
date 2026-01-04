// ====================================
// 🎯 初回ガイド用ツールチップシステム
// ====================================
// 目的: ①②③④の説明テキストにホバーで詳細説明を表示

(function() {
  'use strict';

  console.log('🎯 初回ガイドツールチップシステム初期化開始');

  // ツールチップ設定
  const tooltipConfig = {
    'guide-step-1': {
      content: '全シャッフル（<span style="display: inline-flex; align-items: center; justify-content: center; background: #ff9800; color: white; border: none; padding: 3px 6px; border-radius: 3px; font-size: 10px; font-weight: bold;">🎲 全シャッフル</span>）を押すと、様々な例文が表示されます。<br><br>そこに表示される「英語とイラストのセット」を見て、イラストだけを見て英語が思い出せるようにしましょう'
    },
    'guide-step-2': {
      content: '「<span style="display: inline-flex; align-items: center; justify-content: center; background: #4CAF50; color: white; border: none; padding: 2px 4px; border-radius: 3px; font-size: 9px; font-weight: bold; line-height: 1.2;">英語<br>OFF</span>」を押すと、そこの英語が消えます。<br><br>これによって、自分が練習したい箇所をテストできるようになります。'
    },
    'guide-step-3': {
      content: '「<span style="display: inline-flex; align-items: center; justify-content: center; background: #ff9800; color: white; border: none; padding: 3px 6px; border-radius: 3px; font-size: 10px; font-weight: bold;">🎲 例文全シャッフル</span>」をクリックすると、例文全体が違うものに入れ替わります。<br><br>「<span style="display: inline-flex; align-items: center; justify-content: center; background: #ff9800; color: white; border: none; padding: 3px 6px; border-radius: 3px; font-size: 10px; font-weight: bold;">🎲</span>」をクリックすると、その部分だけが入れ替わります。<br><br>自由にシャッフルし、イラストをヒントに「英語を消した部分を含めた全文」を口に出して言ってください。<br><br>英語の「フォーム」が自然と身に付きます。'
    },
    'guide-step-4': {
      content: '主語の中にまた主語・動詞がある。<br>目的語の中にまた主語・動詞がある、など。<br><br>このような形にできるのが「言語」です。<br><br>例: I know <span style="background: #FFF59D; padding: 2px 4px; font-weight: bold;">that he loves me</span>.<br><br>こうした「中に入っている文」は、「<span style="display: inline-flex; align-items: center; justify-content: center; background: #2196f3; color: white; border: none; padding: 3px 6px; border-radius: 3px; font-size: 10px; font-weight: bold; margin: 0 4px;">▼ 詳細</span>」で取り出すことができます。<br><br><img src="images/guide/subslot-detail-example.png" style="width: 100%; max-width: 300px; margin-top: 10px; border: 2px solid #ddd; border-radius: 4px;">'
    }
  };

  // ツールチップ要素を生成
  function createTooltip() {
    const tooltip = document.createElement('div');
    tooltip.id = 'guide-tooltip';
    tooltip.className = 'guide-tooltip';
    tooltip.style.cssText = `
      position: fixed;
      display: none;
      background: rgba(255, 255, 255, 0.98);
      border: 2px solid #667eea;
      border-radius: 8px;
      padding: 12px 16px;
      max-width: 320px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      z-index: 10000;
      font-size: 13px;
      line-height: 1.6;
      color: #333;
    `;
    document.body.appendChild(tooltip);
    return tooltip;
  }

  // ツールチップを表示
  function showTooltip(element, config) {
    const tooltip = document.getElementById('guide-tooltip') || createTooltip();
    
    // ツールチップの内容を設定
    tooltip.innerHTML = `
      ${config.title ? `<div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #667eea;">${config.title}</div>` : ''}
      <div>
        ${config.content}
      </div>
    `;
    
    // ツールチップの位置を計算
    const rect = element.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    
    // 基本位置: 要素の下中央
    let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
    let top = rect.bottom + 8;
    
    // 画面外にはみ出る場合の調整
    if (left + tooltipRect.width > window.innerWidth - 20) {
      left = window.innerWidth - tooltipRect.width - 20;
    }
    if (left < 20) {
      left = 20;
    }
    
    // 下に表示スペースがない場合は上に表示
    if (top + tooltipRect.height > window.innerHeight - 20) {
      top = rect.top - tooltipRect.height - 8;
    }
    
    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
    tooltip.style.display = 'block';
  }

  // ツールチップを非表示
  function hideTooltip() {
    const tooltip = document.getElementById('guide-tooltip');
    if (tooltip) {
      tooltip.style.display = 'none';
    }
  }

  // イベントリスナーを設定
  function initTooltips() {
    Object.keys(tooltipConfig).forEach(id => {
      const element = document.getElementById(id);
      if (!element) {
        console.warn(`⚠️ ツールチップ対象要素が見つかりません: ${id}`);
        return;
      }

      // ホバー時に表示
      element.addEventListener('mouseenter', () => {
        showTooltip(element, tooltipConfig[id]);
      });

      // ホバー解除時に非表示
      element.addEventListener('mouseleave', () => {
        hideTooltip();
      });

      // クリック時も表示（スマホ対応）
      element.addEventListener('click', (e) => {
        const tooltip = document.getElementById('guide-tooltip');
        if (tooltip && tooltip.style.display === 'block') {
          hideTooltip();
        } else {
          showTooltip(element, tooltipConfig[id]);
        }
        e.stopPropagation();
      });

      console.log(`✅ ツールチップ設定完了: ${id}`);
    });

    // ツールチップ外をクリックしたら閉じる
    document.addEventListener('click', (e) => {
      const tooltip = document.getElementById('guide-tooltip');
      if (tooltip && !tooltip.contains(e.target)) {
        hideTooltip();
      }
    });
  }

  // DOMContentLoaded後に初期化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTooltips);
  } else {
    initTooltips();
  }

  console.log('✅ 初回ガイドツールチップシステム初期化完了');
})();
