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
    // Sスロット用のデータを取得
    const sSlotData = window.loadedJsonData.filter(item => 
      item.Slot && item.Slot.toLowerCase() === 's' && 
      item.SubslotID === "" && 
      item.PhraseType === "word"
    );
    
    if (sSlotData.length === 0) {
      console.warn("⚠️ Sスロットのデータが見つかりません");
      return;
    }
    
    console.log(`📊 Sスロット候補データ: ${sSlotData.length}件`);
    
    // ランダムに1つ選択
    const randomIndex = Math.floor(Math.random() * sSlotData.length);
    const selectedData = sSlotData[randomIndex];
    
    console.log(`🎯 選択されたSスロットデータ:`, selectedData);
    
    // Sスロットの表示を更新（DOM操作は最小限に）
    updateSSlotDisplay(selectedData);
    
    console.log("✅ Sスロット個別ランダマイズ完了");
    
  } catch (error) {
    console.error("❌ Sスロット個別ランダマイズエラー:", error);
  }
}

/**
 * Sスロットの表示のみを更新（既存システムに影響しない）
 */
function updateSSlotDisplay(data) {
  const container = document.getElementById('slot-s');
  
  if (!container) {
    console.warn(`⚠️ Sスロットコンテナが見つかりません`);
    return;
  }
  
  console.log(`🔄 slot-s の表示更新開始`);
  
  // phrase部分の更新
  const phraseDiv = container.querySelector(":scope > .slot-phrase");
  if (phraseDiv && data.SlotPhrase) {
    phraseDiv.textContent = data.SlotPhrase;
    console.log(`✅ slot-s phrase更新: "${data.SlotPhrase}"`);
  }
  
  // text部分の更新
  const textDiv = container.querySelector(":scope > .slot-text");
  if (textDiv && data.SlotText) {
    // 既存の実装に合わせてテキストノードを安全に更新
    if (textDiv.firstChild && textDiv.firstChild.nodeType === Node.TEXT_NODE) {
      textDiv.firstChild.textContent = data.SlotText;
    } else {
      textDiv.textContent = "";
      textDiv.append(document.createTextNode(data.SlotText));
    }
    console.log(`✅ slot-s text更新: "${data.SlotText}"`);
  }
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
    randomizeSlotS();
  });
  
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
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupSSlotRandomizeButton);
  } else {
    setupSSlotRandomizeButton();
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

// 自動初期化
initializeSSlotRandomizer();

console.log("✅ Sスロット個別ランダマイザー読み込み完了");