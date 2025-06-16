
export function buildStructureFromJson(jsonData) {
  // 上位スロット順制御
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
      slotWrapper.appendChild(el);
    }
  });

  // サブスロット順制御（例：O1 展開中のものを想定）
  const subWrapper = document.getElementById('slot-o1-sub');
  if (subWrapper) {
    const subSlots = jsonData.filter(e => e.SubslotID);
    subSlots.sort((a, b) => a.display_order - b.display_order);

    subSlots.forEach(item => {
      const subId = `slot-o1-sub-${item.Slot.toLowerCase()}`;
      const el = document.getElementById(subId);
      if (el) {
        const textDiv = el.querySelector('.slot-text');
        if (textDiv) {
          textDiv.innerText = `${item.SubslotElement || ''} ${item.SubslotText || ''}`.trim();
        }
        subWrapper.appendChild(el);
      }
    });
  }
}
