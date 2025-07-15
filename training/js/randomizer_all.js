
export function randomizeAll(slotData) {
  const groups = [...new Set(slotData.map(entry => entry.V_group_key).filter(v => v))];
  if (groups.length === 0) {
    console.warn("V_group_key 母集団が見つかりません。");
    return [];
  }

  const selectedGroup = groups[Math.floor(Math.random() * groups.length)];
  console.log(`🟢 選択 V_group_key: ${selectedGroup}`);

  const groupSlots = slotData.filter(entry => entry.V_group_key === selectedGroup);
  const exampleIDs = [...new Set(groupSlots.map(entry => entry.例文ID).filter(id => id))];

  if (exampleIDs.length === 0) {
    console.warn("例文ID 母集団が見つかりません。");
    return [];
  }

  let slotSets = [];
  exampleIDs.forEach((id, index) => {
    const setNumber = index + 1;
    const slots = groupSlots.filter(entry => entry.例文ID === id && !entry.SubslotID).map(entry => ({
      ...entry,
      識別番号: `${entry.Slot}-${setNumber}`
    }));
    slotSets.push(slots);
  });

  let selectedSlots = [];
  const slotTypes = [...new Set(groupSlots.map(entry => entry.Slot).filter(s => s))];
  
  slotTypes.forEach(type => {
    if (type === "O1") return;
    
    let candidates = slotSets.flat().filter(entry => entry.Slot === type);
    
    // 🎲 空スロット選択肢を追加（「案2」実装）
    // ただし、疑問詞スロットは例外：疑問詞グループでは必ず疑問詞を表示する
    const hasWhWordInType = candidates.some(c => c.QuestionType === 'wh-word');
    const totalExampleCount = exampleIDs.length;
    const slotExampleCount = [...new Set(candidates.map(c => c.例文ID))].length;
    if (slotExampleCount < totalExampleCount && !hasWhWordInType) {
      // 空スロットを表現する仮想エントリを追加
      candidates.push({
        Slot: type,
        SlotPhrase: "",
        SlotText: "",
        例文ID: "EMPTY_SLOT",
        V_group_key: selectedGroup,
        識別番号: `${type}-EMPTY`
      });
      console.log(`🎲 ${type}スロットに空選択肢を追加（${slotExampleCount}/${totalExampleCount}例文にのみ存在）`);
    } else if (hasWhWordInType) {
      console.log(`🔒 ${type}スロット: 疑問詞を含むため空選択肢は追加しません`);
    }
    
    // �🎯 疑問詞競合回避ロジック
    if (candidates.some(c => c.QuestionType === 'wh-word')) {
      const alreadyHasWhWord = selectedSlots.some(s => s.QuestionType === 'wh-word');
      if (alreadyHasWhWord) {
        // 既に疑問詞が選択済みなら、非疑問詞のみ選択候補にする
        candidates = candidates.filter(c => c.QuestionType !== 'wh-word');
        console.log(`🔒 疑問詞競合回避: ${type}スロットから疑問詞を除外`);
      } else {
        console.log(`✅ 疑問詞選択可能: ${type}スロット`);
      }
    }
    
    if (candidates.length > 0) {
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      
      // 🎲 空スロットが選択された場合の処理
      if (chosen.例文ID === "EMPTY_SLOT") {
        console.log(`🎯 ${type}スロット: 空選択肢が選ばれました（スロットなし）`);
        // 空スロットの場合は何も追加しない（スキップ）
        return;
      }
      
      selectedSlots.push({ ...chosen });
      
      // 疑問詞が選択された場合のログ
      if (chosen.QuestionType === 'wh-word') {
        console.log(`🎯 疑問詞選択: ${chosen.SlotPhrase} (${chosen.Slot})`);
      }
      
      const relatedSubslots = groupSlots.filter(e =>
        e.例文ID === chosen.例文ID &&
        e.Slot === chosen.Slot &&
        e.SubslotID
      );
      relatedSubslots.forEach(sub => {
        selectedSlots.push({ ...sub });
      });
    }
  });

  const o1Entries = groupSlots.filter(e => e.Slot === "O1");
  const uniqueOrders = [...new Set(o1Entries.map(e => e.Slot_display_order))];

  if (uniqueOrders.length > 1) {
    // 🔍 同一例文内でのO1複数順序チェック
    const hasSameExampleMultipleOrders = o1Entries.some(entry => {
      const sameExampleO1s = o1Entries.filter(e => e.例文ID === entry.例文ID);
      const ordersInSameExample = [...new Set(sameExampleO1s.map(e => e.Slot_display_order))];
      return ordersInSameExample.length > 1;
    });
    
    if (hasSameExampleMultipleOrders) {
      // 分離疑問詞構文：同一例文内の複数順序O1を全て選択
      console.log("🔄 分離疑問詞構文検出: 複数O1を選択");
      uniqueOrders.forEach(order => {
        const targets = o1Entries.filter(e => e.Slot_display_order === order);
        targets.forEach(t => selectedSlots.push({ ...t }));
      });
    } else {
      // 異なる例文由来のO1混在：1つだけランダム選択
      console.log("🔄 異なる例文のO1混在検出: 1つだけ選択");
      const chosen = o1Entries[Math.floor(Math.random() * o1Entries.length)];
      selectedSlots.push({ ...chosen });
      const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
      subslots.forEach(sub => selectedSlots.push({ ...sub }));
    }
  } else if (o1Entries.length > 0) {
    const clauseO1 = o1Entries.filter(e => e.PhraseType === "clause");
    if (clauseO1.length > 0) {
      const chosen = clauseO1[Math.floor(Math.random() * clauseO1.length)];
      selectedSlots.push({ ...chosen });
      const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
      subslots.forEach(sub => selectedSlots.push({ ...sub }));
    } else {
      const wordO1 = o1Entries.filter(e => e.PhraseType !== "clause");
      if (wordO1.length > 0) {
        const chosen = wordO1[Math.floor(Math.random() * wordO1.length)];
        selectedSlots.push({ ...chosen });
        const subslots = groupSlots.filter(e => e.例文ID === chosen.例文ID && e.Slot === chosen.Slot && e.SubslotID);
        subslots.forEach(sub => selectedSlots.push({ ...sub }));
      }
    }
  }

  window.slotSets = slotSets;
  window.slotTypes = slotTypes;
  window.lastSelectedSlots = selectedSlots;

  // === 個別ランダマイズ用: 完全なスロットプールを保存 ===
  // 選択されたV_group_keyの全スロットデータ（メイン+サブスロット）を保存
  window.fullSlotPool = groupSlots.map(slot => ({ ...slot }));
  console.log(`💾 個別ランダマイズ用データプール保存完了: ${window.fullSlotPool.length}件`);
  console.log(`💾 V_group_key "${selectedGroup}" の全スロットデータを保存しました`);

  // 疑問文判定と句読点付与
  function detectQuestionPattern(selectedSlots) {
    // Slot_display_order順にソート
    const sortedSlots = selectedSlots.filter(slot => !slot.SubslotID)
      .sort((a, b) => (a.Slot_display_order || 0) - (b.Slot_display_order || 0));
    if (sortedSlots.length === 0) return false;
    // 上位2スロットを判定
    const upperSlots = sortedSlots.slice(0, 2);
    for (const slot of upperSlots) {
      if (slot.QuestionType === 'wh-word') return true;
      const text = (slot.SlotText || "").toLowerCase().trim();
      if (text === "do" || text === "does" || text === "did") return true;
    }
    return false;
  }
  const isQuestionSentence = detectQuestionPattern(selectedSlots);
  const punctuation = isQuestionSentence ? "?" : ".";
  
  // 最後のメインスロットを特定
  const mainSlots = selectedSlots.filter(slot => !slot.SubslotID);
  let lastMainSlotIndex = -1;
  if (mainSlots.length > 0) {
    const lastOrder = Math.max(...mainSlots.map(s => s.Slot_display_order || 0));
    lastMainSlotIndex = selectedSlots.findIndex(s => !s.SubslotID && (s.Slot_display_order || 0) === lastOrder);
  }

  return selectedSlots.map((slot, idx) => {
    let phrase = slot.SlotPhrase || "";
    // 最後のメインスロットのみ句読点をSlotPhraseに付与（英語例文テキストのみ）
    if (idx === lastMainSlotIndex && phrase) {
      phrase = phrase + punctuation;
    }
    return {
      Slot: slot.Slot || "",
      SlotPhrase: phrase,
      SlotText: slot.SlotText || "",
      Slot_display_order: slot.Slot_display_order || 0,
      PhraseType: slot.PhraseType || "",
      SubslotID: slot.SubslotID || "",
      SubslotElement: slot.SubslotElement || "",
      SubslotText: slot.SubslotText || "",
      display_order: slot.display_order || 0,
      識別番号: slot.識別番号 || ""
    };
  });
}
