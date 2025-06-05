
// subslot_renderer_static.js
window.addEventListener("DOMContentLoaded", () => {
  const slotIds = [
    "slot-o1-sub-m1", "slot-o1-sub-s", "slot-o1-sub-aux", "slot-o1-sub-m2",
    "slot-o1-sub-v", "slot-o1-sub-c", "slot-o1-sub-o1", "slot-o1-sub-o2",
    "slot-o1-sub-c2", "slot-o1-sub-m3"
  , "slot-o2-sub-m1", "slot-o2-sub-s", "slot-o2-sub-aux", "slot-o2-sub-m2", "slot-o2-sub-v", "slot-o2-sub-c", "slot-o2-sub-o1", "slot-o2-sub-o2", "slot-o2-sub-c2", "slot-o2-sub-m3", "slot-m1-sub-m1", "slot-m1-sub-s", "slot-m1-sub-aux", "slot-m1-sub-m2", "slot-m1-sub-v", "slot-m1-sub-c", "slot-m1-sub-o1", "slot-m1-sub-o2", "slot-m1-sub-c2", "slot-m1-sub-m3", "slot-s-sub-m1", "slot-s-sub-s", "slot-s-sub-aux", "slot-s-sub-m2", "slot-s-sub-v", "slot-s-sub-c", "slot-s-sub-o1", "slot-s-sub-o2", "slot-s-sub-c2", "slot-s-sub-m3", "slot-m2-sub-m1", "slot-m2-sub-s", "slot-m2-sub-aux", "slot-m2-sub-m2", "slot-m2-sub-v", "slot-m2-sub-c", "slot-m2-sub-o1", "slot-m2-sub-o2", "slot-m2-sub-c2", "slot-m2-sub-m3", "slot-c2-sub-m1", "slot-c2-sub-s", "slot-c2-sub-aux", "slot-c2-sub-m2", "slot-c2-sub-v", "slot-c2-sub-c", "slot-c2-sub-o1", "slot-c2-sub-o2", "slot-c2-sub-c2", "slot-c2-sub-m3", "slot-m3-sub-m1", "slot-m3-sub-s", "slot-m3-sub-aux", "slot-m3-sub-m2", "slot-m3-sub-v", "slot-m3-sub-c", "slot-m3-sub-o1", "slot-m3-sub-o2", "slot-m3-sub-c2", "slot-m3-sub-m3"];

  slotIds.forEach(id => {
    const img = document.querySelector(`#${id} img`);
    if (img) {
      // 仮の画像を共通適用（後で動的に切替可能）
      img.src = `slot_images/common/placeholder.png`;
      img.alt = `Placeholder for ${id}`;
    }
  });
});
