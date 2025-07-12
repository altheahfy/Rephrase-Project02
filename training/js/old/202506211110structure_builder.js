
function buildStructure(selectedSlots) {
  const wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.warn('slot-wrapper not found');
    return;
  }
  wrapper.innerHTML = '';

  console.log('📝 buildStructure received selectedSlots:', selectedSlots);

  // 上位スロットを display_order 順に厳密ソート
  const upperSlots = selectedSlots.filter(e => !e.SubslotID);
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);
  console.log('📝 upperSlots after sort:', upperSlots);

  upperSlots.forEach(item => {
    console.log(`📝 Rendering upperSlot: ${item.Slot}, SlotPhrase: ${item.SlotPhrase}, Slot_display_order: ${item.Slot_display_order}`);

    const slotDiv = document.createElement('div');
    slotDiv.className = 'slot';
    slotDiv.dataset.displayOrder = item.Slot_display_order;

    if (item.PhraseType === 'word') {
      const phraseDiv = document.createElement('div');
      phraseDiv.className = 'slot-phrase';
      phraseDiv.innerText = item.SlotPhrase || '';

      const textDiv = document.createElement('div');
      textDiv.className = 'slot-text';
      textDiv.innerText = item.SlotText || '';

      slotDiv.appendChild(phraseDiv);
      slotDiv.appendChild(textDiv);
    } else {
      const markDiv = document.createElement('div');
      markDiv.className = 'slot-mark';
      markDiv.innerText = '▶';
      slotDiv.appendChild(markDiv);
    }

    wrapper.appendChild(slotDiv);

    // サブスロットは Slot + SlotPhrase + Slot_display_order に基づき付随
    const subslots = selectedSlots.filter(s =>
      s.Slot === item.Slot &&
      s.SubslotID &&
      s.SlotPhrase === item.SlotPhrase &&
      s.Slot_display_order === item.Slot_display_order
    );
    subslots.sort((a, b) => a.display_order - b.display_order);
    console.log(`📝 Subslots for ${item.Slot} (${item.SlotPhrase}):`, subslots);

    subslots.forEach(sub => {
      console.log(`📝 Rendering subSlot: ${sub.SubslotID}, SubslotElement: ${sub.SubslotElement}`);

      const subDiv = document.createElement('div');
      subDiv.className = 'subslot';

      const subElDiv = document.createElement('div');
      subElDiv.className = 'subslot-element';
      subElDiv.innerText = sub.SubslotElement || '';

      const subTextDiv = document.createElement('div');
      subTextDiv.className = 'subslot-text';
      subTextDiv.innerText = sub.SubslotText || '';

      subDiv.appendChild(subElDiv);
      subDiv.appendChild(subTextDiv);

      slotDiv.appendChild(subDiv);
    });
  });
}

export { buildStructure, buildStructure as buildStructureFromJson };
