// 汎用イラスト表示システム
// すべての上位スロットに対応したメタタグマッチング機能

// 🎯 メタタグデータのキャッシュ
let imageMetaTags = [];

// 🎯 対象となる上位スロット一覧
const UPPER_SLOTS = [
  'slot-m1',
  'slot-s', 
  'slot-aux',
  'slot-m2',
  'slot-v',
  'slot-c1',
  'slot-o1',
  'slot-o2',
  'slot-c2',
  'slot-m3'
];

// 🔧 メタタグデータの読み込み
async function loadImageMetaTags() {
  try {
    const response = await fetch('image_meta_tags.json?t=' + Date.now()); // キャッシュ回避
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    imageMetaTags = await response.json();
    console.log('✅ メタタグデータ読み込み成功:', imageMetaTags.length, '件');
    return true;
  } catch (error) {
    console.error('❌ メタタグデータ読み込み失敗:', error);
    return false;
  }
}

// 🔍 テキストから検索対象単語を抽出（語幹抽出付き）
function extractWordsWithStemming(text) {
  if (!text || typeof text !== 'string') {
    return [];
  }
  
  // 2文字以上の単語を抽出
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length >= 2);
  
  const searchWords = new Set();
  
  for (const word of words) {
    // 元の単語を追加
    searchWords.add(word);
    
    // 最小限の語幹抽出
    if (word.endsWith('s') && word.length > 2) {
      searchWords.add(word.slice(0, -1)); // -s
    }
    if (word.endsWith('ed') && word.length > 3) {
      searchWords.add(word.slice(0, -2)); // -ed
    }
    if (word.endsWith('ing') && word.length > 4) {
      searchWords.add(word.slice(0, -3)); // -ing
    }
  }
  
  return Array.from(searchWords);
}

// 🔍 テキストにマッチする画像を検索
function findImageByMetaTag(text) {
  if (!text || !imageMetaTags.length) {
    return null;
  }
  
  const searchWords = extractWordsWithStemming(text);
  console.log('🔍 検索単語:', searchWords);
  
  let bestMatch = null;
  let bestPriority = 0;
  
  for (const imageData of imageMetaTags) {
    for (const metaTag of imageData.meta_tags) {
      if (searchWords.includes(metaTag.toLowerCase())) {
        const priority = imageData.priority || 1;
        if (priority > bestPriority) {
          bestMatch = imageData;
          bestPriority = priority;
        }
        console.log('🎯 マッチング成功:', metaTag, '→', imageData.image_file);
      }
    }
  }
  
  return bestMatch;
}

// 🖼️ 指定スロットに画像を適用
function applyImageToSlot(slotId, phraseText, forceRefresh = false) {
  console.log('🖼️ スロット画像適用開始:', slotId, '→', phraseText);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.error('❌ スロットが見つかりません:', slotId);
    return;
  }
  
  const imgElement = slot.querySelector('.slot-image');
  if (!imgElement) {
    console.error('❌ スロット内に画像要素が見つかりません:', slotId);
    return;
  }
  
  console.log('🔍 現在の画像src:', imgElement.src);
  
  // テキストが空の場合はプレースホルダーを設定
  if (!phraseText || phraseText.trim() === '') {
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${slotId}`;
    console.log('📝 スロットテキストが空のため、プレースホルダーを設定:', slotId);
    return;
  }
  
  // 画像を検索
  const imageData = findImageByMetaTag(phraseText);
  console.log('🔍 検索結果:', imageData);
  
  if (!imageData) {
    console.log('🔍 マッチする画像が見つかりません:', phraseText);
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${slotId}`;
    return;
  }
  
  // 新しい画像パスを構築
  const newImagePath = `slot_images/${imageData.folder}/${imageData.image_file}`;
  console.log('🎨 新しい画像パス:', newImagePath);
  
  // 居座り防止：完全に同じパスの場合のみ更新をスキップ
  const currentImagePath = imgElement.src;
  const fullNewImagePath = new URL(newImagePath, window.location.href).href;
  
  if (!forceRefresh && currentImagePath === fullNewImagePath) {
    console.log('📌 完全に同じ画像のため更新をスキップ:', imageData.image_file);
    console.log('  現在:', currentImagePath);
    console.log('  新規:', fullNewImagePath);
    return;
  }
  
  console.log('🔄 画像を更新します:');
  console.log('  現在:', currentImagePath);
  console.log('  新規:', fullNewImagePath);
  
  // 画像を更新（キャッシュバスター付き）
  const cacheBuster = Date.now(); // キャッシュ回避用のタイムスタンプ
  const imageUrlWithCacheBuster = `${newImagePath}?t=${cacheBuster}`;
  
  imgElement.src = imageUrlWithCacheBuster;
  imgElement.alt = `image for ${slotId}: ${imageData.description || phraseText}`;
  
  console.log('🔄 キャッシュバスター付きURL:', imageUrlWithCacheBuster);
  
  // メタタグ属性を設定（image_auto_hide.js対応）
  imgElement.setAttribute('data-meta-tag', 'true');
  
  // 強制的に表示状態にする
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  imgElement.classList.remove('auto-hidden-image');
  
  // 画像読み込み完了後に再度表示を確認
  imgElement.onload = function() {
    console.log('🎨 画像読み込み完了:', newImagePath);
    this.style.display = 'block';
    this.style.visibility = 'visible';
    this.style.opacity = '1';
    this.classList.remove('auto-hidden-image');
    
    // 1秒後にもう一度強制表示（image_auto_hide.js対策）
    setTimeout(() => {
      console.log('🛡️ 遅延表示強制実行:', slotId);
      this.style.display = 'block';
      this.style.visibility = 'visible';
      this.style.opacity = '1';
      this.classList.remove('auto-hidden-image');
      
      // 最終確認
      const computedStyle = window.getComputedStyle(this);
      console.log('🛡️ 最終表示状態:', {
        slotId: slotId,
        display: computedStyle.display,
        visibility: computedStyle.visibility,
        opacity: computedStyle.opacity
      });
    }, 1000);
  };
  
  console.log('🎨 スロット画像更新完了:', slotId, '→', phraseText, '→', newImagePath);
  console.log('🎨 更新後の画像src:', imgElement.src);
}

// 🎯 指定スロットのテキストを監視して画像を自動更新
function monitorSlotText(slotId) {
  console.log('🔍 スロットテキスト監視開始:', slotId);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.error('❌ スロットが見つかりません:', slotId);
    return;
  }
  
  // slot-phrase または slot-text の内容を監視
  const phraseElement = slot.querySelector('.slot-phrase');
  const textElement = slot.querySelector('.slot-text');
  
  console.log('🔍 phraseElement:', phraseElement, 'textElement:', textElement);
  
  if (!phraseElement && !textElement) {
    console.error('❌ スロット内にテキスト要素が見つかりません:', slotId);
    return;
  }
  
  // 現在のテキストを取得
  const currentPhraseText = phraseElement ? phraseElement.textContent.trim() : '';
  const currentTextText = textElement ? textElement.textContent.trim() : '';
  const currentText = currentPhraseText || currentTextText;
  
  console.log('📝 現在のスロットテキスト:', slotId, '→', currentText);
  
  // 画像を適用
  applyImageToSlot(slotId, currentText);
}

// 🚀 全スロットの画像システム初期化
async function initializeUniversalImageSystem() {
  console.log('🚀 汎用画像システム初期化開始');
  console.log('📍 現在のURL:', window.location.href);
  
  // メタタグデータを読み込み
  const success = await loadImageMetaTags();
  if (!success) {
    console.error('❌ メタタグデータの読み込みに失敗しました');
    return;
  }
  
  // 全上位スロットに対して処理
  for (const slotId of UPPER_SLOTS) {
    console.log(`🔍 処理中のスロット: ${slotId}`);
    
    const slot = document.getElementById(slotId);
    if (!slot) {
      console.warn(`⚠️ スロットが見つかりません: ${slotId}`);
      continue;
    }
    
    // 画像要素の存在確認
    const imgElement = slot.querySelector('.slot-image');
    if (!imgElement) {
      console.warn(`⚠️ スロット内に画像要素が見つかりません: ${slotId}`);
      continue;
    }
    
    console.log(`✅ スロット処理可能: ${slotId}`);
    
    // 初回の画像適用
    monitorSlotText(slotId);
  }
  
  // 5秒後にもう一度実行（遅延読み込み対応）
  setTimeout(() => {
    console.log('🔄 5秒後の再チェック実行');
    for (const slotId of UPPER_SLOTS) {
      monitorSlotText(slotId);
    }
  }, 5000);
  
  console.log('✅ 汎用画像システム初期化完了');
}

// 🔄 外部から呼び出し可能な更新関数（全スロット）
function updateAllSlotImages(forceRefresh = false) {
  console.log('🔄 全スロット画像更新開始:', forceRefresh);
  console.log('🔄 メタタグデータ状態:', imageMetaTags ? imageMetaTags.length : 'null');
  
  for (const slotId of UPPER_SLOTS) {
    updateSlotImage(slotId, forceRefresh);
  }
  
  console.log('✅ 全スロット画像更新完了');
}

// 🔄 外部から呼び出し可能な更新関数（個別スロット）
function updateSlotImage(slotId, forceRefresh = false) {
  console.log('🔄 スロット画像更新:', slotId, forceRefresh);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.error('❌ スロットが見つかりません:', slotId);
    return;
  }
  
  const phraseElement = slot.querySelector('.slot-phrase');
  const textElement = slot.querySelector('.slot-text');
  
  const currentPhraseText = phraseElement ? phraseElement.textContent.trim() : '';
  const currentTextText = textElement ? textElement.textContent.trim() : '';
  const currentText = currentPhraseText || currentTextText;
  
  console.log('🔄 取得したテキスト:', slotId, '→', currentText);
  
  if (!currentText) {
    console.warn('⚠️ スロットテキストが空です:', slotId);
    return;
  }
  
  applyImageToSlot(slotId, currentText, forceRefresh);
  
  // 1秒後に画像の状態を再確認
  setTimeout(() => {
    const imgElement = slot.querySelector('.slot-image');
    if (imgElement) {
      const computedStyle = window.getComputedStyle(imgElement);
      console.log('🔍 1秒後の画像状態:', slotId);
      console.log('  - src:', imgElement.src);
      console.log('  - display:', computedStyle.display);
      console.log('  - visibility:', computedStyle.visibility);
      console.log('  - opacity:', computedStyle.opacity);
      console.log('  - classes:', Array.from(imgElement.classList));
    }
  }, 1000);
}

// 🔄 データ更新後の全スロット画像再更新
function updateAllSlotImagesAfterDataChange() {
  console.log('🔄 データ更新後の全スロット画像再更新を実行...');
  
  // 強制的に画像を再計算
  updateAllSlotImages(true);
  
  console.log('✅ データ更新後の全スロット画像再更新が完了しました');
}

// 🧪 テスト用の手動実行関数
function testUniversalImageSystem() {
  console.log('🧪 汎用画像システム手動テスト開始');
  console.log('🧪 メタタグデータ:', imageMetaTags);
  
  // 各スロットに対してテスト実行
  for (const slotId of UPPER_SLOTS) {
    console.log(`🧪 テスト実行: ${slotId}`);
    updateSlotImage(slotId, true);
  }
  
  console.log('🧪 汎用画像システム手動テスト完了');
}

// 🎯 グローバル関数として公開
window.initializeUniversalImageSystem = initializeUniversalImageSystem;
window.updateAllSlotImages = updateAllSlotImages;
window.updateSlotImage = updateSlotImage;
window.updateAllSlotImagesAfterDataChange = updateAllSlotImagesAfterDataChange;
window.testUniversalImageSystem = testUniversalImageSystem;

// 🔄 旧V専用システムとの互換性維持
window.updateVSlotImage = function(forceRefresh = false) {
  updateSlotImage('slot-v', forceRefresh);
};
window.updateVSlotImageAfterDataChange = function() {
  updateSlotImage('slot-v', true);
};

// DOMContentLoaded で自動初期化
document.addEventListener('DOMContentLoaded', () => {
  // 少し遅延させて他のスクリプトの完了を待つ
  setTimeout(initializeUniversalImageSystem, 500);
});

console.log('📦 汎用画像システムが読み込まれました');
console.log('📦 対象スロット:', UPPER_SLOTS);
console.log('📦 テスト用関数: window.testUniversalImageSystem()');
