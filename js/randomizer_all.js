
/**
 * 全slot（上位 + subslot）に対して、テキストを反映。
 * slotDataのkeyをDOMのslot-idと一致させて更新。
 */
export function randomizeAll(data) {
  for (const [slotId, text] of Object.entries(data)) {
    const el = document.querySelector(`#${slotId} .slot-text`);
    if (el) {
      el.textContent = text;
      console.log(`🟢 テキスト反映: \${slotId} → \${text}`);
    } else {
      console.warn(`🟥 slot-text DOMが見つかりません: \${slotId}`);
    }
  }
}
