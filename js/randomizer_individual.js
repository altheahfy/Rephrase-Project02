/**
 * 個別ランダマイズ機能
 * 特定スロットのみをランダム置換
 * 方針: structure_builder.jsと同じ方法で動的記載エリアに書き込み、MutationObserver同期に任せる
 */

// 🟢 最近使用したスロットの履歴を保持（重複回避用）
let recentSSlotHistory = [];

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
  
  // 現在のSスロット内容と比較（より緩い条件で候補を増やす）
  console.log(`現在のSスロット内容: "${currentSContent}"`);
  
  // 現在表示中のエントリのIDを特定
  const dynamicArea = document.getElementById('dynamic-slot-area');
  let currentExampleID = null;
  if (dynamicArea) {
    const currentSSlot = dynamicArea.querySelector('[data-slot="S"]');
    if (currentSSlot) {
      currentExampleID = currentSSlot.dataset.exampleId;
    }
  }
  console.log(`現在のExample ID: ${currentExampleID}`);
  
  const candidates = mainSSlotEntries.filter(entry => {
    const entryContent = (entry.SlotPhrase || '') + (entry.SlotText || '');
    const isNotEmpty = entryContent.trim() !== '';
    
    // IDベースでの除外（より確実）
    const isDifferentByID = !currentExampleID || entry.Example_ID !== currentExampleID;
    
    // コンテンツベースでの除外（フォールバック）
    const isDifferentByContent = entryContent !== currentSContent;
    
    // 最近使用した履歴での除外（多様性向上）
    const isNotInRecentHistory = !recentSSlotHistory.includes(entry.Example_ID);
    
    const isCandidate = isNotEmpty && (isDifferentByID || isDifferentByContent) && isNotInRecentHistory;
    
    console.log(`エントリ ${entry.Example_ID}: "${entryContent}"`, {
      isNotEmpty,
      isDifferentByID,
      isDifferentByContent,
      isNotInRecentHistory,
      isCandidate
    });
    
    return isCandidate;
  });
  
  // もし履歴フィルタで候補がなくなった場合、履歴を無視して再試行
  let finalCandidates = candidates;
  if (candidates.length === 0) {
    console.log("📝 履歴フィルタで候補がゼロになったため、履歴を無視して再試行");
    finalCandidates = mainSSlotEntries.filter(entry => {
      const entryContent = (entry.SlotPhrase || '') + (entry.SlotText || '');
      const isNotEmpty = entryContent.trim() !== '';
      const isDifferentByID = !currentExampleID || entry.Example_ID !== currentExampleID;
      const isDifferentByContent = entryContent !== currentSContent;
      return isNotEmpty && (isDifferentByID || isDifferentByContent);
    });
  }
  
  console.log(`最終的なSスロット候補数: ${finalCandidates.length}`, finalCandidates);
  
  if (finalCandidates.length === 0) {
    console.warn("⚠️ 現在表示中以外のSスロット候補が見つかりません");
    return;
  }
  
  console.log(`📊 利用可能なSスロット候補: ${finalCandidates.length}個`, finalCandidates);
  
  // ランダムに1つ選択
  const chosen = finalCandidates[Math.floor(Math.random() * finalCandidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 履歴に追加（最大5個まで保持）
  recentSSlotHistory.push(chosen.Example_ID);
  if (recentSSlotHistory.length > 5) {
    recentSSlotHistory.shift(); // 古いものから削除
  }
  console.log(`📚 更新された履歴:`, recentSSlotHistory);
  
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
  
  // 少し遅延させて再度確認
  setTimeout(() => {
    console.log("🔍 200ms後の静的スロット確認");
    const staticSSlot = document.getElementById('slot-s');
    if (staticSSlot) {
      const phraseDiv = staticSSlot.querySelector('.slot-phrase');
      const textDiv = staticSSlot.querySelector('.slot-text');
      console.log("  phraseDiv内容:", phraseDiv?.textContent);
      console.log("  textDiv内容:", textDiv?.textContent);
      console.log("  期待値 phrase:", chosen.SlotPhrase);
      console.log("  期待値 text:", chosen.SlotText);
      
      // 内容が期待値と異なる場合、再度更新を試行
      if (phraseDiv?.textContent !== (chosen.SlotPhrase || '') || 
          textDiv?.textContent !== (chosen.SlotText || '')) {
        console.log("⚠️ 静的スロットが期待値と異なります。再更新を実行します。");
        updateStaticSSlot(chosen);
      }
    }
  }, 200);
  
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
  console.log("🔍 既存Sスロット要素の削除開始");
  console.log("動的記載エリア内の全要素:", dynamicArea.children);
  
  // より確実な方法：Sスロット関連の全要素を削除
  const existingSSlots = Array.from(dynamicArea.children).filter(el => {
    // display-order="2" のスロット要素（Sスロットの位置）を削除
    if (el.classList.contains('slot') && el.dataset.displayOrder === "2") {
      console.log("🎯 削除対象のSスロット要素を発見:", el);
      return true;
    }
    
    // ID にs-sub を含むサブスロット要素を削除
    if (el.classList.contains('subslot') && el.id && el.id.includes('slot-s-sub')) {
      console.log("🎯 削除対象のSサブスロット要素を発見:", el);
      return true;
    }
    
    return false;
  });
  
  console.log(`🔍 削除対象要素数: ${existingSSlots.length}`, existingSSlots);
  existingSSlots.forEach((el, index) => {
    console.log(`🗑️ 削除 ${index + 1}: ${el.className}, id: ${el.id}, display-order: ${el.dataset.displayOrder}`);
    el.remove();
  });
  
  console.log(`🗑️ 既存のSスロット要素を削除: ${existingSSlots.length}個`);

  // 新しいSスロットデータを動的記載エリアに追加（structure_builder.jsの方式を完全に踏襲）
  console.log("📝 新しいSスロット要素の追加開始");
  
  sSlotData.forEach(item => {
    console.log("📝 処理中のアイテム:", item);
    
    if (!item.SubslotID) {
      // メインSスロット - structure_builder.jsの条件と同じ
      console.log(`📝 メインSスロット処理: PhraseType=${item.PhraseType}`);
      
      // structure_builder.jsと同じ動作：常にスロットを作成し、PhraseTypeに応じて内容を切り替え
      console.log(`📝 メインSスロット追加: PhraseType=${item.PhraseType}`);
      
      if (typeof window.renderSlot === 'function') {
        const slotDiv = window.renderSlot(item);
        
        // 適切な位置に挿入（display-orderに基づく）
        const existingSlots = Array.from(dynamicArea.children).filter(el => 
          el.classList.contains('slot') && el.dataset.displayOrder
        );
        
        let inserted = false;
        for (const existingSlot of existingSlots) {
          if (parseInt(existingSlot.dataset.displayOrder) > parseInt(item.Slot_display_order)) {
            dynamicArea.insertBefore(slotDiv, existingSlot);
            inserted = true;
            break;
          }
        }
        
        if (!inserted) {
          dynamicArea.appendChild(slotDiv);
        }
        
        console.log(`📝 renderSlotでメインSスロット追加: ${item.SlotPhrase || ''} / ${item.SlotText || ''} (${item.PhraseType})`, slotDiv);
      } else {
        // フォールバック：手動でSスロット要素を作成
        const slotDiv = document.createElement('div');
        slotDiv.className = 'slot';
        slotDiv.dataset.slot = 'S';
        slotDiv.dataset.displayOrder = item.Slot_display_order;
        slotDiv.dataset.exampleId = item.Example_ID;
        slotDiv.dataset.vGroupKey = item.V_group_key;
        
        if (item.PhraseType === 'word') {
          // wordタイプ：テキスト表示
          const phraseDiv = document.createElement('div');
          phraseDiv.className = 'slot-phrase';
          phraseDiv.innerText = item.SlotPhrase || '';

          const textDiv = document.createElement('div');
          textDiv.className = 'slot-text';
          textDiv.innerText = item.SlotText || '';

          slotDiv.appendChild(phraseDiv);
          slotDiv.appendChild(textDiv);
        } else {
          // clause/phraseタイプ：マーク表示
          const markDiv = document.createElement('div');
          markDiv.className = 'slot-mark';
          markDiv.innerText = '▶';
          slotDiv.appendChild(markDiv);
        }
        
        dynamicArea.appendChild(slotDiv);
        console.log(`📝 手動でメインSスロット追加: ${item.SlotPhrase || ''} / ${item.SlotText || ''} (${item.PhraseType})`, slotDiv);
      }
      
      // サブスロットボタンのバインド（clause/phraseタイプの場合に必要）
      if (item.PhraseType === 'clause' || item.PhraseType === 'phrase') {
        if (typeof window.bindSubslotToggleButtons === "function") {
          window.bindSubslotToggleButtons();
        }
      }
    } else {
      // サブスロット - structure_builder.jsのrenderSubslot関数と同様
      console.log(`📝 サブスロット追加: ${item.SubslotID} = ${item.SubslotElement || ''}`);
      
      if (typeof window.renderSubslot === 'function') {
        const subDiv = window.renderSubslot(item);
        dynamicArea.appendChild(subDiv);
        console.log(`📝 renderSubslotでサブスロット追加: s-${item.SubslotID} = ${item.SubslotElement || ''}`, subDiv);
      } else {
        // フォールバック：手動でサブスロット要素を作成
        const subDiv = document.createElement('div');
        subDiv.className = 'subslot';
        subDiv.id = `slot-s-sub-${item.SubslotID}`;
        if (typeof item.display_order !== 'undefined') {
          subDiv.dataset.displayOrder = item.display_order;
        }
        
        const phraseDiv = document.createElement('div');
        phraseDiv.className = 'slot-phrase';
        phraseDiv.textContent = item.SubslotElement || '';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'slot-text';
        textDiv.textContent = item.SubslotText || '';
        
        subDiv.appendChild(phraseDiv);
        subDiv.appendChild(textDiv);
        dynamicArea.appendChild(subDiv);
        console.log(`📝 手動でサブスロット追加: s-${item.SubslotID} = ${item.SubslotElement || ''} / ${item.SubslotText || ''}`, subDiv);
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
  console.log("🔍 静的Sスロット要素:", staticSSlot);
  
  if (!staticSSlot) {
    console.warn("⚠️ 静的Sスロットが見つかりません");
    return;
  }
  
  // 既存の内容を確認
  const phraseDiv = staticSSlot.querySelector('.slot-phrase');
  const textDiv = staticSSlot.querySelector('.slot-text');
  
  console.log("🔍 phraseDiv要素:", phraseDiv);
  console.log("🔍 textDiv要素:", textDiv);
  console.log("🔍 現在のphraseDiv内容:", phraseDiv?.textContent);
  console.log("🔍 現在のtextDiv内容:", textDiv?.textContent);
  
  // 既存の内容をクリア
  if (phraseDiv) {
    console.log("🧹 phraseDiv をクリア");
    phraseDiv.textContent = '';
  }
  if (textDiv) {
    console.log("🧹 textDiv をクリア");
    textDiv.textContent = '';
  }
  
  // 新しいデータを設定
  console.log("📝 新しいデータ設定開始");
  console.log("  PhraseType:", sSlotData.PhraseType);
  console.log("  SlotPhrase:", sSlotData.SlotPhrase);
  console.log("  SlotText:", sSlotData.SlotText);
  
  // PhraseTypeに基づく表示制御
  if (sSlotData.PhraseType === 'word') {
    // wordタイプ：テキスト表示
    if (phraseDiv) {
      phraseDiv.textContent = sSlotData.SlotPhrase || '';
      console.log(`✅ phraseDiv更新完了: "${phraseDiv.textContent}"`);
    }
    if (textDiv) {
      textDiv.textContent = sSlotData.SlotText || '';
      console.log(`✅ textDiv更新完了: "${textDiv.textContent}"`);
    }
    console.log(`📝 静的Sスロット更新 (${sSlotData.PhraseType}): "${sSlotData.SlotPhrase}" / "${sSlotData.SlotText}"`);
  } else {
    // clause/phraseタイプ：静的スロットは空のまま（実際のコンテンツはサブスロットエリアに表示される）
    if (phraseDiv) {
      phraseDiv.textContent = '';
      console.log(`✅ phraseDiv 空に設定完了`);
    }
    if (textDiv) {
      textDiv.textContent = '';
      console.log(`✅ textDiv 空に設定完了`);
    }
    console.log(`📝 静的Sスロットを空に設定 (PhraseType: ${sSlotData.PhraseType})`);
  }
  
  // 更新後の確認
  console.log("🔍 更新後のphraseDiv内容:", phraseDiv?.textContent);
  console.log("🔍 更新後のtextDiv内容:", textDiv?.textContent);
  
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
