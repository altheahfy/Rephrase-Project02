// 制御パネル表示管理システム
// 上位スロットおよびサブスロット表示制御パネルの表示/非表示を一元管理

// 🎛️ 制御パネル表示状態を管理するグローバル変数
window.controlPanelsVisible = false;

// 🔄 制御パネルの表示状態を取得
function getControlPanelsVisibility() {
  return window.controlPanelsVisible;
}

// 🔄 制御パネルの表示状態を設定
function setControlPanelsVisibility(isVisible) {
  window.controlPanelsVisible = isVisible;
  console.log(`🎛️ 制御パネル表示状態を設定: ${isVisible ? '表示' : '非表示'}`);
}

// 🎛️ 全ての制御パネルの表示/非表示を切り替え
function toggleAllControlPanels() {
  const newState = !window.controlPanelsVisible;
  setControlPanelsVisibility(newState);
  
  // 上位スロット制御パネルの表示/非表示
  const upperControlPanel = document.getElementById('visibility-control-panel-inline');
  if (upperControlPanel) {
    upperControlPanel.style.display = newState ? 'block' : 'none';
  }
  
  // サブスロット制御パネルの表示/非表示
  const subslotPanels = document.querySelectorAll('.subslot-visibility-panel');
  subslotPanels.forEach(panel => {
    panel.style.display = newState ? 'block' : 'none';
  });
  
  // ボタンテキストの更新
  const toggleBtn = document.getElementById('toggle-control-panels');
  if (toggleBtn) {
    toggleBtn.textContent = newState ? '制御パネル (表示中)' : '制御パネル';
  }
  
  console.log(`🎛️ 全制御パネル表示状態変更: ${newState ? '表示' : '非表示'}`);
  return newState;
}

// 🎛️ サブスロット制御パネルの表示を現在の状態に合わせる
function syncSubslotControlPanelVisibility(panelElement) {
  if (panelElement && panelElement.classList.contains('subslot-visibility-panel')) {
    panelElement.style.display = window.controlPanelsVisible ? 'block' : 'none';
    console.log(`🔄 サブスロット制御パネルの表示を同期: ${window.controlPanelsVisible ? '表示' : '非表示'}`);
  }
}

// 🔹 グローバル関数としてエクスポート
window.getControlPanelsVisibility = getControlPanelsVisibility;
window.setControlPanelsVisibility = setControlPanelsVisibility;
window.toggleAllControlPanels = toggleAllControlPanels;
window.syncSubslotControlPanelVisibility = syncSubslotControlPanelVisibility;

console.log("✅ control_panel_manager.js が読み込まれました");
