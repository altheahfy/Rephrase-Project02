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
      console.log('🧹 単一マッチのため複数画像コンテナを削除:', slotId);
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

// 🧹 複数画像コンテナをクリアして単一画像表示に戻す（外部制御用）
function clearMultiImageContainer(slotId) {
  console.log('🧹 複数画像コンテナクリア開始:', slotId);
  
  const slot = document.getElementById(slotId);
  if (!slot) {
    console.error('❌ スロットが見つかりません:', slotId);
    return false;
  }

  // 複数画像コンテナがあれば削除
  const existingContainer = slot.querySelector('.multi-image-container');
  if (existingContainer) {
    existingContainer.remove();
    console.log('🧹 複数画像コンテナを削除しました:', slotId);
  }
  
  // 単一画像を再表示
  const singleImg = slot.querySelector('.slot-image');
  if (singleImg) {
    singleImg.style.display = 'block';
    singleImg.style.visibility = 'visible';
    singleImg.style.opacity = '1';
    console.log('🧹 単一画像を再表示しました:', slotId);
  }
  
  // スロット全体の横幅をリセット
  slot.style.maxWidth = '';
  slot.style.width = '';
  
  console.log('🧹 複数画像コンテナクリア完了:', slotId);
  return true;
}

// 🛠️ デバッグメッセージ表示機能
function displayDebugMessage(message, type = 'info') {
  const debugLog = document.getElementById('universal-debug-log') || (() => {
    const log = document.createElement('div');
    log.id = 'universal-debug-log';
    log.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(0, 0, 0, 0.9);
      color: white;
      padding: 10px;
      border-radius: 4px;
      z-index: 10001;
      max-width: 350px;
      max-height: 400px;
      overflow-y: auto;
      font-family: monospace;
      font-size: 10px;
      line-height: 1.2;
    `;
    log.innerHTML = '<strong>🔍 汎用画像システム ライブログ</strong><br>';
    document.body.appendChild(log);
    return log;
  })();
  
  const timestamp = new Date().toLocaleTimeString();
  const colorClass = type === 'error' ? 'color: #ff6b6b' : 
                    type === 'warning' ? 'color: #ffa500' :
                    type === 'success' ? 'color: #51cf66' : 'color: white';
  
  debugLog.innerHTML += `<div style="${colorClass}">[${timestamp}] ${message}</div>`;
  debugLog.scrollTop = debugLog.scrollHeight;
  
  // 50行を超えたら古いものを削除
  const lines = debugLog.querySelectorAll('div');
  if (lines.length > 50) {
    for (let i = 0; i < lines.length - 50; i++) {
      lines[i].remove();
    }
  }
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
  
  // デバッグパネルは無効化
  // createDebugPanel();
  
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
    
    // スロットテキストの変更を監視（MutationObserver）
    observeSlotChanges(slotId);
  }
  
  // 5秒後にもう一度実行（遅延読み込み対応）
  setTimeout(() => {
    console.log('🔄 5秒後の再チェック実行');
    for (const slotId of UPPER_SLOTS) {
      monitorSlotText(slotId);
    }
    // updateDebugPanel(); // デバッグパネル更新は無効化
  }, 5000);
  
  // 定期的なデバッグパネル更新は無効化
  // setInterval(updateDebugPanel, 10000); // 10秒ごと
  
  console.log('✅ 汎用画像システム初期化完了');
}

// 🛠️ デバッグパネル作成
function createDebugPanel() {
  const debugPanel = document.createElement('div');
  debugPanel.id = 'universal-debug-panel';
  debugPanel.style.cssText = `
    position: fixed;
    bottom: 10px;
    left: 10px;
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 10px;
    border-radius: 4px;
    z-index: 10000;
    max-width: 400px;
    max-height: 300px;
    overflow-y: auto;
    font-family: monospace;
    font-size: 11px;
    line-height: 1.2;
  `;
  debugPanel.innerHTML = '<strong>🔍 汎用画像システム デバッグパネル</strong><br>初期化中...';
  
  document.body.appendChild(debugPanel);
  
  // パネルのオン/オフ切り替え
  debugPanel.addEventListener('click', () => {
    if (debugPanel.style.height === '20px') {
      debugPanel.style.height = 'auto';
      debugPanel.style.maxHeight = '300px';
    } else {
      debugPanel.style.height = '20px';
      debugPanel.style.maxHeight = '20px';
      debugPanel.style.overflow = 'hidden';
    }
  });
}

// 🛠️ デバッグパネル更新
function updateDebugPanel() {
  const debugPanel = document.getElementById('universal-debug-panel');
  if (!debugPanel) return;
  
  let debugInfo = '<strong>🔍 汎用画像システム (クリックで展開/折りたたみ)</strong><br>';
  debugInfo += `⏰ ${new Date().toLocaleTimeString()}<br>`;
  debugInfo += `📊 メタタグ: ${imageMetaTags.length}件<br><br>`;
  
  UPPER_SLOTS.forEach(slotId => {
    const slot = document.getElementById(slotId);
    if (!slot) {
      debugInfo += `❌ ${slotId}: 見つからない<br>`;
      return;
    }
    
    const phraseEl = slot.querySelector('.slot-phrase');
    const textEl = slot.querySelector('.slot-text');
    const imgEl = slot.querySelector('.slot-image');
    
    const phrase = phraseEl ? phraseEl.textContent.trim() : '';
    const text = textEl ? textEl.textContent.trim() : '';
    const currentText = phrase || text;
    const imageSrc = imgEl ? imgEl.src.split('/').pop().split('?')[0] : '不明';
    
    const status = currentText ? '✅' : '⚪';
    debugInfo += `${status} ${slotId}: "${currentText}" → ${imageSrc}<br>`;
  });
  
  debugPanel.innerHTML = debugInfo;
}

// 🔍 スロットの変更を監視
function observeSlotChanges(slotId) {
  const slot = document.getElementById(slotId);
  if (!slot) return;
  
  const observer = new MutationObserver((mutations) => {
    let textChanged = false;
    
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' || 
          (mutation.type === 'characterData' && mutation.target.nodeType === Node.TEXT_NODE)) {
        textChanged = true;
      }
    });
    
    if (textChanged) {
      console.log(`🔄 ${slotId} テキスト変更を検出、画像を更新中...`);
      setTimeout(() => monitorSlotText(slotId), 100); // 少し遅延させて確実に更新
      // updateDebugPanel(); // デバッグパネル更新は無効化
    }
  });
  
  // .slot-phrase と .slot-text の変更を監視
  const phraseEl = slot.querySelector('.slot-phrase');
  const textEl = slot.querySelector('.slot-text');
  
  if (phraseEl) {
    observer.observe(phraseEl, { 
      childList: true, 
      subtree: true, 
      characterData: true 
    });
  }
  
  if (textEl) {
    observer.observe(textEl, { 
      childList: true, 
      subtree: true, 
      characterData: true 
    });
  }
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
  
  // テキストが空の場合は複数画像のクリアのみ実行して従来の単一画像処理に移行
  if (!currentText) {
    console.warn('⚠️ スロットテキストが空です - 複数画像クリア処理のみ実行:', slotId);
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
      console.log('🧹 空テキストのため複数画像コンテナを削除:', slotId);
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
    
    // 従来の処理（insert_test_data_clean.jsのbutton.png制御等）に任せるため、ここで処理終了
    console.log('✅ 空テキスト時の複数画像クリア完了、従来処理に移行:', slotId);
    return;
  }
  
  // 複数画像対応の処理を実行
  applyMultipleImagesToSlot(slotId, currentText, forceRefresh);
  
  // 1秒後に画像の状態を再確認
  setTimeout(() => {
    const imgElement = slot.querySelector('.slot-image');
    const multiImageContainer = slot.querySelector('.multi-image-container');
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

// 🔧 仕様書準拠テスト関数
function testSubslotImageSystemCompliance() {
  console.log('🧪 ==========================================');
  console.log('🧪 サブスロット画像システム仕様書準拠テスト開始');
  console.log('🧪 ==========================================');
  
  // テスト用のサブスロットIDを取得
  const allSubslots = document.querySelectorAll('[id*="-sub-"]');
  console.log('📍 発見されたサブスロット数:', allSubslots.length);
  
  if (allSubslots.length === 0) {
    console.log('⚠️ サブスロットが見つかりません。C1スロットを展開してからテストしてください。');
    return;
  }
  
  // 最初の3つのサブスロットをテスト
  const testCases = [
    { text: 'manager', expectedImage: 'manager.png' },
    { text: 'analyze', expectedImage: 'analyze.png' },
    { text: 'she', expectedImage: 'she.png' }
  ];
  
  testCases.forEach((testCase, index) => {
    if (index < allSubslots.length) {
      const subslot = allSubslots[index];
      const subslotId = subslot.id;
      
      console.log(`\n🔍 テストケース ${index + 1}: ${subslotId} → "${testCase.text}"`);
      
      // 画像を適用
      applyImageToSubslot(subslotId, testCase.text);
      
      // 2秒後に結果を確認
      setTimeout(() => {
        const imgElement = subslot.querySelector('.slot-image');
        if (imgElement) {
          console.log(`✅ 画像要素存在: ${subslotId}`);
          console.log(`🔍 data-meta-tag: ${imgElement.getAttribute('data-meta-tag')}`);
          console.log(`🔍 data-meta-tag-applied: ${imgElement.getAttribute('data-meta-tag-applied')}`);
          console.log(`🔍 data-applied-text: ${imgElement.getAttribute('data-applied-text')}`);
          console.log(`🔍 current src: ${imgElement.src}`);
          console.log(`🔍 display: ${imgElement.style.display}`);
          console.log(`🔍 visibility: ${imgElement.style.visibility}`);
          console.log(`🔍 opacity: ${imgElement.style.opacity}`);
          
          // 仕様書準拠性チェック
          const hasMetaTag = imgElement.getAttribute('data-meta-tag') === 'true';
          const hasAppliedTag = imgElement.getAttribute('data-meta-tag-applied') !== null;
          const hasAppliedText = imgElement.getAttribute('data-applied-text') === testCase.text;
          const isVisible = imgElement.style.display !== 'none' && imgElement.style.visibility !== 'hidden';
          
          console.log(`📊 仕様準拠性: メタタグ=${hasMetaTag}, 適用タグ=${hasAppliedTag}, 適用テキスト=${hasAppliedText}, 可視性=${isVisible}`);
          
          if (hasMetaTag && hasAppliedTag && hasAppliedText && isVisible) {
            console.log(`✅ ${subslotId}: 仕様書完全準拠！`);
          } else {
            console.log(`⚠️ ${subslotId}: 仕様書との差異があります`);
          }
        } else {
          console.error(`❌ ${subslotId}: 画像要素が見つかりません`);
        }
      }, 2000 + (index * 500)); // 段階的にチェック
    }
  });
  
  console.log('\n🧪 ==========================================');
  console.log('🧪 テスト完了まで数秒お待ちください...');
  console.log('🧪 ==========================================');
}

// グローバルに公開
window.testSubslotImageSystemCompliance = testSubslotImageSystemCompliance;

// グローバル関数として公開
window.initializeUniversalImageSystem = initializeUniversalImageSystem;
window.updateAllSlotImages = updateAllSlotImages;
window.updateSlotImage = updateSlotImage;
window.updateAllSlotImagesAfterDataChange = updateAllSlotImagesAfterDataChange;
window.testUniversalImageSystem = testUniversalImageSystem;

// 🖼️ 新機能：複数画像対応の公開関数
window.applyMultipleImagesToSlot = applyMultipleImagesToSlot;
window.findAllImagesByMetaTag = findAllImagesByMetaTag;
window.clearMultiImageContainer = clearMultiImageContainer;

// 🔄 旧V専用システムとの互換性維持
window.updateVSlotImage = function(forceRefresh = false) {
  updateSlotImage('slot-v', forceRefresh);
};
window.updateVSlotImageAfterDataChange = function() {
  updateSlotImage('slot-v', true);
};

// DOMContentLoaded で自動初期化
document.addEventListener('DOMContentLoaded', () => {
  console.log('📦 DOM読み込み完了、汎用画像システム初期化開始...');
  console.log('📦 現在時刻:', new Date().toLocaleTimeString());
  
  initializeUniversalImageSystem();
});

// 🎯 サブスロット専用画像表示システム（既存システムと完全独立）
function updateSubslotImages(parentSlotId) {
  console.log(`🖼️ サブスロット画像更新開始: ${parentSlotId}`);
  console.log(`🔍 デバッグ - メタタグ状態: ${imageMetaTags ? imageMetaTags.length : 'null'}`);
  console.log(`🔍 デバッグ - fullSlotPool状態: ${window.fullSlotPool ? window.fullSlotPool.length : 'null'}`);
  console.log(`🔍 デバッグ - JSONデータ状態: ${window.loadedJsonData ? 'OK' : 'null'}`);
  
  // 🎯 テスト段階：C1スロットのみに限定
  if (parentSlotId !== 'c1') {
    console.log(`⏭️ テスト段階のため ${parentSlotId} はスキップします（C1スロットのみ対象）`);
    return;
  }
  
  // 🔍 サブスロットコンテナの表示状態を確認
  const subslotContainer = document.getElementById(`slot-${parentSlotId}-sub`);
  console.log(`🔍 デバッグ - サブスロットコンテナ:`, subslotContainer);
  if (!subslotContainer) {
    console.warn(`⚠️ サブスロットコンテナが見つかりません: slot-${parentSlotId}-sub`);
    return;
  }
  
  const containerStyle = window.getComputedStyle(subslotContainer);
  console.log(`🔍 デバッグ - コンテナ表示状態: ${containerStyle.display}`);
  if (containerStyle.display === 'none') {
    console.warn(`⚠️ サブスロットコンテナが非表示状態です。画像更新を中断。`);
    return;
  }
  
  console.log(`✅ サブスロットコンテナが表示状態です。画像処理を続行します。`);
  
  // window.fullSlotPoolまたはloadedJsonDataが必要
  if (!window.fullSlotPool && !window.loadedJsonData) {
    console.warn('⚠️ fullSlotPoolおよびJSONデータが両方とも読み込まれていません。サブスロット画像更新を中断。');
    return;
  }
  
  if (!imageMetaTags || imageMetaTags.length === 0) {
    console.warn('⚠️ メタタグデータが読み込まれていません。サブスロット画像更新を中断。');
    return;
  }
  
  // 🆕 実際に存在するサブスロット要素を動的に検出
  console.log('🔍 実際のサブスロット要素を動的検出中...');
  const actualSubslots = [];
  
  // サブスロットコンテナ内のすべての子要素をチェック
  Array.from(subslotContainer.children).forEach(child => {
    if (child.id && child.id.includes('sub')) {
      actualSubslots.push(child.id);
      console.log(`  ✅ 発見: ${child.id}`);
    }
  });
  
  if (actualSubslots.length === 0) {
    console.warn('⚠️ サブスロット要素が一つも見つかりませんでした');
    return;
  }
  
  console.log(`🎯 実際に存在するサブスロット: ${actualSubslots.length}個`, actualSubslots);
  
  // 🎯 デバッグ - 各サブスロット存在確認
  actualSubslots.forEach(id => {
    const element = document.getElementById(id);
    console.log(`  ${id}: ${element ? 'あり' : 'なし'}`);
    if (element) {
      const textEl = element.querySelector('.slot-text');
      const imgEl = element.querySelector('.slot-image');
      console.log(`    テキスト要素: ${textEl ? 'あり' : 'なし'} "${textEl?.textContent?.trim() || ''}"`);
      console.log(`    画像要素: ${imgEl ? 'あり' : 'なし'}`);
    }
  });
  
  for (const subslotId of actualSubslots) {
    const subslotElement = document.getElementById(subslotId);
    if (!subslotElement) {
      console.warn(`⚠️ サブスロット要素が見つかりません: ${subslotId}`);
      continue;
    }
    
    // 🆕 window.fullSlotPoolから英語例文（SubslotElement）を取得
    const englishText = getEnglishTextFromSlotPool(subslotId, parentSlotId);
    
    if (!englishText) {
      console.log(`📝 英語例文が見つからない: ${subslotId}`);
      continue;
    }
    
    console.log(`🔍 サブスロット処理中: ${subslotId}, 英語例文: "${englishText}"`);
    
    // 🎯 サブスロット専用の画像適用（英語例文を使用）
    applyImageToSubslot(subslotId, englishText);
    console.log(`✅ サブスロット画像処理完了: ${subslotId} → "${englishText}"`);
  }
  
  console.log(`✅ サブスロット画像更新完了: ${parentSlotId}`);
}

// 🎯 サブスロット専用画像適用関数（既存システムと完全独立）
function applyImageToSubslot(subslotId, phraseText) {
  console.log('🖼️ サブスロット画像適用開始:', subslotId, '→', phraseText);
  
  const subslot = document.getElementById(subslotId);
  if (!subslot) {
    console.error('❌ サブスロット要素が見つかりません:', subslotId);
    return;
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
  
  console.log('🔍 サブスロット画像要素発見:', imgElement);
  console.log('🔍 サブスロット現在の画像src:', imgElement.src);
  
  // テキストが空の場合はプレースホルダーを設定
  if (!phraseText || phraseText.trim() === '') {
    imgElement.src = 'slot_images/common/placeholder.png';
    imgElement.alt = `image for ${subslotId}`;
    console.log('📝 サブスロットテキストが空のため、プレースホルダーを設定:', subslotId);
    return;
  }
  
  // 画像を検索（日本語対応を含む）
  let imageData = findImageByMetaTag(phraseText);
  console.log('🔍 サブスロット検索結果（通常）:', imageData);
  
  // 通常検索で見つからない場合、日本語マッピングを試行
  if (!imageData) {
    console.log('🇯🇵 日本語マッピング検索を試行:', phraseText);
    imageData = findImageForJapaneseText(phraseText);
    console.log('🔍 サブスロット検索結果（日本語）:', imageData);
  }
  
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
  
  // 🆕 image_auto_hide.js対策：メタタグ属性を設定（仕様書準拠）
  imgElement.setAttribute('data-meta-tag', 'true');
  imgElement.setAttribute('data-meta-tag-applied', imageData.meta_tags ? imageData.meta_tags[0] : phraseText);
  imgElement.setAttribute('data-applied-text', phraseText);
  imgElement.classList.remove('auto-hidden-image');
  
  // 強制的に表示状態にする
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  
  // 🆕 競合対策：定期的な強制表示チェック
  const forceDisplayInterval = setInterval(() => {
    if (imgElement.style.display === 'none' || imgElement.style.visibility === 'hidden') {
      console.log('🛡️ 画像が隠されました。強制再表示:', subslotId);
      imgElement.style.display = 'block';
      imgElement.style.visibility = 'visible';
      imgElement.style.opacity = '1';
    }
  }, 200);
  
  // 3秒後にインターバルを停止
  setTimeout(() => {
    clearInterval(forceDisplayInterval);
    console.log('🛡️ 強制表示監視を終了:', subslotId);
  }, 3000);
  
  // 画像読み込み完了後に再度表示を確認
  imgElement.onload = function() {
    console.log('🎨 サブスロット画像読み込み完了:', newImagePath);
    
    // 🆕 image_auto_hide.js対策を再適用（仕様書準拠）
    this.setAttribute('data-meta-tag', 'true');
    this.setAttribute('data-meta-tag-applied', imageData.meta_tags ? imageData.meta_tags[0] : phraseText);
    this.setAttribute('data-applied-text', phraseText);
    this.classList.remove('auto-hidden-image');
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

// 🧪 デバッグ用：サブスロットの強制画像更新（コンソールから実行）
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

// グローバル公開
window.forceUpdateSubslotImages = forceUpdateSubslotImages;
window.updateSubslotImages = updateSubslotImages;
window.getEnglishTextFromSlotPool = getEnglishTextFromSlotPool;
window.monitorSubslotImageState = monitorSubslotImageState;
window.debugImageDisappearance = debugImageDisappearance;
