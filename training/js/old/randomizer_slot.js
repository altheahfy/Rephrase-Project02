// randomizer_slot.js - 個別スロット専用ランダマイザ

/**
 * 特定のスロットの内容だけをランダマイズ
 * @param {string} slotId - ランダマイズ対象のスロットID (例: "m1", "s", "o1"など)
 * @param {Array} jsonData - 利用可能なJSONデータ
 */
function randomizeSingleSlot(slotId, jsonData) {
  if (!jsonData || !Array.isArray(jsonData) || jsonData.length === 0) {
    console.warn("ランダマイズに利用できるJSONデータがありません");
    return;
  }

  // 対象スロットのデータだけをフィルタ
  let slotData = jsonData.filter(item => 
    item.Slot && item.Slot.toLowerCase() === slotId.toLowerCase() && !item.SubslotID
  );
  
  // 🆕 現在の V_group_key に制限
  if (window.currentRandomizedState && window.currentRandomizedState.vGroupKey) {
    const currentVGroupKey = window.currentRandomizedState.vGroupKey;
    slotData = slotData.filter(item => item.V_group_key === currentVGroupKey);
    console.log(`🎯 現在のV_group_key「${currentVGroupKey}」に制限して検索`);
  }
  
  if (slotData.length === 0) {
    console.warn(`スロット ${slotId} のデータがJSONに見つかりません（V_group_key制限後）`);
    return;
  }
  
  // ランダムに1つ選択
  const randomIndex = Math.floor(Math.random() * slotData.length);
  const selectedData = slotData[randomIndex];
  
  console.log(`🎲 スロット ${slotId} をランダマイズ:`, selectedData);
  
  // DOMに適用
  const slotContainer = document.getElementById(`slot-${slotId.toLowerCase()}`);
  if (!slotContainer) {
    console.warn(`スロットコンテナ #slot-${slotId.toLowerCase()} が見つかりません`);
    return;
  }
  
  // 要素を更新
  const phraseDiv = slotContainer.querySelector(".slot-phrase");
  const textDiv = slotContainer.querySelector(".slot-text");
  const auxtextDiv = slotContainer.querySelector(".slot-auxtext");
  const imageElem = slotContainer.querySelector(".slot-image");
  
  if (phraseDiv) phraseDiv.textContent = selectedData.SlotPhrase || "";
  if (textDiv) textDiv.textContent = selectedData.SlotText || "";
  if (auxtextDiv) auxtextDiv.textContent = selectedData.SlotAuxtext || "";
  
  // 画像パスが指定されていれば更新
  if (imageElem && selectedData.ImagePath) {
    imageElem.src = selectedData.ImagePath;
  }
  
  console.log(`✅ スロット ${slotId} のランダマイズ完了`);
}

// ページ読み込み完了後にイベントリスナーを設定
document.addEventListener("DOMContentLoaded", () => {
  // 個別スロットのランダマイズボタンにイベントリスナーを追加
  document.querySelectorAll(".slot-container").forEach(container => {
    const slotId = container.id.replace("slot-", "");
    const randomizeBtn = container.querySelector(".slot-randomize");
    
    if (randomizeBtn) {
      randomizeBtn.addEventListener("click", () => {
        console.log(`🎲 ${slotId} のランダマイズボタンがクリックされました`);
        // window.loadedJsonDataがあればそれを使用
        if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
          randomizeSingleSlot(slotId, window.loadedJsonData);
        } else {
          alert("先にJSONデータをロードしてください");
        }
      });
    }
  });
  
  console.log("✅ 個別スロットランダマイズ機能の初期化完了");
});
