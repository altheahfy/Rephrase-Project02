// insert_test_data.js をベースにした動的記載エリアから静的DOM同期用スクリプト
// 
// ⚠️⚠️⚠️【重要警告】⚠️⚠️⚠️
// 動的記載エリア(dynamic-slot-area)は絶対に変更禁止！
// - DOM構造の変更厳禁
// - 位置の移動厳禁  
// - ラッパーへの移動厳禁
// - 読み取り専用でのみ使用可能
// ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

// 疑問詞エリアを初期化して確実に空状態にする関数
function initializeQuestionWordArea() {
  const topDiv = document.getElementById("display-top-question-word");
  if (topDiv) {
    topDiv.textContent = "";
    topDiv.innerHTML = ""; // HTMLも完全にクリア
    topDiv.classList.add("empty-content"); // 強制的に空クラスを追加
    console.log("🧹 疑問詞エリアを初期化しました");
  }
  
  // 動的エリアの疑問詞も削除
  const dynamicQuestionDiv = document.getElementById("dynamic-question-word");
  if (dynamicQuestionDiv) {
    dynamicQuestionDiv.remove();
    console.log("🧹 動的エリアの疑問詞を削除しました");
  }
}

// 動的エリアからデータを抽出する関数
// ⚠️【編集禁止】動的記載エリア(dynamic-slot-area)は読み取り専用です
function extractDataFromDynamicArea() {
  // ⚠️【編集禁止】この関数は動的記載エリアからの読み取りのみ行います
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
        topDiv.classList.remove("empty-content"); // 空クラスを削除
        console.log("✅ DisplayAtTop 表示: " + topDisplayItem.DisplayText);
      } else {
        console.warn("⚠ display-top-question-word が見つかりません");
      }
    } else {
      // DisplayAtTopがない場合はクリア
      const topDiv = document.getElementById("display-top-question-word");
      if (topDiv) {
        topDiv.textContent = "";
        topDiv.innerHTML = ""; // HTMLも完全にクリア
        topDiv.classList.add("empty-content"); // 強制的に空クラスを追加
        console.log("🧹 DisplayAtTop 表示をクリア（syncDynamicToStatic）");
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
    const topDisplay = window.loadedJsonData?.find(d => d.DisplayAtTop);
    if (topDisplay && topDisplay.DisplayText) {
      const topDiv = document.getElementById("display-top-question-word");
      if (topDiv) {
        topDiv.textContent = topDisplay.DisplayText;
        topDiv.classList.remove("empty-content"); // 空クラスを削除
        console.log(`🔼 DisplayAtTop 表示: ${topDisplay.DisplayText}`);
      } else {
        console.warn("⚠ display-top-question-word が見つかりません");
      }
    } else {
      // DisplayAtTopがない場合はクリア
      const topDiv = document.getElementById("display-top-question-word");
      if (topDiv) {
        topDiv.textContent = "";
        topDiv.innerHTML = ""; // HTMLも完全にクリア
        topDiv.classList.add("empty-content"); // 強制的に空クラスを追加
        console.log("🧹 DisplayAtTop 表示をクリア（動的エリア抽出失敗時）");
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

    // 📝 フレーズ要素への書き込み（例文テキスト - Grid行4配置責任）
    if (phraseElement) {
      phraseElement.textContent = item.SlotPhrase || "";
      // 🎯 サブスロット配置責任：insert_test_data_clean.jsがGrid行4（例文テキスト）を管理
      phraseElement.style.gridRow = '4';
      phraseElement.style.gridColumn = '1';
      console.log(`✅ サブスロット phrase書き込み成功: ${item.Slot} | 値: "${item.SlotPhrase}" | Grid行4配置`);
    } else {
      console.warn(`❌ サブスロット phrase要素取得失敗: ${item.Slot}`);
    }
    
    // 📝 テキスト要素への書き込み（補助テキスト - Grid行3配置責任）
    if (slotTextElement) {
      slotTextElement.textContent = item.SlotText || "";
      // 🎯 サブスロット配置責任：insert_test_data_clean.jsがGrid行3（補助テキスト）を管理
      slotTextElement.style.gridRow = '3';
      slotTextElement.style.gridColumn = '1';
      console.log(`✅ サブスロット text書き込み成功: ${item.Slot} | 値: "${item.SlotText}" | Grid行3配置`);
      
      // 上位スロットと同じ入れ子構造チェック
      const nestedPhraseDiv = slotTextElement.querySelector(".slot-phrase");
      if (nestedPhraseDiv) {
        console.warn(`⚠️ サブスロット slotTextElement内にslot-phraseが入れ子になっています: ${item.Slot}`);
        console.warn(`⚠️ この入れ子構造が原因で書き込みが上書きされている可能性があります`);
      }
    } else {
      console.warn(`❌ サブスロット text要素取得失敗: ${item.Slot}`);
    }

    // 🖼️ サブスロット用複数画像表示システム（上位スロットと同じ方式）
    // SubslotIDがある場合は、メインスロットのテキストで複数画像検索
    let textForImage = "";
    if (item.SubslotID && window.loadedJsonData) {
      // メインスロット（SubslotID = ""）のデータを探す
      const mainSlotData = window.loadedJsonData.find(dataItem => 
        dataItem.Slot === item.Slot && 
        dataItem.SubslotID === "" && 
        dataItem.PhraseType === "word"
      );
      if (mainSlotData) {
        textForImage = mainSlotData.SlotText || mainSlotData.SlotPhrase || "";
        console.log(`� サブスロット${item.Slot}-${item.SubslotID}: メインスロットのテキスト使用 "${textForImage}"`);
      } else {
        console.warn(`⚠ サブスロット${item.Slot}-${item.SubslotID}: メインスロットデータが見つかりません`);
      }
    } else {
      // 通常のスロットの場合
      textForImage = item.SlotText || item.SlotPhrase || "";
    }
    
    // 上位スロットと同じ複数画像表示システムを使用
    if (textForImage.trim() && typeof window.applyMultipleImagesToSlot === 'function') {
      console.log(`🖼️ サブスロット複数画像表示開始: ${normalizeSlotId(item.Slot)} | テキスト: "${textForImage}"`);
      window.applyMultipleImagesToSlot(normalizeSlotId(item.Slot), textForImage, true);
      console.log(`✅ サブスロット複数画像表示完了: ${item.Slot}-${item.SubslotID}`);
    } else {
      console.warn(`❌ サブスロット複数画像表示失敗: ${item.Slot}-${item.SubslotID} | テキスト="${textForImage.trim()}" | applyMultipleImagesToSlot=${typeof window.applyMultipleImagesToSlot}`);
    }
  });
  
  // 🔢 サブスロット順序修正：window.loadedJsonDataを使用して正しい順序で再書き込み
  console.log("🔢 サブスロット順序修正処理を実行...");
  if (window.loadedJsonData && typeof window.syncSubslotsWithCorrectOrder === 'function') {
    setTimeout(() => {
      window.syncSubslotsWithCorrectOrder(window.loadedJsonData);
      console.log("✅ サブスロット順序修正処理が完了しました");
    }, 50);
  } else {
    console.warn("⚠ window.loadedJsonData または syncSubslotsWithCorrectOrder関数が見つかりません");
  }

  // �🖼 画像処理：データ同期完了後に画像の自動非表示処理を実行
  console.log("🖼 syncDynamicToStatic完了後の画像処理を実行...");
  if (typeof window.processAllImagesWithCoordination === 'function') {
    setTimeout(() => {
      window.processAllImagesWithCoordination();
      console.log("✅ 画像自動非表示処理が完了しました");
    }, 100);
  } else {
    console.warn("⚠ processAllImagesWithCoordination関数が見つかりません");
  }
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
    const questionWord = topDisplayItem.DisplayText.trim();
    
    // 🆕 分離疑問詞の日本語訳
    const translations = {
      'What': '何？',
      'Who': '誰？',
      'When': 'いつ？',
      'Where': 'どこ？',
      'Why': 'なぜ？',
      'How': 'どのように？',
      'Which': 'どちら？',
      'Whose': '誰の？',
      'Whom': '誰を？',
      'How many': 'いくつ？',
      'How much': 'いくら？',
      'How long': 'どのくらい？',
      'How often': 'どのくらいの頻度で？',
      'How far': 'どのくらい遠く？'
    };
    
    // 🆕 HTML構造を確保（なければ作成）
    let textElement = topDiv.querySelector('.question-word-text');
    let auxtextElement = topDiv.querySelector('.question-word-auxtext');
    
    // 🔧 常にHTML構造を強制的に再作成（確実に動作させるため）
//     const translation = translations[questionWord] || '';
//     topDiv.innerHTML = `
//       <div class="question-word-label">疑問詞</div>
//       <div class="question-word-image"></div>
//       <div class="question-word-auxtext">${translation}</div>
//       <div class="question-word-text">${questionWord}</div>
//       <div class="question-word-button-placeholder"></div>
//       <div class="question-word-button-placeholder"></div>
//     `;
    
    // HTML構造を強制的に再作成（疑問詞表示用）
    const translation = translations[questionWord] || '';
    topDiv.innerHTML = `
      <div class="question-word-label">疑問詞</div>
      <div class="question-word-image"></div>
      <div class="question-word-auxtext">${translation}</div>
      <div class="question-word-text">${questionWord}</div>
    `;
    
    console.log("✅ 分離疑問詞として表示: " + questionWord + " (" + translation + ")");
    
    // 🆕 表示状態を復元
    topDiv.style.display = "";
    topDiv.classList.remove("empty-slot-hidden", "hidden", "empty-content");
    topDiv.classList.add("visible"); // visibleクラスを追加してGrid表示を有効化
    
    // 🔹 疑問詞を文頭（slot-wrapper内の最初）に移動
    const slotWrapper = document.querySelector('.slot-wrapper');
    if (slotWrapper && !slotWrapper.contains(topDiv)) {
      // slot-wrapperの最初に移動
      slotWrapper.insertBefore(topDiv, slotWrapper.firstChild);
      console.log("✅ 疑問詞を文頭に移動しました");
    }

    // 🔹 動的記載エリアにも同じ疑問詞を表示
    const dynamicArea = document.getElementById("dynamic-slot-area");
    if (dynamicArea) {
      // 既存の動的エリア用疑問詞要素があるかチェック
      let dynamicQuestionDiv = document.getElementById("dynamic-question-word");
      
      if (!dynamicQuestionDiv) {
        // 初回作成：元の要素をクローン
        dynamicQuestionDiv = topDiv.cloneNode(true);
        dynamicQuestionDiv.id = "dynamic-question-word"; // 異なるIDを設定
        console.log("✅ 動的エリア用疑問詞要素を作成しました");
      }
      
      // テキストを更新（HTML構造を保持）
      const dynamicTextElement = dynamicQuestionDiv.querySelector('.question-word-text');
      if (dynamicTextElement) {
        dynamicTextElement.textContent = topDisplayItem.DisplayText;
      } else {
        // 構造がない場合は単純にテキストを設定
        dynamicQuestionDiv.textContent = topDisplayItem.DisplayText;
      }
      
      // 動的エリアの最初に配置
      if (!dynamicArea.contains(dynamicQuestionDiv)) {
        dynamicArea.insertBefore(dynamicQuestionDiv, dynamicArea.firstChild);
        console.log("✅ 動的エリアに疑問詞を配置しました");
      }
    }
  } else {
    // DisplayAtTopがない場合は表示をクリア
    const textElement = topDiv.querySelector('.question-word-text');
    const auxtextElement = topDiv.querySelector('.question-word-auxtext');
    
    if (textElement && auxtextElement) {
      // 新しい構造でクリア
      textElement.textContent = "";
      auxtextElement.textContent = "";
    } else {
      // 従来の方法でクリア
      topDiv.textContent = "";
      topDiv.innerHTML = ""; // HTMLも完全にクリア
    }
    
    topDiv.classList.add("empty-content"); // 強制的に空クラスを追加
    
    // 🆕 空の場合は非表示にする
    topDiv.style.display = "none";
    topDiv.classList.add("empty-slot-hidden", "hidden");
    topDiv.classList.remove("visible"); // visibleクラスを削除
    console.log("🙈 分離疑問詞エリアを非表示 (DisplayAtTopデータなし)");
    
    // 動的エリアの疑問詞もクリア
    const dynamicQuestionDiv = document.getElementById("dynamic-question-word");
    if (dynamicQuestionDiv) {
      dynamicQuestionDiv.remove();
      console.log("🧹 動的エリアの疑問詞を削除しました");
    }
    
    console.log("🧹 DisplayAtTop 表示をクリア（該当データなし）");
  }
  
  // 🔧 遅延処理は削除（HTML構造を破壊するため）
  // 上記の処理で既に正しく設定済み
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

  // � 全上位スロットの展開ボタン制御（データ存在チェック + PhraseType判定）
  const allTargetSlots = ['c1', 'm1', 's', 'v', 'o1', 'o2', 'm2', 'c2', 'm3', 'aux'];
  console.log(`🎯 展開ボタン制御対象: ${allTargetSlots.join(', ')}`);
  
  allTargetSlots.forEach(slotName => {
    const slotId = `slot-${slotName}`;
    const container = document.getElementById(slotId);
    
    if (!container) {
      console.warn(`⚠ ${slotId}が見つかりません`);
      return;
    }
    
    // このスロットのデータを検索
    const slotData = data.find(item => 
      item.Slot.toLowerCase() === slotName && 
      (!item.SubslotID || item.SubslotID === "")
    );
    
    // このスロットに関連するサブスロットデータをチェック
    const relatedSubslotData = data.filter(item => 
      item.Slot.toLowerCase() === slotName && 
      item.SubslotID && 
      item.SubslotID !== ""
    );
    
    const detailButton = container.querySelector('.subslot-toggle-button');
    if (!detailButton) {
      console.log(`ℹ ${slotName}: 展開ボタンが存在しません`);
      return;
    }
    
    console.log(`🔍 ${slotName}:`);
    console.log(`  - 上位データ: ${slotData ? `PhraseType=${slotData.PhraseType}` : '未存在'}`);
    console.log(`  - 関連サブスロット: ${relatedSubslotData.length}件`);
    
    // サブスロットデータの詳細を出力
    if (relatedSubslotData.length > 0) {
      console.log(`  - サブスロット詳細:`);
      relatedSubslotData.forEach((sub, index) => {
        console.log(`    ${index + 1}. SubslotID=${sub.SubslotID}, PhraseType=${sub.PhraseType}, Element="${sub.SubslotElement}"`);
      });
    }
    
    // 判定ロジック：
    // 1. 上位データが存在し、PhraseType="word" → 展開ボタン非表示
    // 2. 関連サブスロットデータが0件 → 展開ボタン非表示
    // 3. それ以外 → 展開ボタン表示
    
    if (slotData && slotData.PhraseType === "word") {
      detailButton.style.display = 'none';
      console.log(`🚫 ${slotName}: PhraseType=wordのため展開ボタンを非表示`);
      
      // 🖼 展開ボタン非表示の場合は画像を元に戻す
      const slotImage = container.querySelector('.slot-image');
      if (slotImage) {
        slotImage.src = 'slot_images/common/placeholder.png';
        console.log(`🖼 ${slotName}: 画像をplaceholder.pngに戻しました`);
      }
    } else if (relatedSubslotData.length === 0) {
      detailButton.style.display = 'none';
      console.log(`🚫 ${slotName}: サブスロットデータ0件のため展開ボタンを非表示`);
      
      // 🖼 展開ボタン非表示の場合は画像を元に戻す
      const slotImage = container.querySelector('.slot-image');
      if (slotImage) {
        slotImage.src = 'slot_images/common/placeholder.png';
        console.log(`🖼 ${slotName}: 画像をplaceholder.pngに戻しました`);
      }
    } else {
      detailButton.style.display = '';
      console.log(`👁 ${slotName}: サブスロットデータ${relatedSubslotData.length}件のため展開ボタンを表示`);
      
      // 🖼 サブスロット要素がある上位スロットの画像をbutton.pngに変更
      const slotImage = container.querySelector('.slot-image');
      if (slotImage) {
        slotImage.src = 'slot_images/common/button.png';
        console.log(`🖼 ${slotName}: 画像をbutton.pngに変更しました`);
      } else {
        console.warn(`⚠ ${slotName}: slot-imageが見つかりません`);
      }
    }
  });
  const targetSlots = ['c1', 'm1', 's', 'v', 'o1', 'o2', 'm2', 'c2', 'm3', 'aux'];
  console.log(`🎯 空スロット非表示対象: ${targetSlots.join(', ')}`);
  
  targetSlots.forEach(slotName => {
    const slotId = `slot-${slotName}`;
    const slot = document.getElementById(slotId);
    
    if (slot) {
      const phraseDiv = slot.querySelector('.slot-phrase');
      const textDiv = slot.querySelector('.slot-text');
      
      // 上位スロット自体が空かどうかを判定
      const phraseEmpty = !phraseDiv || !phraseDiv.textContent || phraseDiv.textContent.trim() === '';
      const textEmpty = !textDiv || !textDiv.textContent || textDiv.textContent.trim() === '';
      const upperSlotEmpty = phraseEmpty && textEmpty;
      
      // 関連するサブスロットに内容があるかチェック
      const relatedSubSlots = document.querySelectorAll(`[id^="slot-${slotName}-sub-"]`);
      let hasNonEmptySubslots = false;
      
      relatedSubSlots.forEach(subSlot => {
        const subPhraseDiv = subSlot.querySelector('.slot-phrase');
        const subTextDiv = subSlot.querySelector('.slot-text');
        const subPhraseEmpty = !subPhraseDiv || !subPhraseDiv.textContent || subPhraseDiv.textContent.trim() === '';
        const subTextEmpty = !subTextDiv || !subTextDiv.textContent || subTextDiv.textContent.trim() === '';
        
        if (!subPhraseEmpty || !subTextEmpty) {
          hasNonEmptySubslots = true;
        }
      });
      
      console.log(`🔍 ${slotId}:`);
      console.log(`  - 上位スロット空: ${upperSlotEmpty} (phrase="${phraseDiv?.textContent}", text="${textDiv?.textContent}")`);
      console.log(`  - 関連サブスロット: ${relatedSubSlots.length}件`);
      console.log(`  - 空でないサブスロットあり: ${hasNonEmptySubslots}`);
      
      // 判定: 上位スロットが空 かつ 空でないサブスロットがない場合のみ非表示
      const shouldHide = upperSlotEmpty && !hasNonEmptySubslots;
      
      if (shouldHide) {
        slot.style.display = 'none';
        slot.classList.add('empty-slot-hidden', 'hidden');
        console.log(`👻 ${slotId}を非表示にしました`);
      } else {
        slot.style.display = '';
        slot.classList.remove('empty-slot-hidden', 'hidden');
        const reason = !upperSlotEmpty ? '上位スロットに内容あり' : 'サブスロットに内容あり';
        console.log(`👁 ${slotId}を表示状態にしました (理由: ${reason})`);
      }
    } else {
      console.log(`⚠ ${slotId}が見つかりません`);
    }
  });
  
  // 🖼 画像処理：上位スロット同期完了後に画像の自動非表示処理を実行
  // 注意：この処理は最終的にラベル復元後に統合実行されるため、ここでは削除
  // console.log("🖼 syncUpperSlotsFromJson完了後の画像処理を実行...");
  // if (typeof window.processAllImagesWithCoordination === 'function') {
  //   setTimeout(() => {
  //     window.processAllImagesWithCoordination();
  //     console.log("✅ 上位スロット同期後の画像自動非表示処理が完了しました");
  //   }, 50);
  // } else {
  //   console.warn("⚠ processAllImagesWithCoordination関数が見つかりません");
  // }
  
  // 🆕 スロット幅の動的調整を実行
  setTimeout(() => {
    if (typeof window.adjustSlotWidthsBasedOnText === 'function') {
      window.adjustSlotWidthsBasedOnText();
    }
  }, 100);
  
  // 🖼 全スロット画像更新：データ更新後に全スロット画像を再更新
  setTimeout(() => {
    if (typeof window.updateAllSlotImagesAfterDataChange === 'function') {
      window.updateAllSlotImagesAfterDataChange();
      console.log("✅ syncUpperSlotsFromJson完了後の全スロット画像更新を実行");
    } else {
      console.warn("⚠ updateAllSlotImagesAfterDataChange関数が見つかりません");
    }
  }, 150);
  
  // 🏷️ 上位スロット同期後にラベルを復元
  setTimeout(() => {
    if (window.restoreSubslotLabels) {
      window.restoreSubslotLabels();
      console.log("🏷️ 上位スロット同期後のラベル復元を実行しました");
    }
    
    // 🖼 画像処理：この処理はラベル復元内で統合実行されるため、ここでは削除
    // if (typeof window.processAllImagesWithCoordination === 'function') {
    //   window.processAllImagesWithCoordination();
    // }
  }, 150);
}

// ✅ サブスロット同期機能の実装（完全リセット＋再構築方式）
function syncSubslotsFromJson(data) {
  console.log("🔄 サブスロット同期（完全リセット＋再構築）開始");
  if (!data || !Array.isArray(data)) {
    console.warn("⚠ サブスロット同期: データが無効です");
    return;
  }
  
  // DisplayAtTopの要素を特定（サブスロットから除外するため）
  const displayAtTopItem = data.find(d => d.DisplayAtTop);
  
  // サブスロット用のデータをフィルタリング
  const subslotData = data.filter(item => item.SubslotID && item.SubslotID !== "");
  console.log(`📊 サブスロット対象件数: ${subslotData.length}`);
  
  // 🧹 STEP1: 全サブスロットコンテナをクリア
  const allSubContainers = document.querySelectorAll('[id^="slot-"][id$="-sub"]');
  console.log(`🧹 クリア対象サブスロットコンテナ: ${allSubContainers.length}件`);
  
  allSubContainers.forEach(container => {
    // 子要素を全て削除
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    console.log(`🧹 ${container.id} を完全クリア`);
  });
  
  // 🔧 STEP2: display_orderでソートしてから再構築
  // display_orderによる正しい順序でソート
  const sortedSubslotData = subslotData.sort((a, b) => {
    // まず親スロットで並べ、次にdisplay_orderで並べる
    if (a.Slot !== b.Slot) {
      return a.Slot.localeCompare(b.Slot);
    }
    return (a.display_order || 0) - (b.display_order || 0);
  });
  
  console.log("📊 display_orderでソート完了: " + sortedSubslotData.length + "件");
  sortedSubslotData.forEach((item, index) => {
    console.log("  " + (index + 1) + ". " + item.Slot + "-" + item.SubslotID + ": display_order=" + item.display_order);
  });
  
  sortedSubslotData.forEach(item => {
    try {
      // DisplayAtTopの要素をサブスロットから除外
      if (displayAtTopItem && 
          displayAtTopItem.DisplayText && 
          item.SubslotElement === displayAtTopItem.DisplayText) {
        console.log("🚫 DisplayAtTop対象のため除外: " + item.SubslotElement + " (" + item.Slot + "-" + item.SubslotID + ")");
        return;
      }

      // スロット要素ID構築（slot-[親スロット名]-[サブスロットID]形式）
      const parentSlot = item.Slot.toLowerCase();
      const subslotId = item.SubslotID.toLowerCase();
      const fullSlotId = `slot-${parentSlot}-${subslotId}`;
      console.log("📍 サブスロット生成: " + fullSlotId);
      
      // 親コンテナを検索（slot-[親スロット名]-sub）
      const parentContainerId = `slot-${parentSlot}-sub`;
      const parentContainer = document.getElementById(parentContainerId);
      
      if (!parentContainer) {
        console.warn("⚠ 親コンテナが見つかりません: " + parentContainerId);
        return;
      }
      
      // 新しいサブスロットDOM要素を生成
      const slotElement = document.createElement('div');
      slotElement.id = fullSlotId;
      slotElement.className = 'subslot-container';
      
      // 🏷️ ラベル要素を作成（Grid行1）
      const labelElement = document.createElement('label');
      labelElement.textContent = subslotId.toUpperCase();
      labelElement.style.cssText = `
        display: block;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
        font-size: 14px;
        grid-row: 1;
      `;
      
      // 空のslot-imageコンテナを作成（Grid行2）
      const imageElement = document.createElement('div');
      imageElement.className = 'slot-image';
      imageElement.style.cssText = 'grid-row: 2 !important;';
      
      // phrase要素を作成（Grid行3）
      const phraseElement = document.createElement('div');
      phraseElement.className = 'slot-phrase';
      phraseElement.style.cssText = 'grid-row: 3 !important;';
      if (item.SubslotElement) {
        phraseElement.textContent = item.SubslotElement;
      }
      
      // text要素を作成（Grid行4）
      const textElement = document.createElement('div');
      textElement.className = 'slot-text';
      textElement.style.cssText = 'grid-row: 4 !important;';
      if (item.SubslotText) {
        textElement.textContent = item.SubslotText;
      }
      
      // 要素を組み立て（Grid行順序で追加）
      slotElement.appendChild(labelElement);    // Grid行1
      slotElement.appendChild(imageElement);    // Grid行2
      slotElement.appendChild(phraseElement);   // Grid行3
      slotElement.appendChild(textElement);     // Grid行4
      
      // 親コンテナに追加
      parentContainer.appendChild(slotElement);
      
      console.log("✅ サブスロット完全生成（Grid構造）: " + fullSlotId + " | label:\"" + subslotId.toUpperCase() + "\" | phrase:\"" + item.SubslotElement + "\" | text:\"" + item.SubslotText + "\"");
      
    } catch (err) {
      console.error("❌ サブスロット処理エラー: " + err.message, item);
    }
  });
  
  console.log("✅ サブスロット同期完了（完全リセット＋再構築）");
  
  // 🆕 サブスロット同期後にスロット幅調整を実行
  setTimeout(() => {
    if (typeof window.adjustSlotWidthsBasedOnText === 'function') {
      window.adjustSlotWidthsBasedOnText();
    }
  }, 50);
  
  // 🏷️ サブスロット同期後にラベルを復元＋画像処理
  setTimeout(() => {
    if (window.restoreSubslotLabels) {
      window.restoreSubslotLabels();
      console.log("🏷️ サブスロット同期後のラベル復元を実行しました");
    }
    
    // 🖼 画像処理：統合実行
    if (typeof window.processAllImagesWithCoordination === 'function') {
      window.processAllImagesWithCoordination();
      console.log("🖼 サブスロット同期後の画像処理を実行しました");
    }
  }, 100);
}

// サブスロット同期関数をwindowオブジェクトにエクスポート
window.syncSubslotsFromJson = syncSubslotsFromJson;
