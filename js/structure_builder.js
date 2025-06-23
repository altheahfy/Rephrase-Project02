
function validateData(selectedSlots) {
  selectedSlots.forEach(item => {
    // Check for missing required fields in the slot data
    if (!item.Slot) {
      console.warn(`Missing required field: Slot for item`, item);
    }
    if (!item.SlotPhrase) {
      console.warn(`Missing required field: SlotPhrase for item`, item);
    }
    if (!item.SlotText) {
      console.warn(`Missing required field: SlotText for item`, item);
    }
    if (!item.SubslotID && item.PhraseType !== 'word') {
      console.warn(`Missing required field: SubslotID for non-word type item`, item);
    }
  });
}

function renderSlot(item) {
  // Ensure data validity before rendering
  if (!item.SlotPhrase || !item.SlotText) {
    return null;  // Skip rendering this slot if data is incomplete
  }

  const slotDiv = document.createElement('div');
  slotDiv.className = 'slot';
  slotDiv.dataset.displayOrder = item.Slot_display_order;

  const phraseDiv = document.createElement('div');
  phraseDiv.className = 'slot-phrase';
  phraseDiv.innerText = item.SlotPhrase || '';

  const textDiv = document.createElement('div');
  textDiv.className = 'slot-text';
  textDiv.innerText = item.SlotText || '';

  slotDiv.appendChild(phraseDiv);
  slotDiv.appendChild(textDiv);

  return slotDiv;
}

function renderSubslot(sub) {
  // Ensure data validity before rendering subslots
  if (!sub.SubslotElement || !sub.SubslotText) {
    return null;  // Skip rendering this subslot if data is incomplete
  }

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

  // Validate the data
  validateData(selectedSlots);

  const fragment = document.createDocumentFragment();

  // Only render 'word' type slots as upper slots
  const upperSlots = selectedSlots.filter(e => !e.SubslotID && e.PhraseType === 'word');
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    const slotDiv = renderSlot(item);
    if (slotDiv) {  // Only append if it's a valid 'word' slot
      fragment.appendChild(slotDiv);

      const subslots = selectedSlots.filter(s =>
        s.Slot === item.Slot &&
        s.SubslotID &&
        s.Slot_display_order === item.Slot_display_order
      );
      subslots.sort((a, b) => a.display_order - b.display_order);

      subslots.forEach(sub => {
        const subDiv = renderSubslot(sub);
        if (subDiv) {  // Only append valid subslots
          slotDiv.appendChild(subDiv);
        }
      });
    }
  });

  // Append the new content
  wrapper.appendChild(fragment);
}

export { buildStructure, buildStructure as buildStructureFromJson };
