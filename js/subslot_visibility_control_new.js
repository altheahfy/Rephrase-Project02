// サブスロット表示制御システム
// 上位スロット制御パネルと完全に同じ実装方式を採用

// 🎯 サブスロット定義（上位パネルと同じ形式）
const SUB_ELEMENT_TYPES = ['image', 'auxtext', 'text'];
const SUB_ELEMENT_ICONS = {
  image: '🖼️',
  auxtext: '📝',
  text: '📄'
};

// 🎛️ サブスロット制御パネルの生成（上位パネルと完全同等）
function generateSubslotControlPanel(parentSlot) {
  console.log(`🎛️ ${parentSlot}サブスロット制御パネル生成開始`);
  
  // サブスロット要素を検索
  const subslotElements = document.querySelectorAll(`[id^="slot-${parentSlot}-sub-"]`);
  console.log(`🔍 ${parentSlot}のサブスロット要素: ${subslotElements.length}個`);
  
  if (subslotElements.length === 0) {
    console.warn(`⚠ ${parentSlot}: サブスロット要素が見つかりません`);
    return null;
  }
  
  // パネルコンテナ
  const panelContainer = document.createElement('div');
  panelContainer.id = `subslot-visibility-panel-${parentSlot}`;
  panelContainer.className = 'subslot-visibility-panel';
  
  // 上位パネルの表示状態に合わせて初期表示を設定
  const isVisible = window.controlPanelsVisible || false;
  panelContainer.style.display = isVisible ? 'block' : 'none';
  
  // 上位パネルと全く同じCSS
  panelContainer.style.cssText = `
    display: ${isVisible ? 'block' : 'none'};
    background: rgba(255, 255, 255, 0.95);
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
  `;
  
  // フレックスコンテナ（上位パネルと全く同じ）
  const flexContainer = document.createElement('div');
  flexContainer.style.cssText = 'display: flex; gap: 8px; align-items: center; font-size: 12px;';
  
  // サブスロット要素からSlot IDを抽出
  const subslotIds = [];
  subslotElements.forEach(subslot => {
    const match = subslot.id.match(/slot-(\w+)-sub-(\w+)/);
    if (match) {
      const subslotId = match[2]; // 例: slot-m1-sub-s → "s"
      if (!subslotIds.includes(subslotId)) {
        subslotIds.push(subslotId);
      }
    }
  });
  
  console.log(`🔄 ${parentSlot}のサブスロットID: ${subslotIds.join(', ')}`);
  
  // 各サブスロット用のコントロールグループを生成
  subslotIds.forEach(subslotId => {
    const controlGroup = document.createElement('div');
    controlGroup.className = 'slot-control-group';  // ★★★ 上位パネルと同じクラス名 ★★★
    controlGroup.dataset.slot = `${parentSlot}-sub-${subslotId}`;  // ★★★ data-slot設定 ★★★
    controlGroup.style.cssText = `
      padding: 4px;
      border: 1px solid #f0f0f0;
      border-radius: 3px;
    `;
    
    // スロット名（上位パネルと全く同じ）
    const slotLabel = document.createElement('div');
    slotLabel.textContent = subslotId.toUpperCase();
    slotLabel.style.cssText = `
      font-weight: bold;
      font-size: 11px;
      margin-bottom: 2px;
      color: #444;
      text-align: center;
    `;
    controlGroup.appendChild(slotLabel);
    
    // 各要素タイプのチェックボックス
    const elementsContainer = document.createElement('div');
    elementsContainer.style.cssText = 'display: flex; flex-direction: column; gap: 2px; font-size: 10px;';
    
    SUB_ELEMENT_TYPES.forEach(elementType => {
      const label = document.createElement('label');
      label.style.cssText = 'display: flex; align-items: center; gap: 2px;';
      
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'visibility-checkbox';  // ★★★ 上位パネルと同じクラス名 ★★★
      checkbox.checked = true; // 初期状態は表示
      checkbox.dataset.slot = `${parentSlot}-sub-${subslotId}`;  // ★★★ data-slot設定 ★★★
      checkbox.dataset.type = elementType;  // ★★★ data-type設定 ★★★
      
      // ★★★ イベントリスナーは削除 - visibility_control.js が自動的に処理 ★★★
      
      // アイコン
      const icon = document.createElement('span');
      icon.textContent = SUB_ELEMENT_ICONS[elementType];
      
      label.appendChild(checkbox);
      label.appendChild(icon);
      elementsContainer.appendChild(label);
    });
    
    controlGroup.appendChild(elementsContainer);
    flexContainer.appendChild(controlGroup);
  });
  
  // 全表示ボタン（上位パネルと全く同じ）
  const resetButton = document.createElement('button');
  resetButton.id = `reset-subslot-visibility-${parentSlot}`;
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
  resetButton.addEventListener('click', function() {
    console.log(`🔄 ${parentSlot}サブスロット全表示ボタンクリック`);
    resetSubslotVisibility(parentSlot);
  });
  flexContainer.appendChild(resetButton);
  
  panelContainer.appendChild(flexContainer);
  
  console.log(`✅ ${parentSlot}サブスロット制御パネル生成完了`);
  return panelContainer;
}

// 🔄 サブスロット表示リセット機能
function resetSubslotVisibility(parentSlot) {
  console.log(`🔄 ${parentSlot}サブスロット表示リセット開始`);
  
  // サブスロット制御パネルの全チェックボックスをチェック状態に戻す
  const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (panel) {
    const checkboxes = panel.querySelectorAll('.visibility-checkbox');
    checkboxes.forEach(checkbox => {
      checkbox.checked = true;
      // イベントを手動で発火させて実際の表示も更新
      checkbox.dispatchEvent(new Event('change'));
    });
    console.log(`✅ ${parentSlot}サブスロット制御パネルの${checkboxes.length}個のチェックボックスをリセット`);
  }
}

// 🎯 サブスロット制御パネルの表示同期
function syncSubslotControlPanelVisibility(parentSlot) {
  const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (panel) {
    const isVisible = window.controlPanelsVisible || false;
    panel.style.display = isVisible ? 'block' : 'none';
    console.log(`🔄 ${parentSlot}サブスロット制御パネルの表示同期: ${isVisible ? '表示' : '非表示'}`);
  }
}

// 🎯 全サブスロット制御パネルの表示同期
function syncAllSubslotControlPanels() {
  console.log("🔄 全サブスロット制御パネルの表示同期開始");
  
  const panels = document.querySelectorAll('.subslot-visibility-panel');
  const isVisible = window.controlPanelsVisible || false;
  
  panels.forEach(panel => {
    panel.style.display = isVisible ? 'block' : 'none';
  });
  
  console.log(`✅ ${panels.length}個のサブスロット制御パネルの表示同期完了: ${isVisible ? '表示' : '非表示'}`);
}

// 🎯 サブスロット制御パネルの挿入
function insertSubslotControlPanel(parentSlot) {
  console.log(`🎛️ ${parentSlot}サブスロット制御パネル挿入開始`);
  
  // 既存のパネルを削除
  const existingPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (existingPanel) {
    existingPanel.remove();
    console.log(`🗑️ ${parentSlot}の既存サブスロット制御パネルを削除`);
  }
  
  // 新しいパネルを生成
  const newPanel = generateSubslotControlPanel(parentSlot);
  if (!newPanel) {
    console.warn(`⚠ ${parentSlot}のサブスロット制御パネル生成に失敗`);
    return;
  }
  
  // 挿入位置を決定（親スロットの直後）
  const parentSlotElement = document.getElementById(`slot-${parentSlot}`);
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  
  if (parentSlotElement && subslotContainer) {
    // サブスロットコンテナの直前に挿入
    subslotContainer.parentNode.insertBefore(newPanel, subslotContainer);
    console.log(`✅ ${parentSlot}サブスロット制御パネルを挿入`);
  } else {
    console.warn(`⚠ ${parentSlot}の親スロットまたはサブスロットコンテナが見つかりません`);
  }
}

// 🎯 全サブスロット制御パネルの生成・挿入
function generateAllSubslotControlPanels() {
  console.log("🎛️ 全サブスロット制御パネル生成開始");
  
  // 全てのサブスロットコンテナを検索
  const subslotContainers = document.querySelectorAll('[id$="-sub"]');
  console.log(`🔍 サブスロットコンテナ: ${subslotContainers.length}個`);
  
  subslotContainers.forEach(container => {
    const match = container.id.match(/slot-(\w+)-sub$/);
    if (match) {
      const parentSlot = match[1];
      insertSubslotControlPanel(parentSlot);
    }
  });
  
  console.log("✅ 全サブスロット制御パネル生成完了");
}

// 🎯 サブスロット制御パネルの削除
function removeSubslotControlPanel(parentSlot) {
  console.log(`�️ ${parentSlot}サブスロット制御パネル削除開始`);
  
  const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (panel) {
    panel.remove();
    console.log(`✅ ${parentSlot}サブスロット制御パネル削除完了`);
  } else {
    console.warn(`⚠ ${parentSlot}サブスロット制御パネルが見つかりません`);
  }
}

// �🔹 グローバル関数としてエクスポート
window.generateSubslotControlPanel = generateSubslotControlPanel;
window.resetSubslotVisibility = resetSubslotVisibility;
window.syncSubslotControlPanelVisibility = syncSubslotControlPanelVisibility;
window.syncAllSubslotControlPanels = syncAllSubslotControlPanels;
window.insertSubslotControlPanel = insertSubslotControlPanel;
window.removeSubslotControlPanel = removeSubslotControlPanel;
window.generateAllSubslotControlPanels = generateAllSubslotControlPanels;

// 🔄 DOM読み込み後の初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット制御パネルシステム初期化中...");
  
  // 少し遅らせてパネルを生成（DOM構築完了を確実にするため）
  setTimeout(() => {
    generateAllSubslotControlPanels();
  }, 500);
});

// 🔍 デバッグ用：手動でテストできる関数
window.testSubslotControlPanel = function(parentSlot) {
  console.log(`🧪 ${parentSlot}サブスロット制御パネルテスト開始`);
  insertSubslotControlPanel(parentSlot);
  
  // パネルの内容を確認
  const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (panel) {
    const checkboxes = panel.querySelectorAll('.visibility-checkbox');
    console.log(`📋 生成されたチェックボックス: ${checkboxes.length}個`);
    
    checkboxes.forEach((checkbox, index) => {
      console.log(`  ${index + 1}. slot="${checkbox.dataset.slot}" type="${checkbox.dataset.type}"`);
    });
  }
};

console.log("✅ subslot_visibility_control.js が読み込まれました");
