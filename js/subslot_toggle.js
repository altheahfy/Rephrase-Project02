
function toggleExclusiveSubslot(slotId) {
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
