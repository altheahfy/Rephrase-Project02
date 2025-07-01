// 制御パネル表示切り替え機能
// 上位スロットとサブスロットの全制御パネルを一括で表示/非表示

// 制御パネルの表示状態を管理
let controlPanelsVisible = false;

// 🎛️ 制御パネル表示切り替え関数
function toggleControlPanels() {
  console.log(`🎛️ 制御パネル表示切り替え: ${controlPanelsVisible ? '非表示' : '表示'}へ`);
  
  controlPanelsVisible = !controlPanelsVisible;
  
  // body要素にクラスを追加/削除してCSSでスタイル制御
  if (controlPanelsVisible) {
    document.body.classList.add('control-panels-visible');
    console.log('✅ 制御パネルを表示しました');
  } else {
    document.body.classList.remove('control-panels-visible');
    console.log('✅ 制御パネルを非表示にしました');
  }
  
  // ボタンのテキストを更新
  updateToggleButtonText();
}

// 🔄 ボタンのテキスト更新
function updateToggleButtonText() {
  const button = document.getElementById('toggle-control-panels');
  if (button) {
    button.textContent = controlPanelsVisible ? '🎛️ 制御パネル (表示中)' : '🎛️ 制御パネル';
    // ボタンの背景色も変更して状態を視覚的に表示
    button.style.backgroundColor = controlPanelsVisible ? '#4CAF50' : '#2196F3';
  }
}

// 🎯 ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log('🔄 制御パネル切り替え機能を初期化中...');
  
  // 制御パネル切り替えボタンのイベントリスナーを追加
  const toggleButton = document.getElementById('toggle-control-panels');
  if (toggleButton) {
    toggleButton.addEventListener('click', toggleControlPanels);
    console.log('✅ 制御パネル切り替えボタンのイベントリスナーを設定しました');
    
    // 初期状態のボタンテキストを設定
    updateToggleButtonText();
  } else {
    console.error('❌ 制御パネル切り替えボタンが見つかりません');
  }
});

// グローバル関数としてエクスポート
window.toggleControlPanels = toggleControlPanels;
window.updateToggleButtonText = updateToggleButtonText;

console.log("✅ control_panel_toggle.js が読み込まれました");
