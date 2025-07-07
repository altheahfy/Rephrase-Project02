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

    // 📝 フレーズ要素への書き込み（上位スロットと同じ方式 - ラベル保護）
    if (phraseElement) {
      phraseElement.textContent = item.SlotPhrase || "";
      console.log(`✅ サブスロット phrase書き込み成功: ${item.Slot} | 値: "${item.SlotPhrase}"`);
    } else {
      console.warn(`❌ サブスロット phrase要素取得失敗: ${item.Slot}`);
    }
    
    // 📝 テキスト要素への書き込み（上位スロットと同じ方式 - ラベル保護）
    if (slotTextElement) {
      slotTextElement.textContent = item.SlotText || "";
      console.log(`✅ サブスロット text書き込み成功: ${item.Slot} | 値: "${item.SlotText}"`);
      
      // 上位スロットと同じ入れ子構造チェック
      const nestedPhraseDiv = slotTextElement.querySelector(".slot-phrase");
      if (nestedPhraseDiv) {
        console.warn(`⚠️ サブスロット slotTextElement内にslot-phraseが入れ子になっています: ${item.Slot}`);
        console.warn(`⚠️ この入れ子構造が原因で書き込みが上書きされている可能性があります`);
      }
    } else {
      console.warn(`❌ サブスロット text要素取得失敗: ${item.Slot}`);
    }
    
    // 🖼️ サブスロット画像更新（テキスト書き込みと同じ方式）
    console.log("🖼️ サブスロット画像要素検索:", normalizeSlotId(item.Slot));
    const imageElement = slotElement.querySelector(".slot-image");
    console.log("サブスロット imageElement:", imageElement ? imageElement.outerHTML : "未検出");
    
    if (imageElement && typeof window.findImageByMetaTag === 'function') {
      const textForImage = item.SlotText || item.SlotPhrase || "";
      if (textForImage.trim()) {
        const imageData = window.findImageByMetaTag(textForImage);
        if (imageData) {
          const imagePath = `slot_images/${imageData.folder}/${imageData.image_file}`;
          imageElement.src = imagePath;
          imageElement.alt = `image for ${normalizeSlotId(item.Slot)}`;
          console.log(`✅ サブスロット画像更新成功: ${normalizeSlotId(item.Slot)} → "${imagePath}"`);
        } else {
          imageElement.src = 'slot_images/common/placeholder.png';
          imageElement.alt = `No image for ${normalizeSlotId(item.Slot)}`;
          console.log(`📝 サブスロット画像なし: ${normalizeSlotId(item.Slot)} (テキスト: "${textForImage}")`);
        }
      } else {
        imageElement.src = 'slot_images/common/placeholder.png';
        imageElement.alt = `No text for ${normalizeSlotId(item.Slot)}`;
        console.log(`📝 サブスロット画像更新スキップ: ${normalizeSlotId(item.Slot)} (テキストなし)`);
      }
    } else {
      if (!imageElement) {
        console.warn(`❌ サブスロット image要素取得失敗: ${item.Slot}`);
      }
      if (typeof window.findImageByMetaTag !== 'function') {
        console.warn(`❌ findImageByMetaTag関数が見つかりません`);
      }
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
    const translation = translations[questionWord] || '';
    topDiv.innerHTML = `
      <div class="question-word-label">疑問詞</div>
      <div class="question-word-image"></div>
      <div class="question-word-auxtext">${translation}</div>
      <div class="question-word-text">${questionWord}</div>
      <div class="question-word-button-placeholder"></div>
      <div class="question-word-button-placeholder"></div>
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
  
  // 関数の終了
}

// グローバル関数として公開
window.syncDynamicToStatic = syncDynamicToStatic;
