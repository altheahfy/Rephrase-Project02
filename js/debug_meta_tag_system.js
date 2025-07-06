// メタタグシステムの詳細デバッグ関数
window.debugMetaTagSystem = function() {
  console.log("🔍 === メタタグシステム詳細デバッグ ===");
  
  // 1. メタタグデータの読み込み状態確認
  console.log("📋 メタタグデータ読み込み状態:", window.imageMetaTagsLoaded);
  console.log("📋 メタタグデータ:", window.imageMetaTagsData);
  
  // 2. スロット検索の確認
  console.log("\n🔍 === スロット検索テスト ===");
  const allSlots = document.querySelectorAll('.slot-container, .subslot-container');
  console.log("📊 検索されたスロット数:", allSlots.length);
  
  allSlots.forEach((slotElement, index) => {
    console.log(`\n📍 スロット${index + 1}:`, slotElement.id);
    console.log("  - 要素:", slotElement);
    
    const phraseElement = slotElement.querySelector('.slot-phrase');
    console.log("  - .slot-phrase要素:", phraseElement);
    
    if (phraseElement) {
      const phraseText = phraseElement.textContent.trim();
      console.log("  - テキスト:", `"${phraseText}"`);
      
      // メタタグマッチング確認
      if (window.findImageByMetaTag) {
        const imagePath = window.findImageByMetaTag(phraseText);
        console.log("  - マッチング結果:", imagePath || "なし");
      }
    }
    
    const imageElement = slotElement.querySelector('.slot-image');
    if (imageElement) {
      console.log("  - 画像要素:", imageElement);
      console.log("  - 現在のsrc:", imageElement.src);
      console.log("  - メタタグ属性:", imageElement.hasAttribute('data-meta-tag'));
    }
  });
  
  // 3. 特別にVスロットを確認
  console.log("\n🎯 === Vスロット特別確認 ===");
  const vSlot = document.getElementById('slot-v');
  if (vSlot) {
    console.log("✅ Vスロット発見:", vSlot.id);
    const vPhrase = vSlot.querySelector('.slot-phrase');
    if (vPhrase) {
      const vText = vPhrase.textContent.trim();
      console.log("📝 Vスロットテキスト:", `"${vText}"`);
      
      // "become"のマッチング確認
      if (window.findImageByMetaTag) {
        const vImagePath = window.findImageByMetaTag(vText);
        console.log("🔍 Vスロットマッチング:", vImagePath || "なし");
      }
    }
  } else {
    console.error("❌ Vスロットが見つかりません");
  }
  
  console.log("\n✅ === デバッグ完了 ===");
};

// 手動でVスロットにイラストを適用するテスト関数
window.testVSlotImageApply = function() {
  console.log("🧪 === Vスロットイラスト適用テスト ===");
  
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error("❌ Vスロットが見つかりません");
    return;
  }
  
  const vPhrase = vSlot.querySelector('.slot-phrase');
  if (!vPhrase) {
    console.error("❌ Vスロットのテキスト要素が見つかりません");
    return;
  }
  
  const vText = vPhrase.textContent.trim();
  console.log("📝 Vスロットテキスト:", `"${vText}"`);
  
  if (window.applyImageToSlot) {
    console.log("🎯 手動でイラスト適用を実行...");
    const result = window.applyImageToSlot(vSlot, vText, true);
    console.log("✅ 適用結果:", result);
  } else {
    console.error("❌ applyImageToSlot関数が見つかりません");
  }
};

console.log("🧪 メタタグシステムデバッグ関数が利用可能です:");
console.log("- debugMetaTagSystem() : 詳細システム解析");
console.log("- testVSlotImageApply() : Vスロット手動適用テスト");
