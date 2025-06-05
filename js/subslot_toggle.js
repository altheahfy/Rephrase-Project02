// subslot_toggle_v3.js

function toggleExclusiveSubslot(slotId) {
  // 明示的に対象スロットID列挙
  const subslotIds = ["o1", "c"];

  // すでに開かれているスロットを確認
  const target = document.getElementById(`slot-${slotId}-sub`);
  const isOpen = target && target.style.display !== "none";

  // 全て閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) el.style.display = "none";
  });

  // 再度開く必要があるなら開く
  if (!isOpen && target) {
    target.style.display = "flex";
  }
}