// 🎭 サブスロット用オーバーレイ表示制御システム
// シンプルなオーバーレイ方式で要素の表示・非表示を制御

// 🎯 サブスロットの表示・非表示制御に使用するスロット一覧
const SUBSLOT_PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
const SUB_ELEMENT_TYPES = ['image', 'auxtext', 'text'];

// 🏗️ サブスロット用コントロールパネルを生成
function createSubslotControlPanel(parentSlot) {
  console.log(`🏗️ ${parentSlot}サブスロット用オーバーレイコントロールパネル生成開始`);
  
  // パネル全体のコンテナ
  const panelContainer = document.createElement('div');
  panelContainer.id = `subslot-overlay-panel-${parentSlot}`;
  panelContainer.className = 'subslot-overlay-panel';
  
  // 制御パネルの表示状態を確認
  let isControlPanelsVisible = false;
  
  if (window.getControlPanelsVisibility) {
    isControlPanelsVisible = window.getControlPanelsVisibility();
  }
  
  const toggleBtn = document.getElementById('toggle-control-panels');
  if (toggleBtn) {
    const btnTextVisible = toggleBtn.textContent.includes('表示中');
    isControlPanelsVisible = isControlPanelsVisible || btnTextVisible;
  }
  
  const upperPanel = document.getElementById('visibility-control-panel-inline');
  if (upperPanel) {
    const upperVisible = upperPanel.style.display !== 'none';
    isControlPanelsVisible = isControlPanelsVisible || upperVisible;
  }
  
  panelContainer.style.cssText = `
    display: ${isControlPanelsVisible ? 'block' : 'none'};
    background: rgba(255, 255, 255, 0.95);
    padding: 8px;
    margin-top: 15px;
    border-radius: 5px;
    border: 1px solid #ddd;
  `;
  
  // パネルタイトル
  const panelTitle = document.createElement('div');
  panelTitle.style.cssText = `
    font-weight: bold;
    font-size: 12px;
    margin-bottom: 8px;
    color: #444;
    text-align: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
  `;
  panelTitle.textContent = `${parentSlot.toUpperCase()} サブスロット表示制御`;
  panelContainer.appendChild(panelTitle);
  
  // サブスロット要素を検索
  const subslotElements = document.querySelectorAll(`[id^="slot-${parentSlot}-sub-"]`);
  
  if (subslotElements.length === 0) {
    const noSubslotsMsg = document.createElement('div');
    noSubslotsMsg.style.cssText = `
      text-align: center;
      color: #666;
      font-style: italic;
      font-size: 12px;
    `;
    noSubslotsMsg.textContent = 'サブスロットがありません';
    panelContainer.appendChild(noSubslotsMsg);
    return panelContainer;
  }
  
  // サブスロットコントロールのコンテナ
  const controlsContainer = document.createElement('div');
  controlsContainer.style.cssText = `
    display: flex;
    gap: 8px;
    align-items: center;
    font-size: 12px;
    flex-wrap: wrap;
  `;
  
  // 各サブスロット用のコントロールを生成
  const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
  
  desiredOrder.forEach(subslotType => {
    const subslotElement = document.getElementById(`slot-${parentSlot}-sub-${subslotType}`);
    if (subslotElement) {
      const subslotId = subslotElement.id;
      const controlGroup = createSubslotControlGroup(parentSlot, subslotType, subslotId);
      controlsContainer.appendChild(controlGroup);
    }
  });
  
  panelContainer.appendChild(controlsContainer);
  
  // 全表示ボタン（全オーバーレイ削除）
  const resetButton = document.createElement('button');
  resetButton.style.cssText = `
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 6px 10px;
    font-size: 11px;
    cursor: pointer;
    border-radius: 3px;
    margin-left: 8px;
  `;
  resetButton.textContent = '全表示';
  resetButton.addEventListener('click', () => {
    resetSubslotVisibility(parentSlot);
  });
  controlsContainer.appendChild(resetButton);
  
  console.log(`✅ ${parentSlot}サブスロット用オーバーレイコントロールパネル生成完了`);
  return panelContainer;
}

// 🎛️ 個別サブスロット用コントロールグループを生成
function createSubslotControlGroup(parentSlot, subslotType, subslotId) {
  const controlGroup = document.createElement('div');
  controlGroup.className = 'subslot-control-group';
  controlGroup.style.cssText = `
    padding: 4px;
    border: 1px solid #f0f0f0;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.7);
  `;
  
  // スロット名表示
  const slotLabel = document.createElement('div');
  slotLabel.style.cssText = `
    font-weight: bold;
    font-size: 11px;
    margin-bottom: 2px;
    color: #444;
    text-align: center;
  `;
  slotLabel.textContent = subslotType.toUpperCase();
  controlGroup.appendChild(slotLabel);
  
  // 各要素タイプのボタンコンテナ
  const buttonContainer = document.createElement('div');
  buttonContainer.style.cssText = `
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: 10px;
  `;
  
  SUB_ELEMENT_TYPES.forEach(elementType => {
    const controlButton = document.createElement('button');
    controlButton.className = 'subslot-overlay-button';
    controlButton.dataset.parentSlot = parentSlot;
    controlButton.dataset.subslotId = subslotId;
    controlButton.dataset.subslotType = subslotType;
    controlButton.dataset.elementType = elementType;
    
    // LocalStorageからオーバーレイ状態を読み込み
    let hasOverlay = false;
    try {
      const saved = localStorage.getItem('rephrase_subslot_overlay_state');
      if (saved) {
        const overlayState = JSON.parse(saved);
        if (overlayState[subslotId] && overlayState[subslotId][elementType] !== undefined) {
          hasOverlay = overlayState[subslotId][elementType];
        }
      }
    } catch (error) {
      console.error("❌ オーバーレイ状態の読み込みに失敗:", error);
    }
    
    // ボタンの見た目を更新する関数
    function updateButtonAppearance() {
      const isVisible = !hasOverlay;
      controlButton.style.cssText = `
        padding: 3px 6px;
        border: 1px solid ${isVisible ? '#4CAF50' : '#f44336'};
        background-color: ${isVisible ? '#e8f5e8' : '#fde8e8'};
        color: ${isVisible ? '#2e7d32' : '#c62828'};
        border-radius: 3px;
        cursor: pointer;
        font-size: 10px;
        margin: 1px;
        transition: all 0.2s ease;
        min-width: 45px;
      `;
      
      const icon = {
        'image': '🖼️',
        'text': '📄',
        'auxtext': '📝'
      };
      
      controlButton.textContent = `${icon[elementType]}${isVisible ? '' : '❌'}`;
      controlButton.title = `${elementType}: ${isVisible ? '表示中（クリックで非表示）' : '非表示中（クリックで表示）'}`;
    }
    
    updateButtonAppearance();
    
    // ボタンクリック時のイベント
    controlButton.addEventListener('click', function() {
      hasOverlay = !hasOverlay; // 状態を反転
      updateButtonAppearance();
      
      toggleSubslotElementOverlay(
        this.dataset.subslotId,
        this.dataset.elementType,
        hasOverlay
      );
    });
    
    buttonContainer.appendChild(controlButton);
  });
  
  controlGroup.appendChild(buttonContainer);
  return controlGroup;
}

// 🎭 オーバーレイによるサブスロット要素の表示・非表示制御
function toggleSubslotElementOverlay(subslotId, elementType, showOverlay) {
  console.log(`🎭 オーバーレイ制御: ${subslotId} - ${elementType} = ${showOverlay ? 'オーバーレイ表示' : 'オーバーレイ削除'}`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) {
    console.warn(`⚠ サブスロット要素が見つかりません: ${subslotId}`);
    return;
  }
  
  // 対象要素を特定
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image, .multi-image-container'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (!elements || elements.length === 0) {
    console.warn(`⚠ ${elementType}要素が見つかりません in ${subslotId}`);
    return;
  }
  
  elements.forEach((element, index) => {
    const overlayId = `overlay-${subslotId}-${elementType}-${index}`;
    let overlay = document.getElementById(overlayId);
    
    if (!showOverlay) {
      // オーバーレイを削除（表示状態）
      if (overlay) {
        overlay.remove();
        console.log(`✅ ${element.className || element.tagName}のオーバーレイを削除しました`);
      }
    } else {
      // オーバーレイを作成・配置（非表示状態）
      if (!overlay) {
        // 親要素をrelativeに設定
        const parent = element.parentElement;
        if (getComputedStyle(parent).position === 'static') {
          parent.style.position = 'relative';
        }
        
        // オーバーレイ要素を作成
        overlay = document.createElement('div');
        overlay.id = overlayId;
        overlay.className = 'subslot-element-overlay';
        overlay.style.cssText = `
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(128, 128, 128, 0.8);
          backdrop-filter: blur(3px);
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 12px;
          font-weight: bold;
          text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
          border-radius: 4px;
          cursor: pointer;
          user-select: none;
          pointer-events: auto;
        `;
        
        // オーバーレイテキスト
        const overlayText = {
          'image': '🖼️ 画像を非表示',
          'text': '📄 テキストを非表示', 
          'auxtext': '📝 補助テキストを非表示'
        };
        overlay.textContent = overlayText[elementType] || '非表示';
        
        // オーバーレイクリックで表示に戻す機能
        overlay.addEventListener('click', (e) => {
          e.stopPropagation();
          console.log(`🖱️ オーバーレイクリック: ${overlayId} を削除して表示に戻します`);
          
          // オーバーレイを削除
          toggleSubslotElementOverlay(subslotId, elementType, false);
          
          // 制御パネルのボタンも更新
          const button = document.querySelector(`[data-subslot-id="${subslotId}"][data-element-type="${elementType}"]`);
          if (button) {
            button.click(); // これによりボタンの見た目も更新される
          }
        });
        
        // 要素の直前に挿入（相対位置を保つため）
        element.parentNode.insertBefore(overlay, element);
        console.log(`🎭 ${element.className || element.tagName}にオーバーレイを配置しました: ${overlayId}`);
      }
    }
  });
  
  // オーバーレイ状態をlocalStorageに保存
  try {
    let overlayState = {};
    const saved = localStorage.getItem('rephrase_subslot_overlay_state');
    if (saved) {
      overlayState = JSON.parse(saved);
    }
    
    if (!overlayState[subslotId]) {
      overlayState[subslotId] = {};
    }
    overlayState[subslotId][elementType] = showOverlay;
    
    localStorage.setItem('rephrase_subslot_overlay_state', JSON.stringify(overlayState));
    console.log(`💾 ${subslotId}の${elementType}オーバーレイ状態を保存: ${showOverlay}`);
  } catch (error) {
    console.error("❌ オーバーレイ状態の保存に失敗:", error);
  }
}

// 🔄 サブスロットの全オーバーレイ削除（全表示）
function resetSubslotVisibility(parentSlot) {
  console.log(`🔄 ${parentSlot}サブスロットの全オーバーレイを削除して全表示にリセット`);
  
  // 該当するボタンを全て表示状態に
  const buttons = document.querySelectorAll(`[data-parent-slot="${parentSlot}"].subslot-overlay-button`);
  buttons.forEach(button => {
    // オーバーレイを削除（表示状態にする）
    toggleSubslotElementOverlay(
      button.dataset.subslotId,
      button.dataset.elementType,
      false // オーバーレイを削除
    );
    
    // ボタンの見た目も更新（クリックで状態を同期）
    setTimeout(() => {
      const currentOverlay = button.textContent.includes('❌');
      if (currentOverlay) {
        button.click();
      }
    }, 10);
  });
  
  console.log(`✅ ${parentSlot}サブスロットの全表示リセット完了`);
}

// 📋 サブスロット展開時にコントロールパネルを追加
function addSubslotControlPanel(parentSlot) {
  console.log(`📋 ${parentSlot}サブスロット用オーバーレイコントロールパネル追加開始`);
  
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  if (!subslotContainer) {
    console.warn(`⚠ サブスロットコンテナが見つかりません: slot-${parentSlot}-sub`);
    return;
  }
  
  // 既存のパネルがあれば削除
  const existingPanel = document.getElementById(`subslot-overlay-panel-${parentSlot}`);
  if (existingPanel) {
    existingPanel.remove();
  }
  
  // 新しいパネルを生成・追加
  setTimeout(() => {
    const panel = createSubslotControlPanel(parentSlot);
    if (panel) {
      subslotContainer.parentNode.insertBefore(panel, subslotContainer.nextSibling);
      console.log(`✅ ${parentSlot}サブスロット用オーバーレイコントロールパネル追加完了`);
      
      // 保存されたオーバーレイ状態を復元
      applySubslotOverlayState();
    }
  }, 200);
}

// 🗑️ サブスロット折りたたみ時にコントロールパネルを削除
function removeSubslotControlPanel(parentSlot) {
  console.log(`🗑️ ${parentSlot}サブスロット用オーバーレイコントロールパネル削除開始`);
  
  const panel = document.getElementById(`subslot-overlay-panel-${parentSlot}`);
  if (panel) {
    panel.remove();
    console.log(`✅ ${parentSlot}サブスロット用オーバーレイコントロールパネル削除完了`);
  }
}

// 🆕 オーバーレイ状態の復元機能
function applySubslotOverlayState() {
  console.log("🎭 サブスロットオーバーレイ状態をDOMに適用中...");
  
  try {
    const saved = localStorage.getItem('rephrase_subslot_overlay_state');
    if (!saved) {
      console.log("📝 保存されたオーバーレイ状態がありません");
      return;
    }
    
    const overlayState = JSON.parse(saved);
    console.log("📂 復元するオーバーレイ状態:", overlayState);
    
    Object.keys(overlayState).forEach(subslotId => {
      const elementStates = overlayState[subslotId];
      
      ['image', 'auxtext', 'text'].forEach(elementType => {
        const hasOverlay = elementStates[elementType];
        if (hasOverlay !== undefined && hasOverlay) {
          // オーバーレイがある場合は非表示にする
          toggleSubslotElementOverlay(subslotId, elementType, true);
          console.log(`🎭 ${subslotId}の${elementType}にオーバーレイを復元`);
        }
      });
    });
    
    console.log("✅ オーバーレイ状態の復元完了");
  } catch (error) {
    console.error("❌ オーバーレイ状態の復元に失敗:", error);
  }
}

// 🔹 グローバル関数としてエクスポート
window.createSubslotControlPanel = createSubslotControlPanel;
window.addSubslotControlPanel = addSubslotControlPanel;
window.removeSubslotControlPanel = removeSubslotControlPanel;
window.toggleSubslotElementOverlay = toggleSubslotElementOverlay;
window.resetSubslotVisibility = resetSubslotVisibility;
window.applySubslotOverlayState = applySubslotOverlayState;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロットオーバーレイ制御システムを初期化中...");
  
  // オーバーレイ状態の初期復元
  setTimeout(() => {
    applySubslotOverlayState();
  }, 1000);
  
  console.log("✅ サブスロットオーバーレイ制御システム初期化完了");
});

console.log("✅ subslot_visibility_control_overlay.js が読み込まれました");
