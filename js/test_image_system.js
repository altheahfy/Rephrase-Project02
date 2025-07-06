// イラスト表示機構テスト用関数
window.testImageDisplaySystem = function() {
  console.log("🧪 === イラスト表示機構テスト開始 ===");
  
  // 1. メタタグデータの読み込み状態確認
  console.log("📋 メタタグデータ読み込み状態:", window.imageMetaTagsLoaded);
  if (window.imageMetaTagsData) {
    console.log("📊 メタタグデータ件数:", window.imageMetaTagsData.length);
  }
  
  // 2. 各スロットの状態確認
  console.log("\n📍 各スロットの状態:");
  const allSlots = document.querySelectorAll('.slot-container');
  allSlots.forEach((slot, index) => {
    const phraseElement = slot.querySelector('.slot-phrase');
    const imageElement = slot.querySelector('.slot-image');
    const toggleButton = slot.querySelector('[data-subslot-toggle]');
    
    console.log(`\n🔍 スロット${index + 1} (${slot.id}):`);
    console.log(`  - テキスト: "${phraseElement ? phraseElement.textContent.trim() : 'なし'}"`);
    console.log(`  - 画像src: ${imageElement ? imageElement.src : 'なし'}`);
    console.log(`  - メタタグ: ${imageElement && imageElement.hasAttribute('data-meta-tag') ? 'あり' : 'なし'}`);
    console.log(`  - サブスロット: ${toggleButton ? 'あり' : 'なし'}`);
    if (toggleButton) {
      const hasContent = window.hasSubslotContent ? window.hasSubslotContent(slot) : false;
      console.log(`  - サブスロット内容: ${hasContent ? 'あり' : 'なし'}`);
    }
    console.log(`  - 表示状態: ${imageElement ? (imageElement.style.display === 'none' ? '非表示' : '表示') : 'なし'}`);
  });
  
  // 3. 画像統計
  console.log("\n📈 画像統計:");
  const allImages = document.querySelectorAll('.slot-image');
  let buttonImages = 0;
  let metaTagImages = 0;
  let placeholderImages = 0;
  let hiddenImages = 0;
  
  allImages.forEach(img => {
    if (img.src.includes('button.png')) buttonImages++;
    else if (img.hasAttribute('data-meta-tag')) metaTagImages++;
    else if (img.src.includes('placeholder.png')) placeholderImages++;
    
    if (img.classList.contains('auto-hidden-image') || img.style.display === 'none') {
      hiddenImages++;
    }
  });
  
  console.log(`  - 総画像数: ${allImages.length}`);
  console.log(`  - ボタン画像: ${buttonImages}`);
  console.log(`  - メタタグ画像: ${metaTagImages}`);
  console.log(`  - プレースホルダー画像: ${placeholderImages}`);
  console.log(`  - 非表示画像: ${hiddenImages}`);
  
  console.log("\n✅ === テスト完了 ===");
};

// 手動でイラスト表示を実行するテスト関数
window.testApplyMetaTagImages = function() {
  console.log("🧪 手動でイラスト表示を実行...");
  if (window.applyMetaTagImagesToAllSlots) {
    const count = window.applyMetaTagImagesToAllSlots(true);
    console.log(`✅ ${count}件のイラストが適用されました`);
  } else {
    console.log("❌ イラスト表示機構が読み込まれていません");
  }
};

// 共存テスト: 既存ロジックとの競合確認
window.testCoexistenceLogic = function() {
  console.log("🧪 === 共存ロジックテスト開始 ===");
  
  // 1. サブスロット付きスロットの確認
  const slotsWithSubslots = document.querySelectorAll('.slot-container:has([data-subslot-toggle])');
  console.log(`🔍 サブスロット付きスロット数: ${slotsWithSubslots.length}`);
  
  slotsWithSubslots.forEach((slot, index) => {
    const imageElement = slot.querySelector('.slot-image');
    const phraseElement = slot.querySelector('.slot-phrase');
    const hasContent = window.hasSubslotContent ? window.hasSubslotContent(slot) : false;
    
    console.log(`\n📍 サブスロット付きスロット${index + 1}:`);
    console.log(`  - ID: ${slot.id}`);
    console.log(`  - テキスト: "${phraseElement ? phraseElement.textContent.trim() : 'なし'}"`);
    console.log(`  - サブスロット内容: ${hasContent ? 'あり' : 'なし'}`);
    console.log(`  - 画像: ${imageElement ? imageElement.src : 'なし'}`);
    console.log(`  - ボタン画像: ${imageElement && imageElement.src.includes('button.png') ? 'あり' : 'なし'}`);
    console.log(`  - メタタグ: ${imageElement && imageElement.hasAttribute('data-meta-tag') ? 'あり' : 'なし'}`);
    
    if (hasContent) {
      if (imageElement && !imageElement.src.includes('button.png') && imageElement.hasAttribute('data-meta-tag')) {
        console.log("⚠️ 警告: サブスロット内容ありなのにボタン画像がメタタグで上書きされている");
      }
    } else {
      if (imageElement && imageElement.src.includes('button.png')) {
        console.log("⚠️ 警告: サブスロット内容なしなのにボタン画像が表示されている");
      }
    }
  });
  
  // 2. 空スロットの確認
  const emptySlots = [];
  document.querySelectorAll('.slot-container').forEach(slot => {
    const phraseElement = slot.querySelector('.slot-phrase');
    if (!phraseElement || !phraseElement.textContent.trim()) {
      emptySlots.push(slot);
    }
  });
  
  console.log(`\n🔍 空スロット数: ${emptySlots.length}`);
  emptySlots.forEach((slot, index) => {
    const imageElement = slot.querySelector('.slot-image');
    console.log(`  - 空スロット${index + 1}: ${slot.id}, 画像表示: ${imageElement && imageElement.style.display !== 'none' ? '表示' : '非表示'}`);
  });
  
  console.log("\n✅ === 共存ロジックテスト完了 ===");
};

console.log("🧪 テスト関数が利用可能です:");
console.log("- testImageDisplaySystem() : 全体状態確認");
console.log("- testApplyMetaTagImages() : 手動イラスト適用");
console.log("- testCoexistenceLogic() : 共存ロジック確認");
