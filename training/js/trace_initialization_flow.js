// 初期化時の画像検索処理フロー詳細トレース
// O1とO2で画像検索結果が異なる理由を特定

console.log("🔍 初期化時画像検索処理フロートレース開始");

// 画像検索処理の詳細ログ
function traceImageSearch(text, slotContext) {
  console.log(`\n🔍 === 画像検索トレース: "${text}" (${slotContext}) ===`);
  
  if (!window.findAllImagesByMetaTag) {
    console.error("❌ findAllImagesByMetaTag関数が見つかりません");
    return;
  }
  
  // 元の関数を一時的にフック
  const originalFindImages = window.findAllImagesByMetaTag;
  
  window.findAllImagesByMetaTag = function(searchText) {
    console.log(`🔍 findAllImagesByMetaTag呼び出し: "${searchText}"`);
    
    // 元の処理を実行
    const result = originalFindImages.call(this, searchText);
    
    console.log(`📊 検索結果: ${result.length}個の画像`);
    result.forEach((img, index) => {
      console.log(`  ${index + 1}: ${img.image_file} (${img.description}) - 優先度: ${img.priority}`);
    });
    
    return result;
  };
  
  // 検索実行
  const searchResult = window.findAllImagesByMetaTag(text);
  
  // 元の関数を復元
  window.findAllImagesByMetaTag = originalFindImages;
  
  return searchResult;
}

// 初期化時の画像適用処理をトレース
function traceInitialImageApplication() {
  console.log("🔍 === 初期化時画像適用処理トレース ===");
  
  // O1とO2の初期テキストを取得
  const o1PhraseText = document.querySelector('#slot-o1 .slot-phrase')?.textContent || '';
  const o2PhraseText = document.querySelector('#slot-o2 .slot-phrase')?.textContent || '';
  
  console.log(`📊 O1初期テキスト: "${o1PhraseText}"`);
  console.log(`📊 O2初期テキスト: "${o2PhraseText}"`);
  
  // 各スロットの画像検索をトレース
  if (o1PhraseText) {
    const o1Result = traceImageSearch(o1PhraseText, 'O1スロット');
    console.log(`📊 O1検索結果: ${o1Result.length}個 → ${o1Result.length >= 2 ? '複数画像期待' : '単一画像のみ'}`);
  }
  
  if (o2PhraseText) {
    const o2Result = traceImageSearch(o2PhraseText, 'O2スロット');
    console.log(`📊 O2検索結果: ${o2Result.length}個 → ${o2Result.length >= 2 ? '複数画像期待' : '単一画像のみ'}`);
  }
}

// テキスト正規化処理の違いを分析
function analyzeTextNormalization() {
  console.log("🔍 === テキスト正規化処理分析 ===");
  
  const o1Text = document.querySelector('#slot-o1 .slot-phrase')?.textContent || '';
  const o2Text = document.querySelector('#slot-o2 .slot-phrase')?.textContent || '';
  
  console.log(`📊 O1元テキスト: "${o1Text}"`);
  console.log(`📊 O2元テキスト: "${o2Text}"`);
  
  // 正規化プロセスを手動で実行
  const texts = [
    { original: o1Text, context: 'O1' },
    { original: o2Text, context: 'O2' }
  ];
  
  texts.forEach(({ original, context }) => {
    console.log(`\n🔍 ${context}テキスト正規化プロセス:`);
    
    // 1. 句読点除去
    const withoutPunctuation = original.replace(/[.,!?;:]/g, '');
    console.log(`  1. 句読点除去: "${withoutPunctuation}"`);
    
    // 2. 小文字化
    const lowercase = withoutPunctuation.toLowerCase();
    console.log(`  2. 小文字化: "${lowercase}"`);
    
    // 3. 単語分割
    const words = lowercase.split(/\s+/).filter(word => word.length > 0);
    console.log(`  3. 単語分割: [${words.join(', ')}]`);
    
    // 4. 各単語での画像検索
    words.forEach(word => {
      if (window.imageMetaData) {
        const matches = window.imageMetaData.filter(img => 
          img.meta_tags.some(tag => tag.toLowerCase().includes(word))
        );
        console.log(`    "${word}" → ${matches.length}個のマッチ`);
        matches.forEach(match => {
          console.log(`      - ${match.image_file} (${match.description})`);
        });
      }
    });
  });
}

// 初期化時の画像適用条件を分析
function analyzeImageApplicationConditions() {
  console.log("🔍 === 画像適用条件分析 ===");
  
  // 複数画像適用の条件をチェック
  const o1PhraseText = document.querySelector('#slot-o1 .slot-phrase')?.textContent || '';
  const o2PhraseText = document.querySelector('#slot-o2 .slot-phrase')?.textContent || '';
  
  [
    { text: o1PhraseText, slot: 'O1' },
    { text: o2PhraseText, slot: 'O2' }
  ].forEach(({ text, slot }) => {
    console.log(`\n📊 ${slot}スロット画像適用条件:`);
    
    if (window.findAllImagesByMetaTag) {
      const images = window.findAllImagesByMetaTag(text);
      console.log(`  検索結果: ${images.length}個`);
      
      // 複数画像適用条件
      if (images.length >= 2) {
        console.log(`  ✅ 複数画像適用条件: 満たしている`);
        console.log(`  → applyMultipleImagesToSlot('slot-${slot.toLowerCase()}', '${text}') が実行されるはず`);
      } else {
        console.log(`  ❌ 複数画像適用条件: 満たしていない`);
        console.log(`  → applyImageToSlot('slot-${slot.toLowerCase()}', '${text}') が実行されるはず`);
      }
    }
  });
}

// 初期化時の実際の関数呼び出しをフック
function hookInitializationCalls() {
  console.log("🔍 === 初期化時関数呼び出しフック ===");
  
  // 重要な関数をフック
  const originalApplyImage = window.applyImageToSlot;
  const originalApplyMultiple = window.applyMultipleImagesToSlot;
  const originalUpdateSlotImage = window.updateSlotImage;
  
  if (originalApplyImage) {
    window.applyImageToSlot = function(slotId, text, forceUpdate = false) {
      console.log(`📞 applyImageToSlot呼び出し: ${slotId} → "${text}" (force: ${forceUpdate})`);
      console.log(`  → 単一画像適用処理`);
      return originalApplyImage.call(this, slotId, text, forceUpdate);
    };
  }
  
  if (originalApplyMultiple) {
    window.applyMultipleImagesToSlot = function(slotId, text, forceUpdate = false) {
      console.log(`📞 applyMultipleImagesToSlot呼び出し: ${slotId} → "${text}" (force: ${forceUpdate})`);
      console.log(`  → 複数画像適用処理`);
      return originalApplyMultiple.call(this, slotId, text, forceUpdate);
    };
  }
  
  if (originalUpdateSlotImage) {
    window.updateSlotImage = function(slotId, forceUpdate = false) {
      console.log(`📞 updateSlotImage呼び出し: ${slotId} (force: ${forceUpdate})`);
      return originalUpdateSlotImage.call(this, slotId, forceUpdate);
    };
  }
  
  console.log("✅ 初期化時関数呼び出しフック設定完了");
}

// メイン処理フロートレース実行
function runInitializationFlowTrace() {
  console.log("🎯 === 初期化処理フロートレース ===");
  
  // 1. 関数呼び出しフック設定
  hookInitializationCalls();
  
  // 2. 初期テキストでの画像検索トレース
  traceInitialImageApplication();
  
  // 3. テキスト正規化処理分析
  analyzeTextNormalization();
  
  // 4. 画像適用条件分析
  analyzeImageApplicationConditions();
  
  console.log("\n🎯 === 重要な発見 ===");
  console.log("フック設定完了。今度はページをリロードして初期化処理を観察してください。");
}

// グローバルに公開
window.runInitializationFlowTrace = runInitializationFlowTrace;
window.traceImageSearch = traceImageSearch;
window.traceInitialImageApplication = traceInitialImageApplication;
window.analyzeTextNormalization = analyzeTextNormalization;
window.analyzeImageApplicationConditions = analyzeImageApplicationConditions;
window.hookInitializationCalls = hookInitializationCalls;

console.log("✅ 初期化処理フロートレースツール準備完了");
console.log("🔄 実行方法: runInitializationFlowTrace() をコンソールで実行してください");
