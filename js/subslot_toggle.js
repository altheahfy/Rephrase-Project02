function toggleExclusiveSubslot(slotId) {
  if (toggleExclusiveSubslot.lock) {
    console.log(`🔒 toggleExclusiveSubslot: ロック中のため処理をスキップ (${slotId})`);
    return;
  }
  toggleExclusiveSubslot.lock = true;
  console.log(`🔑 toggleExclusiveSubslot called for slot-${slotId}-sub`);

  const subslotIds = ["o1", "c1", "o2", "m1", "s", "m2", "c2", "m3"];
  const target = document.getElementById(`slot-${slotId}-sub`);
  if (!target) {
    console.warn(`⚠ toggleExclusiveSubslot: target slot-${slotId}-sub not found`);
    toggleExclusiveSubslot.lock = false;
    return;
  }

  const isOpen = getComputedStyle(target).display !== "none";

  // 全 subslot を閉じる
  subslotIds.forEach(id => {
    const el = document.getElementById(`slot-${id}-sub`);
    if (el) {
      el.style.setProperty("display", "none", "important");
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

    // 少し遅延を入れて、DOM更新後に処理を実行
    setTimeout(() => {
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

      // ★★★ サブスロット用コントロールパネルを追加（最後に実行） ★★★
      setTimeout(() => {
        if (window.addSubslotControlPanel) {
          console.log(`🎛️ ${slotId} にサブスロット用コントロールパネルを追加します`);
          window.addSubslotControlPanel(slotId);
        } else {
          console.warn("⚠ addSubslotControlPanel 関数が見つかりません");
          console.log("🔍 window.addSubslotControlPanel =", window.addSubslotControlPanel);
        }
      }, 50); // さらに短い遅延でパネル追加
    }, 50); // 50ms遅延でサブスロット処理を実行

  } else {
    console.log(`ℹ slot-${slotId}-sub was already open, now closed`);
  }
  
  // 処理完了後にロックを解除（遅延処理の完了後）
  setTimeout(() => {
    toggleExclusiveSubslot.lock = false;
    console.log(`🔓 toggleExclusiveSubslot: ロック解除 (${slotId})`);
  }, 200); // 十分な遅延を設ける
}

// ページ読み込み時に全サブスロットを初期化（閉じる）する関数
function initializeSubslots() {
  console.log("🔄 サブスロットの初期化を実行します");
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
