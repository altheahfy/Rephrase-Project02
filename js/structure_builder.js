
export function buildStructureFromJson(jsonData) {
  const wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.warn('slot-wrapper not found');
    return;
  }
  wrapper.innerHTML = ''; // クリーン化

  // ExampleID 単位でグループ化
  const examples = {};
  jsonData.forEach(item => {
    if (!examples[item.ExampleID]) {
      examples[item.ExampleID] = [];
    }
    examples[item.ExampleID].push(item);
  });

  // 仮に最初の ExampleID のデータだけ表示
  const exampleID = Object.keys(examples)[0];
  const slots = examples[exampleID];

  // 上位スロットの描画
  const upperSlots = slots.filter(e => !e.SubslotID);
  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    const slotDiv = document.createElement('div');
    slotDiv.className = 'slot';

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

    const subslots = slots.filter(s => s.Slot === item.Slot && s.SubslotID);
    subslots.sort((a, b) => a.display_order - b.display_order);

    subslots.forEach(sub => {
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
