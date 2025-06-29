import { updateSlotDisplay } from './image_handler.js';
import { buildStructure } from './structure_builder.js';

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
 * Sスロット専用の個別ランダマイズ関数（動的記載エリア更新のみ）
 * 同じV_group_key内の他の例文からSスロット（メイン+サブスロット）をランダム選択して置き換える
 * MutationObserver経由で自動的に静的DOMに同期される
 */
function randomizeSlotSIndividual() {
  console.log("🎲 Sスロット個別ランダマイズ開始（動的記載エリア更新のみ）");
  
  // window.slotSetsが存在するかチェック（randomizer_all.jsで設定される）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  console.log(`📊 利用可能な例文セット数: ${window.slotSets.length}`);
  
  // === 全体ランダマイズと同じ仕組みを使用 ===
  // Sスロット候補を抽出（全体ランダマイズのロジックをコピー）
  const candidates = window.slotSets.flat().filter(entry => entry.Slot === "S");
  
  if (candidates.length === 0) {
    console.warn("⚠️ Sスロット候補が見つかりません");
    return;
  }
  
  console.log(`📊 利用可能なSスロット候補: ${candidates.length}個`);
  
  // ランダムに1つ選択（全体ランダマイズと同じ仕組み）
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 選択されたSスロットに関連するサブスロットも取得（全体ランダマイズと同じ仕組み）
  const groupSlots = window.slotSets.flat(); // 全データを平坦化
  const relatedSubslots = groupSlots.filter(e =>
    e.例文ID === chosen.例文ID &&
    e.Slot === chosen.Slot &&
    e.SubslotID
  );
  
  console.log(`📊 関連サブスロット: ${relatedSubslots.length}個`);
  
  // 選択されたSスロット（メイン + サブスロット）を構築
  const newSSlotData = [chosen, ...relatedSubslots];
  
  console.log("🎯 最終的な新Sスロットデータ:", newSSlotData);
  
  // 動的記載エリアのみを更新（静的DOM更新は行わない）
  updateDynamicSlotAreaOnly(newSSlotData);
  
  console.log("✅ Sスロット個別ランダマイズ完了（動的記載エリア更新のみ、静的DOM同期は自動実行）");
}

/**
 * 動的記載エリアのみを更新する関数
 * MutationObserverが変更を検出して、自動的に静的DOMに同期される
 * @param {Array} newSSlotData - 新しいSスロットデータ（メイン+サブスロット）
 */
function updateDynamicSlotAreaOnly(newSSlotData) {
  console.log("🔄 動的記載エリアのみを更新開始");
  
  // 動的記載エリアを取得
  const dynamicArea = document.getElementById("dynamic-slot-area");
  if (!dynamicArea) {
    console.warn("⚠️ 動的記載エリア(dynamic-slot-area)が見つかりません");
    return;
  }
  
  // 現在のSスロット関連要素を削除
  const existingSSlots = dynamicArea.querySelectorAll('[id^="slot-s"], [id*="-s-"]');
  existingSSlots.forEach(element => {
    console.log(`🗑️ 既存のSスロット要素を削除: ${element.id}`);
    element.remove();
  });
  
  // 新しいSスロットデータを動的記載エリアに追加
  newSSlotData.forEach(slotData => {
    const slotElement = createDynamicSlotElement(slotData);
    if (slotElement) {
      dynamicArea.appendChild(slotElement);
      console.log(`✅ 動的記載エリアに追加: ${slotElement.id}`);
    }
  });
  
  console.log("✅ 動的記載エリア更新完了");
}

/**
 * 動的記載エリア用のスロット要素を作成
 * @param {Object} slotData - スロットデータ
 * @returns {HTMLElement|null} - 作成されたスロット要素
 */
function createDynamicSlotElement(slotData) {
  if (!slotData || !slotData.Slot) {
    console.warn("⚠️ 無効なスロットデータ:", slotData);
    return null;
  }
  
  // スロットIDを生成
  let slotId = `slot-${slotData.Slot.toLowerCase()}`;
  if (slotData.SubslotID) {
    slotId += `-sub-${slotData.SubslotID}`;
  }
  
  // スロット要素を作成
  const slotElement = document.createElement('div');
  slotElement.id = slotId;
  slotElement.className = slotData.SubslotID ? 'subslot' : 'slot';
  
  // フレーズ表示部分
  const phraseDiv = document.createElement('div');
  phraseDiv.className = slotData.SubslotID ? 'subslot-element' : 'slot-phrase';
  phraseDiv.textContent = slotData.SlotPhrase || '';
  
  // テキスト表示部分
  const textDiv = document.createElement('div');
  textDiv.className = slotData.SubslotID ? 'subslot-text' : 'slot-text';
  textDiv.textContent = slotData.SlotText || '';
  
  slotElement.appendChild(phraseDiv);
  slotElement.appendChild(textDiv);
  
  console.log(`🔧 動的スロット要素作成: ${slotId}`, slotData);
  
  return slotElement;
}

// グローバル関数としてもエクスポート（動的記載エリア対応版）
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

/**
 * Sスロット個別ランダマイズボタンを静的スロットに設置
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
  
  // クリックイベント - 動的記載エリアを更新するだけ
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

// デバッグ用のヘルパー関数
window.debugIndividualRandomizer = function() {
  console.log("🔍 個別ランダマイザーデバッグ:");
  console.log("  window.loadedJsonData:", window.loadedJsonData);
  console.log("  window.slotSets:", window.slotSets);
  console.log("  動的記載エリア:", document.getElementById("dynamic-slot-area"));
};

console.log("✅ 個別ランダマイザー読み込み完了（動的記載エリア対応版）");