// test_controller.js
import { renderAllSlots, renderAllTexts } from './renderer_core.js';
import { loadSlotImageAndTextMap } from './slot_data_loader.js';

const structureId = "INF-N-OBJ-010";

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const { slotImageMap, slotTextMap } = await loadSlotImageAndTextMap(structureId);
    renderAllSlots();
    renderAllTexts(slotTextMap);
  } catch (error) {
    console.error("描画エラー:", error);
  }
});