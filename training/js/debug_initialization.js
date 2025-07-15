// 初期化時のO1とO2スロットの処理フロー比較
// なぜO1は初期化時に複数画像が表示され、O2は単一画像しか表示されないのかを調査

console.log("🔍 スロット初期化処理分析開始");

// 初期化時のスロット状態を記録
const initializationLog = {
  o1: { events: [], finalState: null },
  o2: { events: [], finalState: null }
};

// 現在のスロット状態をスナップショット
function captureSlotState(slotId) {
  const slot = document.getElementById(slotId);
  if (!slot) return null;
  
  const state = {
    timestamp: Date.now(),
    hasSlotImage: !!slot.querySelector('.slot-image'),
    hasMultiContainer: !!slot.querySelector('.multi-image-container'),
    imageCount: slot.querySelectorAll('img').length,
    multiImageCount: slot.querySelectorAll('.slot-multi-image').length,
    phraseText: slot.querySelector('.slot-phrase')?.textContent || '',
    textContent: slot.querySelector('.slot-text')?.textContent || '',
    slotImageSrc: slot.querySelector('.slot-image')?.src || '',
    multiContainerDisplay: slot.querySelector('.multi-image-container')?.style.display || 'none',
    innerHTML: slot.innerHTML.substring(0, 300) + '...'
  };
  
  return state;
}

// 初期化時のスロット状態を比較
function compareInitializationStates() {
  console.log("📊 === 初期化時スロット状態比較 ===");
  
  const o1State = captureSlotState('slot-o1');
  const o2State = captureSlotState('slot-o2');
  
  console.log("📊 O1スロット初期状態:", o1State);
  console.log("📊 O2スロット初期状態:", o2State);
  
  // 差異の特定
  if (o1State && o2State) {
    const differences = [];
    Object.keys(o1State).forEach(key => {
      if (key !== 'timestamp' && key !== 'innerHTML' && o1State[key] !== o2State[key]) {
        differences.push(`${key}: O1=${o1State[key]}, O2=${o2State[key]}`);
      }
    });
    
    console.log("🔍 初期化時の差異:", differences);
    
    // 重要な差異の分析
    if (o1State.hasMultiContainer !== o2State.hasMultiContainer) {
      console.log("⚠️ 重要: O1とO2で複数画像コンテナの有無が異なります");
      console.log(`  O1: ${o1State.hasMultiContainer ? '複数画像コンテナあり' : '複数画像コンテナなし'}`);
      console.log(`  O2: ${o2State.hasMultiContainer ? '複数画像コンテナあり' : '複数画像コンテナなし'}`);
    }
    
    if (o1State.multiImageCount !== o2State.multiImageCount) {
      console.log("⚠️ 重要: O1とO2で複数画像数が異なります");
      console.log(`  O1: ${o1State.multiImageCount}枚`);
      console.log(`  O2: ${o2State.multiImageCount}枚`);
    }
  }
  
  return { o1State, o2State };
}

// 初期化に関わる関数の実行状況を調査
function analyzeInitializationFunctions() {
  console.log("📊 === 初期化関数実行状況分析 ===");
  
  // 重要な初期化関数をチェック
  const initFunctions = [
    'initializeSlots',
    'setupSlotImageSystem',
    'initializeImageSystem',
    'setupMultiImageSystem',
    'monitorSlotText',
    'setupSlotTextMonitoring',
    'initializeSlotContent',
    'buildStructure',
    'initializeRandomizers'
  ];
  
  initFunctions.forEach(funcName => {
    const func = window[funcName];
    if (func && typeof func === 'function') {
      console.log(`✅ ${funcName}: 利用可能`);
    } else {
      console.log(`❌ ${funcName}: 利用不可`);
    }
  });
  
  // DOMContentLoadedイベントリスナーの確認
  console.log("🔍 DOMContentLoadedイベントリスナーの確認");
  
  // 画像システムの初期化状態確認
  if (window.slotTextObservers) {
    console.log("📊 テキスト監視システム状態:");
    Object.keys(window.slotTextObservers).forEach(slotId => {
      console.log(`  ${slotId}: ${window.slotTextObservers[slotId] ? 'アクティブ' : 'なし'}`);
    });
  }
}

// 初期化時のテキスト内容を分析
function analyzeInitialTextContent() {
  console.log("📊 === 初期テキスト内容分析 ===");
  
  const slots = ['slot-o1', 'slot-o2'];
  
  slots.forEach(slotId => {
    const slot = document.getElementById(slotId);
    if (slot) {
      const phraseElement = slot.querySelector('.slot-phrase');
      const textElement = slot.querySelector('.slot-text');
      
      const phraseText = phraseElement?.textContent || '';
      const textContent = textElement?.textContent || '';
      
      console.log(`📊 ${slotId}の初期テキスト:`);
      console.log(`  phrase: "${phraseText}"`);
      console.log(`  text: "${textContent}"`);
      
      // テキストに基づく画像検索テスト
      if (phraseText && window.findAllImagesByMetaTag) {
        const foundImages = window.findAllImagesByMetaTag(phraseText);
        console.log(`  画像検索結果: ${foundImages.length}個`);
        foundImages.forEach((img, index) => {
          console.log(`    ${index + 1}: ${img.image_file} (${img.description})`);
        });
        
        // 複数画像が期待できるかチェック
        if (foundImages.length >= 2) {
          console.log(`  ✅ ${slotId}: 複数画像表示が期待できます`);
        } else {
          console.log(`  ⚠️ ${slotId}: 複数画像表示は期待できません`);
        }
      }
    }
  });
}

// 初期化時の画像適用ログをキャプチャ
function captureInitializationLog() {
  console.log("📊 === 初期化ログキャプチャ ===");
  
  // universal_image_system.jsの関数をフック
  const originalApplyImage = window.applyImageToSlot;
  const originalApplyMultiple = window.applyMultipleImagesToSlot;
  
  if (originalApplyImage) {
    window.applyImageToSlot = function(slotId, text, forceUpdate = false) {
      console.log(`🔍 applyImageToSlot呼び出し: ${slotId} → "${text}" (force: ${forceUpdate})`);
      initializationLog[slotId.replace('slot-', '')] = initializationLog[slotId.replace('slot-', '')] || { events: [], finalState: null };
      initializationLog[slotId.replace('slot-', '')].events.push({
        type: 'applyImageToSlot',
        text: text,
        forceUpdate: forceUpdate,
        timestamp: Date.now()
      });
      
      return originalApplyImage.call(this, slotId, text, forceUpdate);
    };
  }
  
  if (originalApplyMultiple) {
    window.applyMultipleImagesToSlot = function(slotId, text, forceUpdate = false) {
      console.log(`🔍 applyMultipleImagesToSlot呼び出し: ${slotId} → "${text}" (force: ${forceUpdate})`);
      initializationLog[slotId.replace('slot-', '')] = initializationLog[slotId.replace('slot-', '')] || { events: [], finalState: null };
      initializationLog[slotId.replace('slot-', '')].events.push({
        type: 'applyMultipleImagesToSlot',
        text: text,
        forceUpdate: forceUpdate,
        timestamp: Date.now()
      });
      
      return originalApplyMultiple.call(this, slotId, text, forceUpdate);
    };
  }
  
  console.log("✅ 初期化ログキャプチャ設定完了");
}

// 初期化分析のメイン実行
function runInitializationAnalysis() {
  console.log("🎯 === スロット初期化処理分析 ===");
  
  // 1. 現在の状態比較
  const currentState = compareInitializationStates();
  
  // 2. 初期化関数の確認
  analyzeInitializationFunctions();
  
  // 3. 初期テキスト内容分析
  analyzeInitialTextContent();
  
  // 4. 初期化ログキャプチャを設定
  captureInitializationLog();
  
  // 5. 最終結果の記録
  setTimeout(() => {
    initializationLog.o1.finalState = captureSlotState('slot-o1');
    initializationLog.o2.finalState = captureSlotState('slot-o2');
    
    console.log("📊 === 最終分析結果 ===");
    console.log("O1初期化ログ:", initializationLog.o1);
    console.log("O2初期化ログ:", initializationLog.o2);
    
    // 重要な発見事項の報告
    const o1HasMulti = initializationLog.o1.finalState?.hasMultiContainer || false;
    const o2HasMulti = initializationLog.o2.finalState?.hasMultiContainer || false;
    
    if (o1HasMulti && !o2HasMulti) {
      console.log("🎯 重要な発見: O1は複数画像コンテナを持っているが、O2は持っていません");
      console.log("これが初期化時の違いの原因と考えられます");
    } else if (!o1HasMulti && !o2HasMulti) {
      console.log("🎯 重要な発見: O1もO2も複数画像コンテナを持っていません");
      console.log("初期化時には両方とも単一画像のみが表示されています");
    }
  }, 2000);
}

// グローバルに公開
window.runInitializationAnalysis = runInitializationAnalysis;
window.compareInitializationStates = compareInitializationStates;
window.analyzeInitializationFunctions = analyzeInitializationFunctions;
window.analyzeInitialTextContent = analyzeInitialTextContent;
window.captureInitializationLog = captureInitializationLog;
window.captureSlotState = captureSlotState;
window.initializationLog = initializationLog;

console.log("✅ 初期化分析ツール準備完了");
console.log("🔄 実行方法: runInitializationAnalysis() をコンソールで実行してください");
