/**
 * Sスロット個別ランダマイザー（データ構造対応版）
 * V_group_key、例文IDが存在しないデータに対応
 */

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
  console.log("🎲🎯 Sスロット個別ランダマイズ開始（データ構造対応版）");
  
  // 既存のlastSelectedSlotsの存在確認（なくても実行可能）
  let hasExistingSelection = window.lastSelectedSlots && Array.isArray(window.lastSelectedSlots);
  console.log(`🔍 既存選択データ: ${hasExistingSelection ? "あり" : "なし"}`);
  
  if (!hasExistingSelection) {
    console.log("📢 既存選択がないため、新規でSスロットのみを選択します");
  }
  
  if (!window.loadedJsonData || !Array.isArray(window.loadedJsonData)) {
    console.warn("⚠️ window.loadedJsonDataが見つかりません。先にJSONを読み込んでください。");
    return;
  }
  
  console.log("� 読み込まれたデータの構造を確認中...");
  console.log("📝 利用可能フィールド:", Object.keys(window.loadedJsonData[0] || {}));
  
  // V_group_keyが存在しない場合の対応：直接Sスロット候補を検索
  const allSSlots = window.loadedJsonData.filter(entry => entry.Slot === "S" && !entry.SubslotID);
  console.log(`🔍 全Sスロット候補数: ${allSSlots.length}`);
  console.log(`🔍 Sスロット候補例:`, allSSlots.slice(0, 3));
  
  if (allSSlots.length === 0) {
    console.warn("⚠️ Sスロット候補が見つかりません");
    alert("エラー: Sスロット候補が見つかりません。\n読み込まれたデータにSスロットが存在しないようです。");
    return;
  }
  
  // Sスロットをランダム選択
  const chosenS = allSSlots[Math.floor(Math.random() * allSSlots.length)];
  console.log(`🎯 選択されたSスロット:`, chosenS);
  
  // 関連サブスロットを取得（識別番号またはSlot_display_orderで関連付け）
  let relatedSubslots = [];
  
  // 識別番号による関連付けを試行
  if (chosenS.識別番号) {
    relatedSubslots = window.loadedJsonData.filter(entry =>
      entry.Slot === "S" &&
      entry.SubslotID &&
      entry.識別番号 === chosenS.識別番号
    );
    console.log(`🔍 識別番号による関連サブスロット数: ${relatedSubslots.length}`);
  }
  
  // 識別番号で見つからない場合、Slot_display_orderで関連付け
  if (relatedSubslots.length === 0) {
    relatedSubslots = window.loadedJsonData.filter(entry =>
      entry.Slot === "S" &&
      entry.SubslotID &&
      entry.Slot_display_order === chosenS.Slot_display_order
    );
    console.log(`🔍 Slot_display_orderによる関連サブスロット数: ${relatedSubslots.length}`);
  }
  
  console.log(`🔍 関連サブスロット例:`, relatedSubslots.slice(0, 2));
  
  // 新しいSスロットデータを構築
  const newSSlots = [
    { ...chosenS },
    ...relatedSubslots.map(sub => ({ ...sub }))
  ];
  
  // 既存選択がある場合は、Sスロット以外を保持
  let finalSlots = [];
  if (hasExistingSelection) {
    finalSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
    finalSlots.push(...newSSlots);
    console.log("🔄 既存選択を保持してSスロットのみ更新");
  } else {
    finalSlots = newSSlots;
    console.log("🆕 新規選択としてSスロットのみ設定");
  }
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = finalSlots;
  
  const data = finalSlots.map(slot => ({
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
  
  console.log("🎯 Sスロット個別ランダマイズ結果:", JSON.stringify(data, null, 2));
  
  // 構造を再構築
  buildStructure(data);
  
  // 静的エリアとの同期
  if (typeof syncDynamicToStatic === "function") {
    syncDynamicToStatic();
    console.log("🔄 静的エリアとの同期完了");
  }
  
  console.log("✅ Sスロット個別ランダマイズ完了（データ構造対応版）");
}

/**
 * 指定されたV_group_keyでSスロット個別ランダマイズを実行
 */
function randomizeWithGroup(selectedGroup, groupSlots, exampleIDs) {
  console.log(`🎲 V_group_key "${selectedGroup}" でSスロット個別ランダマイズを実行`);
  
  // スロットセットを構築（元のrandomizeAllと同じロジック）
  let slotSets = [];
  exampleIDs.forEach((id, index) => {
    const setNumber = index + 1;
    const slots = groupSlots.filter(entry => entry.例文ID === id && !entry.SubslotID).map(entry => ({
      ...entry,
      識別番号: `${entry.Slot}-${setNumber}`
    }));
    slotSets.push(slots);
  });
  
  // Sスロット候補を取得
  const sCandidates = slotSets.flat().filter(entry => entry.Slot === "S");
  console.log(`🔍 Sスロット候補数: ${sCandidates.length}`);
  console.log(`🔍 Sスロット候補例:`, sCandidates.slice(0, 3));
  
  if (sCandidates.length === 0) {
    console.warn(`⚠️ V_group_key "${selectedGroup}" にSスロット候補が見つかりません`);
    
    // デバッグ情報
    const availableSlots = [...new Set(groupSlots.map(entry => entry.Slot))];
    console.log(`🔍 利用可能なスロットタイプ:`, availableSlots);
    console.log("🔍 slotSets:", slotSets.slice(0, 2));
    
    alert(`エラー: V_group_key "${selectedGroup}" にSスロット候補が見つかりません。`);
    return;
  }
  
  // Sスロットをランダム選択
  const chosenS = sCandidates[Math.floor(Math.random() * sCandidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosenS);
  
  // 関連サブスロットを取得
  const relatedSubslots = groupSlots.filter(e =>
    e.例文ID === chosenS.例文ID &&
    e.Slot === chosenS.Slot &&
    e.SubslotID
  );
  console.log(`🔍 関連サブスロット数: ${relatedSubslots.length}`);
  
  // 既存のlastSelectedSlotsからSスロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
  
  // 新しいSスロットとサブスロットを追加（V_group_keyも更新）
  const newSSlots = [
    { ...chosenS, V_group_key: selectedGroup }, 
    ...relatedSubslots.map(sub => ({ ...sub, V_group_key: selectedGroup }))
  ];
  filteredSlots.push(...newSSlots);
  
  // lastSelectedSlotsを更新（全ての要素のV_group_keyを更新）
  window.lastSelectedSlots = filteredSlots.map(slot => ({ ...slot, V_group_key: selectedGroup }));
  
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
  
  console.log(`ランダマイズ結果詳細（Sスロット個別・V_group_key: ${selectedGroup}）:`, JSON.stringify(data, null, 2));
  buildStructure(data);
  
  if (typeof syncDynamicToStatic === "function") {
    syncDynamicToStatic();
    console.log("🔄 静的エリアとの同期完了");
  }
  
  console.log(`✅ Sスロット個別ランダマイズ完了（V_group_key: ${selectedGroup}）`);
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

// テスト用関数：ボタンを探してクリック
window.testSIndividualButton = function() {
  console.log("🔍 Sスロット個別ランダマイズボタンのテスト開始");
  const button = document.querySelector(".s-individual-randomize-btn");
  if (button) {
    console.log("✅ ボタンが見つかりました。クリックします:", button);
    button.click();
  } else {
    console.error("❌ ボタンが見つかりません");
  }
};

// ページ読み込み後にボタンの存在を確認
document.addEventListener("DOMContentLoaded", () => {
  console.log("🔍 Sスロット個別ランダマイズボタンの確認開始");
  const button = document.querySelector(".s-individual-randomize-btn");
  if (button) {
    console.log("✅ Sスロット個別ランダマイズボタンが見つかりました:", button);
    console.log("ボタンのスタイル:", window.getComputedStyle(button));
  } else {
    console.error("❌ Sスロット個別ランダマイズボタンが見つかりません");
  }
  
  // 個別ランダマイズボタンのコンテナも確認
  const container = document.querySelector(".individual-randomize-button");
  if (container) {
    console.log("✅ 個別ランダマイズボタンコンテナが見つかりました:", container);
    console.log("コンテナのスタイル:", window.getComputedStyle(container));
  } else {
    console.error("❌ 個別ランダマイズボタンコンテナが見つかりません");
  }
});