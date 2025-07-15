// O2スロットの複数画像表示を修正するスクリプト

// 🔧 O2スロットの複数画像表示を修正する関数
function fixO2MultipleImages() {
  console.log('🔧 O2スロットの複数画像表示を修正します');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  // 1. 現在の状態を確認
  const o2Slot = document.getElementById('slot-o2');
  if (!o2Slot) {
    console.error('❌ O2スロットが見つかりません');
    return;
  }
  
  const o2PhraseElement = o2Slot.querySelector('.slot-phrase');
  const currentText = o2PhraseElement ? o2PhraseElement.textContent.trim() : '';
  
  console.log('📋 現在の状態:');
  console.log('  - O2テキスト:', currentText);
  console.log('  - 複数画像コンテナ:', o2Slot.querySelector('.multi-image-container') ? '存在' : '不存在');
  console.log('  - 単一画像src:', o2Slot.querySelector('.slot-image')?.src || 'なし');
  
  // 2. 複数画像を強制適用
  if (currentText && typeof window.applyMultipleImagesToSlot === 'function') {
    console.log('🎯 複数画像を強制適用します...');
    window.applyMultipleImagesToSlot('slot-o2', currentText, true);
    
    // 適用後の状態を確認
    setTimeout(() => {
      const multiContainer = o2Slot.querySelector('.multi-image-container');
      if (multiContainer) {
        const images = multiContainer.querySelectorAll('img');
        console.log('✅ 修正完了 - 複数画像コンテナ作成');
        console.log('  - 画像数:', images.length);
        images.forEach((img, index) => {
          console.log(`  - 画像${index + 1}: ${img.src.split('/').pop()}`);
        });
      } else {
        console.log('⚠️ 複数画像コンテナが作成されませんでした');
      }
    }, 500);
  } else {
    console.error('❌ 複数画像適用関数が見つからないか、テキストが空です');
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
}

// 🔄 自動的にO2スロットを監視して修正する関数
function setupO2AutoFix() {
  console.log('🔄 O2スロットの自動修正システムを開始します');
  
  // 5秒ごとにO2スロットの状態をチェック
  const checkInterval = setInterval(() => {
    const o2Slot = document.getElementById('slot-o2');
    if (!o2Slot) return;
    
    const o2PhraseElement = o2Slot.querySelector('.slot-phrase');
    const currentText = o2PhraseElement ? o2PhraseElement.textContent.trim() : '';
    const multiContainer = o2Slot.querySelector('.multi-image-container');
    
    // 「a funny story」のテキストがあるが複数画像コンテナがない場合
    if (currentText && currentText.includes('funny') && currentText.includes('story') && !multiContainer) {
      console.log('⚠️ O2スロットで複数画像が表示されていません - 自動修正を実行');
      fixO2MultipleImages();
    }
  }, 5000);
  
  // 30秒後に監視を停止
  setTimeout(() => {
    clearInterval(checkInterval);
    console.log('🛑 O2スロット自動修正システムを停止しました');
  }, 30000);
}

// 🚀 今すぐ修正を実行する関数
function quickFixO2() {
  console.log('🚀 O2スロットの即座修正を実行します');
  
  // 1. 現在の画像システムを初期化
  if (typeof window.updateAllSlotImages === 'function') {
    window.updateAllSlotImages(true);
    console.log('✅ 全スロット画像を更新しました');
  }
  
  // 2. 500ms後にO2スロットを特別に処理
  setTimeout(() => {
    fixO2MultipleImages();
  }, 500);
  
  // 3. 自動監視システムを開始
  setTimeout(() => {
    setupO2AutoFix();
  }, 1000);
}

// 🔍 O2スロットの詳細な状態を確認する関数
function checkO2Status() {
  console.log('🔍 O2スロットの詳細状態確認');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  const o2Slot = document.getElementById('slot-o2');
  if (!o2Slot) {
    console.error('❌ O2スロットが見つかりません');
    return;
  }
  
  const phraseElement = o2Slot.querySelector('.slot-phrase');
  const imageElement = o2Slot.querySelector('.slot-image');
  const multiContainer = o2Slot.querySelector('.multi-image-container');
  
  console.log('📋 O2スロット詳細状態:');
  console.log('  - テキスト:', phraseElement?.textContent?.trim() || '空');
  console.log('  - 単一画像:', imageElement ? 'あり' : 'なし');
  console.log('  - 複数画像コンテナ:', multiContainer ? 'あり' : 'なし');
  
  if (imageElement) {
    console.log('  - 単一画像src:', imageElement.src);
    console.log('  - 単一画像display:', imageElement.style.display || 'デフォルト');
    console.log('  - 単一画像visibility:', imageElement.style.visibility || 'デフォルト');
  }
  
  if (multiContainer) {
    const images = multiContainer.querySelectorAll('img');
    console.log('  - 複数画像数:', images.length);
    images.forEach((img, index) => {
      console.log(`    画像${index + 1}: ${img.src.split('/').pop()}`);
    });
  }
  
  // テキストから期待される画像を確認
  const currentText = phraseElement?.textContent?.trim() || '';
  if (currentText && typeof window.findAllImagesByMetaTag === 'function') {
    const expectedImages = window.findAllImagesByMetaTag(currentText);
    console.log('  - 期待される画像数:', expectedImages.length);
    expectedImages.forEach((img, index) => {
      console.log(`    期待画像${index + 1}: ${img.image_file}`);
    });
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
}

// グローバルに公開
window.fixO2MultipleImages = fixO2MultipleImages;
window.setupO2AutoFix = setupO2AutoFix;
window.quickFixO2 = quickFixO2;
window.checkO2Status = checkO2Status;

console.log('🔧 O2画像修正関数を読み込みました');
console.log('使用方法:');
console.log('  - quickFixO2()          : 今すぐO2スロットを修正');
console.log('  - fixO2MultipleImages() : 複数画像を強制適用');
console.log('  - setupO2AutoFix()      : 自動監視システム開始');
console.log('  - checkO2Status()       : O2スロットの詳細状態確認');
