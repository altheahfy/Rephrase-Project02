/**
 * 個別ランダマイズ機能
 * 仕様: 各スロット専用ボタンで、そのスロットのみをランダム置換
 * 方針: 動的記載エリア経由でMutationObserver同期、静的DOM直接操作禁止
 */

/**
 * Sスロット個別ランダマイズ
 * window.slotSetsから現在表示中以外のSスロットを選択して置換
 */
function randomizeSlotSIndividual() {
  console.log("🎲 Sスロット個別ランダマイズ開始");
  
  // window.slotSetsの存在確認
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  console.log(`📊 利用可能な例文セット数: ${window.slotSets.length}`);
  
  // 動的記載エリアから現在のSスロット情報を取得
  const dynamicArea = document.getElementById('dynamic-slot-area');
  if (!dynamicArea) {
    console.warn("⚠️ dynamic-slot-areaが見つかりません");
    return;
  }
  
  // 現在のSスロット要素を探す
  const currentSSlot = dynamicArea.querySelector('[data-slot="S"]');
  let currentSContent = null;
  if (currentSSlot) {
    currentSContent = currentSSlot.textContent.trim();
    console.log(`📄 現在のSスロット内容: "${currentSContent}"`);
  }
  
  // 全スロットデータを平坦化
  const allSlots = window.slotSets.flat();
  
  // Sスロット候補を抽出（現在表示中以外）
  const candidates = allSlots.filter(entry => 
    entry.Slot === "S" && 
    entry.Content !== currentSContent && // 内容が異なるもの
    entry.Content && entry.Content.trim() !== "" // 空でないもの
  );
  
  if (candidates.length === 0) {
    console.warn("⚠️ 現在表示中以外のSスロット候補が見つかりません");
    return;
  }
  
  console.log(`📊 利用可能なSスロット候補: ${candidates.length}個`);
  
  // ランダムに1つ選択
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 関連するサブスロットも取得
  const relatedSubslots = allSlots.filter(e =>
    e.例文ID === chosen.例文ID &&
    e.Slot === chosen.Slot &&
    e.SubslotID
  );
  
  console.log(`📊 関連サブスロット数: ${relatedSubslots.length}個`);
  
  // 動的記載エリアを更新（MutationObserver経由で静的DOMに反映）
  updateDynamicAreaSSlot(chosen, relatedSubslots);
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

/**
 * 動的記載エリアのSスロットを更新
 * @param {Object} mainSSlot - 選択されたメインSスロット
 * @param {Array} subSlots - 関連サブスロット配列
 */
function updateDynamicAreaSSlot(mainSSlot, subSlots) {
  console.log("🔄 動的記載エリアSスロット更新開始");
  
  const dynamicArea = document.getElementById('dynamic-slot-area');
  if (!dynamicArea) {
    console.warn("⚠️ dynamic-slot-areaが見つかりません");
    return;
  }
  
  // メインSスロット要素を探すか作成
  let sSlotElement = dynamicArea.querySelector('[data-slot="S"]');
  if (!sSlotElement) {
    sSlotElement = document.createElement('div');
    sSlotElement.setAttribute('data-slot', 'S');
    dynamicArea.appendChild(sSlotElement);
    console.log("📝 新しいSスロット要素を作成");
  }
  
  // メインSスロットの内容を更新
  sSlotElement.textContent = mainSSlot.Content || '';
  sSlotElement.setAttribute('data-v-group-key', mainSSlot.V_group_key || '');
  sSlotElement.setAttribute('data-phrase-type', mainSSlot.PhraseType || '');
  
  console.log(`📝 メインSスロット更新: "${mainSSlot.Content}"`);
  
  // サブスロットがある場合は更新
  subSlots.forEach(subSlot => {
    const subSlotId = `s-${subSlot.SubslotID}`;
    let subSlotElement = dynamicArea.querySelector(`[data-subslot="${subSlotId}"]`);
    
    if (!subSlotElement) {
      subSlotElement = document.createElement('div');
      subSlotElement.setAttribute('data-subslot', subSlotId);
      dynamicArea.appendChild(subSlotElement);
      console.log(`📝 新しいサブスロット要素を作成: ${subSlotId}`);
    }
    
    subSlotElement.textContent = subSlot.Content || '';
    subSlotElement.setAttribute('data-v-group-key', subSlot.V_group_key || '');
    
    console.log(`📝 サブスロット更新: ${subSlotId} = "${subSlot.Content}"`);
  });
  
  console.log("✅ 動的記載エリアSスロット更新完了");
}

// グローバル関数として公開（静的HTMLボタンから呼び出し用）
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

// デバッグ用ヘルパー関数
window.debugIndividualRandomizer = function() {
  console.log("🔍 個別ランダマイザーデバッグ:");
  console.log("  window.slotSets:", window.slotSets);
  
  const dynamicArea = document.getElementById('dynamic-slot-area');
  if (dynamicArea) {
    const currentSSlot = dynamicArea.querySelector('[data-slot="S"]');
    console.log("  現在のSスロット要素:", currentSSlot);
    if (currentSSlot) {
      console.log("  現在のSスロット内容:", currentSSlot.textContent);
    }
  }
};

console.log("✅ 個別ランダマイザー読み込み完了");