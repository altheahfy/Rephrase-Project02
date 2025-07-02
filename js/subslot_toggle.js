function toggleExclusiveSubslot(slotId) {
  if (toggleExclusiveSubslot.lock) return;
  toggleExclusiveSubslot.lock = true;
  setTimeout(() => { toggleExclusiveSubslot.lock = false; }, 100);
  console.log(`🔑 toggleExclusiveSubslot called for slot-${slotId}-sub`);

  const subslotIds = ["o1", "c1", "o2", "m1", "s", "m2", "c2", "m3"];
  const target = document.getElementById(`slot-${slotId}-sub`);
  if (!target) {
    console.warn(`⚠ toggleExclusiveSubslot: target slot-${slotId}-sub not found`);
    return;
  }

  const isOpen = getComputedStyle(target).display !== "none";

  // 🔗 全サブスロットを閉じる前に、タブ連結スタイルをクリア
  clearAllTabConnections();
  
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) {
      el.style.setProperty("display", "none", "important");
      // 位置調整スタイルもリセット
      el.style.marginLeft = '';
      el.style.maxWidth = '';
      el.style.removeProperty('--parent-offset');
      console.log(`❌ slot-${id}-sub display set to none`);
      
      // サブスロット用コントロールパネルを削除
      if (window.removeSubslotControlPanel) {
        console.log(`🗑️ ${id} のサブスロット用コントロールパネルを削除します`);
        window.removeSubslotControlPanel(id);
      } else {
        console.warn("⚠ removeSubslotControlPanel 関数が見つかりません");
      }
    }
  });

  // 対象のみ開く
  if (!isOpen) {
    target.style.setProperty("display", "flex", "important");
    target.style.setProperty("visibility", "visible", "important");
    target.style.setProperty("min-height", "100px", "important");
    target.style.visibility = "visible";
    target.style.minHeight = "100px";
    console.log(`✅ slot-${slotId}-sub opened, display: ${getComputedStyle(target).display}`);

    // 🔗 エクセル風タブ連結スタイルを適用
    applyTabConnection(slotId, true);
    
    // 📍 サブスロット位置を調整
    setTimeout(() => {
      adjustSubslotPosition(slotId);
    }, 50);

    // ★★★ 並べ替え処理を呼び出す ★★★
    if (window.reorderSubslotsInContainer && window.loadedJsonData) {
      console.log(`🔄 ${target.id} のサブスロットを並べ替えます`);
      window.reorderSubslotsInContainer(target, window.loadedJsonData);
    } else {
      console.warn("⚠ reorderSubslotsInContainer または window.loadedJsonData が見つかりません");
    }
    
    // ★★★ 空のサブスロット非表示処理を呼び出す ★★★
    console.log(`🙈 ${target.id} 内の空サブスロットを非表示にします`);
    hideEmptySubslotsInContainer(target);

    // ★★★ サブスロット用コントロールパネルを追加 ★★★
    if (window.addSubslotControlPanel) {
      console.log(`🎛️ ${slotId} にサブスロット用コントロールパネルを追加します`);
      window.addSubslotControlPanel(slotId);
    } else {
      console.warn("⚠ addSubslotControlPanel 関数が見つかりません");
      console.log("🔍 window.addSubslotControlPanel =", window.addSubslotControlPanel);
    }

  } else {
    console.log(`ℹ slot-${slotId}-sub was already open, now closed`);
  }
}

// ページ読み込み時に全サブスロットを初期化（閉じる）する関数
function initializeSubslots() {
  console.log("🔄 サブスロットの初期化を実行します");
  
  // 🧹 まず全てのタブ連結スタイルをクリア
  clearAllTabConnections();
  
  const subslotIds = ["o1", "c1", "o2", "m1", "s", "m2", "c2", "m3"];
  
  // 全てのサブスロットコンテナを取得して閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) {
      el.style.setProperty("display", "none", "important");
      console.log(`🔒 初期化: slot-${id}-sub を閉じました`);
    }
  });
  
  // 他のIDパターンのサブスロットも閉じる
  const allSubslotElements = document.querySelectorAll('[id$="-sub"]');
  allSubslotElements.forEach(el => {
    if (el && !el.id.includes('wrapper')) { // wrapper要素は除外
      el.style.setProperty("display", "none", "important");
      // 位置調整スタイルもリセット
      el.style.marginLeft = '';
      el.style.maxWidth = '';
      el.style.removeProperty('--parent-offset');
      console.log(`🔒 初期化: ${el.id} を閉じました`);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // 初期化：全サブスロットを閉じる
  initializeSubslots();
  
  const buttons = document.querySelectorAll("[data-subslot-toggle], .subslot-toggle-button button");
  console.log(`🔍 Found ${buttons.length} toggle candidate buttons`);
  buttons.forEach(button => {
    let slotId = button.getAttribute("data-subslot-toggle");
    if (!slotId) {
      const onclickAttr = button.getAttribute("onclick");
      const match = onclickAttr && onclickAttr.match(/toggleExclusiveSubslot\(['"](.+?)['"]\)/);
      if (match) slotId = match[1];
    }
    console.log(`📝 Button: ${button.outerHTML}`);
    console.log(`➡ slotId resolved: ${slotId}`);

    if (slotId) {
      button.addEventListener("click", () => {
        console.log(`🚀 Event listener triggered for slotId: ${slotId}`);
        toggleExclusiveSubslot(slotId);
      });
      console.log(`✅ Event listener attached for slotId: ${slotId}`);
    } else {
      console.warn(`⚠ No slotId resolved for button`);
    }
  });
});

// ウィンドウリサイズ時にタブ連結の位置を再調整
window.addEventListener('resize', () => {
  // 現在展開中のサブスロットを見つけて位置を再調整
  const activeSubslotArea = document.querySelector('.slot-wrapper.active-subslot-area');
  if (activeSubslotArea) {
    const parentId = activeSubslotArea.id?.replace('slot-', '').replace('-sub', '');
    if (parentId) {
      console.log(`🔄 リサイズ時の位置再調整: ${parentId}`);
      setTimeout(() => {
        adjustSubslotPosition(parentId);
      }, 100);
    }
  }
});

window.toggleExclusiveSubslot = toggleExclusiveSubslot;


function bindSubslotToggleButtons() {
  const buttons = document.querySelectorAll("[data-subslot-toggle], .subslot-toggle-button button");
  console.log(`🔍 Rebinding: Found ${buttons.length} toggle candidate buttons`);
  buttons.forEach(button => {
    let slotId = button.getAttribute("data-subslot-toggle");
    if (!slotId) {
      const onclickAttr = button.getAttribute("onclick");
      const match = onclickAttr && onclickAttr.match(/toggleExclusiveSubslot\(['"](.+?)['"]\)/);
      if (match) slotId = match[1];
    }

    if (slotId) {
      button.onclick = null; // 既存の onclick をクリア
      button.addEventListener("click", () => {
        console.log(`🚀 Event listener triggered for slotId: ${slotId}`);
        toggleExclusiveSubslot(slotId);
      });
      console.log(`✅ Event listener rebound for slotId: ${slotId}`);
    }
  });
}

/**
 * 指定されたサブスロットコンテナ内の空のサブスロットを非表示にする
 * @param {HTMLElement} container - サブスロットコンテナ
 */
function hideEmptySubslotsInContainer(container) {
  if (!container) {
    console.warn("⚠ hideEmptySubslotsInContainer: コンテナが指定されていません");
    return;
  }
  
  console.log(`🔍 ${container.id} 内のサブスロット空判定を開始`);
  
  // コンテナ内の全サブスロットを取得
  const subSlots = container.querySelectorAll('[id*="-sub-"]');
  console.log(`📊 対象サブスロット: ${subSlots.length}件`);
  
  let hiddenCount = 0;
  let visibleCount = 0;
  
  subSlots.forEach(subSlot => {
    const phraseDiv = subSlot.querySelector('.slot-phrase');
    const textDiv = subSlot.querySelector('.slot-text');
    
    // サブスロットが空かどうかを判定（phraseとtext両方が空なら空と判定）
    const phraseEmpty = !phraseDiv || !phraseDiv.textContent || phraseDiv.textContent.trim() === '';
    const textEmpty = !textDiv || !textDiv.textContent || textDiv.textContent.trim() === '';
    const isEmpty = phraseEmpty && textEmpty;
    
    console.log(`🔍 ${subSlot.id}:`);
    console.log(`  - phrase: "${phraseDiv?.textContent || ''}"`);
    console.log(`  - text: "${textDiv?.textContent || ''}"`);
    console.log(`  - 空判定: ${isEmpty}`);
    
    if (isEmpty) {
      subSlot.style.display = 'none';
      subSlot.classList.add('empty-subslot-hidden');
      console.log(`👻 ${subSlot.id} を非表示にしました`);
      hiddenCount++;
    } else {
      subSlot.style.display = '';
      subSlot.classList.remove('empty-subslot-hidden');
      console.log(`👁 ${subSlot.id} を表示状態にしました`);
      visibleCount++;
    }
  });
  
  console.log(`📊 ${container.id} 処理結果: 非表示=${hiddenCount}件, 表示=${visibleCount}件`);
  console.log(`✅ ${container.id} のサブスロット空判定完了`);
}

// 🔗 エクセル風タブ連結システム (統合版)

/**
 * 🔗 エクセル風タブ連結システム: 上位スロットとサブスロットを視覚的に連結
 * @param {string} parentSlotId - 親スロットのID (例: 'm1', 'o2')
 * @param {boolean} isActive - 連結を有効にするかどうか
 */
function applyTabConnection(parentSlotId, isActive) {
  console.log(`🔗 タブ連結${isActive ? '適用' : '解除'}: ${parentSlotId}`);
  
  // 必要な要素を取得
  const parentSlot = document.getElementById(`slot-${parentSlotId}`);
  const subslotArea = document.getElementById(`slot-${parentSlotId}-sub`);
  const subslotLabel = subslotArea?.querySelector('.subslot-label');
  
  if (!parentSlot || !subslotArea) {
    console.warn(`⚠ タブ連結: 必要な要素が見つかりません (parent: ${!!parentSlot}, subslot: ${!!subslotArea})`);
    return;
  }
  
  if (isActive) {
    // 🔗 まず全ての既存のタブ連結をクリア
    clearAllTabConnections();
    
    // 🎨 現在のスロットにタブ連結スタイルを適用
    parentSlot.classList.add('active-parent-slot');
    subslotArea.classList.add('active-subslot-area');
    
    // 📂 サブスロットラベルをタブ風にスタイリング
    if (subslotLabel) {
      subslotLabel.classList.add('tab-style');
      subslotLabel.innerHTML = `📂 ${parentSlotId.toUpperCase()} の詳細スロット`;
    }
    
    // 🎛️ サブスロット制御パネルが存在すれば統合スタイルを適用
    setTimeout(() => {
      const panel = document.getElementById(`subslot-visibility-panel-${parentSlotId}`);
      if (panel) {
        panel.classList.add('tab-connected');
        console.log(`🎛️ サブスロット制御パネルにタブ連結スタイルを適用: ${parentSlotId}`);
      }
    }, 100);
    
    console.log(`✅ ${parentSlotId} のタブ連結スタイルを適用しました`);
  } else {
    // 🔗 タブ連結スタイルを解除
    parentSlot.classList.remove('active-parent-slot');
    subslotArea.classList.remove('active-subslot-area');
    
    // 📂 サブスロットラベルを元に戻す
    if (subslotLabel) {
      subslotLabel.classList.remove('tab-style');
      subslotLabel.innerHTML = `現在展開中：${parentSlotId.toUpperCase()} の subslot`;
    }
    
    // 🎛️ サブスロット制御パネルのタブスタイルも解除
    const panel = document.getElementById(`subslot-visibility-panel-${parentSlotId}`);
    if (panel) {
      panel.classList.remove('tab-connected');
    }
    
    console.log(`❌ ${parentSlotId} のタブ連結スタイルを解除しました`);
  }
}

/**
 * 📍 サブスロットエリアの位置を上位スロットに近づける
 * @param {string} parentSlotId - 親スロットのID
 */
function adjustSubslotPosition(parentSlotId) {
  const parentSlot = document.getElementById(`slot-${parentSlotId}`);
  const subslotArea = document.getElementById(`slot-${parentSlotId}-sub`);
  
  if (!parentSlot || !subslotArea) {
    console.warn(`⚠ 位置調整: 必要な要素が見つかりません`);
    return;
  }
  
  try {
    // 親スロットの位置を取得
    const parentRect = parentSlot.getBoundingClientRect();
    const containerRect = parentSlot.parentElement.getBoundingClientRect();
    
    // サブスロットエリアを親スロットの直下に配置
    const leftOffset = parentRect.left - containerRect.left;
    
    // CSSカスタムプロパティとinlineスタイルで位置調整
    subslotArea.style.setProperty('--parent-offset', `${leftOffset}px`);
    subslotArea.style.marginLeft = `${Math.max(0, leftOffset - 10)}px`;
    subslotArea.style.maxWidth = `calc(100% - ${Math.max(0, leftOffset - 10)}px)`;
    
    console.log(`📍 ${parentSlotId} サブスロットの位置を調整しました (leftOffset: ${leftOffset}px)`);
  } catch (error) {
    console.warn(`⚠ サブスロット位置調整エラー: ${parentSlotId}`, error);
  }
}

/**
 * 🧹 全てのタブ連結スタイルをクリア
 */
function clearAllTabConnections() {
  // 🔗 上位スロットからタブ連結クラスを削除
  const allParentSlots = document.querySelectorAll('.slot-container.active-parent-slot');
  allParentSlots.forEach(slot => slot.classList.remove('active-parent-slot'));
  
  // 🔗 サブスロットエリアからタブ連結クラスを削除
  const allSubslotAreas = document.querySelectorAll('.slot-wrapper.active-subslot-area');
  allSubslotAreas.forEach(area => area.classList.remove('active-subslot-area'));
  
  // 📂 サブスロットラベルからタブスタイルを削除
  const allTabLabels = document.querySelectorAll('.subslot-label.tab-style');
  allTabLabels.forEach(label => {
    label.classList.remove('tab-style');
    // 元のテキストに戻す（IDから推測）
    const parentId = label.closest('[id*="-sub"]')?.id?.replace('slot-', '').replace('-sub', '');
    if (parentId) {
      label.innerHTML = `現在展開中：${parentId.toUpperCase()} の subslot`;
    }
  });
  
  // 🎛️ サブスロット制御パネルからタブ連結スタイルを削除
  const allTabPanels = document.querySelectorAll('.subslot-visibility-panel.tab-connected');
  allTabPanels.forEach(panel => panel.classList.remove('tab-connected'));
  
  console.log(`🧹 全てのタブ連結スタイルをクリアしました`);
}
