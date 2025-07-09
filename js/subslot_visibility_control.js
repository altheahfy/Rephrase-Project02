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
    // ボタン式の制御に変更
    const controlButton = document.createElement('button');
    controlButton.className = 'subslot-visibility-button';
    controlButton.dataset.parentSlot = parentSlot;
    controlButton.dataset.subslotId = subslotId;
    controlButton.dataset.subslotType = subslotType;
    controlButton.dataset.elementType = elementType;
    
    // 🆕 LocalStorageからオーバーレイ状態を読み込んでボタンの初期状態を設定
    let hasOverlay = false; // デフォルトはオーバーレイなし（表示状態）
    try {
      const saved = localStorage.getItem('rephrase_subslot_overlay_state');
      if (saved) {
        const overlayState = JSON.parse(saved);
        if (overlayState[subslotId] && overlayState[subslotId][elementType] !== undefined) {
          hasOverlay = overlayState[subslotId][elementType];
          console.log(`📂 ${subslotId}の${elementType}オーバーレイ状態を読み込み: ${hasOverlay}`);
        }
      }
    } catch (error) {
      console.error("❌ オーバーレイ状態の読み込みに失敗:", error);
    }
    
    // ボタンのスタイルと表示を設定
    function updateButtonAppearance() {
      const isVisible = !hasOverlay;
      controlButton.style.cssText = `
        padding: 3px 6px;
        border: 1px solid ${isVisible ? '#4CAF50' : '#f44336'};
        background-color: ${isVisible ? '#e8f5e8' : '#fde8e8'};
        color: ${isVisible ? '#2e7d32' : '#c62828'};
        border-radius: 3px;
        cursor: pointer;
        font-size: 10px;
        margin: 1px;
        transition: all 0.2s ease;
      `;
      
      const icon = {
        'image': '🖼️',
        'text': '📄',
        'auxtext': '📝'
      };
      
      controlButton.textContent = `${icon[elementType]}${isVisible ? '' : '❌'}`;
      controlButton.title = `${elementType}: ${isVisible ? '表示中（クリックで非表示）' : '非表示中（クリックで表示）'}`;
    }
    
    updateButtonAppearance();
    
    // ボタンクリック時のイベント
    controlButton.addEventListener('click', function() {
      const currentlyVisible = !hasOverlay;
      console.log(`🎛️ ボタンクリック: ${subslotId} - ${elementType} を ${currentlyVisible ? '非表示' : '表示'} に切り替え`);
      
      hasOverlay = currentlyVisible; // 状態を反転
      updateButtonAppearance();
      
      toggleSubslotElementVisibility(
        this.dataset.subslotId,
        this.dataset.elementType,
        !hasOverlay // isVisibleはオーバーレイの逆
      );
    });
    
    checkboxContainer.appendChild(controlButton);
  });
  
  controlGroup.appendChild(checkboxContainer);
  return controlGroup;
}

// � オーバーレイによるサブスロット要素の表示・非表示制御
function toggleSubslotElementVisibility(subslotId, elementType, isVisible) {
  console.log(`� オーバーレイ制御: ${subslotId} - ${elementType} = ${isVisible ? '表示' : '非表示'}`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) {
    console.warn(`⚠ サブスロット要素が見つかりません: ${subslotId}`);
    return;
  }
  
  // 対象要素を特定
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image, .multi-image-container'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (!elements || elements.length === 0) {
    console.warn(`⚠ ${elementType}要素が見つかりません in ${subslotId}`);
    return;
  }
  
  elements.forEach((element, index) => {
    const overlayId = `overlay-${subslotId}-${elementType}-${index}`;
    let overlay = document.getElementById(overlayId);
    
    if (isVisible) {
      // 表示：オーバーレイを削除
      if (overlay) {
        overlay.remove();
        console.log(`✅ ${element.className}のオーバーレイを削除しました`);
      }
    } else {
      // 非表示：オーバーレイを作成・配置
      if (!overlay) {
        // 親要素をrelativeに設定
        const parent = element.parentElement;
        if (getComputedStyle(parent).position === 'static') {
          parent.style.position = 'relative';
        }
        
        // オーバーレイ要素を作成
        overlay = document.createElement('div');
        overlay.id = overlayId;
        overlay.className = 'subslot-element-overlay';
        overlay.style.cssText = `
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(128, 128, 128, 0.8);
          backdrop-filter: blur(3px);
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 12px;
          font-weight: bold;
          text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
          border-radius: 4px;
          cursor: pointer;
          user-select: none;
        `;
        
        // オーバーレイテキスト
        const overlayText = {
          'image': '🖼️ 画像を非表示',
          'text': '📄 テキストを非表示', 
          'auxtext': '📝 補助テキストを非表示'
        };
        overlay.textContent = overlayText[elementType] || '非表示';
        
        // オーバーレイクリックで表示に戻す機能
        overlay.addEventListener('click', (e) => {
          e.stopPropagation();
          console.log(`🖱️ オーバーレイクリック: ${overlayId} を表示に戻します`);
          toggleSubslotElementVisibility(subslotId, elementType, true);
          
          // 制御パネルのチェックボックスも更新
          const checkbox = document.querySelector(`[data-subslot-id="${subslotId}"][data-element-type="${elementType}"]`);
          if (checkbox) {
            checkbox.checked = true;
          }
        });
        
        // 要素の直前に挿入（相対位置を保つため）
        element.parentNode.insertBefore(overlay, element);
        console.log(`🎭 ${element.className}にオーバーレイを配置しました: ${overlayId}`);
      }
    }
  });
  
  // 🆕 オーバーレイ状態をlocalStorageに保存
  try {
    let overlayState = {};
    const saved = localStorage.getItem('rephrase_subslot_overlay_state');
    if (saved) {
      overlayState = JSON.parse(saved);
    }
    
    if (!overlayState[subslotId]) {
      overlayState[subslotId] = {};
    }
    overlayState[subslotId][elementType] = !isVisible; // オーバーレイの存在状態を保存
    
    localStorage.setItem('rephrase_subslot_overlay_state', JSON.stringify(overlayState));
    console.log(`💾 ${subslotId}の${elementType}オーバーレイ状態を保存: ${!isVisible}`);
  } catch (error) {
    console.error("❌ オーバーレイ状態の保存に失敗:", error);
  }
}

// 🔄 サブスロットの全オーバーレイ削除（全表示）
function resetSubslotVisibility(parentSlot) {
  console.log(`🔄 ${parentSlot}サブスロットの全オーバーレイを削除して全表示にリセット`);
  
  // 該当するボタンを全て表示状態に
  const buttons = document.querySelectorAll(`[data-parent-slot="${parentSlot}"].subslot-visibility-button`);
  buttons.forEach(button => {
    // オーバーレイを削除（表示状態にする）
    toggleSubslotElementVisibility(
      button.dataset.subslotId,
      button.dataset.elementType,
      true // 表示
    );
    
    // ボタンの見た目も更新
    button.click(); // これによりupdateButtonAppearance()が呼ばれる
  });
  
  console.log(`✅ ${parentSlot}サブスロットの全表示リセット完了`);
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
  
  // 既存のrestoreSubslotLabels関数をラップ
  const originalRestore = window.restoreSubslotLabels;
  
  // 定期的なラベル復元処理
  setInterval(() => {
    restoreSubslotLabels();
  }, 5000); // 5秒ごとに復元チェック
  
  // MutationObserverでサブスロットの変更を監視
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' || mutation.type === 'characterData') {
        // サブスロットの変更を検出した場合、ラベルを復元
        const target = mutation.target;
        if (target.closest && target.closest('.subslot-container')) {
          setTimeout(() => {
            restoreSubslotLabels();
          }, 100);
        }
      }
    });
  });
  
  // 全てのサブスロットコンテナを監視
  const subslotContainers = document.querySelectorAll('.subslot-container');
  subslotContainers.forEach(container => {
    observer.observe(container, {
      childList: true,
      subtree: true,
      characterData: true
    });
  });
  
  console.log("✅ サブスロットラベル復元システムがフックされました");
}

// 🏷️ サブスロットのラベルを復元する関数（デバウンス機能付き）
let labelRestoreTimeout = null;
let isLabelRestoring = false;

function restoreSubslotLabels() {
  // 既に処理中の場合は重複実行を防ぐ
  if (isLabelRestoring) {
    console.log("⏭️ ラベル復元処理が既に実行中のため、重複実行をスキップします");
    return;
  }
  
  // 既存のタイマーをクリア
  if (labelRestoreTimeout) {
    clearTimeout(labelRestoreTimeout);
    console.log("⏰ 既存のラベル復元タイマーをクリアしました");
  }
  
  // デバウンス：短時間の連続呼び出しを防ぐ
  labelRestoreTimeout = setTimeout(() => {
    isLabelRestoring = true;
    console.log("🏷️ サブスロットラベル復元処理を開始");
    
    // 全てのサブスロットコンテナを検索
    const subslotContainers = document.querySelectorAll('.subslot-container');
    
    subslotContainers.forEach(container => {
      // サブスロット要素を検索
      const subslots = container.querySelectorAll('[id*="-sub-"]');
      
      subslots.forEach(subslot => {
        const slotId = subslot.id;
        
        // IDからサブスロットタイプを抽出 (例: slot-m1-sub-s → s)
        const match = slotId.match(/-sub-([^-]+)$/);
        if (match) {
          const subslotType = match[1];
          
          // 既存のラベルを確認
          let existingLabel = subslot.querySelector('label');
          
          if (!existingLabel) {
            // ラベルが存在しない場合は作成
            existingLabel = document.createElement('label');
            existingLabel.textContent = subslotType.toUpperCase();
            existingLabel.style.cssText = `
              display: block;
              font-weight: bold;
              margin-bottom: 5px;
              color: #333;
              font-size: 14px;
            `;
            
            // サブスロットの最初の要素として挿入
            subslot.insertBefore(existingLabel, subslot.firstChild);
            
            console.log(`✅ サブスロット ${slotId} にラベル "${subslotType.toUpperCase()}" を復元しました`);
          } else {
            // ラベルが存在する場合は内容を確認・修正
            if (existingLabel.textContent !== subslotType.toUpperCase()) {
              existingLabel.textContent = subslotType.toUpperCase();
              console.log(`🔄 サブスロット ${slotId} のラベルを修正しました`);
            }
          }
        }
      });
    });
    
    console.log("✅ サブスロットラベル復元処理が完了しました");
    isLabelRestoring = false;
    
    // 🖼 ラベル復元完了後に画像処理を実行（一度だけ）
    if (typeof window.processAllImagesWithCoordination === 'function') {
      setTimeout(() => {
        window.processAllImagesWithCoordination();
      }, 50);
    }
  }, 200); // 200ms のデバウンス
}

// 🔍 サブスロットのラベル状態をデバッグするための関数
function debugSubslotLabels(parentSlot) {
  console.log(`🔍 === ${parentSlot} サブスロットラベル状態デバッグ ===`);
  
  const subslotContainer = document.getElementById(`slot-${parentSlot}-sub`);
  if (!subslotContainer) {
    console.log(`❌ サブスロットコンテナが見つかりません: slot-${parentSlot}-sub`);
    return;
  }
  
  const subslots = subslotContainer.querySelectorAll('.subslot-container, .subslot');
  console.log(`🔍 ${parentSlot} サブスロット総数: ${subslots.length}`);
  
  subslots.forEach((subslot, index) => {
    const labelElement = subslot.querySelector('label');
    const labelText = labelElement ? labelElement.textContent.trim() : 'ラベルなし';
    console.log(`  ${index + 1}. ${subslot.id}: ラベル="${labelText}"`);
  });
  
  console.log(`🔍 === ${parentSlot} サブスロットラベル状態デバッグ完了 ===`);
}

// 🔍 全サブスロットのラベル状態をデバッグ
function debugAllSubslotLabels() {
  console.log("🔍 === 全サブスロットラベル状態デバッグ開始 ===");
  
  SUBSLOT_PARENT_SLOTS.forEach(parentSlot => {
    debugSubslotLabels(parentSlot);
  });
  
  console.log("🔍 === 全サブスロットラベル状態デバッグ完了 ===");
}

// 🔹 グローバル関数としてエクスポート
window.createSubslotControlPanel = createSubslotControlPanel;
window.addSubslotControlPanel = addSubslotControlPanel;
window.removeSubslotControlPanel = removeSubslotControlPanel;
window.toggleSubslotElementVisibility = toggleSubslotElementVisibility;
window.resetSubslotVisibility = resetSubslotVisibility;
window.hookDataInsertionForLabelRestore = hookDataInsertionForLabelRestore;
window.restoreSubslotLabels = restoreSubslotLabels;
window.debugSubslotLabels = debugSubslotLabels;
window.debugAllSubslotLabels = debugAllSubslotLabels;

// 🆕 オーバーレイ状態の復元機能
function applySubslotOverlayState() {
  console.log("� サブスロットオーバーレイ状態をDOMに適用中...");
  
  try {
    const saved = localStorage.getItem('rephrase_subslot_overlay_state');
    if (!saved) {
      console.log("📝 保存されたオーバーレイ状態がありません");
      return;
    }
    
    const overlayState = JSON.parse(saved);
    console.log("📂 復元するオーバーレイ状態:", overlayState);
    
    Object.keys(overlayState).forEach(subslotId => {
      const elementStates = overlayState[subslotId];
      
      ['image', 'auxtext', 'text'].forEach(elementType => {
        const hasOverlay = elementStates[elementType];
        if (hasOverlay !== undefined && hasOverlay) {
          // オーバーレイがある場合は非表示にする
          toggleSubslotElementVisibility(subslotId, elementType, false);
          console.log(`� ${subslotId}の${elementType}にオーバーレイを復元`);
        }
      });
    });
    
    console.log("✅ オーバーレイ状態の復元完了");
  } catch (error) {
    console.error("❌ オーバーレイ状態の復元に失敗:", error);
  }
}

// 🆕 グローバル関数としてエクスポート
window.applySubslotOverlayState = applySubslotOverlayState;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  console.log("✅ subslot_toggle.js との連携は自動的に行われます");
  
  // 🏷️ ラベル復元システムを有効化
  console.log("🏷️ サブスロットラベル復元システムを有効化中...");
  hookDataInsertionForLabelRestore();
  
  // 🆕 オーバーレイ状態の初期復元
  setTimeout(() => {
    applySubslotOverlayState();
  }, 1000); // DOM構築完了を待って復元
  
  // サブスロットの展開・折りたたみ監視
  if (window.MutationObserver) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' || mutation.type === 'attributes') {
          // サブスロットの表示状態が変化した場合の処理
          restoreSubslotLabels();
          
          // 🆕 サブスロット再生成時に非表示設定を復元
          // 一時的に無効化 - 無限ループの可能性があるため
          /*
          setTimeout(() => {
            applySubslotVisibilityState();
          }, 100); // DOM変更後少し待ってから復元
          */
        }
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['style', 'class']
    });
  }
  
  console.log("✅ サブスロット表示制御システム初期化完了");
});

console.log("✅ subslot_visibility_control.js が読み込まれました");
