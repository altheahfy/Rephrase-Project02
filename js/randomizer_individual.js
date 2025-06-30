/**
 * Sスロット個別ランダマイザー
 * randomizer_all.js と structure_builder.js を完全コピーしてSスロット専用に改造
 */

/**
 * randomizer_all.jsの完全コピー（Sスロット専用に改造）
 * exportを削除してグローバル関数にする
 */
function randomizeAll(slotData) {
  const groups = [...new Set(slotData.map(entry => entry.V_group_key).filter(v => v))];
  if (groups.length === 0) {
    console.warn("V_group_key 母集団が見つかりません。");
    return [];
  }

  const selectedGroup = groups[Math.floor(Math.random() * groups.length)];
  console.log(`🟢 選択 V_group_key: ${selectedGroup}`);

  const groupSlots = slotData.filter(entry => entry.V_group_key === selectedGroup);
  const exampleIDs = [...new Set(groupSlots.map(entry => entry.例文ID).filter(id => id))];

  if (exampleIDs.length === 0) {
    console.warn("例文ID 母集団が見つかりません。");
    return [];
  }

  let slotSets = [];
  exampleIDs.forEach((id, index) => {
    const setNumber = index + 1;
    const slots = groupSlots.filter(entry => entry.例文ID === id && !entry.SubslotID).map(entry => ({
      ...entry,
      識別番号: `${entry.Slot}-${setNumber}`
    }));
    slotSets.push(slots);
  });

  let selectedSlots = [];
  const slotTypes = [...new Set(groupSlots.map(entry => entry.Slot).filter(s => s))];
  slotTypes.forEach(type => {
    // Sスロット個別ランダマイズ：Sスロットのみを対象とする
    if (type !== "S") return;
    
    const candidates = slotSets.flat().filter(entry => entry.Slot === type);
    if (candidates.length > 0) {
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      selectedSlots.push({ ...chosen });
      const relatedSubslots = groupSlots.filter(e =>
        e.例文ID === chosen.例文ID &&
        e.Slot === chosen.Slot &&
        e.SubslotID
      );
      relatedSubslots.forEach(sub => {
        selectedSlots.push({ ...sub });
      });
    }
  });

  // Sスロット個別ランダマイズ：O1処理は不要

  window.slotSets = slotSets;
  window.slotTypes = slotTypes;
  window.lastSelectedSlots = selectedSlots;

  return selectedSlots.map(slot => ({
    Slot: slot.Slot || "",
    SlotPhrase: slot.SlotPhrase || "",
    SlotText: slot.SlotText || "",
    Slot_display_order: slot.Slot_display_order || 0,
    PhraseType: slot.PhraseType || "",
    SubslotID: slot.SubslotID || "",
    SubslotElement: slot.SubslotElement || "",
    SubslotText: slot.SubslotText || "",
    display_order: slot.display_order || 0,
    識別番号: slot.識別番号 || ""
  }));
}

/**
 * structure_builder.jsの完全コピー（Sスロット専用に改造）
 */
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

/**
 * Sスロット個別ランダマイズ（HTMLと同じ呼び出し方式）
 */
function randomizeSlotSIndividual() {
  console.log("🎲🎯 Sスロット個別ランダマイズ開始（完全コピペ版）");
  
  // 既存のlastSelectedSlotsが必要
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  if (!window.loadedJsonData || !Array.isArray(window.loadedJsonData)) {
    console.warn("⚠️ window.loadedJsonDataが見つかりません。先にJSONを読み込んでください。");
    return;
  }
  
  // 現在のV_group_keyを取得
  const firstSlot = window.lastSelectedSlots[0];
  const selectedGroup = firstSlot.V_group_key;
  console.log(`🔑 現在のV_group_key: ${selectedGroup}`);
  
  // そのグループからSスロット候補を取得
  const groupSlots = window.loadedJsonData.filter(entry => entry.V_group_key === selectedGroup);
  const sCandidates = groupSlots.filter(entry => entry.Slot === "S" && !entry.SubslotID);
  
  if (sCandidates.length === 0) {
    console.warn("⚠️ Sスロット候補が見つかりません");
    return;
  }
  
  // Sスロットをランダム選択
  const chosenS = sCandidates[Math.floor(Math.random() * sCandidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosenS);
  
  // 既存のlastSelectedSlotsからSスロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
  
  // 新しいSスロットを追加
  filteredSlots.push({ ...chosenS });
  
  // 関連サブスロットを追加
  const relatedSubslots = groupSlots.filter(e =>
    e.例文ID === chosenS.例文ID &&
    e.Slot === chosenS.Slot &&
    e.SubslotID
  );
  relatedSubslots.forEach(sub => {
    filteredSlots.push({ ...sub });
  });
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  const data = filteredSlots.map(slot => ({
    Slot: slot.Slot || "",
    SlotPhrase: slot.SlotPhrase || "",
    SlotText: slot.SlotText || "",
    Slot_display_order: slot.Slot_display_order || 0,
    PhraseType: slot.PhraseType || "",
    SubslotID: slot.SubslotID || "",
    SubslotElement: slot.SubslotElement || "",
    SubslotText: slot.SubslotText || "",
    display_order: slot.display_order || 0,
    識別番号: slot.識別番号 || ""
  }));
  
  console.log("ランダマイズ結果詳細（Sスロット個別）:", JSON.stringify(data, null, 2));
  buildStructure(data);
  
  if (typeof syncDynamicToStatic === "function") {
    syncDynamicToStatic();
    console.log("🔄 静的エリアとの同期完了");
  }
  
  console.log("✅ Sスロット個別ランダマイズ完了（完全コピペ版）");
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;