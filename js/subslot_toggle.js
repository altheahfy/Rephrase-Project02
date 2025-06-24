
function toggleExclusiveSubslot(slotId) {
  console.log(`🔑 toggleExclusiveSubslot called for slot-${slotId}-sub`);

  const subslotIds = ["o1", "c", "o2", "m1", "s", "m2", "c2", "m3"];
  const target = document.getElementById(`slot-${slotId}-sub`);
  if (!target) {
    console.warn(`⚠ toggleExclusiveSubslot: target slot-${slotId}-sub not found`);
    return;
  }

  const isOpen = target.style.display !== "none";

  // 全 subslot を閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) el.style.display = "none";
  });

  // 対象のみ開く
  if (!isOpen) {
    target.style.display = "flex";
    target.style.visibility = "visible";
    target.style.minHeight = "100px";
    console.log(`✅ slot-${slotId}-sub opened`);
  } else {
    console.log(`ℹ slot-${slotId}-sub was already open, now closed`);
  }
}

// DOM 構築後にイベント登録（既存ボタンに対応）
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("[data-subslot-toggle], .subslot-toggle-button button");
  buttons.forEach(button => {
    let slotId = button.getAttribute("data-subslot-toggle");
    if (!slotId) {
      // fallback: onclick で直接呼ばれるボタンは解析
      const onclickAttr = button.getAttribute("onclick");
      const match = onclickAttr && onclickAttr.match(/toggleExclusiveSubslot\(['"](.+?)['"]\)/);
      if (match) slotId = match[1];
    }
    if (slotId) {
      button.addEventListener("click", () => toggleExclusiveSubslot(slotId));
    }
  });
});

window.toggleExclusiveSubslot = toggleExclusiveSubslot;
