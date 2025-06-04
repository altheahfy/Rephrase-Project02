
// subslot_renderer_static.js
window.addEventListener("DOMContentLoaded", () => {
  const slotIds = [
    "slot-o1-sub-m1", "slot-o1-sub-s", "slot-o1-sub-aux", "slot-o1-sub-m2",
    "slot-o1-sub-v", "slot-o1-sub-c", "slot-o1-sub-o1", "slot-o1-sub-o2",
    "slot-o1-sub-c2", "slot-o1-sub-m3"
  ];

  slotIds.forEach(id => {
    const img = document.querySelector(`#${id} img`);
    if (img) {
      // 仮の画像を共通適用（後で動的に切替可能）
      img.src = `slot_images/common/placeholder.png`;
      img.alt = `Placeholder for ${id}`;
    }
  });
});
