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


function normalizeSlotId(slotId) {
  return slotId.replace(/-sub-sub/g, '-sub');
}


function syncDynamicToStatic() {
  // 🧹 slot-*-sub の中にあるサブスロット phrase/text を初期化
  const allSubContainers = document.querySelectorAll('[id^="slot-"][id$="-sub"]');
  allSubContainers.forEach(container => {
    const phraseBlocks = container.querySelectorAll('.slot-phrase');
    const textBlocks = container.querySelectorAll('.slot-text');
    phraseBlocks.forEach(p => p.textContent = "");
    textBlocks.forEach(t => t.textContent = "");
  });

// 🧹 全サブスロット初期化（静的DOM）
const allSubslots = document.querySelectorAll('[id*="-sub-sub-"]');
allSubslots.forEach(slot => {
  const phrase = slot.querySelector('.slot-phrase');
  const text = slot.querySelector('.slot-text');
  if (phrase) phrase.textContent = "";
  if (text) text.textContent = "";
});

  const data = extractDataFromDynamicArea();
  if (data.length === 0) {
    console.warn("⚠ 動的エリアからデータ抽出できませんでした");
    return;
  }

  
  data.forEach(item => {
    if (item.SubslotID === "" && item.PhraseType === "word") {
      // 上位スロットへの書き込み
      
    console.log("検索ID(normalized):", normalizeSlotId(item.Slot));
    const container = document.getElementById(normalizeSlotId(item.Slot));
      if (container) {
      console.log("container found for ID:", container.id);
        const phraseDiv = container.querySelector(".slot-phrase");
      console.log("phraseDiv:", phraseDiv);
        const textDiv = container.querySelector(".slot-text");
      console.log("textDiv:", textDiv);
        if (phraseDiv) {
          phraseDiv.textContent = item.SlotPhrase || "";
          console.log(`✅ phrase書き込み成功: ${item.Slot} (parent)`);
        }
        if (textDiv) {
          textDiv.textContent = item.SlotText || "";
          console.log(`✅ text書き込み成功: ${item.Slot} (parent)`);
        }
      }
      return;
    }
    // 元のサブスロット書き込み処理（以下は既存処理をそのまま残す）
    console.log("サブスロット検索ID(normalized):", normalizeSlotId(item.Slot));
    const slotElement = document.getElementById(normalizeSlotId(item.Slot));
    if (!slotElement) {
      console.log("サブスロット要素が見つかりません:", normalizeSlotId(item.Slot));
      console.warn(`⚠ スロットが見つかりません: ${item.Slot}`);
      return;
    }
    const phraseElement = slotElement.querySelector(".slot-phrase");
    console.log("サブスロット phraseElement:", phraseElement);
    const slotTextElement = slotElement.querySelector(".slot-text");
    console.log("サブスロット textElement:", slotTextElement);

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
