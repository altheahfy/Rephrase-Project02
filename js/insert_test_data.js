
// ✅ 上位・サブスロットを分離処理した同期用スクリプト

function normalizeSlotId(slotId) {
  return slotId.replace(/-sub-sub/g, '-sub');
}

function syncUpperSlots(data) {
  console.log("🔄 上位スロット同期開始");
  data.forEach(item => {
    if (!item.SubslotID && item.PhraseType === "word") {
      const container = document.getElementById("slot-" + item.Slot.toLowerCase());
      if (container) {
        const phraseDiv = container.querySelector(".slot-phrase");
        const textDiv = container.querySelector(".slot-text");
        if (phraseDiv) {
          phraseDiv.textContent = item.SlotPhrase || "";
          console.log(`✅ 上位 phrase書き込み成功: ${item.Slot}`);
        }
        if (textDiv) {
          textDiv.textContent = item.SlotText || "";
          console.log(`✅ 上位 text書き込み成功: ${item.Slot}`);
        }
      } else {
        console.warn(`⚠ 上位スロットが見つかりません: ${item.Slot}`);
      }
    }
  });
}

function syncSubslots(data) {
  console.log("🔄 サブスロット同期開始");
  data.forEach(item => {
    if (item.SubslotID) {
      const slotElement = document.getElementById(normalizeSlotId(item.Slot));
      if (!slotElement) {
        console.warn(`⚠ サブスロットが見つかりません: ${item.Slot}`);
        return;
      }
      const phraseElement = slotElement.querySelector(".slot-phrase");
      const textElement = slotElement.querySelector(".slot-text");
      if (phraseElement) {
        phraseElement.textContent = item.SlotPhrase || "";
        console.log(`✅ サブ phrase書き込み成功: ${item.Slot}`);
      }
      if (textElement) {
        textElement.textContent = item.SlotText || "";
        console.log(`✅ サブ text書き込み成功: ${item.Slot}`);
      }
    }
  });
}

// ページロード後に同期を開始
window.onload = function() {
  if (window.loadedJsonData) {
    syncUpperSlots(window.loadedJsonData);
    syncSubslots(window.loadedJsonData);
  } else {
    console.warn("⚠ window.loadedJsonData が存在しません");
  }
};
