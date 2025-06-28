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

// ===========================================
// 個別ランダマイズ専用の軽量描画更新関数
// ===========================================

/**
 * 指定されたスロットのDOM内容のみを更新（ボタンやイベントハンドラを保持）
 * @param {string} slotId - 対象スロットのID（例: "slot-s", "slot-m1"）
 * @param {Array} selectedSlots - 更新するスロットデータ
 */
function updateSlotContentsOnly(slotId, selectedSlots) {
  console.log(`🎯 軽量描画更新開始: ${slotId}`);
  
  if (!selectedSlots || selectedSlots.length === 0) {
    console.warn("selectedSlotsが空です");
    return;
  }
  
  // slotIdから対象スロットを特定（slot-s → S）
  const targetSlot = slotId.replace('slot-', '').toUpperCase();
  
  // 上位スロットとサブスロットで明確に分岐して更新
  // 1. 上位スロット（SubslotIDなし）
  const parentSlot = selectedSlots.find(slot => slot.Slot === targetSlot && (!slot.SubslotID || slot.SubslotID === ""));
  if (parentSlot) {
    const parentElement = document.getElementById(`slot-${targetSlot.toLowerCase()}`);
    if (parentElement) {
      // slot-phrase
      const phraseDiv = parentElement.querySelector('.slot-phrase');
      if (phraseDiv) phraseDiv.textContent = parentSlot.SlotPhrase || '';
      // slot-text
      const textDiv = parentElement.querySelector('.slot-text');
      if (textDiv) textDiv.textContent = parentSlot.SlotText || '';
      // subslot-toggle-buttonの表示リセット
      const toggleBtn = parentElement.querySelector('.subslot-toggle-button');
      if (toggleBtn) toggleBtn.style.display = '';
      console.log(`✅ 上位スロット更新完了: ${parentElement.id}`);
    } else {
      console.warn(`⚠ DOM要素が見つかりません: ${targetSlot}`);
    }
  }

  // 2. サブスロット（SubslotIDあり）
  const subslots = selectedSlots.filter(slot => slot.Slot === targetSlot && slot.SubslotID && slot.SubslotID !== "");
  subslots.forEach(slot => {
    const subElement = document.getElementById(`slot-${slot.Slot.toLowerCase()}-sub-${slot.SubslotID.toLowerCase()}`);
    if (subElement) {
      // slot-phrase
      const phraseDiv = subElement.querySelector('.slot-phrase');
      if (phraseDiv) phraseDiv.textContent = slot.SubslotElement || '';
      // slot-text
      const textDiv = subElement.querySelector('.slot-text');
      if (textDiv) textDiv.textContent = slot.SubslotText || '';
      console.log(`✅ サブスロット更新完了: ${subElement.id}`);
    } else {
      console.warn(`⚠ サブスロットDOM要素が見つかりません: ${slot.Slot}-sub-${slot.SubslotID}`);
    }
  });

  console.log(`🎯 軽量描画更新完了: ${slotId}`);
}

// ===========================================
// 個別ランダマイズ機能
// ===========================================

/**
 * 指定されたスロットのみを個別にランダマイズする
 * @param {string} slotId - 対象スロットのID（例: "slot-s", "slot-m1"）
 */
function randomizeIndividual(slotId) {
  console.log(`🎯 個別ランダマイズ開始: ${slotId}`);
  
  // 1. 現在選択されているスロットデータを確認
  if (!window.lastSelectedSlots || window.lastSelectedSlots.length === 0) {
    console.error("❌ 先に全体ランダマイズを実行してください");
    alert("先に全体ランダマイズを実行してください");
    return;
  }
  
  // 2. 対象スロット名を抽出（slot-s → S）
  const targetSlot = slotId.replace('slot-', '').toUpperCase();
  console.log(`🎯 対象スロット: ${targetSlot}`);
  
  // 3. 現在の選択から対象スロットのV_group_keyを取得
  const currentSlotData = window.lastSelectedSlots.find(item => 
    item.Slot && item.Slot.toUpperCase() === targetSlot && 
    (!item.SubslotID || item.SubslotID === "")
  );
  
  if (!currentSlotData) {
    console.error(`❌ 対象スロットが見つかりません: ${targetSlot}`);
    return;
  }
  
  // V_group_keyを取得（window.lastSelectedSlotsから）
  const currentGroupKey = currentSlotData.V_group_key;
  if (!currentGroupKey) {
    console.error("❌ V_group_keyが見つかりません");
    return;
  }
  
  console.log(`📊 現在のグループ: ${currentGroupKey}`);
  console.log(`🔍 対象スロット情報:`, currentSlotData);
  
  // 4. window.allDataまたはwindow.slotSetsから候補データを取得
  let candidateData = [];
  
  if (window.allData) {
    // window.allDataが利用可能な場合
    if (currentSlotData.PhraseType === "word") {
      // 単体選択：該当スロットのみ
      candidateData = window.allData.filter(item => 
        item.V_group_key === currentGroupKey &&
        item.Slot && item.Slot.toUpperCase() === targetSlot &&
        (!item.SubslotID || item.SubslotID === "")
      );
      console.log(`📝 単体選択モード: ${candidateData.length}件の候補`);
    } else {
      // セット選択：親 + 全サブスロット
      candidateData = window.allData.filter(item => 
        item.V_group_key === currentGroupKey &&
        item.Slot && item.Slot.toUpperCase() === targetSlot
      );
      console.log(`📦 セット選択モード: ${candidateData.length}件の候補（親+サブスロット含む）`);
    }
  } else if (window.slotSets) {
    // window.slotSetsから候補を取得
    const allSlotsInSets = window.slotSets.flat();
    candidateData = allSlotsInSets.filter(item => 
      item.Slot && item.Slot.toUpperCase() === targetSlot
    );
    console.log(`📦 slotSetsから選択: ${candidateData.length}件の候補`);
  }
  
  if (candidateData.length === 0) {
    console.warn(`⚠ 候補データが見つかりません: ${targetSlot}`);
    return;
  }
  
  // 5. 候補データを例文ID（識別番号）でグループ化
  const candidatesByExample = {};
  candidateData.forEach(item => {
    const exampleId = item.例文ID || item.識別番号;
    if (!candidatesByExample[exampleId]) {
      candidatesByExample[exampleId] = [];
    }
    candidatesByExample[exampleId].push(item);
  });
  
  const exampleIds = Object.keys(candidatesByExample);
  console.log(`🎲 選択可能な例文: ${exampleIds.join(', ')}`);
  
  if (exampleIds.length === 0) {
    console.warn(`⚠ 選択可能な例文がありません`);
    return;
  }
  
  // 6. ランダムに例文を選択
  const randomExampleId = exampleIds[Math.floor(Math.random() * exampleIds.length)];
  const selectedData = candidatesByExample[randomExampleId];
  
  console.log(`✅ 選択された例文: ${randomExampleId}`);
  console.log(`📋 選択データ:`, selectedData);
  
  // 7. window.lastSelectedSlotsを更新（該当スロットのみ）
  // 既存の該当スロットデータを除去
  window.lastSelectedSlots = window.lastSelectedSlots.filter(item => 
    !item.Slot || item.Slot.toUpperCase() !== targetSlot
  );
  
  // 新しく選択されたデータを追加
  window.lastSelectedSlots.push(...selectedData);
  
  console.log(`🔄 window.lastSelectedSlots更新完了`);
  
  // 8. window.loadedJsonDataも更新（静的DOM同期用）
  if (window.loadedJsonData) {
    // 既存の該当スロットデータを除去
    window.loadedJsonData = window.loadedJsonData.filter(item => 
      !item.Slot || item.Slot.toUpperCase() !== targetSlot
    );
    
    // 新しく選択されたデータを適切な形式で追加
    const formattedData = selectedData.map(slot => ({
      Slot: slot.Slot || "",
      SlotPhrase: slot.SlotPhrase || "",
      SlotText: slot.SlotText || "",
      Slot_display_order: slot.Slot_display_order || 0,
      PhraseType: slot.PhraseType || "",
      SubslotID: slot.SubslotID || "",
      SubslotElement: slot.SubslotElement || "",
      SubslotText: slot.SubslotText || "",
      display_order: slot.display_order || 0
    }));
    
    window.loadedJsonData.push(...formattedData);
    console.log(`🔄 window.loadedJsonData更新完了`);
  }
  
  // 9. 軽量描画更新（ボタンやイベントハンドラを保持）
  if (window.lastSelectedSlots) {
    try {
      updateSlotContentsOnly(slotId, window.lastSelectedSlots);
      console.log(`🏗 軽量描画更新完了`);
    } catch (error) {
      console.error(`❌ 軽量描画更新エラー:`, error);
      // フォールバック: エラー時のみbuildDynamicSlotsを使用
      if (window.buildDynamicSlots) {
        console.log("🔄 フォールバック: buildDynamicSlots使用");
        window.buildDynamicSlots(window.lastSelectedSlots);
      }
    }
  }
  
  // 10. 静的DOMを更新
  if (window.safeJsonSync && window.loadedJsonData) {
    try {
      window.safeJsonSync(window.loadedJsonData);
      console.log(`✅ 個別ランダマイズ完了: ${slotId}`);
    } catch (error) {
      console.error("❌ 静的DOM更新エラー:", error);
    }
  } else {
    console.warn("⚠ safeJsonSync関数またはloadedJsonDataが見つかりません");
  }
}

// グローバルに公開
window.randomizeIndividual = randomizeIndividual;
window.updateSlotContentsOnly = updateSlotContentsOnly;
