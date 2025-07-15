// O1とO2スロットの構造・処理の違いを詳細比較
// O1は正常に複数画像表示、O2は失敗する原因を特定

console.log("🔍 O1とO2スロットの比較分析開始");

// O1とO2の現在の状態を詳細比較
function compareO1O2Structure() {
  console.log("📊 === O1とO2スロット構造比較 ===");
  
  const o1Slot = document.getElementById('slot-o1');
  const o2Slot = document.getElementById('slot-o2');
  
  if (!o1Slot || !o2Slot) {
    console.error("❌ O1またはO2スロットが見つかりません");
    return;
  }
  
  // 基本構造の比較
  const o1Analysis = analyzeSlotStructure(o1Slot, 'O1');
  const o2Analysis = analyzeSlotStructure(o2Slot, 'O2');
  
  console.log("📊 O1スロット構造:", o1Analysis);
  console.log("📊 O2スロット構造:", o2Analysis);
  
  // 差異の特定
  const differences = [];
  Object.keys(o1Analysis).forEach(key => {
    if (o1Analysis[key] !== o2Analysis[key]) {
      differences.push(`${key}: O1=${o1Analysis[key]}, O2=${o2Analysis[key]}`);
    }
  });
  
  console.log("🔍 構造的差異:", differences);
  
  return { o1Analysis, o2Analysis, differences };
}

// スロット構造の詳細分析
function analyzeSlotStructure(slot, slotName) {
  const analysis = {
    id: slot.id,
    className: slot.className,
    childCount: slot.children.length,
    hasSlotImage: !!slot.querySelector('.slot-image'),
    hasMultiContainer: !!slot.querySelector('.multi-image-container'),
    hasSlotPhrase: !!slot.querySelector('.slot-phrase'),
    hasSlotText: !!slot.querySelector('.slot-text'),
    hasIndividualRandomizeButton: !!slot.querySelector('.individual-randomize-button'),
    hasSubslotToggle: !!slot.querySelector('.subslot-toggle-button'),
    phraseText: slot.querySelector('.slot-phrase')?.textContent || '',
    textContent: slot.querySelector('.slot-text')?.textContent || '',
    imageCount: slot.querySelectorAll('img').length,
    multiImageCount: slot.querySelectorAll('.slot-multi-image').length
  };
  
  // 子要素の詳細分析
  const childElements = [];
  Array.from(slot.children).forEach((child, index) => {
    childElements.push({
      index,
      tagName: child.tagName,
      className: child.className,
      id: child.id,
      textContent: child.textContent?.substring(0, 50) || '',
      hasImages: child.querySelectorAll('img').length > 0
    });
  });
  
  analysis.childElements = childElements;
  
  return analysis;
}

// 複数画像コンテナの比較
function compareMultiImageContainers() {
  console.log("📊 === 複数画像コンテナ比較 ===");
  
  const o1Container = document.querySelector('#slot-o1 .multi-image-container');
  const o2Container = document.querySelector('#slot-o2 .multi-image-container');
  
  console.log("🔍 O1の複数画像コンテナ:", o1Container ? "存在" : "なし");
  console.log("🔍 O2の複数画像コンテナ:", o2Container ? "存在" : "なし");
  
  if (o1Container) {
    console.log("📊 O1コンテナ詳細:");
    console.log("- display:", o1Container.style.display);
    console.log("- visibility:", o1Container.style.visibility);
    console.log("- opacity:", o1Container.style.opacity);
    console.log("- 画像数:", o1Container.querySelectorAll('.slot-multi-image').length);
    console.log("- innerHTML:", o1Container.innerHTML.substring(0, 200) + '...');
  }
  
  if (o2Container) {
    console.log("📊 O2コンテナ詳細:");
    console.log("- display:", o2Container.style.display);
    console.log("- visibility:", o2Container.style.visibility);
    console.log("- opacity:", o2Container.style.opacity);
    console.log("- 画像数:", o2Container.querySelectorAll('.slot-multi-image').length);
    console.log("- innerHTML:", o2Container.innerHTML.substring(0, 200) + '...');
  }
  
  return { o1Container, o2Container };
}

// テキスト変更監視システムの違いを分析
function analyzeTextMonitoring() {
  console.log("📊 === テキスト変更監視システム比較 ===");
  
  // 現在のテキストを確認
  const o1PhraseText = document.querySelector('#slot-o1 .slot-phrase')?.textContent || '';
  const o1TextContent = document.querySelector('#slot-o1 .slot-text')?.textContent || '';
  const o2PhraseText = document.querySelector('#slot-o2 .slot-phrase')?.textContent || '';
  const o2TextContent = document.querySelector('#slot-o2 .slot-text')?.textContent || '';
  
  console.log("📊 現在のテキスト状態:");
  console.log("- O1 phrase:", o1PhraseText);
  console.log("- O1 text:", o1TextContent);
  console.log("- O2 phrase:", o2PhraseText);
  console.log("- O2 text:", o2TextContent);
  
  // 監視システムの状態確認
  if (window.slotTextObservers) {
    console.log("📊 テキスト監視システム状態:");
    console.log("- slot-o1監視:", window.slotTextObservers['slot-o1'] ? "アクティブ" : "なし");
    console.log("- slot-o2監視:", window.slotTextObservers['slot-o2'] ? "アクティブ" : "なし");
  }
  
  return {
    o1PhraseText,
    o1TextContent,
    o2PhraseText,
    o2TextContent
  };
}

// 画像適用タイミングの違いを分析
function analyzeImageApplicationTiming() {
  console.log("📊 === 画像適用タイミング分析 ===");
  
  // O1とO2のテキストを一時的に同じにして、処理の違いを確認
  const testText = "analyze timing";
  
  console.log("🔍 O1とO2に同じテキストを設定してタイミング分析");
  
  // O1のテキスト変更
  const o1PhraseElement = document.querySelector('#slot-o1 .slot-phrase');
  const o1TextElement = document.querySelector('#slot-o1 .slot-text');
  
  if (o1PhraseElement && o1TextElement) {
    console.log("📝 O1にテストテキスト設定中...");
    o1PhraseElement.textContent = testText;
    o1TextElement.textContent = testText;
    
    setTimeout(() => {
      const o1MultiContainer = document.querySelector('#slot-o1 .multi-image-container');
      console.log("📊 O1処理結果 (500ms後):", o1MultiContainer ? "複数画像コンテナあり" : "複数画像コンテナなし");
    }, 500);
  }
  
  // O2のテキスト変更
  const o2PhraseElement = document.querySelector('#slot-o2 .slot-phrase');
  const o2TextElement = document.querySelector('#slot-o2 .slot-text');
  
  if (o2PhraseElement && o2TextElement) {
    console.log("📝 O2にテストテキスト設定中...");
    o2PhraseElement.textContent = testText;
    o2TextElement.textContent = testText;
    
    setTimeout(() => {
      const o2MultiContainer = document.querySelector('#slot-o2 .multi-image-container');
      console.log("📊 O2処理結果 (500ms後):", o2MultiContainer ? "複数画像コンテナあり" : "複数画像コンテナなし");
    }, 500);
  }
}

// CSS GridやFlexboxの配置設定の違いを分析
function analyzeLayoutDifferences() {
  console.log("📊 === レイアウト設定比較 ===");
  
  const o1Slot = document.getElementById('slot-o1');
  const o2Slot = document.getElementById('slot-o2');
  
  if (o1Slot && o2Slot) {
    const o1Styles = window.getComputedStyle(o1Slot);
    const o2Styles = window.getComputedStyle(o2Slot);
    
    const layoutProperties = [
      'display',
      'grid-template-rows',
      'grid-template-columns',
      'grid-area',
      'flex-direction',
      'justify-content',
      'align-items',
      'position',
      'z-index'
    ];
    
    console.log("📊 レイアウト設定の違い:");
    layoutProperties.forEach(prop => {
      const o1Value = o1Styles[prop];
      const o2Value = o2Styles[prop];
      
      if (o1Value !== o2Value) {
        console.log(`🔍 ${prop}: O1="${o1Value}", O2="${o2Value}"`);
      }
    });
  }
}

// メイン比較実行
function runO1O2Comparison() {
  console.log("🎯 === O1とO2スロット詳細比較分析 ===");
  
  // 1. 構造比較
  const structureComparison = compareO1O2Structure();
  
  // 2. 複数画像コンテナ比較
  setTimeout(() => {
    compareMultiImageContainers();
  }, 500);
  
  // 3. テキスト監視システム比較
  setTimeout(() => {
    analyzeTextMonitoring();
  }, 1000);
  
  // 4. 画像適用タイミング分析
  setTimeout(() => {
    analyzeImageApplicationTiming();
  }, 1500);
  
  // 5. レイアウト設定比較
  setTimeout(() => {
    analyzeLayoutDifferences();
  }, 2500);
}

// グローバルに公開
window.runO1O2Comparison = runO1O2Comparison;
window.compareO1O2Structure = compareO1O2Structure;
window.compareMultiImageContainers = compareMultiImageContainers;
window.analyzeTextMonitoring = analyzeTextMonitoring;
window.analyzeImageApplicationTiming = analyzeImageApplicationTiming;
window.analyzeLayoutDifferences = analyzeLayoutDifferences;

console.log("✅ O1とO2スロット比較ツール準備完了");
console.log("🔄 実行方法: runO1O2Comparison() をコンソールで実行してください");
