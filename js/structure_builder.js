
function renderSlot(item) {
  console.log("renderSlot item:", item); 
  const slotDiv = document.createElement('div');
  slotDiv.className = 'slot';
  slotDiv.dataset.displayOrder = item.Slot_display_order;

  if (item.PhraseType === 'word' || item.PhraseType === 'clause' || item.PhraseType === 'phrase') {
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
  if (sub.SubslotID) {
    subDiv.id = `slot-${sub.Slot.toLowerCase()}-sub-${sub.SubslotID.toLowerCase()}`;
  }
  if (typeof sub.display_order !== 'undefined') {
    subDiv.dataset.displayOrder = sub.display_order;
  }


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
  console.log("buildStructure called with selectedSlots:", selectedSlots);
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

  // 🔍 分離疑問詞判定とDisplayAtTop付加
  const slotOrderMap = {};
  
  // 🔍 分離疑問詞構文の疑問詞表示（DisplayAtTop）を上位スロットに付与
  const questionWords = ["what", "where", "who", "when", "why", "how"];
  const displayTopMap = new Map();

  selectedSlots.forEach(entry => {
    if (
      entry.SubslotID &&
      entry.SubslotElement &&
      questionWords.includes(entry.SubslotElement.trim().toLowerCase())
    ) {
      const key = entry.Slot + "-" + entry.Slot_display_order;
      displayTopMap.set(key, entry.SubslotElement.trim());
    }
  });

  selectedSlots.forEach(entry => {
    if (!entry.SubslotID) {
      const key = entry.Slot + "-" + entry.Slot_display_order;
      if (displayTopMap.has(key)) {
        entry.DisplayAtTop = true;
        entry.DisplayText = displayTopMap.get(key);
        console.log("🔼 DisplayAtTop 自動付加:", entry.DisplayText, "(slot:", entry.Slot, ")");
      }
    }
  });


  selectedSlots.forEach(entry => {
    if (!entry.SubslotID && slotOrderMap[entry.Slot] && slotOrderMap[entry.Slot].size >= 2) {
      const minOrder = Math.min(...slotOrderMap[entry.Slot]);
      if (entry.Slot_display_order === minOrder && entry.Role === "c1") {
        entry.DisplayAtTop = true;
        entry.DisplayText = entry.Text;
        console.log("🔼 DisplayAtTop 付加:", entry.Text);
      }
    }
  });
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    console.log(`Processing upper slot: ${item.Slot} (PhraseType: ${item.PhraseType})`);

    if (item.PhraseType === 'word') {
      const slotDiv = renderSlot(item);
      dynamicArea.appendChild(slotDiv);
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

    
    // 🔽 DisplayAtTop が付加された上位スロットは動的記載エリアに出力しない
    if (item.DisplayAtTop === true) {
      console.log(`🚫 DisplayAtTop により ${item.Slot} の表示をスキップ`);
      return;
    }

  subslots.forEach(sub => {
      console.log(`Adding subslot to ${item.Slot}: ${sub.SubslotID} (display_order: ${sub.display_order})`);
      const subDiv = renderSubslot(sub);
      dynamicArea.appendChild(subDiv);
    // 差分追加: 安全なM1サブスロット書き込み
    if (sub.Slot === "M1") {
      const target = document.getElementById(`slot-m1-sub-${sub.SubslotID.toLowerCase()}`);
      if (target) {
        const phrase = target.querySelector(".slot-phrase");
        if (phrase) { phrase.textContent = sub.SubslotElement || ""; console.log(`✅ phrase書き込み: ${target.id}`); }
        const text = target.querySelector(".slot-text");
        if (text) { text.textContent = sub.SubslotText || ""; console.log(`✅ text書き込み: ${target.id}`); }
      } else {
        console.warn(`⚠ サブスロットが見つからない: slot-m1-sub-${sub.SubslotID.toLowerCase()}`);
      }
    }
    });
  });
  if (typeof bindSubslotToggleButtons === "function") bindSubslotToggleButtons();
}

export { buildStructure, buildStructure as buildStructureFromJson, renderSlot, renderSubslot };

window.buildStructure = buildStructure;
window.renderSlot = renderSlot;
window.renderSubslot = renderSubslot;
