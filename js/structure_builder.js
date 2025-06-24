
function renderSlot(item) {
  console.log("renderSlot item:", item); 
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
    if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

  return slotDiv;
  if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

function renderSubslot(sub) {
  console.log("renderSubslot sub:", sub);
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
  if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

function buildStructure(selectedSlots) {
  let wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.error('slot-wrapper not found, skipping structure generation');
    return;
    if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

  let dynamicArea = document.getElementById('dynamic-slot-area');
  if (!dynamicArea) {
    dynamicArea = document.createElement('div');
    dynamicArea.id = 'dynamic-slot-area';
    wrapper.appendChild(dynamicArea);
    if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

  dynamicArea.innerHTML = '';

  console.log("buildStructure called with selectedSlots:", selectedSlots);

  // 上位スロットのリセット
  const slotContainers = wrapper.querySelectorAll('.slot-container');
  slotContainers.forEach(container => {
    const phraseDiv = container.querySelector('.slot-phrase');
    if (phraseDiv) phraseDiv.innerText = '';
    const textDiv = container.querySelector('.slot-text');
    if (textDiv) textDiv.innerText = '';
  });

  const upperSlots = selectedSlots.filter(e => !e.SubslotID);
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    console.log(`Processing upper slot: ${item.Slot} (PhraseType: ${item.PhraseType})`);

    if (item.PhraseType === 'word') {
      const slotDiv = renderSlot(item);
      dynamicArea.appendChild(slotDiv);

      if (item.Slot === "M1") {
        const m1Container = document.getElementById("slot-m1");
        if (m1Container) {
          const phraseDiv = m1Container.querySelector(".slot-phrase");
          if (phraseDiv) phraseDiv.innerText = item.SlotPhrase || '';

          const textDiv = m1Container.querySelector(".slot-text");
          if (textDiv) textDiv.innerText = item.SlotText || '';
          if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}
        if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}
    } else {
      console.log(`Skipped upper slot: ${item.Slot} (PhraseType: ${item.PhraseType})`);
      if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

    const subslots = selectedSlots.filter(s =>
      s.Slot === item.Slot &&
      s.SubslotID &&
      s.Slot_display_order === item.Slot_display_order
    );
    subslots.sort((a, b) => a.display_order - b.display_order);

    subslots.forEach(sub => {
      console.log(`Adding subslot to ${item.Slot}: ${sub.SubslotID} (display_order: ${sub.display_order})`);
      const subDiv = renderSubslot(sub);
      dynamicArea.appendChild(subDiv);
    });
  });
  if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

export { buildStructure, buildStructure as buildStructureFromJson };
