/* =======================================// 🔝 PC版上位スロットのクローンを上画面に表示（PC版は保護）
function cloneUpperSlotsToUpperArea() {
  const upperArea = document.querySelector('.upper-slot-area');
  const mainSlotWrapper = document.querySelector('.slot-wrapper');
  
  if (!upperArea || !mainSlotWrapper) {
    console.warn("⚠ 上画面またはslot-wrapperが見つかりません");
    return;
  }
  
  // PC版の完全なクローンを作成（スタイルと構造を保持）
  const clonedWrapper = mainSlotWrapper.cloneNode(true);
  clonedWrapper.classList.add('mobile-slot-clone');
  
  // 上画面に追加
  upperArea.appendChild(clonedWrapper);
  
  console.log("🔝 PC版上位スロットクローンを上画面に表示（PC版完全保護）");
}============ */
/* 📱 モバイル上下2分割レイアウト動的調整システム                      */
/* =================================================================== */
/* PC版完全保護 + クローン表示方式 */

// モバイル検出時に上下分割コンテナを自動生成してPC版をクローン表示
function initializeMobileSplitView() {
  if (!document.documentElement.classList.contains('mobile-device')) {
    console.log("💻 PC版: 上下分割システムをスキップ");
    return;
  }
  
  console.log("📱 モバイル上下2分割システム初期化開始");
  
  // 🔝 上画面コンテナを作成
  const upperArea = document.createElement('div');
  upperArea.className = 'upper-slot-area';
  upperArea.innerHTML = '<div class="area-label">📝 英語構造</div>';
  
  // 🔽 下画面コンテナを作成  
  const lowerArea = document.createElement('div');
  lowerArea.className = 'lower-subslot-area';
  lowerArea.innerHTML = '<div class="area-label">🔍 詳細表示</div>';
  
  // 📍 分割インジケーターを作成
  const divider = document.createElement('div');
  divider.className = 'area-divider';
  
  // body に追加
  document.body.appendChild(upperArea);
  document.body.appendChild(lowerArea);
  document.body.appendChild(divider);
  
  // 🔒 PC版コンテンツのクローンを上画面に表示
  cloneUpperSlotsToUpperArea();
  
  // 🔒 サブスロットコンテンツの動的クローン設定
  setupSubslotAreaControl();
  
  console.log("✅ モバイル上下2分割システム初期化完了");
}

// 🔝 上位スロットを上画面に移動（PC版完全保護）
function moveUpperSlotsToUpperArea() {
  const upperArea = document.querySelector('.upper-slot-area');
  const mainSlotWrapper = document.querySelector('.slot-wrapper:not([id$="-sub"])');
  
  if (!upperArea || !mainSlotWrapper) {
    console.warn("⚠ 上画面移動: 必要な要素が見つかりません");
    return;
  }
  
  // PC版のslot-wrapperをそのまま上画面に移動
  // 内部の制御システムは一切変更しない
  upperArea.appendChild(mainSlotWrapper);
  
  console.log("🔝 上位スロットを上画面に移動（PC版完全保護）");
}

// 🔽 サブスロット表示制御（下画面自動切り替え）
function setupSubslotAreaControl() {
  const lowerArea = document.querySelector('.lower-subslot-area');
  if (!lowerArea) return;
  
  // サブスロット展開ボタンの監視
  document.addEventListener('click', function(event) {
    const button = event.target.closest('[data-subslot-toggle]');
    if (!button) return;
    
    const slotType = button.getAttribute('data-subslot-toggle');
    const subslotContainer = document.getElementById(`slot-${slotType}-sub`);
    
    if (!subslotContainer) return;
    
    // 現在の表示状態を確認
    const isVisible = window.getComputedStyle(subslotContainer).display !== 'none';
    
    if (isVisible) {
      // サブスロットが表示された場合、下画面にクローンを表示
      cloneSubslotToLowerArea(subslotContainer, slotType);
    } else {
      // サブスロットが非表示になった場合、下画面をクリア
      clearLowerArea();
    }
  });
  
  console.log("🔽 サブスロット下画面制御を設定");
}

// 📦 特定のサブスロットのクローンを下画面に表示
function cloneSubslotToLowerArea(subslotContainer, slotType) {
  const lowerArea = document.querySelector('.lower-subslot-area');
  if (!lowerArea || !subslotContainer) return;
  
  // 下画面をクリアして新しいサブスロットクローンを配置
  const existingLabel = lowerArea.querySelector('.area-label');
  lowerArea.innerHTML = '';
  
  if (existingLabel) {
    lowerArea.appendChild(existingLabel);
  }
  
  // PC版サブスロットの完全なクローンを作成
  const clonedSubslot = subslotContainer.cloneNode(true);
  clonedSubslot.classList.add('mobile-slot-clone');
  clonedSubslot.id = `mobile-${subslotContainer.id}`; // ID重複を避ける
  
  // 下画面に追加
  lowerArea.appendChild(clonedSubslot);
  
  console.log(`📦 ${slotType}サブスロットクローンを下画面に表示`);
}

// 🧹 下画面をクリア
function clearLowerArea() {
  const lowerArea = document.querySelector('.lower-subslot-area');
  if (!lowerArea) return;
  
  lowerArea.innerHTML = '<div class="area-label">🔍 詳細表示</div>';
  
  console.log("🧹 下画面をクリア");
}

// 📱 モバイル検出時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  // モバイル検出後に初期化
  setTimeout(() => {
    if (document.documentElement.classList.contains('mobile-device')) {
      initializeMobileSplitView();
    }
  }, 100);
});

// 🔄 ランダマイズ後の再配置
window.addEventListener('randomize-complete', function() {
  if (document.documentElement.classList.contains('mobile-device')) {
    // PC版システムは保護、クローンの再作成のみ
    cloneUpperSlotsToUpperArea();
  }
});
