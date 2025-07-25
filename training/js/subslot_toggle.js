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
      // 位置調整スタイルを完全にリセット
      el.style.marginLeft = '';
      el.style.maxWidth = '';
      el.style.left = '';
      el.style.right = '';
      el.style.position = '';
      el.style.transform = '';
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
    // 🔄 まず位置関連のスタイルを完全にリセット
    target.style.marginLeft = '';
    target.style.maxWidth = '';
    target.style.left = '';
    target.style.right = '';
    target.style.position = '';
    target.style.transform = '';
    target.style.removeProperty('--parent-offset');
    
    // 🎯 サブスロットを表示
    target.style.setProperty("display", "flex", "important");
    target.style.setProperty("visibility", "visible", "important");
    target.style.setProperty("min-height", "100px", "important");
    target.style.visibility = "visible";
    target.style.minHeight = "100px";
    
    console.log(`✅ slot-${slotId}-sub opened, display: ${getComputedStyle(target).display}`);
    console.log(`🔍 位置確認: marginLeft=${target.style.marginLeft}, maxWidth=${target.style.maxWidth}`);

    // 🔗 エクセル風タブ連結スタイルを適用（デバッグ強化版）
    console.log(`🔗 タブ連結スタイル適用開始: ${slotId}`);
    
    // 必要な要素を直接取得してログ出力
    const parentSlot = document.getElementById(`slot-${slotId}`);
    const subslotArea = document.getElementById(`slot-${slotId}-sub`);
    
    console.log(`🔍 要素確認:`);
    console.log(`  - parentSlot (slot-${slotId}): ${!!parentSlot}`);
    console.log(`  - subslotArea (slot-${slotId}-sub): ${!!subslotArea}`);
    
    if (parentSlot && subslotArea) {
      // 🧹 まず既存のタブ連結スタイルをクリア
      clearAllTabConnections();
      
      // 直接クラスを追加
      parentSlot.classList.add('active-parent-slot');
      subslotArea.classList.add('active-subslot-area');
      
      // CSSが優先されるように、インラインスタイルは最小限に（CSS !importantが効くように）
      console.log(`✅ クラス追加完了:`);
      console.log(`  - parentSlot classes: ${parentSlot.className}`);
      console.log(`  - subslotArea classes: ${subslotArea.className}`);
      
      // ラベルの処理
      const subslotLabel = subslotArea.querySelector('.subslot-label');
      if (subslotLabel) {
        subslotLabel.classList.add('tab-style');
        subslotLabel.innerHTML = `📂 ${slotId.toUpperCase()} の詳細スロット`;
        console.log(`✅ ラベル更新完了: ${subslotLabel.innerHTML}`);
      } else {
        console.warn(`⚠ サブスロットラベルが見つかりません`);
      }
    } else {
      console.error(`❌ 必要な要素が見つかりません`);
    }
    
    // 従来の関数も呼び出し
    applyTabConnection(slotId, true);
    
    // �️ 横スクロールドラッグ機能を追加
    console.log(`🖱️ サブスロット ${slotId} に横スクロールドラッグ機能を追加します`);
    addHorizontalDragToSubslot(target);
    
    // �📍 サブスロット位置を調整（安全な軽微調整版）
    setTimeout(() => {
      adjustSubslotPositionSafe(slotId);
    }, 300); // DOM更新とレンダリング完了を確実に待つ（150ms→300ms）

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

    // ★★★ サブスロット制御パネルを作成 ★★★
    if (window.createSubslotControlPanel) {
      console.log(`🎛️ ${slotId} のサブスロット制御パネルを作成します`);
      window.createSubslotControlPanel(slotId);
    } else {
      console.warn("⚠ createSubslotControlPanel 関数が見つかりません");
    }

    // 🔍 ★★★ ズーム機能連携：サブスロット展開後にズーム適用 ★★★
    if (window.forceSubslotDetection) {
      setTimeout(() => {
        console.log(`🔍 ${slotId} サブスロット展開完了 - ズーム適用`);
        window.forceSubslotDetection();
        
        // 🆕 追加：ズーム適用の即座確認
        setTimeout(() => {
          const expandedSubslot = document.getElementById(`slot-${slotId}-sub`);
          if (expandedSubslot) {
            const currentTransform = expandedSubslot.style.transform;
            console.log(`🔍 ${slotId} サブスロット最終確認: transform="${currentTransform}"`);
            
            // ズームが適用されていない場合は直接適用
            if (window.zoomController && !currentTransform.includes('scale')) {
              const currentZoom = window.zoomController.getCurrentZoom();
              console.log(`🔧 ${slotId} サブスロットに直接ズーム適用: ${Math.round(currentZoom * 100)}%`);
              expandedSubslot.style.setProperty('transform', `scale(${currentZoom})`, 'important');
              expandedSubslot.style.setProperty('transform-origin', 'top left', 'important');
            }
          }
        }, 100);
      }, 300); // 遅延を300msに短縮してより迅速なズーム適用
    } else {
      console.warn("⚠ ズームコントローラーが利用できません");
    }

    // ★★★ サブスロット用コントロールパネルを追加 ★★★
    if (window.addSubslotControlPanel) {
      console.log(`🎛️ ${slotId} にサブスロット用コントロールパネルを追加します`);
      window.addSubslotControlPanel(slotId);
    } else {
      console.warn("⚠ addSubslotControlPanel 関数が見つかりません");
      console.log("🔍 window.addSubslotControlPanel =", window.addSubslotControlPanel);
    }

    // ★★★ サブスロット画像更新処理を追加 ★★★
    if (window.handleSubslotDisplay) {
      console.log(`🖼️ ${slotId} のサブスロット画像更新を開始します`);
      window.handleSubslotDisplay(slotId);
    } else {
      console.warn("⚠ handleSubslotDisplay 関数が見つかりません");
      console.log("🔍 window.handleSubslotDisplay =", window.handleSubslotDisplay);
    }

    // 🖼️ C1サブスロット専用：全処理完了後に画像適用
    if (slotId === 'c1') {
      setTimeout(() => {
        console.log('🖼️ C1サブスロット画像を遅延適用開始');
        const c1Subslots = [
          'slot-c1-sub-m1', 'slot-c1-sub-s', 'slot-c1-sub-aux', 'slot-c1-sub-m2',
          'slot-c1-sub-v', 'slot-c1-sub-c1', 'slot-c1-sub-o1', 'slot-c1-sub-o2',
          'slot-c1-sub-c2', 'slot-c1-sub-m3'
        ];
        
        c1Subslots.forEach(subslotId => {
          const container = document.getElementById(subslotId);
          if (container && container.style.display !== 'none') {
            const phraseEl = container.querySelector('.slot-phrase');
            const textEl = container.querySelector('.slot-text');
            const englishText = (phraseEl?.textContent || textEl?.textContent || '').trim();
            
            if (englishText && window.applyImageToSubslot) {
              console.log(`🎯 C1遅延画像適用: ${subslotId} → "${englishText}"`);
              window.applyImageToSubslot(subslotId, englishText);
            }
          }
        });
      }, 1000); // 1秒遅延で確実に全処理完了後に実行
    }

  } else {
    // サブスロットを閉じる場合
    // 対象の親スロットとサブスロットエリアのクラス・インラインスタイルをリセット
    const parentSlot = document.getElementById(`slot-${slotId}`);
    const subslotArea = document.getElementById(`slot-${slotId}-sub`);
    if (parentSlot) {
      parentSlot.classList.remove('active-parent-slot');
      // ブルータブのインラインスタイルを完全にクリア
      parentSlot.style.background = '';
      parentSlot.style.backgroundColor = '';
      parentSlot.style.border = '';
      parentSlot.style.borderBottom = '';
      parentSlot.style.borderRadius = '';
      parentSlot.style.boxShadow = '';
    }
    if (subslotArea) {
      subslotArea.classList.remove('active-subslot-area');
      // ブルータブのインラインスタイルを完全にクリア
      subslotArea.style.background = '';
      subslotArea.style.backgroundColor = '';
      subslotArea.style.border = '';
      subslotArea.style.borderTop = '';
      subslotArea.style.borderRadius = '';
      subslotArea.style.marginTop = '';
      subslotArea.style.boxShadow = '';
    }
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
      // 位置調整スタイルを完全にリセット
      el.style.marginLeft = '';
      el.style.maxWidth = '';
      el.style.left = '';
      el.style.right = '';
      el.style.position = '';
      el.style.transform = '';
      el.style.removeProperty('--parent-offset');
      // ブルータブのインラインスタイルも完全にクリア
      el.style.background = '';
      el.style.backgroundColor = '';
      el.style.border = '';
      el.style.borderTop = '';
      el.style.borderRadius = '';
      el.style.marginTop = '';
      el.style.boxShadow = '';
      console.log(`🔒 初期化: ${el.id} を閉じました`);
    }
  });

  // 全ての上位スロットのブルータブスタイルもクリア
  const allParentSlots = document.querySelectorAll('.slot-container');
  allParentSlots.forEach(slot => {
    slot.classList.remove('active-parent-slot');
    slot.style.background = '';
    slot.style.backgroundColor = '';
    slot.style.border = '';
    slot.style.borderBottom = '';
    slot.style.borderRadius = '';
    slot.style.boxShadow = '';
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
        adjustSubslotPositionSafe(parentId); // 安全版を使用
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
 * 📍 サブスロットエリアの位置を上位スロットに近づける（改良版）
 * 画面端での制限とスマートな位置調整を実装
 * @param {string} parentSlotId - 親スロットのID
 */
function adjustSubslotPosition(parentSlotId) {
  // ⚡ ズーム中は位置調整をスキップ
  if (window.isZooming) {
    console.log(`⚡ ズーム中のため位置調整をスキップ: ${parentSlotId}`);
    return;
  }
  
  const parentSlot = document.getElementById(`slot-${parentSlotId}`);
  const subslotArea = document.getElementById(`slot-${parentSlotId}-sub`);
  
  if (!parentSlot || !subslotArea) {
    console.warn(`⚠ 位置調整: 必要な要素が見つかりません`);
    return;
  }
  
  try {
    // 🔍 サブスロットの実際のサイズを安全に測定
    // 表示中のサブスロットに影響を与えずに幅を取得
    
    // 各種コンテナの位置とサイズを取得
    const parentRect = parentSlot.getBoundingClientRect();
    const containerRect = parentSlot.parentElement.getBoundingClientRect();
    const windowWidth = window.innerWidth;
    
    // サブスロットの現在の幅を取得（一時的な変更は行わない）
    let actualSubslotWidth = subslotArea.offsetWidth;
    
    // もし幅が取得できない場合は、推定値を使用
    if (!actualSubslotWidth || actualSubslotWidth === 0) {
      // コンテナ幅の80%を推定値とする
      const containerWidth = containerRect.width;
      actualSubslotWidth = containerWidth * 0.8;
      console.log(`📏 ${parentSlotId} サブスロット幅を推定: ${actualSubslotWidth}px`);
    }
    
    // 親スロットの中央位置を計算
    const parentCenterX = parentRect.left + (parentRect.width / 2);
    const containerLeft = containerRect.left;
    
    // 理想的な位置: サブスロットの中央が親スロットの中央に合う位置
    const idealLeftOffset = parentCenterX - containerLeft - (actualSubslotWidth / 2);
    
    // 画面境界の制約を計算
    const minLeftOffset = 20; // 左端から最低20px
    const maxLeftOffset = Math.max(20, windowWidth - actualSubslotWidth - 40); // 右端から最低40px
    
    // 🎯 スマートな位置調整：端の方では中央寄せを弱める
    let finalLeftOffset;
    
    if (idealLeftOffset >= minLeftOffset && idealLeftOffset <= maxLeftOffset) {
      // 理想位置が境界内なら、そのまま使用
      finalLeftOffset = idealLeftOffset;
    } else {
      // 境界を超える場合は、減衰効果を適用
      const screenCenter = windowWidth / 2;
      const distanceFromCenter = Math.abs(parentCenterX - screenCenter);
      const maxDistance = screenCenter * 0.8; // 画面中央の80%の位置まで
      
      if (distanceFromCenter <= maxDistance) {
        // 中央寄りの場合は理想位置に近づける
        finalLeftOffset = Math.max(minLeftOffset, Math.min(idealLeftOffset, maxLeftOffset));
      } else {
        // 端寄りの場合は保守的な位置調整
        const baseOffset = parentRect.left - containerLeft;
        const conservativeOffset = baseOffset * 0.3; // 30%だけ調整
        finalLeftOffset = Math.max(minLeftOffset, Math.min(conservativeOffset, maxLeftOffset));
      }
    }
    
    // 最終的な境界チェック
    finalLeftOffset = Math.max(0, Math.min(finalLeftOffset, windowWidth - 100)); // 最低100px幅を確保
    
    // CSSスタイルを安全に適用
    subslotArea.style.setProperty('--parent-offset', `${finalLeftOffset}px`);
    subslotArea.style.marginLeft = `${finalLeftOffset}px`;
    subslotArea.style.maxWidth = `${Math.max(300, windowWidth - finalLeftOffset - 40)}px`; // 最低300px幅を確保
    
    console.log(`📍 ${parentSlotId} 位置調整詳細:`);
    console.log(`  - 親スロット中央: ${parentCenterX.toFixed(1)}px`);
    console.log(`  - サブスロット実測幅: ${actualSubslotWidth}px`);
    console.log(`  - 理想位置: ${idealLeftOffset.toFixed(1)}px`);
    console.log(`  - 最終位置: ${finalLeftOffset.toFixed(1)}px`);
    console.log(`  - 画面幅: ${windowWidth}px`);
    
  } catch (error) {
    console.warn(`⚠ サブスロット位置調整エラー: ${parentSlotId}`, error);
  }
}

/**
 * 📍 安全なサブスロット位置調整（軽微調整版）
 * サブスロットを消さずに最小限の位置調整のみ実行
 * @param {string} parentSlotId - 親スロットのID
 */
function adjustSubslotPositionSafe(parentSlotId) {
  // ⚡ ズーム中は位置調整をスキップ
  if (window.isZooming) {
    console.log(`⚡ ズーム中のため安全位置調整をスキップ: ${parentSlotId}`);
    return;
  }
  
  const parentSlot = document.getElementById(`slot-${parentSlotId}`);
  const subslotArea = document.getElementById(`slot-${parentSlotId}-sub`);
  
  if (!parentSlot || !subslotArea) {
    console.warn(`⚠ 安全位置調整: 必要な要素が見つかりません`);
    return;
  }
  
  // 🔍 現在の表示状態を確認
  if (getComputedStyle(subslotArea).display === 'none') {
    console.warn(`⚠ 安全位置調整: サブスロットが非表示状態のため調整をスキップ`);
    return;
  }
  
  try {
    console.log(`📍 ${parentSlotId} 安全な位置調整を開始`);
    
    // 各種サイズと位置を取得
    const parentRect = parentSlot.getBoundingClientRect();
    const containerRect = parentSlot.parentElement.getBoundingClientRect();
    const windowWidth = window.innerWidth;
    const subslotWidth = subslotArea.offsetWidth;
    
    if (!subslotWidth || subslotWidth === 0) {
      console.warn(`⚠ サブスロット幅が0のため位置調整をスキップ: ${parentSlotId}`);
      return;
    }
    
    // 親スロットの中央位置
    const parentCenterX = parentRect.left + (parentRect.width / 2);
    const containerLeft = containerRect.left;
    
    // 🎯 より積極的な位置調整：画面の80%の範囲で調整
    const screenCenter = windowWidth / 2;
    const distanceFromCenter = Math.abs(parentCenterX - screenCenter);
    const maxAdjustmentDistance = screenCenter * 0.8; // 画面中央80%の範囲で調整（60%→80%に拡大）
    
    if (distanceFromCenter > maxAdjustmentDistance) {
      console.log(`📍 ${parentSlotId} 画面端に近いが、軽微調整を試行`);
      // 完全にスキップせず、より控えめな調整を行う
    }
    
    // 理想位置の計算（中央揃え）
    const idealLeftOffset = parentCenterX - containerLeft - (subslotWidth / 2);
    
    // 安全な境界内での調整
    const minOffset = 10;
    const maxOffset = windowWidth - subslotWidth - 20;
    const safeLeftOffset = Math.max(minOffset, Math.min(idealLeftOffset, maxOffset));
    
    // 現在位置からの差分が小さい場合のチェックを緩和
    const currentLeft = parseInt(subslotArea.style.marginLeft) || 0;
    const adjustment = safeLeftOffset - currentLeft;
    
    if (Math.abs(adjustment) < 2) { // 5px→2pxに緩和してより調整しやすく
      console.log(`📍 ${parentSlotId} 調整量が非常に小さいためスキップ (${adjustment.toFixed(1)}px)`);
      return;
    }
    
    // 🎯 より大きな調整ステップを許可
    const maxAdjustmentStep = 100; // 50px→100pxに拡大してより調整しやすく
    const finalAdjustment = Math.sign(adjustment) * Math.min(Math.abs(adjustment), maxAdjustmentStep);
    const finalLeftOffset = currentLeft + finalAdjustment;
    
    // CSSを安全に適用（複数方法で確実に設定）
    subslotArea.style.marginLeft = `${finalLeftOffset}px`;
    subslotArea.style.setProperty('--dynamic-margin-left', `${finalLeftOffset}px`);
    subslotArea.style.setProperty('margin-left', `${finalLeftOffset}px`, 'important');
    
    // フォールバック：transformも併用
    if (finalLeftOffset > 0) {
      subslotArea.style.transform = `translateX(${finalLeftOffset}px)`;
    } else {
      subslotArea.style.transform = '';
    }
    
    console.log(`📍 ${parentSlotId} 軽微な位置調整完了:`);
    console.log(`  - 調整前: ${currentLeft}px → 調整後: ${finalLeftOffset}px`);
    console.log(`  - 調整量: ${finalAdjustment.toFixed(1)}px`);
    console.log(`  - 親スロット中央: ${parentCenterX.toFixed(1)}px`);
    console.log(`  - 理想位置: ${idealLeftOffset.toFixed(1)}px`);
    
  } catch (error) {
    console.warn(`⚠ 安全位置調整エラー: ${parentSlotId}`, error);
  }
}

/**
 * 🧹 全てのタブ連結スタイルをクリア
 */
function clearAllTabConnections() {
  // 🔗 上位スロットからタブ連結クラスを削除 + インラインスタイルをクリア
  const allParentSlots = document.querySelectorAll('.slot-container');
  allParentSlots.forEach(slot => {
    slot.classList.remove('active-parent-slot');
    // ブルータブのインラインスタイルを完全にクリア
    slot.style.removeProperty('background');
    slot.style.removeProperty('background-color');
    slot.style.removeProperty('border');
    slot.style.removeProperty('border-bottom');
    slot.style.removeProperty('border-radius');
    slot.style.removeProperty('box-shadow');
    slot.style.removeProperty('margin-bottom');
    slot.style.removeProperty('z-index');
    slot.style.removeProperty('position');
  });
  
  // 🔗 サブスロットエリアからタブ連結クラス + インラインスタイルを削除
  const allSubslotAreas = document.querySelectorAll('[id$="-sub"]');
  allSubslotAreas.forEach(area => {
    area.classList.remove('active-subslot-area');
    // ブルータブのインラインスタイルを完全にクリア
    area.style.removeProperty('background');
    area.style.removeProperty('background-color');
    area.style.removeProperty('border');
    area.style.removeProperty('border-top');
    area.style.removeProperty('border-radius');
    area.style.removeProperty('margin-top');
    area.style.removeProperty('box-shadow');
    area.style.removeProperty('padding');
    area.style.removeProperty('z-index');
    area.style.removeProperty('position');
  });
  
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
  
  console.log(`🧹 全てのタブ連結スタイル（インラインスタイル含む）をクリアしました`);
}

/**
 * 🔧 デバッグ用：位置調整のテスト関数
 * コンソールで手動実行して位置調整をテストできる
 */
window.testSubslotPosition = function(slotId) {
  console.log(`🔧 位置調整テスト開始: ${slotId}`);
  
  const parentSlot = document.getElementById(`slot-${slotId}`);
  const subslotArea = document.getElementById(`slot-${slotId}-sub`);
  
  if (!parentSlot || !subslotArea) {
    console.error(`❌ 要素が見つかりません: parent=${!!parentSlot}, subslot=${!!subslotArea}`);
    return;
  }
  
  console.log(`📊 現在の状態:`);
  console.log(`  - サブスロット表示: ${getComputedStyle(subslotArea).display}`);
  console.log(`  - 現在のmarginLeft: ${subslotArea.style.marginLeft}`);
  console.log(`  - 計算後のmarginLeft: ${getComputedStyle(subslotArea).marginLeft}`);
  console.log(`  - サブスロット幅: ${subslotArea.offsetWidth}px`);
  console.log(`  - 親スロット位置: ${parentSlot.getBoundingClientRect().left}px`);
  
  // 🎯 強制的に100px右に移動してテスト
  console.log(`🎯 テスト用に100px右に移動します`);
  subslotArea.style.marginLeft = '100px';
  subslotArea.style.setProperty('margin-left', '100px', 'important');
  subslotArea.style.transform = 'translateX(100px)';
  subslotArea.style.backgroundColor = 'yellow'; // 視覚的確認用
  
  setTimeout(() => {
    // 強制的に位置調整を実行
    adjustSubslotPositionSafe(slotId);
  }, 1000);
};

console.log(`🔧 デバッグ関数を登録しました: window.testSubslotPosition('スロットID')`);

/**
 * 🖱️ サブスロットに横スクロールドラッグ機能を追加
 * @param {HTMLElement} subslotWrapper - サブスロットWrapper要素 (slot-{id}-sub)
 */
function addHorizontalDragToSubslot(subslotWrapper) {
  if (!subslotWrapper || !subslotWrapper.id.endsWith('-sub')) {
    console.warn('⚠️ 横スクロールドラッグ：対象はサブスロットWrapper要素である必要があります');
    return;
  }
  
  console.log(`🖱️ 横スクロールドラッグ機能を追加中: ${subslotWrapper.id}`);
  
  // 既存のドラッグリスナーがあれば削除
  if (subslotWrapper._dragHandlers) {
    subslotWrapper.removeEventListener('mousedown', subslotWrapper._dragHandlers.mousedown);
    document.removeEventListener('mousemove', subslotWrapper._dragHandlers.mousemove);
    document.removeEventListener('mouseup', subslotWrapper._dragHandlers.mouseup);
    console.log('🖱️ 既存のドラッグハンドラーを削除しました');
  }
  
  let isDragging = false;
  let startX = 0;
  let scrollLeft = 0;
  
  const mouseDown = (e) => {
    isDragging = true;
    startX = e.pageX - subslotWrapper.offsetLeft;
    scrollLeft = subslotWrapper.scrollLeft;
    subslotWrapper.style.cursor = 'grabbing';
    console.log('🖱️ ドラッグ開始 - scrollLeft:', scrollLeft);
  };
  
  const mouseMove = (e) => {
    if (!isDragging) return;
    e.preventDefault();
    
    const x = e.pageX - subslotWrapper.offsetLeft;
    const walk = (x - startX) * 2; // スクロール感度調整
    subslotWrapper.scrollLeft = scrollLeft - walk;
    console.log('🖱️ ドラッグ中 - 新しいscrollLeft:', subslotWrapper.scrollLeft);
  };
  
  const mouseUp = () => {
    isDragging = false;
    subslotWrapper.style.cursor = 'grab';
    console.log('🖱️ ドラッグ終了');
  };
  
  // イベントリスナーを追加
  subslotWrapper.addEventListener('mousedown', mouseDown);
  document.addEventListener('mousemove', mouseMove);
  document.addEventListener('mouseup', mouseUp);
  
  // 後で削除できるように保存
  subslotWrapper._dragHandlers = {
    mousedown: mouseDown,
    mousemove: mouseMove,
    mouseup: mouseUp
  };
  
  // ドラッグ対応のスタイルを確認
  subslotWrapper.style.cursor = 'grab';
  subslotWrapper.classList.add('horizontal-drag-enabled');
  
  console.log(`✅ ${subslotWrapper.id} に横スクロールドラッグ機能を追加完了`);
}

/**
 * 🔄 全てのサブスロットに横スクロールドラッグ機能を適用
 */
function addHorizontalDragToAllSubslots() {
  const subslotWrappers = document.querySelectorAll('.slot-wrapper[id$="-sub"]');
  console.log(`🔄 ${subslotWrappers.length}個のサブスロットに横スクロールドラッグを適用します`);
  
  subslotWrappers.forEach(wrapper => {
    addHorizontalDragToSubslot(wrapper);
  });
}

// ページ読み込み完了時に横スクロールドラッグ機能を適用
document.addEventListener('DOMContentLoaded', () => {
  console.log('📖 DOMContentLoaded: 横スクロールドラッグ機能を初期化します');
  addHorizontalDragToAllSubslots();
});

// グローバル関数として公開
window.addHorizontalDragToSubslot = addHorizontalDragToSubslot;
window.addHorizontalDragToAllSubslots = addHorizontalDragToAllSubslots;
