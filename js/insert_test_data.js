
// insert_test_data.js クリーン版：動的DOMスキャン + DisplayAtTop 表示対応
function clearAllUpperSlots() {
  const upperSlots = document.querySelectorAll('[id^="slot-"]:not([id*="-sub-"])');
  upperSlots.forEach(slot => {
    const phrase = slot.querySelector('.slot-phrase');
    const text = slot.querySelector('.slot-text');
    if (phrase) phrase.textContent = "";
    if (text) text.textContent = "";
  });
}

function clearAllSubslots() {
  const subslots = document.querySelectorAll('[id*="-sub-"]');
  subslots.forEach(slot => {
    const phrase = slot.querySelector('.slot-phrase, .subslot-element');
    const text = slot.querySelector('.slot-text, .subslot-text');
    if (phrase) phrase.textContent = "";
    if (text) text.textContent = "";
  });
}

function extractDataFromDynamicArea() {
  const dynamicArea = document.getElementById("dynamic-slot-area");
  if (!dynamicArea) {
    console.warn("⚠ dynamic-slot-area が見つかりません");
    return [];
  }

  const slotElements = dynamicArea.querySelectorAll(".slot, .subslot");
  return Array.from(slotElements).map(el => {
    const slotId = el.id || el.getAttribute("id");
    if (!slotId) return null;
    const phraseEl = el.querySelector(".slot-phrase, .subslot-element");
    const textEl = el.querySelector(".slot-text, .subslot-text");
    return {
      Slot: slotId,
      SlotPhrase: phraseEl?.textContent || "",
      SlotText: textEl?.textContent || ""
    };
  }).filter(Boolean);
}

function normalizeSlotId(slotId) {
  return slotId.replace(/-sub-sub/g, "-sub");
}

function syncDynamicToStatic() {
  clearAllSubslots();
  const data = extractDataFromDynamicArea();
  if (data.length === 0) {
    console.warn("⚠ 動的エリアからデータ抽出できませんでした");
    return;
  }

  data.forEach(item => {
    const slotElement = document.getElementById(normalizeSlotId(item.Slot));
    if (!slotElement) {
      console.warn(`⚠ スロットが見つかりません: ${item.Slot}`);
      return;
    }
    const phraseElement = slotElement.querySelector(".slot-phrase, .subslot-element");
    const textElement = slotElement.querySelector(".slot-text, .subslot-text");
    if (phraseElement) phraseElement.textContent = item.SlotPhrase || "";
    if (textElement) textElement.textContent = item.SlotText || "";
    console.log(`✅ スロット書き込み成功: ${item.Slot}`);
  });

  // DisplayAtTop 表示が可能な場合
  const topDisplayItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
  if (topDisplayItem?.DisplayText) {
    const topDiv = document.getElementById("display-top-question-word");
    if (topDiv) {
      topDiv.textContent = topDisplayItem.DisplayText;
      console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
    } else {
      console.warn("⚠ display-top-question-word が見つかりません");
    }
  }
}

window.onload = function () {
  syncDynamicToStatic();
};
