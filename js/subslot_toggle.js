// subslot_toggle_v2.js

function toggleExclusiveSubslot(slotId) {
  const subslotIds = ["o1", "c"];
  let isCurrentlyVisible = false;

  // チェック：既に開かれているか確認
  const current = document.getElementById(`slot-${slotId}-sub`);
  if (current && current.style.display !== "none") {
    isCurrentlyVisible = true;
  }

  // 全て閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) el.style.display = "none";
  });

  // 対象だけ開く（現在開かれていた場合はそのまま閉じる）
  if (!isCurrentlyVisible && current) {
    current.style.display = "flex";
  }
}