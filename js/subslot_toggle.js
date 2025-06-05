// subslot_toggle_v4.js

function toggleExclusiveSubslot(slotId) {
  const subslotIds = ["o1", "c"];
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