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

function syncDynamicToStatic() {
  const data = extractDataFromDynamicArea();
  if (data.length === 0) {
    console.warn("⚠ 動的エリアからデータ抽出できませんでした");
    return;
  }

  data.forEach(item => {
    const slotElement = document.getElementById(item.Slot);
    if (!slotElement) {
      console.warn(`⚠ スロットが見つかりません: ${item.Slot}`);
      return;
    }
    const phraseElement = slotElement.querySelector(".slot-phrase");
    const slotTextElement = slotElement.querySelector(".slot-text");

    if (phraseElement) {
      phraseElement.textContent = item.SlotPhrase;
      console.log(`✅ phrase書き込み成功: ${item.Slot}`);
    }
    if (slotTextElement) {
      slotTextElement.textContent = item.SlotText;
      console.log(`✅ text書き込み成功: ${item.Slot}`);
    }
  });
}

// 例：ページロード後やJSONロード後に呼ぶ
window.onload = function() {
  syncDynamicToStatic();
};
