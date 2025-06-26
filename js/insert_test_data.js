// insert_test_data.js をベースにした動的記載エリアから静的DOM同期用スクリプト

function extractDataFromDynamicArea() {
  const data = [];
  const slotElements = document.querySelectorAll(".slot, .subslot");

  slotElements.forEach((el) => {
    const slotId = el.id.replace(/^slot-/, "").toUpperCase();

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
  let data = extractDataFromDynamicArea();

  // ❗補完：DOMから構文情報が取れない場合、window.loadedJsonDataを使用
  if (!data || !data.some(d => d.PhraseType || d.SubslotID)) {
    console.warn("⚠ DOMから構文情報が取得できませんでした。window.loadedJsonDataから読み込みます。");
    if (Array.isArray(window.loadedJsonData)) {
      data = window.loadedJsonData;
    } else {
      console.error("❌ window.loadedJsonDataが存在しません。同期できません。");
      return;
    }
  }

  // 上位スロット表示（PhraseType === word, SubslotID === ""）
  data
    .filter((item) => item.SubslotID === "" && item.PhraseType === "word")
    .forEach((item) => {
      const slotId = item.Slot.toLowerCase();
      const container = document.getElementById("slot-" + slotId);
      if (!container) return;
      const phraseEl = container.querySelector(".slot-phrase");
      const textEl = container.querySelector(".slot-text");

      if (item.SlotPhrase && phraseEl) {
        phraseEl.textContent = item.SlotPhrase;
        console.log(`✅ 上位スロット phrase書き込み成功: slot-${slotId}`);
      }
      if (item.SlotText && textEl) {
        textEl.textContent = item.SlotText;
        console.log(`✅ 上位スロット text書き込み成功: slot-${slotId}`);
      }
    });

  // サブスロット表示
  data
    .filter((item) => item.SubslotID && item.PhraseType !== "clause")
    .forEach((sub) => {
      const subslotId = `slot-${sub.Slot.toLowerCase()}-sub-${sub.SubslotID.toLowerCase()}`;
      const container = document.getElementById(subslotId);
      console.log("サブスロット検索ID(normalized):", subslotId);

      if (container) {
        const phraseEl = container.querySelector(".slot-phrase, .subslot-element");
        const textEl = container.querySelector(".slot-text, .subslot-text");
        console.log("サブスロット phraseElement:", phraseEl);
        console.log("サブスロット textElement:", textEl);

        if (phraseEl && sub.SubslotElement) {
          phraseEl.textContent = sub.SubslotElement;
          console.log(`✅ phrase書き込み成功: ${subslotId}`);
        }

        if (textEl && sub.SubslotText) {
          textEl.textContent = sub.SubslotText;
          console.log(`✅ text書き込み成功: ${subslotId}`);
        }
      } else {
        console.warn(`⚠ サブスロット DOM未検出: ${subslotId}`);
      }
    });

  // 補助表示（DisplayAtTop）
  data
    .filter((item) => item.DisplayAtTop && item.DisplayText)
    .forEach((item) => {
      console.log(`✅ DisplayAtTop 表示: ${item.DisplayText}`);
    });
}