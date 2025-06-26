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



// ✅ 修正版：window.loadedJsonData を直接参照してスロット書き込み (順序制御付き)
function syncUpperSlotsFromJson(data) {
  if (!data || !Array.isArray(data)) {
    console.error("❌ 上位スロット同期: 無効なデータが渡されました", data);
    return;
  }
  
  // 上位スロットのデータを抽出し、orderでソート
  const upperSlotData = data.filter(item => item.SubslotID === "" && item.PhraseType === "word");
  const sortedData = sortJsonDataByOrder(upperSlotData);
  
  console.log(`🔄 上位スロット同期: ${upperSlotData.length}件の対象を処理 (順序付け機能適用)`);
  
  // 詳細ログはデバッグが必要な時だけ出す
  if (window.DEBUG_SYNC) {
    console.log("📊 データサンプル:", JSON.stringify(sortedData.slice(0, 3))); // 最初の3件だけ表示
    console.log("🔢 順序付けされたスロット:", sortedData.map(item => `${item.Slot}(${item.order || 0})`).join(', '));
  }
  
  // グローバル変数がなければ初期化
  if (typeof window.DEBUG_SYNC === 'undefined') {
    window.DEBUG_SYNC = false;
  }
  
  // 処理対象のスロットコンテナを保存 (後で再配置するため)
  const processedContainers = new Set();
  
  // orderでソートしたデータに対して処理
  sortedData.forEach(item => {
    console.log("🔍 上位スロット処理開始:", JSON.stringify(item));
    const slotId = "slot-" + item.Slot.toLowerCase();
    console.log("👉 探索するスロットID:", slotId, "順序:", item.order || 0);
    
    const container = document.getElementById(slotId);
    if (container) {
      console.log("✅ スロットコンテナ発見:", container.id);
      // 処理したコンテナを記録
      processedContainers.add(slotId);
      
      // 重要: slot-containerの直下のslot-phraseを選択（:scope > を使用）
      const phraseDiv = container.querySelector(":scope > .slot-phrase");
      console.log("📌 上位スロットのphraseDiv:", phraseDiv ? phraseDiv.outerHTML : "未検出");
      
      const textDiv = container.querySelector(":scope > .slot-text");
      console.log("📌 上位スロットのtextDiv:", textDiv ? textDiv.outerHTML : "未検出");
      
      if (phraseDiv) {
        phraseDiv.textContent = item.SlotPhrase || "";
        console.log(`✅ 上位 phrase書き込み成功: ${item.Slot} | 値: "${item.SlotPhrase}"`);
      } else {
        console.warn(`❌ 上位phraseDiv取得失敗: ${slotId} - 要素が見つかりません`);
      }
      
      if (textDiv) {
        // textDiv内のslot-phraseがあれば、それも合わせてクリア
        const nestedPhraseDiv = textDiv.querySelector(".slot-phrase");
        if (nestedPhraseDiv) {
          nestedPhraseDiv.textContent = "";
        }
        
        // テキストノードを安全に設定（firstChildが存在しない場合の対策）
        if (textDiv.firstChild && textDiv.firstChild.nodeType === Node.TEXT_NODE) {
          textDiv.firstChild.textContent = item.SlotText || "";
        } else {
          // firstChildがない場合は新しいテキストノードを作成
          textDiv.textContent = ""; // 既存のコンテンツをクリア
          textDiv.append(document.createTextNode(item.SlotText || ""));
        }
        console.log(`✅ 上位 text書き込み成功: ${item.Slot} | 値: "${item.SlotText}"`);
        
        // サブスロットの並べ替えを実行
        try {
          reorderSubslots(slotId, data);
        } catch (err) {
          console.error(`❌ ${slotId}のサブスロット並べ替えでエラー:`, err.message);
        }
      } else {
        console.warn(`❌ 上位textDiv取得失敗: ${slotId}`);
      }
    } else {
      console.warn(`❌ 上位スロットが見つかりません: ${slotId}`);
    }
  });
  
  // 親コンテナを探して順序付け
  try {
    const mainContainer = document.querySelector('.slot-container');
    if (mainContainer) {
      console.log("🔢 メインコンテナの上位スロットを順序付けします");
      
      // 順序マップを作成
      const orderMap = new Map();
      upperSlotData.forEach(item => {
        const slotId = "slot-" + item.Slot.toLowerCase();
        orderMap.set(slotId, item.order || 0);
      });
      
      // メインコンテナ内のスロット要素を順序付け
      const slotElements = mainContainer.querySelectorAll('[id^="slot-"]');
      if (slotElements.length > 0) {
        // 対象となる直接の子スロット要素のみをフィルタ
        const directSlots = Array.from(slotElements).filter(el => {
          // サブスロットを除外 (IDが「slot-XX-」形式のものは上位スロット)
          const isTopLevelSlot = el.id.split('-').length === 2;
          return isTopLevelSlot;
        });
        
        if (directSlots.length > 0) {
          console.log(`🔢 上位スロット ${directSlots.length}個を順序付けします`);
          
          // 要素を順序でソート
          const slotsWithOrder = directSlots.map(el => {
            const order = orderMap.get(el.id) || 0;
            return { el, order };
          });
          
          slotsWithOrder.sort((a, b) => a.order - b.order);
          
          // 親要素に順序通りに追加し直す
          slotsWithOrder.forEach(item => {
            mainContainer.appendChild(item.el);
            console.log(`📏 スロット ${item.el.id} を順序 ${item.order} で再配置`);
          });
          
          console.log(`✅ 上位スロットを順序通りに再配置しました`);
        }
      }
    }
  } catch (err) {
    console.error("❌ 上位スロット順序付け中にエラー:", err.message);
  }
}

// ✅ サブスロット同期機能の実装 (順序制御対応版)
function syncSubslotsFromJson(data) {
  console.log("🔄 サブスロット同期（順序制御対応版）開始");
  if (!data || !Array.isArray(data)) {
    console.warn("⚠ サブスロット同期: データが無効です");
    return;
  }
  
  // サブスロット用のデータをフィルタリング
  const subslotData = data.filter(item => item.SubslotID && item.SubslotID !== "");
  console.log(`📊 サブスロット対象件数: ${subslotData.length}`);
  
  // 親スロットごとにデータをグループ化
  const parentSlotGroups = new Map();
  
  subslotData.forEach(item => {
    const parentSlot = item.Slot.toLowerCase();
    if (!parentSlotGroups.has(parentSlot)) {
      parentSlotGroups.set(parentSlot, []);
    }
    parentSlotGroups.get(parentSlot).push(item);
  });
  
  console.log(`📊 サブスロットの親グループ数: ${parentSlotGroups.size}`);
  
  // 各親スロットグループごとに処理
  for (const [parentSlot, items] of parentSlotGroups.entries()) {
    try {
      // このグループ内のサブスロットをorderでソート
      const sortedItems = sortJsonDataByOrder(items);
      const parentSlotId = `slot-${parentSlot}`;
      
      console.log(`🔍 親スロット ${parentSlotId} のサブスロット ${sortedItems.length}個を処理`);
      
      // 各サブスロットを処理
      sortedItems.forEach(item => {
        try {
          const subslotId = item.SubslotID.toLowerCase();
          const fullSlotId = `slot-${parentSlot}-${subslotId}`;
          console.log(`🔍 サブスロット処理: ${fullSlotId} (順序: ${item.order || 0})`);
          
          const slotElement = document.getElementById(fullSlotId);
          if (!slotElement) {
            console.warn(`⚠ サブスロット要素が見つかりません: ${fullSlotId}`);
            return;
          }
          
          // phraseとtextを更新
          const phraseElement = slotElement.querySelector(".slot-phrase");
          const textElement = slotElement.querySelector(".slot-text");
          
          if (phraseElement && item.SubslotElement) {
            phraseElement.textContent = item.SubslotElement;
            console.log(`✅ サブスロット phrase書き込み: ${fullSlotId} | "${item.SubslotElement}"`);
          }
          
          if (textElement && item.SubslotText) {
            textElement.textContent = item.SubslotText;
            console.log(`✅ サブスロット text書き込み: ${fullSlotId} | "${item.SubslotText}"`);
          }
          
          // データ属性にorder値を設定（CSSでの順序付けのため）
          slotElement.dataset.order = item.order || 0;
          
        } catch (err) {
          console.error(`❌ サブスロット処理エラー: ${err.message}`, item);
        }
      });
      
      // サブスロットの順序付けを実行
      reorderSubslots(parentSlotId, data);
      
    } catch (err) {
      console.error(`❌ 親スロット ${parentSlot} のサブスロット処理中にエラー: ${err.message}`);
    }
  }
  
  console.log("✅ サブスロット同期完了（順序付け適用済み）");
}

// 特定のM1スロットをテスト（デバッグ用）
function debugM1Slot() {
  if (!window.loadedJsonData) {
    console.warn("⚠ window.loadedJsonData が存在しないためM1デバッグできません");
    return;
  }
  
  const m1Data = window.loadedJsonData.find(item => 
    item.Slot.toLowerCase() === "m1" && item.SubslotID === "" && item.PhraseType === "word"
  );
  
  if (!m1Data) {
    console.warn("⚠ M1の上位スロットデータが見つかりません");
    return;
  }
  
  console.log("🔍 M1スロットデバッグ - データ:", m1Data);
  
  // M1スロットを直接取得
  const m1Container = document.getElementById("slot-m1");
  if (!m1Container) {
    console.warn("⚠ slot-m1要素が見つかりません");
    return;
  }
  
  // M1の構造を確認
  console.log("📋 M1スロット構造:", m1Container.outerHTML.substring(0, 200));
  
  // 直接の子要素としてのslot-phrase
  const phraseDiv = m1Container.querySelector(":scope > .slot-phrase");
  console.log("📌 M1の直接子としてのslot-phrase:", phraseDiv ? phraseDiv.outerHTML : "未検出");
  
  if (phraseDiv) {
    // 値を設定
    phraseDiv.textContent = m1Data.SlotPhrase || "";
    console.log("✅ M1 phrase値設定:", m1Data.SlotPhrase);
  } else {
    console.warn("⚠ M1にslot-phrase要素がないか、直接の子要素ではありません");
  }
  
  // slot-textの処理
  const textDiv = m1Container.querySelector(":scope > .slot-text");
  if (textDiv) {
    // 入れ子のslot-phraseを確認
    const nestedPhraseDiv = textDiv.querySelector(".slot-phrase");
    console.log("📌 M1のslot-text内のslot-phrase:", nestedPhraseDiv ? nestedPhraseDiv.outerHTML : "未検出");
    
    if (nestedPhraseDiv) {
      // 入れ子のslot-phraseも念のためクリア
      nestedPhraseDiv.textContent = "";
    }
    
    // テキストノードを適切に設定 - 安全に処理
    if (textDiv.firstChild && textDiv.firstChild.nodeType === Node.TEXT_NODE) {
      textDiv.firstChild.textContent = m1Data.SlotText || "";
    } else {
      // firstChildがない場合や適切なノードでない場合は新しくテキストノードを作成
      textDiv.textContent = ""; // 既存のコンテンツをクリア
      textDiv.append(document.createTextNode(m1Data.SlotText || ""));
    }
    console.log("✅ M1 text値設定:", m1Data.SlotText);
  } else {
    console.warn("⚠ M1にslot-text要素が見つかりません");
  }
}

// グローバルにエクスポートする（index.htmlから呼び出せるように）
window.syncUpperSlotsFromJson = syncUpperSlotsFromJson;
window.syncSubslotsFromJson = syncSubslotsFromJson;
window.debugM1Slot = debugM1Slot;

// JSONロードエラー対策：try-catchで囲んでエラーを詳細にログ出力
window.safeJsonSync = function(data) {
  try {
    // 重複実行防止のためのフラグ
    if (window.isSyncInProgress) {
      console.log("⏳ 同期処理が既に実行中のため、このリクエストはスキップします");
      return;
    }
    window.isSyncInProgress = true;
    
    console.log("🔄 同期処理を開始します");
    if (!data || !Array.isArray(data)) {
      console.warn("⚠ 同期処理に渡されたデータが無効です:", typeof data);
      if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
        console.log("✅ window.loadedJsonDataを代わりに使用します");
        data = window.loadedJsonData;
      } else {
        console.error("❌ 有効なJSONデータがありません");
        window.isSyncInProgress = false;
        
        // 1秒後に再試行
        setTimeout(() => {
          console.log("🔄 JSONデータが無効だったため再試行します");
          if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
            window.safeJsonSync(window.loadedJsonData);
          }
        }, 1000);
        return;
      }
    }
    
    // CSS順序制御のためのスタイルを動的に追加
function addOrderingStyles() {
  // すでに追加されていたら何もしない
  if (document.getElementById('order-control-styles')) return;
  
  const styleSheet = document.createElement('style');
  styleSheet.id = 'order-control-styles';
  styleSheet.textContent = `
    /* フレックスボックスを使用して親要素内の順序を制御 */
    .slot-container, [id^="slot-"][id$="-sub"] {
      display: flex;
      flex-direction: column;
    }
    
    /* JavaScriptで設定したdata-order属性に基づいて順序付け */
    [data-order] {
      order: attr(data-order number);
    }
  `;
  
  document.head.appendChild(styleSheet);
  console.log("✅ 順序制御用CSSスタイルを追加しました");
}

// safeJsonSync関数の拡張（CSS順序制御の適用）
window.safeJsonSync = function(data) {
  try {
    // 重複実行防止のためのフラグ
    if (window.isSyncInProgress) {
      console.log("⏳ 同期処理が既に実行中のため、このリクエストはスキップします");
      return;
    }
    window.isSyncInProgress = true;
    
    console.log("🔄 同期処理を開始します");
    if (!data || !Array.isArray(data)) {
      console.warn("⚠ 同期処理に渡されたデータが無効です:", typeof data);
      if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
        console.log("✅ window.loadedJsonDataを代わりに使用します");
        data = window.loadedJsonData;
      } else {
        console.error("❌ 有効なJSONデータがありません");
        window.isSyncInProgress = false;
        
        // 1秒後に再試行
        setTimeout(() => {
          console.log("🔄 JSONデータが無効だったため再試行します");
          if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
            window.safeJsonSync(window.loadedJsonData);
          }
        }, 1000);
        return;
      }
    }
    
    // 順序制御用のCSSを追加
    addOrderingStyles();
    
    // 上位スロット同期を実行
    try {
      syncUpperSlotsFromJson(data);
      console.log("✅ 上位スロットの同期が完了");
    } catch (upperSlotError) {
      console.error("❌ 上位スロット同期中にエラーが発生:", upperSlotError.message);
    }
    
    // サブスロット同期関数があれば実行
    if (typeof syncSubslotsFromJson === 'function') {
      try {
        syncSubslotsFromJson(data);
        console.log("✅ サブスロットの同期が完了");
      } catch (subslotError) {
        console.error("❌ サブスロット同期中にエラーが発生:", subslotError.message);
      }
    }
    
    // 同期完了
    window.isSyncInProgress = false;
  } catch (err) {
    console.error("❌ 同期処理中にエラーが発生しました:", err.message);
    console.error("エラーの詳細:", err.stack);
    window.isSyncInProgress = false; // エラーが発生してもフラグはリセット
  }
};

    // 上位スロット同期を実行
    try {
      syncUpperSlotsFromJson(data);
      console.log("✅ 上位スロットの同期が完了");
    } catch (upperSlotError) {
      console.error("❌ 上位スロット同期中にエラーが発生:", upperSlotError.message);
    }
    
    // サブスロット同期関数があれば実行
    if (typeof syncSubslotsFromJson === 'function') {
      try {
        syncSubslotsFromJson(data);
        console.log("✅ サブスロットの同期が完了");
      } catch (subslotError) {
        console.error("❌ サブスロット同期中にエラーが発生:", subslotError.message);
      }
    }
    
    // 同期完了
    window.isSyncInProgress = false;
  } catch (err) {
    console.error("❌ 同期処理中にエラーが発生しました:", err.message);
    console.error("エラーの詳細:", err.stack);
    window.isSyncInProgress = false; // エラーが発生してもフラグはリセット
  }
};


// JSONデータをorder順に並べ替える関数
function sortJsonDataByOrder(jsonData) {
  if (!jsonData || !Array.isArray(jsonData)) return jsonData;
  
  return [...jsonData].sort((a, b) => {
    // orderが数値ではない場合のための対策
    const orderA = typeof a.order === 'number' ? a.order : parseInt(a.order) || 0;
    const orderB = typeof b.order === 'number' ? b.order : parseInt(b.order) || 0;
    return orderA - orderB;
  });
}

// DOM要素をorder属性に基づいて並べ替える
function reorderDomElements(container, selector, getOrderFunc) {
  if (!container) return;
  
  const elements = container.querySelectorAll(selector);
  if (elements.length <= 1) return; // 要素が1つ以下なら何もしない
  
  console.log(`🔢 ${container.id}内の${selector}要素を並べ替えます (${elements.length}個)`);
  
  // 要素とその順序値の配列を作成
  const elementsWithOrder = Array.from(elements).map(el => {
    const order = getOrderFunc(el);
    return { el, order };
  });
  
  // 順序でソート
  elementsWithOrder.sort((a, b) => a.order - b.order);
  
  // 親要素を取得
  const parent = elements[0].parentNode;
  
  // 順番に再配置
  elementsWithOrder.forEach(item => {
    parent.appendChild(item.el); // 末尾に移動（順序通りに並ぶ）
  });
  
  console.log(`✅ ${container.id}内の要素を順序通りに再配置しました`);
}

// 特定のスロットコンテナ内のサブスロットを順序付けする
function reorderSubslots(parentSlotId, jsonData) {
  const container = document.getElementById(parentSlotId);
  if (!container) {
    console.warn(`⚠ 並べ替え対象のコンテナが見つかりません: ${parentSlotId}`);
    return;
  }
  
  // このスロットに関連するサブスロットのデータを取得
  const parentId = parentSlotId.replace('slot-', '');
  const subslotData = jsonData.filter(item => 
    item.Slot.toLowerCase() === parentId && 
    item.SubslotID && 
    item.SubslotID !== ""
  );
  
  if (subslotData.length <= 1) {
    console.log(`ℹ️ ${parentSlotId}には並べ替えが必要なサブスロットがありません`);
    return;
  }
  
  console.log(`🔢 ${parentSlotId}のサブスロットを並べ替えます (${subslotData.length}個)`);
  
  // SubSlotIDからorderを取得するマップを作成
  const orderMap = new Map();
  subslotData.forEach(item => {
    orderMap.set(item.SubslotID.toLowerCase(), item.order || 0);
  });
  
  // サブスロット要素を取得して順序付け
  const subslotSelector = '[id^="slot-' + parentId.toLowerCase() + '-"]';
  const subslots = container.querySelectorAll(subslotSelector);
  
  if (subslots.length === 0) {
    console.warn(`⚠ ${parentSlotId}内にサブスロット要素が見つかりません`);
    return;
  }
  
  // サブスロット要素とその順序値の配列を作成
  const subslotElements = Array.from(subslots).map(el => {
    // IDからサブスロットIDを抽出（例：slot-m1-sub-o1 → sub-o1）
    const subslotId = el.id.replace(`slot-${parentId.toLowerCase()}-`, '');
    const order = orderMap.get(subslotId) || 0;
    return { el, order };
  });
  
  // 順序でソート
  subslotElements.sort((a, b) => a.order - b.order);
  
  // 親要素に順序通りに追加し直す
  subslotElements.forEach(item => {
    container.appendChild(item.el);
  });
  
  console.log(`✅ ${parentSlotId}内のサブスロットを順序通りに再配置しました`);
}

// ランダマイズ後の同期を確保するためのMutationObserverを設定
window.setupSyncObserver = function() {
  try {
    // 動的記載エリアの変更を監視
    const dynamicArea = document.getElementById("dynamic-slot-area");
    if (!dynamicArea) {
      console.warn("⚠ 監視対象の動的記載エリアが見つかりません");
      return;
    }
    
    console.log("👁 動的記載エリアの監視を開始します");
    
    // 変更の監視設定
    const observer = new MutationObserver(function(mutations) {
      console.log("👀 動的記載エリアに変更を検出しました");
      
      // 処理が重複しないよう、タイマーでデバウンス
      if (window.syncDebounceTimer) {
        clearTimeout(window.syncDebounceTimer);
      }
      
      window.syncDebounceTimer = setTimeout(() => {
        console.log("🔄 変更検出による同期処理を実行します");
        if (window.loadedJsonData) {
          window.safeJsonSync(window.loadedJsonData);
        }
      }, 300); // 300ミリ秒の遅延で実行
    });
    
    // 設定を適用して監視開始
    observer.observe(dynamicArea, { 
      childList: true, 
      subtree: true, 
      characterData: true,
      attributes: true
    });
    
    console.log("✅ MutationObserverの設定が完了しました");
    return observer;
  } catch (err) {
    console.error("❌ 監視設定中にエラーが発生しました:", err.message);
  }
};

// ランダマイザーの監視と同期（ランダマイザー用の特別対応）
window.setupRandomizerSync = function() {
  try {
    // ランダマイズボタンを探す
    const randomizerButtons = document.querySelectorAll('button[data-action="randomize"], button.randomize-button');
    if (randomizerButtons.length === 0) {
      console.warn("⚠ ランダマイズボタンが見つかりません");
      return;
    }
    
    console.log(`🎲 ランダマイズボタンを ${randomizerButtons.length}個 検出しました`);
    
    // 各ボタンにイベントリスナーを追加
    randomizerButtons.forEach((button, index) => {
      // 既存のイベントハンドラを保持するための対応
      const originalClickHandler = button.onclick;
      
      button.addEventListener('click', function(event) {
        console.log(`🎲 ランダマイズボタンがクリックされました (${index + 1})`);
        
        // ランダマイズ処理完了後に確実に同期処理を行う
        setTimeout(() => {
          console.log("🔄 ランダマイズ後の同期処理を実行します (遅延: 1000ms)");
          if (window.loadedJsonData) {
            // ランダマイズ後は強制的に上位スロットを再同期
            window.DEBUG_SYNC = true; // 詳細ログを有効化
            window.safeJsonSync(window.loadedJsonData);
            setTimeout(() => {
              window.DEBUG_SYNC = false; // ログ量を元に戻す
            }, 500);
          }
        }, 1000); // 1000ms（1秒）に延長 - ランダマイズ処理が確実に完了するのを待つ
      }, true); // キャプチャフェーズでイベントをキャッチ
      
      console.log(`✅ ランダマイズボタン(${index + 1})に同期処理を追加しました`);
    });
    
    // window.randomizeAllSlots関数をオーバーライド（存在する場合）
    if (typeof window.randomizeAllSlots === 'function') {
      const originalRandomizeFunc = window.randomizeAllSlots;
      window.randomizeAllSlots = function(...args) {
        console.log("🎲 randomizeAllSlots関数が呼び出されました");
        const result = originalRandomizeFunc.apply(this, args);
        
        // ランダマイズ処理完了後に同期処理を行う
        setTimeout(() => {
          console.log("🔄 randomizeAllSlots後の同期処理を実行します (遅延: 1000ms)");
          if (window.loadedJsonData) {
            // ランダマイズ後は強制的に上位スロットを再同期
            window.DEBUG_SYNC = true; // 詳細ログを有効化
            window.safeJsonSync(window.loadedJsonData);
            setTimeout(() => {
              window.DEBUG_SYNC = false; // ログ量を元に戻す
            }, 500);
          }
        }, 1000); // 1000ms（1秒）に延長
        
        return result;
      };
      console.log("✅ randomizeAllSlots関数をオーバーライドしました");
    }
    
    return true;
  } catch (err) {
    console.error("❌ ランダマイザー監視設定中にエラーが発生しました:", err.message);
    return false;
  }
};

// ページ読み込み完了時に監視を開始
document.addEventListener("DOMContentLoaded", function() {
  console.log("🌐 DOMContentLoaded イベント発生");
  setTimeout(() => {
    window.setupSyncObserver();
    window.setupRandomizerSync();
    
    // 初期同期も実行
    if (window.loadedJsonData) {
      window.safeJsonSync(window.loadedJsonData);
    }
    
    // JSONデータ変更を監視（loadedJsonDataの監視）- 改良版
    let lastJsonDataSignature = "";
    
    // データの特徴的な部分から署名を生成する関数
    function getDataSignature(data) {
      if (!data || !Array.isArray(data) || data.length === 0) return "";
      try {
        // スロットの内容からチェックサムを生成
        const sampleItems = data.slice(0, 3); // 最初の3件のみ使用
        const signature = sampleItems.map(item => 
          `${item.Slot}:${item.SlotPhrase && item.SlotPhrase.substring(0, 10)}`
        ).join('|');
        return signature;
      } catch (e) {
        return "";
      }
    }
    
    // 低頻度で定期チェック (3秒ごと)
    setInterval(() => {
      if (window.loadedJsonData) {
        const newSignature = getDataSignature(window.loadedJsonData);
        if (newSignature && newSignature !== lastJsonDataSignature) {
          console.log("🔄 window.loadedJsonData の実質的な変更を検出");
          window.safeJsonSync(window.loadedJsonData);
          lastJsonDataSignature = newSignature;
        }
      }
    }, 3000); // 3秒ごとに変更をチェック
    
  }, 500); // DOMが完全に構築されるのを待つ
});
