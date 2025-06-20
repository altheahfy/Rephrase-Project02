
/**
 * V_group_key 母集団から各スロットごとに1つずつ選び、そのスロット群を返す。
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

  // スロット種別ごとにランダム選択
  const slotTypes = [...new Set(slotData.map(entry => entry.Slot).filter(s => s))];
  let result = [];

  slotTypes.forEach(slotType => {
    const candidates = slotData.filter(entry => entry.V_group_key === selectedGroup && entry.Slot === slotType);
    if (candidates.length > 0) {
      const selected = candidates[Math.floor(Math.random() * candidates.length)];
      result.push({
        Slot: selected.Slot || "",
        SlotPhrase: selected.SlotPhrase || "",
        SlotText: selected.SlotText || "",
        Slot_display_order: selected.Slot_display_order || 0,
        PhraseType: selected.PhraseType || "",
        SubslotID: selected.SubslotID || "",
        SubslotElement: selected.SubslotElement || "",
        SubslotText: selected.SubslotText || "",
        display_order: selected.display_order || 0
      });
    }
  });

  return result;
}
