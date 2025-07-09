// サブスロット用表示・非表示コントロールパネル
// サブスロット展開時に、サブスロットエリアの下部にコントロールパネルを動的追加

// 🎯 サブスロットの表示・非表示制御に使用するスロット一覧
const SUBSLOT_PARENT_SLOTS = ['m1', 's', 'o1', 'o2', 'm2', 'c1', 'c2', 'm3'];
const SUB_ELEMENT_TYPES = ['image', 'auxtext', 'text'];

// 🔧 サブスロットの表示状態を管理するオブジェクト
let subslotVisibilityState = {};

// 🔧 サブスロットの表示状態を初期化
function initializeSubslotVisibilityState() {
  // 既存の状態を読み込み、なければ初期化
  loadSubslotVisibilityState();
  console.log("🔄 サブスロット表示状態を初期化しました:", subslotVisibilityState);
}

// 📁 サブスロット表示状態をlocalStorageに保存
function saveSubslotVisibilityState() {
  try {
    localStorage.setItem('rephrase_subslot_visibility_state', JSON.stringify(subslotVisibilityState));
    console.log("💾 サブスロット表示状態を保存しました");
  } catch (error) {
    console.error("❌ サブスロット表示状態の保存に失敗:", error);
  }
}

// 📂 サブスロット表示状態をlocalStorageから読み込み
function loadSubslotVisibilityState() {
  try {
    const saved = localStorage.getItem('rephrase_subslot_visibility_state');
    if (saved) {
      subslotVisibilityState = JSON.parse(saved);
      console.log("📂 保存されたサブスロット表示状態を読み込みました:", subslotVisibilityState);
    } else {
      console.log("📝 保存されたサブスロット表示状態がないため、初期化します");
      subslotVisibilityState = {};
    }
  } catch (error) {
    console.error("❌ サブスロット表示状態の読み込みに失敗:", error);
    subslotVisibilityState = {};
  }
}

// 🎨 サブスロットの表示状態をDOMに適用
function applySubslotVisibilityState() {
  console.log("🎨 サブスロット表示状態をDOMに適用開始");
  
  Object.keys(subslotVisibilityState).forEach(subslotId => {
    const subslotElement = document.getElementById(subslotId);
    if (!subslotElement) {
      console.warn(`⚠️ サブスロット要素が見つかりません: ${subslotId}`);
      return;
    }
    
    const elementState = subslotVisibilityState[subslotId];
    Object.keys(elementState).forEach(elementType => {
      const isVisible = elementState[elementType];
      const className = `hidden-subslot-${elementType}`;
      
      // DOM要素のクラス制御
      if (isVisible) {
        subslotElement.classList.remove(className);
      } else {
        subslotElement.classList.add(className);
      }
      
      // 🆕 直接的なスタイル制御も併用
      const targetElements = {
        'image': subslotElement.querySelectorAll('.slot-image'),
        'text': subslotElement.querySelectorAll('.slot-phrase'),
        'auxtext': subslotElement.querySelectorAll('.slot-text')
      };
      
      const elements = targetElements[elementType];
      if (elements && elements.length > 0) {
        if (isVisible) {
          // 表示時は完全解除機能を使用
          forceShowByAllMeans(subslotId, elementType);
          
          // 追加で基本的な解除も実行
          elements.forEach((el) => {
            el.style.display = '';
            el.style.visibility = '';
          });
        } else {
          // 非表示時は通常の制御 + 強制非表示
          elements.forEach((el) => {
            el.style.display = 'none';
            el.style.visibility = 'hidden';
          });
          
          // 追加で強制非表示も実行
          forceHideByAllMeans(subslotId, elementType);
        }
      }
      
      // 複数画像コンテナの直接制御
      if (elementType === 'image') {
        const multiImageContainer = subslotElement.querySelector('.multi-image-container');
        if (multiImageContainer) {
          if (isVisible) {
            // 表示時は完全解除
            multiImageContainer.style.removeProperty('display');
            multiImageContainer.style.removeProperty('visibility');
            multiImageContainer.style.removeProperty('opacity');
            multiImageContainer.style.removeProperty('height');
            multiImageContainer.style.removeProperty('width');
            multiImageContainer.style.removeProperty('overflow');
            multiImageContainer.style.removeProperty('position');
            multiImageContainer.style.removeProperty('left');
            multiImageContainer.removeAttribute('data-force-hidden');
            multiImageContainer.removeAttribute('aria-hidden');
            multiImageContainer.hidden = false;
            multiImageContainer.style.display = 'flex';
            multiImageContainer.style.visibility = 'visible';
          } else {
            // 非表示時は強制非表示
            multiImageContainer.style.display = 'none';
            multiImageContainer.style.visibility = 'hidden';
            multiImageContainer.style.setProperty('opacity', '0', 'important');
            multiImageContainer.setAttribute('data-force-hidden', 'true');
            multiImageContainer.hidden = true;
          }
        }
      }
      
      // 🆕 対応するチェックボックスの状態も同期
      const checkbox = document.querySelector(`[data-subslot-id="${subslotId}"][data-element-type="${elementType}"]`);
      if (checkbox) {
        checkbox.checked = isVisible;
        console.log(`🔄 チェックボックス同期: ${subslotId}-${elementType} = ${isVisible}`);
      }
    });
  });
  
  console.log("🎨 サブスロット表示状態のDOM適用完了");
}

// 📊 サブスロットの表示状態を取得
function getSubslotVisibilityState() {
  return { ...subslotVisibilityState };
}

// 🔄 個別ランダマイズ後の状態復元を強化
function restoreSubslotVisibilityAfterIndividualRandomization(targetSlot) {
  console.log(`🔄 個別ランダマイズ後の状態復元開始: ${targetSlot}`);
  
  // 0. 上位スロットの非表示状態を即座に回避
  neutralizeUpperSlotVisibility(targetSlot);
  
  // 1. 即座適用（DOM再構築直後に即実行）
  applySubslotVisibilityStateImmediately(targetSlot);
  
  // 2. 少し遅延してから通常の適用も実行（安全策）
  setTimeout(() => {
    applySubslotVisibilityState();
    console.log(`🔄 ${targetSlot} 通常適用完了`);
  }, 50);
  
  // 3. さらに遅延してサブスロットコントロールパネルを再構築
  setTimeout(() => {
    const subslotContainer = document.getElementById(`slot-${targetSlot}-sub`);
    if (subslotContainer && getComputedStyle(subslotContainer).display !== 'none') {
      // パネルを再作成
      removeSubslotControlPanel(targetSlot);
      setTimeout(() => {
        addSubslotControlPanel(targetSlot);
        console.log(`🎛️ ${targetSlot}サブスロットコントロールパネル再構築完了`);
      }, 100);
    }
  }, 150);
  
  // 4. 最終確認（最大3回まで再試行）
  let retryCount = 0;
  const maxRetries = 3;
  
  const finalCheck = () => {
    retryCount++;
    console.log(`🔄 最終確認試行 ${retryCount}/${maxRetries}`);
    
    let needsRetry = false;
    Object.keys(subslotVisibilityState).forEach(subslotId => {
      if (!subslotId.includes(`slot-${targetSlot}-sub-`)) return;
      
      const subslotElement = document.getElementById(subslotId);
      if (subslotElement) {
        const elementState = subslotVisibilityState[subslotId];
        Object.keys(elementState).forEach(elementType => {
          const isVisible = elementState[elementType];
          
          if (!isVisible) {
            // 非表示であるべき要素が表示されていないかチェック
            const targetElements = {
              'image': subslotElement.querySelectorAll('.slot-image'),
              'text': subslotElement.querySelectorAll('.slot-phrase'),
              'auxtext': subslotElement.querySelectorAll('.slot-text')
            };
            
            const elements = targetElements[elementType];
            if (elements && elements.length > 0) {
              elements.forEach(el => {
                const computedStyle = window.getComputedStyle(el);
                if (computedStyle.display !== 'none' || computedStyle.visibility !== 'hidden') {
                  needsRetry = true;
                  console.log(`🔄 要素が非表示されていません: ${subslotId}-${elementType}`);
                  // 再度強制非表示を適用
                  forceHideByAllMeans(subslotId, elementType);
                }
              });
            }
          }
        });
      }
    });
    
    if (needsRetry && retryCount < maxRetries) {
      setTimeout(finalCheck, 200);
    } else {
      console.log(`✅ 状態復元完了: ${targetSlot} (試行回数: ${retryCount})`);
    }
  };
  
  // 最終確認を開始
  setTimeout(finalCheck, 300);
}

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
  
  // 🆕 パネル作成後に保存された状態を適用
  setTimeout(() => {
    applySubslotVisibilityState();
    console.log(`🎨 ${parentSlot}サブスロットに保存された表示状態を適用しました`);
  }, 100);
  
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
    
    // 🆕 保存された状態から初期値を設定
    const savedState = subslotVisibilityState[subslotId]?.[elementType];
    checkbox.checked = savedState !== undefined ? savedState : true; // デフォルトは表示
    
    console.log(`🔍 チェックボックス初期化: ${subslotId}-${elementType} = ${checkbox.checked} (保存状態: ${savedState})`);
    
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
  
  // 🆕 状態をメモリに保存
  if (!subslotVisibilityState[subslotId]) {
    subslotVisibilityState[subslotId] = {};
  }
  subslotVisibilityState[subslotId][elementType] = isVisible;
  
  console.log(`🔍 サブスロット要素が見つかりました: ${subslotId}`);
  console.log(`🔍 現在のクラスリスト: ${Array.from(subslotElement.classList).join(', ')}`);
  
  const className = `hidden-subslot-${elementType}`;
  
  // CSSクラスによる制御
  if (isVisible) {
    subslotElement.classList.remove(className);
    console.log(`✅ ${subslotId}の${elementType}を表示しました (removed class: ${className})`);
  } else {
    subslotElement.classList.add(className);
    console.log(`🙈 ${subslotId}の${elementType}を非表示にしました (added class: ${className})`);
  }
  
  // 🆕 直接的なスタイル制御も併用（より確実にするため）
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      if (isVisible) {
        el.style.display = '';
        el.style.visibility = '';
        console.log(`✅ ${elementType}要素${index + 1}を直接表示: ${el.tagName}.${el.className}`);
      } else {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        console.log(`🙈 ${elementType}要素${index + 1}を直接非表示: ${el.tagName}.${el.className}`);
      }
    });
  }
  
  // 🆕 強制制御も併用（他のスクリプトによる上書きを防ぐ）
  if (isVisible) {
    // 表示時は完全解除機能を使用
    forceShowByAllMeans(subslotId, elementType);
    
    // 追加で基本的な解除も実行
    forceShowSubslotElements(subslotId, elementType);
    
    console.log(`✅ ${subslotId} - ${elementType} 完全表示処理完了`);
  } else {
    // 診断実行
    console.log(`🔬 非表示処理前の診断:`);
    diagnoseSubslotElementVisibility(subslotId, elementType);
    
    // 通常の強制非表示
    forceHideSubslotElements(subslotId, elementType);
    
    // それでもダメなら全手段による強制非表示
    setTimeout(() => {
      diagnoseSubslotElementVisibility(subslotId, elementType);
      forceHideByAllMeans(subslotId, elementType);
      
      // 最終確認
      setTimeout(() => {
        console.log(`🔬 最終確認診断:`);
        diagnoseSubslotElementVisibility(subslotId, elementType);
      }, 100);
    }, 50);
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
  
  // 🆕 状態をlocalStorageに永続化
  saveSubslotVisibilityState();
  
  // 実際に要素が非表示になっているかを確認
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      const computedStyle = window.getComputedStyle(el);
      console.log(`📊 ${elementType}要素${index + 1}: display=${computedStyle.display}, visibility=${computedStyle.visibility}`);
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

// 🔷 強制非表示制御機能追加
// 🔒 サブスロット要素の強制非表示制御（他のスクリプトによる上書きを防ぐ）
function forceHideSubslotElements(subslotId, elementType) {
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) return;
  
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el) => {
      // 複数の方法で強制非表示
      el.style.setProperty('display', 'none', 'important');
      el.style.setProperty('visibility', 'hidden', 'important');
      el.style.setProperty('opacity', '0', 'important');
      el.setAttribute('data-force-hidden', 'true');
      console.log(`🔒 強制非表示適用: ${el.tagName}.${el.className}`);
    });
  }
  
  // 複数画像コンテナも同様に制御
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      multiImageContainer.style.setProperty('display', 'none', 'important');
      multiImageContainer.style.setProperty('visibility', 'hidden', 'important');
      multiImageContainer.style.setProperty('opacity', '0', 'important');
      multiImageContainer.setAttribute('data-force-hidden', 'true');
      console.log(`🔒 複数画像コンテナ強制非表示適用`);
    }
  }
}

// 🔓 サブスロット要素の強制非表示解除（完全版）
function forceShowSubslotElements(subslotId, elementType) {
  console.log(`🔓 完全解除開始: ${subslotId} - ${elementType}`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) return;
  
  // 1. CSSクラス削除
  const className = `hidden-subslot-${elementType}`;
  subslotElement.classList.remove(className);
  
  // 2. 親要素からもクラス削除
  const parentContainer = subslotElement.closest('.subslot-container, .subslot');
  if (parentContainer) {
    parentContainer.classList.remove(className);
  }
  
  // 3. 対象要素への直接制御解除
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      // 全てのforceHideByAllMeansで適用したスタイルを削除
      el.style.removeProperty('display');
      el.style.removeProperty('visibility');
      el.style.removeProperty('opacity');
      el.style.removeProperty('height');
      el.style.removeProperty('width');
      el.style.removeProperty('overflow');
      el.style.removeProperty('position');
      el.style.removeProperty('left');
      
      // 全ての非表示属性を削除
      el.removeAttribute('data-force-hidden');
      el.removeAttribute('aria-hidden');
      el.hidden = false;
      
      // デフォルトの表示状態を復元
      if (elementType === 'image') {
        el.style.display = 'block';
      } else {
        el.style.display = 'inline-block';
      }
      
      console.log(`🔓 ${elementType}要素${index + 1}完全解除完了`);
    });
  }
  
  // 4. 複数画像コンテナの完全解除
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      // 全てのforceHideByAllMeansで適用したスタイルを削除
      multiImageContainer.style.removeProperty('display');
      multiImageContainer.style.removeProperty('visibility');
      multiImageContainer.style.removeProperty('opacity');
      multiImageContainer.style.removeProperty('height');
      multiImageContainer.style.removeProperty('width');
      multiImageContainer.style.removeProperty('overflow');
      multiImageContainer.style.removeProperty('position');
      multiImageContainer.style.removeProperty('left');
      
      // 全ての非表示属性を削除
      multiImageContainer.removeAttribute('data-force-hidden');
      multiImageContainer.removeAttribute('aria-hidden');
      multiImageContainer.hidden = false;
      
      // デフォルトの表示状態を復元
      multiImageContainer.style.display = 'flex';
      console.log(`🔓 複数画像コンテナ完全解除完了`);
    }
  }
  
  // 5. 隠れているCSSクラスも削除
  const hiddenClasses = ['hidden', 'hide', 'invisible', 'd-none'];
  hiddenClasses.forEach(cls => {
    subslotElement.classList.remove(cls);
    elements.forEach(el => {
      el.classList.remove(cls);
    });
  });
  
  console.log(`✅ ${subslotId} - ${elementType} 完全解除完了`);
}

// 🔬 サブスロット要素の詳細診断
function diagnoseSubslotElementVisibility(subslotId, elementType) {
  console.log(`🔬 === ${subslotId} - ${elementType} 詳細診断開始 ===`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) {
    console.error(`❌ サブスロット要素が見つかりません: ${subslotId}`);
    return;
  }
  
  // 基本情報
  console.log(`🔍 サブスロット要素: ${subslotElement.tagName}#${subslotElement.id}`);
  console.log(`🔍 クラスリスト: ${Array.from(subslotElement.classList).join(', ')}`);
  
  // 対象要素を取得
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (!elements || elements.length === 0) {
    console.warn(`⚠️ ${elementType}要素が見つかりません`);
    return;
  }
  
  console.log(`🔍 発見された${elementType}要素数: ${elements.length}`);
  
  elements.forEach((el, index) => {
    console.log(`\n--- ${elementType}要素${index + 1} ---`);
    console.log(`タグ: ${el.tagName}`);
    console.log(`クラス: ${el.className}`);
    console.log(`ID: ${el.id}`);
    
    // 計算されたスタイル
    const computedStyle = window.getComputedStyle(el);
    console.log(`display: ${computedStyle.display}`);
    console.log(`visibility: ${computedStyle.visibility}`);
    console.log(`opacity: ${computedStyle.opacity}`);
    
    // インラインスタイル
    console.log(`インラインstyle.display: ${el.style.display}`);
    console.log(`インラインstyle.visibility: ${el.style.visibility}`);
    console.log(`インラインstyle.opacity: ${el.style.opacity}`);
    
    // 強制非表示マーク
    console.log(`data-force-hidden: ${el.getAttribute('data-force-hidden')}`);
    
    // 親要素の状態
    console.log(`親要素display: ${window.getComputedStyle(el.parentElement).display}`);
    
    // CSSルールの確認
    console.log(`適用されているCSSクラス:`);
    el.classList.forEach(cls => {
      console.log(`  .${cls}`);
    });
  });
  
  // 複数画像コンテナの診断
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      console.log(`\n--- 複数画像コンテナ ---`);
      const containerStyle = window.getComputedStyle(multiImageContainer);
      console.log(`display: ${containerStyle.display}`);
      console.log(`visibility: ${containerStyle.visibility}`);
      console.log(`opacity: ${containerStyle.opacity}`);
      console.log(`インラインstyle: ${multiImageContainer.style.cssText}`);
    }
  }
  
  console.log(`🔬 === ${subslotId} - ${elementType} 詳細診断完了 ===`);
}

// 🔧 強制的にすべての手段で非表示にする
function forceHideByAllMeans(subslotId, elementType) {
  console.log(`🔧 全手段による強制非表示: ${subslotId} - ${elementType}`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) return;
  
  // 1. CSSクラス追加
  const className = `hidden-subslot-${elementType}`;
  subslotElement.classList.add(className);
  
  // 2. 対象要素への直接制御
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      // 複数の方法で非表示
      el.style.setProperty('display', 'none', 'important');
      el.style.setProperty('visibility', 'hidden', 'important');
      el.style.setProperty('opacity', '0', 'important');
      el.style.setProperty('height', '0', 'important');
      el.style.setProperty('width', '0', 'important');
      el.style.setProperty('overflow', 'hidden', 'important');
      el.style.setProperty('position', 'absolute', 'important');
      el.style.setProperty('left', '-9999px', 'important');
      el.setAttribute('data-force-hidden', 'true');
      el.setAttribute('aria-hidden', 'true');
      
      // さらに強力に
      el.hidden = true;
      
      console.log(`🔧 ${elementType}要素${index + 1}に全手段適用完了`);
    });
  }
  
  // 3. 複数画像コンテナへの処理
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      multiImageContainer.style.setProperty('display', 'none', 'important');
      multiImageContainer.style.setProperty('visibility', 'hidden', 'important');
      multiImageContainer.style.setProperty('opacity', '0', 'important');
      multiImageContainer.style.setProperty('height', '0', 'important');
      multiImageContainer.style.setProperty('width', '0', 'important');
      multiImageContainer.setAttribute('data-force-hidden', 'true');
      multiImageContainer.hidden = true;
      console.log(`🔧 複数画像コンテナに全手段適用完了`);
    }
  }
  
  // 4. 親要素への影響も考慮
  const parentContainer = subslotElement.closest('.subslot-container, .subslot');
  if (parentContainer) {
    parentContainer.classList.add(className);
  }
}

// 🔧 全手段による強制非表示の完全解除
function forceShowByAllMeans(subslotId, elementType) {
  console.log(`🔧 全手段による強制非表示の完全解除: ${subslotId} - ${elementType}`);
  
  const subslotElement = document.getElementById(subslotId);
  if (!subslotElement) return;
  
  // 1. CSSクラス削除
  const className = `hidden-subslot-${elementType}`;
  subslotElement.classList.remove(className);
  
  // 2. 親要素からもクラス削除
  const parentContainer = subslotElement.closest('.subslot-container, .subslot');
  if (parentContainer) {
    parentContainer.classList.remove(className);
  }
  
  // 3. 対象要素への直接制御解除
  const targetElements = {
    'image': subslotElement.querySelectorAll('.slot-image'),
    'text': subslotElement.querySelectorAll('.slot-phrase'),
    'auxtext': subslotElement.querySelectorAll('.slot-text')
  };
  
  const elements = targetElements[elementType];
  if (elements && elements.length > 0) {
    elements.forEach((el, index) => {
      // 全てのforceHideByAllMeansで適用したスタイルを削除
      el.style.removeProperty('display');
      el.style.removeProperty('visibility');
      el.style.removeProperty('opacity');
      el.style.removeProperty('height');
      el.style.removeProperty('width');
      el.style.removeProperty('overflow');
      el.style.removeProperty('position');
      el.style.removeProperty('left');
      
      // 全ての非表示属性を削除
      el.removeAttribute('data-force-hidden');
      el.removeAttribute('aria-hidden');
      el.hidden = false;
      
      // デフォルトの表示状態を復元
      if (elementType === 'image') {
        el.style.display = 'block';
      } else {
        el.style.display = 'inline-block';
      }
      
      console.log(`🔧 ${elementType}要素${index + 1}完全解除完了`);
    });
  }
  
  // 4. 複数画像コンテナの完全解除
  if (elementType === 'image') {
    const multiImageContainer = subslotElement.querySelector('.multi-image-container');
    if (multiImageContainer) {
      // 全てのforceHideByAllMeansで適用したスタイルを削除
      multiImageContainer.style.removeProperty('display');
      multiImageContainer.style.removeProperty('visibility');
      multiImageContainer.style.removeProperty('opacity');
      multiImageContainer.style.removeProperty('height');
      multiImageContainer.style.removeProperty('width');
      multiImageContainer.style.removeProperty('overflow');
      multiImageContainer.style.removeProperty('position');
      multiImageContainer.style.removeProperty('left');
      
      // 全ての非表示属性を削除
      multiImageContainer.removeAttribute('data-force-hidden');
      multiImageContainer.removeAttribute('aria-hidden');
      multiImageContainer.hidden = false;
      
      // デフォルトの表示状態を復元
      multiImageContainer.style.display = 'flex';
      console.log(`🔧 複数画像コンテナ完全解除完了`);
    }
  }
  
  // 5. 隠れているCSSクラスも削除
  const hiddenClasses = ['hidden', 'hide', 'invisible', 'd-none'];
  hiddenClasses.forEach(cls => {
    subslotElement.classList.remove(cls);
    elements.forEach(el => {
      el.classList.remove(cls);
    });
  });
  
  console.log(`✅ ${subslotId} - ${elementType} 全手段による完全解除完了`);
}

// 🔧 個別ランダマイズ時の即座適用機能（DOM再構築直後に即実行）
function applySubslotVisibilityStateImmediately(targetSlot = null) {
  if (targetSlot) {
    console.log(`⚡ 個別ランダマイズ時の即座適用: ${targetSlot}`);
  } else {
    console.log(`⚡ 全スロット即座適用（buildStructure後）`);
  }
  
  // 1. 上位スロットの非表示状態を一時的に無効化（特定スロットのみ）
  if (targetSlot) {
    const upperSlotElement = document.getElementById(`slot-${targetSlot}`);
    if (upperSlotElement) {
      // 上位スロットの非表示クラスを一時的に削除
      const upperHiddenClasses = Array.from(upperSlotElement.classList).filter(cls => cls.startsWith('hidden-'));
      upperHiddenClasses.forEach(cls => {
        upperSlotElement.classList.remove(cls);
        console.log(`🔓 上位スロット非表示クラス削除: ${cls}`);
      });
    }
  }
  
  // 2. サブスロットの非表示状態を即座に適用
  Object.keys(subslotVisibilityState).forEach(subslotId => {
    const subslotElement = document.getElementById(subslotId);
    if (!subslotElement) return;
    
    // 特定スロットが指定されている場合は、そのスロットのサブスロットのみ処理
    if (targetSlot && !subslotId.includes(`slot-${targetSlot}-sub-`)) return;
    
    const elementState = subslotVisibilityState[subslotId];
    Object.keys(elementState).forEach(elementType => {
      const isVisible = elementState[elementType];
      
      if (!isVisible) {
        if (targetSlot) {
          console.log(`⚡ 即座強制非表示: ${subslotId} - ${elementType}`);
        }
        
        // 即座に完全非表示を適用
        forceHideByAllMeans(subslotId, elementType);
        
        // 追加で要素を確実に非表示
        const targetElements = {
          'image': subslotElement.querySelectorAll('.slot-image'),
          'text': subslotElement.querySelectorAll('.slot-phrase'),
          'auxtext': subslotElement.querySelectorAll('.slot-text')
        };
        
        const elements = targetElements[elementType];
        if (elements && elements.length > 0) {
          elements.forEach(el => {
            el.style.setProperty('display', 'none', 'important');
            el.style.setProperty('visibility', 'hidden', 'important');
            el.style.setProperty('opacity', '0', 'important');
            el.hidden = true;
            el.setAttribute('data-force-hidden', 'true');
          });
        }
        
        // 複数画像コンテナも即座に非表示
        if (elementType === 'image') {
          const multiImageContainer = subslotElement.querySelector('.multi-image-container');
          if (multiImageContainer) {
            multiImageContainer.style.setProperty('display', 'none', 'important');
            multiImageContainer.style.setProperty('visibility', 'hidden', 'important');
            multiImageContainer.style.setProperty('opacity', '0', 'important');
            multiImageContainer.hidden = true;
            multiImageContainer.setAttribute('data-force-hidden', 'true');
          }
        }
      } else {
        if (targetSlot) {
          console.log(`⚡ 即座表示解除: ${subslotId} - ${elementType}`);
        }
        
        // 表示時は完全解除
        forceShowByAllMeans(subslotId, elementType);
      }
    });
  });
  
  // 3. チェックボックスの状態も同期
  Object.keys(subslotVisibilityState).forEach(subslotId => {
    // 特定スロットが指定されている場合は、そのスロットのサブスロットのみ処理
    if (targetSlot && !subslotId.includes(`slot-${targetSlot}-sub-`)) return;
    
    const elementState = subslotVisibilityState[subslotId];
    Object.keys(elementState).forEach(elementType => {
      const isVisible = elementState[elementType];
      const checkbox = document.querySelector(`[data-subslot-id="${subslotId}"][data-element-type="${elementType}"]`);
      if (checkbox) {
        checkbox.checked = isVisible;
      }
    });
  });
  
  if (targetSlot) {
    console.log(`✅ 即座適用完了: ${targetSlot}`);
  } else {
    console.log(`✅ 全スロット即座適用完了`);
  }
}

// 🔧 個別ランダマイズ用の上位スロット非表示状態回避機能
function neutralizeUpperSlotVisibility(targetSlot) {
  console.log(`🔧 上位スロット非表示状態を回避: ${targetSlot}`);
  
  const upperSlotElement = document.getElementById(`slot-${targetSlot}`);
  if (!upperSlotElement) return;
  
  // 上位スロットの非表示クラスを全て削除
  const hiddenClasses = Array.from(upperSlotElement.classList).filter(cls => cls.startsWith('hidden-'));
  hiddenClasses.forEach(cls => {
    upperSlotElement.classList.remove(cls);
    console.log(`🔓 上位スロット非表示クラス削除: ${cls}`);
  });
  
  // 上位スロットの直接スタイルも削除
  upperSlotElement.style.removeProperty('display');
  upperSlotElement.style.removeProperty('visibility');
  upperSlotElement.style.removeProperty('opacity');
  upperSlotElement.removeAttribute('data-force-hidden');
  upperSlotElement.hidden = false;
  
  // サブスロットコンテナも表示状態に
  const subslotContainer = document.getElementById(`slot-${targetSlot}-sub`);
  if (subslotContainer) {
    subslotContainer.style.removeProperty('display');
    subslotContainer.style.removeProperty('visibility');
    subslotContainer.style.removeProperty('opacity');
    subslotContainer.removeAttribute('data-force-hidden');
    subslotContainer.hidden = false;
    
    // 上位スロットの影響を受けないようにサブスロットコンテナを強制表示
    subslotContainer.style.setProperty('display', 'block', 'important');
    subslotContainer.style.setProperty('visibility', 'visible', 'important');
    subslotContainer.style.setProperty('opacity', '1', 'important');
  }
  
  console.log(`✅ 上位スロット非表示状態回避完了: ${targetSlot}`);
}

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 サブスロット表示制御システムを初期化中...");
  console.log("✅ subslot_toggle.js との連携は自動的に行われます");
  
  // サブスロット状態管理システムを初期化
  initializeSubslotVisibilityState();
  
  // 🏷️ ラベル復元システムを有効化
  console.log("🏷️ サブスロットラベル復元システムを有効化中...");
  hookDataInsertionForLabelRestore();
  
  // サブスロットの展開・折りたたみ監視
  if (window.MutationObserver) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' || mutation.type === 'attributes') {
          // サブスロットの表示状態が変化した場合の処理
          restoreSubslotLabels();
          
          // 🆕 状態変更後に保存された状態を再適用
          setTimeout(() => {
            applySubslotVisibilityState();
          }, 200);
        }
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['style', 'class']
    });
    
    // 🆕 強制非表示状態を維持するための監視
    const forceHideObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
          const target = mutation.target;
          if (target.hasAttribute('data-force-hidden')) {
            // 強制非表示状態が上書きされた場合は復元
            target.style.setProperty('display', 'none', 'important');
            target.style.setProperty('visibility', 'hidden', 'important');
            target.style.setProperty('opacity', '0', 'important');
            console.log(`🔒 強制非表示状態を復元: ${target.tagName}.${target.className}`);
          }
        }
      });
    });
    
    forceHideObserver.observe(document.body, {
      attributes: true,
      subtree: true,
      attributeFilter: ['style']
    });
    
    // 🔒 定期的な強制非表示状態の維持
    setInterval(() => {
      Object.keys(subslotVisibilityState).forEach(subslotId => {
        const elementState = subslotVisibilityState[subslotId];
        Object.keys(elementState).forEach(elementType => {
          const isVisible = elementState[elementType];
          if (!isVisible) {
            // 非表示であるべき要素の状態を維持
            forceHideByAllMeans(subslotId, elementType);
          } else {
            // 表示であるべき要素の状態を維持（完全解除）
            forceShowByAllMeans(subslotId, elementType);
          }
        });
      });
    }, 2000); // 2秒ごとに強制維持
  }
  
  console.log("✅ サブスロット表示制御システム初期化完了");
});

console.log("✅ subslot_visibility_control.js が読み込まれました");

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
// 🆕 状態管理関数をエクスポート
window.initializeSubslotVisibilityState = initializeSubslotVisibilityState;
window.saveSubslotVisibilityState = saveSubslotVisibilityState;
window.loadSubslotVisibilityState = loadSubslotVisibilityState;
window.applySubslotVisibilityState = applySubslotVisibilityState;
window.getSubslotVisibilityState = getSubslotVisibilityState;
// 🔄 個別ランダマイズ後の状態復元関数をエクスポート
window.restoreSubslotVisibilityAfterIndividualRandomization = restoreSubslotVisibilityAfterIndividualRandomization;
// 🔒 強制制御関数をエクスポート
window.forceHideSubslotElements = forceHideSubslotElements;
window.forceShowSubslotElements = forceShowSubslotElements;
// 🔬 診断・強制制御関数をエクスポート
window.diagnoseSubslotElementVisibility = diagnoseSubslotElementVisibility;
window.forceHideByAllMeans = forceHideByAllMeans;
window.forceShowByAllMeans = forceShowByAllMeans;
// 🆕 個別ランダマイズ時の即座適用機能をエクスポート
window.applySubslotVisibilityStateImmediately = applySubslotVisibilityStateImmediately;
window.neutralizeUpperSlotVisibility = neutralizeUpperSlotVisibility;
// 🆕 buildStructure実行後の統合適用関数をエクスポート
window.applyVisibilityStateAfterBuildStructure = applyVisibilityStateAfterBuildStructure;

// 🔄 buildStructure実行後の統合適用関数
function applyVisibilityStateAfterBuildStructure() {
  console.log("🔄 buildStructure実行後のサブスロット表示制御適用開始");
  
  // 上位スロットの表示状態を適用（上位スロットの制御システムとの統合）
  if (typeof window.applyVisibilityState === 'function') {
    console.log("🔄 上位スロットの表示状態を適用中...");
    window.applyVisibilityState();
  }
  
  // サブスロットの表示状態を即座に適用
  applySubslotVisibilityStateImmediately();
  
  console.log("✅ buildStructure実行後のサブスロット表示制御適用完了");
}
