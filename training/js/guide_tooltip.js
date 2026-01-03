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
      content: '例文全シャッフル（<span style="display: inline-flex; align-items: center; justify-content: center; background: #ff9800; color: white; border: none; padding: 3px 6px; border-radius: 3px; font-size: 10px; font-weight: bold;">🎲 例文全シャッフル</span>）を押すと、様々な例文が表示されます。<br><br>そこに表示される「英語とイラストのセット」を見て、イラストだけを見て英語が思い出せるようにしましょう'
    }
    // ②③④の設定は後で追加
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
