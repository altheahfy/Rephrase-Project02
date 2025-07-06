// パフォーマンスデバッグ用スクリプト
console.log("🔍 デバッグツール: パフォーマンス監視を開始");

// 各種処理の実行回数を記録
const performanceCounters = {
  imageProcessing: 0,
  mutationObserver: 0,
  intervalChecks: 0,
  metaTagApplications: 0
};

// 元の関数をラップして実行回数を記録
const originalProcessAllImages = window.processAllImagesWithCoordination;
if (originalProcessAllImages) {
  window.processAllImagesWithCoordination = function() {
    performanceCounters.imageProcessing++;
    console.log(`🔄 画像処理実行回数: ${performanceCounters.imageProcessing}`);
    return originalProcessAllImages.apply(this, arguments);
  };
}

// パフォーマンス統計を表示する関数
window.showPerformanceStats = function() {
  console.log("📊 パフォーマンス統計:");
  console.log(`  画像処理: ${performanceCounters.imageProcessing}回`);
  console.log(`  MutationObserver: ${performanceCounters.mutationObserver}回`);
  console.log(`  定期チェック: ${performanceCounters.intervalChecks}回`);
  console.log(`  メタタグ適用: ${performanceCounters.metaTagApplications}回`);
  return performanceCounters;
};

// 統計をリセットする関数
window.resetPerformanceStats = function() {
  Object.keys(performanceCounters).forEach(key => {
    performanceCounters[key] = 0;
  });
  console.log("📊 パフォーマンス統計をリセットしました");
};

// 10秒ごとに統計を表示（無効化）
// setInterval(() => {
//   if (performanceCounters.imageProcessing > 0 || performanceCounters.mutationObserver > 0) {
//     console.log("📊 定期パフォーマンス報告:", performanceCounters);
//   }
// }, 10000);

// 手動で統計を確認する関数
window.showPerformanceReport = function() {
  if (performanceCounters.imageProcessing > 0 || performanceCounters.mutationObserver > 0) {
    console.log("📊 パフォーマンス報告:", performanceCounters);
  } else {
    console.log("📊 パフォーマンス報告: 処理実行なし");
  }
};

console.log("✅ パフォーマンス監視ツールが準備できました");
console.log("使用方法: showPerformanceStats() - 統計表示, resetPerformanceStats() - 統計リセット");
