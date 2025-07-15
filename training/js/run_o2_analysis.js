// O2スロット複数画像表示問題 根本原因分析ツール（即座実行版）
// ブラウザコンソールで直接実行可能

(function() {
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
        
        // 現在のテキスト内容も記録
        const phraseText = slot.querySelector('.slot-phrase')?.textContent || '';
        const textContent = slot.querySelector('.slot-text')?.textContent || '';
        analysis[slotId].currentText = phraseText || textContent;
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
      console.log("- 現在のテキスト:", analysis['slot-o2'].currentText);
    }
    
    return analysis;
  }

  // 🔍 現在のO2スロットの状態を詳細分析
  function analyzeCurrentO2State() {
    console.log("🔍 === 現在のO2スロット詳細分析 ===");
    
    const slot = document.getElementById('slot-o2');
    if (!slot) {
      console.error("❌ O2スロットが見つかりません");
      return;
    }
    
    console.log("📊 O2スロットの現在の状態:");
    console.log("- ID:", slot.id);
    console.log("- className:", slot.className);
    console.log("- innerHTML:", slot.innerHTML);
    
    // 子要素の詳細分析
    const children = slot.children;
    console.log(`📊 子要素数: ${children.length}`);
    
    Array.from(children).forEach((child, index) => {
      console.log(`🔍 子要素${index + 1}:`);
      console.log("- tagName:", child.tagName);
      console.log("- className:", child.className);
      console.log("- textContent:", child.textContent);
      console.log("- innerHTML:", child.innerHTML.substring(0, 100) + '...');
    });
    
    // 画像要素の詳細分析
    const images = slot.querySelectorAll('img');
    console.log(`📊 画像要素数: ${images.length}`);
    
    images.forEach((img, index) => {
      console.log(`🖼️ 画像${index + 1}:`);
      console.log("- src:", img.src);
      console.log("- alt:", img.alt);
      console.log("- className:", img.className);
      console.log("- style.display:", img.style.display);
      console.log("- style.visibility:", img.style.visibility);
      console.log("- style.opacity:", img.style.opacity);
      console.log("- width:", img.width);
      console.log("- height:", img.height);
    });
    
    // 複数画像コンテナの分析
    const multiContainer = slot.querySelector('.multi-image-container');
    if (multiContainer) {
      console.log("🔍 複数画像コンテナ発見:");
      console.log("- style.display:", multiContainer.style.display);
      console.log("- style.visibility:", multiContainer.style.visibility);
      console.log("- style.opacity:", multiContainer.style.opacity);
      console.log("- innerHTML:", multiContainer.innerHTML);
      
      const multiImages = multiContainer.querySelectorAll('.slot-multi-image');
      console.log(`📊 複数画像数: ${multiImages.length}`);
    } else {
      console.log("⚠️ 複数画像コンテナが存在しません");
    }
  }

  // 🎯 メタタグ検索機能の動作確認
  function testMetaTagSearch() {
    console.log("🎯 === メタタグ検索機能テスト ===");
    
    testPatterns.forEach(pattern => {
      console.log(`\n🔍 テスト: "${pattern.text}"`);
      
      if (window.findAllImagesByMetaTag) {
        const foundImages = window.findAllImagesByMetaTag(pattern.text);
        console.log(`📊 検索結果: ${foundImages.length}個の画像`);
        foundImages.forEach((img, index) => {
          console.log(`  ${index + 1}: ${img.image_file} (${img.description})`);
        });
        
        if (foundImages.length !== pattern.expectedImages) {
          console.log(`⚠️ 期待枚数(${pattern.expectedImages})と実際の検索結果(${foundImages.length})が一致しません`);
        }
      } else {
        console.error("❌ findAllImagesByMetaTag関数が見つかりません");
      }
    });
  }

  // 🔄 O2スロット複数画像適用の実際のテスト
  function testO2MultipleImageApplication() {
    console.log("🔄 === O2スロット複数画像適用テスト ===");
    
    const slot = document.getElementById('slot-o2');
    if (!slot) {
      console.error("❌ O2スロットが見つかりません");
      return;
    }
    
    // 現在の状態を記録
    const beforeState = {
      hasMultiContainer: !!slot.querySelector('.multi-image-container'),
      imageCount: slot.querySelectorAll('img').length,
      innerHTML: slot.innerHTML
    };
    
    console.log("📊 適用前の状態:", beforeState);
    
    // "a funny story" で複数画像適用テスト
    const testText = "a funny story";
    console.log(`🎨 "${testText}" で複数画像適用テスト開始`);
    
    // まずフレーズを設定
    const phraseElement = slot.querySelector('.slot-phrase');
    const textElement = slot.querySelector('.slot-text');
    
    if (phraseElement) {
      phraseElement.textContent = testText;
      console.log("✅ .slot-phrase にテキスト設定完了");
    } else {
      console.warn("⚠️ .slot-phrase 要素が見つかりません");
    }
    
    if (textElement) {
      textElement.textContent = testText;
      console.log("✅ .slot-text にテキスト設定完了");
    } else {
      console.warn("⚠️ .slot-text 要素が見つかりません");
    }
    
    // 複数画像適用
    if (window.applyMultipleImagesToSlot) {
      console.log("🎨 applyMultipleImagesToSlot実行中...");
      window.applyMultipleImagesToSlot('slot-o2', testText, true);
      
      // 結果を確認
      setTimeout(() => {
        console.log("📊 適用後の状態確認:");
        
        const afterState = {
          hasMultiContainer: !!slot.querySelector('.multi-image-container'),
          imageCount: slot.querySelectorAll('img').length,
          multiImageCount: slot.querySelectorAll('.slot-multi-image').length,
          innerHTML: slot.innerHTML
        };
        
        console.log("📊 適用後の状態:", afterState);
        
        // 詳細分析
        const multiContainer = slot.querySelector('.multi-image-container');
        if (multiContainer) {
          console.log("✅ 複数画像コンテナが作成されました");
          console.log("- コンテナのスタイル:", multiContainer.style.cssText);
          console.log("- 含まれる画像数:", multiContainer.querySelectorAll('img').length);
          
          const multiImages = multiContainer.querySelectorAll('.slot-multi-image');
          multiImages.forEach((img, index) => {
            console.log(`🖼️ 複数画像${index + 1}:`);
            console.log("- src:", img.src);
            console.log("- style.display:", img.style.display);
            console.log("- style.visibility:", img.style.visibility);
            console.log("- style.opacity:", img.style.opacity);
          });
        } else {
          console.warn("⚠️ 複数画像コンテナが作成されませんでした");
        }
        
        // 単一画像の状態も確認
        const singleImage = slot.querySelector('.slot-image');
        if (singleImage) {
          console.log("🖼️ 単一画像の状態:");
          console.log("- src:", singleImage.src);
          console.log("- style.display:", singleImage.style.display);
          console.log("- style.visibility:", singleImage.style.visibility);
          console.log("- style.opacity:", singleImage.style.opacity);
        }
      }, 2000);
    } else {
      console.error("❌ applyMultipleImagesToSlot関数が見つかりません");
    }
  }

  // 🎯 メイン分析実行
  function runAnalysis() {
    console.log("🎯 === O2スロット複数画像表示問題 根本原因分析 ===");
    
    // 1. 構造分析
    analyzeSlotStructure();
    
    // 2. 現在のO2スロット状態分析
    setTimeout(() => {
      analyzeCurrentO2State();
    }, 500);
    
    // 3. メタタグ検索機能テスト
    setTimeout(() => {
      testMetaTagSearch();
    }, 1000);
    
    // 4. 複数画像適用テスト
    setTimeout(() => {
      testO2MultipleImageApplication();
    }, 1500);
  }

  // 即座に実行
  runAnalysis();
  
  // グローバルに公開（再実行用）
  window.runO2Analysis = runAnalysis;
  window.analyzeSlotStructure = analyzeSlotStructure;
  window.analyzeCurrentO2State = analyzeCurrentO2State;
  window.testMetaTagSearch = testMetaTagSearch;
  window.testO2MultipleImageApplication = testO2MultipleImageApplication;
  
  console.log("✅ 分析ツール実行完了。再実行する場合は runO2Analysis() を使用してください");
})();
