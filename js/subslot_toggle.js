function toggleExclusiveSubslot(slotId) {
  if (toggleExclusiveSubslot.lock) return;
  toggleExclusiveSubslot.lock = true;
  setTimeout(() => { toggleExclusiveSubslot.lock = false; }, 100);
  // console.log(`🔑 toggleExclusiveSubslot called for slot-${slotId}-sub`);

  const subslotIds = ["o1", "c1", "o2", "m1", "s", "m2", "c2", "m3"];
  const target = document.getElementById(`slot-${slotId}-sub`);
  if (!target) {
    console.warn(`⚠ toggleExclusiveSubslot: target slot-${slotId}-sub not found`);
    return;
  }

  const isOpen = getComputedStyle(target).display !== "none";

  // 全 subslot を閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) {
      el.style.setProperty("display", "none", "important");
    }
  });

  // 対象のみ開く
  if (!isOpen) {
    target.style.setProperty("display", "flex", "important");
    target.style.setProperty("visibility", "visible", "important");
    target.style.setProperty("min-height", "100px", "important");
    // console.log(`✅ slot-${slotId}-sub opened`);

    // ★★★ 並べ替え処理を呼び出す ★★★
    if (window.reorderSubslotsInContainer && window.loadedJsonData) {
      console.log(`🔄 Reordering subslots in ${target.id}`);
      window.reorderSubslotsInContainer(target, window.loadedJsonData);
    } else {
      console.warn("⚠ reorderSubslotsInContainer or window.loadedJsonData not found");
    }

  } else {
    // console.log(`ℹ slot-${slotId}-sub was already open, now closed`);
  }
}

// ページ読み込み時に全サブスロットを初期化（閉じる）する関数
function initializeSubslots() {
  console.log("🔄 Initializing subslots to be closed.");
  const subslotIds = ["o1", "c1", "o2", "m1", "s", "m2", "c2", "m3"];
  
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) {
      el.style.setProperty("display", "none", "important");
    }
  });
  
  const allSubslotElements = document.querySelectorAll('[id$="-sub"]');
  allSubslotElements.forEach(el => {
    if (el && !el.id.includes('wrapper')) { // wrapper要素は除外
      el.style.setProperty("display", "none", "important");
    }
  });
}

// イベントリスナーをバインドする統一された関数
function bindSubslotToggleButtons() {
  const buttons = document.querySelectorAll("[data-subslot-toggle], .subslot-toggle-button button");
  // console.log(`🔍 Binding toggle buttons. Found ${buttons.length} candidates.`);
  
  buttons.forEach(button => {
    let slotId = button.getAttribute("data-subslot-toggle");
    if (!slotId) {
      const onclickAttr = button.getAttribute("onclick");
      if (onclickAttr) {
        const match = onclickAttr.match(/toggleExclusiveSubslot\(['"](.+?)['"]\)/);
        if (match) slotId = match[1];
      }
    }

    if (slotId) {
      // onclickプロパティに関数を設定することで、リスナーの重複を避ける
      button.onclick = () => {
        toggleExclusiveSubslot(slotId);
      };
      // console.log(`✅ Click handler attached for slotId: ${slotId}`);
    } else {
      // console.warn(`⚠ Could not resolve slotId for button:`, button);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 DOMContentLoaded: Initializing subslots and binding toggle buttons.");
  initializeSubslots();
  bindSubslotToggleButtons();
});

window.toggleExclusiveSubslot = toggleExclusiveSubslot;
// 動的コンテンツのロード後などに再バインドできるよう、グローバルに公開
window.bindSubslotToggleButtons = bindSubslotToggleButtons;
