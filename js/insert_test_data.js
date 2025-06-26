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
  console.log("🔄 syncDynamicToStatic 実行開始");
// 🔼 DisplayAtTop 対応（分離疑問詞表示）ここから追加
if (window.loadedJsonData) {
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
}
// 🔼 DisplayAtTop 対応ここまで

  console.log("🧹 サブスロット初期化開始");
  // 🧹 slot-*-sub の中にあるサブスロット phrase/text を初期化
  const allSubContainers = document.querySelectorAll('[id^="slot-"][id$="-sub"]');
  console.log(`📊 初期化対象サブコンテナ: ${allSubContainers.length}件`);
  allSubContainers.forEach(container => {
    const phraseBlocks = container.querySelectorAll('.slot-phrase');
    const textBlocks = container.querySelectorAll('.slot-text');
    console.log(`🧹 "${container.id}"内 - phraseBlocks: ${phraseBlocks.length}, textBlocks: ${textBlocks.length}`);
    phraseBlocks.forEach(p => p.textContent = "");
    textBlocks.forEach(t => t.textContent = "");
  });

  console.log("🧹 全サブスロット初期化開始");
// 🧹 全サブスロット初期化（静的DOM）
const allSubslots = document.querySelectorAll('[id*="-sub-sub-"]');
console.log(`📊 初期化対象サブスロット: ${allSubslots.length}件`);
allSubslots.forEach(slot => {
  const phrase = slot.querySelector('.slot-phrase');
  const text = slot.querySelector('.slot-text');
  console.log(`🧹 "${slot.id}"内 - phrase: ${!!phrase}, text: ${!!text}`);
  if (phrase) phrase.textContent = "";
  if (text) text.textContent = "";
});

  console.log("🔄 動的エリアからデータ抽出開始");
  const data = extractDataFromDynamicArea();
  console.log(`📊 動的エリアから抽出したデータ: ${data.length}件`);
  if (data.length === 0) {
    console.log("🔄 動的エリアからのデータ抽出失敗時のDisplayAtTop処理開始");
  // 🔼 分離疑問詞 (DisplayAtTop) 書き込み処理
  const topDisplay = data.find(d => d.DisplayAtTop);
  if (topDisplay && topDisplay.DisplayText) {
    const topDiv = document.getElementById("display-top-question-word");
    if (topDiv) {
      topDiv.textContent = topDisplay.DisplayText;
      console.log(`🔼 DisplayAtTop 表示: ${topDisplay.DisplayText}`);
    } else {
      console.warn("⚠ display-top-question-word が見つかりません");
    }
  }
    console.warn("⚠ 動的エリアからデータ抽出できませんでした");
    return;
  }

  console.log("🔄 抽出データの処理開始");
  data.forEach(item => {
    console.log(`🔄 処理項目: ${JSON.stringify(item)}`);
    if (item.SubslotID === "" && item.PhraseType === "word") {
      // 上位スロットへの書き込み
      console.log(`👑 上位スロット処理: ${item.Slot}`);
    console.log("検索ID(normalized):", normalizeSlotId(item.Slot));
    const container = document.getElementById("slot-" + item.Slot.toLowerCase());
      if (container) {
      console.log("container found for ID:", container.id);
      console.log("container HTML:", container.outerHTML.substring(0, 150) + "...");
        const phraseDiv = container.querySelector(".slot-phrase");
      console.log("phraseDiv:", phraseDiv ? phraseDiv.outerHTML : "未検出");
        const textDiv = container.querySelector(".slot-text");
      console.log("textDiv:", textDiv ? textDiv.outerHTML : "未検出");
        if (phraseDiv) {
          phraseDiv.textContent = item.SlotPhrase || "";
          console.log(`✅ phrase書き込み成功: ${item.Slot} (parent) | 値: "${item.SlotPhrase}"`);
        } else {
          console.warn(`❌ 上位phraseDiv取得失敗: ${item.Slot}`);
        }
        if (textDiv) {
          textDiv.textContent = item.SlotText || "";
          console.log(`✅ text書き込み成功: ${item.Slot} (parent) | 値: "${item.SlotText}"`);
          
          // textDiv内にあるslot-phraseを確認
          const nestedPhraseDiv = textDiv.querySelector(".slot-phrase");
          if (nestedPhraseDiv) {
            console.warn(`⚠️ textDiv内にslot-phraseが入れ子になっています: ${item.Slot}`);
            console.warn(`⚠️ この入れ子構造が原因で書き込みが上書きされている可能性があります`);
          }
        } else {
          console.warn(`❌ 上位textDiv取得失敗: ${item.Slot}`);
        }
      } else {
        console.warn(`❌ 上位スロットが見つかりません: slot-${item.Slot.toLowerCase()}`);
      }
      return;
    }
    // 元のサブスロット書き込み処理（以下は既存処理をそのまま残す）
    console.log("サブスロット検索ID(normalized):", normalizeSlotId(item.Slot));
    
    // 🔽 DisplayAtTop 対象の subslot 要素はスキップ
    if (window.loadedJsonData) {
      const topDisplayItem = window.loadedJsonData.find(d => d.DisplayAtTop);
      if (
        topDisplayItem &&
        topDisplayItem.DisplayText &&
        item.SubslotElement === topDisplayItem.DisplayText
      ) {
        console.log(`🚫 subslot "${item.SubslotElement}" は DisplayAtTop で表示済のためスキップ`);
        return;
      }
    }
    
    console.log("🔍 サブスロット要素検索:", normalizeSlotId(item.Slot));
const slotElement = document.getElementById(normalizeSlotId(item.Slot));
    if (!slotElement) {
      console.log("サブスロット要素が見つかりません:", normalizeSlotId(item.Slot));
      console.warn(`⚠ スロットが見つかりません: ${item.Slot}`);
      return;
    }
    console.log("🔍 サブスロット要素発見:", slotElement.id, "| HTML:", slotElement.outerHTML.substring(0, 100) + "...");
    const phraseElement = slotElement.querySelector(".slot-phrase");
    console.log("サブスロット phraseElement:", phraseElement ? phraseElement.outerHTML : "未検出");
    const slotTextElement = slotElement.querySelector(".slot-text");
    console.log("サブスロット textElement:", slotTextElement ? slotTextElement.outerHTML : "未検出");

    if (phraseElement) {
      phraseElement.textContent = item.SlotPhrase;
      console.log(`✅ phrase書き込み成功: ${item.Slot} | 値: "${item.SlotPhrase}"`);
    } else {
      console.warn(`❌ サブphrase要素取得失敗: ${item.Slot}`);
    }
    if (slotTextElement) {
      slotTextElement.textContent = item.SlotText;
      console.log(`✅ text書き込み成功: ${item.Slot} | 値: "${item.SlotText}"`);
      
      // slotTextElement内にあるslot-phraseを確認
      const nestedPhraseDiv = slotTextElement.querySelector(".slot-phrase");
      if (nestedPhraseDiv) {
        console.warn(`⚠️ slotTextElement内にslot-phraseが入れ子になっています: ${item.Slot}`);
        console.warn(`⚠️ この入れ子構造が原因で書き込みが上書きされている可能性があります`);
      }
    } else {
      console.warn(`❌ サブtext要素取得失敗: ${item.Slot}`);
    }
  });

}

// 例：ページロード後やJSONロード後に呼ぶ
// window.onload = function() {
//   syncDynamicToStatic();
// };


// DisplayAtTop に対応する疑問詞をページ上部に表示
const topDisplayItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
if (topDisplayItem && topDisplayItem.DisplayText) {
  const topDiv = document.getElementById("display-top-question-word");
  if (topDiv) {
    topDiv.textContent = topDisplayItem.DisplayText;
    console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
  } else {
    console.warn("⚠ display-top-question-word が見つかりません");
  }

// 🔼 DisplayAtTop スロット表示（遅延でDOM書き込み）
setTimeout(() => {
  const topDisplayItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
  if (topDisplayItem && topDisplayItem.DisplayText) {
    const topDiv = document.getElementById("display-top-question-word");
    if (topDiv) {
      topDiv.textContent = topDisplayItem.DisplayText;
      console.log("✅ DisplayAtTop 表示（遅延）:", topDisplayItem.DisplayText);
    } else {
      console.warn("⚠ display-top-question-word が見つかりません");
    }
  }
}, 0);

}



// ✅ 修正版：window.loadedJsonData を直接参照してスロット書き込み
function syncUpperSlotsFromJson(data) {
  console.log("🔄 上位スロット同期（from window.loadedJsonData）開始");
  console.log("📊 データ全体:", JSON.stringify(data.slice(0, 3))); // 最初の3件だけ表示
  console.log("📝 上位スロット対象件数:", data.filter(item => item.SubslotID === "" && item.PhraseType === "word").length);
  
  data.forEach(item => {
    if (item.SubslotID === "" && item.PhraseType === "word") {
      console.log("🔍 上位スロット処理開始:", JSON.stringify(item));
      const slotId = "slot-" + item.Slot.toLowerCase();
      console.log("👉 探索するスロットID:", slotId);
      
      const container = document.getElementById(slotId);
      if (container) {
        console.log("✅ スロットコンテナ発見:", container.id, "| HTML:", container.outerHTML.substring(0, 100) + "...");
        
        // すべての .slot-phrase 要素を取得（入れ子構造も考慮）
        const allPhraseDivs = container.querySelectorAll(".slot-phrase");
        console.log("🔢 slot-phrase要素数:", allPhraseDivs.length);
        
        // 最初の .slot-phrase を使用
        const phraseDiv = allPhraseDivs[0];
        console.log("📌 使用するphraseDiv:", phraseDiv ? phraseDiv.outerHTML : "未検出");
        
        // .slot-text直下の.slot-phraseを除外した本来のtextDivを取得
        const textDiv = container.querySelector(".slot-text");
        console.log("📌 使用するtextDiv:", textDiv ? textDiv.outerHTML : "未検出");
        
        if (phraseDiv) {
          phraseDiv.textContent = item.SlotPhrase || "";
          console.log(`✅ 上位 phrase書き込み成功: ${item.Slot} | 値: "${item.SlotPhrase}"`);
        } else {
          console.warn(`❌ 上位phraseDiv取得失敗: ${slotId}`);
        }
        
        if (textDiv) {
          textDiv.textContent = item.SlotText || "";
          console.log(`✅ 上位 text書き込み成功: ${item.Slot} | 値: "${item.SlotText}"`);
          
          // textDiv内のslot-phraseも確認
          const nestedPhraseDiv = textDiv.querySelector(".slot-phrase");
          if (nestedPhraseDiv) {
            console.warn(`⚠️ textDiv内にslot-phraseが入れ子になっています: ${slotId}`);
          }
        } else {
          console.warn(`❌ 上位textDiv取得失敗: ${slotId}`);
        }
      } else {
        console.warn(`❌ 上位スロットが見つかりません: ${slotId}`);
        // 念のため存在するスロットIDを確認
        const allSlots = document.querySelectorAll('[id^="slot-"]');
        console.log("📋 存在するスロットID一覧:", Array.from(allSlots).map(el => el.id).join(", "));
      }
    }
  });
}

function syncSubslotsFromJson(data) {
  console.log("🔄 サブスロット同期（from window.loadedJsonData）開始");
  console.log("📊 サブスロット対象件数:", data.filter(item => item.SubslotID !== "").length);
  
  data.forEach(item => {
    if (item.SubslotID !== "") {
      console.log("🔍 サブスロット処理開始:", JSON.stringify(item));
      const slotId = "slot-" + item.Slot.toLowerCase() + "-sub-" + item.SubslotID;
      console.log("👉 探索するサブスロットID:", slotId);
      
      const slotElement = document.getElementById(slotId);
      if (!slotElement) {
        console.warn(`❌ サブスロットが見つかりません: ${slotId}`);
        // 近いIDを検索
        const similarElements = document.querySelectorAll(`[id^="slot-${item.Slot.toLowerCase()}-"]`);
        if (similarElements.length > 0) {
          console.log(`📋 類似IDの要素一覧:`, Array.from(similarElements).map(el => el.id).join(", "));
        }
        return;
      }
      
      console.log("✅ サブスロット要素発見:", slotElement.id, "| HTML:", slotElement.outerHTML.substring(0, 100) + "...");
      
      const phraseElement = slotElement.querySelector(".slot-phrase");
      console.log("📌 サブスロットphraseElement:", phraseElement ? phraseElement.outerHTML : "未検出");
      
      const textElement = slotElement.querySelector(".slot-text");
      console.log("📌 サブスロットtextElement:", textElement ? textElement.outerHTML : "未検出");
      
      if (phraseElement) {
        phraseElement.textContent = item.SlotPhrase || "";
        console.log(`✅ サブ phrase書き込み成功: ${slotId} | 値: "${item.SlotPhrase}"`);
      } else {
        console.warn(`❌ サブphrase要素取得失敗: ${slotId}`);
      }
      
      if (textElement) {
        textElement.textContent = item.SlotText || "";
        console.log(`✅ サブ text書き込み成功: ${slotId} | 値: "${item.SlotText}"`);
        
        // textElement内のslot-phraseも確認
        const nestedPhraseDiv = textElement.querySelector(".slot-phrase");
        if (nestedPhraseDiv) {
          console.warn(`⚠️ textElement内にslot-phraseが入れ子になっています: ${slotId}`);
        }
      } else {
        console.warn(`❌ サブtext要素取得失敗: ${slotId}`);
      }
    }
  });
}

// ✅ 差分追加：window.loadedJsonData を使った同期を起動
window.onload = function() {
  console.log("🚀 window.onload 発火");
  console.log("📊 window.loadedJsonData存在確認:", !!window.loadedJsonData);
  
  if (window.loadedJsonData) {
    console.log("📦 loadedJsonData件数:", window.loadedJsonData.length);
    console.log("📝 最初のデータサンプル:", JSON.stringify(window.loadedJsonData[0]));
  }
  
  // DOM構造の検証
  console.log("🔍 slot-containerの数:", document.querySelectorAll(".slot-container").length);
  console.log("🔍 slot-phraseの数:", document.querySelectorAll(".slot-phrase").length);
  console.log("🔍 slot-textの数:", document.querySelectorAll(".slot-text").length);
  
  // 重要: テキストエリア内のslot-phraseを確認
  const textDivsWithPhrase = Array.from(document.querySelectorAll(".slot-text")).filter(
    div => div.querySelector(".slot-phrase")
  );
  console.log("⚠️ slot-text内にslot-phraseを持つ要素数:", textDivsWithPhrase.length);
  if (textDivsWithPhrase.length > 0) {
    console.log("⚠️ 例:", textDivsWithPhrase[0].outerHTML);
  }
  
  syncDynamicToStatic();
  
  if (window.loadedJsonData) {
    syncUpperSlotsFromJson(window.loadedJsonData);
    syncSubslotsFromJson(window.loadedJsonData);
  } else {
    console.warn("⚠ window.loadedJsonData が存在しません");
  }
};
