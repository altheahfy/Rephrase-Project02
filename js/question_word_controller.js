/**
 * 疑問詞エリア表示制御
 * display-top-question-wordの空判定と非表示制御
 */

/**
 * 分離疑問詞の日本語訳マッピング
 */
const questionWordTranslations = {
  'What': '何？',
  'Who': '誰？',
  'When': 'いつ？',
  'Where': 'どこ？',
  'Why': 'なぜ？',
  'How': 'どのように？',
  'Which': 'どちら？',
  'Whose': '誰の？',
  'Whom': '誰を？',
  'How many': 'いくつ？',
  'How much': 'いくら？',
  'How long': 'どのくらい？',
  'How often': 'どのくらいの頻度で？',
  'How far': 'どのくらい遠く？'
};

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
 * 分離疑問詞かどうかを判定する
 * @param {string} text - チェックするテキスト
 * @returns {boolean} 分離疑問詞の場合true
 */
function isQuestionWord(text) {
  if (!text) return false;
  const cleanText = text.trim();
  return Object.keys(questionWordTranslations).includes(cleanText);
}

/**
 * 分離疑問詞エリアにテキストと補助テキストを表示する
 * @param {string} questionWord - 疑問詞（例: "What"）
 */
function displayQuestionWord(questionWord) {
  const questionWordElement = document.getElementById('display-top-question-word');
  if (!questionWordElement) {
    console.warn("⚠️ display-top-question-word要素が見つかりません");
    return;
  }

  // 疑問詞テキストと補助テキストの要素を取得
  const textElement = questionWordElement.querySelector('.question-word-text');
  const auxtextElement = questionWordElement.querySelector('.question-word-auxtext');
  
  if (!textElement || !auxtextElement) {
    console.warn("⚠️ 疑問詞エリアの子要素が見つかりません");
    return;
  }

  // テキストを設定
  textElement.textContent = questionWord;
  
  // 補助テキスト（日本語訳）を設定
  const translation = questionWordTranslations[questionWord] || '';
  auxtextElement.textContent = translation;
  
  // 表示状態にする
  questionWordElement.classList.remove('empty-content');
  questionWordElement.style.display = 'block';
  
  console.log(`✅ 分離疑問詞を表示しました: ${questionWord} (${translation})`);
  
  // 制御パネルの設定に基づいて表示/非表示を制御
  applyQuestionWordVisibility();
}

/**
 * 分離疑問詞エリアをクリアする
 */
function clearQuestionWord() {
  const questionWordElement = document.getElementById('display-top-question-word');
  if (!questionWordElement) return;

  const textElement = questionWordElement.querySelector('.question-word-text');
  const auxtextElement = questionWordElement.querySelector('.question-word-auxtext');
  
  if (textElement) textElement.textContent = '';
  if (auxtextElement) auxtextElement.textContent = '';
  
  // 空状態にする
  questionWordElement.classList.add('empty-content');
  questionWordElement.style.display = 'none';
  
  console.log("🧹 分離疑問詞エリアをクリアしました");
}

/**
 * 制御パネルの設定に基づいて分離疑問詞エリアの表示/非表示を制御
 */
function applyQuestionWordVisibility() {
  const questionWordElement = document.getElementById('display-top-question-word');
  if (!questionWordElement) return;

  const textElement = questionWordElement.querySelector('.question-word-text');
  const auxtextElement = questionWordElement.querySelector('.question-word-auxtext');
  
  // 制御パネルのチェックボックスの状態を取得
  const textCheckbox = document.querySelector('.visibility-checkbox[data-slot="question-word"][data-type="text"]');
  const auxtextCheckbox = document.querySelector('.visibility-checkbox[data-slot="question-word"][data-type="auxtext"]');
  
  // テキストの表示/非表示
  if (textElement) {
    textElement.style.display = (textCheckbox && textCheckbox.checked) ? 'block' : 'none';
  }
  
  // 補助テキストの表示/非表示
  if (auxtextElement) {
    auxtextElement.style.display = (auxtextCheckbox && auxtextCheckbox.checked) ? 'block' : 'none';
  }
  
  // 両方とも非表示の場合、全体を非表示
  const isTextVisible = textElement && textElement.style.display !== 'none' && textElement.textContent.trim();
  const isAuxtextVisible = auxtextElement && auxtextElement.style.display !== 'none' && auxtextElement.textContent.trim();
  
  if (!isTextVisible && !isAuxtextVisible) {
    questionWordElement.style.display = 'none';
  } else {
    questionWordElement.style.display = 'block';
  }
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
window.displayQuestionWord = displayQuestionWord;
window.clearQuestionWord = clearQuestionWord;

console.log("✅ 疑問詞エリア表示制御モジュールが読み込まれました");
