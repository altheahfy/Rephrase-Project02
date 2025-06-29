import { updateSlotDisplay } from './image_handler.js';

/**
 * null や undefined に対してフォールバック値を返す
 */
function safe(value, fallback = "") {
  return value === null || value === undefined ? fallback : value;
}

/**
 * 指定された key に対応する slot 内容だけを更新
 */
export function randomizeSlot(data, key) {
  const contentMap = {
    s: data.subject,
    aux: data.auxiliary,
    v: data.verb,
    o1: data.object,
    o_v: data.object_verb,
    c1: data.complement,
    o2: data.object2,
    c2: data.complement2,
    m1: data.adverbial,
    m2: data.adverbial2,
    m3: data.adverbial3,
    // sub-slot
    "o1-m1": data.sub_m1,
    "o1-s": data.sub_s,
    "o1-aux": data.sub_aux,
    "o1-m2": data.sub_m2,
    "o1-v": data.sub_v,
    "o1-c1": data.sub_c1,
    "o1-o1": data.sub_o1,
    "o1-o2": data.sub_o2,
    "o1-c2": data.sub_c2,
    "o1-m3": data.sub_m3
  };

  updateSlotDisplay(`slot-${key}`, safe(contentMap[key]));
}

// === Sスロット個別ランダマイズ機能 ===

/**
 * Sスロット専用の個別ランダマイズ関数
 * 同じV_group_key内の他の例文からSスロット（メイン+サブスロット）をランダム選択して置き換える
 */
function randomizeSlotSIndividual() {
  console.log("🎲 Sスロット個別ランダマイズ開始");
  
  // デバッグ：現在のデータ状況を確認
  console.log("🔍 デバッグ情報:");
  console.log("  window.loadedJsonData:", window.loadedJsonData);
  console.log("  window.slotSets:", window.slotSets);
  
  // window.slotSetsが存在するかチェック（randomizer_all.jsで設定される）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  // window.slotSetsから全てのSスロットデータを抽出
  const allSSlots = [];
  window.slotSets.forEach((sentenceSet, setIndex) => {
    const sSlotData = sentenceSet.filter(item => 
      item.Slot && item.Slot.toLowerCase() === 's'
    );
    if (sSlotData.length > 0) {
      allSSlots.push({
        setIndex: setIndex,
        例文ID: sentenceSet[0]?.例文ID,
        sSlotData: sSlotData
      });
    }
  });
  
  if (allSSlots.length < 2) {
    console.warn("⚠️ 利用可能なSスロットが不足しています（最低2つ必要）");
    console.log("利用可能なSスロット:", allSSlots);
    return;
  }
  
  console.log(`📊 利用可能なSスロット: ${allSSlots.length}種類`);
  
  // 現在表示中のSスロットデータを取得
  const currentSSlot = getCurrentDisplayedSSlot();
  console.log("📍 現在表示中のSスロット:", currentSSlot);
  
  // 現在表示中以外のSスロットからランダム選択
  const availableSlots = allSSlots.filter(slot => {
    // 現在表示中のSスロットと異なるものを選択
    return !isSameSSlot(currentSSlot, slot.sSlotData);
  });
  
  if (availableSlots.length === 0) {
    console.warn("⚠️ 選択可能な他のSスロットが見つかりません");
    return;
  }
  
  // ランダムに1つ選択
  const randomIndex = Math.floor(Math.random() * availableSlots.length);
  const selectedSlot = availableSlots[randomIndex];
  
  console.log(`🎯 選択されたSスロット（例文ID: ${selectedSlot.例文ID}）:`, selectedSlot.sSlotData);
  
  // 現在のSスロット表示を選択されたデータで更新
  updateSSlotWithNewData(selectedSlot.sSlotData);
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

/**
 * 現在表示中のSスロットデータを取得
 */
function getCurrentDisplayedSSlot() {
  const sContainer = document.getElementById('slot-s');
  if (!sContainer) return null;
  
  const phraseDiv = sContainer.querySelector('.slot-phrase');
  const textDiv = sContainer.querySelector('.slot-text');
  
  return {
    SlotPhrase: phraseDiv?.textContent || "",
    SlotText: textDiv?.textContent || ""
  };
}

/**
 * 2つのSスロットが同じかどうかを判定
 */
function isSameSSlot(currentSlot, sSlotDataArray) {
  if (!currentSlot || !sSlotDataArray || sSlotDataArray.length === 0) return false;
  
  // メインスロットデータを取得
  const mainSlotData = sSlotDataArray.find(item => 
    !item.SubslotID && 
    (item.PhraseType === "word" || item.PhraseType === "phrase" || item.PhraseType === "clause")
  );
  
  if (!mainSlotData) return false;
  
  // フレーズとテキストが同じかチェック
  return currentSlot.SlotPhrase === (mainSlotData.SlotPhrase || "") &&
         currentSlot.SlotText === (mainSlotData.SlotText || "");
}

/**
 * 現在表示中の例文IDを取得（旧バージョン・デバッグ用）
 */
function getCurrentSentenceId() {
  console.log("🔍 getCurrentSentenceId デバッグ:");
  console.log("  window.loadedJsonData存在:", !!window.loadedJsonData);
  console.log("  window.loadedJsonData型:", typeof window.loadedJsonData);
  console.log("  window.loadedJsonData長さ:", window.loadedJsonData?.length);
  
  if (window.loadedJsonData && window.loadedJsonData.length > 0) {
    console.log("  最初の要素:", window.loadedJsonData[0]);
    const sentenceId = window.loadedJsonData[0]?.例文ID;
    console.log("  抽出された例文ID:", sentenceId);
    return sentenceId;
  }
  
  console.log("  例文IDを取得できませんでした");
  return null;
}

/**
 * 選択されたSスロットデータで現在のSスロット表示を更新
 * @param {Array} newSSlotData - 新しいSスロットデータ（メイン+サブスロット）
 */
function updateSSlotWithNewData(newSSlotData) {
  console.log("🔄 Sスロット表示更新開始");
  console.log("🔍 新しいSスロットデータ:", newSSlotData);
  
  // メインスロットデータを取得
  const mainSlotData = newSSlotData.find(item => 
    !item.SubslotID && 
    (item.PhraseType === "word" || item.PhraseType === "phrase" || item.PhraseType === "clause")
  );
  
  if (!mainSlotData) {
    console.warn("⚠️ メインスロットデータが見つかりません");
    return;
  }
  
  console.log(`🔍 PhraseType: ${mainSlotData.PhraseType}`);
  
  if (mainSlotData.PhraseType === "word") {
    // Type "word" の場合：上位スロットに書き込む
    console.log("📝 Type 'word' → 上位スロットに書き込み");
    
    const container = document.getElementById('slot-s');
    if (container) {
      const phraseDiv = container.querySelector('.slot-phrase');
      const textDiv = container.querySelector('.slot-text');
      
      if (phraseDiv) {
        phraseDiv.textContent = mainSlotData.SlotPhrase || "";
      }
      if (textDiv) {
        textDiv.textContent = mainSlotData.SlotText || "";
      }
      
      console.log("✅ 上位Sスロット更新完了");
    }
  } else {
    // Type "phrase" または "clause" の場合：サブスロットに分散
    console.log(`📝 Type '${mainSlotData.PhraseType}' → サブスロットに分散`);
    
    // 上位スロットは空にする
    const container = document.getElementById('slot-s');
    if (container) {
      const phraseDiv = container.querySelector('.slot-phrase');
      const textDiv = container.querySelector('.slot-text');
      if (phraseDiv) phraseDiv.textContent = "";
      if (textDiv) textDiv.textContent = "";
      console.log("🧹 上位Sスロットをクリア");
    }
    
    // サブスロットに分散
    distributeMainSlotToSubslots(mainSlotData);
  }
  
  // サブスロットデータがある場合は個別に更新
  const subSlotData = newSSlotData.filter(item => 
    item.SubslotID && 
    (item.SubslotElement || item.SubslotText)
  );
  
  if (subSlotData.length > 0) {
    console.log(`📊 追加のサブスロット更新: ${subSlotData.length}件`);
    subSlotData.forEach(subData => {
      console.log(`🔧 サブスロット ${subData.SubslotID} を更新:`, subData);
      updateSSlotDisplay(subData, true);
    });
  }
}

/**
 * メインスロットデータをサブスロット構造に分散
 * @param {Object} mainData - メインスロットデータ
 */
function distributeMainSlotToSubslots(mainData) {
  console.log("🔄 メインスロットデータをサブスロットに分散:", mainData);
  
  // SlotPhraseとSlotTextを適切なサブスロットに配置
  const phrase = mainData.SlotPhrase || "";
  const text = mainData.SlotText || "";
  
  // 実際に存在するSサブスロットを探して更新
  const sContainer = document.getElementById('slot-s');
  if (!sContainer) {
    console.warn("⚠️ Sスロットコンテナが見つかりません");
    return;
  }
  
  // Sスロット内の全サブスロット要素を取得
  const subslotElements = sContainer.querySelectorAll('[id^="slot-s-"]');
  console.log(`🔍 発見されたSサブスロット: ${subslotElements.length}個`);
  
  if (subslotElements.length > 0) {
    // 最初のサブスロット（通常はメインの内容）にデータを配置
    const firstSubslot = subslotElements[0];
    const elementDiv = firstSubslot.querySelector('.subslot-element');
    const textDiv = firstSubslot.querySelector('.subslot-text');
    
    if (elementDiv) {
      elementDiv.textContent = phrase;
      console.log(`✅ 最初のサブスロット要素に設定: "${phrase}"`);
    }
    if (textDiv) {
      textDiv.textContent = text;
      console.log(`✅ 最初のサブスロットテキストに設定: "${text}"`);
    }
  } else {
    // サブスロットが存在しない場合の代替処理
    console.log("ℹ️ サブスロットが見つからないため、上位スロットに配置");
    const phraseDiv = sContainer.querySelector('.slot-phrase');
    const textDiv = sContainer.querySelector('.slot-text');
    if (phraseDiv) phraseDiv.textContent = phrase;
    if (textDiv) textDiv.textContent = text;
  }
}

/**
 * Sスロットの表示を更新
 * @param {Object} data - 更新データ
 * @param {boolean} isSubslot - サブスロットかどうか
 */
function updateSSlotDisplay(data, isSubslot = false) {
  if (isSubslot) {
    // サブスロットの更新
    const subslotId = `slot-s-${data.SubslotID}`;
    const subslotElement = document.getElementById(subslotId);
    
    if (subslotElement) {
      // サブスロット要素の更新
      const elementDiv = subslotElement.querySelector('.subslot-element');
      if (elementDiv) {
        elementDiv.textContent = data.SubslotElement || "";
      }
      
      const textDiv = subslotElement.querySelector('.subslot-text');
      if (textDiv) {
        textDiv.textContent = data.SubslotText || "";
      }
      
      console.log(`✅ サブスロット ${data.SubslotID} 更新完了`);
    } else {
      console.warn(`⚠️ サブスロット要素が見つかりません: ${subslotId}`);
    }
  } else {
    // メインスロットの更新
    const container = document.getElementById('slot-s');
    if (container) {
      const phraseDiv = container.querySelector('.slot-phrase');
      if (phraseDiv) {
        phraseDiv.textContent = data.SlotPhrase || "";
      }
      
      const textDiv = container.querySelector('.slot-text');
      if (textDiv) {
        textDiv.textContent = data.SlotText || "";
      }
      
      console.log("✅ メインSスロット更新完了");
    } else {
      console.warn("⚠️ Sスロットコンテナが見つかりません");
    }
  }
  
  // 視覚的な確認のため一時的に枠を赤くする
  const container = document.getElementById('slot-s');
  if (container) {
    container.style.border = "3px solid red";
    setTimeout(() => {
      container.style.border = "";
    }, 1000);
  }
}

/**
 * Sスロット個別ランダマイズボタンを設置
 */
function setupSSlotRandomizeButton() {
  const sContainer = document.getElementById('slot-s');
  if (!sContainer) {
    console.warn("⚠️ Sスロットコンテナが見つかりません");
    return;
  }
  
  // 既存ボタンがあれば削除
  const existingButton = sContainer.querySelector('.s-individual-randomize-btn');
  if (existingButton) {
    existingButton.remove();
  }
  
  // 個別ランダマイズボタンを作成
  const randomizeBtn = document.createElement('button');
  randomizeBtn.className = 's-individual-randomize-btn';
  randomizeBtn.textContent = '🎲';
  randomizeBtn.title = 'Sスロット個別ランダマイズ';
  randomizeBtn.style.cssText = `
    position: absolute;
    top: 5px;
    right: 5px;
    width: 25px;
    height: 25px;
    font-size: 12px;
    border: 1px solid #ccc;
    background: #f9f9f9;
    cursor: pointer;
    border-radius: 3px;
    z-index: 10;
  `;
  
  // クリックイベント
  randomizeBtn.addEventListener('click', function(event) {
    event.stopPropagation();
    event.preventDefault();
    
    console.log("🎲 Sスロット個別ランダマイズボタンがクリックされました");
    randomizeSlotSIndividual();
  });
  
  // スロットコンテナに相対位置を設定
  if (sContainer.style.position !== 'relative') {
    sContainer.style.position = 'relative';
  }
  
  // ボタンを追加
  sContainer.appendChild(randomizeBtn);
  
  console.log("✅ Sスロット個別ランダマイズボタンを設置しました");
}

/**
 * 初期化処理（エクスポート版）
 */
export function initializeIndividualRandomizers() {
  console.log("🚀 個別ランダマイザー初期化開始");
  
  // DOMが準備できてからボタンを設置
  function setupWhenReady() {
    const sContainer = document.getElementById('slot-s');
    if (sContainer) {
      setupSSlotRandomizeButton();
      console.log("✅ Sスロット個別ランダマイズボタン設置完了");
    } else {
      console.log("⏳ Sスロットが見つからないため、1秒後に再試行...");
      setTimeout(setupWhenReady, 1000);
    }
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupWhenReady);
  } else {
    setupWhenReady();
  }
}

/**
 * 内部使用の初期化処理
 */
function initializeIndividualRandomizer() {
  console.log("🚀 個別ランダマイザー初期化開始");
  
  // DOMが準備できてからボタンを設置
  function setupWhenReady() {
    const sContainer = document.getElementById('slot-s');
    if (sContainer) {
      setupSSlotRandomizeButton();
      console.log("✅ Sスロット個別ランダマイズボタン設置完了");
    } else {
      console.log("⏳ Sスロットが見つからないため、1秒後に再試行...");
      setTimeout(setupWhenReady, 1000);
    }
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupWhenReady);
  } else {
    setupWhenReady();
  }
}

// グローバル関数としてもエクスポート
window.randomizeSlotSIndividual = randomizeSlotSIndividual;
window.setupSSlotRandomizeButton = setupSSlotRandomizeButton;

// デバッグ用のヘルパー関数
window.debugIndividualRandomizer = function() {
  console.log("🔍 個別ランダマイザーデバッグ:");
  console.log("  window.loadedJsonData:", window.loadedJsonData);
  console.log("  window.slotSets:", window.slotSets);
  console.log("  getCurrentSentenceId():", getCurrentSentenceId());
};

console.log("✅ 個別ランダマイザー読み込み完了");