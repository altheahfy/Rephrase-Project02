// renderer_core.js
export function renderSlotImage(slotId, imagePath) {
  const img = document.querySelector(`#${slotId} img`);
  if (img) {
    img.src = imagePath;
    img.alt = `Image for ${slotId}`;
  }
}

export function renderAllSlots(slotImageMap) {
  Object.entries(slotImageMap).forEach(([slotId, imagePath]) => {
    renderSlotImage(slotId, imagePath);
  });
}