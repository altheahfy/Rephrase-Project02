/* =================================================================== */
/* 📱 モバイル上下2分割システム - PC版そのまま表示                     */
/* =================================================================== */
/* PC版完全保護、JavaScriptによる追加制御は最小限 */

// モバイル検出時の初期化（最小限の処理のみ）
function initializeMobileSplitView() {
  if (!document.documentElement.classList.contains('mobile-device')) {
    console.log("💻 PC版: 上下分割システムをスキップ");
    return;
  }
  
  console.log("📱 モバイル上下2分割システム初期化開始");
  
  // PC版をそのまま表示、追加のDOM操作は行わない
  // CSSで位置・サイズのみ調整済み
  
  console.log("✅ モバイル上下2分割システム初期化完了（PC版そのまま表示）");
}

// 📱 モバイル検出時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  // モバイル検出後に初期化
  setTimeout(() => {
    if (document.documentElement.classList.contains('mobile-device')) {
      initializeMobileSplitView();
    }
  }, 100);
});

// 🔄 ランダマイズ後の処理（PC版システムは保護）
window.addEventListener('randomize-complete', function() {
  if (document.documentElement.classList.contains('mobile-device')) {
    // PC版システムは完全保護、特別な処理は不要
    console.log("📱 ランダマイズ完了: PC版システム保護のため追加処理なし");
  }
});
