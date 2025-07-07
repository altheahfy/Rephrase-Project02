// ブラウザキャッシュを強制クリアして再読み込み
console.log('🔄 ブラウザキャッシュを強制クリア中...');

// 1. 全ての画像要素のsrcを一度クリアしてから再設定
const allImages = document.querySelectorAll('img');
allImages.forEach((img, index) => {
  const originalSrc = img.src;
  if (originalSrc && !originalSrc.includes('?t=')) {
    const separator = originalSrc.includes('?') ? '&' : '?';
    const newSrc = originalSrc + separator + 't=' + Date.now();
    console.log(`🔄 画像 ${index + 1}: ${originalSrc} → ${newSrc}`);
    img.src = newSrc;
  }
});

// 2. 特に V スロットの画像を強制リロード
const vSlotImages = document.querySelectorAll('#slot-v img');
vSlotImages.forEach((img, index) => {
  const originalSrc = img.src;
  if (originalSrc) {
    // 既存のキャッシュバスターを削除
    const baseSrc = originalSrc.split('?')[0];
    const newSrc = baseSrc + '?t=' + Date.now() + Math.random();
    console.log(`🎯 Vスロット画像 ${index + 1}: ${originalSrc} → ${newSrc}`);
    img.src = newSrc;
  }
});

// 3. 少し待ってから完全に再読み込み
setTimeout(() => {
  console.log('🔄 完全なページリロードを実行します...');
  location.reload(true);
}, 2000);
