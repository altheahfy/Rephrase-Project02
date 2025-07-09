// 制御パネル表示管理システム
// 上位スロットおよびサブスロット表示制御パネルの表示/非表示を一元管理

// 🎛️ 制御パネル表示状態を管理するグローバル変数
window.controlPanelsVisible = false;

// 🔄 制御パネルの表示状態を取得
function getControlPanelsVisibility() {
  // ボタンのテキストからも状態を確認
  const toggleBtn = document.getElementById('toggle-control-panels');
  if (toggleBtn && toggleBtn.textContent.includes('表示中')) {
    window.controlPanelsVisible = true;
  }
  
  console.log(`🔍 制御パネル表示状態取得: ${window.controlPanelsVisible}`);
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
  
  console.log(`🎛️ 制御パネル切り替え開始: ${newState ? '表示' : '非表示'}`);
  
  // 上位スロット制御パネルの表示/非表示
  const upperControlPanel = document.getElementById('visibility-control-panel-inline');
  if (upperControlPanel) {
    upperControlPanel.style.display = newState ? 'block' : 'none';
    console.log(`✅ 上位スロット制御パネル: ${newState ? '表示' : '非表示'}`);
  } else {
    console.warn("⚠ 上位スロット制御パネルが見つかりません");
  }
  
  // サブスロット制御パネルの表示/非表示（旧方式 + 新方式）
  const subslotPanels = document.querySelectorAll('.subslot-visibility-panel');
  const overlayPanels = document.querySelectorAll('.subslot-overlay-panel');
  const allSubslotPanels = [...subslotPanels, ...overlayPanels];
  
  console.log(`🔍 見つかったサブスロット制御パネル: ${subslotPanels.length}個（旧方式）`);
  console.log(`🔍 見つかったオーバーレイ制御パネル: ${overlayPanels.length}個（新方式）`);
  console.log(`🔍 合計制御パネル数: ${allSubslotPanels.length}個`);
  
  allSubslotPanels.forEach((panel, index) => {
    panel.style.display = newState ? 'block' : 'none';
    console.log(`  - パネル${index + 1} (${panel.id}): ${newState ? '表示' : '非表示'}`);
  });
  
  // ボタンテキストの更新
  const toggleBtn = document.getElementById('toggle-control-panels');
  if (toggleBtn) {
    toggleBtn.textContent = newState ? '制御パネル (表示中)' : '制御パネル';
    console.log(`✅ ボタンテキスト更新: "${toggleBtn.textContent}"`);
  } else {
    console.warn("⚠ 制御パネルボタンが見つかりません");
  }
  
  console.log(`🎛️ 全制御パネル表示状態変更完了: ${newState ? '表示' : '非表示'}`);
  return newState;
}

// 🎛️ サブスロット制御パネルの表示を現在の状態に合わせる
function syncSubslotControlPanelVisibility(panelElement) {
  if (panelElement && (panelElement.classList.contains('subslot-visibility-panel') || panelElement.classList.contains('subslot-overlay-panel'))) {
    panelElement.style.display = window.controlPanelsVisible ? 'block' : 'none';
    console.log(`🔄 サブスロット制御パネルの表示を同期: ${window.controlPanelsVisible ? '表示' : '非表示'}`);
  }
}

// 🔹 グローバル関数としてエクスポート
window.getControlPanelsVisibility = getControlPanelsVisibility;
window.setControlPanelsVisibility = setControlPanelsVisibility;
window.toggleAllControlPanels = toggleAllControlPanels;
window.syncSubslotControlPanelVisibility = syncSubslotControlPanelVisibility;

// 🔍 デバッグ用：現在の制御パネル状態を詳細表示
window.debugControlPanelStatus = function() {
  console.log("🔍 === 制御パネル状態デバッグ ===");
  console.log(`グローバル変数: ${window.controlPanelsVisible}`);
  
  const toggleBtn = document.getElementById('toggle-control-panels');
  console.log(`ボタンテキスト: "${toggleBtn ? toggleBtn.textContent : 'ボタンなし'}"`);
  
  const upperPanel = document.getElementById('visibility-control-panel-inline');
  console.log(`上位パネル表示: ${upperPanel ? upperPanel.style.display : 'パネルなし'}`);
  
  const subslotPanels = document.querySelectorAll('.subslot-visibility-panel');
  const overlayPanels = document.querySelectorAll('.subslot-overlay-panel');
  
  console.log(`サブスロットパネル数（旧方式）: ${subslotPanels.length}`);
  subslotPanels.forEach((panel, index) => {
    console.log(`  - 旧パネル${index + 1} (${panel.id}): ${panel.style.display}`);
  });
  
  console.log(`オーバーレイパネル数（新方式）: ${overlayPanels.length}`);
  overlayPanels.forEach((panel, index) => {
    console.log(`  - 新パネル${index + 1} (${panel.id}): ${panel.style.display}`);
  });
  
  console.log("🔍 ========================");
};

console.log("✅ control_panel_manager.js が読み込まれました");
