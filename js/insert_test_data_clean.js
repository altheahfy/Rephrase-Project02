// insert_test_data.js をベースにした動的記載エリアから静的DOM同期用スクリプト

// 動的エリアからデータを抽出する関数
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

// スロットIDを正規化する関数
function normalizeSlotId(slotId) {
  return slotId.replace(/-sub-sub/g, '-sub');
}

// JSONデータをorder順に並べ替える関数（順序制御の基本関数）
function sortJsonDataByOrder(jsonData) {
  if (!jsonData || !Array.isArray(jsonData)) return jsonData;
  
  return [...jsonData].sort((a, b) => {
    // orderが数値ではない場合のための対策
    const orderA = typeof a.order === 'number' ? a.order : parseInt(a.order) || 0;
    const orderB = typeof b.order === 'number' ? b.order : parseInt(b.order) || 0;
    return orderA - orderB;
  });
}

// DOM要素をorder属性に基づいて並べ替える関数（注意：DOM構造変更を伴うため慎重に使用）
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

// 特定のスロットコンテナ内のサブスロットを順序付けする関数（改良版）
function reorderSubslots(parentSlotId, jsonData) {
  console.log(`🔄 サブスロット順序処理開始: ${parentSlotId}`);
  
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
  
  // サブスロットのデータをオーダー順にソート
  const sortedSubslotData = sortJsonDataByOrder(subslotData);
  console.log(`🔄 サブスロットの順序情報:`, sortedSubslotData.map(item => 
    `${item.SubslotID}:${item.display_order || item.order || 0}`
  ).join(', '));
  
  // SubSlotIDからorderを取得するマップを作成
  const orderMap = new Map();
  
  // 内容があるサブスロットを追跡
  const usedSubslots = new Set();
  
  subslotData.forEach(item => {
    // 順序値の取得
    const orderValue = item.display_order || item.order || 0;
    orderMap.set(item.SubslotID.toLowerCase(), orderValue);
    
    // 内容のあるサブスロットを記録
    if ((item.SubslotElement && item.SubslotElement.trim() !== "") || 
        (item.SubslotText && item.SubslotText.trim() !== "")) {
      usedSubslots.add(item.SubslotID.toLowerCase());
    }
  });
  
  console.log(`📋 ${parentSlotId}の使用中サブスロット:`, Array.from(usedSubslots).join(', '));
  
  // サブスロットのコンテナ（通常はslot-*-subの要素）
  const subslotContainer = container.querySelector(`#${parentSlotId}-sub`) || container;
  
  // サブスロット要素を取得して順序付けとフィルタリング
  const subslotSelector = '.subslot';
  const subslots = subslotContainer.querySelectorAll(subslotSelector);
  
  if (subslots.length === 0) {
    console.warn(`⚠ ${parentSlotId}内にサブスロット要素が見つかりません`);
    return;
  }
  
  // コンテナにFlex表示を明示的に設定して順序制御を有効化
  subslotContainer.style.display = 'flex';
  subslotContainer.style.flexDirection = 'column';  // サブスロットは縦並びが基本
  
  console.log(`🔎 ${parentSlotId}のサブスロット要素数: ${subslots.length}`);
  
  // CSSのorder属性を使用して順序を設定し、未使用のサブスロットを非表示にする
  Array.from(subslots).forEach(el => {
    // IDからサブスロットIDを抽出（例：slot-m1-sub-o1 → o1）
    const idParts = el.id.split('-');
    const subslotId = idParts[idParts.length - 1].toLowerCase();
    
    // 順序を設定
    const orderValue = orderMap.get(subslotId);
    if (orderValue !== undefined) {
      el.style.order = orderValue;
      // データ属性としても設定（デバッグ用）
      el.setAttribute('data-order', orderValue);
      console.log(`🔢 サブスロット "${el.id}" に順序 ${orderValue} を適用`);
    } else {
      console.warn(`⚠ サブスロット "${el.id}" の順序情報が見つかりません`);
      el.style.order = '999'; // 順序不明の場合は末尾に
    }
    
    // 使用状況に応じた表示/非表示を設定
    if (usedSubslots.has(subslotId)) {
      el.style.display = 'flex';  // 表示するときはflex（子要素の配置制御のため）
      console.log(`✅ サブスロット "${el.id}" を表示、順序 ${el.style.order} を適用`);
    } else {
      el.style.display = 'none';
      console.log(`🚫 サブスロット "${el.id}" は未使用のため非表示`);
    }
  });
  
  console.log(`✅ ${parentSlotId}内のサブスロットの表示順と表示状態を適用しました`);
}

// すべての上位スロットを順序付けする関数 - 表示順制御と未使用スロットの非表示
function applyOrderToAllSlots(jsonData) {
  if (!jsonData || !Array.isArray(jsonData)) {
    console.warn("⚠ 順序付けに使用するデータが無効です");
    return;
  }
  
  console.log("🔢 上位スロットの表示順を適用開始");
  
  // 上位スロットのIDとorderマッピングを作成
  const upperSlots = jsonData.filter(item => item.SubslotID === "" && item.PhraseType === "word");
  const slotOrderMap = new Map();
  
  // 使用されているスロットのセット（例文に登場する要素のみ表示するため）
//   const usedSlots = new Set();
  
  // DisplayAtTopフラグを持つスロットのIDを追跡
  const displayAtTopSlots = new Set();
  
  upperSlots.forEach(item => {
    // DisplayAtTopフラグを持つスロットを記録（上部に別途表示されるため通常表示から除外）
    if (item.DisplayAtTop === true) {
      displayAtTopSlots.add(item.Slot.toLowerCase());
      console.log(`🔼 DisplayAtTop対象: ${item.Slot} (${item.DisplayText || ''})`);
      return; // このスロットはorder処理や使用済みセットへの追加をスキップ
    }
    
    // 使用されている（内容がある）スロットを記録
    if (item.SlotPhrase && item.SlotPhrase.trim() !== "") {
      usedSlots.add(item.Slot.toLowerCase());
    }
    
    // order値を取得（display_order、Slot_display_orderまたはorderフィールド）
    const orderValue = item.display_order || item.Slot_display_order || item.order || 0;
    slotOrderMap.set(item.Slot.toLowerCase(), orderValue);
    console.log(`📊 順序マッピング: ${item.Slot.toLowerCase()} => ${orderValue}`);
  });
  
  // 使用中とDisplayAtTopスロットのリストを表示（デバッグ用）
  console.log("📋 使用中スロット:", Array.from(usedSlots).join(', '));
  console.log("🔼 DisplayAtTopスロット:", Array.from(displayAtTopSlots).join(', '));
  
  // マップのエントリを確認
  console.log("📊 スロット順序マップ:", [...slotOrderMap.entries()].map(([id, order]) => `${id}:${order}`).join(', '));
  
  // 親コンテナを取得
  const slotWrapper = document.querySelector('.slot-wrapper');
  if (!slotWrapper) {
    console.warn("⚠ スロットラッパーが見つかりません");
    return;
  }
  
  // すでにflex設定がされている場合は尊重し、されていない場合のみ設定
  const wrapperStyle = window.getComputedStyle(slotWrapper);
  const currentDisplay = wrapperStyle.display;
  
  // flex表示を明示的に設定して順序制御を有効化
  if (currentDisplay === 'none' || currentDisplay === '') {
    slotWrapper.style.display = 'flex';
  }
  
  // 既存の方向設定を優先（CSSで設定されている可能性がある）
  // フレキシブルディレクション - 既存の方向を尊重
  if (!slotWrapper.style.flexDirection) {
    slotWrapper.style.flexDirection = 'row';
  }
  
  if (!slotWrapper.style.flexWrap) {
    slotWrapper.style.flexWrap = 'wrap';
  }
  
  if (!slotWrapper.style.alignItems) {
    slotWrapper.style.alignItems = 'flex-start';
  }
  
  console.log(`📐 スロットラッパースタイル適用: display=${slotWrapper.style.display}, direction=${slotWrapper.style.flexDirection}`);
  
  // すべての上位スロットコンテナを取得して処理
  const slotContainers = Array.from(slotWrapper.querySelectorAll('.slot-container'));
  console.log(`🔎 検出したスロットコンテナ数: ${slotContainers.length}`);
  
  slotContainers.forEach(container => {
    const slotId = container.id.replace('slot-', '').toLowerCase();
    console.log(`🔍 スロット処理: ${slotId}`);
    
    // 1. DisplayAtTopフラグを持つスロットは非表示（別の場所に表示されるため）
//     if (displayAtTopSlots.has(slotId)) {
//       container.style.display = 'none';
//       console.log(`🚫 スロット "${slotId}" はDisplayAtTopのため非表示`);
//       return;
//     }
    
    // 2. 表示順の適用
    const orderValue = slotOrderMap.get(slotId);
    if (orderValue !== undefined) {
      container.style.order = orderValue;
      // データ属性としても設定（CSSセレクタで使用可能）
      container.setAttribute('data-order', orderValue);
      console.log(`🔢 スロット "${slotId}" に順序 ${orderValue} を適用`);
    } else {
      console.warn(`⚠ スロット "${slotId}" の順序情報が見つかりません`);
      container.style.order = '999'; // 末尾に配置
    }
    
    // 3. 使用状況に応じた表示/非表示の設定
    if (usedSlots.has(slotId)) {
      container.style.display = 'flex';
      console.log(`✅ スロット "${slotId}" を表示、順序 ${container.style.order} を適用`);
    } else {
      container.style.display = 'none';
      console.log(`🚫 スロット "${slotId}" は未使用のため非表示`);
    }
  });
  
  console.log("✅ 上位スロットの表示順と表示状態の適用完了");
}

// 動的エリアから静的DOMへの同期関数
function syncDynamicToStatic() {
  console.log("🔄 syncDynamicToStatic 実行開始");
  // 🔼 DisplayAtTop 対応（分離疑問詞表示）
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

        // 直接の子要素としてのslot-phrase
        const phraseDiv = container.querySelector(":scope > .slot-phrase");
        console.log("上位スロットのphraseDiv:", phraseDiv ? phraseDiv.outerHTML : "未検出");
        
        const textDiv = container.querySelector(".slot-text");
        console.log("上位スロットのtextDiv:", textDiv ? textDiv.outerHTML : "未検出");
        
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
    
    // 元のサブスロット書き込み処理
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

    // phraseとtextを更新
    const phraseElement = slotElement.querySelector(".slot-phrase");
    const slotTextElement = slotElement.querySelector(".slot-text");

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

// DisplayAtTop に対応する疑問詞をページ上部に表示する処理
function displayTopQuestionWord() {
  const topDisplayItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
  if (topDisplayItem && topDisplayItem.DisplayText) {
    const topDiv = document.getElementById("display-top-question-word");
    if (topDiv) {
      topDiv.textContent = topDisplayItem.DisplayText;
      console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
    } else {
      console.warn("⚠ display-top-question-word が見つかりません");
    }
  }
  
  // 遅延表示（DOM操作タイミングの保険）
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
  if (!data || !Array.isArray(data)) {
    console.error("❌ 上位スロット同期: 無効なデータが渡されました", data);
    return;
  }
  
  const upperSlotCount = data.filter(item => item.SubslotID === "" && item.PhraseType === "word").length;
  console.log(`🔄 上位スロット同期: ${upperSlotCount}件の対象を処理`);

//   // 詳細ログはデバッグが必要な時だけ出す
//   if (window.DEBUG_SYNC) {
//     console.log("📊 データサンプル:", JSON.stringify(data.slice(0, 3))); // 最初の3件だけ表示
//   }
  
  // グローバル変数がなければ初期化
  if (typeof window.DEBUG_SYNC === 'undefined') {
    window.DEBUG_SYNC = false;
  }
  
  data.forEach(item => {
    if (item.SubslotID === "" && item.PhraseType === "word") {
      console.log("🔍 上位スロット処理開始:", JSON.stringify(item));
      const slotId = "slot-" + item.Slot.toLowerCase();
      console.log("👉 探索するスロットID:", slotId);
      
      const container = document.getElementById(slotId);
      if (container) {
        console.log("✅ スロットコンテナ発見:", container.id);
        
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
        } else {
          console.warn(`❌ 上位textDiv取得失敗: ${slotId}`);
        }
      } else {
        console.warn(`❌ 上位スロットが見つかりません: ${slotId}`);
      }
    }
  });
}

// ✅ サブスロット同期機能の実装
function syncSubslotsFromJson(data) {
  console.log("🔄 サブスロット同期（from window.loadedJsonData）開始");
  if (!data || !Array.isArray(data)) {
    console.warn("⚠ サブスロット同期: データが無効です");
    return;
  }
  
  // サブスロット用のデータをフィルタリング
  const subslotData = data.filter(item => item.SubslotID && item.SubslotID !== "");
  console.log(`📊 サブスロット対象件数: ${subslotData.length}`);
  
  subslotData.forEach(item => {
    try {
      // スロット要素ID構築（slot-[親スロット名]-[サブスロットID]形式）
      const parentSlot = item.Slot.toLowerCase();
      const subslotId = item.SubslotID.toLowerCase();
      const fullSlotId = `slot-${parentSlot}-${subslotId}`;
      console.log(`🔍 サブスロット処理: ${fullSlotId}`);
      
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
    } catch (err) {
      console.error(`❌ サブスロット処理エラー: ${err.message}`, item);
    }
  });
  
  console.log("✅ サブスロット同期完了");
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
// window.syncUpperSlotsFromJson = syncUpperSlotsFromJson;
// window.syncSubslotsFromJson = syncSubslotsFromJson;
// window.debugM1Slot = debugM1Slot;
// window.displayTopQuestionWord = displayTopQuestionWord;
// window.applyOrderToAllSlots = applyOrderToAllSlots;
// window.reorderSubslots = reorderSubslots;

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
    
    // 新機能：表示順の適用処理
    try {
      // スロットの表示順を適用
      if (typeof applyOrderToAllSlots === 'function') {
        applyOrderToAllSlots(data);
        console.log("✅ スロット表示順の適用が完了");
      }
      
      // 必要に応じて個別のサブスロット順序を適用（特定の上位スロットのみ）
      // M1スロットのサブスロット順序設定例
      if (typeof reorderSubslots === 'function') {
        // もっとも重要な構文スロットのサブスロット順序を整理
        reorderSubslots('slot-m1', data);
        reorderSubslots('slot-s', data);
        reorderSubslots('slot-v', data);
        reorderSubslots('slot-c', data);
        reorderSubslots('slot-o', data);
        console.log("✅ 主要スロットのサブスロット順序適用が完了");
      }
    } catch (orderError) {
      console.error("❌ 表示順適用中にエラーが発生:", orderError.message);
    }
    
    // 同期完了
    window.isSyncInProgress = false;
  } catch (err) {
    console.error("❌ 同期処理中にエラーが発生しました:", err.message);
    console.error("エラーの詳細:", err.stack);
    window.isSyncInProgress = false; // エラーが発生してもフラグはリセット
  }
};

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
    const randomizerButtons = document.querySelectorAll('button[data-action="randomize"], button.randomize-button, #randomize-all');
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
            
            // 表示順制御も再適用
            if (typeof applyOrderToAllSlots === 'function') {
              console.log("🔢 ランダマイズ後のスロット表示順適用");
              applyOrderToAllSlots(window.loadedJsonData);
            }
            
            // 全体の再同期
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
            
            // 表示順制御も再適用
            if (typeof applyOrderToAllSlots === 'function') {
              console.log("🔢 randomizeAllSlots後のスロット表示順適用");
              applyOrderToAllSlots(window.loadedJsonData);
            }
            
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
  
  // 動的エリアの位置調整
  ensureDynamicAreaPosition();
  
  setTimeout(() => {
    // ①監視を設定
    window.setupSyncObserver();
    window.setupRandomizerSync();
    
    // ②強制的に順序制御を実行（最初の表示時）
    console.log("🔄 初期表示時の順序制御を強制実行します");
    if (window.loadedJsonData) {
      // 表示順制御を優先的に適用
      if (typeof applyOrderToAllSlots === 'function') {
        applyOrderToAllSlots(window.loadedJsonData);
      }
      
      // 最重要な構文スロットのサブスロット順序を優先的に適用
      if (typeof reorderSubslots === 'function') {
        ['slot-m1', 'slot-s', 'slot-v', 'slot-c', 'slot-o'].forEach(slotId => {
          reorderSubslots(slotId, window.loadedJsonData);
        });
      }
      
      // その後で全体同期を実行
      window.safeJsonSync(window.loadedJsonData);
    }
    
    // ③追加の保険：1秒後にもう一度順序制御を実行（全てのDOM要素が確実にロードされた後）
    setTimeout(() => {
      console.log("🔄 遅延実行の順序制御をトリガー（DOM完全ロード後）");
      if (window.loadedJsonData) {
        if (typeof applyOrderToAllSlots === 'function') {
          applyOrderToAllSlots(window.loadedJsonData);
        }
        
        // 全てのスロットに対してサブスロット順序も適用
        const allSlotContainers = document.querySelectorAll('.slot-container');
        if (typeof reorderSubslots === 'function' && allSlotContainers.length > 0) {
          Array.from(allSlotContainers).forEach(container => {
            if (container.id.startsWith('slot-')) {
              reorderSubslots(container.id, window.loadedJsonData);
            }
          });
        }
      }
    }, 1000);
    
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
          
          // 順序制御も優先的に実行
          if (typeof applyOrderToAllSlots === 'function') {
            applyOrderToAllSlots(window.loadedJsonData);
            console.log("✅ 定期チェックによる順序制御を実行しました");
          }
          
          window.safeJsonSync(window.loadedJsonData);
          lastJsonDataSignature = newSignature;
        }
      }
      
      // 定期的に動的エリアの位置も確認
      ensureDynamicAreaPosition();
    }, 3000); // 3秒ごとに変更をチェック
    
  }, 500); // DOMが完全に構築されるのを待つ
});

// 動的エリアの位置を調整する関数
function ensureDynamicAreaPosition() {
  // 動的エリアコンテナを取得
  const container = document.getElementById("dynamic-area-container");
  
  // コンテナが存在する場合
  if (container) {
    // コンテナが最後の要素でない場合は移動
    if (container !== document.body.lastElementChild) {
      // すべてのスロット関連要素とサブスロット要素の後に配置する
      document.body.appendChild(container);
      console.log("🔄 動的エリアコンテナを再配置しました");
    }
    
    // 動的エリア内部の調整
    const dynamicArea = document.getElementById("dynamic-slot-area");
    const wrapper = document.getElementById("dynamic-slot-area-wrapper");
    
    if (dynamicArea && wrapper && !wrapper.contains(dynamicArea)) {
      wrapper.appendChild(dynamicArea);
      console.log("🔄 動的エリアをラッパー内に再配置しました");
    }
  }
}
