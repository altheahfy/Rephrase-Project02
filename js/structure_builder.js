
function renderSlot(item) {
  // Log the rendering of each slot
  console.log('Rendering slot:', item);

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
  // Log the rendering of each subslot
  console.log('Rendering subslot:', sub);

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

  const fragment = document.createDocumentFragment();

  // Only render 'word' type slots as upper slots
  const upperSlots = selectedSlots.filter(e => !e.SubslotID && e.PhraseType === 'word');
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    const slotDiv = renderSlot(item);
    if (slotDiv) {  // Only append if it's a valid 'word' slot
      fragment.appendChild(slotDiv);

      const subslots = selectedSlots.filter(s => s.Slot === item.Slot && s.SubslotID);
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
