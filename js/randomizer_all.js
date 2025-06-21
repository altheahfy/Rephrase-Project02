
export function randomizeAll(slotData) {
  const groups = [...new Set(slotData.map(entry => entry.V_group_key).filter(v => v))];
  if (groups.length === 0) {
    console.warn("V_group_key 母集団が見つかりません。");
    return [];
  }

  const selectedGroup = groups[Math.floor(Math.random() * groups.length)];
  console.log(`🟢 選択 V_group_key: ${selectedGroup}`);

  const groupSlots = slotData.filter(entry => entry.V_group_key === selectedGroup);
  const exampleIDs = [...new Set(groupSlots.map(entry => entry.例文ID).filter(id => id))];

  if (exampleIDs.length === 0) {
    console.warn("例文ID 母集団が見つかりません。");
    return [];
  }

  let slotSets = [];
  exampleIDs.forEach((id, index) => {
    const setNumber = index + 1;
    const slots = groupSlots.filter(entry => entry.例文ID === id && !entry.SubslotID).map(entry => {
      let o1Siblings = groupSlots.filter(e => e.例文ID === id && e.Slot === "O1");
      let o1Orders = [...new Set(o1Siblings.map(e => e.Slot_display_order))];
      let o1Index = o1Orders.indexOf(entry.Slot_display_order) + 1;
      let idSuffix = "";
      if (entry.Slot === "O1" && o1Orders.length > 1) {
        idSuffix = `-${o1Index}`;
      }
      return {
        ...entry,
        識別番号: `${entry.Slot}-${setNumber}${idSuffix}`
      };
    });
    slotSets.push(slots);
  });

  let selectedSlots = [];
  const slotTypes = [...new Set(groupSlots.map(entry => entry.Slot).filter(s => s))];
  slotTypes.forEach(type => {
    if (type === "O1") return;
    const candidates = slotSets.flat().filter(entry => entry.Slot === type);
    if (candidates.length > 0) {
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      selectedSlots.push({ ...chosen });
      const relatedSubslots = groupSlots.filter(e =>
        e.例文ID === chosen.例文ID &&
        e.Slot === chosen.Slot &&
        e.SubslotID
      );
      relatedSubslots.forEach(sub => selectedSlots.push({ ...sub }));
    }
  });

  const o1Candidates = slotSets.flat().filter(e => e.Slot === "O1");
  const doubleO1 = o1Candidates.filter(e => /O1-\d+-\d+/.test(e.識別番号));
  if (doubleO1.length > 0) {
    doubleO1.forEach(e => selectedSlots.push({ ...e }));
  } else {
    if (o1Candidates.length > 0) {
      const chosen = o1Candidates[Math.floor(Math.random() * o1Candidates.length)];
      selectedSlots.push({ ...chosen });
    }
  }

  window.slotSets = slotSets;
  window.slotTypes = slotTypes;
  window.lastSelectedSlots = selectedSlots;

  return selectedSlots.map(slot => ({
    Slot: slot.Slot || "",
    SlotPhrase: slot.SlotPhrase || "",
    SlotText: slot.SlotText || "",
    Slot_display_order: slot.Slot_display_order || 0,
    PhraseType: slot.PhraseType || "",
    SubslotID: slot.SubslotID || "",
    SubslotElement: slot.SubslotElement || "",
    SubslotText: slot.SubslotText || "",
    display_order: slot.display_order || 0,
    識別番号: slot.識別番号 || ""
  }));
}
