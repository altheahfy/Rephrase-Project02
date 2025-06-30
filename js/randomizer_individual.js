/**
 * Sスロット個別ランダマイザー
 * randomizer_all.js と structure_builder.js を完全コピーしてSスロット専用に改造
 */

/**
 * Sスロット個別ランダマイズ（全体ランダマイザーの完全コピー版）
 */
function randomizeSlotSIndividual() {
  console.log("🎲🎯 Sスロット個別ランダマイズ開始（完全コピー版）");
  
  // 現在のwindow.lastSelectedSlotsから既存データを取得
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  // 現在のV_group_keyを取得
  const currentVGroupKey = getCurrentVGroupKey();
  if (!currentVGroupKey) {
    console.warn("⚠️ 現在のV_group_keyが特定できませんでした");
    return;
  }
  
  console.log(`🔑 現在のV_group_key: ${currentVGroupKey}`);
  
  // window.slotSetsから候補を取得（randomizer_all.jsと同じ）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません");
    return;
  }
  
  const allEntries = window.slotSets.flat();
  const groupSlots = allEntries.filter(entry => entry.V_group_key === currentVGroupKey);
  
  // Sスロットのメイン候補を抽出
  const sSlotCandidates = groupSlots.filter(entry => 
    entry.Slot === "S" && !entry.SubslotID
  );
  
  console.log(`📊 Sスロット候補: ${sSlotCandidates.length}個`, sSlotCandidates);
  
  if (sSlotCandidates.length === 0) {
    console.warn("⚠️ Sスロット候補が見つかりません");
    return;
  }
  
  // ランダムに1つ選択（randomizer_all.jsと同じ方法）
  const chosenSSlot = sSlotCandidates[Math.floor(Math.random() * sSlotCandidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosenSSlot);
  
  // 関連サブスロットを取得（randomizer_all.jsと同じ方法）
  const relatedSubslots = groupSlots.filter(e =>
    e.例文ID === chosenSSlot.例文ID &&
    e.Slot === chosenSSlot.Slot &&
    e.SubslotID
  );
  
  console.log(`🎯 関連サブスロット: ${relatedSubslots.length}個`, relatedSubslots);
  
  // 🔍 デバッグ: 選択されたSスロットの詳細情報
  console.log("🔍 選択されたSスロットの詳細:");
  console.log("  - 例文ID:", chosenSSlot.例文ID);
  console.log("  - Slot:", chosenSSlot.Slot);
  console.log("  - PhraseType:", chosenSSlot.PhraseType);
  console.log("  - SlotPhrase:", chosenSSlot.SlotPhrase);
  
  // 🔍 デバッグ: 同じ例文IDを持つ全エントリをチェック
  const sameExampleEntries = groupSlots.filter(e => e.例文ID === chosenSSlot.例文ID);
  console.log(`🔍 同じ例文ID(${chosenSSlot.例文ID})を持つ全エントリ: ${sameExampleEntries.length}個`);
  sameExampleEntries.forEach((entry, index) => {
    console.log(`  [${index}] Slot: ${entry.Slot}, SubslotID: ${entry.SubslotID}, PhraseType: ${entry.PhraseType}`);
  });
  
  // 🔍 特別処理: PhraseType が clause の場合の対応
  if (chosenSSlot.PhraseType === 'clause' && relatedSubslots.length === 0) {
    console.log("⚠️ Sスロットが clause で関連サブスロットが見つからない場合の特別処理");
    
    // 他のSスロット候補でword型を探す
    const wordSSlotCandidates = sSlotCandidates.filter(entry => entry.PhraseType === 'word');
    if (wordSSlotCandidates.length > 0) {
      const wordChosenSSlot = wordSSlotCandidates[Math.floor(Math.random() * wordSSlotCandidates.length)];
      console.log("🔄 word型のSスロットに変更:", wordChosenSSlot);
      
      // 変数を更新
      chosenSSlot = wordChosenSSlot;
      
      // 関連サブスロットを再取得
      const newRelatedSubslots = groupSlots.filter(e =>
        e.例文ID === chosenSSlot.例文ID &&
        e.Slot === chosenSSlot.Slot &&
        e.SubslotID
      );
      console.log(`🔄 新しい関連サブスロット: ${newRelatedSubslots.length}個`, newRelatedSubslots);
      relatedSubslots.length = 0; // 配列をクリア
      relatedSubslots.push(...newRelatedSubslots); // 新しいサブスロットを追加
    }
  }
  
  // 新しいSスロットデータセットを作成
  const newSSlots = [chosenSSlot, ...relatedSubslots].map(slot => ({
    Slot: slot.Slot || "",
    SlotPhrase: slot.SlotPhrase || "",
    SlotText: slot.SlotText || "",
    Slot_display_order: slot.Slot_display_order || 0,
    PhraseType: slot.PhraseType || "",
    SubslotID: slot.SubslotID || "",
    SubslotElement: slot.SubslotElement || "",
    SubslotText: slot.SubslotText || "",
    display_order: slot.display_order || 0,
    識別番号: slot.識別番号 || "",
    V_group_key: slot.V_group_key || "",
    例文ID: slot.例文ID || ""
  }));
  
  console.log(`🔄 新しいSスロットデータセット:`, newSSlots);
  
  // 既存のwindow.lastSelectedSlotsからSスロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
  
  // 新しいSスロットデータを追加
  const updatedSlots = [...filteredSlots, ...newSSlots];
  
  // window.lastSelectedSlotsを更新
  window.lastSelectedSlots = updatedSlots;
  
  console.log(`✅ 更新されたwindow.lastSelectedSlots:`, window.lastSelectedSlots);
  
  // structure_builder.jsの仕組みを完全に使用して再構築
  buildStructureForSIndividual(updatedSlots);
  
  // 静的エリアとの同期（全体ランダマイザーと同じ）
  if (typeof syncDynamicToStatic === "function") {
    syncDynamicToStatic();
    console.log("🔄 静的エリアとの同期完了");
  }
  
  console.log("✅ Sスロット個別ランダマイズ完了（完全コピー版）");
}

/**
 * 現在のV_group_keyを取得（randomizer_all.jsと同じ）
 */
function getCurrentVGroupKey() {
  if (window.lastSelectedSlots && window.lastSelectedSlots.length > 0) {
    const firstSlot = window.lastSelectedSlots[0];
    return firstSlot.V_group_key;
  }
  return null;
}

/**
 * Sスロット個別用のstructure_builder（完全コピー版）
 */
function buildStructureForSIndividual(selectedSlots) {
  console.log("🏗️ buildStructureForSIndividual called with selectedSlots:", selectedSlots);
  
  let wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.error('slot-wrapper not found, skipping structure generation');
    return;
  }

  let dynamicArea = document.getElementById('dynamic-slot-area');
  if (!dynamicArea) {
    dynamicArea = document.createElement('div');
    dynamicArea.id = 'dynamic-slot-area';
    wrapper.appendChild(dynamicArea);
  }

  // 動的記載エリアを完全にクリア
  dynamicArea.innerHTML = '';

  // 上位スロットのリセット（structure_builder.jsと同じ）
  const slotContainers = wrapper.querySelectorAll('.slot-container');
  slotContainers.forEach(container => {
    const phraseDiv = container.querySelector('.slot-phrase');
    if (phraseDiv) phraseDiv.innerText = '';
    const textDiv = container.querySelector('.slot-text');
    if (textDiv) textDiv.innerText = '';
  });

  const upperSlots = selectedSlots.filter(e => !e.SubslotID);

  // 🔍 分離疑問詞判定とDisplayAtTop付加（structure_builder.jsと同じ）
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

  upperSlots.sort((a, b) => a.Slot_display_order - b.Slot_display_order);

  upperSlots.forEach(item => {
    console.log(`Processing upper slot: ${item.Slot} (PhraseType: ${item.PhraseType})`);

    // 🔽 DisplayAtTop が付加された上位スロットは動的記載エリアに出力しない
    if (item.DisplayAtTop === true) {
      console.log(`🚫 DisplayAtTop により ${item.Slot} の表示をスキップ`);
      return;
    }

    if (item.PhraseType === 'word') {
      const slotDiv = renderSlotForSIndividual(item);
      dynamicArea.appendChild(slotDiv);
    } else {
      console.log(`Skipped upper slot: ${item.Slot} (PhraseType: ${item.PhraseType})`);
    }

    const subslots = selectedSlots.filter(s =>
      s.Slot === item.Slot &&
      s.SubslotID &&
      s.Slot_display_order === item.Slot_display_order
    );
    subslots.sort((a, b) => a.display_order - b.display_order);

    subslots.forEach(sub => {
      console.log(`Adding subslot to ${item.Slot}: ${sub.SubslotID} (display_order: ${sub.display_order})`);
      const subDiv = renderSubslotForSIndividual(sub);
      dynamicArea.appendChild(subDiv);
    });
  });
}

/**
 * Sスロット個別用のrenderSlot（structure_builder.jsの完全コピー）
 */
function renderSlotForSIndividual(item) {
  console.log("renderSlotForSIndividual item:", item); 
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
  }

  return slotDiv;
}

/**
 * Sスロット個別用のrenderSubslot（structure_builder.jsの完全コピー）
 */
function renderSubslotForSIndividual(sub) {
  console.log("renderSubslotForSIndividual sub:", sub);
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
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

// デバッグ: 関数が正しく設定されたか確認
console.log("✅ Sスロット個別ランダマイザー読み込み完了（完全コピー版）");
console.log("🔍 window.randomizeSlotSIndividual:", typeof window.randomizeSlotSIndividual);

// グローバルスコープテスト関数を追加
window.testSRandomizer = function() {
  console.log("🧪 テスト関数が動作しています");
  console.log("🧪 randomizeSlotSIndividual関数:", typeof window.randomizeSlotSIndividual);
  return "テスト成功";
};