// V スロット専用画像表示システム
// 設計仕様書に基づいたメタタグマッチング機能

// 🎯 メタタグデータのキャッシュ
let imageMetaTags = [];

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

// 🖼️ Vスロットに画像を適用
function applyImageToVSlot(phraseText, forceRefresh = false) {
  console.log('🖼️ Vスロット画像適用開始:', phraseText);
  
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error('❌ Vスロットが見つかりません');
    return;
  }
  
  const imgElement = vSlot.querySelector('.slot-image');
  if (!imgElement) {
    console.error('❌ Vスロット内に画像要素が見つかりません');
    return;
  }
  
  console.log('🔍 現在の画像src:', imgElement.src);
  
  // テキストが空の場合はプレースホルダーを設定
  if (!phraseText || phraseText.trim() === '') {
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = 'image for V';
    console.log('📝 Vスロットテキストが空のため、プレースホルダーを設定');
    return;
  }
  
  // 画像を検索
  const imageData = findImageByMetaTag(phraseText);
  console.log('🔍 検索結果:', imageData);
  
  if (!imageData) {
    console.log('🔍 マッチする画像が見つかりません:', phraseText);
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = 'image for V';
    return;
  }
  
  // 新しい画像パスを構築
  const newImagePath = `slot_images/${imageData.folder}/${imageData.image_file}`;
  console.log('🎨 新しい画像パス:', newImagePath);
  
  // 居座り防止：同じ画像の場合は更新しない
  if (!forceRefresh && imgElement.src.includes(imageData.image_file)) {
    console.log('📌 同じ画像のため更新をスキップ:', imageData.image_file);
    return;
  }
  
  // 画像を更新
  imgElement.src = newImagePath;
  imgElement.alt = `image for V: ${imageData.description || phraseText}`;
  
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
  };
  
  console.log('🎨 Vスロット画像更新完了:', phraseText, '→', newImagePath);
  console.log('🎨 更新後の画像src:', imgElement.src);
}

// 🎯 Vスロットのテキストを監視して画像を自動更新
function monitorVSlotText() {
  console.log('🔍 Vスロットテキスト監視開始');
  
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error('❌ Vスロットが見つかりません');
    return;
  }
  
  // slot-phrase または slot-text の内容を監視
  const phraseElement = vSlot.querySelector('.slot-phrase');
  const textElement = vSlot.querySelector('.slot-text');
  
  console.log('🔍 phraseElement:', phraseElement);
  console.log('🔍 textElement:', textElement);
  
  if (!phraseElement && !textElement) {
    console.error('❌ Vスロット内にテキスト要素が見つかりません');
    return;
  }
  
  // 現在のテキストを取得
  const currentPhraseText = phraseElement ? phraseElement.textContent.trim() : '';
  const currentTextText = textElement ? textElement.textContent.trim() : '';
  const currentText = currentPhraseText || currentTextText;
  
  console.log('📝 現在のVスロットテキスト（phrase）:', currentPhraseText);
  console.log('📝 現在のVスロットテキスト（text）:', currentTextText);
  console.log('📝 採用されたテキスト:', currentText);
  
  // 画像を適用
  applyImageToVSlot(currentText);
}

// 🚀 初期化処理
async function initializeVSlotImageSystem() {
  console.log('🚀 Vスロット画像システム初期化開始');
  console.log('📍 現在のURL:', window.location.href);
  
  // メタタグデータを読み込み
  const success = await loadImageMetaTags();
  if (!success) {
    console.error('❌ メタタグデータの読み込みに失敗しました');
    return;
  }
  
  // Vスロットの存在確認
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error('❌ Vスロット（#slot-v）が見つかりません');
    return;
  }
  console.log('✅ Vスロット発見:', vSlot);
  
  // 画像要素の存在確認
  const imgElement = vSlot.querySelector('.slot-image');
  if (!imgElement) {
    console.error('❌ Vスロット内に画像要素が見つかりません');
    return;
  }
  console.log('✅ 画像要素発見:', imgElement);
  
  // 初回の画像適用
  monitorVSlotText();
  
  // 5秒後にもう一度実行（遅延読み込み対応）
  setTimeout(() => {
    console.log('🔄 5秒後の再チェック実行');
    monitorVSlotText();
  }, 5000);
  
  console.log('✅ Vスロット画像システム初期化完了');
}

// 🔄 外部から呼び出し可能な更新関数
function updateVSlotImage(forceRefresh = false) {
  console.log('🔄 updateVSlotImage呼び出し:', forceRefresh);
  
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error('❌ Vスロットが見つかりません');
    return;
  }
  
  const phraseElement = vSlot.querySelector('.slot-phrase');
  const textElement = vSlot.querySelector('.slot-text');
  
  const currentPhraseText = phraseElement ? phraseElement.textContent.trim() : '';
  const currentTextText = textElement ? textElement.textContent.trim() : '';
  const currentText = currentPhraseText || currentTextText;
  
  console.log('🔄 取得したテキスト:', currentText);
  
  applyImageToVSlot(currentText, forceRefresh);
}

// 🧪 テスト用の手動実行関数
function testVSlotImage() {
  console.log('🧪 手動テスト開始');
  console.log('🧪 メタタグデータ:', imageMetaTags);
  
  // 強制的に "become" をテスト
  applyImageToVSlot('become', true);
  
  console.log('🧪 手動テスト完了');
}

// 🎯 グローバル関数として公開
window.initializeVSlotImageSystem = initializeVSlotImageSystem;
window.updateVSlotImage = updateVSlotImage;
window.monitorVSlotText = monitorVSlotText;
window.testVSlotImage = testVSlotImage;

// DOMContentLoaded で自動初期化
document.addEventListener('DOMContentLoaded', () => {
  // 少し遅延させて他のスクリプトの完了を待つ
  setTimeout(initializeVSlotImageSystem, 500);
});

console.log('📦 Vスロット画像システムが読み込まれました');
console.log('📦 テスト用関数: window.testVSlotImage()');
