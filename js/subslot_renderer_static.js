// subslot_renderer_static.js
// ✅ TEST ONLY: This file is for verifying placeholder image display in static subslot structure.
// ❗️ Do not use in production. Replace with dynamic renderer in the final system.

document.addEventListener("DOMContentLoaded", () => {
  const slotIds = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];
  slotIds.forEach(id => {
    const img = document.querySelector(`#slot-o1-sub-${id} img`);
    if (img) {
      img.src = "slot_images/common/placeholder.png";
    }
  });
});
