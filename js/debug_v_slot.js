// Vスロット専用デバッグ関数
window.debugVSlot = function() {
  console.log("🔍 === Vスロット詳細解析 ===");
  
  // Vスロットの要素を取得
  const vSlot = document.getElementById('slot-v');
  
  if (!vSlot) {
    console.error("❌ Vスロットが見つかりません");
    return;
  }
  
  console.log("📍 Vスロット要素:", vSlot);
  console.log("📍 Vスロット HTML:", vSlot.outerHTML);
  
  // 各子要素の状態確認
  const label = vSlot.querySelector('label');
  const image = vSlot.querySelector('.slot-image');
  const text = vSlot.querySelector('.slot-text');
  const phrase = vSlot.querySelector('.slot-phrase');
  
  console.log("\n🔍 === 子要素解析 ===");
  console.log("📌 ラベル:", label ? label.textContent : 'なし');
  console.log("📌 画像要素:", image);
  if (image) {
    console.log("  - src:", image.src);
    console.log("  - alt:", image.alt);
    console.log("  - classList:", Array.from(image.classList).join(', '));
    console.log("  - style.display:", image.style.display);
    console.log("  - naturalWidth:", image.naturalWidth);
    console.log("  - naturalHeight:", image.naturalHeight);
    console.log("  - complete:", image.complete);
  }
  
  console.log("📌 補助テキスト:", text);
  if (text) {
    console.log("  - textContent:", `"${text.textContent}"`);
    console.log("  - innerHTML:", `"${text.innerHTML}"`);
  }
  
  console.log("📌 例文テキスト:", phrase);
  if (phrase) {
    console.log("  - textContent:", `"${phrase.textContent}"`);
    console.log("  - innerHTML:", `"${phrase.innerHTML}"`);
  }
  
  // サブスロット確認
  const subslots = vSlot.querySelectorAll('.subslot-container');
  console.log("📌 サブスロット数:", subslots.length);
  
  console.log("\n✅ === Vスロット解析完了 ===");
};

console.log("🧪 Vスロット専用デバッグ関数が利用可能です:");
console.log("- debugVSlot() : Vスロットの詳細解析");
