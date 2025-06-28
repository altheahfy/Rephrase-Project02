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

// 特定のスロットコンテナ内のサブスロットを順序付けする関数
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
    console.log(`ℹ️ ${parentSlotId}には並べ替えが必要なサブスロットが1つ以下です`);
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
    console.warn(`⚠ ${parentId}内にサブスロット要素が見つかりません`);
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
  
  console.log(`✅ ${parentId}内のサブスロットを順序通りに再配置しました`);
}

// すべての上位スロットを順序付けする関数 - CSSのorder属性を使用する安全版
function applyOrderToAllSlots(jsonData) {
  if (!jsonData || !Array.isArray(jsonData)) {
    console.warn("⚠ 順序付けに使用するデータが無効です");
    return;
  }
  
  console.log("🔢 上位スロットの表示順を適用開始");
  
  // 上位スロットのIDとorderマッピングを作成
  const upperSlots = jsonData.filter(item => item.SubslotID === "" && item.PhraseType === "word");
  const slotOrderMap = new Map();
  
  upperSlots.forEach(item => {
    // order値を取得（display_order、Slot_display_orderまたはorderフィールド）
    const orderValue = item.display_order || item.Slot_display_order || item.order || 0;
    slotOrderMap.set(item.Slot.toLowerCase(), orderValue);
  });
  
  // マップのエントリを確認
  console.log("📊 スロット順序マップ:", [...slotOrderMap.entries()]);
  
  // 順序をCSSのorder属性として適用（DOM構造自体は変更しない安全な方法）
  slotOrderMap.forEach((orderValue, slotId) => {
    const slotElement = document.getElementById(`slot-${slotId}`);
    if (slotElement) {
      // CSSのorder属性を設定
      slotElement.style.order = orderValue;
      console.log(`✅ スロット "${slotId}" に表示順 ${orderValue} を適用 (CSS order)`);
    }
  });
  
  // 親コンテナにflexboxレイアウトを適用（必要な場合）
  const slotWrapper = document.querySelector('.slot-wrapper');
  if (slotWrapper) {
    slotWrapper.style.display = 'flex';
    slotWrapper.style.flexDirection = 'column';
    console.log("✅ スロットラッパーにflex表示を適用");
  }
  
  console.log("✅ 上位スロットの表示順適用完了");
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
  // 🧹 DisplayAtTop対象となりうるサブスロットを明示的にクリア
  const displayAtTopItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
  if (displayAtTopItem && displayAtTopItem.DisplayText) {
    console.log(`🧹 DisplayAtTop対象のサブスロットを検索: "${displayAtTopItem.DisplayText}"`);
    
    // 全てのサブスロットから DisplayAtTop.DisplayText と一致するものを探してクリア
    const allSubslots = document.querySelectorAll('[id*="-sub-"]');
    allSubslots.forEach(subslot => {
      const phraseEl = subslot.querySelector('.slot-phrase');
      if (phraseEl && phraseEl.textContent.trim() === displayAtTopItem.DisplayText.trim()) {
        phraseEl.textContent = "";
        console.log(`🧹 DisplayAtTop対象サブスロットをクリア: ${subslot.id}`);
      }
    });
  }
  
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

// DisplayAtTop に対応する疑問詞をページ上部に表示する処理
function displayTopQuestionWord() {
  const topDiv = document.getElementById("display-top-question-word");
  if (!topDiv) {
    console.warn("⚠ display-top-question-word が見つかりません");
    return;
  }

  const topDisplayItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
  if (topDisplayItem && topDisplayItem.DisplayText) {
    topDiv.textContent = topDisplayItem.DisplayText;
    console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
  } else {
    // DisplayAtTopがない場合は表示をクリア
    topDiv.textContent = "";
    console.log("🧹 DisplayAtTop 表示をクリア（該当データなし）");
  }
  
  // 遅延表示（DOM操作タイミングの保険）
  setTimeout(() => {
    const topDisplayItem = window.loadedJsonData?.find(d => d.DisplayAtTop);
    if (topDisplayItem && topDisplayItem.DisplayText) {
      const topDiv = document.getElementById("display-top-question-word");
      if (topDiv) {
        topDiv.textContent = topDisplayItem.DisplayText;
        console.log("✅ DisplayAtTop 表示（遅延）:", topDisplayItem.DisplayText);
      }
    } else {
      // 遅延処理でもクリア
      const topDiv = document.getElementById("display-top-question-word");
      if (topDiv) {
        topDiv.textContent = "";
        console.log("🧹 DisplayAtTop 表示をクリア（遅延・該当データなし）");
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
  
  // 詳細ログはデバッグが必要な時だけ出す
  if (window.DEBUG_SYNC) {
    console.log("📊 データサンプル:", JSON.stringify(data.slice(0, 3))); // 最初の3件だけ表示
  }
  
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

  // 🔍 全ての上位スロットをチェックして空のものを非表示（全スロット対応）
  const upperSlotIds = ['c1', 'm1', 's', 'v', 'o1', 'o2', 'm2', 'c2', 'aux'];
  
  upperSlotIds.forEach(slotId => {
    const slotElement = document.getElementById(`slot-${slotId}`);
    if (slotElement) {
      const phraseDiv = slotElement.querySelector('.slot-phrase');
      const isEmpty = !phraseDiv || !phraseDiv.textContent || phraseDiv.textContent.trim() === '';
      console.log(`🔍 ${slotId.toUpperCase()}スロット空判定: textContent="${phraseDiv?.textContent}" → isEmpty=${isEmpty}`);
      
      if (isEmpty) {
        slotElement.style.display = 'none';
        console.log(`👻 ${slotId.toUpperCase()}スロットを非表示にしました`);
      } else {
        slotElement.style.display = '';
        console.log(`👁 ${slotId.toUpperCase()}スロットを表示状態にしました`);
      }
    } else {
      console.log(`⚠ slot-${slotId}が見つかりません`);
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
  
  // DisplayAtTopの要素を特定（サブスロットから除外するため）
  const displayAtTopItem = data.find(d => d.DisplayAtTop);
  
  // サブスロット用のデータをフィルタリング
  const subslotData = data.filter(item => item.SubslotID && item.SubslotID !== "");
  console.log(`📊 サブスロット対象件数: ${subslotData.length}`);
  
  subslotData.forEach(item => {
    try {
      // DisplayAtTopの要素をサブスロットから除外
      if (displayAtTopItem && 
          displayAtTopItem.DisplayText && 
          item.SubslotElement === displayAtTopItem.DisplayText) {
        console.log(`🚫 DisplayAtTop対象のため除外: ${item.SubslotElement} (${item.Slot}-${item.SubslotID})`);
        return;
      }

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
window.syncUpperSlotsFromJson = syncUpperSlotsFromJson;
window.syncSubslotsFromJson = syncSubslotsFromJson;
window.debugM1Slot = debugM1Slot;
window.displayTopQuestionWord = displayTopQuestionWord;
window.applyOrderToAllSlots = applyOrderToAllSlots;
window.reorderSubslots = reorderSubslots;
window.hideEmptySlots = hideEmptySlots;
window.hideEmptyUpperSlots = hideEmptyUpperSlots;
window.hideEmptySubslots = hideEmptySubslots;
window.hideEmptySubslotContainers = hideEmptySubslotContainers;
window.debugEmptySlots = debugEmptySlots;
window.forceHideEmptySlots = forceHideEmptySlots;

/**
 * 空のスロットを非表示にする機構
 * @param {Array} jsonData - window.loadedJsonData
 */
function hideEmptySlots(jsonData) {
  if (!jsonData || !Array.isArray(jsonData)) {
    console.warn("⚠ hideEmptySlots: JSONデータが無効なため、静的DOM解析に切り替えます");
    // JSONデータが無効な場合は forceHideEmptySlots を使用
    forceHideEmptySlots();
    return;
  }

  console.log("🙈 === 空のスロット非表示処理を開始（JSONベース）===");
  console.log(`📊 処理対象データ件数: ${jsonData.length}`);

  // 改良された方式：forceHideEmptySlots を使用（より信頼性が高い）
  forceHideEmptySlots();

  console.log("✅ === 空のスロット非表示処理が完了 ===");
}

/**
 * 空の上位スロットを非表示にする（改良版：サブスロットの存在も考慮）
 * @param {Array} jsonData - JSONデータ
 */
function hideEmptyUpperSlots(jsonData) {
  // 上位スロットデータを取得
  const upperSlots = jsonData.filter(item => 
    item.SubslotID === "" && item.PhraseType === "word"
  );

  console.log(`🔍 上位スロット非表示チェック: ${upperSlots.length}件`);

  upperSlots.forEach(item => {
    const slotId = `slot-${item.Slot.toLowerCase()}`;
    const slotElement = document.getElementById(slotId);
    
    if (!slotElement) {
      console.warn(`⚠ 上位スロット要素が見つかりません: ${slotId}`);
      return;
    }

    // 上位スロット自体が空かどうかを判定
    const upperSlotIsEmpty = (!item.SlotPhrase || item.SlotPhrase.trim() === "") && 
                           (!item.SlotText || item.SlotText.trim() === "");

    // この上位スロットに関連するサブスロットを確認
    const relatedSubslots = jsonData.filter(subItem => 
      subItem.Slot.toLowerCase() === item.Slot.toLowerCase() && 
      subItem.SubslotID && 
      subItem.SubslotID !== ""
    );

    // 関連サブスロットのうち、空でないものがあるかチェック
    const hasNonEmptySubslots = relatedSubslots.some(subItem => 
      (subItem.SubslotElement && subItem.SubslotElement.trim() !== "") ||
      (subItem.SubslotText && subItem.SubslotText.trim() !== "")
    );

    console.log(`🔍 上位スロット [${item.Slot}]:`);
    console.log(`  - 上位スロット自体が空: ${upperSlotIsEmpty}`);
    console.log(`  - 関連サブスロット数: ${relatedSubslots.length}`);
    console.log(`  - 空でないサブスロットあり: ${hasNonEmptySubslots}`);

    // 判定：上位スロット自体が空 かつ 空でないサブスロットがない場合のみ非表示
    const shouldHide = upperSlotIsEmpty && !hasNonEmptySubslots;

    if (shouldHide) {
      slotElement.style.display = "none";
      slotElement.classList.add("empty-slot-hidden", "hidden");
      console.log(`🙈 上位スロットを非表示: ${slotId} (理由: 上位・サブスロット共に空)`);
    } else {
      slotElement.style.display = "";
      slotElement.classList.remove("empty-slot-hidden", "hidden");
      if (upperSlotIsEmpty && hasNonEmptySubslots) {
        console.log(`👁 上位スロットを表示: ${slotId} (理由: サブスロットに内容あり)`);
      } else if (!upperSlotIsEmpty) {
        console.log(`👁 上位スロットを表示: ${slotId} (理由: 上位スロットに内容あり)`);
      }
    }
  });
}

/**
 * 空のサブスロットを非表示にする
 * @param {Array} jsonData - JSONデータ
 */
function hideEmptySubslots(jsonData) {
  // サブスロットデータを取得
  const subSlots = jsonData.filter(item => 
    item.SubslotID && item.SubslotID !== ""
  );

  console.log(`🔍 サブスロット非表示チェック: ${subSlots.length}件`);

  subSlots.forEach(item => {
    const parentSlot = item.Slot.toLowerCase();
    const subslotId = item.SubslotID.toLowerCase();
    const fullSlotId = `slot-${parentSlot}-${subslotId}`;
    const slotElement = document.getElementById(fullSlotId);
    
    if (!slotElement) {
      console.warn(`⚠ サブスロット要素が見つかりません: ${fullSlotId}`);
      return;
    }

    // DisplayAtTop対象は非表示判定から除外
    const displayAtTopItem = jsonData.find(d => d.DisplayAtTop);
    const isDisplayAtTopTarget = displayAtTopItem && 
                                displayAtTopItem.DisplayText && 
                                item.SubslotElement === displayAtTopItem.DisplayText;

    if (isDisplayAtTopTarget) {
      // DisplayAtTop対象は強制的に非表示（別途上部に表示されるため）
      slotElement.style.display = "none";
      slotElement.classList.add("display-at-top-hidden", "hidden");
      console.log(`🚫 DisplayAtTop対象サブスロットを非表示: ${fullSlotId}`);
      return;
    }

    // 空かどうかを判定（SubslotElementとSubslotTextが両方とも空）
    const isEmpty = (!item.SubslotElement || item.SubslotElement.trim() === "") && 
                   (!item.SubslotText || item.SubslotText.trim() === "");

    if (isEmpty) {
      slotElement.style.display = "none";
      slotElement.classList.add("empty-slot-hidden", "hidden");
      console.log(`🙈 サブスロットを非表示: ${fullSlotId}`);
    } else {
      slotElement.style.display = "";
      slotElement.classList.remove("empty-slot-hidden", "display-at-top-hidden", "hidden");
      console.log(`👁 サブスロットを表示: ${fullSlotId}`);
    }
  });
}

/**
 * 全てのサブスロットが非表示の場合、サブスロットコンテナも非表示にする
 */
function hideEmptySubslotContainers() {
  // 全てのサブスロットコンテナを取得
  const subslotContainers = document.querySelectorAll('[id^="slot-"][id$="-sub"]');
  
  console.log(`🔍 サブスロットコンテナ非表示チェック: ${subslotContainers.length}件`);

  subslotContainers.forEach(container => {
    // コンテナ内の全サブスロット要素を取得
    const subslots = container.querySelectorAll('[id*="-sub-"]');
    
    if (subslots.length === 0) {
      // サブスロットが存在しない場合は非表示
      container.style.display = "none";
      container.classList.add("empty-container-hidden", "hidden");
      console.log(`🙈 空のサブスロットコンテナを非表示: ${container.id}`);
      return;
    }

    // 表示されているサブスロットの数をカウント
    const visibleSubslots = Array.from(subslots).filter(subslot => 
      window.getComputedStyle(subslot).display !== "none"
    );

    if (visibleSubslots.length === 0) {
      // 全てのサブスロットが非表示の場合、コンテナも非表示
      container.style.display = "none";
      container.classList.add("empty-container-hidden", "hidden");
      console.log(`🙈 全サブスロット非表示のためコンテナを非表示: ${container.id}`);
    } else {
      // 表示されているサブスロットがある場合、コンテナを表示
      container.style.display = "";
      container.classList.remove("empty-container-hidden", "hidden");
      console.log(`👁 サブスロットコンテナを表示: ${container.id} (表示中サブスロット: ${visibleSubslots.length}件)`);
    }
  });
}

// 指定されたコンテナ内のサブスロットを order に従ってDOMを直接並べ替える関数
function reorderSubslotsInContainer(container, jsonData) {
  if (!container || !jsonData) {
    console.warn("⚠ reorderSubslotsInContainer: コンテナまたはデータがありません");
    return;
  }
  const subslots = container.querySelectorAll(".subslot");
  if (subslots.length <= 1) {
    console.log(`ℹ️ ${container.id} には並べ替えが必要なサブスロットが1つ以下です`);
    return; // 並べ替える必要なし
  }

  console.log(`🔢 DOM並べ替え実行: ${container.id} (${subslots.length}個の要素)`);

  // container.id = "slot-m1-sub" -> parentSlotId = "m1"
  const parentSlotId = container.id.replace("slot-", "").replace("-sub", "").toUpperCase();
  console.log(`親スロットID: ${parentSlotId}`);

  const elementsWithOrder = Array.from(subslots).map(el => {
    // 'slot-m1-sub-s' から 's' を取り出し、'sub-s' 形式にする
    const subId = el.id.substring(el.id.lastIndexOf('-') + 1);
    const fullSubslotId = `sub-${subId}`;
    console.log(`  - 処理中のサブスロット要素: ${el.id} (検索ID: ${fullSubslotId})`);
    
    // 親スロットと SubslotID の両方でマッチング
    const data = jsonData.find(d => 
      d.Slot?.toUpperCase() === parentSlotId && 
      d.SubslotID?.toLowerCase() === fullSubslotId.toLowerCase()
    );
    const order = data ? data.display_order : 999;
    
    if(data){
        console.log(`    ✅ データ発見 (Slot: ${data.Slot}, SubslotID: ${data.SubslotID}), order=${order}`);
    } else {
        console.log(`    ❌ データ未発見 (親: ${parentSlotId}, SubslotID: ${fullSubslotId})`);
    }
    
    return { el, order };
  });

  elementsWithOrder.sort((a, b) => a.order - b.order);

  console.log("📊 ソート後の順序:", elementsWithOrder.map(item => ({id: item.el.id, order: item.order})));
  
  console.log("🔄 DOM要素の再配置を開始");
  elementsWithOrder.forEach(item => {
    container.appendChild(item.el);
  });

  console.log(`✅ DOM並べ替え完了: ${container.id}`);
}

// 新しい順序付け関数
function applyDisplayOrder(data) {
  if (!data || !Array.isArray(data)) {
    console.warn("⚠ applyDisplayOrder: 無効なデータです");
    return;
  }

  console.log("🔢 表示順序の適用を開始します");
  const dynamicArea = document.getElementById('dynamic-slot-area');
  // dynamicAreaが存在しない場合は処理を中断
  if (!dynamicArea) {
      console.error("❌ 動的記載エリア #dynamic-slot-area が見つかりません。順序付けを中止します。");
      return;
  }

  // 上位スロットの順序を適用
  const upperSlots = data.filter(item => !item.SubslotID || item.SubslotID === "");
  upperSlots.forEach(item => {
    if (item.Slot && typeof item.Slot_display_order !== 'undefined') {
      const slotElement = document.getElementById(`slot-${item.Slot.toLowerCase()}`);
      // 要素が存在し、かつ動的エリアの子要素ではない場合にのみ処理
      if (slotElement && !dynamicArea.contains(slotElement)) {
        slotElement.style.order = item.Slot_display_order;
        console.log(`✅ 静的上位スロット[${slotElement.id}]に order: ${item.Slot_display_order} を適用`);
      }
    }
  });

  // サブスロットの順序を適用
  const subSlots = data.filter(item => item.SubslotID && item.SubslotID !== "");
  subSlots.forEach(item => {
    if (item.Slot && item.SubslotID && typeof item.display_order !== 'undefined') {
      const subSlotElement = document.getElementById(`slot-${item.Slot.toLowerCase()}-sub-${item.SubslotID.toLowerCase()}`);
      // 要素が存在し、かつ動的エリアの子要素ではない場合にのみ処理
      if (subSlotElement && !dynamicArea.contains(subSlotElement)) {
        subSlotElement.style.order = item.display_order;
        console.log(`✅ 静的サブスロット[${subSlotElement.id}]に order: ${item.display_order} を適用`);
      }
    }
  });

  // すべてのサブスロットコンテナに flexbox を適用して order を有効化
  const subSlotContainers = document.querySelectorAll('[id$="-sub"]');
  subSlotContainers.forEach(container => {
      // .visible クラスを持つ（＝表示されている）コンテナのみを対象
      if (container.classList.contains('visible')) {
          container.style.display = 'flex';
          container.style.flexWrap = 'wrap';
          container.style.gap = '8px';
          console.log(`✅ サブスロットコンテナ [${container.id}] にflexboxを適用`);
      }
  });

  console.log("✅ 表示順序の適用が完了しました");
}

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
    
    // 分離疑問詞表示の更新
    try {
      if (typeof displayTopQuestionWord === 'function') {
        displayTopQuestionWord();
        console.log("✅ 分離疑問詞表示の更新が完了");
      }
    } catch (displayError) {
      console.error("❌ 分離疑問詞表示更新中にエラーが発生:", displayError.message);
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

      // ★新しい順序付け関数を呼び出す
      applyDisplayOrder(data);

    } catch (orderError) {
      console.error("❌ 表示順適用中にエラーが発生しました:", orderError.message);
    }
    
    // 空のスロット非表示処理
    try {
      if (typeof hideEmptySlots === 'function') {
        hideEmptySlots(data);
        console.log("✅ 空のスロット非表示処理が完了");
      }
    } catch (hideError) {
      console.error("❌ 空のスロット非表示処理中にエラーが発生:", hideError.message);
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
      
      // 定期的に動的エリアの位置も確認
      ensureDynamicAreaPosition();
    }, 3000); // 3秒ごとに変更をチェック
    
    // 「詳細」ボタンクリック時に順序を再適用する
    document.body.addEventListener('click', (event) => {
        // クリックされたのが「.slot-container」内の要素かチェック
        const slotContainer = event.target.closest('.slot-container');
        if (slotContainer) {
            console.log('スロットコンテナ内の要素がクリックされました。100ms後に順序を再適用します。');
            // 元のスクリプトがコンテナを表示するのを待つために少し遅延させる
            setTimeout(() => {
                if (window.loadedJsonData) {
                    applyDisplayOrder(window.loadedJsonData);
                }
            }, 100); // 100ミリ秒の遅延
        }
    });
    
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

/**
 * デバッグ用：空のスロット検出状況を詳細にレポートする関数
 */
function debugEmptySlots() {
  if (!window.loadedJsonData) {
    console.warn("⚠ window.loadedJsonData が存在しません");
    return;
  }

  console.log("🔍 === 空のスロット検出デバッグ開始 ===");
  
  // 上位スロットの状況確認
  const upperSlots = window.loadedJsonData.filter(item => 
    item.SubslotID === "" && item.PhraseType === "word"
  );
  
  console.log(`📊 上位スロット総数: ${upperSlots.length}`);
  upperSlots.forEach(item => {
    const slotId = `slot-${item.Slot.toLowerCase()}`;
    const slotElement = document.getElementById(slotId);
    const isEmpty = (!item.SlotPhrase || item.SlotPhrase.trim() === "") && 
                   (!item.SlotText || item.SlotText.trim() === "");
    
    console.log(`🔍 上位スロット [${item.Slot}]:`);
    console.log(`  - SlotPhrase: "${item.SlotPhrase}"`);
    console.log(`  - SlotText: "${item.SlotText}"`);
    console.log(`  - isEmpty: ${isEmpty}`);
    console.log(`  - DOM要素存在: ${!!slotElement}`);
    if (slotElement) {
      console.log(`  - 現在のdisplay: ${window.getComputedStyle(slotElement).display}`);
      console.log(`  - クラス: ${slotElement.className}`);
    }
  });

  // サブスロットの状況確認
  const subSlots = window.loadedJsonData.filter(item => 
    item.SubslotID && item.SubslotID !== ""
  );
  
  console.log(`📊 サブスロット総数: ${subSlots.length}`);
  subSlots.forEach(item => {
    const parentSlot = item.Slot.toLowerCase();
    const subslotId = item.SubslotID.toLowerCase();
    const fullSlotId = `slot-${parentSlot}-${subslotId}`;
    const slotElement = document.getElementById(fullSlotId);
    const isEmpty = (!item.SubslotElement || item.SubslotElement.trim() === "") && 
                   (!item.SubslotText || item.SubslotText.trim() === "");
    
    console.log(`🔍 サブスロット [${item.Slot}-${item.SubslotID}]:`);
    console.log(`  - SubslotElement: "${item.SubslotElement}"`);
    console.log(`  - SubslotText: "${item.SubslotText}"`);
    console.log(`  - isEmpty: ${isEmpty}`);
    console.log(`  - DOM要素存在: ${!!slotElement}`);
    if (slotElement) {
      console.log(`  - 現在のdisplay: ${window.getComputedStyle(slotElement).display}`);
      console.log(`  - クラス: ${slotElement.className}`);
    }
  });

  console.log("✅ === 空のスロット検出デバッグ終了 ===");
}

/**
 * 強制的に空のスロットを非表示にするテスト関数（デバッグ用・改良版）
 */
function forceHideEmptySlots() {
  console.log("🚀 === 強制的な空のスロット非表示テスト（全スロット対応版）===");
  
  // 対象となる全上位スロット名
  const targetSlots = ['c1', 'm1', 's', 'v', 'o1', 'o2', 'm2', 'c2', 'm3', 'aux'];
  
  console.log(`🎯 対象上位スロット: ${targetSlots.join(', ')}`);
  
  let hiddenCount = 0;
  let visibleCount = 0;
  
  targetSlots.forEach(slotName => {
    const slotId = `slot-${slotName}`;
    const slot = document.getElementById(slotId);
    
    if (!slot) {
      console.warn(`⚠ スロット要素が見つかりません: ${slotId}`);
      return;
    }
    
    const phraseEl = slot.querySelector('.slot-phrase');
    const textEl = slot.querySelector('.slot-text');
    
    const phraseText = phraseEl ? phraseEl.textContent.trim() : '';
    const textText = textEl ? textEl.textContent.trim() : '';
    
    // この上位スロットに関連するサブスロットを確認
    const relatedSubSlots = document.querySelectorAll(`[id^="slot-${slotName}-sub-"]`);
    
    // 関連サブスロットの内容を詳細チェック
    const subSlotContents = [];
    let hasNonEmptySubslots = false;
    
    relatedSubSlots.forEach(subSlot => {
      const subPhraseEl = subSlot.querySelector('.slot-phrase');
      const subTextEl = subSlot.querySelector('.slot-text');
      const subPhraseText = subPhraseEl ? subPhraseEl.textContent.trim() : '';
      const subTextText = subTextEl ? subTextEl.textContent.trim() : '';
      
      subSlotContents.push({
        id: subSlot.id,
        phrase: subPhraseText,
        text: subTextText,
        isEmpty: subPhraseText === '' && subTextText === ''
      });
      
      if (subPhraseText !== '' || subTextText !== '') {
        hasNonEmptySubslots = true;
      }
    });
    
    console.log(`🔍 ${slotId}:`);
    console.log(`  📝 上位スロット内容:`);
    console.log(`    - phrase: "${phraseText}"`);
    console.log(`    - text: "${textText}"`);
    console.log(`  📁 関連サブスロット: ${relatedSubSlots.length}件`);
    
    if (subSlotContents.length > 0) {
      console.log(`  🔍 サブスロット詳細:`);
      subSlotContents.forEach(sub => {
        console.log(`    - ${sub.id}: phrase="${sub.phrase}", text="${sub.text}", 空=${sub.isEmpty}`);
      });
    }
    
    // 判定：上位スロット自体が空 かつ 空でないサブスロットがない場合のみ非表示
    const upperSlotIsEmpty = phraseText === '' && textText === '';
    const shouldHide = upperSlotIsEmpty && !hasNonEmptySubslots;
    
    console.log(`  📊 判定結果:`);
    console.log(`    - 上位スロット空: ${upperSlotIsEmpty}`);
    console.log(`    - 空でないサブスロットあり: ${hasNonEmptySubslots}`);
    console.log(`    - 最終判定（非表示）: ${shouldHide}`);
    
    if (shouldHide) {
      console.log(`  🙈 非表示に設定: ${slotId}`);
      slot.style.display = 'none';
      slot.classList.add('empty-slot-hidden', 'hidden');
      hiddenCount++;
    } else {
      const reason = !upperSlotIsEmpty ? '上位スロットに内容あり' : 'サブスロットに内容あり';
      console.log(`  👁 表示維持: ${slotId} (理由: ${reason})`);
      slot.style.display = '';
      slot.classList.remove('empty-slot-hidden', 'hidden');
      visibleCount++;
    }
    
    console.log(`  ─────────────────────────────────`);
  });
  
  // サブスロットの処理
  console.log("🔧 === サブスロット非表示処理 ===");
  const allSubSlots = document.querySelectorAll('[id*="-sub-"]');
  console.log(`📊 検出されたサブスロット: ${allSubSlots.length}件`);
  
  let hiddenSubSlotCount = 0;
  let visibleSubSlotCount = 0;
  
  allSubSlots.forEach(slot => {
    const phraseEl = slot.querySelector('.slot-phrase');
    const textEl = slot.querySelector('.slot-text');
    
    const phraseText = phraseEl ? phraseEl.textContent.trim() : '';
    const textText = textEl ? textEl.textContent.trim() : '';
    
    const isEmpty = phraseText === '' && textText === '';
    
    console.log(`🔍 ${slot.id}: phrase="${phraseText}", text="${textText}", 空=${isEmpty}`);
    
    if (isEmpty) {
      console.log(`  🙈 空のため非表示に設定: ${slot.id}`);
      slot.style.display = 'none';
      slot.classList.add('empty-slot-hidden', 'hidden');
      hiddenSubSlotCount++;
    } else {
      console.log(`  👁 表示維持: ${slot.id}`);
      slot.style.display = '';
      slot.classList.remove('empty-slot-hidden', 'hidden');
      visibleSubSlotCount++;
    }
  });
  
  console.log("📊 === 処理結果サマリー ===");
  console.log(`🎯 上位スロット - 非表示: ${hiddenCount}件, 表示: ${visibleCount}件`);
  console.log(`📁 サブスロット - 非表示: ${hiddenSubSlotCount}件, 表示: ${visibleSubSlotCount}件`);
  console.log("✅ === 空のスロット非表示処理完了 ===");
}

/**
 * 空のスロット非表示機能のテスト用関数
 */
function testEmptySlotHiding() {
  console.log("🧪 === 空のスロット非表示機能テスト ===");
  
  // 現在の表示状態を記録
  const beforeState = {};
  const allSlots = document.querySelectorAll('[id^="slot-"]');
  allSlots.forEach(slot => {
    beforeState[slot.id] = {
      display: slot.style.display,
      visible: slot.style.display !== 'none'
    };
  });
  
  console.log("📊 テスト前の状態:", beforeState);
  
  // 空のスロット非表示を実行
  forceHideEmptySlots();
  
  // テスト後の状態を記録
  const afterState = {};
  allSlots.forEach(slot => {
    afterState[slot.id] = {
      display: slot.style.display,
      visible: slot.style.display !== 'none'
    };
  });
  
  console.log("📊 テスト後の状態:", afterState);
  
  // 変更があったスロットを報告
  const changes = [];
  Object.keys(beforeState).forEach(slotId => {
    if (beforeState[slotId].visible !== afterState[slotId].visible) {
      changes.push({
        slotId,
        before: beforeState[slotId].visible ? '表示' : '非表示',
        after: afterState[slotId].visible ? '表示' : '非表示'
      });
    }
  });
  
  console.log("🔄 変更されたスロット:", changes);
  console.log("✅ === テスト完了 ===");
  
  return { beforeState, afterState, changes };
}

// グローバルに公開
window.testEmptySlotHiding = testEmptySlotHiding;
