// 汎用イラスト表示システム
// すべての上位スロットに対応したメタタグマッチング機能

// 🎯 メタタグデータのキャッシュ
let imageMetaTags = [];

// デバッグ用：グローバルに公開
window.imageMetaTags = imageMetaTags;

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

// 🎯 サブスロットのマッピング（親スロット → サブスロット一覧）
const SUBSLOT_MAPPING = {
  's': ['slot-s-sub-m1', 'slot-s-sub-s', 'slot-s-sub-aux', 'slot-s-sub-m2', 'slot-s-sub-v', 'slot-s-sub-c1', 'slot-s-sub-o1', 'slot-s-sub-o2', 'slot-s-sub-c2', 'slot-s-sub-m3'],
  'm1': ['slot-m1-sub-m1', 'slot-m1-sub-s', 'slot-m1-sub-aux', 'slot-m1-sub-m2', 'slot-m1-sub-v', 'slot-m1-sub-c1', 'slot-m1-sub-o1', 'slot-m1-sub-o2', 'slot-m1-sub-c2', 'slot-m1-sub-m3'],
  'm2': ['slot-m2-sub-m1', 'slot-m2-sub-s', 'slot-m2-sub-aux', 'slot-m2-sub-m2', 'slot-m2-sub-v', 'slot-m2-sub-c1', 'slot-m2-sub-o1', 'slot-m2-sub-o2', 'slot-m2-sub-c2', 'slot-m2-sub-m3'],
  'c1': ['slot-c1-sub-m1', 'slot-c1-sub-s', 'slot-c1-sub-aux', 'slot-c1-sub-m2', 'slot-c1-sub-v', 'slot-c1-sub-c1', 'slot-c1-sub-o1', 'slot-c1-sub-o2', 'slot-c1-sub-c2', 'slot-c1-sub-m3'],
  'o1': ['slot-o1-sub-m1', 'slot-o1-sub-s', 'slot-o1-sub-aux', 'slot-o1-sub-m2', 'slot-o1-sub-v', 'slot-o1-sub-c1', 'slot-o1-sub-o1', 'slot-o1-sub-o2', 'slot-o1-sub-c2', 'slot-o1-sub-m3'],
  'o2': ['slot-o2-sub-m1', 'slot-o2-sub-s', 'slot-o2-sub-aux', 'slot-o2-sub-m2', 'slot-o2-sub-v', 'slot-o2-sub-c1', 'slot-o2-sub-o1', 'slot-o2-sub-o2', 'slot-o2-sub-c2', 'slot-o2-sub-m3'],
  'c2': ['slot-c2-sub-m1', 'slot-c2-sub-s', 'slot-c2-sub-aux', 'slot-c2-sub-m2', 'slot-c2-sub-v', 'slot-c2-sub-c1', 'slot-c2-sub-o1', 'slot-c2-sub-o2', 'slot-c2-sub-c2', 'slot-c2-sub-m3'],
  'm3': ['slot-m3-sub-m1', 'slot-m3-sub-s', 'slot-m3-sub-aux', 'slot-m3-sub-m2', 'slot-m3-sub-v', 'slot-m3-sub-c1', 'slot-m3-sub-o1', 'slot-m3-sub-o2', 'slot-m3-sub-c2', 'slot-m3-sub-m3']
};

// 🔧 メタタグデータの読み込み
async function loadImageMetaTags() {
  console.log('🔄 メタタグデータ読み込み開始...');
  console.log('📍 読み込み予定URL:', window.location.origin + '/image_meta_tags.json');
  
  try {
    const response = await fetch('image_meta_tags.json?t=' + Date.now()); // キャッシュ回避
    console.log('📡 Fetch response:', response);
    console.log('📊 Response status:', response.status);
    console.log('📊 Response ok:', response.ok);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    imageMetaTags = data;
    
    // グローバルに公開（デバッグ用）
    window.imageMetaTags = imageMetaTags;
    
    console.log('✅ メタタグデータ読み込み成功:', imageMetaTags.length, '件');
    console.log('📋 読み込まれたデータ（最初の3件）:', imageMetaTags.slice(0, 3));
    return true;
  } catch (error) {
    console.error('❌ メタタグデータ読み込み失敗:', error);
    console.error('🔍 エラー詳細:', {
      message: error.message,
      stack: error.stack,
      currentURL: window.location.href
    });
    return false;
  }
}

// 🔍 テキストから検索対象単語を抽出（改良版語幹抽出付き）
function extractWordsWithStemming(text) {
  if (!text || typeof text !== 'string') {
    return [];
  }
  
  // 🆕 日本語テキスト対応：全角・半角文字、句読点を適切に処理
  const normalizedText = text.toLowerCase()
    .replace(/[、。，！？]/g, ' ') // 日本語句読点を空白に
    .replace(/[^\w\s-]/g, ' '); // その他の記号を空白に
  
  const words = normalizedText.split(/\s+/).filter(word => word.length >= 2);
  
  console.log('🔍 日本語対応 - 元テキスト:', text);
  console.log('🔍 日本語対応 - 正規化後:', normalizedText);
  console.log('🔍 日本語対応 - 抽出単語:', words);
  
  const searchWords = new Set();
  
  // まず元のフレーズをそのまま追加
  searchWords.add(normalizedText.trim());
  
  for (const word of words) {
    // 元の単語を追加
    searchWords.add(word);
    
    // 改良された語幹抽出
    if (word.endsWith('s') && word.length > 2) {
      searchWords.add(word.slice(0, -1)); // -s
    }
    if (word.endsWith('ed') && word.length > 3) {
      const stem = word.slice(0, -2);
      searchWords.add(stem); // -ed
      // 特別ケース：figured → figure
      if (word === 'figured') {
        searchWords.add('figure');
      }
    }
    if (word.endsWith('ing') && word.length > 4) {
      searchWords.add(word.slice(0, -3)); // -ing
    }
  }
  
  const result = Array.from(searchWords).filter(word => word.length > 0);
  console.log('🔍 最終検索単語:', result);
  
  return result;
}

// 🔍 テキストにマッチする画像を検索
function findImageByMetaTag(text) {
  if (!text || !imageMetaTags.length) {
    console.log('🔍 検索条件不足:', { text, metaTagsLength: imageMetaTags.length });
    return null;
  }
  
  const searchWords = extractWordsWithStemming(text);
  console.log('🔍 検索単語:', searchWords);
  console.log('🔍 検索対象テキスト:', text);
  console.log('🔍 メタタグデータ件数:', imageMetaTags.length);
  
  let bestMatch = null;
  let bestPriority = 0;
  let matchDetails = [];
  
  for (const imageData of imageMetaTags) {
    for (const metaTag of imageData.meta_tags) {
      if (searchWords.includes(metaTag.toLowerCase())) {
        const priority = imageData.priority || 1;
        matchDetails.push({
          image: imageData.image_file,
          metaTag: metaTag,
          priority: priority
        });
        
        if (priority > bestPriority) {
          bestMatch = imageData;
          bestPriority = priority;
        }
        console.log('🎯 マッチング成功:', metaTag, '→', imageData.image_file, `(優先度: ${priority})`);
      }
    }
  }
  
  console.log('🔍 全マッチング結果:', matchDetails);
  console.log('🔍 最終選択:', bestMatch ? bestMatch.image_file : 'なし');
  
  // 確実にマッチしていることをアラートでも表示（デバッグ用）
  if (bestMatch) {
    console.log(`🎉 MATCH FOUND: "${text}" → ${bestMatch.image_file}`);
    
    // 重要なマッチの場合は強制アラート
    if (text.toLowerCase().includes('analyze') || text.toLowerCase().includes('engineer') || text.toLowerCase().includes('manager')) {
      // ブラウザアラートは使わず、ページ上に表示
      const debugDiv = document.getElementById('debug-match-info') || (() => {
        const div = document.createElement('div');
        div.id = 'debug-match-info';
        div.style.cssText = 'position: fixed; top: 10px; right: 10px; background: #28a745; color: white; padding: 10px; border-radius: 4px; z-index: 9999; max-width: 300px;';
        document.body.appendChild(div);
        return div;
      })();
      
      debugDiv.innerHTML = `🎉 MATCH: "${text}" → ${bestMatch.image_file}`;
      
      // 5秒後に削除
      setTimeout(() => {
        if (debugDiv.parentNode) {
          debugDiv.parentNode.removeChild(debugDiv);
        }
      }, 5000);
    }
  }
  
  return bestMatch;
}

// 🔍 テキストにマッチする全ての画像を検索（複数画像対応）
function findAllImagesByMetaTag(text) {
  if (!text || !imageMetaTags.length) {
    console.log('🔍 検索条件不足:', { text, metaTagsLength: imageMetaTags.length });
    return [];
  }
  
  const searchWords = extractWordsWithStemming(text);
  console.log('🔍 複数検索 - 検索単語:', searchWords);
  console.log('🔍 複数検索 - 検索対象テキスト:', text);
  
  let allMatches = [];
  const usedImages = new Set(); // 重複防止用
  
  // フレーズ全体での検索を最初に試行
  const phraseText = text.toLowerCase().trim();
  for (const imageData of imageMetaTags) {
    for (const metaTag of imageData.meta_tags) {
      if (metaTag.toLowerCase() === phraseText) {
        allMatches.push(imageData);
        usedImages.add(imageData.image_file);
        console.log('🎯 フレーズ完全マッチ:', metaTag, '→', imageData.image_file);
        return allMatches; // フレーズ全体でマッチした場合は即座に返す
      }
    }
  }
  
  // 個別単語でのマッチング（元の順序を保持）
  const individualWords = text.toLowerCase().split(/\s+/).filter(word => word.length >= 2);
  
  for (const word of individualWords) {
    let bestMatchForWord = null;
    let bestPriorityForWord = 0;
    
    for (const imageData of imageMetaTags) {
      // 既に使用済みの画像はスキップ
      if (usedImages.has(imageData.image_file)) {
        continue;
      }
      
      for (const metaTag of imageData.meta_tags) {
        // 個別単語との厳密マッチング
        if (metaTag.toLowerCase() === word.toLowerCase() || 
            (word.endsWith('ed') && metaTag.toLowerCase() === word.slice(0, -2).toLowerCase()) ||
            (word.endsWith('ing') && metaTag.toLowerCase() === word.slice(0, -3).toLowerCase()) ||
            (word.endsWith('s') && word.length > 2 && metaTag.toLowerCase() === word.slice(0, -1).toLowerCase())) {
          const priority = imageData.priority || 1;
          
          if (priority > bestPriorityForWord) {
            bestMatchForWord = imageData;
            bestPriorityForWord = priority;
          }
          console.log('🎯 個別単語マッチング成功:', metaTag, '→', imageData.image_file, `(優先度: ${priority})`);
        }
      }
    }
    
    // その単語に最もマッチする画像を追加
    if (bestMatchForWord) {
      allMatches.push(bestMatchForWord);
      usedImages.add(bestMatchForWord.image_file);
      console.log(`🎉 単語 "${word}" のマッチ追加:`, bestMatchForWord.image_file);
    }
  }
  
  console.log('🔍 全複数マッチング結果:', allMatches.map(m => m.image_file));
  return allMatches;
}

// 🖼️ 指定スロットに画像を適用
function applyImageToSlot(slotId, phraseText, forceRefresh = false) {
  console.log('🖼️ スロット画像適用開始:', slotId, '→', phraseText);
  
  // デバッグメッセージは無効化
  // displayDebugMessage(`🖼️ ${slotId}: "${phraseText}" 処理開始`);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.error('❌ スロットが見つかりません:', slotId);
    // displayDebugMessage(`❌ ${slotId}: スロット要素が見つかりません`, 'error');
    return;
  }
  
  const imgElement = slot.querySelector('.slot-image');
  if (!imgElement) {
    console.error('❌ スロット内に画像要素が見つかりません:', slotId);
    // displayDebugMessage(`❌ ${slotId}: 画像要素が見つかりません`, 'error');
    return;
  }
  
  console.log('🔍 現在の画像src:', imgElement.src);
  
  // テキストが空の場合はプレースホルダーを設定
  if (!phraseText || phraseText.trim() === '') {
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${slotId}`;
    console.log('📝 スロットテキストが空のため、プレースホルダーを設定:', slotId);
    // displayDebugMessage(`📝 ${slotId}: テキストが空、プレースホルダー設定`);
    return;
  }
  
  // 画像を検索
  const imageData = findImageByMetaTag(phraseText);
  console.log('🔍 検索結果:', imageData);
  
  if (!imageData) {
    console.log('🔍 マッチする画像が見つかりません:', phraseText);
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${slotId}`;
    // displayDebugMessage(`🔍 ${slotId}: "${phraseText}" マッチなし`, 'warning');
    return;
  }
  
  // 新しい画像パスを構築（URLエンコーディング対応）
  const encodedImageFile = encodeURIComponent(imageData.image_file);
  const newImagePath = `slot_images/${imageData.folder}/${encodedImageFile}`;
  console.log('🎨 新しい画像パス:', newImagePath);
  console.log('🔤 元ファイル名:', imageData.image_file);
  console.log('🔤 エンコード後:', encodedImageFile);
  // displayDebugMessage(`🎨 ${slotId}: "${phraseText}" → ${imageData.image_file}`);
  
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
    // displayDebugMessage(`✅ ${slotId}: 画像読み込み完了`, 'success');
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
  
  // 画像読み込みエラー時の処理
  imgElement.onerror = function() {
    console.error('❌ 画像読み込みエラー:', newImagePath);
    // displayDebugMessage(`❌ ${slotId}: 画像読み込みエラー - ${imageData.image_file}`, 'error');
    this.src = 'slot_images/common/placeholder.png';
  };
  
  console.log('🎨 スロット画像更新完了:', slotId, '→', phraseText, '→', newImagePath);
  console.log('🎨 更新後の画像src:', imgElement.src);
}

// 🖼️ 指定スロットに複数画像を適用（新機能）
function applyMultipleImagesToSlot(slotId, phraseText, forceRefresh = false) {
  console.log('🖼️ 複数スロット画像適用開始:', slotId, '→', phraseText);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.error('❌ スロットが見つかりません:', slotId);
    return;
  }

  // テキストが空の場合は複数画像コンテナを完全削除して通常の単一画像処理に戻す
  if (!phraseText || phraseText.trim() === '') {
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
      console.log('🧹 テキストが空のため複数画像コンテナを削除:', slotId);
    }
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
      singleImg.style.opacity = '1';
    }
    
    // スロット全体の横幅をリセット
    slot.style.maxWidth = '';
    slot.style.width = '';
    
    // 単一画像にplaceholder.pngを設定（空テキスト処理）
    applyImageToSlot(slotId, phraseText, forceRefresh);
    return;
  }

  // 複数の画像を検索
  const imageDataArray = findAllImagesByMetaTag(phraseText);
  console.log('🔍 複数検索結果:', imageDataArray);

  // マッチする画像がない場合は複数画像コンテナを完全削除して通常の処理に戻す
  if (imageDataArray.length === 0) {
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
      console.log('🧹 マッチなしのため複数画像コンテナを削除:', slotId);
    }
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
      singleImg.style.opacity = '1';
    }
    
    // スロット全体の横幅をリセット
    slot.style.maxWidth = '';
    slot.style.width = '';
    
    // 単一画像にplaceholder.pngまたはマッチ結果を設定
    applyImageToSlot(slotId, phraseText, forceRefresh);
    return;
  }

  // 1個しかマッチしない場合は複数画像コンテナを完全削除して通常の処理に戻す
  if (imageDataArray.length === 1) {
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
      console.log('🧹 単一マッチのため複数画像を削除:', slotId);
    }
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
      singleImg.style.opacity = '1';
    }
    
    // スロット全体の横幅をリセット
    slot.style.maxWidth = '';
    slot.style.width = '';
    
    // 単一画像にマッチした画像を設定
    applyImageToSlot(slotId, phraseText, forceRefresh);
    return;
  }

  // 複数画像対応：画像コンテナを作成
  let imageContainer = slot.querySelector('.multi-image-container');
  if (!imageContainer) {
    // 既存の単一画像を確実に非表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'none';
      singleImg.style.visibility = 'hidden';
    }

    // 複数画像用のコンテナを作成
    imageContainer = document.createElement('div');
    imageContainer.className = 'multi-image-container';
    
    // Grid Layout対応のスタイルを設定
    imageContainer.style.cssText = `
      grid-row: 2;
      grid-column: 1;
      display: flex !important;
      gap: 6px;
      align-items: center;
      justify-content: center;
      flex-wrap: nowrap !important;
      width: 100%;
      height: 180px !important;
      padding: 5px;
      box-sizing: border-box;
      border-radius: 4px;
      background: rgba(40, 167, 69, 0.05);
      border: 1px dashed rgba(40, 167, 69, 0.3);
      visibility: visible !important;
      opacity: 1 !important;
      overflow: hidden;
    `;
    slot.appendChild(imageContainer);
  }

  // 既存の画像をクリア
  imageContainer.innerHTML = '';

  // 各画像を追加
  imageDataArray.forEach((imageData, index) => {
    const imgElement = document.createElement('img');
    const encodedImageFile = encodeURIComponent(imageData.image_file);
    const imagePath = `slot_images/${imageData.folder}/${encodedImageFile}`;
    const cacheBuster = Date.now() + index; // 各画像に個別のキャッシュバスター
    
    imgElement.src = `${imagePath}?t=${cacheBuster}`;
    imgElement.alt = `image ${index + 1} for ${slotId}: ${imageData.description || phraseText}`;
    imgElement.className = 'slot-multi-image';
    
    // 🎯 画像枚数に応じた動的サイズ調整システム
    const imageCount = imageDataArray.length;
    const baseContainerWidth = 390; // 基本スロット幅（1枚用）
    const minImageWidth = 50; // 画像1枚の最小幅
    const maxImageWidth = 120; // 画像1枚の最大幅
    const gap = 6; // 画像間の隙間
    
    // 🆕 スロット全体の横幅を画像枚数に応じて拡大
    const expandedContainerWidth = baseContainerWidth + (imageCount - 1) * 80; // 1枚増えるごとに+80px
    const totalGapWidth = (imageCount - 1) * gap;
    const availableWidth = expandedContainerWidth - totalGapWidth - 20; // padding等を考慮
    const dynamicWidth = Math.min(maxImageWidth, Math.max(minImageWidth, Math.floor(availableWidth / imageCount)));
    
    // 🆕 スロット全体の横幅を動的に設定
    slot.style.maxWidth = `${expandedContainerWidth}px`;
    slot.style.width = 'auto';
    
    console.log(`🎯 スロット拡大: ${imageCount}枚 → 容器幅 ${expandedContainerWidth}px, 各画像幅 ${dynamicWidth}px`);
    
    // 複数画像用のスタイル - 動的サイズ適用
    imgElement.style.cssText = `
      height: 160px !important;
      width: ${dynamicWidth}px !important;
      max-width: ${dynamicWidth}px !important;
      min-width: 50px !important;
      border-radius: 5px;
      border: 1px solid rgba(40, 167, 69, 0.6);
      object-fit: fill !important;
      display: block;
      visibility: visible;
      opacity: 1;
      flex-shrink: 1;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    `;

    // ホバー効果を追加
    imgElement.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.05)';
      this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.2)';
      this.style.borderColor = 'rgba(40, 167, 69, 0.8)';
    });

    imgElement.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
      this.style.boxShadow = 'none';
      this.style.borderColor = 'rgba(40, 167, 69, 0.6)';
    });

    console.log(`🎯 画像 ${index + 1}/${imageCount}: 動的幅 ${dynamicWidth}px`);

    // メタタグ属性を設定
    imgElement.setAttribute('data-meta-tag', 'true');
    imgElement.setAttribute('data-image-index', index);

    // 画像読み込み完了処理
    imgElement.onload = function() {
      console.log(`🎨 複数画像 ${index + 1} 読み込み完了:`, imagePath);
      this.style.display = 'block';
      this.style.visibility = 'visible';
      this.style.opacity = '1';
    };

    // 画像読み込みエラー処理
    imgElement.onerror = function() {
      console.error(`❌ 複数画像 ${index + 1} 読み込みエラー:`, imagePath);
      this.src = 'slot_images/common/placeholder.png';
    };

    imageContainer.appendChild(imgElement);
  });

  console.log(`🎨 複数画像表示完了: ${slotId} → ${imageDataArray.length}枚`);
}

// 🖼️ サブスロット用単一画像表示関数（従来機能を分離）
function applySingleImageToSubslot(subslotId, phraseText) {
  console.log('🖼️ サブスロット単一画像適用開始:', subslotId, '→', phraseText);
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.error('❌ サブスロット要素が見つかりません:', subslotId);
    return;
  }

  // 複数画像コンテナがあれば削除
  const existingContainer = subslot.querySelector('.multi-image-container');
  if (existingContainer) {
    existingContainer.remove();
    console.log('🧹 サブスロット：単一画像のため複数画像コンテナを削除:', subslotId);
  }

  // 既存の画像要素を探す
  let imgElement = subslot.querySelector('.slot-image');
  
  // 画像要素がない場合は動的に作成
  if (!imgElement) {
    console.log('📱 サブスロット画像要素を動的作成:', subslotId);
    imgElement = document.createElement('img');
    imgElement.className = 'slot-image';
    imgElement.alt = `image for ${subslotId}`;
    imgElement.style.cssText = `
      width: 180px;
      height: 180px;
      border-radius: 4px;
      border: 1px solid #ddd;
      object-fit: cover;
      display: block;
      margin: 5px 0;
    `;
    
    // ラベルの直後に画像要素を挿入
    const label = subslot.querySelector('label');
    if (label && label.nextSibling) {
      subslot.insertBefore(imgElement, label.nextSibling);
    } else {
      // ラベルがない場合は先頭に挿入
      subslot.insertBefore(imgElement, subslot.firstChild);
    }
    
    console.log('✅ サブスロット画像要素を動的作成・挿入完了:', subslotId);
  }

  // 単一画像を再表示
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  
  // サブスロット全体の横幅をリセット
  subslot.style.maxWidth = '';
  subslot.style.width = '';
  
  console.log('🔍 サブスロット画像要素発見:', imgElement);
  console.log('🔍 サブスロット現在の画像src:', imgElement.src);
  
  // テキストが空の場合はプレースホルダーを設定
  if (!phraseText || phraseText.trim() === '') {
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${subslotId}`;
    console.log('📝 サブスロットテキストが空のため、プレースホルダーを設定:', subslotId);
    return;
  }
  
  // 画像を検索（英語テキストのみ）
  let imageData = findImageByMetaTag(phraseText);
  console.log('🔍 サブスロット検索結果:', imageData);
  
  if (!imageData) {
    console.log('🔍 サブスロット：マッチする画像が見つかりません:', phraseText);
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${subslotId}`;
    return;
  }
  
  // 新しい画像パスを構築
  const encodedImageFile = encodeURIComponent(imageData.image_file);
  const newImagePath = `slot_images/${imageData.folder}/${encodedImageFile}`;
  console.log('🎨 サブスロット新しい画像パス:', newImagePath);
  
  // 画像を更新（キャッシュバスター付き）
  const cacheBuster = Date.now();
  const imageUrlWithCacheBuster = `${newImagePath}?t=${cacheBuster}`;
  
  imgElement.src = imageUrlWithCacheBuster;
  imgElement.alt = `image for ${subslotId}: ${imageData.description || phraseText}`;
  
  console.log('🔄 サブスロット キャッシュバスター付きURL:', imageUrlWithCacheBuster);
  
  // 強制的に表示状態にする
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  
  // image_auto_hide.js対策：data-meta-tag属性を設定
  imgElement.setAttribute('data-meta-tag', 'true');
  imgElement.setAttribute('data-meta-tag-applied', imageData.meta_tags[0] || 'unknown');
  imgElement.setAttribute('data-applied-text', phraseText);
  
  // 🆕 競合対策：定期的な強制表示チェック
  const forceDisplayInterval = setInterval(() => {
    if (imgElement.style.display === 'none' || imgElement.style.visibility === 'hidden' || 
        imgElement.classList.contains('auto-hidden-image')) {
      console.log('🛡️ 画像が隠されました。強制再表示:', subslotId);
      imgElement.style.display = 'block';
      imgElement.style.visibility = 'visible';
      imgElement.style.opacity = '1';
      imgElement.classList.remove('auto-hidden-image');
    }
  }, 100);
  
  // 3秒後にインターバルを停止
  setTimeout(() => {
    clearInterval(forceDisplayInterval);
    console.log('🛡️ 強制表示監視を終了:', subslotId);
  }, 3000);
  
  // 画像読み込み完了後に再度表示を確認
  imgElement.onload = function() {
    console.log('🎨 サブスロット画像読み込み完了:', newImagePath);
    this.style.display = 'block';
    this.style.visibility = 'visible';
    this.style.opacity = '1';
    
    console.log('🛡️ サブスロット最終表示状態:', {
      subslotId: subslotId,
      src: this.src,
      display: this.style.display,
      visibility: this.style.visibility,
      opacity: this.style.opacity
    });
  };
  
  // 画像読み込みエラー時の処理
  imgElement.onerror = function() {
    console.error('❌ サブスロット画像読み込みエラー:', newImagePath);
    this.src = 'slot_images/common/placeholder.png';
  };
  
  console.log('🎨 サブスロット画像更新完了:', subslotId, '→', phraseText, '→', newImagePath);
}

// 🎯 サブスロット表示時の画像更新を処理（タイミング調整付き）
function handleSubslotDisplay(parentSlotId) {
  console.log('🎭 サブスロット表示処理開始:', parentSlotId);
  
  // メタタグが読み込まれていない場合は待機
  if (imageMetaTags.length === 0) {
    console.log('⏳ メタタグ読み込み待機中...');
    setTimeout(() => handleSubslotDisplay(parentSlotId), 100);
    return;
  }
  
  // 🆕 複数段階の遅延実行でタイミング競合を回避
  console.log('⏱️ タイミング調整開始: 他システムの処理完了を待機');
  
  // 段階1: 100ms後 - 基本的なDOM生成完了待ち
  setTimeout(() => {
    console.log('⏱️ 段階1: 基本処理完了後の画像適用');
    updateSubslotImages(parentSlotId);
  }, 100);
  
  // 段階2: 300ms後 - insert_test_data_clean.js等の処理完了後
  setTimeout(() => {
    console.log('⏱️ 段階2: データ同期処理完了後の画像再適用');
    updateSubslotImages(parentSlotId);
  }, 300);
  
  // 段階3: 600ms後 - 最終確認・強制適用
  setTimeout(() => {
    console.log('⏱️ 段階3: 最終確認・強制画像適用');
    updateSubslotImages(parentSlotId);
  }, 600);
}

// 🔍 サブスロット画像の状態を監視する関数（デバッグ用）
function monitorSubslotImageState(subslotId, duration = 5000) {
  console.log(`🔍 画像状態監視開始: ${subslotId} (${duration}ms間)`);
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.warn(`⚠️ 監視対象が見つかりません: ${subslotId}`);
    return;
  }
  
  // 🆕 MutationObserverで要素の変更を監視
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'attributes') {
        console.log(`🔍 ${subslotId} 属性変更:`, {
          attributeName: mutation.attributeName,
          oldValue: mutation.oldValue,
          newValue: mutation.target.getAttribute(mutation.attributeName)
        });
      } else if (mutation.type === 'childList') {
        console.log(`🔍 ${subslotId} 子要素変更:`, {
          addedNodes: mutation.addedNodes.length,
          removedNodes: mutation.removedNodes.length
        });
      }
    });
  });
  
  observer.observe(subslot, {
    attributes: true,
    attributeOldValue: true,
    childList: true,
    subtree: true
  });
  
  const startTime = Date.now();
  const checkInterval = setInterval(() => {
    const imgElement = subslot.querySelector('.slot-image');
    if (imgElement) {
      const computedStyle = window.getComputedStyle(imgElement);
      const isVisible = computedStyle.display !== 'none' && 
                       computedStyle.visibility !== 'hidden' && 
                       computedStyle.opacity !== '0';
      
      console.log(`🔍 ${subslotId} 画像状態:`, {
        src: imgElement.src.split('/').pop(),
        display: computedStyle.display,
        visibility: computedStyle.visibility,
        opacity: computedStyle.opacity,
        isVisible: isVisible,
        timestamp: Date.now() - startTime + 'ms'
      });
      
      if (!isVisible) {
        console.warn(`⚠️ 画像が非表示になりました: ${subslotId}`);
        console.log(`🔍 非表示時の要素:`, imgElement);
        console.log(`🔍 非表示時の親要素:`, subslot);
      }
    } else {
      console.warn(`⚠️ 画像要素が見つかりません: ${subslotId}`);
    }
    
    if (Date.now() - startTime >= duration) {
      clearInterval(checkInterval);
      observer.disconnect();
      console.log(`✅ 監視終了: ${subslotId}`);
    }
  }, 100);
}

// 🧪 デバッグ用：サブスロット強制画像更新（コンソールから実行）
function forceUpdateSubslotImages() {
  console.log('🧪 === サブスロット強制更新テスト開始 ===');
  
  // C1サブスロットコンテナを強制表示
  const c1Container = document.getElementById('slot-c1-sub');
  if (c1Container) {
    c1Container.style.display = 'block';
    console.log('🔧 C1サブスロットコンテナを強制表示');
  }
  
  // メタタグ確認
  console.log('📊 メタタグデータ:', imageMetaTags?.length);
  console.log('📊 fullSlotPoolデータ:', window.fullSlotPool?.length);
  
  // データ構造の確認
  if (window.fullSlotPool && window.fullSlotPool.length > 0) {
    const sampleSubslot = window.fullSlotPool.find(entry => entry.SubslotID);
    if (sampleSubslot) {
      console.log('📋 サブスロットデータサンプル:', sampleSubslot);
    }
  }
  
  // サブスロット画像更新実行（複数段階）
  console.log('🧪 段階的更新テスト実行...');
  updateSubslotImages('c1');
  
  setTimeout(() => {
    console.log('🧪 300ms後の再更新...');
    updateSubslotImages('c1');
  }, 300);
  
  setTimeout(() => {
    console.log('🧪 600ms後の最終更新...');
    updateSubslotImages('c1');
  }, 600);
  
  // 個別テスト（実際に存在するサブスロットのみ）
  console.log('🧪 個別テスト実行...');
  
  // 実際に存在するサブスロットを取得
  const testContainer = document.getElementById('slot-c1-sub');
  if (testContainer) {
    const existingSubslots = [];
    Array.from(testContainer.children).forEach(child => {
      if (child.id && child.id.includes('sub')) {
        existingSubslots.push(child.id);
      }
    });
    
    console.log('🧪 存在するサブスロット:', existingSubslots);
    
    // 存在するサブスロットのみテスト
    existingSubslots.forEach((subslotId, index) => {
      setTimeout(() => {
        console.log(`🧪 テスト中: ${subslotId}`);
        
        // サブスロット種別に応じたテストテキストを選択
        let testText = 'analyze'; // デフォルト
        if (subslotId.includes('-v')) testText = 'figure out';
        else if (subslotId.includes('-m1')) testText = 'manager';
        else if (subslotId.includes('-s')) testText = 'everyone';
        else if (subslotId.includes('-o1')) testText = 'engineer';
        
        applyImageToSubslot(subslotId, testText);
        monitorSubslotImageState(subslotId, 3000);
      }, index * 100);
    });
  }
  
  console.log('🧪 === テスト完了 ===');
}

// 🧪 C1サブスロット画像消失問題の詳細デバッグ
function debugImageDisappearance() {
  console.log('🔍 === C1サブスロット画像消失デバッグ開始 ===');
  
  const container = document.getElementById('slot-c1-sub');
  if (!container) {
    console.error('❌ C1サブスロットコンテナが見つかりません');
    return;
  }
  
  // 実際に存在するサブスロットを特定
  const existingSubslots = [];
  Array.from(container.children).forEach(child => {
    if (child.id && child.id.includes('sub')) {
      existingSubslots.push(child.id);
    }
  });
  
  console.log('📋 存在するサブスロット:', existingSubslots);
  
  if (existingSubslots.length === 0) {
    console.warn('⚠️ サブスロット要素が見つかりません');
    return;
  }
  
  // 最初の存在するサブスロットで詳細テスト
  const testSubslotId = existingSubslots[0];
  console.log(`🎯 テスト対象: ${testSubslotId}`);
  
  // 詳細監視開始
  monitorSubslotImageState(testSubslotId, 10000);
  
  // 画像適用
  console.log('🖼️ 画像適用実行...');
  applyImageToSubslot(testSubslotId, 'analyze');
  
  // 1秒後に再確認
  setTimeout(() => {
    const subslot = document.getElementById(testSubslotId);
    const imgElement = subslot?.querySelector('.slot-image');
    if (imgElement) {
      console.log('🔍 1秒後の画像状態:', {
        src: imgElement.src,
        display: imgElement.style.display,
        visibility: imgElement.style.visibility,
        opacity: imgElement.style.opacity
      });
    }
  }, 1000);
}

// 🧪 デバッグ用：サブスロット画像状態確認
function debugSubslotImages() {
  console.log('🧪 === サブスロット画像状態確認 ===');
  
  // メタタグ状態確認
  console.log('📊 メタタグデータ:', imageMetaTags?.length || 'なし');
  if (imageMetaTags && imageMetaTags.length > 0) {
    console.log('📋 メタタグサンプル:', imageMetaTags.slice(0, 3));
  }
  
  // C1サブスロット確認
  const c1Container = document.getElementById('slot-c1-sub');
  console.log('🔍 C1サブスロットコンテナ:', c1Container ? 'あり' : 'なし');
  
  if (c1Container) {
    console.log('🔍 C1コンテナ表示状態:', window.getComputedStyle(c1Container).display);
    
    // 実際のサブスロット要素を確認
    const subslots = Array.from(c1Container.children).filter(child => 
      child.id && child.id.includes('sub')
    );
    
    console.log(`🔍 実際のサブスロット数: ${subslots.length}`);
    
    subslots.forEach(subslot => {
      const phraseEl = subslot.querySelector('.slot-phrase');
      const textEl = subslot.querySelector('.slot-text');
      const imgEl = subslot.querySelector('.slot-image');
      const multiContainer = subslot.querySelector('.multi-image-container');
      
      console.log(`📝 ${subslot.id}:`);
      console.log(`  phrase: "${phraseEl?.textContent?.trim() || 'なし'}"`);
      console.log(`  text: "${textEl?.textContent?.trim() || 'なし'}"`);
      console.log(`  画像要素: ${imgEl ? 'あり' : 'なし'}`);
      console.log(`  複数画像コンテナ: ${multiContainer ? 'あり' : 'なし'}`);
      
      if (imgEl) {
        console.log(`  画像src: ${imgEl.src}`);
        console.log(`  画像表示: ${imgEl.style.display || window.getComputedStyle(imgEl).display}`);
      }
    });
  }
  
  // fullSlotPool確認
  console.log('📊 fullSlotPool:', window.fullSlotPool?.length || 'なし');
  if (window.fullSlotPool && window.fullSlotPool.length > 0) {
    const c1Subslots = window.fullSlotPool.filter(entry => 
      entry.SubslotID && entry.SubslotID.includes('c1-sub')
    );
    console.log(`📋 C1サブスロットデータ数: ${c1Subslots.length}`);
    if (c1Subslots.length > 0) {
      console.log('📋 C1サブスロットデータサンプル:', c1Subslots.slice(0, 3));
    }
  }
}

// 🧪 デバッグ用：簡単なサブスロット画像テスト
function testSubslotImageSimple(subslotId, testText) {
  console.log(`🧪 簡単テスト開始: ${subslotId} → "${testText}"`);
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.error(`❌ サブスロット要素が見つかりません: ${subslotId}`);
    return;
  }
  
  console.log('✅ サブスロット要素発見');
  
  // メタタグ確認
  if (!imageMetaTags || imageMetaTags.length === 0) {
    console.error('❌ メタタグデータがありません');
    return;
  }
  
  console.log('✅ メタタグデータあり');
  
  // 画像検索
  const imageData = findImageByMetaTag(testText);
  console.log('🔍 検索結果:', imageData);
  
  if (!imageData) {
    console.warn('⚠️ マッチする画像がありません');
    return;
  }
  
  console.log('✅ 画像データ取得成功');
  
  // 画像要素確認
  let imgElement = subslot.querySelector('.slot-image');
  if (!imgElement) {
    console.log('📱 画像要素を動的作成');
    imgElement = document.createElement('img');
    imgElement.className = 'slot-image';
    imgElement.style.cssText = `
      width: 180px;
      height: 180px;
      border-radius: 4px;
      border: 1px solid #ddd;
      object-fit: cover;
      display: block;
      margin: 5px 0;
    `;
    subslot.appendChild(imgElement);
  }
  
  // 画像設定
  const encodedImageFile = encodeURIComponent(imageData.image_file);
  const imagePath = `slot_images/${imageData.folder}/${encodedImageFile}`;
  const cacheBuster = Date.now();
  
  imgElement.src = `${imagePath}?t=${cacheBuster}`;
  imgElement.alt = `image for ${subslotId}`;
  imgElement.setAttribute('data-meta-tag', 'true');
  
  console.log('🎨 画像設定完了:', imagePath);
}

// 🎯 サブスロット専用画像適用関数（既存システムと完全独立）
function applyImageToSubslot(subslotId, phraseText) {
  console.log('🖼️ サブスロット画像適用開始:', subslotId, '→', phraseText);
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.error('❌ サブスロット要素が見つかりません:', subslotId);
    return;
  }

  // テキストが空の場合の処理
  if (!phraseText || phraseText.trim() === '') {
    // 複数画像コンテナがあれば削除
    const existingContainer = subslot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
      console.log('🧹 サブスロット：テキストが空のため複数画像コンテナを削除:', subslotId);
    }
    
    // 単一画像にプレースホルダーを設定
    let imgElement = subslot.querySelector('.slot-image');
    if (imgElement) {
      imgElement.style.display = 'block';
      imgElement.src = 'slot_images/common/placeholder.png';
      imgElement.alt = `image for ${subslotId}`;
    }
    console.log('📝 サブスロットテキストが空のため、プレースホルダーを設定:', subslotId);
    return;
  }

  // 複数の画像を検索
  const imageDataArray = findAllImagesByMetaTag(phraseText);
  console.log('🔍 サブスロット複数検索結果:', imageDataArray);

  // 複数画像が見つかった場合（2個以上）
  if (imageDataArray.length >= 2) {
    console.log('🎯 サブスロット複数画像表示開始:', imageDataArray.length, '個');
    applyMultipleImagesToSubslot(subslotId, imageDataArray, phraseText);
    return;
  }

  // 単一画像またはマッチなしの場合は従来の処理
  applySingleImageToSubslot(subslotId, phraseText);
}

// 🖼️ サブスロット用複数画像表示関数（新機能）
function applyMultipleImagesToSubslot(subslotId, imageDataArray, phraseText) {
  console.log('🖼️ サブスロット複数画像適用開始:', subslotId, '→', imageDataArray.length, '個');
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.error('❌ サブスロット要素が見つかりません:', subslotId);
    return;
  }

  // 既存の単一画像を非表示
  const singleImg = subslot.querySelector('.slot-image');
  if (singleImg) {
    singleImg.style.display = 'none';
    singleImg.style.visibility = 'hidden';
  }

  // 複数画像用のコンテナを作成または取得
  let imageContainer = subslot.querySelector('.multi-image-container');
  if (!imageContainer) {
    imageContainer = document.createElement('div');
    imageContainer.className = 'multi-image-container';
    
    // サブスロット用のスタイルを設定（より小さく）
    imageContainer.style.cssText = `
      display: flex !important;
      gap: 4px;
      align-items: center;
      justify-content: center;
      flex-wrap: nowrap !important;
      width: 100%;
      height: 140px !important;
      padding: 3px;
      box-sizing: border-box;
      border-radius: 4px;
      background: rgba(40, 167, 69, 0.05);
      border: 1px dashed rgba(40, 167, 69, 0.3);
      visibility: visible !important;
      opacity: 1 !important;
      overflow: hidden;
      margin: 5px 0;
    `;
    subslot.appendChild(imageContainer);
  }

  // 既存の画像をクリア
  imageContainer.innerHTML = '';

  // 各画像を追加
  imageDataArray.forEach((imageData, index) => {
    const imgElement = document.createElement('img');
    const encodedImageFile = encodeURIComponent(imageData.image_file);
    const imagePath = `slot_images/${imageData.folder}/${encodedImageFile}`;
    const cacheBuster = Date.now() + index; // 各画像に個別のキャッシュバスター
    
    imgElement.src = `${imagePath}?t=${cacheBuster}`;
    imgElement.alt = `image ${index + 1} for ${subslotId}: ${imageData.description || phraseText}`;
    imgElement.className = 'slot-multi-image subslot-multi-image';
    
    // 🎯 サブスロット用画像枚数に応じた動的サイズ調整システム
    const imageCount = imageDataArray.length;
    const baseContainerWidth = 180; // サブスロット基本幅（上位スロットより小さく）
    const minImageWidth = 35; // 画像1枚の最小幅
    const maxImageWidth = 80; // 画像1枚の最大幅
    const gap = 4; // 画像間の隙間
    
    // サブスロット全体の横幅を画像枚数に応じて拡大
    const expandedContainerWidth = baseContainerWidth + (imageCount - 1) * 50; // 1枚増えるごとに+50px
    const totalGapWidth = (imageCount - 1) * gap;
    const availableWidth = expandedContainerWidth - totalGapWidth - 10; // padding等を考慮
    const dynamicWidth = Math.min(maxImageWidth, Math.max(minImageWidth, Math.floor(availableWidth / imageCount)));
    
    // サブスロット全体の横幅を動的に設定
    subslot.style.maxWidth = `${expandedContainerWidth}px`;
    subslot.style.width = 'auto';
    
    console.log(`🎯 サブスロット拡大: ${imageCount}枚 → 容器幅 ${expandedContainerWidth}px, 各画像幅 ${dynamicWidth}px`);
    
    // サブスロット複数画像用のスタイル - 動的サイズ適用
    imgElement.style.cssText = `
      height: 120px !important;
      width: ${dynamicWidth}px !important;
      max-width: ${dynamicWidth}px !important;
      min-width: 35px !important;
      border-radius: 3px;
      border: 1px solid rgba(40, 167, 69, 0.6);
      object-fit: fill !important;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      cursor: pointer;
      flex-shrink: 0;
      margin: 0;
      padding: 0;
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
    `;

    // ホバー効果
    imgElement.addEventListener('mouseenter', () => {
      imgElement.style.transform = 'scale(1.05)';
      imgElement.style.boxShadow = '0 4px 8px rgba(0,0,0,0.3)';
      imgElement.style.zIndex = '10';
    });

    imgElement.addEventListener('mouseleave', () => {
      imgElement.style.transform = 'scale(1)';
      imgElement.style.boxShadow = 'none';
      imgElement.style.zIndex = '1';
    });

    // image_auto_hide.js対策：data-meta-tag属性を設定
    imgElement.setAttribute('data-meta-tag', 'true');
    imgElement.setAttribute('data-meta-tag-applied', imageData.meta_tags[0] || 'unknown');
    imgElement.setAttribute('data-applied-text', phraseText);

    // エラーハンドリング
    imgElement.addEventListener('error', () => {
      console.error('❌ サブスロット画像読み込み失敗:', imagePath);
      imgElement.src = 'slot_images/common/placeholder.png';
    });

    imageContainer.appendChild(imgElement);
    console.log(`✅ サブスロット複数画像追加 ${index + 1}/${imageCount}:`, imageData.image_file);
  });

  // 競合対策：3秒間監視して表示状態を維持（image_auto_hide.js対策）
  const forceShowInterval = setInterval(() => {
    const images = imageContainer.querySelectorAll('.subslot-multi-image');
    images.forEach(img => {
      if (img.style.display === 'none' || 
          img.classList.contains('auto-hidden-image')) {
        img.style.display = 'block';
        img.style.visibility = 'visible';
        img.style.opacity = '1';
        img.classList.remove('auto-hidden-image');
        console.log(`🔧 サブスロット複数画像の表示を強制維持: ${subslotId}`);
      }
    });
  }, 100);
  
  // 3秒後に監視終了
  setTimeout(() => clearInterval(forceShowInterval), 3000);

  console.log('✅ サブスロット複数画像表示完了:', subslotId, imageDataArray.length, '個');
}

// 🖼️ サブスロット用単一画像表示関数（従来機能を分離）
function applySingleImageToSubslot(subslotId, phraseText) {
  console.log('🖼️ サブスロット単一画像適用開始:', subslotId, '→', phraseText);
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.error('❌ サブスロット要素が見つかりません:', subslotId);
    return;
  }

  // 複数画像コンテナがあれば削除
  const existingContainer = subslot.querySelector('.multi-image-container');
  if (existingContainer) {
    existingContainer.remove();
    console.log('🧹 サブスロット：単一画像のため複数画像コンテナを削除:', subslotId);
  }

  // 既存の画像要素を探す
  let imgElement = subslot.querySelector('.slot-image');
  
  // 画像要素がない場合は動的に作成
  if (!imgElement) {
    console.log('📱 サブスロット画像要素を動的作成:', subslotId);
    imgElement = document.createElement('img');
    imgElement.className = 'slot-image';
    imgElement.alt = `image for ${subslotId}`;
    imgElement.style.cssText = `
      width: 180px;
      height: 180px;
      border-radius: 4px;
      border: 1px solid #ddd;
      object-fit: cover;
      display: block;
      margin: 5px 0;
    `;
    
    // ラベルの直後に画像要素を挿入
    const label = subslot.querySelector('label');
    if (label && label.nextSibling) {
      subslot.insertBefore(imgElement, label.nextSibling);
    } else {
      // ラベルがない場合は先頭に挿入
      subslot.insertBefore(imgElement, subslot.firstChild);
    }
    
    console.log('✅ サブスロット画像要素を動的作成・挿入完了:', subslotId);
  }

  // 単一画像を再表示
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  
  // サブスロット全体の横幅をリセット
  subslot.style.maxWidth = '';
  subslot.style.width = '';
  
  console.log('🔍 サブスロット画像要素発見:', imgElement);
  console.log('🔍 サブスロット現在の画像src:', imgElement.src);
  
  // テキストが空の場合はプレースホルダーを設定
  if (!phraseText || phraseText.trim() === '') {
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${subslotId}`;
    console.log('📝 サブスロットテキストが空のため、プレースホルダーを設定:', subslotId);
    return;
  }
  
  // 画像を検索（英語テキストのみ）
  let imageData = findImageByMetaTag(phraseText);
  console.log('🔍 サブスロット検索結果:', imageData);
  
  if (!imageData) {
    console.log('🔍 サブスロット：マッチする画像が見つかりません:', phraseText);
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${subslotId}`;
    return;
  }
  
  // 新しい画像パスを構築
  const encodedImageFile = encodeURIComponent(imageData.image_file);
  const newImagePath = `slot_images/${imageData.folder}/${encodedImageFile}`;
  console.log('🎨 サブスロット新しい画像パス:', newImagePath);
  
  // 画像を更新（キャッシュバスター付き）
  const cacheBuster = Date.now();
  const imageUrlWithCacheBuster = `${newImagePath}?t=${cacheBuster}`;
  
  imgElement.src = imageUrlWithCacheBuster;
  imgElement.alt = `image for ${subslotId}: ${imageData.description || phraseText}`;
  
  console.log('🔄 サブスロット キャッシュバスター付きURL:', imageUrlWithCacheBuster);
  
  // 強制的に表示状態にする
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  
  // image_auto_hide.js対策：data-meta-tag属性を設定
  imgElement.setAttribute('data-meta-tag', 'true');
  imgElement.setAttribute('data-meta-tag-applied', imageData.meta_tags[0] || 'unknown');
  imgElement.setAttribute('data-applied-text', phraseText);
  
  // 🆕 競合対策：定期的な強制表示チェック
  const forceDisplayInterval = setInterval(() => {
    if (imgElement.style.display === 'none' || imgElement.style.visibility === 'hidden' || 
        imgElement.classList.contains('auto-hidden-image')) {
      console.log('🛡️ 画像が隠されました。強制再表示:', subslotId);
      imgElement.style.display = 'block';
      imgElement.style.visibility = 'visible';
      imgElement.style.opacity = '1';
      imgElement.classList.remove('auto-hidden-image');
    }
  }, 100);
  
  // 3秒後にインターバルを停止
  setTimeout(() => {
    clearInterval(forceDisplayInterval);
    console.log('🛡️ 強制表示監視を終了:', subslotId);
  }, 3000);
  
  // 画像読み込み完了後に再度表示を確認
  imgElement.onload = function() {
    console.log('🎨 サブスロット画像読み込み完了:', newImagePath);
    this.style.display = 'block';
    this.style.visibility = 'visible';
    this.style.opacity = '1';
    
    console.log('🛡️ サブスロット最終表示状態:', {
      subslotId: subslotId,
      src: this.src,
      display: this.style.display,
      visibility: this.style.visibility,
      opacity: this.style.opacity
    });
  };
  
  // 画像読み込みエラー時の処理
  imgElement.onerror = function() {
    console.error('❌ サブスロット画像読み込みエラー:', newImagePath);
    this.src = 'slot_images/common/placeholder.png';
  };
  
  console.log('🎨 サブスロット画像更新完了:', subslotId, '→', phraseText, '→', newImagePath);
}

// 🔧 グローバル公開関数
window.clearMultiImageContainer = clearMultiImageContainer;

// 🖼️ サブスロット用公開関数
window.applyImageToSubslot = applyImageToSubslot;
window.applyMultipleImagesToSubslot = applyMultipleImagesToSubslot;
window.applySingleImageToSubslot = applySingleImageToSubslot;

// 🧪 デバッグ用公開関数
window.debugSubslotImages = debugSubslotImages;
window.testSubslotImageSimple = testSubslotImageSimple;

// 🔄 旧V専用システムとの互換性維持
window.updateVSlotImage = function(forceRefresh = false) {
  updateSlotImage('slot-v', forceRefresh);
};
window.updateVSlotImageAfterDataChange = function() {
  updateSlotImage('slot-v', true);
};
