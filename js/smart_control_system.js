// スマート処理制御システム
console.log("🎯 スマート処理制御システム読み込み");

// 制御状態
let isInitializationComplete = false;
let initializationTimer = null;
let periodicProcesses = [];

// 初期化完了判定
function checkInitializationComplete() {
  // 基本的な要素が揃っているかチェック
  const hasSlots = document.querySelectorAll('.slot-container').length > 0;
  const hasContent = document.querySelectorAll('.slot-phrase').length > 0;
  const hasDynamicArea = document.getElementById('dynamic-area') !== null;
  const hasJsonData = window.loadedJsonData !== null;
  
  if (hasSlots && hasContent && hasDynamicArea && hasJsonData) {
    console.log("✅ 初期化完了条件を満たしています");
    return true;
  }
  
  console.log("⏳ 初期化未完了:", { hasSlots, hasContent, hasDynamicArea, hasJsonData });
  return false;
}

// 定期処理を停止
function stopPeriodicProcesses() {
  console.log("🛑 定期処理を停止中...");
  
  // 既存の定期処理を停止
  periodicProcesses.forEach(processId => {
    clearInterval(processId);
  });
  periodicProcesses = [];
  
  isInitializationComplete = true;
  console.log("✅ 定期処理を停止しました");
}

// 初期化完了監視
function monitorInitializationComplete() {
  console.log("👀 初期化完了監視開始");
  
  // 10秒後に強制的に初期化完了とする
  setTimeout(() => {
    if (!isInitializationComplete) {
      console.log("⏰ 10秒経過 - 強制的に初期化完了");
      stopPeriodicProcesses();
    }
  }, 10000);
  
  // 定期的に初期化完了をチェック
  const checkInterval = setInterval(() => {
    if (checkInitializationComplete()) {
      console.log("🎉 初期化完了を検出");
      clearInterval(checkInterval);
      
      // 少し待ってから定期処理を停止
      setTimeout(() => {
        stopPeriodicProcesses();
      }, 2000);
    }
  }, 1000);
}

// 手動実行関数（ユーザー操作時に実行）
function executeMaintenanceOnDemand() {
  if (isInitializationComplete) {
    console.log("🔄 オンデマンド処理実行中...");
    
    // 必要な処理を実行
    if (window.triggerLabelRestore) {
      window.triggerLabelRestore();
    }
    
    if (window.triggerDataSync) {
      window.triggerDataSync();
    }
    
    if (window.processAllImagesWithCoordination) {
      window.processAllImagesWithCoordination();
    }
    
    if (window.applyMetaTagImagesToAllSlots) {
      window.applyMetaTagImagesToAllSlots(true);
    }
    
    console.log("✅ オンデマンド処理完了");
  }
}

// デバウンス機能付きオンデマンド実行
let onDemandTimeout;
function executeMaintenanceOnDemandDebounced() {
  clearTimeout(onDemandTimeout);
  onDemandTimeout = setTimeout(executeMaintenanceOnDemand, 500);
}

// ユーザー操作イベントリスナー
function setupUserActionListeners() {
  console.log("🎯 ユーザー操作リスナー設定");
  
  // ランダマイズボタン
  const randomizeButton = document.getElementById('randomize-button');
  if (randomizeButton) {
    randomizeButton.addEventListener('click', () => {
      console.log("🎲 ランダマイズボタンクリック");
      setTimeout(executeMaintenanceOnDemandDebounced, 1000);
    });
  }
  
  // 詳細ボタン（動的）
  document.addEventListener('click', (event) => {
    if (event.target.hasAttribute('data-subslot-toggle')) {
      console.log("🔍 詳細ボタンクリック");
      setTimeout(executeMaintenanceOnDemandDebounced, 500);
    }
  });
  
  // 制御パネル
  const controlPanels = document.querySelectorAll('[id*="control-panel"], [class*="control-panel"]');
  controlPanels.forEach(panel => {
    panel.addEventListener('click', () => {
      console.log("⚙️ 制御パネルクリック");
      executeMaintenanceOnDemandDebounced();
    });
  });
}

// 初期化システム
function initializeSmartControl() {
  console.log("🚀 スマート制御システム初期化");
  
  // 初期化完了監視開始
  monitorInitializationComplete();
  
  // ユーザー操作リスナー設定
  setTimeout(setupUserActionListeners, 2000);
}

// グローバル関数として公開
window.executeMaintenanceOnDemand = executeMaintenanceOnDemand;
window.executeMaintenanceOnDemandDebounced = executeMaintenanceOnDemandDebounced;
window.stopPeriodicProcesses = stopPeriodicProcesses;
window.isInitializationComplete = () => isInitializationComplete;

// DOMContentLoaded時に初期化
document.addEventListener('DOMContentLoaded', () => {
  console.log("📋 DOMContentLoaded - スマート制御システム開始");
  setTimeout(initializeSmartControl, 1000);
});

console.log("✅ スマート処理制御システムが準備完了");
