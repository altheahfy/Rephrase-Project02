import { injectSlotText } from './renderer_core.js';

function toggleExclusiveSubslot(slotId) {
  if (slotId === "s") console.log("✅ slot-s-sub toggle triggered");

  const subslotIds = ["o1", "c", "o2", "m1", "s", "m2", "c2", "m3"];
  const target = document.getElementById(`slot-${slotId}-sub`);
  const isOpen = target && target.style.display !== "none";

  // 全 subslot を閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) el.style.display = "none";
  });

  // 必要なら開く
  if (!isOpen && target) {
    target.style.display = "flex";
    target.style.visibility = "visible";
    target.style.minHeight = "100px";
    injectSlotText(`slot-${slotId}-sub`);  // PH-07-8-h-9 inject
    console.log("✅ 強制表示style適用: ", target.id);
    console.log("🔍 target.style.display set to:", target.style.display);
    const forceRedraw = target.offsetHeight; // force reflow
    console.log("📐 target.offsetHeight (for reflow):", forceRedraw);
  }

  // ラベル更新呼び出し
  updateSubslotLabel(slotId);
}

// ↓ DOM 構築後にイベント登録
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("[data-subslot-toggle]");
  buttons.forEach(button => {
    const slotId = button.getAttribute("data-subslot-toggle");
    button.addEventListener("click", () => toggleExclusiveSubslot(slotId));
  });
});


window.toggleExclusiveSubslot = toggleExclusiveSubslot;