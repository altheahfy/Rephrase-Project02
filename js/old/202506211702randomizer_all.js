
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
    const slots = groupSlots.filter(entry => entry.例文ID === id && !entry.SubslotID).map(entry => ({
      ...entry,
      識別番号: `${entry.Slot}-${setNumber}`
    }));
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

  const o1Entries = groupSlots.filter(e => e.Slot === "O1");
  const o1Orders = [...new Set(o1Entries.map(e => e.Slot_display_order))];
  if (o1Orders.length > 1) {
    const o1Head = o1Entries.find(e => e.Slot_display_order === Math.min(...o1Orders));
    const o1Tail = o1Entries.find(e => e.Slot_display_order === Math.max(...o1Orders));
    if (o1Head) {
      selectedSlots.push({ ...o1Head });
      const subHead = groupSlots.filter(e =>
        e.例文ID === o1Head.例文ID &&
        e.Slot === o1Head.Slot &&
        e.SubslotID
      );
      subHead.forEach(sub => selectedSlots.push({ ...sub }));
    }
    if (o1Tail) {
      selectedSlots.push({ ...o1Tail });
      const subTail = groupSlots.filter(e =>
        e.例文ID === o1Tail.例文ID &&
        e.Slot === o1Tail.Slot &&
        e.SubslotID
      );
      subTail.forEach(sub => selectedSlots.push({ ...sub }));
    }
  } else if (o1Entries.length > 0) {
    const o1 = o1Entries[0];
    selectedSlots.push({ ...o1 });
    const sub = groupSlots.filter(e =>
      e.例文ID === o1.例文ID &&
      e.Slot === o1.Slot &&
      e.SubslotID
    );
    sub.forEach(s => selectedSlots.push({ ...s }));
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
