
// subslot_renderer_dev.js
window.addEventListener("DOMContentLoaded", () => {
  const slotIds = [
    "slot-o1-sub-m1", "slot-o1-sub-s", "slot-o1-sub-aux", "slot-o1-sub-m2",
    "slot-o1-sub-v", "slot-o1-sub-c", "slot-o1-sub-o1", "slot-o1-sub-o2",
    "slot-o1-sub-c2", "slot-o1-sub-m3",

    "slot-o2-sub-m1", "slot-o2-sub-s", "slot-o2-sub-aux", "slot-o2-sub-m2",
    "slot-o2-sub-v", "slot-o2-sub-c", "slot-o2-sub-o1", "slot-o2-sub-o2",
    "slot-o2-sub-c2", "slot-o2-sub-m3",

    "slot-c-sub-m1", "slot-c-sub-s", "slot-c-sub-aux", "slot-c-sub-m2",
    "slot-c-sub-v", "slot-c-sub-c", "slot-c-sub-o1", "slot-c-sub-o2",
    "slot-c-sub-c2", "slot-c-sub-m3"
  ];

  slotIds.forEach(id => {
    const img = document.querySelector(`#${id} img`);
    if (img) {
      console.log(`Rendering: ${id}`);
      img.src = `slot_images/common/placeholder.png`;
      img.alt = `Placeholder for ${id}`;
    } else {
      console.warn(`Not found: ${id}`);
    }
  });
});
