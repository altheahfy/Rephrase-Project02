
/**
 * 全slot（上位 + subslot）に対して、テキストと画像を一括で反映
 */
export function randomizeAll(data) {
  for (const [slotId, text] of Object.entries(data)) {
    if (text && typeof text === "string") {
      const el = document.querySelector(`#${slotId} .slot-text`);
      if (el) {
        el.textContent = text;
        console.log(`🟢 テキスト反映: \${slotId} → \${text}`);
      } else {
        console.warn(`⚠️ slot-text not found for \${slotId}`);
      }
    }
  }
}
