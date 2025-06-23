
function renderSlot(item) {
  const slotDiv = document.createElement('div');
  slotDiv.className = 'slot';
  slotDiv.dataset.displayOrder = item.Slot_display_order;

  // Only add word-type Slot data
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
    // For other types (e.g. clause), show a placeholder or mark
    const markDiv = document.createElement('div');
    markDiv.className = 'slot-mark';
    markDiv.innerText = '▶';
    slotDiv.appendChild(markDiv);
  }

  return slotDiv;
}

function renderSubslot(sub) {
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

  return subDiv;
}

function buildStructure(selectedSlots) {
  const wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.error('slot-wrapper not found, skipping structure generation');
    return;
  }

  // Clear the previous content before adding new content
  wrapper.innerHTML = '';

  const upperSlots = selectedSlots.filter(e => !e.SubslotID);
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    const slotDiv = renderSlot(item);
    wrapper.appendChild(slotDiv);

    const subslots = selectedSlots.filter(s =>
      s.Slot === item.Slot &&
      s.SubslotID &&
      s.Slot_display_order === item.Slot_display_order
    );
    subslots.sort((a, b) => a.display_order - b.display_order);

    subslots.forEach(sub => {
      const subDiv = renderSubslot(sub);
      slotDiv.appendChild(subDiv);
    });
  });
}

export { buildStructure, buildStructure as buildStructureFromJson };
