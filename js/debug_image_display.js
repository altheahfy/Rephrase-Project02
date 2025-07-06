// 画像適用後の状態確認関数
window.checkVSlotAfterApply = function() {
  console.log("🔍 === 画像適用後のVスロット状態確認 ===");
  
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error("❌ Vスロットが見つかりません");
    return;
  }
  
  const imageElement = vSlot.querySelector('.slot-image');
  if (!imageElement) {
    console.error("❌ 画像要素が見つかりません");
    return;
  }
  
  console.log("📍 画像要素の詳細:");
  console.log("  - src:", imageElement.src);
  console.log("  - alt:", imageElement.alt);
  console.log("  - classList:", Array.from(imageElement.classList).join(', '));
  console.log("  - style.display:", imageElement.style.display);
  console.log("  - style.visibility:", imageElement.style.visibility);
  console.log("  - style.opacity:", imageElement.style.opacity);
  console.log("  - naturalWidth:", imageElement.naturalWidth);
  console.log("  - naturalHeight:", imageElement.naturalHeight);
  console.log("  - complete:", imageElement.complete);
  console.log("  - data-meta-tag:", imageElement.getAttribute('data-meta-tag'));
  console.log("  - data-meta-tag-applied:", imageElement.getAttribute('data-meta-tag-applied'));
  console.log("  - data-applied-text:", imageElement.getAttribute('data-applied-text'));
  
  // auto-hidden-image クラスが付いているかチェック
  if (imageElement.classList.contains('auto-hidden-image')) {
    console.log("⚠️ 警告: auto-hidden-image クラスが付いています");
    console.log("  - これが原因で画像が非表示になっている可能性があります");
  }
  
  // CSSで非表示になっているかチェック
  const computedStyle = window.getComputedStyle(imageElement);
  console.log("📋 計算されたスタイル:");
  console.log("  - display:", computedStyle.display);
  console.log("  - visibility:", computedStyle.visibility);
  console.log("  - opacity:", computedStyle.opacity);
  
  console.log("\n✅ === 状態確認完了 ===");
};

// 画像を強制的に表示する関数
window.forceShowVSlotImage = function() {
  console.log("💪 === Vスロット画像を強制表示 ===");
  
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error("❌ Vスロットが見つかりません");
    return;
  }
  
  const imageElement = vSlot.querySelector('.slot-image');
  if (!imageElement) {
    console.error("❌ 画像要素が見つかりません");
    return;
  }
  
  // auto-hidden-image クラスを削除
  imageElement.classList.remove('auto-hidden-image');
  
  // 表示スタイルを強制設定
  imageElement.style.display = 'block';
  imageElement.style.visibility = 'visible';
  imageElement.style.opacity = '1';
  
  console.log("✅ 強制表示設定完了");
  console.log("  - 現在のsrc:", imageElement.src);
};

console.log("🧪 画像適用後確認関数が利用可能です:");
console.log("- checkVSlotAfterApply() : 適用後状態確認");
console.log("- forceShowVSlotImage() : 強制表示");
