// 3要素表示制御システム - 全10スロット対応
// S, Aux, V, M1, M2, C1, O1, O2, C2, M3スロットの画像・補助テキスト・例文テキストの個別表示制御

// 🎯 スロット定義
const ALL_SLOTS = ['s', 'aux', 'v', 'm1', 'm2', 'c1', 'o1', 'o2', 'c2', 'm3'];
const ELEMENT_TYPES = ['auxtext', 'text'];

// 🔧 表示状態を管理するオブジェクト
let visibilityState = {};

// 初期化：全要素を表示状態に設定
function initializeVisibilityState() {
  ALL_SLOTS.forEach(slot => {
    visibilityState[slot] = {};
    ELEMENT_TYPES.forEach(type => {
      visibilityState[slot][type] = true; // 初期状態は全て表示
    });
  });
  console.log("🔄 表示状態を初期化しました:", visibilityState);
}

// 🎛️ 個別スロット・要素の表示制御
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
  
  // 🆕 グローバル参照も更新（inline_visibility_toggle.jsが参照するため）
  window.visibilityState = visibilityState;
  
  // DOM要素を取得
  const slotElement = document.getElementById(`slot-${slotKey}`);
  const className = `hidden-${elementType}`; // CSSクラス名に合わせて修正
  
  if (slotElement) {
    if (isVisible) {
      slotElement.classList.remove(className);
      console.log(`✅ ${slotKey}スロットの${elementType}を表示しました`);
    } else {
      slotElement.classList.add(className);
      console.log(`🙈 ${slotKey}スロットの${elementType}を非表示にしました`);
    }
    
    // 🆕 英語例文（text要素）の直接制御
    if (elementType === 'text') {
      const textElement = slotElement.querySelector('.slot-phrase');
      if (textElement) {
        if (isVisible) {
          textElement.style.opacity = '1';
          textElement.style.visibility = 'visible';
          console.log(`✅ ${slotKey}スロットの英語例文を表示しました`);
        } else {
          textElement.style.opacity = '0';
          textElement.style.visibility = 'hidden';
          console.log(`🙈 ${slotKey}スロットの英語例文を非表示にしました`);
        }
      }
    }
    
    // サブスロットも同様に制御
    const subSlots = document.querySelectorAll(`[id^="slot-${slotKey}-sub-"]`);
    console.log(`🔍 DEBUG: ${slotKey}のサブスロット検索結果: ${subSlots.length}個`);
    subSlots.forEach(subSlot => {
      console.log(`🔍 DEBUG: サブスロット処理中: ${subSlot.id}, isVisible=${isVisible}`);
      if (isVisible) {
        subSlot.classList.remove(className);
        // 🆕 syncSubslotsFromJsonが追加するクラスも除去
        subSlot.classList.remove('hidden-subslot-text');
        subSlot.classList.remove('hidden-subslot-auxtext');
      } else {
        subSlot.classList.add(className);
        // 🆕 syncSubslotsFromJsonと同じクラスも追加
        if (elementType === 'text') {
          subSlot.classList.add('hidden-subslot-text');
        } else if (elementType === 'auxtext') {
          subSlot.classList.add('hidden-subslot-auxtext');
        }
      }
      
      // 🆕 サブスロットの英語例文（text要素）も直接制御
      if (elementType === 'text') {
        const subTextElement = subSlot.querySelector('.slot-phrase');
        console.log(`🔍 DEBUG: サブスロット ${subSlot.id} の .slot-phrase 要素: ${subTextElement ? '存在' : '不存在'}`);
        if (subTextElement) {
          if (isVisible) {
            subTextElement.style.opacity = '1';
            subTextElement.style.visibility = 'visible';
            console.log(`✅ ${subSlot.id} の英語例文を表示しました (opacity=1, visibility=visible)`);
          } else {
            subTextElement.style.opacity = '0';
            subTextElement.style.visibility = 'hidden';
            console.log(`🙈 ${subSlot.id} の英語例文を非表示にしました (opacity=0, visibility=hidden)`);
          }
        }
      }
    });
    
    console.log(`🔄 ${slotKey}スロットのサブスロット${subSlots.length}個も更新しました`);
  } else {
    console.warn(`⚠ スロット要素が見つかりません: slot-${slotKey}`);
  }
  
  // localStorage に状態を保存
  saveVisibilityState();
}

// 📁 表示状態をstate-manager経由で保存
function saveVisibilityState() {
  try {
    // 🎯 **修正：state-manager経由で状態保存**
    if (window.RephraseState) {
      window.RephraseState.setState('visibility.slots', visibilityState);
      console.log("💾 表示状態をstate-manager経由で保存しました");
    } else {
      // フォールバック：直接localStorage保存
      localStorage.setItem('rephrase_visibility_state', JSON.stringify(visibilityState));
      console.log("💾 表示状態を直接localStorageに保存しました（state-manager未利用）");
    }
    
    // 🆕 グローバル参照も更新（inline_visibility_toggle.jsが参照するため）
    window.visibilityState = visibilityState;
  } catch (error) {
    console.error("❌ 表示状態の保存に失敗:", error);
  }
}

// 📂 表示状態をstate-manager経由で読み込み
function loadVisibilityState() {
  try {
    // 🎯 **修正：state-manager経由で状態読み込み**
    if (window.RephraseState) {
      const savedState = window.RephraseState.getState('visibility.slots');
      if (savedState && Object.keys(savedState).length > 0) {
        visibilityState = savedState;
        console.log("📂 state-manager経由で表示状態を読み込みました:", visibilityState);
      } else {
        console.log("📝 state-managerに保存された状態がないため、初期化します");
        initializeVisibilityState();
      }
    } else {
      // フォールバック：直接localStorage読み込み
      const saved = localStorage.getItem('rephrase_visibility_state');
      if (saved) {
        visibilityState = JSON.parse(saved);
        console.log("📂 直接localStorageから表示状態を読み込みました:", visibilityState);
      } else {
        console.log("📝 保存された表示状態がないため、初期化します");
        initializeVisibilityState();
      }
    }
    
    // 読み込んだ状態をDOMに適用
    applyVisibilityState();
    
    // 🆕 グローバル参照を更新
    window.visibilityState = visibilityState;
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
        
        // 🆕 英語例文（text要素）の直接制御
        if (elementType === 'text') {
          const textElement = slotElement.querySelector('.slot-phrase');
          if (textElement) {
            if (isVisible) {
              textElement.style.opacity = '1';
              textElement.style.visibility = 'visible';
            } else {
              textElement.style.opacity = '0';
              textElement.style.visibility = 'hidden';
            }
          }
        }
        
        // サブスロットも同様に適用
        const subSlots = document.querySelectorAll(`[id^="slot-${slotKey}-sub-"]`);
        subSlots.forEach(subSlot => {
          if (isVisible) {
            subSlot.classList.remove(className);
          } else {
            subSlot.classList.add(className);
          }
          
          // 🆕 サブスロットの英語例文（text要素）も直接制御
          if (elementType === 'text') {
            const subTextElement = subSlot.querySelector('.slot-phrase');
            if (subTextElement) {
              if (isVisible) {
                subTextElement.style.opacity = '1';
                subTextElement.style.visibility = 'visible';
              } else {
                subTextElement.style.opacity = '0';
                subTextElement.style.visibility = 'hidden';
              }
            }
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
  
  // 🆕 全サブスロットの英文状態もlocalStorageでリセット
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    let visibilityState = {};
    if (saved) {
      visibilityState = JSON.parse(saved);
    }
    
    // 全親スロットの全サブスロットの英文をtrueに設定
    const PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
    const SUBSLOT_TYPES = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
    
    PARENT_SLOTS.forEach(parentSlot => {
      SUBSLOT_TYPES.forEach(subslotType => {
        const subslotId = `slot-${parentSlot.toLowerCase()}-sub-${subslotType.toLowerCase()}`;
        if (!visibilityState[subslotId]) {
          visibilityState[subslotId] = {};
        }
        visibilityState[subslotId].text = true;
      });
    });
    
    localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(visibilityState));
    console.log("🔄 全サブスロットの英文状態をlocalStorageでリセットしました");
    
    // 🆕 現在画面上にあるサブスロットの表示も直接更新
    PARENT_SLOTS.forEach(parentSlot => {
      SUBSLOT_TYPES.forEach(subslotType => {
        const subslotId = `slot-${parentSlot.toLowerCase()}-sub-${subslotType.toLowerCase()}`;
        const subslotElement = document.getElementById(subslotId);
        
        if (subslotElement) {
          // 非表示クラスを削除
          subslotElement.classList.remove('hidden-subslot-text');
          
          // 英文要素の直接制御
          const textElements = subslotElement.querySelectorAll('.slot-phrase');
          textElements.forEach(textElement => {
            textElement.style.opacity = '1';
            textElement.style.visibility = 'visible';
          });
          
          console.log(`🔄 ${subslotId}の英文表示を復活させました`);
        }
      });
    });
    
    // サブスロット制御パネルのボタンも更新
    const subslotPanels = document.querySelectorAll('.subslot-visibility-panel');
    subslotPanels.forEach(panel => {
      const textButtons = panel.querySelectorAll('.subslot-toggle-button[data-element-type="text"]');
      textButtons.forEach(button => {
        // ボタンスタイルを表示状態に更新
        if (window.updateToggleButtonStyle) {
          window.updateToggleButtonStyle(button, true);
        }
      });
    });
    
  } catch (error) {
    console.error("❌ サブスロット英文状態のリセットに失敗:", error);
  }
  
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
window.visibilityState = visibilityState; // 🆕 状態オブジェクトを公開
window.getSlotVisibilityState = getSlotVisibilityState;

// 🎛️ UI制御パネルとの連携
function setupVisibilityControlUI() {
  console.log("🎛️ 表示制御UIのイベントハンドラーを設定中...");
  
  // チェックボックスのイベントハンドラー（スロット用・疑問詞用）
  const checkboxes = document.querySelectorAll('.visibility-checkbox');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const slotKey = this.dataset.slot;
      const elementType = this.dataset.type;
      const isVisible = this.checked;
      
      console.log(`🎛️ UIチェンジ: ${slotKey}-${elementType} = ${isVisible}`);
      
      // 🆕 チェックボックスの親label要素の背景色を変更（英文のみ）
      if (elementType === 'text') {
        const labelElement = this.closest('label');
        if (labelElement) {
          if (isVisible) {
            labelElement.style.backgroundColor = '#4CAF50'; // 緑色
            labelElement.style.color = 'white';
            labelElement.style.padding = '2px 6px';
            labelElement.style.borderRadius = '3px';
          } else {
            labelElement.style.backgroundColor = '#757575'; // グレー色
            labelElement.style.color = 'white';
            labelElement.style.padding = '2px 6px';
            labelElement.style.borderRadius = '3px';
          }
        }
      }
      
      // 疑問詞の場合
      if (slotKey === 'question-word') {
        // question_word_visibility.js の関数を呼び出し
        if (window.toggleQuestionWordVisibility) {
          window.toggleQuestionWordVisibility(elementType, isVisible);
        } else {
          console.warn("⚠ toggleQuestionWordVisibility 関数が見つかりません");
        }
      } else {
        // 通常のスロット制御
        toggleSlotElementVisibility(slotKey, elementType, isVisible);
      }
    });
    
    // 🆕 初期状態の色を設定（英文チェックボックスのみ）
    if (checkbox.dataset.type === 'text') {
      const labelElement = checkbox.closest('label');
      if (labelElement) {
        if (checkbox.checked) {
          labelElement.style.backgroundColor = '#4CAF50'; // 緑色
          labelElement.style.color = 'white';
          labelElement.style.padding = '2px 6px';
          labelElement.style.borderRadius = '3px';
        } else {
          labelElement.style.backgroundColor = '#757575'; // グレー色
          labelElement.style.color = 'white';
          labelElement.style.padding = '2px 6px';
          labelElement.style.borderRadius = '3px';
        }
      }
    }
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
      
      // 疑問詞の表示もリセット
      if (typeof window.resetQuestionWordVisibility === 'function') {
        window.resetQuestionWordVisibility();
        console.log("✅ 疑問詞表示もリセットしました");
      }
    });
  }
  
  // 🆕 全英文非表示ボタン（トグル方式に変更）
  const hideAllEnglishButton = document.getElementById('hide-all-english-visibility');
  if (hideAllEnglishButton) {
    // 🆕 最初に強制的に緑色を設定（HTMLの初期値を上書き）
    hideAllEnglishButton.style.backgroundColor = '#4CAF50';
    hideAllEnglishButton.innerHTML = '🙈 英語全OFF';
    console.log("🎨 英語全OFFボタンの初期色を緑色に設定しました");
    
    hideAllEnglishButton.addEventListener('click', function() {
      console.log("🔄 英語表示切替ボタンがクリックされました");
      
      // 現在の状態を確認（最初のスロットの状態で判定）
      const isCurrentlyVisible = visibilityState['s']?.['text'] !== false;
      
      if (isCurrentlyVisible) {
        // 非表示にする
        console.log("🔒 全英文を非表示にします");
        hideAllEnglishText();
        hideAllEnglishButton.innerHTML = '👁️ 英語ON';
        hideAllEnglishButton.style.backgroundColor = '#757575'; // グレー色
      } else {
        // 表示にする
        console.log("👁️ 全英文を表示します");
        showAllEnglishText();
        hideAllEnglishButton.innerHTML = '🙈 英語全OFF';
        hideAllEnglishButton.style.backgroundColor = '#4CAF50'; // 緑色
      }
      
      // UIの英文チェックボックスも同期
      const englishCheckboxes = document.querySelectorAll('.visibility-checkbox[data-type="text"]');
      englishCheckboxes.forEach(cb => {
        cb.checked = !isCurrentlyVisible;
        
        // 🆕 チェックボックスのlabel要素の色も同期
        const labelElement = cb.closest('label');
        if (labelElement) {
          if (!isCurrentlyVisible) {
            // ONにする → 緑色
            labelElement.style.backgroundColor = '#4CAF50';
            labelElement.style.color = 'white';
            labelElement.style.padding = '2px 6px';
            labelElement.style.borderRadius = '3px';
          } else {
            // OFFにする → グレー色
            labelElement.style.backgroundColor = '#757575';
            labelElement.style.color = 'white';
            labelElement.style.padding = '2px 6px';
            labelElement.style.borderRadius = '3px';
          }
        }
      });
    });
    
    // 初期状態のボタンラベルと色を設定
    const initiallyVisible = visibilityState['s']?.['text'] !== false;
    if (!initiallyVisible) {
      hideAllEnglishButton.innerHTML = '👁️ 英語ON';
      hideAllEnglishButton.style.backgroundColor = '#757575';
    } else {
      // 初期状態が表示中の場合も明示的に緑色を設定
      hideAllEnglishButton.innerHTML = '🙈 英語全OFF';
      hideAllEnglishButton.style.backgroundColor = '#4CAF50';
    }
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
  
  // 通常のスロット状態を更新
  ALL_SLOTS.forEach(slotKey => {
    ELEMENT_TYPES.forEach(elementType => {
      const isVisible = visibilityState[slotKey]?.[elementType] ?? true;
      const checkbox = document.querySelector(`.visibility-checkbox[data-slot="${slotKey}"][data-type="${elementType}"]`);
      
      if (checkbox) {
        checkbox.checked = isVisible;
      }
    });
  });
  
  // 疑問詞状態を更新
  ['text', 'auxtext'].forEach(elementType => {
    const isVisible = questionWordVisibilityState[elementType] ?? true;
    const checkbox = document.querySelector(`.visibility-checkbox[data-slot="question-word"][data-type="${elementType}"]`);
    
    if (checkbox) {
      checkbox.checked = isVisible;
      console.log(`🔄 疑問詞チェックボックス更新: ${elementType} = ${isVisible}`);
    } else {
      console.warn(`⚠ 疑問詞チェックボックスが見つかりません: question-word/${elementType}`);
    }
    
    // 実際の表示状態も適用
    toggleQuestionWordVisibility(elementType, isVisible);
  });
  
  console.log("✅ UIの更新が完了しました");
}

// 既存のloadVisibilityState関数を拡張
const originalLoadVisibilityState = loadVisibilityState;
loadVisibilityState = function() {
  originalLoadVisibilityState();
  updateUIFromState();
};

// 疑問詞表示制御機能
let questionWordVisibilityState = {
  text: true,    // 疑問詞テキスト（What等）
  auxtext: true  // 補助テキスト（何？等）
};

// 🔧 疑問詞の表示状態管理
function toggleQuestionWordVisibility(elementType, isVisible) {
  if (!['text', 'auxtext'].includes(elementType)) {
    console.error(`❌ 無効な疑問詞要素タイプ: ${elementType}`);
    return;
  }

  // 状態を更新
  questionWordVisibilityState[elementType] = isVisible;
  
  // 🆕 グローバル変数を確実に同期（insert_test_data_clean.jsとの連携のため）
  window.questionWordVisibilityState = questionWordVisibilityState;
  
  // DOM要素を制御
  const questionWordArea = document.getElementById('display-top-question-word');
  if (questionWordArea) {
    if (elementType === 'text') {
      // 疑問詞テキスト（What等）の表示制御
      const textElements = questionWordArea.querySelectorAll('.question-word-text');
      textElements.forEach(element => {
        element.style.display = isVisible ? 'inline' : 'none';
      });
      console.log(`🔄 疑問詞テキストを${isVisible ? '表示' : '非表示'}にしました`);
    } else if (elementType === 'auxtext') {
      // 補助テキスト（何？等）の表示制御
      const auxtextElements = questionWordArea.querySelectorAll('.question-word-auxtext');
      auxtextElements.forEach(element => {
        element.style.display = isVisible ? 'inline' : 'none';
      });
      console.log(`🔄 疑問詞補助テキストを${isVisible ? '表示' : '非表示'}にしました`);
    }
  }
  
  // localStorage に状態を保存
  saveQuestionWordVisibilityState();
}

// 📁 疑問詞表示状態をstate-manager経由で保存
function saveQuestionWordVisibilityState() {
  try {
    // 🆕 グローバル変数を確実に更新（insert_test_data_clean.jsとの連携のため）
    window.questionWordVisibilityState = questionWordVisibilityState;
    
    // 🎯 **修正：state-manager経由で状態保存**
    if (window.RephraseState) {
      window.RephraseState.setState('visibility.questionWord', questionWordVisibilityState);
      console.log("💾 疑問詞表示状態をstate-manager経由で保存しました:", questionWordVisibilityState);
    } else {
      // フォールバック：直接localStorage保存
      localStorage.setItem('rephrase_question_word_visibility', JSON.stringify(questionWordVisibilityState));
      console.log("💾 疑問詞表示状態を直接localStorageに保存しました（state-manager未利用）");
    }
  } catch (error) {
    console.error("❌ 疑問詞表示状態の保存に失敗:", error);
  }
}

// 📂 疑問詞表示状態をstate-manager経由で読み込み
function loadQuestionWordVisibilityState() {
  try {
    // 🎯 **修正：state-manager経由で状態読み込み**
    if (window.RephraseState) {
      const savedState = window.RephraseState.getState('visibility.questionWord');
      if (savedState && Object.keys(savedState).length > 0) {
        questionWordVisibilityState = { ...questionWordVisibilityState, ...savedState };
        console.log("📂 state-manager経由で疑問詞表示状態を読み込みました:", questionWordVisibilityState);
      } else {
        console.log("📝 state-managerに疑問詞状態がないため、デフォルト値を使用");
      }
    } else {
      // フォールバック：直接localStorage読み込み
      const saved = localStorage.getItem('rephrase_question_word_visibility');
      if (saved) {
        questionWordVisibilityState = { ...questionWordVisibilityState, ...JSON.parse(saved) };
        console.log("📂 直接localStorageから疑問詞表示状態を読み込みました:", questionWordVisibilityState);
      }
    }
    
    // 🆕 グローバル変数を確実に更新（insert_test_data_clean.jsとの連携のため）
    window.questionWordVisibilityState = questionWordVisibilityState;
    console.log("🔄 グローバル疑問詞状態を同期しました:", window.questionWordVisibilityState);
    
  } catch (error) {
    console.error("❌ 疑問詞表示状態の読み込みに失敗:", error);
  }
}

// 🔄 疑問詞表示をリセット
function resetQuestionWordVisibility() {
  questionWordVisibilityState.text = true;
  questionWordVisibilityState.auxtext = true;
  
  // 🆕 グローバル変数を確実に同期（insert_test_data_clean.jsとの連携のため）
  window.questionWordVisibilityState = questionWordVisibilityState;
  
  toggleQuestionWordVisibility('text', true);
  toggleQuestionWordVisibility('auxtext', true);
  
  // UIのチェックボックスも更新
  const textCheckbox = document.querySelector('.visibility-checkbox[data-slot="question-word"][data-type="text"]');
  const auxtextCheckbox = document.querySelector('.visibility-checkbox[data-slot="question-word"][data-type="auxtext"]');
  
  if (textCheckbox) {
    textCheckbox.checked = true;
    console.log("✅ 疑問詞textチェックボックスをリセット");
  } else {
    console.warn("⚠ 疑問詞textチェックボックスが見つかりません");
  }
  if (auxtextCheckbox) {
    auxtextCheckbox.checked = true;
    console.log("✅ 疑問詞auxtextチェックボックスをリセット");
  } else {
    console.warn("⚠ 疑問詞auxtextチェックボックスが見つかりません");
  }
  
  console.log("🔄 疑問詞表示をリセットしました");
}

// 🔒 全英文例文を非表示にする
function hideAllEnglishText() {
  console.log("🔒 全英文例文を非表示にします");
  
  // 全スロットの英文例文（text要素）を非表示にする
  ALL_SLOTS.forEach(slot => {
    toggleSlotElementVisibility(slot, 'text', false);
  });
  
  // 疑問詞の英文例文も非表示にする
  if (typeof window.toggleQuestionWordVisibility === 'function') {
    window.toggleQuestionWordVisibility('text', false);
    console.log("🔒 疑問詞の英文例文も非表示にしました");
  }
  
  // 🆕 全サブスロットの英文状態もlocalStorageに保存
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    let visibilityState = {};
    if (saved) {
      visibilityState = JSON.parse(saved);
    }
    
    // 全親スロットの全サブスロットの英文をfalseに設定
    const PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
    const SUBSLOT_TYPES = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
    
    PARENT_SLOTS.forEach(parentSlot => {
      SUBSLOT_TYPES.forEach(subslotType => {
        const subslotId = `slot-${parentSlot.toLowerCase()}-sub-${subslotType.toLowerCase()}`;
        if (!visibilityState[subslotId]) {
          visibilityState[subslotId] = {};
        }
        visibilityState[subslotId].text = false;
      });
    });
    
    localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(visibilityState));
    console.log("🔒 全サブスロットの英文状態をlocalStorageに保存しました");
    
    // 🆕 画面上の個別ボタンも同期（サブスロット）
    const allSubslotToggleButtons = document.querySelectorAll('.subslot-toggle-btn');
    allSubslotToggleButtons.forEach(button => {
      button.innerHTML = '英語<br>ON';
      button.style.backgroundColor = '#757575';
      button.title = '英語を表示';
    });
    console.log(`🔄 ${allSubslotToggleButtons.length}個のサブスロット個別ボタンを「英語ON」に同期しました`);
    
    // 🆕 画面上の個別ボタンも同期（親スロット）
    const allUpperSlotToggleButtons = document.querySelectorAll('.upper-slot-toggle-btn');
    allUpperSlotToggleButtons.forEach(button => {
      button.innerHTML = '英語<br>ON';
      button.style.backgroundColor = '#757575';
      button.title = '英語を表示';
    });
    console.log(`🔄 ${allUpperSlotToggleButtons.length}個の親スロット個別ボタンを「英語ON」に同期しました`);
    
  } catch (error) {
    console.error("❌ サブスロット英文状態の保存に失敗:", error);
  }
  
  // 状態を永続化
  saveVisibilityState();
  
  console.log("✅ 全英文例文を非表示にしました");
}

// 🆕 全英文表示関数（トグル用）
function showAllEnglishText() {
  console.log("👁️ 全英文例文を表示します");
  console.log(`🔍 DEBUG: 現在のDOM状態チェック - 全サブスロット数: ${document.querySelectorAll('[id*="-sub-"]').length}個`);
  
  // 全スロットの英文例文（text要素）を表示にする
  ALL_SLOTS.forEach(slot => {
    console.log(`🔍 DEBUG: showAllEnglishText - ${slot}スロットの処理開始`);
    toggleSlotElementVisibility(slot, 'text', true);
  });
  
  // 疑問詞の英文例文も表示にする
  if (typeof window.toggleQuestionWordVisibility === 'function') {
    window.toggleQuestionWordVisibility('text', true);
    console.log("👁️ 疑問詞の英文例文も表示にしました");
  }
  
  // 🆕 全サブスロットの英文状態もlocalStorageに保存
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    let visibilityState = {};
    if (saved) {
      visibilityState = JSON.parse(saved);
    }
    
    // 全親スロットの全サブスロットの英文をtrueに設定
    const PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
    const SUBSLOT_TYPES = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
    
    PARENT_SLOTS.forEach(parentSlot => {
      SUBSLOT_TYPES.forEach(subslotType => {
        const subslotId = `slot-${parentSlot.toLowerCase()}-sub-${subslotType.toLowerCase()}`;
        if (!visibilityState[subslotId]) {
          visibilityState[subslotId] = {};
        }
        visibilityState[subslotId].text = true;
      });
    });
    
    localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(visibilityState));
    console.log("👁️ 全サブスロットの英文状態をlocalStorageに保存しました");
    
    // 🆕 画面上の個別ボタンも同期（サブスロット）
    const allSubslotToggleButtons = document.querySelectorAll('.subslot-toggle-btn');
    allSubslotToggleButtons.forEach(button => {
      button.innerHTML = 'EN<br>OFF';
      button.style.backgroundColor = '#4CAF50';
      button.title = '英語を非表示';
    });
    console.log(`🔄 ${allSubslotToggleButtons.length}個のサブスロット個別ボタンを「EN OFF」に同期しました`);
    
    // 🆕 画面上の個別ボタンも同期（親スロット）
    const allUpperSlotToggleButtons = document.querySelectorAll('.upper-slot-toggle-btn');
    allUpperSlotToggleButtons.forEach(button => {
      button.innerHTML = 'EN<br>OFF';
      button.style.backgroundColor = '#4CAF50';
      button.title = '英語を非表示';
    });
    console.log(`🔄 ${allUpperSlotToggleButtons.length}個の親スロット個別ボタンを「EN OFF」に同期しました`);
    
  } catch (error) {
    console.error("❌ サブスロット英文状態の保存に失敗:", error);
  }
  
  // 状態を永続化
  saveVisibilityState();
  
  console.log("✅ 全英文例文を表示にしました");
}

// 🔹 新しい関数もグローバルにエクスポート
window.hideAllEnglishText = hideAllEnglishText;
window.showAllEnglishText = showAllEnglishText;

// 🔹 疑問詞機能をグローバルにエクスポート
window.toggleQuestionWordVisibility = toggleQuestionWordVisibility;
window.resetQuestionWordVisibility = resetQuestionWordVisibility;
window.questionWordVisibilityState = questionWordVisibilityState;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 3要素表示制御システムを初期化中...");
  loadVisibilityState();
  
  // 🆕 疑問詞状態も読み込み
  loadQuestionWordVisibilityState();
  
  // 🆕 グローバル変数を確実に初期化（insert_test_data_clean.jsとの連携のため）
  window.questionWordVisibilityState = questionWordVisibilityState;
  console.log("🔄 グローバル疑問詞状態を初期化しました:", window.questionWordVisibilityState);
  
  // UI設定は少し遅らせて実行（DOM構築完了を確実にするため）
  setTimeout(() => {
    setupVisibilityControlUI();
    
    // 🆕 ボタンラベルを現在の状態に同期
    const hideAllEnglishButton = document.getElementById('hide-all-english-visibility');
    if (hideAllEnglishButton && visibilityState['s']) {
      const isCurrentlyVisible = visibilityState['s']['text'] !== false;
      if (!isCurrentlyVisible) {
        hideAllEnglishButton.innerHTML = '👁️ 英語ON';
        hideAllEnglishButton.style.backgroundColor = '#757575'; // グレー色
      } else {
        hideAllEnglishButton.innerHTML = '🙈 英語全OFF';
        hideAllEnglishButton.style.backgroundColor = '#4CAF50'; // 緑色
      }
      console.log('🔄 ボタンラベルを同期しました:', isCurrentlyVisible ? '表示中' : '非表示');
    }
  }, 100);
});

console.log("✅ visibility_control.js が読み込まれました");
