
function validateData(selectedSlots) {
  selectedSlots.forEach(item => {
    if (!item.Slot || !item.SlotPhrase || !item.SlotText) {
      console.warn(`Missing required data for Slot: ${item.Slot}`);
    }
  });
}

function renderSlot(item, options = {}) {
  // Only render 'word' type slots as upper slots
  if (item.PhraseType !== 'word') {
    return null;  // Return nothing if it's not a 'word' type slot
  }

  const slotDiv = document.createElement('div');
  slotDiv.className = 'slot';
  slotDiv.dataset.displayOrder = item.Slot_display_order;

  if (options.className) {
    slotDiv.classList.add(options.className);  // Optional class addition
  }

  const phraseDiv = document.createElement('div');
  phraseDiv.className = 'slot-phrase';
  phraseDiv.innerText = item.SlotPhrase || '';

  if (options.textColor) {
    phraseDiv.style.color = options.textColor;  // Optional text color change
  }

  slotDiv.appendChild(phraseDiv);
  const textDiv = document.createElement('div');
  textDiv.className = 'slot-text';
  textDiv.innerText = item.SlotText || '';
  slotDiv.appendChild(textDiv);

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

function safeRender(callback) {
  try {
    callback();
  } catch (error) {
    console.error('Rendering error:', error);
    alert('表示中にエラーが発生しました。コンソールを確認してください。');
  }
}

function buildStructure(selectedSlots) {
  const wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.error('slot-wrapper not found, skipping structure generation');
    return;
  }

  // Clear previous content
  wrapper.innerHTML = '';

  // Validate the data
  validateData(selectedSlots);

  const fragment = document.createDocumentFragment();

  // Only filter and render 'word' type slots as upper slots
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
        slotDiv.appendChild(subDiv);
      });
    }
  });

  // Append the new content
  wrapper.appendChild(fragment);
}

export { buildStructure, buildStructure as buildStructureFromJson };
