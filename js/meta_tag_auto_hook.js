// メタタグシステム自動実行フック
console.log("🎯 メタタグシステム自動実行フック読み込み");

// ページ読み込み完了時の自動実行（最適化版）
window.addEventListener('load', function() {
  console.log("📋 window.load イベント発生 - メタタグシステムを実行");
  
  // 初期化時のみ実行
  setTimeout(() => {
    if (window.applyMetaTagImagesToAllSlots) {
      console.log("🎯 [HOOK] 初期化時メタタグシステム実行");
      window.applyMetaTagImagesToAllSlots(true);
    }
  }, 1000);
  
  // 確実性のため追加で1回実行
  setTimeout(() => {
    if (window.applyMetaTagImagesToAllSlots) {
      console.log("🎯 [HOOK] 追加実行（確実性のため）");
      window.applyMetaTagImagesToAllSlots(true);
    }
  }, 3000);
});

// スロットのテキストが変更されたときの自動実行
function setupTextChangeObserver() {
  const observer = new MutationObserver((mutations) => {
    let textChanged = false;
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' || mutation.type === 'characterData') {
        const target = mutation.target;
        if (target.closest('.slot-phrase') || target.classList.contains('slot-phrase')) {
          textChanged = true;
        }
      }
    });
    
    if (textChanged) {
      console.log("🔄 [HOOK] スロットテキスト変更を検出");
      setTimeout(() => {
        if (window.applyMetaTagImagesToAllSlots) {
          window.applyMetaTagImagesToAllSlots(true);
        }
      }, 200);
    }
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true
  });
  
  console.log("✅ [HOOK] テキスト変更監視開始");
}

// DOMContentLoaded時に監視を開始
document.addEventListener('DOMContentLoaded', function() {
  console.log("🚀 [HOOK] DOMContentLoaded - テキスト変更監視を開始");
  setTimeout(setupTextChangeObserver, 500);
});

console.log("✅ メタタグシステム自動実行フックが準備完了");
