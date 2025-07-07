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
  
  // 各単語に対してマッチする画像を探す
  for (const word of searchWords) {
    let bestMatchForWord = null;
    let bestPriorityForWord = 0;
    
    for (const imageData of imageMetaTags) {
      // 既に使用済みの画像はスキップ
      if (usedImages.has(imageData.image_file)) {
        continue;
      }
      
      for (const metaTag of imageData.meta_tags) {
        if (metaTag.toLowerCase() === word.toLowerCase()) {
          const priority = imageData.priority || 1;
          
          if (priority > bestPriorityForWord) {
            bestMatchForWord = imageData;
            bestPriorityForWord = priority;
          }
          console.log('🎯 複数マッチング成功:', metaTag, '→', imageData.image_file, `(優先度: ${priority})`);
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
  
  // 新しい画像パスを構築
  const newImagePath = `slot_images/${imageData.folder}/${imageData.image_file}`;
  console.log('🎨 新しい画像パス:', newImagePath);
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

  // テキストが空の場合は通常の単一画像処理に戻す
  if (!phraseText || phraseText.trim() === '') {
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
    }
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
    }
    
    applyImageToSlot(slotId, phraseText, forceRefresh);
    return;
  }

  // 複数の画像を検索
  const imageDataArray = findAllImagesByMetaTag(phraseText);
  console.log('🔍 複数検索結果:', imageDataArray);

  // マッチする画像がない場合は通常の処理に戻す
  if (imageDataArray.length === 0) {
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
    }
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
    }
    
    applyImageToSlot(slotId, phraseText, forceRefresh);
    return;
  }

  // 1個しかマッチしない場合は通常の処理に戻す
  if (imageDataArray.length === 1) {
    // 複数画像コンテナがあれば削除
    const existingContainer = slot.querySelector('.multi-image-container');
    if (existingContainer) {
      existingContainer.remove();
    }
    
    // 単一画像を再表示
    const singleImg = slot.querySelector('.slot-image');
    if (singleImg) {
      singleImg.style.display = 'block';
      singleImg.style.visibility = 'visible';
    }
    
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
      gap: 8px;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      width: 100%;
      min-height: 120px;
      max-height: 150px;
      padding: 8px;
      box-sizing: border-box;
      border-radius: 6px;
      background: rgba(40, 167, 69, 0.08);
      border: 2px dashed rgba(40, 167, 69, 0.4);
      visibility: visible !important;
      opacity: 1 !important;
    `;
    slot.appendChild(imageContainer);
  }

  // 既存の画像をクリア
  imageContainer.innerHTML = '';

  // 🎯 画像数に応じてコンテナのクラスを設定
  imageContainer.className = 'multi-image-container';
  if (imageDataArray.length === 2) {
    imageContainer.classList.add('images-2');
  } else if (imageDataArray.length === 3) {
    imageContainer.classList.add('images-3');
  } else if (imageDataArray.length === 4) {
    imageContainer.classList.add('images-4');
  } else if (imageDataArray.length >= 5) {
    imageContainer.classList.add('images-5-plus');
  }

  console.log(`🎨 画像コンテナクラス設定: ${imageContainer.className} (${imageDataArray.length}枚)`);

  // 各画像を追加
  imageDataArray.forEach((imageData, index) => {
    const imgElement = document.createElement('img');
    const imagePath = `slot_images/${imageData.folder}/${imageData.image_file}`;
    const cacheBuster = Date.now() + index; // 各画像に個別のキャッシュバスター
    
    imgElement.src = `${imagePath}?t=${cacheBuster}`;
    imgElement.alt = `image ${index + 1} for ${slotId}: ${imageData.description || phraseText}`;
    imgElement.className = 'slot-multi-image';
    
    // 🎯 画像数に応じて動的にサイズを調整
    const baseSize = Math.max(140 - (imageDataArray.length - 2) * 20, 60);
    const minSize = Math.max(baseSize * 0.7, 50);
    
    imgElement.style.cssText = `
      flex: 1 1 auto;
      max-width: ${baseSize}px !important;
      max-height: ${baseSize}px !important;
      min-width: ${minSize}px !important;
      min-height: ${minSize}px !important;
      width: auto;
      height: auto;
      border-radius: 6px;
      border: 2px solid rgba(40, 167, 69, 0.6);
      object-fit: cover;
      display: block;
      visibility: visible;
      opacity: 1;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      aspect-ratio: 1 / 1;
    `;

    console.log(`🎨 画像${index + 1}サイズ: max:${baseSize}px, min:${minSize}px`);

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

  console.log(`🎨 複数画像表示完了: ${slotId} → ${imageDataArray.length}枚`);
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
  
  if (!currentText) {
    console.warn('⚠️ スロットテキストが空です:', slotId);
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

// 🎯 グローバル関数として公開
window.initializeUniversalImageSystem = initializeUniversalImageSystem;
window.updateAllSlotImages = updateAllSlotImages;
window.updateSlotImage = updateSlotImage;
window.updateAllSlotImagesAfterDataChange = updateAllSlotImagesAfterDataChange;
window.testUniversalImageSystem = testUniversalImageSystem;

// 🖼️ 新機能：複数画像対応の公開関数
window.applyMultipleImagesToSlot = applyMultipleImagesToSlot;
window.findAllImagesByMetaTag = findAllImagesByMetaTag;

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
  
  // 少し遅延させて他のスクリプトの完了を待つ
  setTimeout(() => {
    console.log('📦 遅延初期化実行中...');
    initializeUniversalImageSystem();
  }, 500);
});

console.log('📦 汎用画像システムが読み込まれました');
console.log('📦 対象スロット:', UPPER_SLOTS);
console.log('📦 テスト用関数: window.testUniversalImageSystem()');
console.log('📦 スクリプト読み込み時刻:', new Date().toLocaleTimeString());
