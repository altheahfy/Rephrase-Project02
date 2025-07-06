/**
 * メタタグによる画像自動表示機能
 * 既存システムに影響を与えない独立したモジュール
 */

// グローバル変数：メタタグデータ
window.imageMetaTagsData = null;
window.imageMetaTagsLoaded = false;

/**
 * ページ読み込み時にメタタグデータを自動読み込み
 */
async function loadImageMetaTagsOnStartup() {
  try {
    console.log("🖼️ [META] メタタグデータの読み込みを開始...");
    
    // キャッシュ無効化のためのクエリパラメータ
    const timestamp = new Date().getTime();
    const response = await fetch(`image_meta_tags.json?_=${timestamp}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    window.imageMetaTagsData = data;
    window.imageMetaTagsLoaded = true;

    console.log(`✅ [META] メタタグデータ読み込み完了: ${data.length}件`);
    return true;

  } catch (error) {
    console.warn("⚠️ [META] メタタグデータの読み込みに失敗:", error.message);
    window.imageMetaTagsData = [];
    window.imageMetaTagsLoaded = false;
    return false;
  }
}

/**
 * テキストから単語を抽出し、語幹を取得する
 */
function extractWordsWithStemming(text) {
  if (!text || typeof text !== 'string') return [];

  // 小文字化、記号除去、単語分割
  const words = text.toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 1); // 2文字以上の単語（短い重要語に対応）

  // 語幹抽出（簡易版）
  const stemmed = words.map(word => {
    // 複数形・過去形・現在分詞の基本的な語幹抽出
    if (word.endsWith('ies') && word.length > 4) return word.slice(0, -3) + 'y';
    if (word.endsWith('ed') && word.length > 4) return word.slice(0, -2);
    if (word.endsWith('ing') && word.length > 5) return word.slice(0, -3);
    if (word.endsWith('es') && word.length > 3 && !word.endsWith('ses') && !word.endsWith('oes')) return word.slice(0, -2);
    if (word.endsWith('s') && word.length > 3 && !word.endsWith('ss') && !word.endsWith('us') && !word.endsWith('is')) return word.slice(0, -1);
    return word;
  });

  // 元の単語と語幹の両方を返す（重複削除）
  return [...new Set([...words, ...stemmed])];
}

/**
 * テキストにマッチする画像パスを検索（優先度対応）
 */
function findImageByMetaTag(text) {
  if (!window.imageMetaTagsLoaded || !window.imageMetaTagsData) {
    return null;
  }

  const textWords = extractWordsWithStemming(text);
  console.log(`🔍 [META] 単語抽出 "${text}" → [${textWords.join(', ')}]`);

  const matches = [];

  for (const imageData of window.imageMetaTagsData) {
    for (const tag of imageData.meta_tags) {
      if (textWords.includes(tag.toLowerCase())) {
        matches.push({
          imageData,
          matchedTag: tag,
          priority: imageData.priority || 1
        });
      }
    }
  }

  if (matches.length === 0) return null;

  // 優先度でソート（高い順）
  matches.sort((a, b) => b.priority - a.priority);
  
  const bestMatch = matches[0];
  const imagePath = `slot_images/${bestMatch.imageData.folder}/${bestMatch.imageData.image_file}`;
  
  console.log(`✅ [META] マッチ: "${text}" → "${bestMatch.matchedTag}" → ${imagePath} (優先度: ${bestMatch.priority})`);
  return imagePath;
}

/**
 * スロット画像をクリア
 */
function clearSlotImage(slotElement) {
  if (!slotElement) return;
  
  const imageElement = slotElement.querySelector('.slot-image');
  if (!imageElement) return;
  
  // メタタグ画像またはプレースホルダーのみクリア
  if (imageElement.hasAttribute('data-meta-tag') || imageElement.src.includes('placeholder.png')) {
    imageElement.src = 'slot_images/common/placeholder.png';
    imageElement.removeAttribute('data-meta-tag');
    imageElement.removeAttribute('data-meta-tag-applied');
    imageElement.removeAttribute('data-applied-text');
    // auto-hidden-image クラスも削除
    imageElement.classList.remove('auto-hidden-image');
    console.log(`🗑️ [META] 画像クリア: ${slotElement.id}`);
  }
}

/**
 * 単一スロットに画像を適用（居座り防止機能付き）
 */
function applyImageToSlot(slotElement, phraseText, forceRefresh = false) {
  if (!slotElement || !phraseText) return false;

  const imageElement = slotElement.querySelector('.slot-image');
  if (!imageElement) return false;

  // 居座り防止：同じテキストで同じ画像が既に適用されている場合はスキップ
  const currentAppliedText = imageElement.getAttribute('data-applied-text');
  if (!forceRefresh && currentAppliedText === phraseText && imageElement.hasAttribute('data-meta-tag')) {
    console.log(`⏭️ [META] スキップ（同一画像適用済み）: ${slotElement.id} → "${phraseText}"`);
    return true;
  }

  const imagePath = findImageByMetaTag(phraseText);
  if (!imagePath) {
    // マッチしない場合はプレースホルダーを設定
    if (!imageElement.src.includes('placeholder.png')) {
      clearSlotImage(slotElement);
    }
    return false;
  }

  // 画像を適用
  imageElement.src = imagePath;
  imageElement.setAttribute('data-meta-tag', 'true');
  imageElement.setAttribute('data-meta-tag-applied', phraseText);
  imageElement.setAttribute('data-applied-text', phraseText);
  
  // auto-hidden-image クラスを削除（image_auto_hide.jsとの競合を回避）
  imageElement.classList.remove('auto-hidden-image');
  
  // 表示の正規化
  imageElement.style.visibility = 'visible';
  imageElement.style.opacity = '1';
  imageElement.style.display = 'block';
  
  console.log(`📷 [META] 画像適用: ${slotElement.id} → "${phraseText}" → ${imagePath}`);
  return true;
}

/**
 * テキスト変更時の画像更新処理
 */
function handleSlotTextChange(slotElement) {
  if (!slotElement) return;
  
  const phraseElement = slotElement.querySelector('.slot-phrase');
  if (!phraseElement) return;
  
  const phraseText = phraseElement.textContent.trim();
  
  // 居座り防止：まず画像をクリアしてから新しい画像を適用
  clearSlotImage(slotElement);
  
  if (phraseText) {
    // 短い遅延を入れて適用（DOM更新の完了を待つ）
    setTimeout(() => {
      applyImageToSlot(slotElement, phraseText, true);
    }, 50);
  }
}

/**
 * 全スロットに対してメタタグ画像を適用
 */
function applyMetaTagImagesToAllSlots(forceRefresh = false) {
  if (!window.imageMetaTagsLoaded) {
    console.warn("⚠️ [META] メタタグデータが読み込まれていません");
    return 0;
  }

  console.log("🖼️ [META] === 全スロット画像適用開始 ===");
  let appliedCount = 0;

  // 上位スロット + サブスロットを一括処理
  const allSlots = document.querySelectorAll('.slot-container, .subslot-container');
  
  allSlots.forEach(slotElement => {
    const phraseElement = slotElement.querySelector('.slot-phrase');
    if (!phraseElement) return;

    const phraseText = phraseElement.textContent.trim();
    if (!phraseText) return;

    if (applyImageToSlot(slotElement, phraseText, forceRefresh)) {
      appliedCount++;
    }
  });

  console.log(`✅ [META] === 画像適用完了: ${appliedCount}件 ===`);
  return appliedCount;
}

/**
 * DOM変更監視・自動画像更新
 */
function setupIndividualRandomizeObserver() {
  const targetNode = document.getElementById('training-container');
  if (!targetNode) {
    console.warn("⚠️ [META] training-container が見つかりません");
    return;
  }

  const observer = new MutationObserver((mutations) => {
    let shouldUpdate = false;
    
    mutations.forEach((mutation) => {
      // デバッグコンソールの変更は無視
      if (mutation.target.id === 'debug-console' || 
          mutation.target.closest('#debug-console')) {
        return;
      }
      
      if (mutation.type === 'characterData' || mutation.type === 'childList') {
        shouldUpdate = true;
      }
    });
    
    if (shouldUpdate) {
      console.log("🔄 [META] DOM変更を検出 - 画像を更新");
      // 短い遅延を入れてから更新（DOM更新の完了を待つ）
      setTimeout(() => {
        applyMetaTagImagesToAllSlots(true);
      }, 100);
    }
  });

  observer.observe(targetNode, {
    childList: true,
    subtree: true,
    characterData: true
  });

  console.log("👁️ [META] DOM変更監視を開始");
  return observer;
}

/**
 * メタタグ機能の初期化（ページ読み込み時に自動実行）
 */
async function initializeMetaTagSystem() {
  console.log("🚀 [META] メタタグシステム初期化開始");

  // メタタグデータを読み込み
  const loaded = await loadImageMetaTagsOnStartup();
  
  if (loaded) {
    // 少し遅延してから初回画像適用
    setTimeout(() => {
      applyMetaTagImagesToAllSlots();
      
      // DOM変更監視を開始
      setupIndividualRandomizeObserver();
    }, 500);
  }
}

/**
 * デバッグ用：厳密マッチングの動作確認
 */
function debugStrictMatching() {
  console.log("🔍 [DEBUG] === 厳密マッチングデバッグ ===");
  
  if (!window.imageMetaTagsLoaded) {
    console.log("❌ メタタグデータが読み込まれていません");
    return;
  }
  
  console.log(`📊 利用可能メタタグ: ${window.imageMetaTagsData.length}件`);
  console.log("🎯 マッチングルール: 厳密一致のみ（部分マッチなし）");
  
  const allSlots = document.querySelectorAll('.slot-container, .subslot-container');
  let totalSlots = 0;
  let matchedSlots = 0;
  
  allSlots.forEach(slot => {
    const phraseElement = slot.querySelector('.slot-phrase');
    if (!phraseElement) return;
    
    const text = phraseElement.textContent.trim();
    if (!text) return;
    
    totalSlots++;
    const imagePath = findImageByMetaTag(text);
    
    if (imagePath) {
      matchedSlots++;
      console.log(`✅ ${slot.id}: "${text}" → ${imagePath}`);
    } else {
      console.log(`❌ ${slot.id}: "${text}" → マッチなし`);
    }
  });
  
  console.log(`📈 マッチング統計: ${matchedSlots}/${totalSlots} (${((matchedSlots/totalSlots)*100).toFixed(1)}%)`);
}

// グローバル関数として公開
window.loadImageMetaTagsOnStartup = loadImageMetaTagsOnStartup;
window.findImageByMetaTag = findImageByMetaTag;
window.applyMetaTagImagesToAllSlots = applyMetaTagImagesToAllSlots;
window.initializeMetaTagSystem = initializeMetaTagSystem;
window.debugStrictMatching = debugStrictMatching;
window.handleSlotTextChange = handleSlotTextChange;
window.clearSlotImage = clearSlotImage;

// DOMContentLoaded後に自動初期化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeMetaTagSystem);
} else {
  initializeMetaTagSystem();
}
