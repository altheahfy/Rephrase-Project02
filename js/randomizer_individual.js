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
 * Sスロット専用の個別ランダマイズ関数
 * 同じV_group_key内の他の例文からSスロット（メイン+サブスロット）をランダム選択して置き換える
 * 動的記載エリア（dynamic-content-area）のみを更新し、MutationObserver経由で静的DOMに反映
 */
function randomizeSlotSIndividual() {
  console.log("🎲 Sスロット個別ランダマイズ開始");
  
  // window.slotSetsが存在するかチェック（randomizer_all.jsで設定される）
  if (!window.slotSets || !Array.isArray(window.slotSets)) {
    console.warn("⚠️ window.slotSetsが見つかりません。先に全体ランダマイズを実行してください。");
    return;
  }
  
  console.log(`📊 利用可能な例文セット数: ${window.slotSets.length}`);
  
  // === 現在表示中のSスロットを取得（比較用） ===
  const dynamicArea = document.getElementById('dynamic-content-area');
  if (!dynamicArea) {
    console.warn("⚠️ 動的記載エリアが見つかりません");
    return;
  }
  
  const currentSSlot = dynamicArea.querySelector('[data-slot="S"]');
  const currentSExampleId = currentSSlot ? currentSSlot.getAttribute('data-example-id') : null;
  console.log(`📄 現在のSスロット例文ID: ${currentSExampleId}`);
  
  // === Sスロット候補を抽出（現在表示中以外の例文から選択） ===
  const allSlots = window.slotSets.flat();
  const candidates = allSlots.filter(entry => 
    entry.Slot === "S" && 
    entry.例文ID !== currentSExampleId // 現在表示中以外から選択
  );
  
  if (candidates.length === 0) {
    console.warn("⚠️ 現在表示中以外のSスロット候補が見つかりません");
    return;
  }
  
  console.log(`📊 利用可能なSスロット候補: ${candidates.length}個（現在表示中を除く）`);
  
  // ランダムに1つ選択
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  console.log(`🎯 選択されたSスロット:`, chosen);
  
  // 選択されたSスロットに関連するサブスロットも取得
  const relatedSubslots = allSlots.filter(e =>
    e.例文ID === chosen.例文ID &&
    e.Slot === chosen.Slot &&
    e.SubslotID
  );
  
  console.log(`📊 関連サブスロット: ${relatedSubslots.length}個`);
  
  // 選択されたSスロット（メイン + サブスロット）を構築
  const newSSlotData = [chosen, ...relatedSubslots];
  
  console.log("🎯 最終的な新Sスロットデータ:", newSSlotData);
  
  // 動的記載エリアのSスロットのみを更新（MutationObserver経由で静的DOMに反映される）
  updateDynamicAreaSSlotOnly(newSSlotData);
  
  console.log("✅ Sスロット個別ランダマイズ完了");
}

/**
 * 動的記載エリア（dynamic-content-area）のSスロットのみを更新
 * @param {Array} newSSlotData - 新しいSスロットデータ（メイン+サブスロット）
 */
function updateDynamicAreaSSlotOnly(newSSlotData) {
  console.log("🔄 動的記載エリアのSスロット更新開始");
  
  const dynamicArea = document.getElementById('dynamic-content-area');
  if (!dynamicArea) {
    console.warn("⚠️ 動的記載エリアが見つかりません");
    return;
  }
  
  // Sスロットのメインデータを取得
  const mainSSlot = newSSlotData.find(item => !item.SubslotID);
  if (!mainSSlot) {
    console.warn("⚠️ メインSスロットデータが見つかりません");
    return;
  }
  
  // 動的記載エリア内のSスロット要素を探す
  let sSlotElement = dynamicArea.querySelector('[data-slot="S"]');
  
  if (!sSlotElement) {
    // Sスロット要素が存在しない場合は作成
    sSlotElement = document.createElement('div');
    sSlotElement.setAttribute('data-slot', 'S');
    dynamicArea.appendChild(sSlotElement);
    console.log("📝 新しいSスロット要素を作成しました");
  }
  
  // Sスロット要素の属性とテキストを更新
  sSlotElement.setAttribute('data-example-id', mainSSlot.例文ID || '');
  sSlotElement.setAttribute('data-v-group-key', mainSSlot.V_group_key || '');
  sSlotElement.textContent = mainSSlot.Content || '';
  
  console.log(`📝 Sスロット更新: ${mainSSlot.Content} (例文ID: ${mainSSlot.例文ID})`);
  
  // サブスロットの更新
  const subslots = newSSlotData.filter(item => item.SubslotID);
  console.log(`📊 サブスロット更新数: ${subslots.length}個`);
  
  subslots.forEach(subslot => {
    const subslotId = `${subslot.Slot.toLowerCase()}-${subslot.SubslotID}`;
    let subslotElement = dynamicArea.querySelector(`[data-subslot="${subslotId}"]`);
    
    if (!subslotElement) {
      // サブスロット要素が存在しない場合は作成
      subslotElement = document.createElement('div');
      subslotElement.setAttribute('data-subslot', subslotId);
      dynamicArea.appendChild(subslotElement);
      console.log(`� 新しいサブスロット要素を作成: ${subslotId}`);
    }
    
    // サブスロット要素の属性とテキストを更新
    subslotElement.setAttribute('data-example-id', subslot.例文ID || '');
    subslotElement.setAttribute('data-v-group-key', subslot.V_group_key || '');
    subslotElement.textContent = subslot.Content || '';
    
    console.log(`📝 サブスロット更新: ${subslotId} = ${subslot.Content}`);
  });
  
  console.log("✅ 動的記載エリアのSスロット更新完了");
}

// === 初期化関数 ===
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

// Sスロット個別ランダマイズボタンは静的HTML側で設置済みのため、動的設置処理は削除

/**
 * 初期化処理（動的ボタン設置は削除）
 */
export function initializeIndividualRandomizers() {
  console.log("🚀 個別ランダマイザー初期化完了（ボタンは静的HTML側で設置済み）");
}

// グローバル関数エクスポート（ボタンイベント用）
window.randomizeSlotSIndividual = randomizeSlotSIndividual;

// デバッグ用のヘルパー関数
window.debugIndividualRandomizer = function() {
  console.log("🔍 個別ランダマイザーデバッグ:");
  console.log("  window.loadedJsonData:", window.loadedJsonData);
  console.log("  window.slotSets:", window.slotSets);
  
  // 現在の動的記載エリア状況
  const dynamicArea = document.getElementById('dynamic-content-area');
  if (dynamicArea) {
    const currentSSlot = dynamicArea.querySelector('[data-slot="S"]');
    const currentSExampleId = currentSSlot ? currentSSlot.getAttribute('data-example-id') : null;
    console.log("  現在のSスロット例文ID:", currentSExampleId);
  }
};

console.log("✅ 個別ランダマイザー読み込み完了");