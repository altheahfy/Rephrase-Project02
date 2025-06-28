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
  const uniqueOrders = [...new Set(o1Entries.map(e => e.Slot_display_order))];

  if (uniqueOrders.length > 1) {
    uniqueOrders.forEach(order => {
      const targets = o1Entries.filter(e => e.Slot_display_order === order);
      targets.forEach(t => selectedSlots.push({ ...t }));
    });
  } else if (o1Entries.length > 0) {
    const clauseO1 = o1Entries.filter(e => e.PhraseType === "clause");
    if (clauseO1.length > 0) {
      const chosen = clauseO1[Math.floor(Math.random() * clauseO1.length)];
      selectedSlots.push({ ...chosen });
      const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
      subslots.forEach(sub => selectedSlots.push({ ...sub }));
    } else {
      const wordO1 = o1Entries.filter(e => e.PhraseType !== "clause");
      if (wordO1.length > 0) {
        const chosen = wordO1[Math.floor(Math.random() * wordO1.length)];
        selectedSlots.push({ ...chosen });
        const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
        subslots.forEach(sub => selectedSlots.push({ ...sub }));
      }
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

// 個別スロットランダマイズ関数
export function randomizeIndividualSlot(slotData, targetSlot, currentData) {
  console.log(`🎲 個別ランダマイズ開始: ${targetSlot}`);
  
  // 現在のV_group_keyを維持
  const currentVGroup = currentData.find(entry => entry.V_group_key)?.V_group_key;
  if (!currentVGroup) {
    console.warn("現在のV_group_keyが見つかりません");
    return currentData;
  }
  
  // 同じV_group_key内の該当スロットの候補を取得
  const candidates = slotData.filter(entry => 
    entry.V_group_key === currentVGroup && 
    entry.Slot === targetSlot &&
    !entry.SubslotID
  );
  
  if (candidates.length === 0) {
    console.warn(`${targetSlot}スロットの候補が見つかりません`);
    return currentData;
  }
  
  // ランダムに選択
  const selectedCandidate = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択された${targetSlot}:`, selectedCandidate);
  
  // 新しいデータセットを作成（該当スロットのみ更新）
  let newData = currentData.filter(entry => entry.Slot !== targetSlot);
  
  // 選択されたスロットを追加
  newData.push({ ...selectedCandidate });
  
  // 関連するサブスロットも追加
  const relatedSubslots = slotData.filter(entry =>
    entry.例文ID === selectedCandidate.例文ID &&
    entry.Slot === selectedCandidate.Slot &&
    entry.SubslotID
  );
  
  relatedSubslots.forEach(sub => {
    newData.push({ ...sub });
  });
  
  console.log(`✅ ${targetSlot}の個別ランダマイズ完了`);
  return newData;
}
