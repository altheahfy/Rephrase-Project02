// test_controller.js
import { renderAllSlots } from './renderer_core.js';
import { loadSlotImageMap } from './slot_data_loader.js';

const structureId = "INF-N-OBJ-010";

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const slotImageMap = await loadSlotImageMap(structureId);
    renderAllSlots(slotImageMap);
  } catch (error) {
    console.error("描画エラー:", error);
  }
});