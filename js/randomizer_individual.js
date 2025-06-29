/**
 * Sスロット個別ランダマイズ
 * 全体ランダマイザーの仕組みをSスロット専用にコピー
 */

/**
 * null や undefined に対してフォールバック値を返す
 */
function safe(value, fallback = "") {
  return value === null || value === undefined ? fallback : value;
}

/**
 * Sスロット個別ランダマイズ
 * 全体ランダマイザーの仕組みをSスロット専用にコピー
 */
function randomizeSlotSIndividual() {
  console.log("🎲 Sスロット個別ランダマイズ開始");
  
  // window.slotSetsの存在確認（全体ランダマイザーから継承）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  // 現在のV_group_keyを取得（全体ランダマイザーと同じ方法）
  const currentVGroupKey = getCurrentVGroupKey();
  if (!currentVGroupKey) {
    console.warn("⚠️ 現在のV_group_keyが特定できませんでした");
    return;
  }
  
  console.log(`🔑 現在のV_group_key: ${currentVGroupKey}`);
  
  // window.slotSetsを平坦化してSスロット候補を抽出（randomizer_all.jsと同じ方法）
  const allEntries = window.slotSets.flat();
  const groupSlots = allEntries.filter(entry => entry.V_group_key === currentVGroupKey);
  
  // Sスロットのメイン候補を抽出（SubslotIDなし）
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
  
  // 選択されたSスロットに関連するサブスロットを取得（randomizer_all.jsと同じ方法）
  const relatedSubslots = groupSlots.filter(e =>
    e.例文ID === chosenSSlot.例文ID &&
    e.Slot === chosenSSlot.Slot &&
    e.SubslotID
  );
  
  console.log(`🎯 関連サブスロット: ${relatedSubslots.length}個`, relatedSubslots);
  
  // 選択されたスロットセットを作成（structure_builder.jsに渡す形式）
  const selectedSlots = [chosenSSlot, ...relatedSubslots];
  
  // structure_builder.jsの仕組みを使って動的記載エリアを更新
  updateSSlotOnly(selectedSlots);
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

/**
 * 現在のV_group_keyを取得（全体ランダマイザーと同じ方法）
 */
function getCurrentVGroupKey() {
  if (window.lastSelectedSlots && window.lastSelectedSlots.length > 0) {
    const firstSlot = window.lastSelectedSlots[0];
    return firstSlot.V_group_key;
  }
  return null;
}

/**
 * Sスロットのみを更新（structure_builder.jsの仕組みを完全コピー）
 */
function updateSSlotOnly(selectedSlots) {
  console.log("🔄 Sスロット更新開始 (structure_builder.jsの仕組みを使用)", selectedSlots);
  
  // structure_builder.jsと同じDOM操作
  let wrapper = document.querySelector('.slot-wrapper');
  if (!wrapper) {
    console.error('slot-wrapper not found, skipping update');
    return;
  }

  let dynamicArea = document.getElementById('dynamic-slot-area');
  if (!dynamicArea) {
    dynamicArea = document.createElement('div');
    dynamicArea.id = 'dynamic-slot-area';
    wrapper.appendChild(dynamicArea);
  }

  // 既存のSスロット関連要素を削除
  const existingSSlots = Array.from(dynamicArea.children).filter(el => {
    return (el.classList.contains('slot') && el.dataset.displayOrder === "2") ||
           (el.classList.contains('subslot') && el.id && el.id.includes('slot-s-sub'));
  });
  
  existingSSlots.forEach(el => el.remove());
  console.log(`🗑️ 既存のSスロット要素を削除: ${existingSSlots.length}個`);

  // structure_builder.jsの処理を完全再現
  const upperSlots = selectedSlots.filter(e => !e.SubslotID);
  
  upperSlots.forEach(item => {
    console.log(`Processing upper slot: ${item.Slot} (PhraseType: ${item.PhraseType})`);

    // structure_builder.jsと同じ条件分岐
    if (item.PhraseType === 'word') {
      const slotDiv = window.renderSlot(item);
      dynamicArea.appendChild(slotDiv);
      console.log(`✅ 上位スロット追加: ${item.Slot} (PhraseType: word)`);
    } else {
      console.log(`🚫 上位スロットスキップ: ${item.Slot} (PhraseType: ${item.PhraseType})`);
    }

    // サブスロットの処理（structure_builder.jsと同じ）
    const subslots = selectedSlots.filter(s =>
      s.Slot === item.Slot &&
      s.SubslotID &&
      s.Slot_display_order === item.Slot_display_order
    );
    subslots.sort((a, b) => a.display_order - b.display_order);

    subslots.forEach(sub => {
      console.log(`Adding subslot to ${item.Slot}: ${sub.SubslotID} (display_order: ${sub.display_order})`);
      const subDiv = window.renderSubslot(sub);
      dynamicArea.appendChild(subDiv);
    });
  });
  
  console.log("✅ Sスロット更新完了 (structure_builder.jsの仕組みを使用)");
}

// グローバル関数として公開
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

// デバッグ: 関数が正しく設定されたか確認
console.log("✅ Sスロット個別ランダマイザー読み込み完了");
console.log("🔍 window.randomizeSlotSIndividual:", typeof window.randomizeSlotSIndividual);
console.log("🔍 function definition:", window.randomizeSlotSIndividual);

// グローバルスコープテスト関数を追加
window.testSRandomizer = function() {
  console.log("🧪 テスト関数が動作しています");
  console.log("🧪 randomizeSlotSIndividual関数:", typeof window.randomizeSlotSIndividual);
  return "テスト成功";
};