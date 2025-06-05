// slot_data_loader.js

export async function loadSlotImageMap(structureId) {
  // 末尾の構文番号（例: 010）から数値フォルダ名を導出（例: 10）
  const idPart = structureId.split("-").pop(); // "010"
  const folderNumber = parseInt(idPart, 10);   // 10
  const jsonPath = `slot_assignment/${folderNumber}/slot_assignment.json`;

  const response = await fetch(jsonPath);
  const data = await response.json();

  const slotImageMap = {};
  const slotKeys = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

  slotKeys.forEach(key => {
    const slotData = data[`slot-${key}`];
    if (slotData && slotData.image) {
      slotImageMap[`slot-o1-sub-${key}`] = slotData.image;
    }
  });

  return slotImageMap;
}