/**
 * 疑問詞エリア表示制御
 * display-top-question-wordの空判定と非表示制御
 */

/**
 * 疑問詞エリアの内容をチェックして空の場合は非表示にする
 */
function controlQuestionWordDisplay() {
  const questionWordElement = document.getElementById('display-top-question-word');
  
  if (!questionWordElement) {
    console.warn("⚠️ display-top-question-word要素が見つかりません");
    return;
  }
  
  // 内容を取得（テキストコンテンツのみ）
  const content = questionWordElement.textContent?.trim() || '';
  const innerHTML = questionWordElement.innerHTML?.trim() || '';
  
  console.log("🔍 疑問詞エリア内容チェック:", {
    textContent: content,
    innerHTML: innerHTML,
    isEmpty: content === '' && innerHTML === ''
  });
  
  // 空判定：テキストコンテンツもHTMLも空の場合
  if (content === '' && innerHTML === '') {
    // 空の場合：非表示
    questionWordElement.classList.add('empty-content');
    console.log("✅ 疑問詞エリアを非表示にしました（空のため）");
  } else {
    // 内容がある場合：表示
    questionWordElement.classList.remove('empty-content');
    console.log("✅ 疑問詞エリアを表示しました（内容あり）");
  }
}

/**
 * 疑問詞エリアを強制的に非表示にする
 */
function hideQuestionWordArea() {
  const questionWordElement = document.getElementById('display-top-question-word');
  if (questionWordElement) {
    questionWordElement.classList.add('empty-content');
    console.log("🔒 疑問詞エリアを強制非表示にしました");
  }
}

/**
 * 疑問詞エリアを強制的に表示する
 */
function showQuestionWordArea() {
  const questionWordElement = document.getElementById('display-top-question-word');
  if (questionWordElement) {
    questionWordElement.classList.remove('empty-content');
    console.log("🔓 疑問詞エリアを強制表示にしました");
  }
}

/**
 * 疑問詞エリアに内容をセットして表示制御も行う
 */
function setQuestionWordContent(content) {
  const questionWordElement = document.getElementById('display-top-question-word');
  
  if (!questionWordElement) {
    console.warn("⚠️ display-top-question-word要素が見つかりません");
    return;
  }
  
  // 内容をセット
  if (content && content.trim() !== '') {
    questionWordElement.textContent = content.trim();
    console.log("📝 疑問詞エリアに内容をセット:", content.trim());
  } else {
    questionWordElement.textContent = '';
    console.log("🗑️ 疑問詞エリアの内容をクリア");
  }
  
  // 表示制御を実行
  controlQuestionWordDisplay();
}

/**
 * DOM読み込み完了時に疑問詞エリアの初期状態をチェック
 */
document.addEventListener('DOMContentLoaded', () => {
  console.log("🚀 疑問詞エリア表示制御を初期化");
  
  // 初期状態をチェック
  controlQuestionWordDisplay();
  
  // MutationObserver で内容変更を監視
  const questionWordElement = document.getElementById('display-top-question-word');
  if (questionWordElement) {
    const observer = new MutationObserver(() => {
      console.log("🔄 疑問詞エリアの内容が変更されました");
      controlQuestionWordDisplay();
    });
    
    observer.observe(questionWordElement, {
      childList: true,
      subtree: true,
      characterData: true
    });
    
    console.log("👁️ 疑問詞エリアの内容変更監視を開始");
  }
});

// グローバル関数として公開
window.controlQuestionWordDisplay = controlQuestionWordDisplay;
window.hideQuestionWordArea = hideQuestionWordArea;
window.showQuestionWordArea = showQuestionWordArea;
window.setQuestionWordContent = setQuestionWordContent;

console.log("✅ 疑問詞エリア表示制御モジュールが読み込まれました");
