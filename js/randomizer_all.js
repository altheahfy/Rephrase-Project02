
/**
 * V_group_key 母集団から1つ選び、スロット種別ごとに1候補のみランダム選択し返す。
 * structure_builder.js に渡すデータを生成。
 * @param {Array} slotData - slot_order_data.json のデータ配列
 * @returns {Array} 選択されたスロット群（上位スロット＋サブスロット含む）のデータ配列
 */
export function randomizeAll(slotData) {
  const groups = [...new Set(slotData.map(entry => entry.V_group_key).filter(v => v))];
  if (groups.length === 0) {
    console.warn("V_group_key 母集団が見つかりません。");
    return [];
  }

  const selectedGroup = groups[Math.floor(Math.random() * groups.length)];
  console.log(`🟢 選択 V_group_key: ${selectedGroup}`);

  const groupSlots = slotData.filter(entry => entry.V_group_key === selectedGroup);
  const slotTypes = [...new Set(groupSlots.map(entry => entry.Slot).filter(s => s))];
  const result = [];

  slotTypes.forEach(slotType => {
    const candidates = groupSlots.filter(entry => entry.Slot === slotType && !entry.SubslotID);
    if (candidates.length > 0) {
      const selected = candidates[Math.floor(Math.random() * candidates.length)];
      result.push(selected);
      // サブスロットも同じ Slot のものを追加
      const subslots = groupSlots.filter(entry => entry.Slot === slotType && entry.SubslotID);
      result.push(...subslots);
    }
  });

  window.lastSelectedSlots = result;

  return result.map(slot => ({
    Slot: slot.Slot || "",
    SlotPhrase: slot.SlotPhrase || "",
    SlotText: slot.SlotText || "",
    Slot_display_order: slot.Slot_display_order || 0,
    PhraseType: slot.PhraseType || "",
    SubslotID: slot.SubslotID || "",
    SubslotElement: slot.SubslotElement || "",
    SubslotText: slot.SubslotText || "",
    display_order: slot.display_order || 0
  }));
}