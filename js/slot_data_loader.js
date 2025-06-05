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
  const subPrefixes = ["o1", "c"]; // 展開対象subslot接頭辞

  slotKeys.forEach(key => {
    const upperId = `slot-${key}`;
    const upperData = data[upperId];
    if (upperData) {
      if (upperData.image) slotImageMap[upperId] = upperData.image;
      if (upperData.text) slotTextMap[upperId] = upperData.text;
    }

    subPrefixes.forEach(prefix => {
      const subId = `slot-${prefix}-sub-${key}`;
      const subData = data[subId];
      if (subData) {
        if (subData.image) slotImageMap[subId] = subData.image;
        if (subData.text) slotTextMap[subId] = subData.text;
      }
    });
  });

  return {
    slotImageMap,
    slotTextMap
  };
}