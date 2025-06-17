
/**
 * V_group_key 母集団から1つ選び、そのスロット群を返す。
 * structure_builder.js に渡すデータを生成。
 * @param {Array} slotData - slot_order_data.json のデータ配列
 * @returns {Object} 選択されたスロット群の slotId → text マップ
 */
export function randomizeAll(slotData) {
  // V_group_key 母集団を列挙
  const groups = [...new Set(slotData.map(entry => entry.V_group_key).filter(v => v))];
  if (groups.length === 0) {
    console.warn("V_group_key 母集団が見つかりません。");
    return {};
  }

  // ランダムに V_group_key を選択
  const selectedGroup = groups[Math.floor(Math.random() * groups.length)];

  // 選択グループのスロット群を収集
  const selectedSlots = slotData.filter(entry => entry.V_group_key === selectedGroup);

  // スロットID → SlotPhrase のマップを生成
  const result = {};
  for (const slot of selectedSlots) {
    if (slot.Slot && slot.SlotPhrase) {
      result[`slot-${slot.Slot.toLowerCase()}`] = slot.SlotPhrase;
    }
  }

  return result;
}
