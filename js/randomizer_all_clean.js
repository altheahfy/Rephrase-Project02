// main.js - ランダマイズ機能統合版

function randomizeAll() {
  console.log('🔥 全体ランダマイズ開始');
  
  if (!window.allData || !Array.isArray(window.allData)) {
    console.error('allDataが見つかりません');
    return;
  }

  const groupedByKey = window.allData.reduce((acc, item) => {
    if (!acc[item.V_group_key]) {
      acc[item.V_group_key] = [];
    }
    acc[item.V_group_key].push(item);
    return acc;
  }, {});

  console.log('グループ化完了:', Object.keys(groupedByKey).length, 'グループ');

  const allGroupKeys = Object.keys(groupedByKey);
  if (allGroupKeys.length === 0) {
    console.error('有効なグループが見つかりません');
    return;
  }

  const randomKey = allGroupKeys[Math.floor(Math.random() * allGroupKeys.length)];
  console.log('選択されたグループ:', randomKey);

  const selectedSlots = groupedByKey[randomKey];
  console.log('選択されたスロット数:', selectedSlots.length);

  window.lastSelectedSlots = selectedSlots;

  window.loadedJsonData = selectedSlots.map(slot => ({
    "識別番号": slot["識別番号"] || "",
    V_group_key: slot.V_group_key || "",
    Slot: slot.Slot || "",
    PhraseType: slot.PhraseType || "",
    SlotPhrase: slot.SlotPhrase || "",
    SlotText: slot.SlotText || "",
    Slot_display_order: slot.Slot_display_order || 0,
    SubslotID: slot.SubslotID || "",
    SubslotElement: slot.SubslotElement || "",
    SubslotText: slot.SubslotText || "",
    display_order: slot.display_order || 0
  }));

  console.log('loadedJsonData更新完了:', window.loadedJsonData.length, '件');

  if (window.buildDynamicSlots && window.safeJsonSync) {
    window.buildDynamicSlots(selectedSlots);
    window.safeJsonSync(window.loadedJsonData);
    console.log('✅ 全体ランダマイズ完了');
  } else {
    console.error('❌ 必要な関数が見つかりません (buildDynamicSlots/safeJsonSync)');
  }
}

// 個別ランダマイズ専用の軽量描画更新関数
function updateSlotContentsOnly(slotId, selectedSlots) {
  console.log(`🎯 軽量描画更新開始: ${slotId}`);
  
  if (!selectedSlots || selectedSlots.length === 0) {
    console.warn("selectedSlotsが空です");
    return;
  }
  
  // slotIdから対象スロットを特定
  const targetSlot = slotId.replace('slot-', '').toUpperCase();
  
  // 該当スロットのデータのみを抽出
  const relevantSlots = selectedSlots.filter(slot => 
    slot.Slot === targetSlot
  );
  
  if (relevantSlots.length === 0) {
    console.warn(`${targetSlot}に該当するスロットデータが見つかりません`);
    return;
  }
  
  console.log(`🎯 更新対象スロット: ${targetSlot}, 件数: ${relevantSlots.length}`);
  
  // 静的DOMの該当スロットコンテナを更新
  relevantSlots.forEach(slot => {
    let targetElement = null;
    
    if (slot.SubslotID) {
      // サブスロットの場合
      targetElement = document.getElementById(`slot-${slot.Slot.toLowerCase()}-sub-${slot.SubslotID.toLowerCase()}`);
    } else {
      // 上位スロットの場合
      targetElement = document.getElementById(`slot-${slot.Slot.toLowerCase()}`);
    }
    
    if (targetElement) {
      // slot-phraseを更新
      const phraseDiv = targetElement.querySelector('.slot-phrase');
      if (phraseDiv) {
        if (slot.SubslotID) {
          phraseDiv.textContent = slot.SubslotElement || '';
        } else {
          phraseDiv.textContent = slot.SlotPhrase || '';
        }
      }
      
      // slot-textを更新
      const textDiv = targetElement.querySelector('.slot-text');
      if (textDiv) {
        if (slot.SubslotID) {
          textDiv.textContent = slot.SubslotText || '';
        } else {
          textDiv.textContent = slot.SlotText || '';
        }
      }
      
      console.log(`✅ 更新完了: ${targetElement.id}`);
    } else {
      console.warn(`⚠ DOM要素が見つかりません: ${slot.Slot}${slot.SubslotID ? `-sub-${slot.SubslotID}` : ''}`);
    }
  });
  
  console.log(`🎯 軽量描画更新完了: ${slotId}`);
}

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
  const groupedByExampleId = candidateData.reduce((acc, item) => {
    const exampleId = item["識別番号"] || "unknown";
    if (!acc[exampleId]) {
      acc[exampleId] = [];
    }
    acc[exampleId].push(item);
    return acc;
  }, {});
  
  console.log(`📋 例文ID別グループ数: ${Object.keys(groupedByExampleId).length}`);
  
  // 6. ランダムに1つの例文IDを選択
  const exampleIds = Object.keys(groupedByExampleId);
  const randomExampleId = exampleIds[Math.floor(Math.random() * exampleIds.length)];
  const selectedGroup = groupedByExampleId[randomExampleId];
  
  console.log(`🎲 選択された例文ID: ${randomExampleId}, スロット数: ${selectedGroup.length}`);
  
  // 7. window.lastSelectedSlotsから対象スロットのデータを除去
  window.lastSelectedSlots = window.lastSelectedSlots.filter(item => 
    !(item.Slot && item.Slot.toUpperCase() === targetSlot)
  );
  
  // 8. 新しく選択されたデータを追加
  window.lastSelectedSlots.push(...selectedGroup);
  console.log(`🔄 lastSelectedSlots更新完了: ${window.lastSelectedSlots.length}件`);
  
  // window.loadedJsonDataも同様に更新
  if (window.loadedJsonData) {
    // 対象スロットを除去
    window.loadedJsonData = window.loadedJsonData.filter(item => 
      !(item.Slot && item.Slot.toUpperCase() === targetSlot)
    );
    
    // 新しいデータを追加
    const formattedData = selectedGroup.map(slot => ({
      "識別番号": slot["識別番号"] || "",
      V_group_key: slot.V_group_key || "",
      Slot: slot.Slot || "",
      PhraseType: slot.PhraseType || "",
      SlotPhrase: slot.SlotPhrase || "",
      SlotText: slot.SlotText || "",
      Slot_display_order: slot.Slot_display_order || 0,
      SubslotID: slot.SubslotID || "",
      SubslotElement: slot.SubslotElement || "",
      SubslotText: slot.SubslotText || "",
      display_order: slot.display_order || 0
    }));
    
    window.loadedJsonData.push(...formattedData);
    console.log(`🔄 window.loadedJsonData更新完了`);
  }
  
  // 9. 軽量描画更新（buildDynamicSlotsの代わりに使用）
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
window.randomizeAll = randomizeAll;
window.randomizeIndividual = randomizeIndividual;
window.updateSlotContentsOnly = updateSlotContentsOnly;
