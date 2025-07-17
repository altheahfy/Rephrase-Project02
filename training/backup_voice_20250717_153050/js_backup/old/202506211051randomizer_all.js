
/**
 * V_group_key 母集団から1つ選び、例文ID単位で母集団を形成し、1例文を選択。
 * structure_builder.js に渡すデータを生成。
 * @param {Array} slotData - slot_order_data.json のデータ配列
 * @returns {Array} 選択されたスロット群
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
  const exampleIDs = [...new Set(groupSlots.map(entry => entry.例文ID).filter(id => id))];

  if (exampleIDs.length === 0) {
    console.warn("例文ID 母集団が見つかりません。");
    return [];
  }

  const selectedExampleID = exampleIDs[Math.floor(Math.random() * exampleIDs.length)];
  console.log(`🟢 選択 例文ID: ${selectedExampleID}`);

  const selectedSlots = groupSlots.filter(entry => entry.例文ID === selectedExampleID);

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
    display_order: slot.display_order || 0
  }));
}
