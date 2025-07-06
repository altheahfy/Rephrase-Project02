// 画像スロット自動非表示機構
// プレースホルダー画像や読み込みエラー画像を自動的に非表示にする

// 🎯 画像状態キャッシュ（重複処理を回避）
const imageStateCache = new Map();

// 🎯 非表示対象とする画像のパターン
const HIDDEN_IMAGE_PATTERNS = [
  'placeholder.png',           // プレースホルダー画像
  'common/placeholder.png',    // プレースホルダー画像（フルパス）
  'slot_images/common/placeholder.png', // プレースホルダー画像（完全パス）
  '?',                         // 「？」画像
  'question',                  // 「？」関連画像
  'unknown',                   // 不明画像
  'default',                   // デフォルト画像
  'broken',                    // 壊れた画像
  'error',                     // エラー画像
  'missing',                   // 見つからない画像
];

// 🎯 表示すべき有効な画像のパターン（意図したイラスト）
const VALID_IMAGE_PATTERNS = [
  'button.png',                // 詳細ボタンがあるスロット用の指アイコン
  'click_button.png',          // ボタンを押す指のアイコン
  'expand_icon.png',           // 展開アイコン
  'action_icon.png',           // アクションアイコン
  'finger',                    // 指関連の画像
  'hand',                      // 手関連の画像
  'pointer',                   // ポインター画像
  'icon',                      // アイコン系画像
];

// 🎯 メタタグを持つ画像かどうかを判定
function hasImageMetaTag(imgElement) {
  // data-meta-tag 属性を持つ画像は意図したイラスト
  if (imgElement.hasAttribute('data-meta-tag')) {
    return true;
  }
  
  // プレースホルダー以外の画像で、commonフォルダ内の画像は基本的にメタタグ画像
  const src = imgElement.src;
  if (src.includes('slot_images/common/') && !src.includes('placeholder.png')) {
    return true;
  }
  
  return false;
}

// 🔍 画像が非表示対象かどうかを判定
function shouldHideImage(imgElement) {
  if (!imgElement || !imgElement.src) {
    console.log(`🙈 画像にsrcがありません`);
    return true; // src が無い場合は非表示
  }
  
  const src = imgElement.src;
  const alt = imgElement.alt || '';
  
  console.log(`🔍 画像判定中: src="${src}", alt="${alt}"`);
  console.log(`   complete=${imgElement.complete}, naturalWidth=${imgElement.naturalWidth}, naturalHeight=${imgElement.naturalHeight}`);
  
  // 将来のメタタグ対応：メタタグを持つ画像は常に表示
  if (hasImageMetaTag(imgElement)) {
    console.log(`👁 メタタグ付き画像は表示対象: ${src}`);
    return false;
  }
  
  // 詳細ボタンがあるスロットの button.png は常に表示
  const slotContainer = imgElement.closest('.slot-container');
  if (slotContainer) {
    const hasSubslotToggle = slotContainer.querySelector('[data-subslot-toggle]');
    if (hasSubslotToggle && src.includes('button.png')) {
      console.log(`👁 詳細ボタン付きスロットの指アイコンは表示対象: ${src}`);
      return false;
    }
  }
  
  // 有効な画像パターンの場合は表示
  for (const pattern of VALID_IMAGE_PATTERNS) {
    if (src.includes(pattern)) {
      console.log(`👁 有効な画像パターンは表示対象: ${src} (pattern: ${pattern})`);
      return false;
    }
  }
  
  // プレースホルダー画像の場合は非表示
  for (const pattern of HIDDEN_IMAGE_PATTERNS) {
    if (src.includes(pattern)) {
      console.log(`🙈 プレースホルダー画像を検出: ${src} (pattern: ${pattern})`);
      return true;
    }
  }
  
  // 画像読み込みエラーの場合は非表示
  if (imgElement.complete && imgElement.naturalWidth === 0) {
    console.log(`🙈 画像読み込みエラーを検出: ${src}`);
    return true;
  }
  
  // altテキストで判定（"image for" で始まる場合は無効画像）
  if (alt.startsWith('image for')) {
    console.log(`🙈 altテキストで無効画像を検出: ${alt}`);
    return true;
  }
  
  // ブラウザのデフォルト壊れた画像表示（テキスト表示）を検出
  if (imgElement.complete && imgElement.naturalWidth === 0 && imgElement.naturalHeight === 0) {
    console.log(`🙈 壊れた画像を検出: ${src}`);
    return true;
  }
  
  // srcが data:image で始まり、実際の画像データが無い場合
  if (src.startsWith('data:image') && imgElement.complete && imgElement.naturalWidth === 0) {
    console.log(`🙈 無効なdata:image URLを検出: ${src.substring(0, 50)}...`);
    return true;
  }
  
  // 「？」マークのような1x1ピクセルの小さな画像も非表示対象
  if (imgElement.complete && imgElement.naturalWidth <= 16 && imgElement.naturalHeight <= 16) {
    console.log(`🙈 小さすぎる画像（プレースホルダーの可能性）を検出: ${imgElement.naturalWidth}x${imgElement.naturalHeight} - ${src}`);
    return true;
  }
  
  console.log(`👁 画像は表示対象: ${src}`);
  return false; // 有効な画像として表示
}

// 🔍 画像が有効（意図したイラスト）かどうかを判定
function isValidImage(imgElement) {
  if (!imgElement || !imgElement.src) {
    return false;
  }
  
  const src = imgElement.src;
  
  // 将来のメタタグ対応：メタタグを持つ画像は常に表示
  if (hasImageMetaTag(imgElement)) {
    console.log(`✅ メタタグ付き画像を検出: ${src}`);
    return true;
  }
  
  // 詳細ボタンがあるスロットかどうかを判定
  const slotContainer = imgElement.closest('.slot-container');
  if (slotContainer) {
    const hasSubslotToggle = slotContainer.querySelector('[data-subslot-toggle]');
    if (hasSubslotToggle && src.includes('button.png')) {
      console.log(`✅ 詳細ボタン付きスロットの指アイコンを検出: ${src}`);
      return true;
    }
  }
  
  // 有効な画像パターンの場合は表示
  for (const pattern of VALID_IMAGE_PATTERNS) {
    if (src.includes(pattern)) {
      console.log(`✅ 有効な画像パターンを検出: ${src} (pattern: ${pattern})`);
      return true;
    }
  }
  
  // 画像が正常に読み込まれており、プレースホルダーでない場合は有効
  if (imgElement.complete && imgElement.naturalWidth > 16 && imgElement.naturalHeight > 16 && 
      !HIDDEN_IMAGE_PATTERNS.some(pattern => src.includes(pattern))) {
    console.log(`✅ 正常な画像を検出: ${src}`);
    return true;
  }
  
  return false;
}

// 🎨 画像スロットに自動非表示クラスを適用
function applyAutoHideToImage(imgElement) {
  if (!imgElement) return;
  
  const src = imgElement.src;
  const alt = imgElement.alt || '';
  const cacheKey = `${src}|${alt}`;
  
  // キャッシュから状態をチェック
  if (imageStateCache.has(cacheKey)) {
    const cachedResult = imageStateCache.get(cacheKey);
    if (cachedResult.shouldHide) {
      imgElement.classList.add('auto-hidden-image');
      console.log(`🔄 キャッシュから非表示設定: ${imgElement.alt || imgElement.src}`);
    } else {
      imgElement.classList.remove('auto-hidden-image');
      console.log(`🔄 キャッシュから表示設定: ${imgElement.alt || imgElement.src}`);
    }
    return;
  }
  
  // 新しい判定を実行
  const shouldHide = shouldHideImage(imgElement);
  
  // 結果をキャッシュに保存
  imageStateCache.set(cacheKey, { shouldHide, timestamp: Date.now() });
  
  if (shouldHide) {
    imgElement.classList.add('auto-hidden-image');
    console.log(`🙈 画像を自動非表示に設定: ${imgElement.alt || imgElement.src}`);
  } else {
    imgElement.classList.remove('auto-hidden-image');
    console.log(`👁 画像を表示に設定: ${imgElement.alt || imgElement.src}`);
  }
}

// 🎯 詳細ボタンがあるスロットにbutton.pngを自動設定
function setButtonImageForDetailSlots() {
  console.log("🎯 詳細ボタン付きスロットにbutton.png自動設定を開始...");
  
  // 詳細ボタンがあるスロットコンテナを全て取得
  const slotsWithToggle = document.querySelectorAll('.slot-container:has([data-subslot-toggle])');
  
  slotsWithToggle.forEach((slotContainer, index) => {
    const imgElement = slotContainer.querySelector('.slot-image');
    const toggleButton = slotContainer.querySelector('[data-subslot-toggle]');
    
    if (imgElement && toggleButton) {
      const currentSrc = imgElement.src;
      
      // プレースホルダー画像や無効な画像の場合のみbutton.pngに変更
      const shouldReplaceImage = HIDDEN_IMAGE_PATTERNS.some(pattern => currentSrc.includes(pattern)) ||
                                imgElement.alt.startsWith('image for') ||
                                (imgElement.complete && imgElement.naturalWidth === 0);
      
      if (shouldReplaceImage) {
        const buttonImageSrc = 'slot_images/common/button.png';
        imgElement.src = buttonImageSrc;
        imgElement.alt = 'Click to expand details';
        console.log(`✅ スロット${index + 1}にbutton.pngを設定: ${slotContainer.id}`);
      } else if (currentSrc.includes('button.png')) {
        console.log(`👁 スロット${index + 1}は既にbutton.pngが設定済み: ${slotContainer.id}`);
      } else {
        console.log(`🔍 スロット${index + 1}には別の有効な画像が設定済み: ${currentSrc}`);
      }
    }
  });
  
  console.log("✅ 詳細ボタン付きスロットのbutton.png自動設定が完了しました");
}

// 🔄 統合処理：詳細ボタン用画像設定 + 自動非表示処理
function processAllImagesWithButtonAutoSet() {
  console.log("🔄 詳細ボタン用画像設定 + 自動非表示処理を開始...");
  
  // まず詳細ボタン付きスロットにbutton.pngを設定
  setButtonImageForDetailSlots();
  
  // その後、自動非表示処理を実行
  setTimeout(() => {
    processAllImagesWithCoordination();
  }, 100); // 画像設定の反映を待つ
  
  console.log("✅ 統合処理が完了しました");
}

// 🔄 全画像スロットの自動非表示判定を実行
function processAllImageSlots() {
  console.log("🔄 画像スロット自動非表示処理を開始...");
  
  const allImages = document.querySelectorAll('.slot-image');
  console.log(`📊 検出された画像スロット: ${allImages.length}個`);
  
  allImages.forEach((img, index) => {
    console.log(`🔍 画像${index + 1}を処理中:`);
    console.log(`  - src: ${img.src}`);
    console.log(`  - alt: ${img.alt}`);
    console.log(`  - complete: ${img.complete}`);
    console.log(`  - naturalWidth: ${img.naturalWidth}`);
    console.log(`  - naturalHeight: ${img.naturalHeight}`);
    
    // 画像の読み込み完了を待ってから判定
    if (img.complete) {
      applyAutoHideToImage(img);
    } else {
      console.log(`⏳ 画像${index + 1}は読み込み中...`);
      // 画像読み込み完了時に判定
      img.addEventListener('load', () => {
        console.log(`✅ 画像${index + 1}読み込み完了`);
        applyAutoHideToImage(img);
      });
      
      // エラー時も判定
      img.addEventListener('error', () => {
        console.log(`❌ 画像${index + 1}読み込みエラー`);
        applyAutoHideToImage(img);
      });
    }
  });
  
  console.log("✅ 画像スロット自動非表示処理が完了しました");
}

// 🔄 データ更新時の画像再判定
function reprocessImagesAfterDataUpdate() {
  console.log("🔄 データ更新後の画像再判定を実行...");
  
  // 少し遅延させてDOM更新完了を待つ
  setTimeout(() => {
    processAllImageSlots();
  }, 100);
}

// 🔄 ランダマイズ後の画像再判定
function reprocessImagesAfterRandomize() {
  console.log("🔄 ランダマイズ後の画像再判定を実行...");
  
  // ランダマイズ処理完了後に再判定
  setTimeout(() => {
    processAllImageSlots();
  }, 200);
}

// 🎭 手動表示制御との協調動作
function shouldRespectManualControl(imgElement) {
  if (!imgElement) return false;
  
  // 親要素で手動非表示が設定されている場合は、自動制御を停止
  const slotContainer = imgElement.closest('.slot-container, .subslot');
  if (!slotContainer) return false;
  
  // 手動で画像非表示が設定されているかチェック
  const manualHiddenClasses = [
    'hidden-image', 'hidden-s-image', 'hidden-aux-image', 'hidden-v-image',
    'hidden-m1-image', 'hidden-m2-image', 'hidden-c1-image', 'hidden-o1-image',
    'hidden-o2-image', 'hidden-c2-image', 'hidden-m3-image'
  ];
  
  return manualHiddenClasses.some(className => slotContainer.classList.contains(className));
}

// 🔄 手動制御と協調した画像処理
function processImageWithManualControl(imgElement) {
  if (!imgElement) return;
  
  // 手動制御が有効な場合は自動制御を停止
  if (shouldRespectManualControl(imgElement)) {
    imgElement.classList.remove('auto-hidden-image');
    console.log(`⚙️ 手動制御優先: ${imgElement.alt || imgElement.src}`);
    return;
  }
  
  // 自動制御を適用
  applyAutoHideToImage(imgElement);
}

// 🔄 統合処理関数（デバウンス機能付き）
let imageProcessingTimeout = null;
let isImageProcessingActive = false;

function processAllImagesWithCoordination() {
  // 既に処理中の場合は重複実行を防ぐ
  if (isImageProcessingActive) {
    console.log("⏭️ 画像処理が既に実行中のため、重複実行をスキップします");
    return;
  }
  
  // 既存のタイマーをクリア
  if (imageProcessingTimeout) {
    clearTimeout(imageProcessingTimeout);
    console.log("⏰ 既存のタイマーをクリアしました");
  }
  
  // デバウンス：短時間の連続呼び出しを防ぐ
  imageProcessingTimeout = setTimeout(() => {
    isImageProcessingActive = true;
    console.log("🔄 手動制御協調型画像処理を開始...");
    
    const allImages = document.querySelectorAll('.slot-image');
    allImages.forEach(img => {
      processImageWithManualControl(img);
    });
    
    console.log("✅ 手動制御協調型画像処理が完了しました");
    isImageProcessingActive = false;
  }, 300); // 300ms のデバウンス（さらに長く設定）
}

// 🗑️ 画像キャッシュをクリアする関数
function clearImageStateCache() {
  imageStateCache.clear();
  console.log("🗑️ 画像状態キャッシュをクリアしました");
}

// 📊 画像処理統計を表示する関数
function showImageProcessingStats() {
  console.log("📊 === 画像処理統計情報 ===");
  console.log(`キャッシュエントリ数: ${imageStateCache.size}`);
  console.log(`現在の処理状態: ${isImageProcessingActive ? '処理中' : '待機中'}`);
  console.log(`タイマー状態: ${imageProcessingTimeout ? 'セット中' : 'クリア'}`);
  
  if (imageStateCache.size > 0) {
    console.log("📋 キャッシュ内容:");
    let hiddenCount = 0;
    let visibleCount = 0;
    
    imageStateCache.forEach((value, key) => {
      if (value.shouldHide) {
        hiddenCount++;
      } else {
        visibleCount++;
      }
      console.log(`  ${key} -> ${value.shouldHide ? '非表示' : '表示'}`);
    });
    
    console.log(`📈 統計: 表示=${visibleCount}個, 非表示=${hiddenCount}個`);
  }
}

// 🔹 グローバル関数としてエクスポート
window.processAllImageSlots = processAllImageSlots;
window.reprocessImagesAfterDataUpdate = reprocessImagesAfterDataUpdate;
window.reprocessImagesAfterRandomize = reprocessImagesAfterRandomize;
window.processAllImagesWithCoordination = processAllImagesWithCoordination;
window.setButtonImageForDetailSlots = setButtonImageForDetailSlots;
window.processAllImagesWithButtonAutoSet = processAllImagesWithButtonAutoSet;
window.clearImageStateCache = clearImageStateCache;
window.showImageProcessingStats = showImageProcessingStats;

// 🔹 デバッグ用手動実行関数
window.debugImageHiding = function() {
  console.log("🔧 デバッグ: 手動で画像非表示処理を実行");
  processAllImagesWithCoordination();
};

window.showAllImageInfo = function() {
  console.log("🔍 全画像要素の情報を表示:");
  const allImages = document.querySelectorAll('.slot-image');
  allImages.forEach((img, index) => {
    console.log(`画像${index + 1}:`);
    console.log(`  - ID: ${img.closest('.slot-container')?.id || 'unknown'}`);
    console.log(`  - src: ${img.src}`);
    console.log(`  - alt: ${img.alt}`);
    console.log(`  - complete: ${img.complete}`);
    console.log(`  - naturalWidth: ${img.naturalWidth}`);
    console.log(`  - naturalHeight: ${img.naturalHeight}`);
    console.log(`  - classList: ${Array.from(img.classList).join(', ')}`);
    console.log(`  - style.display: ${img.style.display}`);
    console.log(`  - 詳細ボタン有無: ${img.closest('.slot-container')?.querySelector('[data-subslot-toggle]') ? 'あり' : 'なし'}`);
  });
};

// 🔄 ページ読み込み時の自動実行
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 画像自動非表示システムを初期化中...");
  
  // insert_test_data_clean.jsの処理完了を待ってから実行
  setTimeout(() => {
    console.log("🔄 insert_test_data_clean.js処理完了後の画像処理を実行...");
    processAllImagesWithCoordination();
  }, 800); // より長い遅延でinsert_test_data_clean.jsの完了を確実に待つ
  
  // データの変更を監視して画像を再判定
  const observer = new MutationObserver(function(mutations) {
    let shouldReprocess = false;
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList' || 
          (mutation.type === 'attributes' && mutation.attributeName === 'src')) {
        shouldReprocess = true;
      }
    });
    
    if (shouldReprocess) {
      setTimeout(() => {
        processAllImagesWithCoordination();
      }, 100);
    }
  });
  
  // 画像要素の変更を監視
  observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['src', 'alt']
  });
});

console.log("✅ image_auto_hide.js が読み込まれました");
