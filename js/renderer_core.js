// renderer_core.js

export function renderSlotImage(slotId, imagePath) {
  const img = document.querySelector(`#${slotId} img`);
  if (img) {
    console.log(`描画中: ${slotId} → ${imagePath}`);
    img.src = imagePath;
    img.alt = `Image for ${slotId}`;
  }
}

export function renderSlotText(slotId, textContent) {
  const textContainer = document.querySelector(`#${slotId} .slot-text`);
  if (textContainer) {
    console.log(`テキスト描画: ${slotId} → ${textContent}`);
    textContainer.textContent = textContent;
  }
}

export function renderAllSlots(slotImageMap) {
  Object.entries(slotImageMap).forEach(([slotId, imagePath]) => {
    renderSlotImage(slotId, imagePath);
  });
}

export function renderAllTexts(slotTextMap) {
  Object.entries(slotTextMap).forEach(([slotId, text]) => {
    renderSlotText(slotId, text);
  });
}