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
  
  // window.slotSetsが存在するかチェック（randomizer_all.jsで設定される）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  // 現在表示中のデータから例文IDを取得
  const currentSentenceId = getCurrentSentenceId();
  if (!currentSentenceId) {
    console.warn("⚠️ 現在の例文IDが特定できません");
    return;
  }
  
  console.log(`📍 現在の例文ID: ${currentSentenceId}`);
  console.log(`📊 利用可能な例文セット数: ${window.slotSets.length}`);
  
  // 現在の例文以外のセットを取得
  const otherSentenceSets = window.slotSets.filter(sentenceSet => {
    if (!sentenceSet || sentenceSet.length === 0) return false;
    const sentenceId = sentenceSet[0]?.例文ID;
    return sentenceId && sentenceId !== currentSentenceId;
  });
  
  if (otherSentenceSets.length === 0) {
    console.warn("⚠️ 他の例文セットが見つかりません（個別ランダマイズには最低2例文必要）");
    return;
  }
  
  console.log(`📊 他の例文セット数: ${otherSentenceSets.length}`);
  
  // ランダムに1つの例文セットを選択
  const randomIndex = Math.floor(Math.random() * otherSentenceSets.length);
  const selectedSentenceSet = otherSentenceSets[randomIndex];
  const selectedSentenceId = selectedSentenceSet[0]?.例文ID;
  
  console.log(`🎯 選択された例文ID: ${selectedSentenceId}`);
  
  // 選択された例文セットからSスロットデータを抽出
  const selectedSSlotData = selectedSentenceSet.filter(item => 
    item.Slot && item.Slot.toLowerCase() === 's'
  );
  
  if (selectedSSlotData.length === 0) {
    console.warn("⚠️ 選択された例文にSスロットデータが見つかりません");
    return;
  }
  
  console.log(`📊 選択されたSスロットデータ: ${selectedSSlotData.length}件`, selectedSSlotData);
  
  // 現在のSスロット表示を選択されたデータで更新
  updateSSlotWithNewData(selectedSSlotData);
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

/**
 * 現在表示中の例文IDを取得
 */
function getCurrentSentenceId() {
  if (window.loadedJsonData && window.loadedJsonData.length > 0) {
    return window.loadedJsonData[0]?.例文ID;
  }
  return null;
}

/**
 * 選択されたSスロットデータで現在のSスロット表示を更新
 * @param {Array} newSSlotData - 新しいSスロットデータ（メイン+サブスロット）
 */
function updateSSlotWithNewData(newSSlotData) {
  console.log("🔄 Sスロット表示更新開始");
  
  // メインスロットデータを取得（SubslotID=""で、PhraseTypeが指定されているもの）
  const mainSlotData = newSSlotData.find(item => 
    !item.SubslotID && 
    (item.PhraseType === "word" || item.PhraseType === "phrase" || item.PhraseType === "clause")
  );
  
  if (mainSlotData) {
    console.log("🔧 メインSスロット更新:", mainSlotData);
    updateSSlotDisplay(mainSlotData, false);
  }
  
  // サブスロットデータを取得して更新
  const subSlotData = newSSlotData.filter(item => 
    item.SubslotID && 
    (item.SubslotElement || item.SubslotText)
  );
  
  console.log(`📊 更新対象サブスロット: ${subSlotData.length}件`);
  
  // 各サブスロットを個別に更新
  subSlotData.forEach(subData => {
    console.log(`🔧 サブスロット ${subData.SubslotID} を更新:`, subData);
    updateSSlotDisplay(subData, true);
  });
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
 * 初期化処理
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

// グローバル関数としてエクスポート
window.randomizeSlotSIndividual = randomizeSlotSIndividual;
window.setupSSlotRandomizeButton = setupSSlotRandomizeButton;

// 自動初期化
initializeIndividualRandomizer();

console.log("✅ 個別ランダマイザー読み込み完了");