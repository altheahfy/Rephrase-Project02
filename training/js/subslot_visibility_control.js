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
  
  // サブスロット候補を取得（display状態に関係なく検索）
  let subslotElements = document.querySelectorAll(`#slot-${parentSlot}-sub .subslot-container`);
  
  // 互換性のため.subslotクラスもチェック
  if (subslotElements.length === 0) {
    subslotElements = document.querySelectorAll(`#slot-${parentSlot}-sub .subslot`);
    console.log(`🔄 ${parentSlot}: .subslot-containerが見つからないため.subslotクラスで検索`);
  }
  
  // さらに直接IDベースでも検索（より確実）
  if (subslotElements.length === 0) {
    subslotElements = document.querySelectorAll(`[id^="slot-${parentSlot}-sub-"]`);
    console.log(`🔄 ${parentSlot}: IDパターンで検索`);
  }
  
  console.log(`🔍 ${parentSlot}のサブスロット要素: ${subslotElements.length}個`);
  
  // デバッグ: 検出されたサブスロットの詳細を表示
  subslotElements.forEach((subslot, index) => {
    console.log(`  - サブスロット${index + 1}: ${subslot.id} (${subslot.className}) display:${getComputedStyle(subslot).display}`);
  });
  
  // さらに詳細デバッグ：サブスロットコンテナの存在確認
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  if (subslotContainer) {
    console.log(`🔍 ${parentSlot}サブスロットコンテナ詳細:`);
    console.log(`  - ID: ${subslotContainer.id}`);
    console.log(`  - 表示状態: ${getComputedStyle(subslotContainer).display}`);
    console.log(`  - 子要素数: ${subslotContainer.children.length}`);
    Array.from(subslotContainer.children).forEach((child, index) => {
      console.log(`    子要素${index + 1}: ${child.id} (${child.className})`);
    });
  } else {
    console.error(`❌ ${parentSlot}のサブスロットコンテナが見つかりません`);
  }
  
  if (subslotElements.length === 0) {
    console.warn(`⚠ ${parentSlot}: サブスロット要素が見つかりません`);
    console.log(`🔍 デバッグ: #slot-${parentSlot}-sub の内容:`, document.querySelector(`#slot-${parentSlot}-sub`));
    
    const noSubslotsMsg = document.createElement('div');
    noSubslotsMsg.style.cssText = `
      text-align: center;
      color: #666;
      font-style: italic;
      font-size: 12px;
    `;
    noSubslotsMsg.textContent = 'サブスロットがありません';
    panelContainer.appendChild(noSubslotsMsg);
    return panelContainer;
  }
  
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
    ${hasData ? '' : 'opacity: 0.7;'}
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
    
    // 🎯 **修正：データがない場合でも常にアクティブ**
    // データがない場合でも完全にアクティブにする
    button.title = hasData ? '' : 'データはありませんが制御は有効です';
    
    // クリック時のイベント（データの有無に関係なく常に有効）
    button.addEventListener('click', function() {
      
      console.log(`🎛️ トグルボタンクリック:`);
      console.log(`  - subslotId: ${this.dataset.subslotId}`);
      console.log(`  - elementType: ${this.dataset.elementType}`);
      
      // 現在の状態を取得して反転
      const currentVisibility = getSubslotElementVisibility(this.dataset.subslotId, this.dataset.elementType);
      const newVisibility = !currentVisibility;
      
      console.log(`  - 現在の状態: ${currentVisibility} → 新しい状態: ${newVisibility}`);
      
      // 表示状態を切り替え
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
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) {
    console.warn(`⚠ サブスロット要素が見つかりません: ${subslotId}`);
    return;
  }
  
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
  
  // 実際に要素が非表示になっているかを確認
  const targetElements = {
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      const computedStyle = window.getComputedStyle(el);
      console.log(`📊 ${elementType}要素${index + 1}: display=${computedStyle.display}`);
    });
  } else {
    console.warn(`⚠ ${elementType}要素が見つかりません in ${subslotId}`);
  }
  
  // 🆕 サブスロット表示状態をlocalStorageに保存
  try {
    let subslotVisibilityState = {};
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (saved) {
      subslotVisibilityState = JSON.parse(saved);
    }
    
    if (!subslotVisibilityState[subslotId]) {
      subslotVisibilityState[subslotId] = {};
    }
    subslotVisibilityState[subslotId][elementType] = isVisible;
    
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
  
  // 🎯 **修正：rephrase_subslot_visibility_stateシステムを使用**
  const saved = localStorage.getItem('rephrase_subslot_visibility_state');
  let visibilityState = {};
  if (saved) {
    try {
      visibilityState = JSON.parse(saved);
    } catch (e) {
      console.error('Error parsing rephrase_subslot_visibility_state:', e);
    }
  }
  
  desiredOrder.forEach(subslotType => {
    const subslotId = `slot-${parentSlot}-sub-${subslotType}`;
    const elementId = `slot-${parentSlot.toLowerCase()}-sub-${subslotType.toLowerCase()}`;
    const subslotElement = document.getElementById(subslotId);
    
    // 🎯 **修正：全10種類のサブスロットをtrueに設定**
    if (!visibilityState[elementId]) {
      visibilityState[elementId] = {};
    }
    visibilityState[elementId].text = true;
    console.log(`🔄 rephrase_subslot_visibility_state設定: ${elementId}.text = true`);
    
    if (subslotElement) {
      // 英文を表示にする（textタイプのみ）
      toggleSubslotElementVisibility(subslotId, 'text', true);
      console.log(`🔄 ${subslotId}の英文を表示にしました`);
    } else {
      console.log(`🔄 ${subslotId}は表示されていませんが、localStorage設定済み`);
    }
  });
  
  // localStorageに保存
  localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(visibilityState));
  
  // 該当するトグルボタンを全て表示状態に
  const toggleButtons = document.querySelectorAll(`[data-parent-slot="${parentSlot}"].subslot-toggle-button`);
  toggleButtons.forEach(button => {
    // ボタンスタイルを更新
    updateToggleButtonStyle(button, true);
  });
  
  console.log(`✅ ${parentSlot}サブスロットの表示リセット完了`);
}

// 📋 サブスロット展開時にコントロールパネルを追加
function addSubslotControlPanel(parentSlot) {
  console.log(`📋 ${parentSlot}サブスロット用コントロールパネル追加開始`);
  
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  if (!subslotContainer) {
    console.warn(`⚠ サブスロットコンテナが見つかりません: slot-${parentSlot}-sub`);
    return;
  }
  
  console.log(`✅ サブスロットコンテナが見つかりました: ${subslotContainer.id}`);
  console.log(`🔍 コンテナの表示状態: display=${getComputedStyle(subslotContainer).display}`);
  
  // 既存のパネルがあれば削除
  const existingPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (existingPanel) {
    existingPanel.remove();
    console.log(`🗑️ 既存のコントロールパネルを削除: ${parentSlot}`);
  }
  
  // サブスロットが完全に展開されるまで少し待つ
  setTimeout(() => {
    console.log(`🏗️ 新しいコントロールパネルを生成中... (遅延後)`);
    const panel = createSubslotControlPanel(parentSlot);
    
    if (panel) {
      // コンテナの直後にパネルを挿入
      subslotContainer.parentNode.insertBefore(panel, subslotContainer.nextSibling);
      console.log(`✅ ${parentSlot}サブスロット用コントロールパネル追加完了`);
      console.log(`🔍 追加されたパネル: ${panel.id}, クラス: ${panel.className}`);
      
      // 表示状態を同期
      setTimeout(() => {
        if (window.syncAllSubslotControlPanels) {
          window.syncAllSubslotControlPanels();
        }
      }, 50);
      
    } else {
      console.error(`❌ パネルの生成に失敗しました: ${parentSlot}`);
    }
  }, 200); // 200ms遅延
}

// 🗑️ サブスロット折りたたみ時にコントロールパネルを削除
function removeSubslotControlPanel(parentSlot) {
  console.log(`🗑️ ${parentSlot}サブスロット用コントロールパネル削除開始`);
  
  const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (panel) {
    panel.remove();
    console.log(`✅ ${parentSlot}サブスロット用コントロールパネル削除完了`);
  }
}

// 🔒 特定の親スロットのサブスロット内の全英文例文を非表示にする
function hideAllEnglishInSubslots(parentSlot) {
  console.log(`🔒 ${parentSlot}のサブスロット内の全英文例文を非表示にします`);
  
  const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
  
  // 🎯 **修正：rephrase_subslot_visibility_stateシステムを使用**
  const saved = localStorage.getItem('rephrase_subslot_visibility_state');
  let visibilityState = {};
  if (saved) {
    try {
      visibilityState = JSON.parse(saved);
    } catch (e) {
      console.error('Error parsing rephrase_subslot_visibility_state:', e);
    }
  }
  
  desiredOrder.forEach(subslotType => {
    const subslotId = `slot-${parentSlot}-sub-${subslotType}`;
    const elementId = `slot-${parentSlot.toLowerCase()}-sub-${subslotType.toLowerCase()}`;
    const subslotElement = document.getElementById(subslotId);
    
    // 🎯 **修正：全10種類のサブスロットをfalseに設定**
    if (!visibilityState[elementId]) {
      visibilityState[elementId] = {};
    }
    visibilityState[elementId].text = false;
    console.log(`🔒 rephrase_subslot_visibility_state設定: ${elementId}.text = false`);
    
    if (subslotElement) {
      // 英文のみを非表示にする（textタイプのみ）
      toggleSubslotElementVisibility(subslotId, 'text', false);
      console.log(`🔒 ${subslotId}の英文を非表示にしました`);
    } else {
      console.log(`🔒 ${subslotId}は表示されていませんが、localStorage設定済み`);
    }
  });
  
  // localStorageに保存
  localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(visibilityState));
  
  // サブスロット制御パネルのボタン状態を更新
  const controlPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
  if (controlPanel) {
    const textButtons = controlPanel.querySelectorAll('.subslot-toggle-button[data-element-type="text"]');
    textButtons.forEach(button => {
      // データの有無に関係なく常にボタンを更新
      updateToggleButtonStyle(button, false);
    });
  }
  
  console.log(`✅ ${parentSlot}のサブスロット内の全英文例文を非表示にしました`);
}

console.log("✅ subslot_visibility_control.js が読み込まれました");
