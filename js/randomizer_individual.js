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
    const allEntries = window.slotSets.flat();
    const matchingEntry = allEntries.find(entry => 
      entry.Slot_display_order == displayOrder
    );
    if (matchingEntry && matchingEntry.V_group_key) {
      return matchingEntry.V_group_key;
    }
  }

  // フォールバック：window.slotSetsから最初のV_group_keyを取得
  if (window.slotSets && window.slotSets.length > 0) {
    const allEntries = window.slotSets.flat();
    const entryWithVGroupKey = allEntries.find(entry => entry.V_group_key);
    return entryWithVGroupKey ? entryWithVGroupKey.V_group_key : null;
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
  console.log("🔍 Sスロット候補の検索開始");
  
  // window.slotSetsを平坦化
  const allEntries = window.slotSets.flat();
  console.log(`全エントリ数: ${allEntries.length}`);
  
  // V_group_keyでフィルタ
  const sameVGroupEntries = allEntries.filter(entry => entry.V_group_key === currentVGroupKey);
  console.log(`同じV_group_key (${currentVGroupKey}) のエントリ数: ${sameVGroupEntries.length}`, sameVGroupEntries);
  
  // Sスロットのみでフィルタ
  const sSlotEntries = sameVGroupEntries.filter(entry => entry.Slot === "S");
  console.log(`Sスロットエントリ数: ${sSlotEntries.length}`, sSlotEntries);
  
  // メインSスロット（SubslotIDなし）のみでフィルタ
  const mainSSlotEntries = sSlotEntries.filter(entry => !entry.SubslotID);
  console.log(`メインSスロットエントリ数: ${mainSSlotEntries.length}`, mainSSlotEntries);
  
  // 現在のSスロット内容と比較
  console.log(`現在のSスロット内容: "${currentSContent}"`);
  
  const candidates = mainSSlotEntries.filter(entry => {
    const entryContent = (entry.SlotPhrase || '') + (entry.SlotText || '');
    console.log(`エントリ内容: "${entryContent}" vs 現在: "${currentSContent}"`);
    const isDifferent = entryContent !== currentSContent;
    const isNotEmpty = entryContent.trim() !== '';
    console.log(`異なる: ${isDifferent}, 空でない: ${isNotEmpty}`);
    return isDifferent && isNotEmpty;
  });
  
  console.log(`最終的なSスロット候補数: ${candidates.length}`, candidates);
  
  if (candidates.length === 0) {
    console.warn("⚠️ 現在表示中以外のSスロット候補が見つかりません");
    return;
  }
  
  console.log(`📊 利用可能なSスロット候補: ${candidates.length}個`, candidates);
  
  // ランダムに1つ選択
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 同じV_group_key内のSサブスロットもランダム選択
  console.log("🔍 Sサブスロット候補の検索開始");
  
  const allSSubslots = allEntries.filter(e => {
    console.log(`エントリチェック: Slot=${e.Slot}, V_group_key=${e.V_group_key}, SubslotID=${e.SubslotID}, SubslotElement="${e.SubslotElement}"`);
    return e.Slot === "S" &&
           e.V_group_key === currentVGroupKey && // 同じV_group_keyのみ
           e.SubslotID &&
           e.SubslotElement &&
           e.SubslotElement.trim() !== "";
  });
  
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
  
  // 手動で静的スロットも更新
  updateStaticSSlot(chosen);
  
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
  // Sスロットのclass="slot"とdata-display-orderでフィルタ
  const existingSSlots = Array.from(dynamicArea.children).filter(el => {
    if (el.classList.contains('slot') && el.dataset.displayOrder) {
      // Sスロットかどうかを確認（structure_builder.jsと同じロジック）
      return sSlotData.some(item => 
        !item.SubslotID && 
        item.Slot === "S" && 
        item.Slot_display_order == el.dataset.displayOrder
      );
    }
    if (el.classList.contains('subslot')) {
      // Sサブスロットかどうかを確認
      return sSlotData.some(item => 
        item.SubslotID && 
        item.Slot === "S"
      );
    }
    return false;
  });
  
  existingSSlots.forEach(el => el.remove());
  console.log(`🗑️ 既存のSスロット要素を削除: ${existingSSlots.length}個`);

  // 新しいSスロットデータを動的記載エリアに追加（structure_builder.jsのrenderSlot/renderSubslot方式）
  sSlotData.forEach(item => {
    if (!item.SubslotID) {
      // メインSスロット - structure_builder.jsのrenderSlot関数と同様
      if (typeof window.renderSlot === 'function') {
        const slotDiv = window.renderSlot(item);
        dynamicArea.appendChild(slotDiv);
        console.log(`📝 renderSlotでメインSスロット追加: ${item.SlotPhrase || ''} / ${item.SlotText || ''}`);
      } else {
        // フォールバック：手動でSスロット要素を作成
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
        
        dynamicArea.appendChild(slotDiv);
        console.log(`📝 手動でメインSスロット追加: ${item.SlotPhrase || ''} / ${item.SlotText || ''}`);
      }
    } else {
      // サブスロット - structure_builder.jsのrenderSubslot関数と同様
      if (typeof window.renderSubslot === 'function') {
        const subDiv = window.renderSubslot(item);
        dynamicArea.appendChild(subDiv);
        console.log(`📝 renderSubslotでサブスロット追加: s-${item.SubslotID} = ${item.SubslotElement || ''}`);
      } else {
        // フォールバック：手動でサブスロット要素を作成
        const subDiv = document.createElement('div');
        subDiv.className = 'subslot';
        if (item.SubslotID) {
          subDiv.id = `slot-${item.Slot.toLowerCase()}-sub-${item.SubslotID.toLowerCase()}`;
        }
        if (typeof item.display_order !== 'undefined') {
          subDiv.dataset.displayOrder = item.display_order;
        }

        const subElDiv = document.createElement('div');
        subElDiv.className = 'subslot-element';
        subElDiv.innerText = item.SubslotElement || '';

        const subTextDiv = document.createElement('div');
        subTextDiv.className = 'subslot-text';
        subTextDiv.innerText = item.SubslotText || '';

        subDiv.appendChild(subElDiv);
        subDiv.appendChild(subTextDiv);
        
        dynamicArea.appendChild(subDiv);
        console.log(`📝 手動でサブスロット追加: s-${item.SubslotID} = ${item.SubslotElement || ''} / ${item.SubslotText || ''}`);
      }
    }
  });
  
  console.log("✅ Sスロット更新完了");
}

/**
 * 静的Sスロットを直接更新
 * @param {Object} sSlotData - 選択されたSスロットデータ
 */
function updateStaticSSlot(sSlotData) {
  console.log("🔄 静的Sスロット更新開始", sSlotData);
  
  const staticSSlot = document.getElementById('slot-s');
  if (!staticSSlot) {
    console.warn("⚠️ 静的Sスロットが見つかりません");
    return;
  }
  
  // 既存の内容をクリア
  const phraseDiv = staticSSlot.querySelector('.slot-phrase');
  const textDiv = staticSSlot.querySelector('.slot-text');
  
  if (phraseDiv) phraseDiv.textContent = '';
  if (textDiv) textDiv.textContent = '';
  
  // 新しいデータを設定
  if (sSlotData.PhraseType === 'word') {
    if (phraseDiv) phraseDiv.textContent = sSlotData.SlotPhrase || '';
    if (textDiv) textDiv.textContent = sSlotData.SlotText || '';
    console.log(`📝 静的Sスロット更新: "${sSlotData.SlotPhrase}" / "${sSlotData.SlotText}"`);
  } else {
    // マーク表示の場合
    if (phraseDiv) phraseDiv.textContent = '▶';
    if (textDiv) textDiv.textContent = '';
    console.log(`📝 静的Sスロットをマーク表示に更新`);
  }
  
  console.log("✅ 静的Sスロット更新完了");
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
