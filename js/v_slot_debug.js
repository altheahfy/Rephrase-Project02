// 🔧 Vスロット画像表示デバッグツール
// 問題を特定するための詳細な診断機能

function debugVSlotImage() {
  console.log('🔧 === Vスロット画像デバッグ開始 ===');
  
  // 1. Vスロットの存在確認
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error('❌ Vスロット（#slot-v）が見つかりません');
    return;
  }
  console.log('✅ Vスロット発見:', vSlot);
  
  // 2. 画像要素の詳細確認
  const imgElement = vSlot.querySelector('.slot-image');
  if (!imgElement) {
    console.error('❌ 画像要素が見つかりません');
    return;
  }
  
  console.log('📷 画像要素詳細:');
  console.log('  - src:', imgElement.src);
  console.log('  - alt:', imgElement.alt);
  console.log('  - complete:', imgElement.complete);
  console.log('  - naturalWidth:', imgElement.naturalWidth);
  console.log('  - naturalHeight:', imgElement.naturalHeight);
  console.log('  - data-meta-tag:', imgElement.getAttribute('data-meta-tag'));
  
  // 3. CSS スタイル確認
  const computedStyle = window.getComputedStyle(imgElement);
  console.log('🎨 CSS スタイル:');
  console.log('  - display:', computedStyle.display);
  console.log('  - visibility:', computedStyle.visibility);
  console.log('  - opacity:', computedStyle.opacity);
  console.log('  - width:', computedStyle.width);
  console.log('  - height:', computedStyle.height);
  
  // 4. クラス確認
  console.log('🏷️ クラス一覧:', Array.from(imgElement.classList));
  
  // 5. 親要素のスタイル確認
  const parentStyle = window.getComputedStyle(vSlot);
  console.log('📦 親要素スタイル:');
  console.log('  - display:', parentStyle.display);
  console.log('  - visibility:', parentStyle.visibility);
  console.log('  - opacity:', parentStyle.opacity);
  
  // 6. 画像ファイルの存在確認（fetch）
  fetch(imgElement.src)
    .then(response => {
      if (response.ok) {
        console.log('✅ 画像ファイルは存在します:', imgElement.src);
      } else {
        console.error('❌ 画像ファイルが見つかりません:', response.status, imgElement.src);
      }
    })
    .catch(error => {
      console.error('❌ 画像ファイルの確認に失敗:', error);
    });
  
  // 7. 強制的な表示設定を試行
  console.log('🔧 強制表示設定を試行...');
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  imgElement.style.width = 'auto';
  imgElement.style.height = 'auto';
  imgElement.style.maxWidth = '100px';
  imgElement.style.maxHeight = '100px';
  imgElement.classList.remove('auto-hidden-image');
  
  // 8. 結果の再確認
  setTimeout(() => {
    const newComputedStyle = window.getComputedStyle(imgElement);
    console.log('🔧 強制設定後のスタイル:');
    console.log('  - display:', newComputedStyle.display);
    console.log('  - visibility:', newComputedStyle.visibility);
    console.log('  - opacity:', newComputedStyle.opacity);
    console.log('  - width:', newComputedStyle.width);
    console.log('  - height:', newComputedStyle.height);
    
    console.log('🔧 === Vスロット画像デバッグ完了 ===');
  }, 1000);
}

// 🎯 画像を直接設定する関数
function forceSetVSlotImage(imageName = 'become.png') {
  const vSlot = document.getElementById('slot-v');
  if (!vSlot) {
    console.error('❌ Vスロットが見つかりません');
    return;
  }
  
  const imgElement = vSlot.querySelector('.slot-image');
  if (!imgElement) {
    console.error('❌ 画像要素が見つかりません');
    return;
  }
  
  console.log('🎯 画像を直接設定:', imageName);
  
  // 画像を直接設定
  imgElement.src = `slot_images/common/${imageName}`;
  imgElement.alt = `Direct set: ${imageName}`;
  imgElement.setAttribute('data-meta-tag', 'true');
  
  // 強制表示設定
  imgElement.style.display = 'block !important';
  imgElement.style.visibility = 'visible !important';
  imgElement.style.opacity = '1 !important';
  imgElement.classList.remove('auto-hidden-image');
  
  // 追加でCSSを直接挿入
  const styleElement = document.createElement('style');
  styleElement.textContent = `
    #slot-v .slot-image {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      width: auto !important;
      height: auto !important;
      max-width: 100px !important;
      max-height: 100px !important;
    }
  `;
  document.head.appendChild(styleElement);
  
  console.log('✅ 画像設定完了');
  
  // 1秒後に結果確認
  setTimeout(() => {
    debugVSlotImage();
  }, 1000);
}

// グローバル関数として公開
window.debugVSlotImage = debugVSlotImage;
window.forceSetVSlotImage = forceSetVSlotImage;

console.log('🔧 Vスロット画像デバッグツールが読み込まれました');
console.log('🔧 使用方法:');
console.log('  - debugVSlotImage() : 詳細な診断を実行');
console.log('  - forceSetVSlotImage() : 画像を強制設定');
