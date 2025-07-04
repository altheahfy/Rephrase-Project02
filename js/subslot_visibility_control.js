// サブスロット用表示・非表示コントロールパネル
// サブスロット展開時に、サブスロットエリアの下部にコントロールパネルを動的追加

// 🎯 サブスロットの表示・非表示制御に使用するスロット一覧
const SUBSLOT_PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
const SUB_ELEMENT_TYPES = ['image', 'auxtext', 'text'];

// 🏗️ サブスロット用コントロールパネルを生成
function createSubslotControlPanel(parentSlot) {
  console.log(`🏗️ ${parentSlot}サブスロット用コントロールパネル生成開始`);
  
  // パネル全体のコンテナ
  const panelContainer = document.createElement('div');
  panelContainer.id = `subslot-visibility-panel-${parentSlot}`;
  panelContainer.className = 'subslot-visibility-panel';
  
  // 制御パネルの表示状態を複数の方法で確認
  let isControlPanelsVisible = false;
  
  // 方法1: グローバル変数から取得  // 🔧 デバッグ用コンソールメッセージ
  console.log("\n🔧 ===== デバッグ用コマンド =====");
  console.log("📋 サブスロットラベル確認: debugAllSubslotLabels()");
  console.log("🏷️ ラベル復元実行: restoreAllSubslotLabels()");
  console.log("💾 ラベル保護実行: preserveAllSubslotLabels()");
  console.log("✨ ラベル新規作成: createAllSubslotLabels()");
  console.log("🔧 ラベル強制再生成: forceRegenerateAllSubslotLabels()");
  console.log("🧪 データ挿入テスト: simulateDataInsertion()");
  console.log("🔍 特定スロットのラベル確認: debugSubslotLabels('m1')");
  console.log("🔧 ==============================\n");window.getControlPanelsVisibility) {
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
  
  // 各サブスロット用のコントロールを生成（上位スロットパネルと同じ順序）
  const desiredOrder = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
  
  desiredOrder.forEach(subslotType => {
    // 該当するサブスロット要素があるかチェック
    const subslotElement = document.getElementById(`slot-${parentSlot}-sub-${subslotType}`);
    if (subslotElement) {
      const subslotId = subslotElement.id;
      const controlGroup = createSubslotControlGroup(parentSlot, subslotType, subslotId);
      controlsContainer.appendChild(controlGroup);
    }
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
  controlGroup.style.cssText = `
    padding: 4px;
    border: 1px solid #f0f0f0;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.7);
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

// 🏷️ サブスロットラベル復元システム
function hookDataInsertionForLabelRestore() {
  console.log("🏷️ サブスロットラベル復元システムをフックします");
  
  // データ挿入関数のオーバーライド
  const originalSyncDynamic = window.syncDynamicToStatic;
  if (originalSyncDynamic) {
    window.syncDynamicToStatic = function(...args) {
      console.log("🏷️ データ挿入前にラベルを保護します");
      preserveAllSubslotLabels();
      
      // 元の関数を実行
      const result = originalSyncDynamic.apply(this, args);
      
      // データ挿入後にラベルを復元
      setTimeout(() => {
        restoreAllSubslotLabels();
        console.log("🏷️ データ挿入後にラベルを復元しました");
      }, 100);
      
      return result;
    };
  }
  
  // 定期的なラベル復元処理
  setInterval(() => {
    restoreAllSubslotLabels();
  }, 3000); // 3秒ごとに復元チェック
  
  console.log("✅ サブスロットラベル復元システムがフックされました");
}

// 🏷️ 全てのサブスロットラベルを保護
function preserveAllSubslotLabels() {
  console.log("🏷️ 全サブスロットラベルを保護中...");
  
  if (!window.preservedSubslotLabels) {
    window.preservedSubslotLabels = new Map();
  }
  
  // 全てのサブスロットコンテナを検索
  const subslotContainers = document.querySelectorAll('.subslot-container');
  
  subslotContainers.forEach(container => {
    const label = container.querySelector('label');
    if (label) {
      window.preservedSubslotLabels.set(container.id, {
        text: label.textContent,
        style: label.style.cssText,
        className: label.className
      });
      console.log(`💾 保護: ${container.id} → "${label.textContent}"`);
    }
  });
  
  console.log(`💾 ${window.preservedSubslotLabels.size} 個のラベルを保護しました`);
}

// 🏷️ 全てのサブスロットラベルを復元
function restoreAllSubslotLabels() {
  console.log("🏷️ 全サブスロットラベルを復元中...");
  
  if (!window.preservedSubslotLabels) {
    console.log("💾 保護されたラベルがありません - 新規作成します");
    createAllSubslotLabels();
    return;
  }
  
  let restoredCount = 0;
  
  // 保護されたラベルを復元
  window.preservedSubslotLabels.forEach((labelInfo, containerId) => {
    const container = document.getElementById(containerId);
    if (container) {
      let label = container.querySelector('label');
      
      if (!label) {
        // ラベルが存在しない場合は新規作成
        label = document.createElement('label');
        container.insertBefore(label, container.firstChild);
        console.log(`✨ 新規作成: ${containerId} → "${labelInfo.text}"`);
      }
      
      // ラベルの内容を復元
      label.textContent = labelInfo.text;
      if (labelInfo.style) {
        label.style.cssText = labelInfo.style;
      }
      if (labelInfo.className) {
        label.className = labelInfo.className;
      }
      
      // デフォルトスタイルを適用
      if (!label.style.cssText) {
        label.style.cssText = `
          display: block;
          font-weight: bold;
          margin-bottom: 5px;
          color: #333;
          font-size: 14px;
        `;
      }
      
      restoredCount++;
    }
  });
  
  console.log(`✅ ${restoredCount} 個のラベルを復元しました`);
}

// 🏷️ 全てのサブスロットラベルを新規作成（保護データがない場合）
function createAllSubslotLabels() {
  console.log("🏷️ 全サブスロットラベルを新規作成中...");
  
  const subslotContainers = document.querySelectorAll('.subslot-container');
  let createdCount = 0;
  
  subslotContainers.forEach(container => {
    const slotId = container.id;
    
    // IDからサブスロットタイプを抽出 (例: slot-m1-sub-s → S)
    const match = slotId.match(/-sub-([^-]+)$/);
    if (match) {
      const subslotType = match[1];
      
      // 既存のラベルを確認
      let label = container.querySelector('label');
      
      if (!label) {
        // ラベルが存在しない場合は新規作成
        label = document.createElement('label');
        container.insertBefore(label, container.firstChild);
        console.log(`✨ 新規作成: ${slotId} → "${subslotType.toUpperCase()}"`);
      }
      
      // ラベルの内容を設定
      label.textContent = subslotType.toUpperCase();
      label.style.cssText = `
        display: block;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
        font-size: 14px;
      `;
      
      createdCount++;
    }
  });
  
  console.log(`✅ ${createdCount} 個のラベルを新規作成しました`);
}

// 🏷️ サブスロットのラベルを復元する関数（互換性のため残す）
function restoreSubslotLabels() {
  restoreAllSubslotLabels();
}

// 🔍 サブスロットのラベル状態をデバッグするための関数
function debugSubslotLabels(parentSlot) {
  console.log(`🔍 === ${parentSlot} サブスロットラベル状態デバッグ ===`);
  
  // サブスロットコンテナを検索
  const subslotContainer = document.querySelector(`#slot-${parentSlot}-sub`);
  if (!subslotContainer) {
    console.error(`❌ サブスロットコンテナが見つかりません: #slot-${parentSlot}-sub`);
    return;
  }
  
  console.log(`✅ サブスロットコンテナ発見: ${subslotContainer.id}`);
  console.log(`📋 コンテナHTML: ${subslotContainer.outerHTML.substring(0, 200)}...`);
  
  // 全てのサブスロット要素を検索
  const subslotElements = subslotContainer.querySelectorAll('[id*="-sub-"]');
  console.log(`📊 サブスロット要素数: ${subslotElements.length}`);
  
  subslotElements.forEach((element, index) => {
    console.log(`\n🔍 サブスロット要素 ${index + 1}:`);
    console.log(`  ID: ${element.id}`);
    console.log(`  クラス: ${element.className}`);
    
    // ラベル要素を検索
    const labelElements = element.querySelectorAll('label');
    console.log(`  ラベル要素数: ${labelElements.length}`);
    
    labelElements.forEach((label, labelIndex) => {
      console.log(`  ラベル ${labelIndex + 1}:`);
      console.log(`    テキスト: "${label.textContent}"`);
      console.log(`    スタイル: ${label.style.cssText}`);
      console.log(`    表示状態: ${window.getComputedStyle(label).display}`);
    });
    
    // 他の重要な要素も表示
    const phraseElements = element.querySelectorAll('.slot-phrase');
    const textElements = element.querySelectorAll('.slot-text');
    const imageElements = element.querySelectorAll('.slot-image');
    
    console.log(`  フレーズ要素数: ${phraseElements.length}`);
    console.log(`  テキスト要素数: ${textElements.length}`);
    console.log(`  画像要素数: ${imageElements.length}`);
    
    // 要素の全体構造を表示
    console.log(`  HTML構造: ${element.outerHTML.substring(0, 150)}...`);
  });
  
  console.log(`🔍 === ${parentSlot} サブスロットラベル状態デバッグ完了 ===\n`);
}

// 🏷️ 全てのサブスロットのラベル状態を一括デバッグ
function debugAllSubslotLabels() {
  console.log("🔍 === 全サブスロットラベル状態デバッグ開始 ===");
  
  SUBSLOT_PARENT_SLOTS.forEach(parentSlot => {
    debugSubslotLabels(parentSlot);
  });
  
  console.log("🔍 === 全サブスロットラベル状態デバッグ完了 ===");
}

// 🔧 テスト用：サブスロットラベルの強制再生成
function forceRegenerateAllSubslotLabels() {
  console.log("🔧 サブスロットラベルの強制再生成を開始...");
  
  // 既存のラベルを全て削除
  const existingLabels = document.querySelectorAll('.subslot-container label');
  existingLabels.forEach(label => {
    label.remove();
  });
  console.log(`🗑️ ${existingLabels.length} 個の既存ラベルを削除しました`);
  
  // 保護データをクリア
  window.preservedSubslotLabels = new Map();
  
  // 新しいラベルを作成
  createAllSubslotLabels();
  
  console.log("✅ サブスロットラベルの強制再生成が完了しました");
}

// 🔧 テスト用：データ挿入のシミュレーション
function simulateDataInsertion() {
  console.log("🔧 データ挿入のシミュレーションを開始...");
  
  // ラベル保護
  preserveAllSubslotLabels();
  
  // 一部のサブスロットの内容を変更（シミュレーション）
  const testContainers = document.querySelectorAll('.subslot-container');
  testContainers.forEach((container, index) => {
    if (index < 3) { // 最初の3つをテスト
      const phraseElement = container.querySelector('.slot-phrase');
      const textElement = container.querySelector('.slot-text');
      
      if (phraseElement) {
        phraseElement.textContent = `テストフレーズ ${index + 1}`;
      }
      if (textElement) {
        textElement.textContent = `テストテキスト ${index + 1}`;
      }
    }
  });
  
  // ラベル復元
  setTimeout(() => {
    restoreAllSubslotLabels();
    console.log("✅ データ挿入シミュレーションが完了しました");
  }, 100);
}

//  グローバル関数としてエクスポート
window.createSubslotControlPanel = createSubslotControlPanel;
window.addSubslotControlPanel = addSubslotControlPanel;
window.removeSubslotControlPanel = removeSubslotControlPanel;
window.toggleSubslotElementVisibility = toggleSubslotElementVisibility;
window.resetSubslotVisibility = resetSubslotVisibility;
window.hookDataInsertionForLabelRestore = hookDataInsertionForLabelRestore;
window.restoreSubslotLabels = restoreSubslotLabels;
window.restoreAllSubslotLabels = restoreAllSubslotLabels;
window.preserveAllSubslotLabels = preserveAllSubslotLabels;
window.createAllSubslotLabels = createAllSubslotLabels;
window.debugSubslotLabels = debugSubslotLabels;
window.debugAllSubslotLabels = debugAllSubslotLabels;
window.forceRegenerateAllSubslotLabels = forceRegenerateAllSubslotLabels;
window.simulateDataInsertion = simulateDataInsertion;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  console.log("✅ subslot_toggle.js との連携は自動的に行われます");
  
  // 🏷️ 初期ラベル保護・作成
  setTimeout(() => {
    console.log("🏷️ 初期ラベル保護を実行中...");
    preserveAllSubslotLabels();
    createAllSubslotLabels();
    console.log("✅ 初期ラベル保護・作成が完了しました");
  }, 1000);
  
  // 🏷️ ラベル復元システムを有効化
  console.log("🏷️ サブスロットラベル復元システムを有効中...");
  hookDataInsertionForLabelRestore();
  console.log("✅ ラベル復元システムが有効になりました");
  
  // 🔧 デバッグ用コンソールメッセージ
  console.log("\n🔧 ===== デバッグ用コマンド =====");
  console.log("📋 サブスロットラベル確認: debugAllSubslotLabels()");
  console.log("🏷️ ラベル復元実行: restoreAllSubslotLabels()");
  console.log("� ラベル保護実行: preserveAllSubslotLabels()");
  console.log("✨ ラベル新規作成: createAllSubslotLabels()");
  console.log("🔍 特定スロットのラベル確認: debugSubslotLabels('m1')");
  console.log("🔧 ==============================\n");
});

console.log("✅ subslot_visibility_control.js が読み込まれました");
console.log("🔧 デバッグ用コマンドはページ読み込み完了後に利用できます");
