
export function buildStructureFromJson(jsonData) {
  const slotWrapper = document.querySelector('.slot-wrapper');
  if (!slotWrapper) {
    console.warn("slot-wrapper not found");
    return;
  }

  const upperSlots = jsonData.filter(e => !e.SubslotID);
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    const slotId = `slot-${item.Slot.toLowerCase()}`;
    const el = document.getElementById(slotId);
    if (el) {
      const textDiv = el.querySelector('.slot-text');
      if (textDiv) {
        textDiv.innerText = `${item.SubslotElement || ''} ${item.SlotText || ''}`.trim();
      }
    }
  });

  const subSlots = jsonData.filter(e => e.SubslotID);
  subSlots.sort((a, b) => a.display_order - b.display_order);

  subSlots.forEach(item => {
    const subWrapperId = `slot-${item.Slot.toLowerCase()}-sub`;
    const subWrapper = document.getElementById(subWrapperId);
    if (subWrapper) {
      subWrapper.style.display = 'flex'; // サブスロット表示切り替え
    
      const subId = `${subWrapperId}-${item.SubslotID.toLowerCase()}`;
      const el = document.getElementById(subId);
      if (el) {
        const textDiv = el.querySelector('.slot-text');
        if (textDiv) {
          textDiv.innerText = `${item.SubslotElement || ''} ${item.SubslotText || ''}`.trim();
        }
      }
    }
  });
}
