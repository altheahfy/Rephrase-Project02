// Vスロット専用イラスト表示テスト関数
window.testVSlotImage = function() {
  console.log("🧪 === Vスロット イラスト表示テスト ===");
  
  // メタタグデータの読み込み状況確認
  console.log("📋 メタタグデータ読み込み状況:");
  console.log("  - imageMetaTagsLoaded:", window.imageMetaTagsLoaded);
  console.log("  - imageMetaTagsData:", window.imageMetaTagsData ? `${window.imageMetaTagsData.length}件` : 'なし');
  
  // Vスロットの要素取得
  const vSlot = document.getElementById('slot-v');
  const phraseElement = vSlot.querySelector('.slot-phrase');
  const imageElement = vSlot.querySelector('.slot-image');
  
  console.log("\n🔍 現在の状態:");
  console.log("  - テキスト:", phraseElement.textContent);
  console.log("  - 画像src:", imageElement.src);
  console.log("  - 画像クラス:", Array.from(imageElement.classList).join(', '));
  
  // 手動でマッチング処理を実行
  if (window.findImageByMetaTag) {
    const matchResult = window.findImageByMetaTag(phraseElement.textContent);
    console.log("\n🎯 マッチング結果:");
    console.log("  - マッチした画像:", matchResult || 'なし');
    
    if (matchResult) {
      console.log("  - 画像適用を実行中...");
      imageElement.src = matchResult;
      imageElement.setAttribute('data-meta-tag', 'true');
      imageElement.classList.remove('auto-hidden-image');
      imageElement.style.display = 'block';
      console.log("  - 画像適用完了:", matchResult);
    }
  } else {
    console.error("❌ findImageByMetaTag 関数が見つかりません");
  }
  
  // メタタグシステムの全体実行
  if (window.applyMetaTagImagesToAllSlots) {
    console.log("\n🔄 メタタグシステム全体実行...");
    const count = window.applyMetaTagImagesToAllSlots(true);
    console.log(`  - 適用件数: ${count}件`);
  }
  
  console.log("\n✅ === テスト完了 ===");
};

// メタタグデータを強制再読み込み
window.forceReloadMetaTags = async function() {
  console.log("🔄 メタタグデータ強制再読み込み...");
  
  if (window.loadImageMetaTagsOnStartup) {
    const success = await window.loadImageMetaTagsOnStartup();
    console.log(`  - 再読み込み結果: ${success ? '成功' : '失敗'}`);
    
    if (success) {
      console.log("  - データ件数:", window.imageMetaTagsData.length);
      // テスト用にbecomeを検索
      const becomeEntry = window.imageMetaTagsData.find(entry => 
        entry.meta_tags.includes('become')
      );
      console.log("  - 'become'エントリ:", becomeEntry || 'なし');
    }
  }
};

console.log("🧪 Vスロット専用テスト関数が利用可能です:");
console.log("- testVSlotImage() : Vスロットのイラスト表示テスト");
console.log("- forceReloadMetaTags() : メタタグデータの強制再読み込み");
