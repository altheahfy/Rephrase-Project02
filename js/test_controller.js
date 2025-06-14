// test_controller.js
import { renderAllSlots, renderAllTexts, renderAllSubslots } from './renderer_core.js';
import { loadSlotImageAndTextMap } from './slot_data_loader.js';

const structureId = "INF-N-OBJ-010";

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const { slotImageMap, slotTextMap } = await loadSlotImageAndTextMap(structureId);
    window.lastSlotData = window.lastSlotData || {};
    renderAllSlots(window.lastSlotData);
    renderAllTexts(slotTextMap);
    renderAllSubslots(window.lastSlotData);
  } catch (error) {
    console.error("描画エラー:", error);
  }
});