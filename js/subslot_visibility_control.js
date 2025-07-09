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
    // 🔄 O1-sub-s-imageのみボタンに変更し、その他はチェックボックスのまま
    const isO1SubSImage = (parentSlot === 'o1' && subslotType === 's' && elementType === 'image');
    
    if (isO1SubSImage) {
      // O1-sub-s-imageのみボタンとして生成
      const button = document.createElement('button');
      button.style.cssText = `
        display: flex;
        align-items: center;
        gap: 2px;
        cursor: pointer;
        border: none;
        background: #f0f0f0;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        color: #333;
        transition: all 0.2s;
        min-width: 50px;
      `;
      
      button.dataset.parentSlot = parentSlot;
      button.dataset.subslotId = subslotId;
      button.dataset.subslotType = subslotType;
      button.dataset.elementType = elementType;
      button.dataset.overlayActive = 'false'; // 初期状態は非表示オーバーレイ無し
      
      // ボタンの初期状態を設定
      button.style.background = '#f0f0f0';
      button.style.color = '#333';
      button.textContent = '🖼️';
      
      // ボタンクリック時のイベント
      button.addEventListener('click', function() {
        const currentOverlayState = this.dataset.overlayActive === 'true';
        const newOverlayState = !currentOverlayState;
        
        console.log(`🎛️ O1-sub-s-imageボタンクリック:`);
        console.log(`  - subslotId: ${this.dataset.subslotId}`);
        console.log(`  - elementType: ${this.dataset.elementType}`);
        console.log(`  - overlayActive: ${currentOverlayState} → ${newOverlayState}`);
        
        // オーバーレイ制御を呼び出し
        toggleSubslotElementOverlay(
          this.dataset.subslotId,
          this.dataset.elementType,
          newOverlayState
        );
        
        // ボタンの状態を更新
        this.dataset.overlayActive = newOverlayState.toString();
      });
      
      checkboxContainer.appendChild(button);
    } else {
      // その他は従来通りチェックボックス
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
    }
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
  
  // 🆕 複数画像コンテナの直接制御（image要素の場合）
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      if (isVisible) {
        multiImageContainer.style.display = 'flex';
        multiImageContainer.style.visibility = 'visible';
        console.log(`✅ ${subslotId}の複数画像コンテナを表示しました`);
      } else {
        multiImageContainer.style.display = 'none';
        multiImageContainer.style.visibility = 'hidden';
        console.log(`🙈 ${subslotId}の複数画像コンテナを非表示にしました`);
      }
    }
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

// 🎛️ オーバーレイ方式でサブスロット要素の表示・非表示制御
function toggleSubslotElementOverlay(subslotId, elementType, isOverlayActive) {
  console.log(`🎛️ オーバーレイ方式サブスロット制御: ${subslotId} - ${elementType} = ${isOverlayActive}`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) {
    console.warn(`⚠ サブスロット要素が見つかりません: ${subslotId}`);
    return;
  }
  
  console.log(`🔍 サブスロット要素が見つかりました: ${subslotId}`);
  
  // オーバーレイ用のクラス名
  const overlayClass = `overlay-hidden-${elementType}`;
  
  if (isOverlayActive) {
    // オーバーレイを適用（要素を隠す）
    subslotElement.classList.add(overlayClass);
    console.log(`🙈 ${subslotId}の${elementType}をオーバーレイで隠しました (added class: ${overlayClass})`);
  } else {
    // オーバーレイを解除（要素を表示）
    subslotElement.classList.remove(overlayClass);
    console.log(`✅ ${subslotId}の${elementType}のオーバーレイを解除しました (removed class: ${overlayClass})`);
  }
  
  // 🆕 複数画像コンテナの直接制御（image要素の場合）
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      if (isOverlayActive) {
        // オーバーレイスタイルを適用
        multiImageContainer.style.position = 'relative';
        
        // 既存のオーバーレイを削除
        const existingOverlay = multiImageContainer.querySelector('.image-overlay');
        if (existingOverlay) {
          existingOverlay.remove();
        }
        
        // 新しいオーバーレイを作成
        const overlay = document.createElement('div');
        overlay.className = 'image-overlay';
        overlay.style.cssText = `
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: #ffffff;
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 10;
          pointer-events: auto;
        `;
        
        // オーバーレイ内容
        const overlayContent = document.createElement('div');
        overlayContent.style.cssText = `
          background: rgba(0, 0, 0, 0.8);
          color: white;
          padding: 8px 12px;
          border-radius: 4px;
          font-size: 12px;
          text-align: center;
        `;
        overlayContent.textContent = '🙈 画像非表示';
        
        overlay.appendChild(overlayContent);
        multiImageContainer.appendChild(overlay);
        
        console.log(`✅ ${subslotId}の複数画像コンテナにオーバーレイを適用しました`);
      } else {
        // オーバーレイを削除
        const existingOverlay = multiImageContainer.querySelector('.image-overlay');
        if (existingOverlay) {
          existingOverlay.remove();
          console.log(`🙈 ${subslotId}の複数画像コンテナのオーバーレイを削除しました`);
        }
      }
    }
  }
  
  console.log(`🔍 更新後のクラスリスト: ${Array.from(subslotElement.classList).join(', ')}`);
  
  // 🆕 オーバーレイ状態をlocalStorageに保存
  try {
    let subslotOverlayState = {};
    const saved = localStorage.getItem('rephrase_subslot_overlay_state');
    if (saved) {
      subslotOverlayState = JSON.parse(saved);
    }
    
    if (!subslotOverlayState[subslotId]) {
      subslotOverlayState[subslotId] = {};
    }
    subslotOverlayState[subslotId][elementType] = isOverlayActive;
    
    localStorage.setItem('rephrase_subslot_overlay_state', JSON.stringify(subslotOverlayState));
    console.log(`💾 ${subslotId}の${elementType}オーバーレイ状態を保存しました: ${isOverlayActive}`);
  } catch (error) {
    console.error("❌ サブスロットオーバーレイ状態の保存に失敗:", error);
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
  
  // 🆕 O1-sub-s-imageボタンのリセット
  const o1SubSButtons = document.querySelectorAll(`[data-parent-slot="${parentSlot}"][data-subslot-type="s"][data-element-type="image"]`);
  o1SubSButtons.forEach(button => {
    // オーバーレイを解除
    toggleSubslotElementOverlay(
      button.dataset.subslotId,
      button.dataset.elementType,
      false
    );
    
    // ボタンの状態を更新
    button.dataset.overlayActive = 'false';
    
    console.log(`✅ ${button.dataset.subslotId}のオーバーレイボタンをリセットしました`);
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
window.toggleSubslotElementOverlay = toggleSubslotElementOverlay;
window.resetSubslotVisibility = resetSubslotVisibility;
window.hookDataInsertionForLabelRestore = hookDataInsertionForLabelRestore;
window.restoreSubslotLabels = restoreSubslotLabels;
window.debugSubslotLabels = debugSubslotLabels;
window.debugAllSubslotLabels = debugAllSubslotLabels;

// 🆕 サブスロット表示状態の復元機能
function applySubslotVisibilityState() {
  console.log("🎨 サブスロット表示状態をDOMに適用中...");
  
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (!saved) {
      console.log("📝 保存されたサブスロット表示状態がありません");
      return;
    }
    
    const subslotVisibilityState = JSON.parse(saved);
    console.log("📂 復元するサブスロット表示状態:", subslotVisibilityState);
    
    Object.keys(subslotVisibilityState).forEach(subslotId => {
      const subslot = subslotVisibilityState[subslotId];
      
      ['image', 'auxtext', 'text'].forEach(elementType => {
        const isVisible = subslot[elementType];
        if (isVisible !== undefined) {
          const subslotElement = document.getElementById(subslotId);
          if (subslotElement) {
            const className = `hidden-subslot-${elementType}`;
            
            if (isVisible) {
              subslotElement.classList.remove(className);
            } else {
              subslotElement.classList.add(className);
            }
            
            // 複数画像コンテナの直接制御（image要素の場合）
            if (elementType === 'image') {
              const multiImageContainer = subslotElement.querySelector('.multi-image-container');
              if (multiImageContainer) {
                if (isVisible) {
                  multiImageContainer.style.display = 'flex';
                  multiImageContainer.style.visibility = 'visible';
                } else {
                  multiImageContainer.style.display = 'none';
                  multiImageContainer.style.visibility = 'hidden';
                }
              }
            }
            
            console.log(`🎨 ${subslotId}の${elementType}表示状態を復元: ${isVisible}`);
          }
        }
      });
    });
    
    console.log("✅ サブスロット表示状態の復元完了");
  } catch (error) {
    console.error("❌ サブスロット表示状態の復元に失敗:", error);
  }
}

// 🆕 サブスロットオーバーレイ状態の復元機能
function applySubslotOverlayState() {
  console.log("🎨 サブスロットオーバーレイ状態をDOMに適用中...");
  
  try {
    const saved = localStorage.getItem('rephrase_subslot_overlay_state');
    if (!saved) {
      console.log("📝 保存されたサブスロットオーバーレイ状態がありません");
      return;
    }
    
    const subslotOverlayState = JSON.parse(saved);
    console.log("📂 復元するサブスロットオーバーレイ状態:", subslotOverlayState);
    
    Object.keys(subslotOverlayState).forEach(subslotId => {
      const subslot = subslotOverlayState[subslotId];
      
      ['image', 'auxtext', 'text'].forEach(elementType => {
        const isOverlayActive = subslot[elementType];
        if (isOverlayActive !== undefined) {
          // オーバーレイ状態を復元
          toggleSubslotElementOverlay(subslotId, elementType, isOverlayActive);
          
          // 対応するボタンの状態も復元
          const button = document.querySelector(`[data-subslot-id="${subslotId}"][data-element-type="${elementType}"]`);
          if (button && button.dataset.overlayActive !== undefined) {
            button.dataset.overlayActive = isOverlayActive.toString();
          }
          
          console.log(`🎨 ${subslotId}の${elementType}オーバーレイ状態を復元: ${isOverlayActive}`);
        }
      });
    });
    
    console.log("✅ サブスロットオーバーレイ状態の復元完了");
  } catch (error) {
    console.error("❌ サブスロットオーバーレイ状態の復元に失敗:", error);
  }
}

// 🆕 ランダマイズ後のボタン機能復元
function restoreOverlayButtonsAfterRandomization() {
  console.log("🔄 ランダマイズ後のオーバーレイボタン機能を復元中...");
  
  // 少し待ってからボタンの状態を確認・復元
  setTimeout(() => {
    const o1SubSButtons = document.querySelectorAll('[data-parent-slot="o1"][data-subslot-type="s"][data-element-type="image"]');
    
    o1SubSButtons.forEach(button => {
      const subslotId = button.dataset.subslotId;
      
      // 保存されたオーバーレイ状態を確認
      try {
        const saved = localStorage.getItem('rephrase_subslot_overlay_state');
        if (saved) {
          const subslotOverlayState = JSON.parse(saved);
          if (subslotOverlayState[subslotId] && subslotOverlayState[subslotId]['image']) {
            // オーバーレイが有効な場合は復元
            toggleSubslotElementOverlay(subslotId, 'image', true);
            button.dataset.overlayActive = 'true';
            console.log(`🎨 ${subslotId}のオーバーレイボタン状態を復元しました`);
          } else {
            button.dataset.overlayActive = 'false';
          }
        }
      } catch (error) {
        console.error("❌ オーバーレイボタン状態の復元に失敗:", error);
        button.dataset.overlayActive = 'false';
      }
    });
    
    console.log("✅ ランダマイズ後のオーバーレイボタン機能復元完了");
  }, 1000);
}

// 🆕 グローバル関数としてエクスポート
window.applySubslotVisibilityState = applySubslotVisibilityState;
window.applySubslotOverlayState = applySubslotOverlayState;
window.restoreOverlayButtonsAfterRandomization = restoreOverlayButtonsAfterRandomization;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  console.log("✅ subslot_toggle.js との連携は自動的に行われます");
  
  // 🏷️ ラベル復元システムを有効化
  console.log("🏷️ サブスロットラベル復元システムを有効化中...");
  hookDataInsertionForLabelRestore();
  
  // 🆕 サブスロット表示状態の初期復元
  setTimeout(() => {
    applySubslotVisibilityState();
    applySubslotOverlayState();
  }, 1000); // DOM構築完了を待って復元
  
  // サブスロットの展開・折りたたみ監視
  if (window.MutationObserver) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' || mutation.type === 'attributes') {
          // サブスロットの表示状態が変化した場合の処理
          restoreSubslotLabels();
          
          // 🆕 ランダマイズ後のオーバーレイ状態復元
          setTimeout(() => {
            applySubslotOverlayState();
            restoreOverlayButtonsAfterRandomization();
          }, 500); // DOM更新完了を待ってから復元
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
