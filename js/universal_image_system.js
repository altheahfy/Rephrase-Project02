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

// 🚀 全スロットの画像更新（個別呼び出し用）
function updateSlotImage(slotId, forceRefresh = false) {
  console.log('🔄 個別スロット画像更新:', slotId);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.warn(`⚠️ スロットが見つかりません: ${slotId}`);
    return;
  }
  
  // phraseまたはtextからテキストを取得
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
  
  // 空テキスト時は汎用システムが介入しない（責務分離）
  if (!currentText) {
    // 複数画像クリアのみ実行
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
    }
    // 静的制御（button.png制御）に委譲
    return;
  }
  
  // 複数画像対応：まず複数画像適用を試行
  applyMultipleImagesToSlot(slotId, currentText, forceRefresh);
}

// 🚀 全スロットの画像を一括更新
function updateAllSlotImages(forceRefresh = false) {
  console.log('🔄 全スロット画像一括更新開始', forceRefresh ? '（強制更新）' : '');
  
  for (const slotId of UPPER_SLOTS) {
    updateSlotImage(slotId, forceRefresh);
  }
  
  console.log('✅ 全スロット画像一括更新完了');
}

// 🔄 データ変更後の全スロット画像更新
function updateAllSlotImagesAfterDataChange() {
  console.log('🔄 データ変更後の全スロット画像更新');
  updateAllSlotImages(true); // 強制更新
}

// 🧹 複数画像コンテナのクリア（外部制御用）
function clearMultiImageContainer(slotId) {
  console.log('🧹 複数画像コンテナクリア:', slotId);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.warn(`⚠️ スロットが見つかりません: ${slotId}`);
    return;
  }
  
  const container = slot.querySelector('.multi-image-container');
  if (container) {
    container.remove();
    console.log('✅ 複数画像コンテナを削除:', slotId);
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
      singleImg.style.opacity = '1';
    }
  }
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
  }
  
  console.log('✅ 汎用画像システム初期化完了');
  
  // 初回画像適用
  setTimeout(() => {
    console.log('🎯 初回画像適用開始');
    updateAllSlotImages();
  }, 500);
}

// 🔍 個別ランダマイズボタンに関連するDOM変更を監視
function setupIndividualRandomizeObserver() {
  console.log('👀 個別ランダマイズ監視開始');
  
  const targetNode = document.getElementById('training-container');
  if (!targetNode) {
    console.warn('⚠️ training-containerが見つかりません');
    return;
  }
  
  // 重複処理防止用のデバウンス
  let updateTimeout = null;
  const processedSlots = new Set();
  
  const observer = new MutationObserver((mutations) => {
    let needsUpdate = false;
    
    mutations.forEach((mutation) => {
      // デバッグコンソール関連の変更は無視
      if (mutation.target.id === 'debug-console' ||
          mutation.target.closest('#debug-console')) {
        return;
      }
      
      if (mutation.type === 'childList' || mutation.type === 'characterData') {
        // スロット関連の変更を検出
        const changedSlotIds = new Set();
        
        // 変更されたノードからスロットIDを抽出
        [mutation.target, ...Array.from(mutation.addedNodes || [])].forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // 直接スロットの場合
            if (node.id && UPPER_SLOTS.includes(node.id)) {
              changedSlotIds.add(node.id);
            }
            // スロット内の要素の場合
            const parentSlot = node.closest('.slot-container');
            if (parentSlot && UPPER_SLOTS.includes(parentSlot.id)) {
              changedSlotIds.add(parentSlot.id);
            }
          }
        });
        
        changedSlotIds.forEach(slotId => {
          if (!processedSlots.has(slotId)) {
            processedSlots.add(slotId);
            needsUpdate = true;
            console.log(`🔄 変更検出: ${slotId}`);
          }
        });
      }
    });
    
    if (needsUpdate) {
      // デバウンス：連続した変更をまとめて処理
      clearTimeout(updateTimeout);
      updateTimeout = setTimeout(() => {
        console.log('🔄 DOM変更による画像更新実行');
        updateAllSlotImages();
        processedSlots.clear(); // 処理済みセットをクリア
      }, 100);
    }
  });
  
  observer.observe(targetNode, {
    childList: true,
    subtree: true,
    characterData: true
  });
  
  console.log('👀 個別ランダマイズ監視設定完了');
}

// 🧪 手動テスト用関数
function testUniversalImageSystem() {
  console.log('🧪 汎用画像システムテスト開始');
  
  // メタタグデータ確認
  console.log('📊 メタタグデータ:', imageMetaTags.length, '件');
  
  // 各スロットの状態確認
  UPPER_SLOTS.forEach(slotId => {
    const slot = document.getElementById(slotId);
    if (slot) {
      const phraseEl = slot.querySelector('.slot-phrase');
      const textEl = slot.querySelector('.slot-text');
      const imgEl = slot.querySelector('.slot-image');
      
      const phrase = phraseEl ? phraseEl.textContent.trim() : '';
      const text = textEl ? textEl.textContent.trim() : '';
      const currentText = phrase || text;
      
      console.log(`📝 ${slotId}: "${currentText}" ${imgEl ? '(画像要素あり)' : '(画像要素なし)'}`);
      
      if (currentText && imgEl) {
        updateSlotImage(slotId, true);
      }
    } else {
      console.warn(`⚠️ ${slotId}: スロット要素なし`);
    }
  });
  
  console.log('🧪 テスト完了');
}

// 🔧 グローバル公開関数
window.loadImageMetaTags = loadImageMetaTags;
window.updateAllSlotImages = updateAllSlotImages;
window.updateSlotImage = updateSlotImage;
window.updateAllSlotImagesAfterDataChange = updateAllSlotImagesAfterDataChange;
window.testUniversalImageSystem = testUniversalImageSystem;
window.initializeUniversalImageSystem = initializeUniversalImageSystem;

// 🖼️ 新機能：複数画像対応の公開関数
window.applyMultipleImagesToSlot = applyMultipleImagesToSlot;
window.findAllImagesByMetaTag = findAllImagesByMetaTag;
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

// 🚀 DOMContentLoaded で自動初期化
document.addEventListener('DOMContentLoaded', () => {
  console.log('📦 DOM読み込み完了、汎用画像システム初期化開始...');
  console.log('📦 現在時刻:', new Date().toLocaleTimeString());
  
  // 500ms後に初期化実行（他のスクリプトの読み込み完了を待つ）
  setTimeout(async () => {
    console.log('🚀 汎用画像システム初期化実行');
    
    try {
      await initializeUniversalImageSystem();
      console.log('✅ 汎用画像システム初期化成功');
      
      // DOM監視開始
      setupIndividualRandomizeObserver();
      
    } catch (error) {
      console.error('❌ 汎用画像システム初期化エラー:', error);
    }
  }, 500);
});

console.log('📋 universal_image_system.js 読み込み完了');
