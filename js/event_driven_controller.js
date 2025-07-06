// イベントドリブン処理制御システム
console.log("🎯 イベントドリブン処理制御システム読み込み");

// 必要な処理を実行する統合関数
function executeMaintenanceTasks() {
  console.log("🔄 必要な処理を実行中...");
  
  // ラベル復元
  if (window.triggerLabelRestore) {
    window.triggerLabelRestore();
  }
  
  // データ同期
  if (window.triggerDataSync) {
    window.triggerDataSync();
  }
  
  // 画像処理
  if (window.processAllImagesWithCoordination) {
    window.processAllImagesWithCoordination();
  }
  
  // メタタグ適用
  if (window.applyMetaTagImagesToAllSlots) {
    window.applyMetaTagImagesToAllSlots(true);
  }
  
  console.log("✅ 必要な処理が完了しました");
}

// デバウンス機能付きの実行関数
let maintenanceTimeout;
function executeMaintenanceTasksDebounced() {
  clearTimeout(maintenanceTimeout);
  maintenanceTimeout = setTimeout(() => {
    executeMaintenanceTasks();
  }, 300);
}

// 主要なイベントにリスナーを設定
function setupEventDrivenHandlers() {
  console.log("🎯 イベントドリブンハンドラーを設定中...");
  
  // ランダマイズボタンのクリック
  const randomizeButton = document.getElementById('randomize-button');
  if (randomizeButton) {
    randomizeButton.addEventListener('click', () => {
      console.log("🎲 ランダマイズボタンクリック検出");
      setTimeout(() => {
        executeMaintenanceTasksDebounced();
      }, 500); // ランダマイズ処理完了後
    });
  }
  
  // 詳細ボタンのクリック（動的に追加されるボタンも対象）
  document.addEventListener('click', (event) => {
    if (event.target.hasAttribute('data-subslot-toggle')) {
      console.log("🔍 詳細ボタンクリック検出");
      setTimeout(() => {
        executeMaintenanceTasksDebounced();
      }, 200);
    }
  });
  
  // 制御パネルのクリック
  const controlPanels = document.querySelectorAll('[id*="control-panel"], [class*="control-panel"]');
  controlPanels.forEach(panel => {
    panel.addEventListener('click', () => {
      console.log("⚙️ 制御パネルクリック検出");
      executeMaintenanceTasksDebounced();
    });
  });
  
  // 入力フィールドの変更（手動編集時）
  document.addEventListener('input', (event) => {
    if (event.target.closest('.slot-phrase') || event.target.classList.contains('slot-phrase')) {
      console.log("✏️ スロットテキスト入力検出");
      executeMaintenanceTasksDebounced();
    }
  });
  
  // フォーカスアウト時の処理
  document.addEventListener('blur', (event) => {
    if (event.target.closest('.slot-phrase') || event.target.classList.contains('slot-phrase')) {
      console.log("👁️ スロットテキストフォーカスアウト検出");
      executeMaintenanceTasksDebounced();
    }
  }, true);
  
  console.log("✅ イベントドリブンハンドラーの設定完了");
}

// 初期化時にも一度実行
function initialMaintenanceRun() {
  console.log("🚀 初期化時のメンテナンス実行");
  setTimeout(() => {
    executeMaintenanceTasks();
  }, 2000);
}

// DOM準備完了時にセットアップ
document.addEventListener('DOMContentLoaded', () => {
  console.log("📋 DOMContentLoaded - イベントドリブンシステム初期化");
  
  // 少し遅延してからセットアップ
  setTimeout(() => {
    setupEventDrivenHandlers();
    initialMaintenanceRun();
  }, 1000);
});

// グローバル関数として公開
window.executeMaintenanceTasks = executeMaintenanceTasks;
window.executeMaintenanceTasksDebounced = executeMaintenanceTasksDebounced;

console.log("✅ イベントドリブン処理制御システムが準備完了");
