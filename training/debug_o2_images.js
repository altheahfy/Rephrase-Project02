// O2スロットの画像表示問題を診断するためのデバッグスクリプト

// 🔍 O2スロットの画像表示問題を診断する関数
function debugO2ImageIssue() {
  console.log('🔍 O2スロット画像表示問題の診断開始');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  // 1. O2スロットの基本情報を確認
  const o2Slot = document.getElementById('slot-o2');
  if (!o2Slot) {
    console.error('❌ O2スロットが見つかりません');
    return;
  }
  
  const o2PhraseElement = o2Slot.querySelector('.slot-phrase');
  const o2ImageElement = o2Slot.querySelector('.slot-image');
  const o2MultiImageContainer = o2Slot.querySelector('.multi-image-container');
  
  const currentText = o2PhraseElement ? o2PhraseElement.textContent.trim() : '';
  
  console.log('📋 O2スロット基本情報:');
  console.log('  - テキスト:', currentText);
  console.log('  - 画像要素:', o2ImageElement ? '存在' : '不存在');
  console.log('  - 複数画像コンテナ:', o2MultiImageContainer ? '存在' : '不存在');
  
  if (o2ImageElement) {
    console.log('  - 単一画像src:', o2ImageElement.src);
    console.log('  - 単一画像display:', o2ImageElement.style.display);
    console.log('  - 単一画像visibility:', o2ImageElement.style.visibility);
    console.log('  - 単一画像opacity:', o2ImageElement.style.opacity);
    console.log('  - 単一画像classes:', Array.from(o2ImageElement.classList));
  }
  
  if (o2MultiImageContainer) {
    console.log('  - 複数画像コンテナdisplay:', o2MultiImageContainer.style.display);
    console.log('  - 複数画像コンテナ内の画像数:', o2MultiImageContainer.querySelectorAll('img').length);
    
    const multiImages = o2MultiImageContainer.querySelectorAll('img');
    multiImages.forEach((img, index) => {
      console.log(`    画像${index + 1}: ${img.src}`);
      console.log(`      display: ${img.style.display}`);
      console.log(`      visibility: ${img.style.visibility}`);
      console.log(`      opacity: ${img.style.opacity}`);
    });
  }
  
  // 2. メタタグデータの確認
  console.log('\n📊 メタタグデータ確認:');
  console.log('  - imageMetaTags配列:', window.imageMetaTags ? window.imageMetaTags.length + '件' : '未読み込み');
  
  if (window.imageMetaTags && window.imageMetaTags.length > 0) {
    // funnyとstoryの定義を確認
    const funnyImage = window.imageMetaTags.find(img => img.meta_tags.includes('funny'));
    const storyImage = window.imageMetaTags.find(img => img.meta_tags.includes('story'));
    
    console.log('  - funny画像定義:', funnyImage ? funnyImage.image_file : '未定義');
    console.log('  - story画像定義:', storyImage ? storyImage.image_file : '未定義');
    
    if (funnyImage) {
      console.log('    funny詳細:', funnyImage);
    }
    if (storyImage) {
      console.log('    story詳細:', storyImage);
    }
  }
  
  // 3. 複数画像検索のテスト
  console.log('\n🔍 複数画像検索テスト:');
  if (typeof window.findAllImagesByMetaTag === 'function') {
    const testResults = window.findAllImagesByMetaTag('a funny story');
    console.log('  - "a funny story"の検索結果:', testResults);
    console.log('  - 検索結果数:', testResults.length);
    
    testResults.forEach((result, index) => {
      console.log(`    ${index + 1}. ${result.image_file} (${result.folder})`);
    });
    
    // 個別単語でもテスト
    const funnyResults = window.findAllImagesByMetaTag('funny');
    console.log('  - "funny"の検索結果:', funnyResults);
    
    const storyResults = window.findAllImagesByMetaTag('story');
    console.log('  - "story"の検索結果:', storyResults);
  } else {
    console.error('❌ findAllImagesByMetaTag関数が見つかりません');
  }
  
  // 4. 画像適用のテスト
  console.log('\n🎯 画像適用テスト:');
  if (typeof window.applyMultipleImagesToSlot === 'function') {
    console.log('  - applyMultipleImagesToSlot関数: 存在');
    console.log('  - 手動で画像適用を試行します...');
    
    // 手動で画像適用を実行
    window.applyMultipleImagesToSlot('slot-o2', 'a funny story', true);
    
    // 実行後の状態を確認
    setTimeout(() => {
      const updatedMultiContainer = o2Slot.querySelector('.multi-image-container');
      console.log('  - 適用後の複数画像コンテナ:', updatedMultiContainer ? '存在' : '不存在');
      
      if (updatedMultiContainer) {
        const images = updatedMultiContainer.querySelectorAll('img');
        console.log('  - 適用後の画像数:', images.length);
        
        images.forEach((img, index) => {
          console.log(`    画像${index + 1}: ${img.src}`);
          console.log(`      alt: ${img.alt}`);
          console.log(`      display: ${img.style.display}`);
          console.log(`      visibility: ${img.style.visibility}`);
          console.log(`      opacity: ${img.style.opacity}`);
          console.log(`      onload: ${img.onload ? 'あり' : 'なし'}`);
        });
      } else {
        // 単一画像を確認
        const singleImg = o2Slot.querySelector('.slot-image');
        if (singleImg) {
          console.log('  - 単一画像に戻った:', singleImg.src);
        }
      }
    }, 1000);
  } else {
    console.error('❌ applyMultipleImagesToSlot関数が見つかりません');
  }
  
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🔍 O2スロット画像表示問題の診断完了');
}

// 🔧 強制的にO2スロットに画像を適用する関数
function forceApplyO2Images() {
  console.log('🔧 O2スロットに強制的に画像を適用します');
  
  const o2Slot = document.getElementById('slot-o2');
  if (!o2Slot) {
    console.error('❌ O2スロットが見つかりません');
    return;
  }
  
  const o2PhraseElement = o2Slot.querySelector('.slot-phrase');
  const currentText = o2PhraseElement ? o2PhraseElement.textContent.trim() : '';
  
  if (!currentText) {
    console.error('❌ O2スロットにテキストがありません');
    return;
  }
  
  console.log('🎯 現在のテキスト:', currentText);
  
  // 複数画像適用を強制実行
  if (typeof window.applyMultipleImagesToSlot === 'function') {
    window.applyMultipleImagesToSlot('slot-o2', currentText, true);
    console.log('✅ 複数画像適用を実行しました');
  } else {
    console.error('❌ applyMultipleImagesToSlot関数が見つかりません');
  }
}

// 🔄 全スロットの画像を強制更新する関数
function forceUpdateAllImages() {
  console.log('🔄 全スロットの画像を強制更新します');
  
  if (typeof window.updateAllSlotImages === 'function') {
    window.updateAllSlotImages(true);
    console.log('✅ 全スロット画像更新を実行しました');
  } else {
    console.error('❌ updateAllSlotImages関数が見つかりません');
  }
}

// 🔍 画像ファイルの存在確認テスト
function testImageFileExistence() {
  console.log('🔍 画像ファイルの存在確認テスト');
  
  const testImages = [
    'slot_images/common/funny.png',
    'slot_images/common/story.png'
  ];
  
  testImages.forEach((imagePath, index) => {
    const img = new Image();
    img.onload = function() {
      console.log(`✅ 画像${index + 1} 存在確認: ${imagePath}`);
    };
    img.onerror = function() {
      console.error(`❌ 画像${index + 1} 存在しない: ${imagePath}`);
    };
    img.src = imagePath + '?t=' + Date.now();
  });
}

// 🔍 システム全体の状態確認
function checkSystemStatus() {
  console.log('🔍 システム全体の状態確認');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  // 重要な関数の存在確認
  const functions = [
    'window.imageMetaTags',
    'window.findAllImagesByMetaTag',
    'window.applyMultipleImagesToSlot',
    'window.updateSlotImage',
    'window.updateAllSlotImages',
    'window.initializeUniversalImageSystem'
  ];
  
  console.log('📋 重要な関数の存在確認:');
  functions.forEach(func => {
    const exists = eval(`typeof ${func} !== 'undefined'`);
    console.log(`  ${exists ? '✅' : '❌'} ${func}: ${exists ? '存在' : '不存在'}`);
  });
  
  // DOM要素の確認
  const o2Slot = document.getElementById('slot-o2');
  if (o2Slot) {
    console.log('📋 O2スロットDOM構造:');
    console.log('  - .slot-phrase:', o2Slot.querySelector('.slot-phrase') ? '存在' : '不存在');
    console.log('  - .slot-image:', o2Slot.querySelector('.slot-image') ? '存在' : '不存在');
    console.log('  - .slot-text:', o2Slot.querySelector('.slot-text') ? '存在' : '不存在');
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
}

// グローバルに公開
window.debugO2ImageIssue = debugO2ImageIssue;
window.forceApplyO2Images = forceApplyO2Images;
window.forceUpdateAllImages = forceUpdateAllImages;
window.testImageFileExistence = testImageFileExistence;
window.checkSystemStatus = checkSystemStatus;

console.log('🎯 O2画像デバッグ関数を読み込みました');
console.log('使用方法:');
console.log('  - debugO2ImageIssue()        : 問題を診断');
console.log('  - forceApplyO2Images()       : O2スロットに強制的に画像適用');
console.log('  - forceUpdateAllImages()     : 全スロット画像の強制更新');
console.log('  - testImageFileExistence()   : 画像ファイルの存在確認');
console.log('  - checkSystemStatus()        : システム全体の状態確認');
