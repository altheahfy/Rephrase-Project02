// slot_data_loader.js

export async function loadSlotImageAndTextMap(structureId) {
  const idPart = structureId.split("-").pop(); // "010"
  const folderNumber = parseInt(idPart, 10);   // 10
  const jsonPath = `slot_assignments/${folderNumber}/slot_assignment.json`;

  const response = await fetch(jsonPath);
  const data = await response.json();

  const slotImageMap = {};
  const slotTextMap = {};
  const slotKeys = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

  slotKeys.forEach(key => {
    const slotData = data[`slot-${key}`];
    const domId = `slot-o1-sub-${key}`;
    if (slotData) {
      if (slotData.image) {
        slotImageMap[domId] = slotData.image;
      }
      if (slotData.text) {
        slotTextMap[domId] = slotData.text;
      }
    }
  });

  return {
    slotImageMap,
    slotTextMap
  };
}