/**
 * Sスロット個別ランダマイザー
 */

/**
 * Sスロット個別ランダマイズ関数
 */
function randomizeSlotSIndividual() {
  console.log("🎲🎯 Sスロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからSスロット候補を取得
  const sCandidates = window.fullSlotPool.filter(entry => entry.Slot === "S" && !entry.SubslotID);
  console.log(`🔍 Sスロット候補数: ${sCandidates.length}`);
  console.log(`🔍 Sスロット候補:`, sCandidates);
  
  if (sCandidates.length <= 1) {
    console.warn("⚠️ Sスロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にSスロットの候補が複数ありません。");
    return;
  }
  
  // 現在のSスロットを取得
  const currentS = window.lastSelectedSlots.find(slot => slot.Slot === "S" && !slot.SubslotID);
  console.log(`🔍 現在のSスロット:`, currentS);
  
  // 現在と異なるSスロット候補を取得
  let availableCandidates = sCandidates;
  if (currentS && currentS.例文ID) {
    availableCandidates = sCandidates.filter(candidate => candidate.例文ID !== currentS.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるSスロット候補が見つかりません");
    alert("エラー: 現在と異なるSスロット候補が見つかりません。");
    return;
  }
  
  // 新しいSスロットをランダム選択
  const chosenS = availableCandidates[Math.floor(Math.random() * availableCandidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosenS);
  
  // 選択されたSスロットに関連するサブスロットを取得
  const relatedSubslots = window.fullSlotPool.filter(entry =>
    entry.例文ID === chosenS.例文ID &&
    entry.Slot === "S" &&
    entry.SubslotID
  );
  console.log(`🔍 関連サブスロット数: ${relatedSubslots.length}`);
  console.log(`🔍 関連サブスロット:`, relatedSubslots);
  
  // lastSelectedSlotsからSスロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
  
  // 新しいSスロットとサブスロットを追加
  const newSSlots = [
    { ...chosenS },
    ...relatedSubslots.map(sub => ({ ...sub }))
  ];
  filteredSlots.push(...newSSlots);
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  // buildStructure用のデータ形式に変換
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
  
  console.log("🎯 Sスロット個別ランダマイズ結果:", JSON.stringify(data, null, 2));
  
  // 構造を再構築（buildStructureを使用）
  if (typeof buildStructure === "function") {
    buildStructure(data);
  } else {
    console.error("❌ buildStructure関数が見つかりません");
  }
  
  // 静的エリアとの同期
  if (typeof syncUpperSlotsFromJson === "function") {
    syncUpperSlotsFromJson(data);
    console.log("🔄 上位スロット同期完了");
  }
  
  if (typeof syncSubslotsFromJson === "function") {
    syncSubslotsFromJson(data);
    console.log("🔄 サブスロット同期完了");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🖼️ Sサブスロット画像更新（個別ランダム化後）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('s');
      console.log("🎨 Sサブスロット画像更新完了");
    }, 150);
  }
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

/**
 * M1スロット個別ランダマイズ関数
 */
function randomizeSlotM1Individual() {
  console.log("🎲🎯 M1スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に例文シャッフルを実行してください。");
    alert("エラー: 先に例文シャッフルを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからM1スロット候補を取得
  const m1Candidates = window.fullSlotPool.filter(entry => entry.Slot === "M1" && !entry.SubslotID);
  console.log(`🔍 M1スロット候補数: ${m1Candidates.length}`);
  console.log(`🔍 M1スロット候補:`, m1Candidates);
  
  if (m1Candidates.length <= 1) {
    console.warn("⚠️ M1スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にM1スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のM1スロットを取得
  const currentM1 = window.lastSelectedSlots.find(slot => slot.Slot === "M1" && !slot.SubslotID);
  console.log(`🔍 現在のM1スロット:`, currentM1);
  
  // 現在と異なるM1スロット候補を取得
  let availableCandidates = m1Candidates;
  if (currentM1 && currentM1.例文ID) {
    availableCandidates = m1Candidates.filter(candidate => candidate.例文ID !== currentM1.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるM1スロット候補が見つかりません");
    alert("エラー: 現在と異なるM1スロット候補が見つかりません。");
    return;
  }
  
  // 新しいM1スロットをランダム選択
  const chosenM1 = availableCandidates[Math.floor(Math.random() * availableCandidates.length)];
  console.log(`🎯 選択されたM1スロット:`, chosenM1);
  
  // 選択されたM1スロットに関連するサブスロットを取得
  const relatedSubslots = window.fullSlotPool.filter(entry =>
    entry.例文ID === chosenM1.例文ID &&
    entry.Slot === "M1" &&
    entry.SubslotID
  );
  console.log(`🔍 関連サブスロット数: ${relatedSubslots.length}`);
  console.log(`🔍 関連サブスロット:`, relatedSubslots);
  
  // lastSelectedSlotsからM1スロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "M1");
  
  // 新しいM1スロットとサブスロットを追加
  const newM1Slots = [
    { ...chosenM1 },
    ...relatedSubslots.map(sub => ({ ...sub }))
  ];
  filteredSlots.push(...newM1Slots);
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  // buildStructure用のデータ形式に変換
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
  
  console.log("🎯 M1スロット個別ランダマイズ結果:", JSON.stringify(data, null, 2));
  
  // 構造を再構築（buildStructureを使用）
  if (typeof buildStructure === "function") {
    buildStructure(data);
  } else {
    console.error("❌ buildStructure関数が見つかりません");
  }
  
  // 静的エリアとの同期
  if (typeof syncUpperSlotsFromJson === "function") {
    syncUpperSlotsFromJson(data);
    console.log("🔄 上位スロット同期完了");
  }
  
  if (typeof syncSubslotsFromJson === "function") {
    syncSubslotsFromJson(data);
    console.log("🔄 サブスロット同期完了");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🖼️ M1サブスロット画像更新（個別ランダム化後）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('m1');
      console.log("🎨 M1サブスロット画像更新完了");
    }, 150);
  }
  
  console.log("✅ M1スロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotM1Individual = randomizeSlotM1Individual;

/**
 * M2スロット個別ランダマイズ関数
 */
function randomizeSlotM2Individual() {
  console.log("🎲🎯 M2スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからM2スロット候補を取得
  const m2Candidates = window.fullSlotPool.filter(entry => entry.Slot === "M2" && !entry.SubslotID);
  console.log(`🔍 M2スロット候補数: ${m2Candidates.length}`);
  console.log(`🔍 M2スロット候補:`, m2Candidates);
  
  if (m2Candidates.length <= 1) {
    console.warn("⚠️ M2スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にM2スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のM2スロットを取得
  const currentM2 = window.lastSelectedSlots.find(slot => slot.Slot === "M2" && !slot.SubslotID);
  console.log(`🔍 現在のM2スロット:`, currentM2);
  
  // 現在と異なるM2スロット候補を取得
  let availableCandidates = m2Candidates;
  if (currentM2 && currentM2.例文ID) {
    availableCandidates = m2Candidates.filter(candidate => candidate.例文ID !== currentM2.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるM2スロット候補が見つかりません");
    alert("エラー: 現在と異なるM2スロット候補が見つかりません。");
    return;
  }
  
  // 新しいM2スロットをランダム選択
  const chosenM2 = availableCandidates[Math.floor(Math.random() * availableCandidates.length)];
  console.log(`🎯 選択されたM2スロット:`, chosenM2);
  
  // 選択されたM2スロットに関連するサブスロットを取得
  const relatedSubslots = window.fullSlotPool.filter(entry =>
    entry.例文ID === chosenM2.例文ID &&
    entry.Slot === "M2" &&
    entry.SubslotID
  );
  console.log(`🔍 関連サブスロット数: ${relatedSubslots.length}`);
  console.log(`🔍 関連サブスロット:`, relatedSubslots);
  
  // lastSelectedSlotsからM2スロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "M2");
  
  // 新しいM2スロットとサブスロットを追加
  const newM2Slots = [
    { ...chosenM2 },
    ...relatedSubslots.map(sub => ({ ...sub }))
  ];
  filteredSlots.push(...newM2Slots);
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  // buildStructure用のデータ形式に変換
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
  
  console.log("🎯 M2スロット個別ランダマイズ結果:", JSON.stringify(data, null, 2));
  
  // 構造を再構築（buildStructureを使用）
  if (typeof buildStructure === "function") {
    buildStructure(data);
  } else {
    console.error("❌ buildStructure関数が見つかりません");
  }
  
  // 静的エリアとの同期
  if (typeof syncUpperSlotsFromJson === "function") {
    syncUpperSlotsFromJson(data);
    console.log("🔄 上位スロット同期完了");
  }
  
  if (typeof syncSubslotsFromJson === "function") {
    syncSubslotsFromJson(data);
    console.log("🔄 サブスロット同期完了");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🖼️ M2サブスロット画像更新（個別ランダム化後）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('m2');
      console.log("🎨 M2サブスロット画像更新完了");
    }, 150);
  }
  
  console.log("✅ M2スロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotM2Individual = randomizeSlotM2Individual;

/**
 * C1スロット個別ランダマイズ関数
 */
function randomizeSlotC1Individual() {
  console.log("🎲🎯 C1スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからC1スロット候補を取得
  const c1Candidates = window.fullSlotPool.filter(entry => entry.Slot === "C1" && !entry.SubslotID);
  console.log(`🔍 C1スロット候補数: ${c1Candidates.length}`);
  console.log(`🔍 C1スロット候補:`, c1Candidates);
  
  if (c1Candidates.length <= 1) {
    console.warn("⚠️ C1スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にC1スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のC1スロットを取得
  const currentC1 = window.lastSelectedSlots.find(slot => slot.Slot === "C1" && !slot.SubslotID);
  console.log(`🔍 現在のC1スロット:`, currentC1);
  
  // 現在と異なるC1スロット候補を取得
  let availableCandidates = c1Candidates;
  if (currentC1 && currentC1.例文ID) {
    availableCandidates = c1Candidates.filter(candidate => candidate.例文ID !== currentC1.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるC1スロット候補が見つかりません");
    alert("エラー: 現在と異なるC1スロット候補が見つかりません。");
    return;
  }
  
  // 新しいC1スロットをランダム選択
  const chosenC1 = availableCandidates[Math.floor(Math.random() * availableCandidates.length)];
  console.log(`🎯 選択されたC1スロット:`, chosenC1);
  
  // 選択されたC1スロットに関連するサブスロットを取得
  const relatedSubslots = window.fullSlotPool.filter(entry =>
    entry.例文ID === chosenC1.例文ID &&
    entry.Slot === "C1" &&
    entry.SubslotID
  );
  console.log(`🔍 関連サブスロット数: ${relatedSubslots.length}`);
  console.log(`🔍 関連サブスロット:`, relatedSubslots);
  
  // lastSelectedSlotsからC1スロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "C1");
  
  // 新しいC1スロットとサブスロットを追加
  const newC1Slots = [
    { ...chosenC1 },
    ...relatedSubslots.map(sub => ({ ...sub }))
  ];
  filteredSlots.push(...newC1Slots);
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  // buildStructure用のデータ形式に変換
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
  
  console.log("🎯 C1スロット個別ランダマイズ結果:", JSON.stringify(data, null, 2));
  
  // 構造を再構築（buildStructureを使用）
  if (typeof buildStructure === "function") {
    buildStructure(data);
  } else {
    console.error("❌ buildStructure関数が見つかりません");
  }
  
  // 静的エリアとの同期
  if (typeof syncUpperSlotsFromJson === "function") {
    syncUpperSlotsFromJson(data);
    console.log("🔄 上位スロット同期完了");
  }
  
  if (typeof syncSubslotsFromJson === "function") {
    syncSubslotsFromJson(data);
    console.log("🔄 サブスロット同期完了");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🆕 サブスロット画像更新（C1専用）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('c1');
      console.log("🎨 C1サブスロット画像更新完了");
    }, 200);
  }
  
  console.log("✅ C1スロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotC1Individual = randomizeSlotC1Individual;

/**
 * O1スロット個別ランダマイズ関数
 */
function randomizeSlotO1Individual() {
  console.log("🎲🎯 O1スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからO1スロット候補を取得
  const o1Candidates = window.fullSlotPool.filter(entry => entry.Slot === "O1" && !entry.SubslotID);
  console.log(`🔍 O1スロット候補数: ${o1Candidates.length}`);
  console.log(`🔍 O1スロット候補:`, o1Candidates);
  
  if (o1Candidates.length <= 1) {
    console.warn("⚠️ O1スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にO1スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のO1スロットを取得
  const currentO1 = window.lastSelectedSlots.find(slot => slot.Slot === "O1" && !slot.SubslotID);
  console.log(`🔍 現在のO1スロット:`, currentO1);
  
  // 現在と異なるO1スロット候補を取得
  let availableCandidates = o1Candidates;
  if (currentO1 && currentO1.例文ID) {
    availableCandidates = o1Candidates.filter(candidate => candidate.例文ID !== currentO1.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるO1スロット候補が見つかりません");
    alert("エラー: 現在と異なるO1スロット候補が見つかりません。");
    return;
  }
  
  // 新しいO1スロットをランダム選択
  const chosenO1 = availableCandidates[Math.floor(Math.random() * availableCandidates.length)];
  console.log(`🎯 選択されたO1スロット:`, chosenO1);
  
  // 選択されたO1スロットに関連するサブスロットを取得
  const relatedSubslots = window.fullSlotPool.filter(entry =>
    entry.例文ID === chosenO1.例文ID &&
    entry.Slot === "O1" &&
    entry.SubslotID
  );
  console.log(`🔍 関連サブスロット数: ${relatedSubslots.length}`);
  console.log(`🔍 関連サブスロット:`, relatedSubslots);
  
  // lastSelectedSlotsからO1スロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "O1");
  
  // 新しいO1スロットとサブスロットを追加
  const newO1Slots = [
    { ...chosenO1 },
    ...relatedSubslots.map(sub => ({ ...sub }))
  ];
  filteredSlots.push(...newO1Slots);
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  // buildStructure用のデータ形式に変換
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
  
  console.log("🎯 O1スロット個別ランダマイズ結果:", JSON.stringify(data, null, 2));
  
  // 構造を再構築（buildStructureを使用）
  if (typeof buildStructure === "function") {
    buildStructure(data);
  } else {
    console.error("❌ buildStructure関数が見つかりません");
  }
  
  // 静的エリアとの同期
  if (typeof syncUpperSlotsFromJson === "function") {
    syncUpperSlotsFromJson(data);
    console.log("🔄 上位スロット同期完了");
  }
  
  if (typeof syncSubslotsFromJson === "function") {
    syncSubslotsFromJson(data);
    console.log("🔄 サブスロット同期完了");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🖼️ O1サブスロット画像更新（個別ランダム化後）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('o1');
      console.log("🎨 O1サブスロット画像更新完了");
    }, 150);
  }
  
  // 🎛️ O1サブスロットの表示状態を復元（パネル設定を再適用）
  setTimeout(() => {
    restoreO1SubslotVisibility();
    console.log("🎛️ O1サブスロット表示状態復元完了");
  }, 200);
  
  console.log("✅ O1スロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotO1Individual = randomizeSlotO1Individual;

/**
 * O2スロット個別ランダマイズ関数
 */
function randomizeSlotO2Individual() {
  console.log("🎲🎯 O2スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからO2スロット候補を取得
  const o2Candidates = window.fullSlotPool.filter(entry => entry.Slot === "O2" && !entry.SubslotID);
  console.log(`🔍 O2スロット候補数: ${o2Candidates.length}`);
  console.log(`🔍 O2スロット候補:`, o2Candidates);
  
  if (o2Candidates.length <= 1) {
    console.warn("⚠️ O2スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にO2スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のO2スロットを取得
  const currentO2 = window.lastSelectedSlots.find(slot => slot.Slot === "O2" && !slot.SubslotID);
  console.log(`🔍 現在のO2スロット:`, currentO2);
  
  // 現在と異なるO2スロット候補を取得
  let availableCandidates = o2Candidates;
  if (currentO2 && currentO2.例文ID) {
    availableCandidates = o2Candidates.filter(candidate => candidate.例文ID !== currentO2.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるO2スロット候補が見つかりません");
    alert("エラー: 現在と異なるO2スロット候補が見つかりません。");
    return;
  }
  
  // ランダムに新しいO2スロットを選択
  const randomIndex = Math.floor(Math.random() * availableCandidates.length);
  const newO2 = availableCandidates[randomIndex];
  console.log(`🎲 新しいO2スロット選択:`, newO2);
  
  // O2サブスロットを取得
  const newO2Subslots = window.fullSlotPool.filter(entry => 
    entry.Slot === "O2" && 
    entry.SubslotID && 
    entry.例文ID === newO2.例文ID
  );
  console.log(`🔍 新しいO2サブスロット (${newO2Subslots.length}個):`, newO2Subslots);
  
  // lastSelectedSlotsを更新（O2とそのサブスロットのみ）
  // 既存のO2関連データを削除
  window.lastSelectedSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "O2");
  
  // 新しいO2メインスロットを追加
  window.lastSelectedSlots.push(newO2);
  
  // 新しいO2サブスロットを追加
  newO2Subslots.forEach(subslot => {
    window.lastSelectedSlots.push(subslot);
  });
  
  console.log(`✅ O2スロット個別ランダマイズ完了: ${newO2.例文ID} → ${newO2.Text}`);
  console.log(`📊 更新後のlastSelectedSlots:`, window.lastSelectedSlots);
  
  // 構造を再構築し、静的エリアも同期
  if (typeof buildStructure === 'function') {
    buildStructure(window.lastSelectedSlots);
    console.log("🏗️ buildStructure()実行完了");
  } else {
    console.warn("⚠️ buildStructure関数が見つかりません");
  }
  
  // 静的エリアの同期
  if (typeof syncUpperSlotsFromJson === 'function') {
    syncUpperSlotsFromJson(window.lastSelectedSlots);
    console.log("🔄 syncUpperSlotsFromJson()実行完了");
  } else {
    console.warn("⚠️ syncUpperSlotsFromJson関数が見つかりません");
  }
  
  if (typeof syncSubslotsFromJson === 'function') {
    syncSubslotsFromJson(window.lastSelectedSlots);
    console.log("🔄 syncSubslotsFromJson()実行完了");
  } else {
    console.warn("⚠️ syncSubslotsFromJson関数が見つかりません");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🖼️ O2サブスロット画像更新（個別ランダム化後）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('o2');
      console.log("🎨 O2サブスロット画像更新完了");
    }, 150);
  }
  
  console.log("✅ O2スロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotO2Individual = randomizeSlotO2Individual;

/**
 * C2スロット個別ランダマイズ関数
 */
function randomizeSlotC2Individual() {
  console.log("🎲🎯 C2スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからC2スロット候補を取得
  const c2Candidates = window.fullSlotPool.filter(entry => entry.Slot === "C2" && !entry.SubslotID);
  console.log(`🔍 C2スロット候補数: ${c2Candidates.length}`);
  console.log(`🔍 C2スロット候補:`, c2Candidates);
  
  if (c2Candidates.length <= 1) {
    console.warn("⚠️ C2スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にC2スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のC2スロットを取得
  const currentC2 = window.lastSelectedSlots.find(slot => slot.Slot === "C2" && !slot.SubslotID);
  console.log(`🔍 現在のC2スロット:`, currentC2);
  
  // 現在と異なるC2スロット候補を取得
  let availableCandidates = c2Candidates;
  if (currentC2 && currentC2.例文ID) {
    availableCandidates = c2Candidates.filter(candidate => candidate.例文ID !== currentC2.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるC2スロット候補が見つかりません");
    alert("エラー: 現在と異なるC2スロット候補が見つかりません。");
    return;
  }
  
  // ランダムに新しいC2スロットを選択
  const randomIndex = Math.floor(Math.random() * availableCandidates.length);
  const newC2 = availableCandidates[randomIndex];
  console.log(`🎲 新しいC2スロット選択:`, newC2);
  
  // C2サブスロットを取得
  const newC2Subslots = window.fullSlotPool.filter(entry => 
    entry.Slot === "C2" && 
    entry.SubslotID && 
    entry.例文ID === newC2.例文ID
  );
  console.log(`🔍 新しいC2サブスロット (${newC2Subslots.length}個):`, newC2Subslots);
  
  // lastSelectedSlotsを更新（C2とそのサブスロットのみ）
  // 既存のC2関連データを削除
  window.lastSelectedSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "C2");
  
  // 新しいC2メインスロットを追加
  window.lastSelectedSlots.push(newC2);
  
  // 新しいC2サブスロットを追加
  newC2Subslots.forEach(subslot => {
    window.lastSelectedSlots.push(subslot);
  });
  
  console.log(`✅ C2スロット個別ランダマイズ完了: ${newC2.例文ID} → ${newC2.Text}`);
  console.log(`📊 更新後のlastSelectedSlots:`, window.lastSelectedSlots);
  
  // 構造を再構築し、静的エリアも同期
  if (typeof buildStructure === 'function') {
    buildStructure(window.lastSelectedSlots);
    console.log("🏗️ buildStructure()実行完了");
  } else {
    console.warn("⚠️ buildStructure関数が見つかりません");
  }
  
  // 静的エリアの同期
  if (typeof syncUpperSlotsFromJson === 'function') {
    syncUpperSlotsFromJson(window.lastSelectedSlots);
    console.log("🔄 syncUpperSlotsFromJson()実行完了");
  } else {
    console.warn("⚠️ syncUpperSlotsFromJson関数が見つかりません");
  }
  
  if (typeof syncSubslotsFromJson === 'function') {
    syncSubslotsFromJson(window.lastSelectedSlots);
    console.log("🔄 syncSubslotsFromJson()実行完了");
  } else {
    console.warn("⚠️ syncSubslotsFromJson関数が見つかりません");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }
  
  // 🖼️ C2サブスロット画像更新（個別ランダム化後）
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('c2');
      console.log("🎨 C2サブスロット画像更新完了");
    }, 150);
  }
  
  console.log("✅ C2スロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotC2Individual = randomizeSlotC2Individual;

/**
 * M3スロット個別ランダマイズ関数
 */
function randomizeSlotM3Individual() {
  console.log("🎲🎯 M3スロット個別ランダマイズ開始");
  
  // fullSlotPoolの存在確認
  if (!window.fullSlotPool || !Array.isArray(window.fullSlotPool)) {
    console.warn("⚠️ window.fullSlotPoolが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // fullSlotPoolからM3スロット候補を取得
  const m3Candidates = window.fullSlotPool.filter(entry => entry.Slot === "M3" && !entry.SubslotID);
  console.log(`🔍 M3スロット候補数: ${m3Candidates.length}`);
  console.log(`🔍 M3スロット候補:`, m3Candidates);
  
  if (m3Candidates.length <= 1) {
    console.warn("⚠️ M3スロット候補が1つ以下のため、ランダマイズできません");
    alert("エラー: 同じグループ内にM3スロットの候補が複数ありません。");
    return;
  }
  
  // 現在のM3スロットを取得
  const currentM3 = window.lastSelectedSlots.find(slot => slot.Slot === "M3" && !slot.SubslotID);
  console.log(`🔍 現在のM3スロット:`, currentM3);
  
  // 現在と異なるM3スロット候補を取得
  let availableCandidates = m3Candidates;
  if (currentM3 && currentM3.例文ID) {
    availableCandidates = m3Candidates.filter(candidate => candidate.例文ID !== currentM3.例文ID);
  }
  
  if (availableCandidates.length === 0) {
    console.warn("⚠️ 現在と異なるM3スロット候補が見つかりません");
    alert("エラー: 現在と異なるM3スロット候補が見つかりません。");
    return;
  }
  
  // ランダムに新しいM3スロットを選択
  const randomIndex = Math.floor(Math.random() * availableCandidates.length);
  const newM3 = availableCandidates[randomIndex];
  console.log(`🎲 新しいM3スロット選択:`, newM3);
  
  // M3サブスロットを取得
  const newM3Subslots = window.fullSlotPool.filter(entry => 
    entry.Slot === "M3" && 
    entry.SubslotID && 
    entry.例文ID === newM3.例文ID
  );
  console.log(`🔍 新しいM3サブスロット (${newM3Subslots.length}個):`, newM3Subslots);
  
  // lastSelectedSlotsを更新（M3とそのサブスロットのみ）
  // 既存のM3関連データを削除
  window.lastSelectedSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "M3");
  
  // 新しいM3メインスロットを追加
  window.lastSelectedSlots.push(newM3);
  
  // 新しいM3サブスロットを追加
  newM3Subslots.forEach(subslot => {
    window.lastSelectedSlots.push(subslot);
  });
  
  console.log(`✅ M3スロット個別ランダマイズ完了: ${newM3.例文ID} → ${newM3.Text}`);
  console.log(`📊 更新後のlastSelectedSlots:`, window.lastSelectedSlots);
  
  // 構造を再構築し、静的エリアも同期
  if (typeof buildStructure === 'function') {
    buildStructure(window.lastSelectedSlots);
    console.log("🏗️ buildStructure()実行完了");
  } else {
    console.warn("⚠️ buildStructure関数が見つかりません");
  }
  
  // 静的エリアの同期
  if (typeof syncUpperSlotsFromJson === 'function') {
    syncUpperSlotsFromJson(window.lastSelectedSlots);
    console.log("🔄 syncUpperSlotsFromJson()実行完了");
  } else {
    console.warn("⚠️ syncUpperSlotsFromJson関数が見つかりません");
  }
  
  if (typeof syncSubslotsFromJson === 'function') {
    syncSubslotsFromJson(window.lastSelectedSlots);
    console.log("🔄 syncSubslotsFromJson()実行完了");
  } else {
    console.warn("⚠️ syncSubslotsFromJson関数が見つかりません");
  }
  
  // 全スロット画像更新
  if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
    setTimeout(() => {
      window.updateAllSlotImagesAfterDataChange();
      console.log("🎨 全スロット画像更新完了");
    }, 100);
  }

  // M3サブスロット画像更新
  if (typeof window.updateSubslotImages === "function") {
    setTimeout(() => {
      window.updateSubslotImages('m3');
      console.log("🎨 M3サブスロット画像更新完了");
    }, 150);
  }
}

// グローバル関数として公開
window.randomizeSlotM3Individual = randomizeSlotM3Individual;

// === 母集団確認用デバッグ関数群 ===

// 1. window.loadedJsonData内のSスロット母集団確認
window.checkSSlotInLoadedJson = function() {
  console.log("🔍=== window.loadedJsonData内のSスロット確認 ===");
  
  if (!window.loadedJsonData) {
    console.warn("⚠️ window.loadedJsonDataが存在しません");
    return;
  }
  
  console.log("📊 loadedJsonData総数:", window.loadedJsonData.length);
  
  // Sスロット関連データの抽出
  const sMainSlots = window.loadedJsonData.filter(entry => entry.Slot === "S" && !entry.SubslotID);
  const sSubSlots = window.loadedJsonData.filter(entry => entry.Slot === "S" && entry.SubslotID);
  
  console.log("📊 Sメインスロット数:", sMainSlots.length);
  console.log("📊 Sサブスロット数:", sSubSlots.length);
  
  if (sMainSlots.length > 0) {
    console.log("🔍 Sメインスロット一覧:", sMainSlots);
    
    // V_group_key別の分布
    const vGroupKeys = [...new Set(sMainSlots.map(s => s.V_group_key))];
    console.log("📊 利用可能なV_group_key:", vGroupKeys);
    
    vGroupKeys.forEach(key => {
      const slotsInGroup = sMainSlots.filter(s => s.V_group_key === key);
      const subsInGroup = sSubSlots.filter(s => s.V_group_key === key);
      console.log(`📊 V_group_key "${key}": メイン${slotsInGroup.length}個 + サブ${subsInGroup.length}個`);
    });
  }
  
  return { mainSlots: sMainSlots, subSlots: sSubSlots };
};

// 2. window.slotSets内のSスロット確認
window.checkSSlotInSlotSets = function() {
  console.log("🔍=== window.slotSets内のSスロット確認 ===");
  
  if (!window.slotSets) {
    console.warn("⚠️ window.slotSetsが存在しません");
    return;
  }
  
  console.log("📊 slotSets構造:", window.slotSets);
  const flatSlots = window.slotSets.flat();
  const sSlotsInSets = flatSlots.filter(entry => entry.Slot === "S");
  
  console.log("📊 slotSets内のSスロット総数:", sSlotsInSets.length);
  console.log("🔍 slotSets内のSスロット詳細:", sSlotsInSets);
  
  // サブスロット情報があるかチェック
  const sSubsInSets = sSlotsInSets.filter(entry => entry.SubslotID);
  console.log("📊 slotSets内のSサブスロット数:", sSubsInSets.length);
  
  return sSlotsInSets;
};

// 3. 現在選択中のデータ確認
window.checkCurrentSelection = function() {
  console.log("🔍=== 現在選択中のデータ確認 ===");
  
  if (window.lastSelectedSlots) {
    console.log("📊 lastSelectedSlots:", window.lastSelectedSlots);
    const currentS = window.lastSelectedSlots.filter(slot => slot.Slot === "S");
    console.log("📊 現在のSスロット:", currentS);
  } else {
    console.warn("⚠️ window.lastSelectedSlotsが存在しません");
  }
};

// 4. 総合確認関数
window.checkAllSSlotSources = function() {
  console.log("🔍=== 全Sスロットデータソース確認 ===");
  
  const loadedJson = window.checkSSlotInLoadedJson();
  const slotSets = window.checkSSlotInSlotSets();
  window.checkCurrentSelection();
  
  console.log("📊=== まとめ ===");
  console.log("loadedJsonData使用可能:", !!loadedJson && loadedJson.mainSlots.length > 0);
  console.log("slotSets使用可能:", !!slotSets && slotSets.length > 0);
  
  return {
    loadedJsonAvailable: !!loadedJson && loadedJson.mainSlots.length > 0,
    slotSetsAvailable: !!slotSets && slotSets.length > 0
  };
};

// 5. 新規追加: window.fullSlotPool確認関数
window.checkFullSlotPool = function() {
  console.log("🔍=== window.fullSlotPool確認 ===");
  
  if (!window.fullSlotPool) {
    console.warn("⚠️ window.fullSlotPoolが存在しません");
    return null;
  }
  
  console.log("📊 fullSlotPool総数:", window.fullSlotPool.length);
  
  // Sスロット関連データの抽出
  const sMainSlots = window.fullSlotPool.filter(entry => entry.Slot === "S" && !entry.SubslotID);
  const sSubSlots = window.fullSlotPool.filter(entry => entry.Slot === "S" && entry.SubslotID);
  
  console.log("📊 Sメインスロット数:", sMainSlots.length);
  console.log("📊 Sサブスロット数:", sSubSlots.length);
  
  if (sMainSlots.length > 0) {
    console.log("🔍 Sメインスロット一覧:", sMainSlots);
    
    // V_group_key別の分布
    const vGroupKeys = [...new Set(sMainSlots.map(s => s.V_group_key))];
    console.log("📊 利用可能なV_group_key:", vGroupKeys);
    
    // 例文ID別の分布
    const exampleIds = [...new Set(sMainSlots.map(s => s.例文ID))];
    console.log("📊 利用可能な例文ID:", exampleIds);
    
    exampleIds.forEach(id => {
      const slotsForId = sMainSlots.filter(s => s.例文ID === id);
      const subsForId = sSubSlots.filter(s => s.例文ID === id);
      console.log(`📊 例文ID "${id}": メイン${slotsForId.length}個 + サブ${subsForId.length}個`);
    });
  }
  
  if (sSubSlots.length > 0) {
    console.log("🔍 Sサブスロット詳細（最初の3個）:", sSubSlots.slice(0, 3));
  }
  
  return { 
    mainSlots: sMainSlots, 
    subSlots: sSubSlots,
    total: window.fullSlotPool.length
  };
};

/**
 * O1サブスロットの表示状態をリセットする関数
 * 個別ランダマイズ後は新しいコンテンツなので全て表示状態にリセット
 */
function restoreO1SubslotVisibility() {
  console.log("🎛️ O1サブスロット表示状態リセット開始（新しいコンテンツのため全て表示）");
  
  try {
    // O1サブスロットのIDパターンを取得
    const o1SubslotElements = document.querySelectorAll('[id^="slot-o1-sub-"]');
    console.log(`🔍 O1サブスロット要素: ${o1SubslotElements.length}個`);
    
    console.log("🎛️ O1サブスロット表示状態を全て表示にリセット中...");
    
    // 各O1サブスロットについて全て表示状態に設定
    o1SubslotElements.forEach(subslotElement => {
      const subslotId = subslotElement.id;
      
      // 各要素タイプ（image, text, auxtext）について全て表示状態にリセット
      ['image', 'text', 'auxtext'].forEach(elementType => {
        console.log(`🎛️ ${subslotId}の${elementType}: 表示状態にリセット (新しいコンテンツのため)`);
        
        // 新しいオーバーレイシステムでオーバーレイを削除して表示状態にする
        if (typeof toggleSubslotElementOverlay === "function") {
          toggleSubslotElementOverlay(subslotId, elementType, false); // falseでオーバーレイ削除=表示
        } else {
          console.warn(`⚠️ toggleSubslotElementOverlay関数が見つかりません`);
        }
      });
    });
    
  // ⏰ 復元後の状態を詳細にログ出力
  setTimeout(() => {
    const o1SubslotElementsAfter = document.querySelectorAll('[id^="slot-o1-sub-"]');
    console.log(`🔍 復元後のO1サブスロット要素数: ${o1SubslotElementsAfter.length}個`);
      
      o1SubslotElementsAfter.forEach(element => {
        const textElements = element.querySelectorAll('.slot-phrase, .slot-text');
        const imageElements = element.querySelectorAll('.slot-image');
        console.log(`📊 ${element.id} 復元後状態:`);
        console.log(`  - テキスト要素数: ${textElements.length}`);
        console.log(`  - 画像要素数: ${imageElements.length}`);
        console.log(`  - 表示状態: display=${getComputedStyle(element).display}`);
        console.log(`  - クラスリスト: ${Array.from(element.classList).join(', ')}`);
        
        textElements.forEach((textEl, idx) => {
          console.log(`  - テキスト${idx + 1}: "${textEl.textContent.substring(0, 50)}..." display=${getComputedStyle(textEl).display}`);
        });
      });
    }, 100);
    
    console.log("✅ O1サブスロット表示状態復元完了（復元処理はスキップ）");
  } catch (error) {
    console.error("❌ O1サブスロット表示状態復元に失敗:", error);
  }
}