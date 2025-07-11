// サブスロット用表示・非表示コントロールパネル
// サブスロット展開時に、サブスロットエリアの下部にコントロールパネルを動的追加

// 🎯 サブスロットの表示・非表示制御に使用するスロット一覧
const SUBSLOT_PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
const SUB_ELEMENT_TYPES = ['auxtext', 'text'];

// 🏗️ サブスロット用コントロールパネルを生成
function createSubslotControlPanel(parentSlot) {
  console.log(`🏗️ ${parentSlot}サブスロット用コントロールパネル生成開始`);
  
  // パネル全体のコンテナ
  const panelContainer = document.createElement('div');
  panelContainer.id = `subslot-visibility-panel-${parentSlot}`;
  panelContainer.className = 'subslot-visibility-panel';
  
  // 制御パネルの表示状態を複数の方法で確認
  let isControlPanelsVisible = false;
  
  // 方法1: グローバル変数から取得
  if (window.getControlPanelsVisibility) {
    isControlPanelsVisible = window.getControlPanelsVisibility();
    console.log(`🔍 方法1(グローバル変数): ${isControlPanelsVisible}`);
  }
  
  // 方法2: ボタンのテキストから判定
  const toggleBtn = document.getElementById('toggle-control-panels');
  if (toggleBtn) {
    const btnTextVisible = toggleBtn.textContent.includes('表示中');
    console.log(`🔍 方法2(ボタンテキスト): ${btnTextVisible}`);
    isControlPanelsVisible = isControlPanelsVisible || btnTextVisible;
  }
  
  // 方法3: 上位制御パネルの表示状態から判定
  const upperPanel = document.getElementById('visibility-control-panel-inline');
  if (upperPanel) {
    const upperVisible = upperPanel.style.display !== 'none';
    console.log(`🔍 方法3(上位パネル表示): ${upperVisible}`);
    isControlPanelsVisible = isControlPanelsVisible || upperVisible;
  }
  
  console.log(`🔍 ${parentSlot} サブスロット制御パネル最終判定: ${isControlPanelsVisible}`);
  
  panelContainer.style.cssText = `
    display: ${isControlPanelsVisible ? 'block' : 'none'};
    background: rgba(255, 255, 255, 0.95);
    padding: 8px;
    margin-top: 15px;
    border-radius: 5px;
    border: 1px solid #ddd;
  `;
  
  // パネルタイトル
  const panelTitle = document.createElement('div');
  panelTitle.style.cssText = `
    font-weight: bold;
    font-size: 12px;
    margin-bottom: 8px;
    color: #444;
    text-align: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
  `;
  panelTitle.textContent = `${parentSlot.toUpperCase()} サブスロット表示制御`;
  panelContainer.appendChild(panelTitle);
  
  // サブスロットコントロールのコンテナ
  const controlsContainer = document.createElement('div');
  controlsContainer.style.cssText = `
    display: flex;
    gap: 8px;
    align-items: center;
    font-size: 12px;
    flex-wrap: wrap;
  `;
  
  // 各サブスロット用のコントロールを生成（常に10個のスロット制御を表示）
  const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
  
  desiredOrder.forEach(subslotType => {
    // サブスロット要素の存在に関係なく、常に制御を表示
    const subslotId = `slot-${parentSlot}-sub-${subslotType}`;
    const controlGroup = createSubslotControlGroup(parentSlot, subslotType, subslotId);
    controlsContainer.appendChild(controlGroup);
  });
  
  panelContainer.appendChild(controlsContainer);
  
  // 全表示ボタンを controlsContainer 内に追加（上位パネルと同じ配置）
  const resetButton = document.createElement('button');
  resetButton.style.cssText = `
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 6px 10px;
    font-size: 11px;
    cursor: pointer;
    border-radius: 3px;
    margin-left: 8px;
  `;
  resetButton.textContent = '全表示';
  resetButton.addEventListener('click', () => {
    resetSubslotVisibility(parentSlot);
  });
  controlsContainer.appendChild(resetButton);
  
  // 全英文非表示ボタンを追加
  const hideAllEnglishButton = document.createElement('button');
  hideAllEnglishButton.style.cssText = `
    background-color: #f44336;
    color: white;
    border: none;
    padding: 6px 10px;
    font-size: 11px;
    cursor: pointer;
    border-radius: 3px;
    margin-left: 8px;
  `;
  hideAllEnglishButton.textContent = '全英文非表示';
  hideAllEnglishButton.addEventListener('click', () => {
    hideAllEnglishInSubslots(parentSlot);
  });
  controlsContainer.appendChild(hideAllEnglishButton);
  
  // 制御パネルの表示状態を同期
  if (window.syncSubslotControlPanelVisibility) {
    window.syncSubslotControlPanelVisibility(panelContainer);
  }
  
  console.log(`✅ ${parentSlot}サブスロット用コントロールパネル生成完了`);
  return panelContainer;
}

// 🎛️ 個別サブスロット用コントロールグループを生成
function createSubslotControlGroup(parentSlot, subslotType, subslotId) {
  const controlGroup = document.createElement('div');
  controlGroup.className = 'subslot-control-group';
  
  // サブスロット要素の存在確認
  const subslotElement = document.getElementById(subslotId);
  const hasData = subslotElement && subslotElement.querySelector('.slot-phrase, .slot-text');
  
  controlGroup.style.cssText = `
    padding: 4px;
    border: 1px solid #f0f0f0;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.7);
    ${hasData ? '' : 'opacity: 0.5;'}
  `;
  
  // スロット名表示
  const slotLabel = document.createElement('div');
  slotLabel.style.cssText = `
    font-weight: bold;
    font-size: 11px;
    margin-bottom: 2px;
    color: #444;
    text-align: center;
  `;
  slotLabel.textContent = subslotType.toUpperCase();
  controlGroup.appendChild(slotLabel);
  
  // 各要素タイプのトグルボタン
  const buttonsContainer = document.createElement('div');
  buttonsContainer.style.cssText = `
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: 10px;
  `;
  
  SUB_ELEMENT_TYPES.forEach(elementType => {
    const button = document.createElement('button');
    button.className = 'subslot-toggle-button';
    button.dataset.parentSlot = parentSlot;
    button.dataset.subslotId = subslotId;
    button.dataset.subslotType = subslotType;
    button.dataset.elementType = elementType;
    
    // ボタンスタイル
    const baseStyle = `
      display: flex;
      align-items: center;
      gap: 3px;
      padding: 3px 6px;
      border: 1px solid #ddd;
      border-radius: 3px;
      cursor: pointer;
      font-size: 10px;
      transition: all 0.2s;
    `;
    
    // 初期状態の設定（localStorageから取得）
    const isVisible = getSubslotElementVisibility(subslotId, elementType);
    
    // アイコンとテキストを設定
    const icon = document.createElement('span');
    const text = document.createElement('span');
    
    switch(elementType) {
      case 'text':
        icon.textContent = '📄';
        text.textContent = '英文';
        break;
      case 'auxtext':
        icon.textContent = '📝';
        text.textContent = '補助';
        break;
    }
    
    button.appendChild(icon);
    button.appendChild(text);
    
    // 初期状態のボタンスタイルを適用
    updateToggleButtonStyle(button, isVisible);
    
    // データがない場合は視覚的に区別するが、操作は可能にする
    if (!hasData) {
      button.style.opacity = '0.7';
      button.title = 'データがありません（操作は可能）';
    }
    
    // クリック時のイベント（常に操作可能）
    button.addEventListener('click', function() {
      console.log(`🎛️ トグルボタンクリック:`);
      console.log(`  - subslotId: ${this.dataset.subslotId}`);
      console.log(`  - elementType: ${this.dataset.elementType}`);
      
      // 現在の状態を取得して反転
      const currentVisibility = getSubslotElementVisibility(this.dataset.subslotId, this.dataset.elementType);
      const newVisibility = !currentVisibility;
      
      console.log(`  - 現在の状態: ${currentVisibility} → 新しい状態: ${newVisibility}`);
      
      // 表示状態を切り替え（データがなくても設定を保存）
      toggleSubslotElementVisibility(
        this.dataset.subslotId,
        this.dataset.elementType,
        newVisibility
      );
      
      // ボタンスタイルを更新
      updateToggleButtonStyle(this, newVisibility);
    });
    
    buttonsContainer.appendChild(button);
  });
  
  controlGroup.appendChild(buttonsContainer);
  return controlGroup;
}

// 🎨 トグルボタンのスタイルを更新
function updateToggleButtonStyle(button, isVisible) {
  const baseStyle = `
    display: flex;
    align-items: center;
    gap: 3px;
    padding: 3px 6px;
    border: 1px solid #ddd;
    border-radius: 3px;
    cursor: pointer;
    font-size: 10px;
    transition: all 0.2s;
  `;
  
  if (isVisible) {
    // 表示状態（有効）
    button.style.cssText = baseStyle + `
      background-color: #e8f5e8;
      border-color: #4CAF50;
      color: #2e7d32;
    `;
    button.title = 'クリックして非表示にする';
  } else {
    // 非表示状態（無効）
    button.style.cssText = baseStyle + `
      background-color: #ffebee;
      border-color: #f44336;
      color: #c62828;
      opacity: 0.8;
    `;
    button.title = 'クリックして表示する';
  }
}

// 🔍 サブスロット要素の表示状態を取得
function getSubslotElementVisibility(subslotId, elementType) {
  // まず、localStorageから永続化された状態を取得
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (saved) {
      const state = JSON.parse(saved);
      const key = `${subslotId}_${elementType}`;
      if (state.hasOwnProperty(key)) {
        console.log(`🔍 localStorageから取得: ${key} = ${state[key]}`);
        return state[key];
      }
    }
  } catch (error) {
    console.warn('⚠ localStorage読み取りエラー:', error);
  }
  
  // localStorageにない場合は、DOM要素から現在の状態を取得
  const subslotElement = document.getElementById(subslotId);
  if (subslotElement) {
    const className = `hidden-subslot-${elementType}`;
    const isHidden = subslotElement.classList.contains(className);
    console.log(`🔍 DOM要素から取得: ${subslotId} ${elementType} = ${!isHidden}`);
    return !isHidden;
  }
  
  // デフォルトは表示
  console.log(`🔍 デフォルト値を返す: ${subslotId} ${elementType} = true`);
  return true;
}

// 🎛️ サブスロット要素の表示・非表示制御
function toggleSubslotElementVisibility(subslotId, elementType, isVisible) {
  console.log(`🎛️ サブスロット表示制御: ${subslotId} - ${elementType} = ${isVisible}`);
  
  // DOM要素が存在しない場合も設定を保存（将来のランダマイズに対応）
  const subslotElement = document.getElementById(subslotId);
  if (subslotElement) {
    console.log(`🔍 サブスロット要素が見つかりました: ${subslotId}`);
    console.log(`🔍 現在のクラスリスト: ${Array.from(subslotElement.classList).join(', ')}`);
    
    const className = `hidden-subslot-${elementType}`;
    
    if (isVisible) {
      subslotElement.classList.remove(className);
      console.log(`✅ ${subslotId}の${elementType}を表示しました (removed class: ${className})`);
    } else {
      subslotElement.classList.add(className);
      console.log(`🙈 ${subslotId}の${elementType}を非表示にしました (added class: ${className})`);
    }
    
    console.log(`🔍 更新後のクラスリスト: ${Array.from(subslotElement.classList).join(', ')}`);
  } else {
    console.log(`⚠ サブスロット要素が見つかりません: ${subslotId} - 設定のみ保存します`);
  }
  
  // 🆕 サブスロット表示状態をlocalStorageに保存（DOM要素の有無に関係なく）
  try {
    let subslotVisibilityState = {};
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (saved) {
      subslotVisibilityState = JSON.parse(saved);
    }
    
    const key = `${subslotId}_${elementType}`;
    subslotVisibilityState[key] = isVisible;
    
    localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(subslotVisibilityState));
    console.log(`💾 ${subslotId}の${elementType}状態を保存しました: ${isVisible}`);
  } catch (error) {
    console.error("❌ サブスロット表示状態の保存に失敗:", error);
  }
}

// 🔄 サブスロットの全表示リセット
function resetSubslotVisibility(parentSlot) {
  console.log(`🔄 ${parentSlot}サブスロットの表示を全てリセット`);
  
  const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
  
  desiredOrder.forEach(subslotType => {
    const subslotId = `slot-${parentSlot}-sub-${subslotType}`;
    
    SUB_ELEMENT_TYPES.forEach(elementType => {
      // 表示状態を設定
      toggleSubslotElementVisibility(subslotId, elementType, true);
    });
  });
  
  // サブスロット制御パネルのボタン状態を更新
  const controlPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (controlPanel) {
    const allButtons = controlPanel.querySelectorAll('.subslot-toggle-button');
    allButtons.forEach(button => {
      updateToggleButtonStyle(button, true);
    });
  }
  
  console.log(`✅ ${parentSlot}サブスロットの表示リセット完了`);
}

// 🔒 特定の親スロットのサブスロット内の全英文例文を非表示にする
function hideAllEnglishInSubslots(parentSlot) {
  console.log(`🔒 ${parentSlot}のサブスロット内の全英文例文を非表示にします`);
  
  const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
  
  desiredOrder.forEach(subslotType => {
    const subslotId = `slot-${parentSlot}-sub-${subslotType}`;
    
    // 英文のみを非表示にする（textタイプのみ）
    toggleSubslotElementVisibility(subslotId, 'text', false);
    console.log(`🔒 ${subslotId}の英文を非表示にしました`);
  });
  
  // サブスロット制御パネルのボタン状態を更新
  const controlPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (controlPanel) {
    const textButtons = controlPanel.querySelectorAll('.subslot-toggle-button[data-element-type="text"]');
    textButtons.forEach(button => {
      updateToggleButtonStyle(button, false);
    });
  }
  
  console.log(`✅ ${parentSlot}のサブスロット内の全英文例文を非表示にしました`);
}

// 📋 サブスロット展開時にコントロールパネルを追加
function addSubslotControlPanel(parentSlot) {
  console.log(`📋 ${parentSlot}サブスロット用コントロールパネル追加開始`);
  
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  if (!subslotContainer) {
    console.warn(`⚠ サブスロットコンテナが見つかりません: slot-${parentSlot}-sub`);
    return;
  }
  
  // 既存のコントロールパネルを削除
  const existingPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (existingPanel) {
    existingPanel.remove();
    console.log(`🗑️ 既存のコントロールパネルを削除: ${parentSlot}`);
  }
  
  // 新しいコントロールパネルを作成
  const controlPanel = createSubslotControlPanel(parentSlot);
  
  // サブスロットコンテナに追加
  subslotContainer.appendChild(controlPanel);
  
  console.log(`✅ ${parentSlot}サブスロット用コントロールパネル追加完了`);
}

// 🗑️ サブスロット折りたたみ時にコントロールパネルを削除
function removeSubslotControlPanel(parentSlot) {
  console.log(`🗑️ ${parentSlot}サブスロット用コントロールパネル削除開始`);
  
  const controlPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (controlPanel) {
    controlPanel.remove();
    console.log(`✅ ${parentSlot}サブスロット用コントロールパネル削除完了`);
  } else {
    console.log(`⚠ 削除対象のコントロールパネルが見つかりません: ${parentSlot}`);
  }
}

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  console.log("✅ subslot_visibility_control_fixed.js が読み込まれました");
});

console.log("✅ subslot_visibility_control_fixed.js が読み込まれました");
