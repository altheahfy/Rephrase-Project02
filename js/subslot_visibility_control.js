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

// 🆕 サブスロット表示状態の復元機能
function applySubslotVisibilityState() {
  console.log("🎨 サブスロット表示状態をDOMに適用中...");
  
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (!saved) {
      console.log("📝 保存されたサブスロット表示状態がありません - デフォルト状態を維持");
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
              console.log(`🎨 ${subslotId}の${elementType}を表示: hiddenクラス削除`);
            } else {
              subslotElement.classList.add(className);
              console.log(`🎨 ${subslotId}の${elementType}を非表示: hiddenクラス追加`);
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
            
            console.log(`🎨 ${subslotId}の${elementType}表示状態を復元: ${isVisible} (クラス: ${subslotElement.className})`);
          } else {
            console.warn(`⚠️ ${subslotId}の要素が見つかりません - 復元をスキップ`);
          }
        }
      });
    });
    
    console.log("✅ サブスロット表示状態の復元完了");
  } catch (error) {
    console.error("❌ サブスロット表示状態の復元に失敗:", error);
  }
}

// 🆕 グローバル関数としてエクスポート
window.applySubslotVisibilityState = applySubslotVisibilityState;
window.diagnoseAndFixSubslotVisibility = diagnoseAndFixSubslotVisibility;
window.resetSubslotVisibilityState = resetSubslotVisibilityState;

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

// 🔧 ページ読み込み完了後にO1, C1, C2の診断を実行（軽量版）
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    console.log("🔧 ページ初期化: O1, C1, C2の軽量診断を実行中...");
    
    // 軽量版の診断: 保存された設定がない場合のみ実行
    try {
      const saved = localStorage.getItem('rephrase_subslot_visibility_state');
      if (!saved) {
        console.log("📝 保存された設定がないため、軽量診断を実行");
        if (typeof window.diagnoseAndFixSubslotVisibility === 'function') {
          window.diagnoseAndFixSubslotVisibility();
          console.log("🔧 ページ初期化: O1, C1, C2の軽量診断を実行しました");
        }
      } else {
        console.log("📝 保存された設定があるため、軽量診断をスキップ");
      }
    } catch (error) {
      console.error("❌ 軽量診断の実行に失敗:", error);
    }
  }, 2000); // 2秒後に実行（他の初期化処理の完了を待つ）
});

// 🔧 デバッグ用: コンソールから実行可能な修正関数
window.fixO1C1C2 = function() {
  console.log("🔧 O1, C1, C2の修正を手動実行中...");
  
  if (typeof window.diagnoseAndFixSubslotVisibility === 'function') {
    window.diagnoseAndFixSubslotVisibility();
  }
  
  // 追加で非表示設定を再適用
  if (typeof window.applySubslotVisibilityState === 'function') {
    window.applySubslotVisibilityState();
  }
  
  console.log("✅ O1, C1, C2の修正完了");
};

// 🧹 デバッグ用: サブスロット表示状態の完全リセット
window.resetAllSubslots = function() {
  console.log("🧹 サブスロット表示状態を完全リセット中...");
  
  if (typeof window.resetSubslotVisibilityState === 'function') {
    window.resetSubslotVisibilityState();
  }
  
  // ページをリロード
  setTimeout(() => {
    location.reload();
  }, 1000);
};

console.log("✅ subslot_visibility_control.js が読み込まれました");

// 🔧 O1, C1, C2の表示問題診断・修正機能（改良版）
function diagnoseAndFixSubslotVisibility() {
  console.log("🔧 O1, C1, C2のサブスロット表示問題を診断中...");
  
  // 保存された設定を読み込み
  let savedSettings = {};
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (saved) {
      savedSettings = JSON.parse(saved);
      console.log("📂 保存されたサブスロット設定を読み込み:", savedSettings);
    }
  } catch (error) {
    console.error("❌ 保存された設定の読み込みに失敗:", error);
  }
  
  const problematicSlots = ['o1', 'c1', 'c2'];
  
  problematicSlots.forEach(slotId => {
    console.log(`🔍 ${slotId.toUpperCase()}スロットの診断開始`);
    
    // サブスロット要素を検索
    const subslotElements = document.querySelectorAll(`[id^="slot-${slotId}-"]`);
    console.log(`  - 検出されたサブスロット要素: ${subslotElements.length}個`);
    
    subslotElements.forEach(subslot => {
      if (subslot.id.includes('-sub-')) {
        console.log(`  - サブスロット: ${subslot.id}`);
        
        // 保存された設定を確認
        const savedSubslotSettings = savedSettings[subslot.id];
        
        // テキスト要素の表示状態を確認
        const textElement = subslot.querySelector('.slot-text');
        if (textElement) {
          const computedStyle = getComputedStyle(textElement);
          const isHidden = subslot.classList.contains('hidden-subslot-text');
          const hasContent = textElement.textContent.trim() !== '';
          
          console.log(`    - テキスト要素: display=${computedStyle.display}, visibility=${computedStyle.visibility}`);
          console.log(`    - hiddenクラス: ${isHidden}`);
          console.log(`    - 内容: "${textElement.textContent}"`);
          console.log(`    - 保存された設定: ${savedSubslotSettings ? JSON.stringify(savedSubslotSettings) : 'なし'}`);
          
          // 修正ロジック: 保存された設定を優先
          if (savedSubslotSettings && savedSubslotSettings.text !== undefined) {
            // 保存された設定がある場合は、それに従う
            const shouldBeVisible = savedSubslotSettings.text;
            
            if (shouldBeVisible && isHidden) {
              console.log(`    - 🔧 保存された設定に従って表示: ${subslot.id}`);
              subslot.classList.remove('hidden-subslot-text');
            } else if (!shouldBeVisible && !isHidden) {
              console.log(`    - 🔧 保存された設定に従って非表示: ${subslot.id}`);
              subslot.classList.add('hidden-subslot-text');
            }
          } else if (isHidden && hasContent) {
            // 保存された設定がない場合のみ、不正な非表示状態を修正
            console.log(`    - 🔧 保存された設定がないため、不正な非表示クラスを削除: ${subslot.id}`);
            subslot.classList.remove('hidden-subslot-text');
          }
        }
        
        // 画像要素の表示状態を確認
        const imageContainer = subslot.querySelector('.multi-image-container');
        if (imageContainer) {
          const isImageHidden = subslot.classList.contains('hidden-subslot-image');
          console.log(`    - 画像要素: display=${imageContainer.style.display}, hidden=${isImageHidden}`);
          
          // 保存された設定を確認
          if (savedSubslotSettings && savedSubslotSettings.image !== undefined) {
            const shouldBeVisible = savedSubslotSettings.image;
            
            if (shouldBeVisible && isImageHidden) {
              console.log(`    - 🔧 保存された設定に従って画像表示: ${subslot.id}`);
              subslot.classList.remove('hidden-subslot-image');
              imageContainer.style.display = 'flex';
              imageContainer.style.visibility = 'visible';
            } else if (!shouldBeVisible && !isImageHidden) {
              console.log(`    - 🔧 保存された設定に従って画像非表示: ${subslot.id}`);
              subslot.classList.add('hidden-subslot-image');
              imageContainer.style.display = 'none';
              imageContainer.style.visibility = 'hidden';
            }
          } else if (isImageHidden && imageContainer.children.length > 0) {
            // 保存された設定がない場合のみ、不正な非表示状態を修正
            console.log(`    - 🔧 保存された設定がないため、画像の非表示クラスを削除: ${subslot.id}`);
            subslot.classList.remove('hidden-subslot-image');
            imageContainer.style.display = 'flex';
            imageContainer.style.visibility = 'visible';
          }
        }
        
        // aux要素の表示状態を確認
        const auxElement = subslot.querySelector('.slot-phrase');
        if (auxElement) {
          const isAuxHidden = subslot.classList.contains('hidden-subslot-auxtext');
          const hasAuxContent = auxElement.textContent.trim() !== '';
          
          console.log(`    - aux要素: hidden=${isAuxHidden}, 内容: "${auxElement.textContent}"`);
          
          // 保存された設定を確認
          if (savedSubslotSettings && savedSubslotSettings.auxtext !== undefined) {
            const shouldBeVisible = savedSubslotSettings.auxtext;
            
            if (shouldBeVisible && isAuxHidden) {
              console.log(`    - 🔧 保存された設定に従ってaux表示: ${subslot.id}`);
              subslot.classList.remove('hidden-subslot-auxtext');
            } else if (!shouldBeVisible && !isAuxHidden) {
              console.log(`    - 🔧 保存された設定に従ってaux非表示: ${subslot.id}`);
              subslot.classList.add('hidden-subslot-auxtext');
            }
          } else if (isAuxHidden && hasAuxContent) {
            // 保存された設定がない場合のみ、不正な非表示状態を修正
            console.log(`    - 🔧 保存された設定がないため、auxの非表示クラスを削除: ${subslot.id}`);
            subslot.classList.remove('hidden-subslot-auxtext');
          }
        }
      }
    });
  });
  
  console.log("✅ O1, C1, C2のサブスロット表示問題診断完了");
}

// 🧹 サブスロット表示状態のリセット機能
function resetSubslotVisibilityState() {
  console.log("🧹 サブスロット表示状態をリセット中...");
  
  // localStorageをクリア
  localStorage.removeItem('rephrase_subslot_visibility_state');
  
  // 全てのサブスロットから非表示クラスを削除
  const allSubslots = document.querySelectorAll('[id^="slot-"][id*="-sub-"]');
  allSubslots.forEach(subslot => {
    subslot.classList.remove('hidden-subslot-text', 'hidden-subslot-image', 'hidden-subslot-auxtext');
    
    // 画像コンテナの表示を復元
    const imageContainer = subslot.querySelector('.multi-image-container');
    if (imageContainer) {
      imageContainer.style.display = 'flex';
      imageContainer.style.visibility = 'visible';
    }
    
    console.log(`🧹 ${subslot.id}の表示状態をリセット`);
  });
  
  console.log("✅ サブスロット表示状態のリセット完了");
}
