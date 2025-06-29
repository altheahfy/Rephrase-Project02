// import { updateSlotDisplay } from './image_handler.js';

/**
 * null や undefined に対してフォールバック値を返す
 */
function safe(value, fallback = "") {
  return value === null || value === undefined ? fallback : value;
}

/**
 * 指定された key に対応する slot 内容だけを更新
 */
function randomizeSlot(data, key) {
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

  // updateSlotDisplay(`slot-${key}`, safe(contentMap[key]));
  console.log(`🔄 randomizeSlot called for ${key}:`, safe(contentMap[key]));
}

// === 新しい個別ランダマイズ機能（Sスロット専用テスト） ===

console.log("🎯 Sスロット個別ランダマイザー読み込み開始");

/**
 * Sスロット専用の個別ランダマイズ関数
 */
function randomizeSlotS() {
  console.log("🎲 Sスロット個別ランダマイズ開始");
  
  if (!window.loadedJsonData) {
    console.warn("⚠️ JSONデータが読み込まれていません");
    return;
  }
  
  try {
    // 現在のV_group_keyを取得（既存システムから）
    const currentVGroupKey = window.currentVGroupKey || getCurrentVGroupKey();
    if (!currentVGroupKey) {
      console.warn("⚠️ 現在のV_group_keyが特定できません");
      return;
    }
    
    console.log(`🎯 現在のV_group_key: ${currentVGroupKey}`);
    
    // 同じV_group_key内の全ての例文IDを取得
    const sameVGroupData = window.loadedJsonData.filter(item => 
      item.V_group_key === currentVGroupKey && 
      item.Slot && item.Slot.toLowerCase() === 's'
    );
    
    if (sameVGroupData.length === 0) {
      console.warn(`⚠️ V_group_key "${currentVGroupKey}" のSスロットデータが見つかりません`);
      return;
    }
    
    // 例文IDごとにグループ化
    const sentenceGroups = {};
    sameVGroupData.forEach(item => {
      const sentenceId = item.例文ID;
      if (!sentenceGroups[sentenceId]) {
        sentenceGroups[sentenceId] = [];
      }
      sentenceGroups[sentenceId].push(item);
    });
    
    const availableSentenceIds = Object.keys(sentenceGroups);
    console.log(`📊 同じV_group_key内の例文ID: ${availableSentenceIds.length}件`, availableSentenceIds);
    
    if (availableSentenceIds.length <= 1) {
      console.warn(`⚠️ V_group_key "${currentVGroupKey}" に複数の例文が存在しません（個別ランダマイズには最低2例文必要）`);
      return;
    }
    
    // 現在表示中の例文ID以外からランダム選択
    const currentSentenceId = getCurrentSentenceId();
    const otherSentenceIds = availableSentenceIds.filter(id => id !== currentSentenceId);
    
    if (otherSentenceIds.length === 0) {
      console.warn("⚠️ 現在の例文以外の選択肢が見つかりません");
      return;
    }
    
    const randomIndex = Math.floor(Math.random() * otherSentenceIds.length);
    const selectedSentenceId = otherSentenceIds[randomIndex];
    const selectedSentenceData = sentenceGroups[selectedSentenceId];
    
    console.log(`🎯 ランダマイズ選択例文ID: ${selectedSentenceId} (現在: ${currentSentenceId})`);
    console.log(`📊 選択例文のSスロットデータ: ${selectedSentenceData.length}件`);
    
    // 選択された例文のSスロット構造全体を取得
    // メインスロット + 全サブスロットを含む
    updateSSlotWithNewSentenceData(selectedSentenceData);
    
    console.log("✅ Sスロット個別ランダマイズ完了");
    
  } catch (error) {
    console.error("❌ Sスロット個別ランダマイズエラー:", error);
  }
}

/**
 * 現在のV_group_keyを取得
 */
function getCurrentVGroupKey() {
  // 既存システムから現在のV_group_keyを取得する方法を実装
  // とりあえず最初のデータからV_group_keyを取得
  if (window.loadedJsonData && window.loadedJsonData.length > 0) {
    return window.loadedJsonData[0].V_group_key;
  }
  return null;
}

/**
 * 現在の例文IDを取得
 */
function getCurrentSentenceId() {
  // 既存システムから現在の例文IDを取得する方法を実装
  // とりあえず最初のデータから例文IDを取得
  if (window.loadedJsonData && window.loadedJsonData.length > 0) {
    return window.loadedJsonData[0].例文ID;
  }
  return null;
}

/**
 * 選択された例文のSスロットデータで現在のSスロット表示を更新
 * @param {Array} newSentenceData - 新しい例文のSスロットデータ配列
 */
function updateSSlotWithNewSentenceData(newSentenceData) {
  console.log("🔄 Sスロット構造全体を新しい例文データで更新開始");
  
  // メインスロットデータを取得
  const mainSlotData = newSentenceData.find(item => 
    item.SubslotID === "" && 
    (item.PhraseType === "word" || item.PhraseType === "phrase" || item.PhraseType === "clause")
  );
  
  if (mainSlotData) {
    // メインスロット部分を更新
    updateSSlotDisplay(mainSlotData, false);
  }
  
  // サブスロットデータを取得して更新
  const subSlotData = newSentenceData.filter(item => 
    item.SubslotID !== "" && 
    item.SubslotText && 
    item.SubslotText.trim() !== ""
  );
  
  console.log(`📊 更新対象サブスロット: ${subSlotData.length}件`);
  
  // 各サブスロットを個別に更新
  subSlotData.forEach(subData => {
    console.log(`🔧 サブスロット ${subData.SubslotID} を更新:`, subData.SubslotText);
    updateSSlotDisplay(subData, true);
  });
}

/**
 * Sスロットの表示のみを更新（既存システムに影響しない）
 * @param {Object} data - 選択されたデータ
 * @param {boolean} isSubslot - サブスロットかどうか
 */
function updateSSlotDisplay(data, isSubslot = false) {
  const container = document.getElementById('slot-s');
  
  if (!container) {
    console.warn(`⚠️ Sスロットコンテナが見つかりません`);
    return;
  }
  
  console.log(`🔄 slot-s の表示更新開始 (${isSubslot ? 'サブスロット' : 'メインスロット'})`);
  console.log(`🔧 更新データ:`, data);
  
  if (isSubslot) {
    // サブスロットの場合：対応するサブスロット要素を更新
    // SubslotID "sub-aux" → slot-s-sub-aux
    const subslotId = `slot-s-${data.SubslotID}`;
    const subslotElement = document.getElementById(subslotId);
    
    console.log(`🔧 サブスロット要素検索: ${subslotId}`);
    console.log(`🔧 見つかったサブスロット要素:`, subslotElement);
    
    if (subslotElement) {
      // サブスロット要素内のテキスト部分を更新
      const textDiv = subslotElement.querySelector('.slot-text');
      if (textDiv) {
        const oldText = textDiv.textContent;
        textDiv.textContent = data.SubslotText || "SUBSLOT UPDATED";
        console.log(`✅ サブスロット ${data.SubslotID} text更新: "${oldText}" → "${textDiv.textContent}"`);
      } else {
        console.warn(`⚠️ サブスロット内の.slot-textが見つかりません: ${subslotId}`);
      }
    } else {
      console.warn(`⚠️ サブスロット要素が見つかりません: ${subslotId}`);
      console.log(`🔧 利用可能なサブスロット要素:`);
      const allSubslots = document.querySelectorAll('[id^="slot-s-sub-"]');
      allSubslots.forEach(sub => console.log(`🔧 - ${sub.id}`));
    }
  } else {
    // メインスロットの場合：従来通りの更新
    // phrase部分の更新
    const phraseDiv = container.querySelector(":scope > .slot-phrase");
    if (phraseDiv) {
      const oldPhrase = phraseDiv.textContent;
      phraseDiv.textContent = data.SlotPhrase || "PHRASE UPDATED";
      console.log(`✅ slot-s phrase更新: "${oldPhrase}" → "${phraseDiv.textContent}"`);
    }
    
    // text部分の更新
    const textDiv = container.querySelector(":scope > .slot-text");
    if (textDiv) {
      const oldText = textDiv.textContent;
      textDiv.textContent = data.SlotText || "TEXT UPDATED";
      console.log(`✅ slot-s text更新: "${oldText}" → "${textDiv.textContent}"`);
    }
  }
  
  // 視覚的な確認のため、一時的にボーダーを変更
  container.style.border = "3px solid red";
  setTimeout(() => {
    container.style.border = "";
  }, 1000);
}

/**
 * Sスロット用の個別ランダマイズボタンを設置
 */
function setupSSlotRandomizeButton() {
  const sContainer = document.getElementById('slot-s');
  if (!sContainer) {
    console.warn("⚠️ Sスロットコンテナが見つかりません");
    return;
  }
  
  // 既存の個別ランダマイズボタンがあれば削除
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
  
  // イベントリスナーを追加（既存システムとの競合を避ける）
  randomizeBtn.addEventListener('click', function(event) {
    event.stopPropagation(); // イベントの伝播を防ぐ
    event.preventDefault();
    
    console.log("🎲 Sスロット個別ランダマイズボタンがクリックされました");
    
    // デバッグ用：JSONデータの確認
    console.log("🔧 window.loadedJsonData:", window.loadedJsonData);
    
    // メイン処理を実行
    randomizeSlotS();
  }, true); // キャプチャフェーズでイベントを捕捉
  
  // スロットコンテナに相対位置を設定
  if (sContainer.style.position !== 'relative') {
    sContainer.style.position = 'relative';
  }
  
  // ボタンをスロットに追加
  sContainer.appendChild(randomizeBtn);
  
  console.log("✅ Sスロット個別ランダマイズボタンを設置しました");
}

/**
 * 初期化処理
 */
function initializeSSlotRandomizer() {
  console.log("🚀 Sスロット個別ランダマイザー初期化開始");
  
  // DOMが準備できるまで待機
  function setupWhenReady() {
    const sContainer = document.getElementById('slot-s');
    if (sContainer) {
      setupSSlotRandomizeButton();
      console.log("✅ Sスロットが見つかったのでボタンを設置しました");
    } else {
      console.log("⏳ Sスロットがまだ見つからないため、1秒後に再試行...");
      setTimeout(setupWhenReady, 1000);
    }
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupWhenReady);
  } else {
    setupWhenReady();
  }
  
  // JSONデータの読み込み完了を待機
  const checkDataInterval = setInterval(() => {
    if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
      console.log("✅ JSONデータ確認完了 - Sスロット個別ランダマイザー準備完了");
      clearInterval(checkDataInterval);
    }
  }, 500);
  
  console.log("✅ Sスロット個別ランダマイザー初期化完了");
}

// グローバル関数としてエクスポート
window.randomizeSlotS = randomizeSlotS;
window.setupSSlotRandomizeButton = setupSSlotRandomizeButton;

// デバッグ用：強制的にボタンを設置するテスト関数
window.debugSetupButton = function() {
  console.log("🔧 デバッグ: 強制的にSスロットボタン設置を試行");
  const sContainer = document.getElementById('slot-s');
  console.log("🔧 Sスロットコンテナ:", sContainer);
  
  if (sContainer) {
    console.log("🔧 Sスロットが見つかりました");
    setupSSlotRandomizeButton();
  } else {
    console.log("🔧 Sスロットが見つかりません - 利用可能なスロット:");
    const allSlots = document.querySelectorAll('[id^="slot-"]');
    allSlots.forEach(slot => console.log("🔧 発見されたスロット:", slot.id));
  }
};

// 自動初期化
initializeSSlotRandomizer();

// 追加の初期化タイミング（保険）
setTimeout(() => {
  console.log("🔧 追加初期化タイミング - 3秒後");
  window.debugSetupButton();
}, 3000);

console.log("✅ Sスロット個別ランダマイザー読み込み完了");