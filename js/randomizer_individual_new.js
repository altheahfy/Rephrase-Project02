/**
 * 個別ランダマイズ機能
 * 特定スロットのみをランダム置換
 * 方針: structure_builder.jsと同じ方法で動的記載エリアに書き込み、MutationObserver同期に任せる
 */

// 🟢 現在のV_group_keyを取得する関数
function getCurrentVGroupKey() {
  // 動的記載エリアから現在表示中のスロットを取得
  const dynamicArea = document.getElementById('dynamic-slot-area');
  if (!dynamicArea) return null;

  const slots = dynamicArea.querySelectorAll('[data-v-group-key]');
  if (slots.length > 0) {
    const vGroupKey = slots[0].dataset.vGroupKey;
    if (vGroupKey) return vGroupKey;
  }

  // データ属性がない場合、window.slotSetsから推測
  const allSlots = dynamicArea.querySelectorAll('[data-display-order]');
  if (allSlots.length > 0 && window.slotSets) {
    const displayOrder = allSlots[0].dataset.displayOrder;
    const matchingEntry = window.slotSets.find(entry => 
      entry.Slot_display_order == displayOrder
    );
    if (matchingEntry && matchingEntry.V_group_key) {
      return matchingEntry.V_group_key;
    }
  }

  // フォールバック：window.slotSetsから最初のV_group_keyを取得
  if (window.slotSets && window.slotSets.length > 0) {
    const firstEntry = window.slotSets.find(entry => entry.V_group_key);
    return firstEntry ? firstEntry.V_group_key : null;
  }

  return null;
}

/**
 * Sスロット個別ランダマイズ
 * window.slotSetsから現在表示中以外のSスロットを選択して置換
 * V_group_key単位で候補を絞り、例文ID依存を排除
 */
function randomizeSlotSIndividual() {
  console.log("🎲 Sスロット個別ランダマイズ開始");
  
  // window.slotSetsの存在確認
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  console.log(`📊 利用可能な例文セット数: ${window.slotSets.length}`);
  
  // 現在のV_group_keyを取得
  const currentVGroupKey = getCurrentVGroupKey();
  if (!currentVGroupKey) {
    console.warn("⚠️ 現在のV_group_keyが特定できませんでした");
    return;
  }
  
  console.log(`🔑 現在のV_group_key: ${currentVGroupKey}`);
  
  // 現在のSスロットを取得（静的DOMから）
  const currentSContainer = document.getElementById('slot-s');
  let currentSContent = '';
  if (currentSContainer) {
    const phraseDiv = currentSContainer.querySelector('.slot-phrase');
    const textDiv = currentSContainer.querySelector('.slot-text');
    currentSContent = (phraseDiv?.textContent || '') + (textDiv?.textContent || '');
  }
  
  console.log(`📄 現在のSスロット内容: "${currentSContent}"`);
  
  // 同じV_group_key内のSスロット候補を抽出（現在表示中以外）
  const candidates = window.slotSets.filter(entry => {
    if (entry.Slot !== "S" || entry.SubslotID) return false; // メインSスロットのみ
    if (entry.V_group_key !== currentVGroupKey) return false; // 同じV_group_keyのみ
    const entryContent = (entry.SlotPhrase || '') + (entry.SlotText || '');
    return entryContent !== currentSContent && entryContent.trim() !== '';
  });
  
  if (candidates.length === 0) {
    console.warn("⚠️ 現在表示中以外のSスロット候補が見つかりません");
    return;
  }
  
  console.log(`📊 利用可能なSスロット候補: ${candidates.length}個`, candidates);
  
  // ランダムに1つ選択
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 同じV_group_key内のSサブスロットもランダム選択
  const allSSubslots = window.slotSets.filter(e =>
    e.Slot === "S" &&
    e.V_group_key === currentVGroupKey && // 同じV_group_keyのみ
    e.SubslotID &&
    e.SubslotElement &&
    e.SubslotElement.trim() !== ""
  );
  
  console.log(`📊 利用可能なSサブスロット候補: ${allSSubslots.length}個`, allSSubslots);
  
  // ランダムでSサブスロットを選択（必要に応じて複数選択も可能）
  const chosenSubslots = [];
  if (allSSubslots.length > 0) {
    // 簡単のため1つだけ選択（後で拡張可能）
    const randomSubslot = allSSubslots[Math.floor(Math.random() * allSSubslots.length)];
    chosenSubslots.push(randomSubslot);
    console.log(`🎯 選択されたSサブスロット:`, randomSubslot);
  }
  
  // Sスロットのみを含む配列を作成してbuildStructureを呼び出し
  const sSlotData = [chosen, ...chosenSubslots];
  updateSSlotOnly(sSlotData);
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

/**
 * Sスロットのみを更新（structure_builder.jsの方式を踏襲）
 * @param {Array} sSlotData - Sスロットデータ（メイン+サブスロット）
 */
function updateSSlotOnly(sSlotData) {
  console.log("🔄 Sスロット更新開始", sSlotData);
  
  // 動的記載エリアを取得または作成（structure_builder.jsと同じ）
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

  // 既存の動的記載エリア内のSスロット要素をクリア
  const existingSSlots = dynamicArea.querySelectorAll('[data-slot="S"], [data-subslot^="s-"]');
  existingSSlots.forEach(el => el.remove());

  // 新しいSスロットデータを動的記載エリアに追加
  sSlotData.forEach(item => {
    if (!item.SubslotID) {
      // メインSスロット
      const slotDiv = document.createElement('div');
      slotDiv.className = 'slot';
      slotDiv.dataset.slot = item.Slot;
      slotDiv.dataset.exampleId = item.Example_ID || '';
      slotDiv.dataset.vGroupKey = item.V_group_key || '';
      slotDiv.dataset.phraseType = item.PhraseType || '';
      slotDiv.dataset.displayOrder = item.Slot_display_order || '';
      
      if (item.PhraseType === 'word') {
        slotDiv.innerHTML = `
          <div class="slot-phrase">${item.SlotPhrase || ''}</div>
          <div class="slot-text">${item.SlotText || ''}</div>
        `;
      } else {
        slotDiv.innerHTML = '<div class="slot-mark">▶</div>';
      }
      
      dynamicArea.appendChild(slotDiv);
      console.log(`📝 メインSスロット追加: ${item.SlotPhrase || ''} / ${item.SlotText || ''}`);
    } else {
      // サブスロット
      const subDiv = document.createElement('div');
      subDiv.className = 'subslot';
      subDiv.dataset.subslot = `s-${item.SubslotID}`;
      subDiv.dataset.exampleId = item.Example_ID || '';
      subDiv.dataset.vGroupKey = item.V_group_key || '';
      subDiv.dataset.displayOrder = item.display_order || '';
      
      subDiv.innerHTML = `
        <div class="subslot-element">${item.SubslotElement || ''}</div>
        <div class="subslot-text">${item.SubslotText || ''}</div>
      `;
      
      dynamicArea.appendChild(subDiv);
      console.log(`📝 サブスロット追加: s-${item.SubslotID} = ${item.SubslotElement || ''} / ${item.SubslotText || ''}`);
    }
  });
  
  console.log("✅ Sスロット更新完了");
}

// グローバル関数として公開（静的HTMLボタンから呼び出し用）
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

// デバッグ用ヘルパー関数
window.debugIndividualRandomizer = function() {
  console.log("🔍 個別ランダマイザーデバッグ:");
  console.log("  window.slotSets:", window.slotSets);
  console.log("  現在のV_group_key:", getCurrentVGroupKey());
  
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
