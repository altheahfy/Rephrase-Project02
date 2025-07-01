// 3要素表示制御システム - 全10スロット対応 + 分離疑問詞対応
// S, Aux, V, M1, M2, C1, O1, O2, C2, M3スロットの画像・補助テキスト・例文テキストの個別表示制御
// 分離疑問詞エリアの表示制御も含む

// 🎯 スロット定義（分離疑問詞を追加）
const ALL_SLOTS = ['s', 'aux', 'v', 'm1', 'm2', 'c1', 'o1', 'o2', 'c2', 'm3', 'question-word'];
const ELEMENT_TYPES = ['image', 'auxtext', 'text'];

// 🔧 表示状態を管理するオブジェクト
let visibilityState = {};

// 初期化：全要素を表示状態に設定（分離疑問詞を含む）
function initializeVisibilityState() {
  ALL_SLOTS.forEach(slot => {
    visibilityState[slot] = {};
    ELEMENT_TYPES.forEach(type => {
      // 分離疑問詞はimageを持たない
      if (slot === 'question-word' && type === 'image') {
        visibilityState[slot][type] = false;
      } else {
        visibilityState[slot][type] = true; // 初期状態は全て表示
      }
    });
  });
  console.log("🔄 表示状態を初期化しました（分離疑問詞含む）:", visibilityState);
}

// 🎛️ 個別スロット・要素の表示制御（分離疑問詞対応）
function toggleSlotElementVisibility(slotKey, elementType, isVisible) {
  if (!ALL_SLOTS.includes(slotKey)) {
    console.error(`❌ 無効なスロットキー: ${slotKey}`);
    return;
  }
  
  if (!ELEMENT_TYPES.includes(elementType)) {
    console.error(`❌ 無効な要素タイプ: ${elementType}`);
    return;
  }

  // 状態を更新
  visibilityState[slotKey][elementType] = isVisible;
  
  // 🆕 分離疑問詞の場合は専用処理
  if (slotKey === 'question-word') {
    // question_word_controller.jsの関数を呼び出し
    if (typeof applyQuestionWordVisibility === 'function') {
      applyQuestionWordVisibility();
      console.log(`✅ 分離疑問詞の${elementType}表示を更新しました: ${isVisible}`);
    }
    return;
  }
  
  // 通常のスロット処理
  const slotElement = document.getElementById(`slot-${slotKey}`);
  const className = `hidden-${slotKey}-${elementType}`;
  
  if (slotElement) {
    if (isVisible) {
      slotElement.classList.remove(className);
      console.log(`✅ ${slotKey}スロットの${elementType}を表示しました`);
    } else {
      slotElement.classList.add(className);
      console.log(`🙈 ${slotKey}スロットの${elementType}を非表示にしました`);
    }
    
    // サブスロットも同様に制御
    const subSlots = document.querySelectorAll(`[id^="slot-${slotKey}-sub-"]`);
    subSlots.forEach(subSlot => {
      if (isVisible) {
        subSlot.classList.remove(className);
      } else {
        subSlot.classList.add(className);
      }
    });
    
    console.log(`🔄 ${slotKey}スロットのサブスロット${subSlots.length}個も更新しました`);
  } else {
    console.warn(`⚠ スロット要素が見つかりません: slot-${slotKey}`);
  }
  
  // localStorage に状態を保存
  saveVisibilityState();
}

// 📁 表示状態をlocalStorageに保存
function saveVisibilityState() {
  try {
    localStorage.setItem('rephrase_visibility_state', JSON.stringify(visibilityState));
    console.log("💾 表示状態を保存しました");
  } catch (error) {
    console.error("❌ 表示状態の保存に失敗:", error);
  }
}

// 📂 表示状態をlocalStorageから読み込み
function loadVisibilityState() {
  try {
    const saved = localStorage.getItem('rephrase_visibility_state');
    if (saved) {
      visibilityState = JSON.parse(saved);
      console.log("📂 保存された表示状態を読み込みました:", visibilityState);
      
      // 読み込んだ状態をDOMに適用
      applyVisibilityState();
    } else {
      console.log("📝 保存された表示状態がないため、初期化します");
      initializeVisibilityState();
    }
  } catch (error) {
    console.error("❌ 表示状態の読み込みに失敗:", error);
    initializeVisibilityState();
  }
}

// 🎨 現在の表示状態をDOMに適用
function applyVisibilityState() {
  ALL_SLOTS.forEach(slotKey => {
    ELEMENT_TYPES.forEach(elementType => {
      const isVisible = visibilityState[slotKey]?.[elementType] ?? true;
      const slotElement = document.getElementById(`slot-${slotKey}`);
      const className = `hidden-${slotKey}-${elementType}`;
      
      if (slotElement) {
        if (isVisible) {
          slotElement.classList.remove(className);
        } else {
          slotElement.classList.add(className);
        }
        
        // サブスロットも同様に適用
        const subSlots = document.querySelectorAll(`[id^="slot-${slotKey}-sub-"]`);
        subSlots.forEach(subSlot => {
          if (isVisible) {
            subSlot.classList.remove(className);
          } else {
            subSlot.classList.add(className);
          }
        });
      }
    });
  });
  console.log("🎨 表示状態をDOMに適用しました");
}

// 🔄 特定スロットの全要素表示をリセット
function resetSlotVisibility(slotKey) {
  if (!ALL_SLOTS.includes(slotKey)) {
    console.error(`❌ 無効なスロットキー: ${slotKey}`);
    return;
  }
  
  ELEMENT_TYPES.forEach(elementType => {
    toggleSlotElementVisibility(slotKey, elementType, true);
  });
  console.log(`🔄 ${slotKey}スロットの表示をリセットしました`);
}

// 🔄 全スロットの表示をリセット
function resetAllVisibility() {
  ALL_SLOTS.forEach(slotKey => {
    resetSlotVisibility(slotKey);
  });
  console.log("🔄 全スロットの表示をリセットしました");
}

// 📊 現在の表示状態を取得
function getVisibilityState() {
  return { ...visibilityState };
}

// 📊 特定スロットの表示状態を取得
function getSlotVisibilityState(slotKey) {
  return visibilityState[slotKey] ? { ...visibilityState[slotKey] } : null;
}

// 🔹 グローバル関数としてエクスポート
window.initializeVisibilityState = initializeVisibilityState;
window.toggleSlotElementVisibility = toggleSlotElementVisibility;
window.loadVisibilityState = loadVisibilityState;
window.saveVisibilityState = saveVisibilityState;
window.applyVisibilityState = applyVisibilityState;
window.resetSlotVisibility = resetSlotVisibility;
window.resetAllVisibility = resetAllVisibility;
window.getVisibilityState = getVisibilityState;
window.getSlotVisibilityState = getSlotVisibilityState;

// 🎛️ UI制御パネルとの連携
function setupVisibilityControlUI() {
  console.log("🎛️ 表示制御UIのイベントハンドラーを設定中...");
  
  // チェックボックスのイベントハンドラー
  const checkboxes = document.querySelectorAll('.visibility-checkbox');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const slotKey = this.dataset.slot;
      const elementType = this.dataset.type;
      const isVisible = this.checked;
      
      console.log(`🎛️ UIチェンジ: ${slotKey}-${elementType} = ${isVisible}`);
      toggleSlotElementVisibility(slotKey, elementType, isVisible);
    });
  });
  
  // 全表示ボタン
  const resetAllButton = document.getElementById('reset-all-visibility');
  if (resetAllButton) {
    resetAllButton.addEventListener('click', function() {
      console.log("🔄 全表示ボタンがクリックされました");
      resetAllVisibility();
      
      // UIのチェックボックスも全てチェック状態に戻す
      const allCheckboxes = document.querySelectorAll('.visibility-checkbox');
      allCheckboxes.forEach(cb => cb.checked = true);
    });
  }
  
  // 折畳みボタン（新しいUIには存在しないのでコメントアウト）
  /*
  const togglePanelButton = document.getElementById('toggle-visibility-panel');
  const controlsContainer = document.getElementById('slot-controls-container');
  if (togglePanelButton && controlsContainer) {
    togglePanelButton.addEventListener('click', function() {
      if (controlsContainer.style.display === 'none') {
        controlsContainer.style.display = '';
        togglePanelButton.textContent = '折畳';
        console.log("📖 表示制御パネルを展開しました");
      } else {
        controlsContainer.style.display = 'none';
        togglePanelButton.textContent = '展開';
        console.log("📕 表示制御パネルを折り畳みました");
      }
    });
  }
  */
  
  console.log(`✅ 表示制御UI設定完了: チェックボックス${checkboxes.length}個`);
}

// 🔄 保存状態に基づいてUIを更新
function updateUIFromState() {
  console.log("🔄 保存状態に基づいてUIを更新中...");
  
  ALL_SLOTS.forEach(slotKey => {
    ELEMENT_TYPES.forEach(elementType => {
      const isVisible = visibilityState[slotKey]?.[elementType] ?? true;
      const checkbox = document.querySelector(`.visibility-checkbox[data-slot="${slotKey}"][data-type="${elementType}"]`);
      
      if (checkbox) {
        checkbox.checked = isVisible;
      }
    });
  });
  
  console.log("✅ UIの更新が完了しました");
}

// 既存のloadVisibilityState関数を拡張
const originalLoadVisibilityState = loadVisibilityState;
loadVisibilityState = function() {
  originalLoadVisibilityState();
  updateUIFromState();
};

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 3要素表示制御システムを初期化中...");
  loadVisibilityState();
  
  // UI設定は少し遅らせて実行（DOM構築完了を確実にするため）
  setTimeout(() => {
    setupVisibilityControlUI();
  }, 100);
});

console.log("✅ visibility_control.js が読み込まれました");
