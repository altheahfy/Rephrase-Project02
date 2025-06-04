// slot_data_loader.js

export async function loadSlotImageMap(structureId) {
  const response = await fetch(`slot_assignment/${structureId}.json`);
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