/**
 * 指定された slotId のテキストを更新する
 */
function updateSlotDisplay(slotId, text) {
  const element = document.getElementById(slotId);
  if (!element) return;
  const span = element.querySelector(".chunk-content");
  if (span) {
    span.textContent = text;
  } else {
    element.textContent = text;
  }
}

/**
 * 指定された slotId の画像を更新する
 */
function updateSlotImage(slotId, imageFile) {
  const element = document.getElementById(slotId);
  if (!element) return;

  let img = element.querySelector("img");
  if (!img) {
    img = document.createElement("img");
    element.appendChild(img);
  }

  img.src = `slot_images/common/${imageFile}`;
  img.alt = slotId;
  img.onerror = () => {
    console.warn(`⚠️ image not found: ${imageFile}`);
    img.style.display = "none";
  };
  img.onload = () => {
    img.style.display = "inline-block";
  };
}

// 明示的に export
export { updateSlotDisplay, updateSlotImage };