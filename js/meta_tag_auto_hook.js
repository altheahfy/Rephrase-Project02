// メタタグシステム自動実行フック
console.log("🎯 メタタグシステム自動実行フック読み込み");

// ページ読み込み完了時の自動実行
window.addEventListener('load', function() {
  console.log("📋 window.load イベント発生 - メタタグシステムを実行");
  
  // 複数のタイミングで実行して確実にする
  setTimeout(() => {
    if (window.applyMetaTagImagesToAllSlots) {
      console.log("🎯 [HOOK] 1秒後にメタタグシステム実行");
      window.applyMetaTagImagesToAllSlots(true);
    }
  }, 1000);
  
  setTimeout(() => {
    if (window.applyMetaTagImagesToAllSlots) {
      console.log("🎯 [HOOK] 2秒後にメタタグシステム実行");
      window.applyMetaTagImagesToAllSlots(true);
    }
  }, 2000);
  
  setTimeout(() => {
    if (window.applyMetaTagImagesToAllSlots) {
      console.log("🎯 [HOOK] 3秒後にメタタグシステム実行");
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
