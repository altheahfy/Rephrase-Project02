// O1とO2の比較デバッグ用スクリプト
// ブラウザのコンソールでテストするために使用

// O1とO2の現在状態を比較する関数
function compareO1AndO2() {
  console.log('🔍 ===== O1とO2の比較デバッグ =====');
  
  // O1スロットの状態確認
  console.log('\n🔍 O1スロットの状態:');
  const o1Slot = document.getElementById('slot-o1');
  if (o1Slot) {
    const o1Phrase = o1Slot.querySelector('.slot-phrase');
    const o1Text = o1Phrase ? o1Phrase.textContent.trim() : '';
    console.log('📝 O1テキスト:', o1Text);
    
    const o1MultiContainer = o1Slot.querySelector('.multi-image-container');
    if (o1MultiContainer) {
      const o1Images = o1MultiContainer.querySelectorAll('img');
      console.log(`🖼️ O1複数画像数: ${o1Images.length}`);
      o1Images.forEach((img, index) => {
        console.log(`  - O1画像${index + 1}: ${img.src.split('/').pop()}`);
      });
    } else {
      const o1SingleImage = o1Slot.querySelector('.slot-image');
      if (o1SingleImage) {
        console.log('🖼️ O1単一画像:', o1SingleImage.src.split('/').pop());
      }
    }
    
    // O1の複数画像検索テスト
    if (o1Text && typeof window.findAllImagesByMetaTag === 'function') {
      const o1Results = window.findAllImagesByMetaTag(o1Text);
      console.log('🔍 O1の複数画像検索結果:', o1Results.map(r => r.image_file));
    }
  }
  
  // O2スロットの状態確認
  console.log('\n🔍 O2スロットの状態:');
  const o2Slot = document.getElementById('slot-o2');
  if (o2Slot) {
    const o2Phrase = o2Slot.querySelector('.slot-phrase');
    const o2Text = o2Phrase ? o2Phrase.textContent.trim() : '';
    console.log('📝 O2テキスト:', o2Text);
    
    const o2MultiContainer = o2Slot.querySelector('.multi-image-container');
    if (o2MultiContainer) {
      const o2Images = o2MultiContainer.querySelectorAll('img');
      console.log(`🖼️ O2複数画像数: ${o2Images.length}`);
      o2Images.forEach((img, index) => {
        console.log(`  - O2画像${index + 1}: ${img.src.split('/').pop()}`);
      });
    } else {
      const o2SingleImage = o2Slot.querySelector('.slot-image');
      if (o2SingleImage) {
        console.log('🖼️ O2単一画像:', o2SingleImage.src.split('/').pop());
      }
    }
    
    // O2の複数画像検索テスト
    if (o2Text && typeof window.findAllImagesByMetaTag === 'function') {
      const o2Results = window.findAllImagesByMetaTag(o2Text);
      console.log('🔍 O2の複数画像検索結果:', o2Results.map(r => r.image_file));
    }
  }
  
  console.log('\n🔍 ===========================');
}

// 特定のテキストでO1とO2をテストする関数
function testO1AndO2WithText(testText) {
  console.log(`\n🧪 テスト文字列 "${testText}" でO1とO2を比較:`);
  
  // O1にテストテキストを適用
  console.log('🔍 O1への適用:');
  if (typeof window.applyMultipleImagesToSlot === 'function') {
    window.applyMultipleImagesToSlot('slot-o1', testText, true);
  }
  
  // O2にテストテキストを適用
  console.log('🔍 O2への適用:');
  if (typeof window.applyMultipleImagesToSlot === 'function') {
    window.applyMultipleImagesToSlot('slot-o2', testText, true);
  }
  
  // 結果を確認
  setTimeout(() => {
    console.log(`\n🔍 テスト結果 "${testText}":`);
    compareO1AndO2();
  }, 1000);
}

// 問題のテストケースを実行
function runProblemTests() {
  console.log('🚀 問題のテストケース実行');
  
  const problemCases = [
    "important message",
    "funny story",
    "some news"
  ];
  
  problemCases.forEach((testCase, index) => {
    setTimeout(() => {
      testO1AndO2WithText(testCase);
    }, index * 3000); // 3秒間隔で実行
  });
}

// コンソールから実行するための案内
console.log('🔧 O1とO2の比較デバッグ用関数を読み込みました');
console.log('💡 使用方法:');
console.log('  - compareO1AndO2() : 現在のO1とO2の状態比較');
console.log('  - testO1AndO2WithText("important message") : 特定テキストでテスト');
console.log('  - runProblemTests() : 問題のテストケース一括実行');
