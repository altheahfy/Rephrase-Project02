// subslot_toggle.js

// 常に1つのslotだけが開くように制御する
function toggleExclusiveSubslot(slotId) {
  const subslotIds = ["o1", "c"]; // 展開対象のslot IDを列挙

  // 全て閉じる
  subslotIds.forEach(id => {
    const subEl = document.getElementById(`slot-${id}-sub`);
    if (subEl) subEl.style.display = "none";
  });

  // 対象だけ開く
  const target = document.getElementById(`slot-${slotId}-sub`);
  if (target) target.style.display = "flex";
}