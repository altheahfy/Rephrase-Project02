// O2スロット画像表示問題のデバッグ用スクリプト
// ブラウザのコンソールでテストするために使用

// テスト用関数: 複数画像検索のデバッグ
function debugO2SlotImages() {
  console.log('🔍 O2スロット画像表示問題のデバッグ開始');
  
  const testCases = [
    "important message",
    "funny story", 
    "some news"
  ];
  
  testCases.forEach(testCase => {
    console.log(`\n===== テストケース: "${testCase}" =====`);
    
    // 複数画像検索の結果を確認
    const results = window.findAllImagesByMetaTag(testCase);
    console.log(`🔍 複数画像検索結果:`, results);
    
    // 個別単語の確認
    const individualWords = testCase.toLowerCase().split(/\s+/).filter(word => word.length >= 2);
    console.log(`🔍 個別単語:`, individualWords);
    
    // 各単語の検索結果を確認
    individualWords.forEach(word => {
      const wordResult = window.findImageByMetaTag(word);
      console.log(`  - "${word}" → ${wordResult ? wordResult.image_file : 'なし'}`);
    });
    
    // 実際にO2スロットに適用してみる
    console.log(`🖼️ O2スロットに適用テスト:`);
    if (typeof window.applyMultipleImagesToSlot === 'function') {
      window.applyMultipleImagesToSlot('slot-o2', testCase, true);
    }
  });
}

// メタタグデータを確認する関数
function checkMetaTagData() {
  console.log('🔍 メタタグデータの確認');
  
  const targetWords = ['important', 'message', 'funny', 'story', 'some', 'news'];
  
  targetWords.forEach(word => {
    const matches = window.imageMetaTags.filter(item => 
      item.meta_tags.some(tag => tag.toLowerCase() === word.toLowerCase())
    );
    console.log(`"${word}" にマッチするメタタグ:`, matches);
  });
}

// O2スロットの現在の状態を確認
function checkO2SlotState() {
  console.log('🔍 O2スロットの現在の状態');
  
  const o2Slot = document.getElementById('slot-o2');
  if (!o2Slot) {
    console.log('❌ O2スロットが見つかりません');
    return;
  }
  
  const phraseElement = o2Slot.querySelector('.slot-phrase');
  const imageElement = o2Slot.querySelector('.slot-image');
  const multiImageContainer = o2Slot.querySelector('.multi-image-container');
  
  console.log('📝 現在のテキスト:', phraseElement ? phraseElement.textContent : 'なし');
  console.log('🖼️ 単一画像src:', imageElement ? imageElement.src : 'なし');
  console.log('🖼️ 複数画像コンテナ:', multiImageContainer ? '存在' : '不存在');
  
  if (multiImageContainer) {
    const images = multiImageContainer.querySelectorAll('img');
    console.log(`🖼️ 複数画像数: ${images.length}`);
    images.forEach((img, index) => {
      console.log(`  - 画像${index + 1}: ${img.src}`);
    });
  }
}

// 実行用の統合関数
function runO2SlotDebug() {
  console.log('🚀 O2スロット画像表示問題のデバッグ実行');
  
  // 1. メタタグデータの確認
  checkMetaTagData();
  
  // 2. 現在の状態確認
  checkO2SlotState();
  
  // 3. 画像表示テスト
  debugO2SlotImages();
}

// コンソールから実行するための案内
console.log('🔧 O2スロット画像表示問題のデバッグ用関数を読み込みました');
console.log('💡 使用方法:');
console.log('  - runO2SlotDebug() : 全体的なデバッグ実行');
console.log('  - checkMetaTagData() : メタタグデータの確認');
console.log('  - checkO2SlotState() : O2スロットの現在状態確認');
console.log('  - debugO2SlotImages() : 画像表示テスト');
