/**
 * Sスロット個別ランダマイザー
 * randomizer_all.js と structure_builder.js を完全コピーしてSスロット専用に改造
 */

/**
 * randomizer_all.jsの完全コピー版でSスロットのみに限定
 */
function randomizeSlotSIndividual() {
  console.log("🎲🎯 Sスロット個別ランダマイズ開始（完全コピー版）");
  
  // 現在のwindow.lastSelectedSlotsから既存データを取得
  if (!window.lastSelectedSlots || !Array.isArray(window.lastSelectedSlots)) {
    console.warn("⚠️ window.lastSelectedSlotsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  // 現在のV_group_keyを取得（randomizer_all.jsのように）
  const firstSlot = window.lastSelectedSlots[0];
  const selectedGroup = firstSlot.V_group_key;
  console.log(`🔑 現在のV_group_key: ${selectedGroup}`);
  
  // window.slotSetsから候補を取得（randomizer_all.jsと同じ）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません");
    return;
  }
  
  // Sスロットのみを対象とする（randomizer_all.jsのslotTypes.forEach部分をSのみに限定）
  const candidates = window.slotSets.flat().filter(entry => entry.Slot === "S");
  if (candidates.length === 0) {
    console.warn("⚠️ Sスロット候補が見つかりません");
    return;
  }
  
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 既存のlastSelectedSlotsからSスロット関連を削除
  const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
  
  // 新しいSスロットを追加
  filteredSlots.push({ ...chosen });
  
  // 関連サブスロットを追加（randomizer_all.jsと同じ方法）
  const allSlots = window.slotSets.flat();
  const relatedSubslots = allSlots.filter(e =>
    e.例文ID === chosen.例文ID &&
    e.Slot === chosen.Slot &&
    e.SubslotID
  );
  relatedSubslots.forEach(sub => {
    filteredSlots.push({ ...sub });
  });
  
  // lastSelectedSlotsを更新
  window.lastSelectedSlots = filteredSlots;
  
  // structure_builder.jsのbuildStructureを呼び出す
  import('./structure_builder.js').then(module => {
    module.buildStructure(window.lastSelectedSlots);
  });
  
  // 静的エリアとの同期
  if (typeof syncDynamicToStatic === "function") {
    syncDynamicToStatic();
    console.log("🔄 静的エリアとの同期完了");
  }
  
  console.log("✅ Sスロット個別ランダマイズ完了（完全コピー版）");
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

console.log("✅ Sスロット個別ランダマイザー読み込み完了（完全コピー版）");