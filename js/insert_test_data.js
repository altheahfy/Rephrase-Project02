
// insert_test_data.js をベースにした動的記載エリアから静的DOM同期用スクリプト

function syncAllSlotsFromJson(data) {
  console.log("🔄 全スロット同期開始");

  // 上位スロット処理
  data.filter(item =>
    (item.SubslotID === "" || item.SubslotID === undefined) &&
    item.PhraseType === "word"
  ).forEach(item => {
    const id = "slot-" + item.Slot.toLowerCase();
    const container = document.getElementById(id);
    if (!container) {
      console.warn(`⚠ 上位スロットが見つかりません: ${id}`);
      return;
    }
    const phraseDiv = container.querySelector(".slot-phrase");
    const textDiv = container.querySelector(".slot-text");
    if (phraseDiv) phraseDiv.textContent = item.SlotPhrase || "";
    if (textDiv) textDiv.textContent = item.SlotText || "";
    console.log(`✅ 上位スロット書き込み: ${id}`);
  });

  // サブスロット処理
  data.filter(item =>
    item.SubslotID && item.SubslotID.trim() !== ""
  ).forEach(item => {
    const id = `slot-${item.Slot.toLowerCase()}-sub-${item.SubslotID.toLowerCase()}`;
    const container = document.getElementById(id);
    if (!container) {
      console.warn(`⚠ サブスロットが見つかりません: ${id}`);
      return;
    }
    const phraseDiv = container.querySelector(".slot-phrase, .subslot-element");
    const textDiv = container.querySelector(".slot-text, .subslot-text");
    if (phraseDiv) phraseDiv.textContent = item.SlotPhrase || item.SubslotElement || "";
    if (textDiv) textDiv.textContent = item.SlotText || item.SubslotText || "";
    console.log(`✅ サブスロット書き込み: ${id}`);
  });
}

// DisplayAtTop に対応する疑問詞をページ上部に表示（オプション）
window.addEventListener('load', () => {
  if (window.loadedJsonData) {
    syncAllSlotsFromJson(window.loadedJsonData);

    const topDisplayItem = window.loadedJsonData.find(d => d.DisplayAtTop);
    if (topDisplayItem && topDisplayItem.DisplayText) {
      const topDiv = document.getElementById("display-top-question-word");
      if (topDiv) {
        topDiv.textContent = topDisplayItem.DisplayText;
        console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
      } else {
        console.warn("⚠ display-top-question-word が見つかりません");
      }
    }
  } else {
    console.warn("⚠ window.loadedJsonData が存在しません");
  }
});
