// O2スロット複数画像表示問題 根本原因分析ツール
// 他のスロット（S、O1など）と比較して、O2スロットの処理フローの違いを検証

console.log("🔍 O2スロット複数画像表示問題 根本原因分析開始");

// 🎯 テスト用テキストパターン
const testPatterns = [
  { text: "some unexpected news", expectedImages: 2, description: "正常動作パターン" },
  { text: "a funny story", expectedImages: 2, description: "問題発生パターン" }
];

// 📊 全スロットの構造を比較分析
function analyzeSlotStructure() {
  console.log("📊 === 全スロット構造分析 ===");
  
  const allSlots = ['slot-s', 'slot-o1', 'slot-o2', 'slot-c1', 'slot-v', 'slot-m1', 'slot-m2', 'slot-c2', 'slot-m3'];
  const analysis = {};
  
  allSlots.forEach(slotId => {
    const slot = document.getElementById(slotId);
    if (slot) {
      analysis[slotId] = {
        exists: true,
        hasSlotImage: !!slot.querySelector('.slot-image'),
        hasMultiContainer: !!slot.querySelector('.multi-image-container'),
        hasSlotPhrase: !!slot.querySelector('.slot-phrase'),
        hasSlotText: !!slot.querySelector('.slot-text'),
        hasSlotMark: !!slot.querySelector('.slot-mark'),
        innerHTML: slot.innerHTML.substring(0, 200) + '...'
      };
    } else {
      analysis[slotId] = { exists: false };
    }
  });
  
  console.log("📊 全スロット構造分析結果:", analysis);
  
  // O2スロットの構造に特異な点があるかチェック
  if (analysis['slot-o2']) {
    console.log("🔍 O2スロット詳細構造:");
    console.log("- HTML構造:", analysis['slot-o2'].innerHTML);
    console.log("- 画像要素:", analysis['slot-o2'].hasSlotImage);
    console.log("- 複数画像コンテナ:", analysis['slot-o2'].hasMultiContainer);
    console.log("- フレーズ要素:", analysis['slot-o2'].hasSlotPhrase);
    console.log("- テキスト要素:", analysis['slot-o2'].hasSlotText);
  }
  
  return analysis;
}

// 🔄 画像適用処理の差異分析
function analyzeImageApplicationFlow() {
  console.log("🔄 === 画像適用処理フロー分析 ===");
  
  // 各スロットに対して同じテキストを適用して結果を比較
  const testText = "analyze";
  const targetSlots = ['slot-s', 'slot-o1', 'slot-o2', 'slot-c1'];
  
  targetSlots.forEach(slotId => {
    console.log(`🔄 ${slotId}への画像適用テスト開始`);
    
    // 現在の状態を記録
    const slot = document.getElementById(slotId);
    if (slot) {
      const beforeState = {
        slotImage: slot.querySelector('.slot-image')?.src,
        multiContainer: !!slot.querySelector('.multi-image-container'),
        phraseText: slot.querySelector('.slot-phrase')?.textContent || '',
        textContent: slot.querySelector('.slot-text')?.textContent || ''
      };
      
      console.log(`📊 ${slotId} 適用前状態:`, beforeState);
      
      // 画像適用
      if (window.updateSlotImage) {
        window.updateSlotImage(slotId, true);
      }
      
      // 適用後の状態を記録
      setTimeout(() => {
        const afterState = {
          slotImage: slot.querySelector('.slot-image')?.src,
          multiContainer: !!slot.querySelector('.multi-image-container'),
          phraseText: slot.querySelector('.slot-phrase')?.textContent || '',
          textContent: slot.querySelector('.slot-text')?.textContent || ''
        };
        
        console.log(`📊 ${slotId} 適用後状態:`, afterState);
        
        // 差異分析
        const differences = [];
        Object.keys(beforeState).forEach(key => {
          if (beforeState[key] !== afterState[key]) {
            differences.push(`${key}: ${beforeState[key]} → ${afterState[key]}`);
          }
        });
        
        if (differences.length > 0) {
          console.log(`🔍 ${slotId} 変更点:`, differences);
        } else {
          console.log(`⚠️ ${slotId} 変更なし`);
        }
      }, 1000);
    }
  });
}

// 🎯 O2スロット専用の複数画像適用テスト
function testO2MultipleImages() {
  console.log("🎯 === O2スロット複数画像適用テスト ===");
  
  testPatterns.forEach(pattern => {
    console.log(`\n🔍 テスト: "${pattern.text}" (期待枚数: ${pattern.expectedImages})`);
    
    const slot = document.getElementById('slot-o2');
    if (!slot) {
      console.error("❌ O2スロットが見つかりません");
      return;
    }
    
    // まず現在の状態をクリア
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
    }
    
    // フレーズとテキストを設定
    const phraseElement = slot.querySelector('.slot-phrase');
    const textElement = slot.querySelector('.slot-text');
    
    if (phraseElement) {
      phraseElement.textContent = pattern.text;
    }
    if (textElement) {
      textElement.textContent = pattern.text;
    }
    
    console.log(`📝 O2スロットにテキスト設定完了: "${pattern.text}"`);
    
    // 画像検索テスト
    if (window.findAllImagesByMetaTag) {
      const foundImages = window.findAllImagesByMetaTag(pattern.text);
      console.log(`🔍 メタタグ検索結果: ${foundImages.length}個の画像`);
      foundImages.forEach((img, index) => {
        console.log(`  ${index + 1}: ${img.image_file} (${img.description})`);
      });
      
      // 複数画像適用テスト
      if (window.applyMultipleImagesToSlot) {
        console.log("🎨 複数画像適用開始...");
        window.applyMultipleImagesToSlot('slot-o2', pattern.text, true);
        
        // 結果確認
        setTimeout(() => {
          const multiContainer = slot.querySelector('.multi-image-container');
          const actualImages = multiContainer ? multiContainer.querySelectorAll('.slot-multi-image').length : 0;
          
          console.log(`📊 適用結果: ${actualImages}個の画像が表示 (期待: ${pattern.expectedImages})`);
          
          if (actualImages === pattern.expectedImages) {
            console.log(`✅ ${pattern.description}: 成功`);
          } else {
            console.log(`❌ ${pattern.description}: 失敗`);
            
            // 詳細な失敗原因分析
            if (multiContainer) {
              console.log("🔍 複数画像コンテナの状態:");
              console.log("- display:", multiContainer.style.display);
              console.log("- visibility:", multiContainer.style.visibility);
              console.log("- opacity:", multiContainer.style.opacity);
              console.log("- innerHTML:", multiContainer.innerHTML);
            } else {
              console.log("🔍 複数画像コンテナが存在しません");
            }
          }
        }, 2000);
      }
    }
  });
}

// 🔄 画像自動非表示システムの影響分析
function analyzeAutoHideSystemImpact() {
  console.log("🔄 === 画像自動非表示システム影響分析 ===");
  
  const slot = document.getElementById('slot-o2');
  if (!slot) {
    console.error("❌ O2スロットが見つかりません");
    return;
  }
  
  // 現在の画像要素を分析
  const allImages = slot.querySelectorAll('img');
  console.log(`📊 O2スロット内の画像要素数: ${allImages.length}`);
  
  allImages.forEach((img, index) => {
    console.log(`🖼️ 画像${index + 1}:`);
    console.log("- src:", img.src);
    console.log("- alt:", img.alt);
    console.log("- className:", img.className);
    console.log("- style.display:", img.style.display);
    console.log("- style.visibility:", img.style.visibility);
    console.log("- style.opacity:", img.style.opacity);
    console.log("- data-meta-tag:", img.getAttribute('data-meta-tag'));
    console.log("- hasAttribute auto-hidden-image:", img.classList.contains('auto-hidden-image'));
  });
  
  // image_auto_hide.jsの設定を確認
  if (window.shouldHideImage) {
    allImages.forEach((img, index) => {
      const shouldHide = window.shouldHideImage(img);
      console.log(`🔍 画像${index + 1}の非表示判定: ${shouldHide}`);
    });
  }
}

// 🎯 メイン分析実行
function runO2Analysis() {
  console.log("🎯 === O2スロット複数画像表示問題 根本原因分析 ===");
  
  // 1. 構造分析
  const structureAnalysis = analyzeSlotStructure();
  
  // 2. 画像適用フロー分析
  setTimeout(() => {
    analyzeImageApplicationFlow();
  }, 1000);
  
  // 3. O2専用複数画像テスト
  setTimeout(() => {
    testO2MultipleImages();
  }, 3000);
  
  // 4. 自動非表示システム影響分析
  setTimeout(() => {
    analyzeAutoHideSystemImpact();
  }, 8000);
}

// グローバルに公開
window.runO2Analysis = runO2Analysis;
window.analyzeSlotStructure = analyzeSlotStructure;
window.analyzeImageApplicationFlow = analyzeImageApplicationFlow;
window.testO2MultipleImages = testO2MultipleImages;
window.analyzeAutoHideSystemImpact = analyzeAutoHideSystemImpact;

console.log("✅ O2スロット分析ツール準備完了");
console.log("🔄 実行方法: runO2Analysis() をコンソールで実行してください");
