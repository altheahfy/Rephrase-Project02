
// insert_test_data.js をベースにした動的記載エリアから静的DOM同期用スクリプト

function extractDataFromDynamicArea() {
  const dynamicArea = document.getElementById("dynamic-slot-area");
  if (!dynamicArea) {
    console.warn("⚠ dynamic-slot-area が見つかりません");
    return [];
  }

  const slotElements = dynamicArea.querySelectorAll(".slot, .subslot");
  const data = [];

  slotElements.forEach(el => {
    const slotId = el.id || el.getAttribute("id");
    if (!slotId) return;

    const phraseEl = el.querySelector(".slot-phrase, .subslot-element");
    const textEl = el.querySelector(".slot-text, .subslot-text");

    const phraseText = phraseEl ? phraseEl.textContent : "";
    const slotText = textEl ? textEl.textContent : "";

    data.push({
      Slot: slotId,
      SlotPhrase: phraseText,
      SlotText: slotText
    });
  });

  return data;
}

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

function fallbackSyncFromDOM() {
  console.warn("⚠ JSON読み込みに失敗したため、動的エリアから同期します");
  const data = extractDataFromDynamicArea();
  syncAllSlotsFromJson(data);
}

function loadJsonWithFallback(url, fallbackFn) {
  fetch(url)
    .then(res => res.text())
    .then(text => {
      try {
        const parsed = JSON.parse(text);
        window.loadedJsonData = parsed;
        syncAllSlotsFromJson(parsed);

        const topDisplayItem = parsed.find(d => d.DisplayAtTop);
        if (topDisplayItem && topDisplayItem.DisplayText) {
          const topDiv = document.getElementById("display-top-question-word");
          if (topDiv) {
            topDiv.textContent = topDisplayItem.DisplayText;
            console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
          } else {
            console.warn("⚠ display-top-question-word が見つかりません");
          }
        }
      } catch (e) {
        console.error("❌ JSON構文エラー", e, text);
        alert("無効な JSON ファイルです。フォールバック動作に切り替えます。");
        fallbackFn();
      }
    });
}

window.addEventListener('load', () => {
  loadJsonWithFallback("slot_order_data.json", fallbackSyncFromDOM);
});
