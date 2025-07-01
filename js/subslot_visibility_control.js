// サブスロット用表示・非表示コントロールパネル
// サブスロット展開時に、サブスロットエリアの下部にコントロールパネルを動的追加

// 🎯 サブスロットの表示・非表示制御に使用するスロット一覧
const SUBSLOT_PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
const SUB_ELEMENT_TYPES = ['image', 'text', 'auxtext'];

// 🏗️ サブスロット用コントロールパネルを生成
function createSubslotControlPanel(parentSlot) {
  console.log(`🏗️ ${parentSlot}サブスロット用コントロールパネル生成開始`);
  
  // パネル全体のコンテナ
  const panelContainer = document.createElement('div');
  panelContainer.id = `subslot-visibility-panel-${parentSlot}`;
  panelContainer.className = 'subslot-visibility-panel';
  panelContainer.style.cssText = `
    background: rgba(240, 248, 255, 0.95);
    padding: 12px;
    margin-top: 16px;
    border-radius: 8px;
    border: 2px solid #4a90e2;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  `;
  
  // パネルタイトル
  const panelTitle = document.createElement('div');
  panelTitle.style.cssText = `
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 8px;
    color: #2c5aa0;
    text-align: center;
    border-bottom: 1px solid #4a90e2;
    padding-bottom: 4px;
  `;
  panelTitle.textContent = `${parentSlot.toUpperCase()} サブスロット表示制御`;
  panelContainer.appendChild(panelTitle);
  
  // サブスロット候補を取得
  const subslotElements = document.querySelectorAll(`#slot-${parentSlot}-sub .subslot`);
  console.log(`🔍 ${parentSlot}のサブスロット要素: ${subslotElements.length}個`);
  
  // デバッグ: 検出されたサブスロットの詳細を表示
  subslotElements.forEach((subslot, index) => {
    console.log(`  - サブスロット${index + 1}: ${subslot.id} (${subslot.className})`);
  });
  
  if (subslotElements.length === 0) {
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
    align-items: flex-start;
    font-size: 12px;
    flex-wrap: wrap;
    justify-content: center;
  `;
  
  // 各サブスロット用のコントロールを生成
  subslotElements.forEach(subslotElement => {
    const subslotId = subslotElement.id;
    const slotMatch = subslotId.match(/slot-(.+)-sub-(.+)$/);
    
    if (slotMatch) {
      const subslotType = slotMatch[2]; // 例: m1, s, aux, v, etc.
      const controlGroup = createSubslotControlGroup(parentSlot, subslotType, subslotId);
      controlsContainer.appendChild(controlGroup);
    }
  });
  
  panelContainer.appendChild(controlsContainer);
  
  // 全表示ボタン
  const resetButton = document.createElement('button');
  resetButton.style.cssText = `
    margin-top: 8px;
    padding: 4px 8px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 11px;
    cursor: pointer;
    display: block;
    margin-left: auto;
    margin-right: auto;
  `;
  resetButton.textContent = '全表示';
  resetButton.addEventListener('click', () => {
    resetSubslotVisibility(parentSlot);
  });
  panelContainer.appendChild(resetButton);
  
  console.log(`✅ ${parentSlot}サブスロット用コントロールパネル生成完了`);
  return panelContainer;
}

// 🎛️ 個別サブスロット用コントロールグループを生成
function createSubslotControlGroup(parentSlot, subslotType, subslotId) {
  const controlGroup = document.createElement('div');
  controlGroup.className = 'subslot-control-group';
  controlGroup.style.cssText = `
    padding: 6px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.7);
    min-width: 60px;
  `;
  
  // スロット名表示
  const slotLabel = document.createElement('div');
  slotLabel.style.cssText = `
    font-weight: bold;
    font-size: 11px;
    margin-bottom: 4px;
    color: #333;
    text-align: center;
  `;
  slotLabel.textContent = subslotType.toUpperCase();
  controlGroup.appendChild(slotLabel);
  
  // 各要素タイプのチェックボックス
  const checkboxContainer = document.createElement('div');
  checkboxContainer.style.cssText = `
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: 10px;
  `;
  
  SUB_ELEMENT_TYPES.forEach(elementType => {
    const label = document.createElement('label');
    label.style.cssText = `
      display: flex;
      align-items: center;
      gap: 2px;
      cursor: pointer;
    `;
    
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'subslot-visibility-checkbox';
    checkbox.dataset.parentSlot = parentSlot;
    checkbox.dataset.subslotId = subslotId;
    checkbox.dataset.subslotType = subslotType;
    checkbox.dataset.elementType = elementType;
    checkbox.checked = true; // 初期状態は表示
    
    // チェックボックス変更時のイベント
    checkbox.addEventListener('change', function() {
      console.log(`🎛️ チェックボックス変更イベント:`);
      console.log(`  - subslotId: ${this.dataset.subslotId}`);
      console.log(`  - elementType: ${this.dataset.elementType}`);
      console.log(`  - checked: ${this.checked}`);
      
      toggleSubslotElementVisibility(
        this.dataset.subslotId,
        this.dataset.elementType,
        this.checked
      );
    });
    
    const icon = document.createElement('span');
    switch(elementType) {
      case 'image':
        icon.textContent = '🖼️';
        break;
      case 'text':
        icon.textContent = '📄';
        break;
      case 'auxtext':
        icon.textContent = '📝';
        break;
    }
    
    label.appendChild(checkbox);
    label.appendChild(icon);
    checkboxContainer.appendChild(label);
  });
  
  controlGroup.appendChild(checkboxContainer);
  return controlGroup;
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
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
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
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      const computedStyle = window.getComputedStyle(el);
      console.log(`� ${elementType}要素${index + 1}: display=${computedStyle.display}`);
    });
  } else {
    console.warn(`⚠ ${elementType}要素が見つかりません in ${subslotId}`);
  }
}
}

// 🔄 サブスロットの全表示リセット
function resetSubslotVisibility(parentSlot) {
  console.log(`🔄 ${parentSlot}サブスロットの表示を全てリセット`);
  
  // 該当するチェックボックスを全てチェック状態に
  const checkboxes = document.querySelectorAll(`[data-parent-slot="${parentSlot}"].subslot-visibility-checkbox`);
  checkboxes.forEach(checkbox => {
    checkbox.checked = true;
    toggleSubslotElementVisibility(
      checkbox.dataset.subslotId,
      checkbox.dataset.elementType,
      true
    );
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
  const existingPanel = subslotContainer.querySelector('.subslot-visibility-panel');
  if (existingPanel) {
    existingPanel.remove();
    console.log(`🗑️ 既存のコントロールパネルを削除: ${parentSlot}`);
  }
  
  // 新しいパネルを生成して追加
  console.log(`🏗️ 新しいコントロールパネルを生成中...`);
  const panel = createSubslotControlPanel(parentSlot);
  
  if (panel) {
    subslotContainer.appendChild(panel);
    console.log(`✅ ${parentSlot}サブスロット用コントロールパネル追加完了`);
    console.log(`🔍 追加されたパネル: ${panel.id}, クラス: ${panel.className}`);
  } else {
    console.error(`❌ パネルの生成に失敗しました: ${parentSlot}`);
  }
}

// 🗑️ サブスロット折りたたみ時にコントロールパネルを削除
function removeSubslotControlPanel(parentSlot) {
  console.log(`🗑️ ${parentSlot}サブスロット用コントロールパネル削除開始`);
  
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  if (!subslotContainer) {
    console.warn(`⚠ サブスロットコンテナが見つかりません: slot-${parentSlot}-sub`);
    return;
  }
  
  const panel = subslotContainer.querySelector('.subslot-visibility-panel');
  if (panel) {
    panel.remove();
    console.log(`✅ ${parentSlot}サブスロット用コントロールパネル削除完了`);
  }
}

//  グローバル関数としてエクスポート
window.createSubslotControlPanel = createSubslotControlPanel;
window.addSubslotControlPanel = addSubslotControlPanel;
window.removeSubslotControlPanel = removeSubslotControlPanel;
window.toggleSubslotElementVisibility = toggleSubslotElementVisibility;
window.resetSubslotVisibility = resetSubslotVisibility;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  console.log("✅ subslot_toggle.js との連携は自動的に行われます");
});

console.log("✅ subslot_visibility_control.js が読み込まれました");
