export function randomizeAll(slotData) {
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
    if (type === "O1") return;
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

  const o1Entries = groupSlots.filter(e => e.Slot === "O1");
  const uniqueOrders = [...new Set(o1Entries.map(e => e.Slot_display_order))];

  if (uniqueOrders.length > 1) {
    uniqueOrders.forEach(order => {
      const targets = o1Entries.filter(e => e.Slot_display_order === order);
      targets.forEach(t => selectedSlots.push({ ...t }));
    });
  } else if (o1Entries.length > 0) {
    const clauseO1 = o1Entries.filter(e => e.PhraseType === "clause");
    if (clauseO1.length > 0) {
      const chosen = clauseO1[Math.floor(Math.random() * clauseO1.length)];
      selectedSlots.push({ ...chosen });
      const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
      subslots.forEach(sub => selectedSlots.push({ ...sub }));
    } else {
      const wordO1 = o1Entries.filter(e => e.PhraseType !== "clause");
      if (wordO1.length > 0) {
        const chosen = wordO1[Math.floor(Math.random() * wordO1.length)];
        selectedSlots.push({ ...chosen });
        const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
        subslots.forEach(sub => selectedSlots.push({ ...sub }));
      }
    }
  }

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
 * 指定スロット（例：S）のみ個別ランダマイズする（親＋サブスロットセットごと）
 * @param {string} slotName - 例: "S"（大文字）
 */
function randomizeIndividualSlot(slotName) {
  // 1. 現在のv_group_keyを取得
  if (!window.lastSelectedSlots || window.lastSelectedSlots.length === 0) {
    alert("先に全体ランダマイズを実行してください");
    return;
  }
  // 例: S, M1 など
  const targetSlot = slotName.toUpperCase();
  // どのグループか
  const currentSlot = window.lastSelectedSlots.find(item => item.Slot === targetSlot && (!item.SubslotID || item.SubslotID === ""));
  if (!currentSlot || !currentSlot.V_group_key) {
    alert("グループ情報が取得できません。全体ランダマイズをやり直してください。");
    return;
  }
  const vGroupKey = currentSlot.V_group_key;
  // 2. window.allDataから該当グループ・スロットの全例文セットを抽出
  const all = window.allData || [];
  // 例文IDごとに親＋サブスロットをまとめる
  const exampleIdSetMap = {};
  all.forEach(item => {
    if (item.V_group_key === vGroupKey && item.Slot === targetSlot) {
      const exid = item.例文ID;
      if (!exampleIdSetMap[exid]) exampleIdSetMap[exid] = [];
      exampleIdSetMap[exid].push(item);
    }
  });
  const exampleIds = Object.keys(exampleIdSetMap);
  if (exampleIds.length === 0) {
    alert("該当スロットの候補がありません");
    return;
  }
  // 3. ランダムに1セット選ぶ
  const randomId = exampleIds[Math.floor(Math.random() * exampleIds.length)];
  const selectedSet = exampleIdSetMap[randomId];
  // 4. window.lastSelectedSlotsから該当スロット（親＋サブ）を除去
  window.lastSelectedSlots = window.lastSelectedSlots.filter(item => item.Slot !== targetSlot);
  // 5. 新しいセットを追加
  window.lastSelectedSlots.push(...selectedSet);
  // 6. 必要ならDOM更新関数を呼ぶ（例: buildDynamicSlots, updateSlotContentsOnly など）
  if (window.buildDynamicSlots) {
    window.buildDynamicSlots(window.lastSelectedSlots);
<<<<<<< HEAD
=======
  // 🔧 強制的にUIを再構築（slotが反映されないケース対策）
  if (window.buildStructure && window.lastSelectedSlots) {
    buildStructure(window.lastSelectedSlots);
    if (window.syncDynamicToStatic) {
      syncDynamicToStatic();
    }
  }

>>>>>>> parent of 51da046 (Update randomizer_all.js)
  }
  // 7. 必要ならwindow.loadedJsonDataも同期
  if (window.loadedJsonData) {
    window.loadedJsonData = window.loadedJsonData.filter(item => item.Slot !== targetSlot);
    window.loadedJsonData.push(...selectedSet.map(slot => ({
      Slot: slot.Slot || "",
      SlotPhrase: slot.SlotPhrase || "",
      SlotText: slot.SlotText || "",
      Slot_display_order: slot.Slot_display_order || 0,
      PhraseType: slot.PhraseType || "",
      SubslotID: slot.SubslotID || "",
      SubslotElement: slot.SubslotElement || "",
      SubslotText: slot.SubslotText || "",
      display_order: slot.display_order || 0
    })));
  }
}

// グローバル公開
window.randomizeIndividualSlot = randomizeIndividualSlot;
