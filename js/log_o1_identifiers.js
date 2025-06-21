
export function logO1Identifiers(slotData) {
  const exampleIDs = [...new Set(slotData.map(entry => entry.例文ID).filter(id => id))];
  let o1Identifiers = [];

  exampleIDs.forEach((id, index) => {
    const setNumber = index + 1;
    const o1Entries = slotData.filter(entry => entry.例文ID === id && entry.Slot === "O1");
    const orders = [...new Set(o1Entries.map(e => e.Slot_display_order))];
    o1Entries.forEach(entry => {
      const orderIndex = orders.indexOf(entry.Slot_display_order) + 1;
      let identifier = "";
      if (orders.length > 1) {
        identifier = `${entry.Slot}-${setNumber}-${orderIndex}`;
      } else {
        identifier = `${entry.Slot}-${setNumber}`;
      }
      o1Identifiers.push({
        例文ID: id,
        識別番号: identifier,
        SlotPhrase: entry.SlotPhrase
      });
    });
  });

  console.log("📝 O1 識別番号付与確認結果", o1Identifiers);
  return o1Identifiers;
}
