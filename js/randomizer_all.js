
/**
 * V_group_key 母集団から1つ選び、そのスロット群を返す。
 * structure_builder.js に渡すデータを生成。
 * @param {Array} slotData - slot_order_data.json のデータ配列
 * @returns {Array} 選択されたスロット群（上位スロット＋サブスロット含む）のデータ配列
 */
export function randomizeAll(slotData) {
  // V_group_key 母集団を列挙
  const groups = [...new Set(slotData.map(entry => entry.V_group_key).filter(v => v))];
  if (groups.length === 0) {
    console.warn("V_group_key 母集団が見つかりません。");
    return [];
  }

  // ランダムに V_group_key を選択
  const selectedGroup = groups[Math.floor(Math.random() * groups.length)];
  console.log(`🟢 選択 V_group_key: ${selectedGroup}`);

  // 選択グループのスロット群を収集
  const selectedSlots = slotData.filter(entry => entry.V_group_key === selectedGroup);

  // 上位スロット・サブスロットをまとめて返す
  // structure_builder が直接利用できる形式（配列）で出力
  return selectedSlots.map(slot => ({
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
