/**
 * Sスロット個別ランダマイザー
 */

/**
 * Sスロット個別ランダマイズ関数
 */
function randomizeSlotSIndividual() {
  console.log("🎲🎯 Sスロット個別ランダマイズ開始");
  
  // slotSetsの存在確認
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    alert("エラー: 先に全体ランダマイズを実行してください。");
    return;
  }
  
  // lastSelectedSlotsの存在確認
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。");
    alert("エラー: 現在の選択データが見つかりません。");
    return;
  }
  
  // slotSetsからSスロット候補を取得
  const sCandidates = window.slotSets.flat().filter(entry => entry.Slot === "S" && !entry.SubslotID);
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
  const relatedSubslots = window.loadedJsonData.filter(entry =>
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
  if (typeof syncDynamicToStatic === "function") {
    syncDynamicToStatic();
    console.log("🔄 静的エリアとの同期完了");
  }
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

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