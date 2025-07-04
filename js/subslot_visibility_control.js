// サブスロット用表示・非表示コントロールパネル
// サブスロット展開時に、サブスロットエリアの下部にコントロールパネルを動的追加

// 🎯 サブスロットの表示・非表示制御に使用するスロット一覧
const SUBSLOT_PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
const SUB_ELEMENT_TYPES = ['image', 'subslot-element', 'subslot-text'];

// サブスロット要素タイプのラベル
const SUB_ELEMENT_LABELS = {
  'image': { icon: '🖼️' },
  'subslot-element': { icon: '📄' },
  'subslot-text': { icon: '📝' }
};

// 🏗️ サブスロット用コントロールパネルを生成
function createSubslotControlPanel(parentSlot) {
  console.log(`🏗️ ${parentSlot}サブスロット用コントロールパネル生成開始`);
  
  try {
    // パネル全体のコンテナ
    const panelContainer = document.createElement('div');
    panelContainer.id = `subslot-visibility-panel-${parentSlot}`;
    panelContainer.className = 'subslot-visibility-panel';
    
    // 制御パネルの表示状態を取得
    const isControlPanelsVisible = getControlPanelVisibility();
    console.log(`🔍 ${parentSlot} サブスロット制御パネル表示状態: ${isControlPanelsVisible}`);
    
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
    
    // サブスロット候補を取得（IDベース検索）
    let subslotElements = document.querySelectorAll(`[id^="slot-${parentSlot}-sub-"]`);
    
    // 互換性のため他のパターンもチェック
    if (subslotElements.length === 0) {
      subslotElements = document.querySelectorAll(`#slot-${parentSlot}-sub .subslot-container`);
      console.log(`🔄 ${parentSlot}: ID検索で見つからないため.subslot-containerで検索`);
    }
    
    if (subslotElements.length === 0) {
      subslotElements = document.querySelectorAll(`#slot-${parentSlot}-sub .subslot`);
      console.log(`🔄 ${parentSlot}: .subslot-containerも見つからないため.subslotクラスで検索`);
    }
    
    console.log(`🔍 ${parentSlot}のサブスロット要素: ${subslotElements.length}個`);
    
    // デバッグ用：検索されたサブスロット要素のIDを出力
    if (subslotElements.length > 0) {
      const foundIds = Array.from(subslotElements).map(el => el.id || el.className).join(', ');
      console.log(`📋 検索されたサブスロット要素: ${foundIds}`);
    }
    
    if (subslotElements.length === 0) {
      console.warn(`⚠ ${parentSlot}: サブスロット要素が見つかりません`);
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
    
    // 各サブスロット用のコントロールを生成
    const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
    
    desiredOrder.forEach(subslotType => {
      const subslotElement = document.getElementById(`slot-${parentSlot}-sub-${subslotType}`);
      if (subslotElement) {
        const subslotId = subslotElement.id;
        const controlGroup = createSubslotControlGroup(parentSlot, subslotType, subslotId);
        controlsContainer.appendChild(controlGroup);
      }
    });
    
    panelContainer.appendChild(controlsContainer);
    
    // 全表示ボタンを追加
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
    
    console.log(`✅ ${parentSlot}サブスロット用コントロールパネル生成完了`);
    return panelContainer;
    
  } catch (error) {
    console.error(`❌ ${parentSlot}サブスロット制御パネル生成でエラー:`, error);
    console.error("エラーの詳細:", error.stack);
    return null;
  }
}

// 🎛️ 個別サブスロット用コントロールグループを生成
function createSubslotControlGroup(parentSlot, subslotType, subslotId) {
  const controlGroup = document.createElement('div');
  controlGroup.className = 'subslot-control-group';
  controlGroup.style.cssText = `
    padding: 6px;
    border: 1px solid #f0f0f0;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.7);
    min-width: 60px;
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
  
  // 各要素タイプのチェックボックス
  const checkboxContainer = document.createElement('div');
  checkboxContainer.style.cssText = `
    display: flex;
    flex-direction: row;
    gap: 6px;
    font-size: 12px;
    justify-content: center;
  `;
  
  SUB_ELEMENT_TYPES.forEach(elementType => {
    const label = document.createElement('label');
    label.style.cssText = `
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      cursor: pointer;
      padding: 2px;
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
      console.log(`🎛️ チェックボックス変更: ${this.dataset.subslotId} - ${this.dataset.elementType} = ${this.checked}`);
      
      toggleSubslotElementVisibility(
        this.dataset.subslotId,
        this.dataset.elementType,
        this.checked
      );
    });
    
    const icon = document.createElement('span');
    const config = SUB_ELEMENT_LABELS[elementType] || { icon: '❓' };
    icon.textContent = config.icon;
    icon.style.cssText = `
      font-size: 16px;
      margin-bottom: 2px;
    `;
    
    label.appendChild(icon);
    label.appendChild(checkbox);
    checkboxContainer.appendChild(label);
  });
  
  controlGroup.appendChild(checkboxContainer);
  return controlGroup;
}

// 🎛️ サブスロット要素の表示・非表示制御
function toggleSubslotElementVisibility(subslotId, elementType, isVisible) {
  console.log(`🎛️ サブスロット表示制御: ${subslotId} - ${elementType} = ${isVisible}`);
  
  try {
    const subslotElement = document.getElementById(subslotId);
    if (!subslotElement) {
      console.warn(`⚠ サブスロット要素が見つかりません: ${subslotId}`);
      return;
    }
    
    let targetElement = null;
    
    if (elementType === 'image') {
      // イメージ要素の検索（複数のパターンを試す）
      targetElement = subslotElement.querySelector('.image') ||
                     subslotElement.querySelector('.slot-image') ||
                     subslotElement.querySelector('.subslot-image') ||
                     subslotElement.querySelector('img');
    } else {
      // その他の要素の検索
      targetElement = subslotElement.querySelector(`.${elementType}`);
    }
    
    if (targetElement) {
      targetElement.style.display = isVisible ? 'block' : 'none';
      console.log(`✅ ${subslotId} の ${elementType} を ${isVisible ? '表示' : '非表示'} に設定`);
    } else {
      console.warn(`⚠ ${subslotId} 内に ${elementType} 要素が見つかりません`);
      // デバッグ用：実際に存在する要素を確認
      const childElements = Array.from(subslotElement.children).map(child => {
        return `${child.tagName.toLowerCase()}${child.className ? '.' + child.className : ''}`;
      });
      console.log(`📋 ${subslotId} 内の実際の要素: ${childElements.join(', ')}`);
    }
    
  } catch (error) {
    console.error(`❌ サブスロット表示制御でエラー:`, error);
  }
}

// 🔄 サブスロットの全要素を表示状態にリセット
function resetSubslotVisibility(parentSlot) {
  console.log(`🔄 ${parentSlot} サブスロットの表示状態をリセット`);
  
  try {
    const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
    if (panel) {
      const checkboxes = panel.querySelectorAll('.subslot-visibility-checkbox');
      checkboxes.forEach(checkbox => {
        checkbox.checked = true;
        // チェックボックスの変更イベントを発火
        checkbox.dispatchEvent(new Event('change'));
      });
      console.log(`✅ ${parentSlot} サブスロットの表示状態をリセット完了`);
    }
  } catch (error) {
    console.error(`❌ ${parentSlot} サブスロット表示状態リセットでエラー:`, error);
  }
}

// 📋 サブスロット展開時にコントロールパネルを追加
function addSubslotControlPanel(parentSlot) {
  console.log(`📋 ${parentSlot}サブスロット用コントロールパネル追加開始`);
  
  try {
    const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
    if (!subslotContainer) {
      console.warn(`⚠ サブスロットコンテナが見つかりません: slot-${parentSlot}-sub`);
      return;
    }
    
    console.log(`✅ サブスロットコンテナが見つかりました: ${subslotContainer.id}`);
    
    // 既存のパネルがあれば削除
    const existingPanel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
    if (existingPanel) {
      existingPanel.remove();
      console.log(`🗑️ 既存のコントロールパネルを削除: ${parentSlot}`);
    }
    
    // 新しいパネルを生成
    const panel = createSubslotControlPanel(parentSlot);
    
    if (panel) {
      // コンテナの直後にパネルを挿入
      subslotContainer.parentNode.insertBefore(panel, subslotContainer.nextSibling);
      console.log(`✅ ${parentSlot}サブスロット用コントロールパネル追加完了`);
      
      // 表示状態を同期
      setTimeout(() => {
        if (window.syncAllSubslotControlPanels) {
          window.syncAllSubslotControlPanels();
        }
      }, 50);
      
    } else {
      console.error(`❌ パネルの生成に失敗しました: ${parentSlot}`);
    }
    
  } catch (error) {
    console.error(`❌ ${parentSlot}サブスロット制御パネル追加でエラー:`, error);
    console.error("エラーの詳細:", error.stack);
  }
}

// 🗑️ サブスロット折りたたみ時にコントロールパネルを削除
function removeSubslotControlPanel(parentSlot) {
  console.log(`🗑️ ${parentSlot}サブスロット用コントロールパネル削除開始`);
  
  try {
    const panel = document.getElementById(`subslot-visibility-panel-${parentSlot}`);
    if (panel) {
      panel.remove();
      console.log(`✅ ${parentSlot}サブスロット用コントロールパネル削除完了`);
    }
  } catch (error) {
    console.error(`❌ ${parentSlot}サブスロット制御パネル削除でエラー:`, error);
  }
}

// 🔍 制御パネルの表示状態を取得（複数の方法でチェック）
function getControlPanelVisibility() {
  // 方法1: グローバル変数から取得
  if (window.getControlPanelsVisibility) {
    return window.getControlPanelsVisibility();
  }
  
  // 方法2: ボタンのテキストから判定
  const toggleBtn = document.getElementById('toggle-control-panels');
  if (toggleBtn && toggleBtn.textContent.includes('表示中')) {
    return true;
  }
  
  // 方法3: 上位制御パネルの表示状態から判定
  const upperPanel = document.getElementById('visibility-control-panel-inline');
  if (upperPanel && upperPanel.style.display !== 'none') {
    return true;
  }
  
  return false;
}

// 🔄 全てのサブスロット制御パネルの表示状態を同期
function syncAllSubslotControlPanels() {
  try {
    console.log("🔄 全サブスロット制御パネルの状態同期開始");
    
    const subslotPanels = document.querySelectorAll('.subslot-visibility-panel');
    const isVisible = getControlPanelVisibility();
    
    console.log(`🔍 制御パネル表示状態: ${isVisible}, 対象パネル数: ${subslotPanels.length}`);
    
    subslotPanels.forEach(panel => {
      panel.style.display = isVisible ? 'block' : 'none';
      console.log(`🔄 パネル ${panel.id} を ${isVisible ? '表示' : '非表示'} に設定`);
    });
    
    console.log("✅ 全サブスロット制御パネルの状態同期完了");
  } catch (error) {
    console.error("❌ サブスロット制御パネルの状態同期でエラー:", error);
  }
}

// 🔍 制御パネルの表示状態監視を設定
function setupControlPanelVisibilityWatcher() {
  const toggleButton = document.getElementById('toggle-control-panels');
  if (toggleButton) {
    // MutationObserver でボタンのテキスト変更を監視
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' || mutation.type === 'characterData') {
          console.log("🔍 制御パネルボタンのテキストが変更されました:", toggleButton.textContent);
          syncAllSubslotControlPanels();
        }
      });
    });
    
    observer.observe(toggleButton, {
      childList: true,
      subtree: true,
      characterData: true
    });
    
    console.log("✅ 制御パネル状態監視を設定しました");
  }
}

//  グローバル関数としてエクスポート
window.createSubslotControlPanel = createSubslotControlPanel;
window.addSubslotControlPanel = addSubslotControlPanel;
window.removeSubslotControlPanel = removeSubslotControlPanel;
window.toggleSubslotElementVisibility = toggleSubslotElementVisibility;
window.resetSubslotVisibility = resetSubslotVisibility;
window.syncAllSubslotControlPanels = syncAllSubslotControlPanels;
window.getControlPanelVisibility = getControlPanelVisibility;

// 🔧 デバッグ用テスト関数
window.testSubslotControlPanel = function() {
  console.log("🔧 === サブスロット制御パネル手動テスト開始 ===");
  
  // 1. 制御パネルを表示状態にする
  console.log("🔧 ステップ1: 制御パネルを表示状態にする");
  if (window.toggleAllControlPanels) {
    const currentState = window.getControlPanelsVisibility ? window.getControlPanelsVisibility() : false;
    console.log(`🔍 現在の制御パネル状態: ${currentState}`);
    
    if (!currentState) {
      window.toggleAllControlPanels();
      console.log("✅ 制御パネルを表示状態に変更");
    } else {
      console.log("ℹ️ 制御パネルは既に表示状態です");
    }
  } else {
    console.warn("⚠ toggleAllControlPanels 関数が見つかりません");
  }
  
  // 2. 利用可能なサブスロットを探す
  console.log("🔧 ステップ2: 利用可能なサブスロットを探す");
  const slotIds = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
  let testSlotId = null;
  
  for (const slotId of slotIds) {
    const subslotContainer = document.getElementById(`slot-${slotId}-sub`);
    if (subslotContainer) {
      console.log(`🔍 発見: ${slotId} のサブスロットコンテナが存在`);
      testSlotId = slotId;
      break;
    }
  }
  
  if (!testSlotId) {
    console.warn("⚠ 利用可能なサブスロットコンテナが見つかりません");
    return;
  }
  
  // 3. 手動でサブスロット制御パネルを追加
  console.log(`🔧 ステップ3: ${testSlotId} にサブスロット制御パネルを手動追加`);
  if (window.addSubslotControlPanel) {
    window.addSubslotControlPanel(testSlotId);
    
    // 4. パネルが実際に追加されたかチェック
    setTimeout(() => {
      const panel = document.getElementById(`subslot-visibility-panel-${testSlotId}`);
      console.log(`🔍 パネル追加結果: ${panel ? '成功' : '失敗'}`);
      if (panel) {
        console.log(`✅ パネル詳細: ID=${panel.id}, クラス=${panel.className}, 表示=${panel.style.display}`);
        console.log(`✅ パネル位置: ${panel.parentNode ? panel.parentNode.id : '親なし'}`);
      }
    }, 100);
    
  } else {
    console.warn("⚠ addSubslotControlPanel 関数が見つかりません");
  }
  
  console.log("🔧 === サブスロット制御パネル手動テスト終了 ===");
};

// 🔧 簡単なテスト実行コマンド
window.runQuickTest = function() {
  console.log("🔧 クイックテスト実行");
  setTimeout(() => {
    window.testSubslotControlPanel();
  }, 1000);
};

console.log("🔧 デバッグ用テスト関数を追加しました");
console.log("🔧 実行方法: window.testSubslotControlPanel() または window.runQuickTest()");

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  
  // ★★★ 詳細デバッグ情報を出力 ★★★
  console.log("🔍 === サブスロット制御システム詳細デバッグ ===");
  console.log("🔍 現在のURL:", window.location.href);
  console.log("🔍 subslot_visibility_control.js の読み込み状況:");
  console.log("  - window.addSubslotControlPanel =", typeof window.addSubslotControlPanel);
  console.log("  - window.removeSubslotControlPanel =", typeof window.removeSubslotControlPanel);
  console.log("  - window.toggleSubslotElementVisibility =", typeof window.toggleSubslotElementVisibility);
  console.log("  - window.syncAllSubslotControlPanels =", typeof window.syncAllSubslotControlPanels);
  console.log("  - window.getControlPanelVisibility =", typeof window.getControlPanelVisibility);
  
  // 制御パネル要素の存在確認
  const toggleBtn = document.getElementById('toggle-control-panels');
  const upperPanel = document.getElementById('visibility-control-panel-inline');
  console.log("🔍 制御パネル要素の存在確認:");
  console.log("  - 制御パネルボタン:", toggleBtn ? "存在" : "なし");
  console.log("  - 上位制御パネル:", upperPanel ? "存在" : "なし");
  
  // サブスロットコンテナの存在確認
  const subslotContainers = document.querySelectorAll('[id$="-sub"]');
  console.log("🔍 サブスロットコンテナ:", subslotContainers.length, "個見つかりました");
  subslotContainers.forEach((container, index) => {
    console.log(`  - コンテナ${index + 1}: ${container.id}`);
  });
  
  console.log("🔍 =======================================");
  
  // 初期化状態を確認
  setTimeout(() => {
    console.log("🔍 初期化状態チェック開始");
    console.log("🔍 window.addSubslotControlPanel =", typeof window.addSubslotControlPanel);
    console.log("🔍 window.removeSubslotControlPanel =", typeof window.removeSubslotControlPanel);
    console.log("🔍 window.toggleSubslotElementVisibility =", typeof window.toggleSubslotElementVisibility);
  }, 100);
  
  // 制御パネルの表示状態監視を設定
  setupControlPanelVisibilityWatcher();
  
  console.log("✅ subslot_toggle.js との連携は自動的に行われます");
});

console.log("✅ subslot_visibility_control.js が読み込まれました");
