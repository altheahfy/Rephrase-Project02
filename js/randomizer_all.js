
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
      let identifier = `${entry.Slot}-${setNumber}`;
      if (entry.Slot === "O1") {
        const o1Count = groupSlots.filter(e => e.例文ID === id && e.Slot === "O1").length;
        if (o1Count > 1) {
          identifier = `${entry.Slot}-${setNumber}-${entry.Slot_display_order}`;
        }
      }
      return { ...entry, 識別番号: identifier };
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
      relatedSubslots.forEach(sub => {
        selectedSlots.push({ ...sub });
      });
    }
  });

  const o1Candidates = slotSets.flat().filter(e => e.Slot === "O1");
  const twoPartO1 = o1Candidates.filter(e => e.識別番号.match(/O1-\d+-\d+/));
  if (twoPartO1.length > 0) {
    twoPartO1.forEach(o1 => {
      selectedSlots.push({ ...o1 });
      groupSlots.filter(e =>
        e.例文ID === o1.例文ID &&
        e.Slot === o1.Slot &&
        e.SubslotID
      ).forEach(sub => {
        selectedSlots.push({ ...sub });
      });
    });
  } else if (o1Candidates.length > 0) {
    const chosen = o1Candidates[Math.floor(Math.random() * o1Candidates.length)];
    selectedSlots.push({ ...chosen });
    groupSlots.filter(e =>
      e.例文ID === chosen.例文ID &&
      e.Slot === chosen.Slot &&
      e.SubslotID
    ).forEach(sub => {
      selectedSlots.push({ ...sub });
    });
  }

  selectedSlots.sort((a, b) => (a.Slot_display_order || 0) - (b.Slot_display_order || 0));

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
