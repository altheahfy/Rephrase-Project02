// 分離疑問詞表示制御システム
// display-top-question-word エリアの表示内容と制御パネル連携

// 🎯 疑問詞の日本語訳マッピング
const QUESTION_WORD_TRANSLATIONS = {
  'what': '何？',
  'who': '誰？',
  'where': 'どこ？',
  'when': 'いつ？',
  'why': 'なぜ？',
  'how': 'どのように？',
  'which': 'どれ？',
  'whose': '誰の？'
};

// 🎯 分離疑問詞の表示状態管理
let questionWordData = {
  text: '',
  auxtext: '',
  visible: true
};

// 🔄 分離疑問詞データの設定
function setQuestionWordData(text, auxtext = '') {
  questionWordData.text = text || '';
  
  // 補助テキストが指定されていない場合は自動生成
  if (!auxtext && text) {
    auxtext = QUESTION_WORD_TRANSLATIONS[text.toLowerCase()] || '';
    console.log(`🤖 補助テキストを自動生成: "${text}" → "${auxtext}"`);
  }
  
  questionWordData.auxtext = auxtext || '';
  console.log(`🔤 分離疑問詞データ設定: text="${text}", auxtext="${auxtext}"`);
  updateQuestionWordDisplay();
}

// 🔄 分離疑問詞の表示更新
function updateQuestionWordDisplay() {
  const textElement = document.getElementById('question-word-text');
  const auxtextElement = document.getElementById('question-word-auxtext');
  
  if (!textElement || !auxtextElement) {
    console.warn("⚠ 分離疑問詞表示要素が見つかりません");
    return;
  }
  
  // テキスト表示の制御
  const isTextVisible = getQuestionWordVisibility('text');
  const isAuxtextVisible = getQuestionWordVisibility('auxtext');
  
  if (isTextVisible && questionWordData.text) {
    textElement.textContent = questionWordData.text;
    textElement.style.display = 'block';
  } else {
    textElement.style.display = 'none';
  }
  
  // 補助テキスト表示の制御
  if (isAuxtextVisible && questionWordData.auxtext) {
    auxtextElement.textContent = questionWordData.auxtext;
    auxtextElement.style.display = 'block';
  } else {
    auxtextElement.style.display = 'none';
  }
  
  console.log(`🔄 分離疑問詞表示更新: text=${isTextVisible ? '表示' : '非表示'}, auxtext=${isAuxtextVisible ? '表示' : '非表示'}`);
}

// 🔍 分離疑問詞の表示状態取得
function getQuestionWordVisibility(elementType) {
  // 表示制御システムから状態を取得
  if (window.getSlotVisibilityState) {
    const state = window.getSlotVisibilityState('question-word');
    return state?.[elementType] ?? true;
  }
  
  // フォールバック: チェックボックスから直接取得
  const checkbox = document.querySelector(`.visibility-checkbox[data-slot="question-word"][data-type="${elementType}"]`);
  return checkbox ? checkbox.checked : true;
}

// 🔄 分離疑問詞の表示/非表示切り替え
function toggleQuestionWordVisibility(elementType, isVisible) {
  console.log(`🎛️ 分離疑問詞表示切り替え: ${elementType} = ${isVisible ? '表示' : '非表示'}`);
  
  // 既存の表示制御システムを使用
  if (window.toggleSlotElementVisibility) {
    window.toggleSlotElementVisibility('question-word', elementType, isVisible);
  }
  
  // 表示を更新
  updateQuestionWordDisplay();
}

// 🔄 分離疑問詞エリアの初期化
function initializeQuestionWordArea() {
  console.log("🔄 分離疑問詞エリアを初期化中...");
  
  const questionWordArea = document.getElementById('display-top-question-word');
  if (!questionWordArea) {
    console.warn("⚠ 分離疑問詞エリアが見つかりません");
    return;
  }
  
  // 既存の古い形式のコンテンツをクリア
  const textElement = document.getElementById('question-word-text');
  const auxtextElement = document.getElementById('question-word-auxtext');
  
  if (textElement && auxtextElement) {
    // 新形式の場合は何もしない（既に正しい構造）
    console.log("✅ 分離疑問詞エリアは既に新形式です");
  } else {
    // 古い形式の場合は内容をクリア
    console.log("🔄 古い形式から新形式に移行中...");
    questionWordArea.innerHTML = `
      <!-- メインテキスト表示エリア -->
      <div id="question-word-text" class="question-word-element" style="margin-bottom: 0.5rem;"></div>
      <!-- 補助テキスト表示エリア -->
      <div id="question-word-auxtext" class="question-word-element" style="font-size: 1rem; color: #666; font-weight: normal;"></div>
    `;
  }
  
  console.log("✅ 分離疑問詞エリア初期化完了");
}

// 🔄 分離疑問詞のリセット
function resetQuestionWordArea() {
  console.log("🔄 分離疑問詞エリアをリセット");
  setQuestionWordData('', '');
}

// 🧪 分離疑問詞機能のテスト関数
function testQuestionWordFeatures() {
  console.log("🧪 分離疑問詞機能テスト開始");
  
  // テスト1: What の設定と自動翻訳
  console.log("\n=== テスト1: What の設定 ===");
  setQuestionWordData('What');
  
  // テスト2: Who の設定と自動翻訳
  setTimeout(() => {
    console.log("\n=== テスト2: Who の設定 ===");
    setQuestionWordData('Who');
  }, 2000);
  
  // テスト3: 制御パネルでの切り替えテスト
  setTimeout(() => {
    console.log("\n=== テスト3: 表示切り替えテスト ===");
    console.log("📄テキストを非表示にします");
    toggleQuestionWordVisibility('text', false);
    
    setTimeout(() => {
      console.log("📝補助テキストを非表示にします");
      toggleQuestionWordVisibility('auxtext', false);
      
      setTimeout(() => {
        console.log("🔄すべてを再表示します");
        toggleQuestionWordVisibility('text', true);
        toggleQuestionWordVisibility('auxtext', true);
      }, 1500);
    }, 1500);
  }, 4000);
  
  // テスト4: カスタム補助テキストのテスト
  setTimeout(() => {
    console.log("\n=== テスト4: カスタム補助テキスト ===");
    setQuestionWordData('Where', 'カスタム場所？');
  }, 8000);
  
  console.log("✅ テストシーケンスを開始しました（10秒間）");
}

// 🔧 デバッグ用: 分離疑問詞エリアの状態を確認
function debugQuestionWordArea() {
  console.log("🔍 分離疑問詞エリアの状態を確認:");
  
  // DOM要素の存在確認
  const questionWordArea = document.getElementById('display-top-question-word');
  const textElement = document.getElementById('question-word-text');
  const auxtextElement = document.getElementById('question-word-auxtext');
  
  console.log("📍 DOM要素の状態:");
  console.log("  - エリア:", questionWordArea ? "✅存在" : "❌不存在");
  console.log("  - テキスト要素:", textElement ? "✅存在" : "❌不存在");
  console.log("  - 補助テキスト要素:", auxtextElement ? "✅存在" : "❌不存在");
  
  // 制御パネルのチェックボックス確認
  const textCheckbox = document.querySelector('.visibility-checkbox[data-slot="question-word"][data-type="text"]');
  const auxtextCheckbox = document.querySelector('.visibility-checkbox[data-slot="question-word"][data-type="auxtext"]');
  
  console.log("📍 制御パネルのチェックボックス:");
  console.log("  - テキスト:", textCheckbox ? `✅存在 (${textCheckbox.checked ? 'チェック済み' : 'チェックなし'})` : "❌不存在");
  console.log("  - 補助テキスト:", auxtextCheckbox ? `✅存在 (${auxtextCheckbox.checked ? 'チェック済み' : 'チェックなし'})` : "❌不存在");
  
  // データの状態確認
  console.log("📍 データ状態:");
  console.log("  - questionWordData:", questionWordData);
  
  // 表示状態確認
  console.log("📍 表示状態:");
  console.log("  - text visibility:", getQuestionWordVisibility('text'));
  console.log("  - auxtext visibility:", getQuestionWordVisibility('auxtext'));
  
  return {
    dom: { questionWordArea, textElement, auxtextElement },
    checkboxes: { textCheckbox, auxtextCheckbox },
    data: questionWordData,
    visibility: {
      text: getQuestionWordVisibility('text'),
      auxtext: getQuestionWordVisibility('auxtext')
    }
  };
}

// 🔧 制御パネルのイベントリスナーを手動で設定
function setupQuestionWordControlListeners() {
  console.log("🔧 分離疑問詞制御パネルのイベントリスナーを設定中...");
  
  // 全ての制御パネルで分離疑問詞のチェックボックスを探す
  const textCheckboxes = document.querySelectorAll('.visibility-checkbox[data-slot="question-word"][data-type="text"]');
  const auxtextCheckboxes = document.querySelectorAll('.visibility-checkbox[data-slot="question-word"][data-type="auxtext"]');
  
  console.log(`📋 見つかったチェックボックス: text=${textCheckboxes.length}個, auxtext=${auxtextCheckboxes.length}個`);
  
  // テキストチェックボックスの設定
  textCheckboxes.forEach((checkbox, index) => {
    console.log(`🔧 テキストチェックボックス ${index + 1} にイベントリスナーを設定`);
    checkbox.removeEventListener('change', handleQuestionWordTextChange);
    checkbox.addEventListener('change', handleQuestionWordTextChange);
  });
  
  // 補助テキストチェックボックスの設定
  auxtextCheckboxes.forEach((checkbox, index) => {
    console.log(`🔧 補助テキストチェックボックス ${index + 1} にイベントリスナーを設定`);
    checkbox.removeEventListener('change', handleQuestionWordAuxtextChange);
    checkbox.addEventListener('change', handleQuestionWordAuxtextChange);
  });
  
  if (textCheckboxes.length === 0) {
    console.warn("⚠ テキストチェックボックスが見つかりません");
  }
  
  if (auxtextCheckboxes.length === 0) {
    console.warn("⚠ 補助テキストチェックボックスが見つかりません");
  }
  
  console.log("✅ 分離疑問詞制御パネルのイベントリスナー設定完了");
}

// 🎛️ イベントハンドラー
function handleQuestionWordTextChange(event) {
  const isVisible = event.target.checked;
  console.log(`🎛️ 疑問詞テキスト表示切り替え: ${isVisible ? '表示' : '非表示'}`);
  toggleQuestionWordVisibility('text', isVisible);
}

function handleQuestionWordAuxtextChange(event) {
  const isVisible = event.target.checked;
  console.log(`🎛️ 疑問詞補助テキスト表示切り替え: ${isVisible ? '表示' : '非表示'}`);
  toggleQuestionWordVisibility('auxtext', isVisible);
}

// 🔧 分離疑問詞エリアを強制的に修正
function forceFixQuestionWordArea() {
  console.log("🔧 分離疑問詞エリアを強制修正中...");
  
  const questionWordArea = document.getElementById('display-top-question-word');
  if (!questionWordArea) {
    console.error("❌ 分離疑問詞エリアが見つかりません");
    return false;
  }
  
  console.log("📍 修正前の内容:", questionWordArea.innerHTML);
  
  // 既存の内容をクリアして新しい構造を作成
  questionWordArea.innerHTML = `
    <!-- メインテキスト表示エリア -->
    <div id="question-word-text" class="question-word-element" style="margin-bottom: 0.5rem;"></div>
    <!-- 補助テキスト表示エリア -->
    <div id="question-word-auxtext" class="question-word-element" style="font-size: 1rem; color: #666; font-weight: normal;"></div>
  `;
  
  console.log("📍 修正後の内容:", questionWordArea.innerHTML);
  console.log("✅ 分離疑問詞エリアの構造を修正しました");
  
  // 要素の存在確認
  const textElement = document.getElementById('question-word-text');
  const auxtextElement = document.getElementById('question-word-auxtext');
  console.log("📍 作成された要素:");
  console.log("  - textElement:", textElement ? "✅存在" : "❌不存在");
  console.log("  - auxtextElement:", auxtextElement ? "✅存在" : "❌不存在");
  
  // データを再設定して表示
  if (questionWordData.text) {
    updateQuestionWordDisplay();
    console.log("✅ 表示を更新しました");
  }
  
  return true;
}

// 🔧 緊急時の完全修復関数
function emergencyFixQuestionWordArea() {
  console.log("🚨 緊急修復: 分離疑問詞エリアを完全に再構築します");
  
  const questionWordArea = document.getElementById('display-top-question-word');
  if (!questionWordArea) {
    console.error("❌ 分離疑問詞エリアが見つかりません");
    return false;
  }
  
  // 既存の内容を完全にクリア
  questionWordArea.innerHTML = '';
  
  // 新しい構造を作成
  const textElement = document.createElement('div');
  textElement.id = 'question-word-text';
  textElement.className = 'question-word-element';
  textElement.style.marginBottom = '0.5rem';
  
  const auxtextElement = document.createElement('div');
  auxtextElement.id = 'question-word-auxtext';
  auxtextElement.className = 'question-word-element';
  auxtextElement.style.fontSize = '1rem';
  auxtextElement.style.color = '#666';
  auxtextElement.style.fontWeight = 'normal';
  
  questionWordArea.appendChild(textElement);
  questionWordArea.appendChild(auxtextElement);
  
  console.log("✅ 緊急修復完了");
  
  // 要素の存在確認
  const checkText = document.getElementById('question-word-text');
  const checkAuxtext = document.getElementById('question-word-auxtext');
  console.log("📍 修復後の確認:");
  console.log("  - textElement:", checkText ? "✅存在" : "❌不存在");
  console.log("  - auxtextElement:", checkAuxtext ? "✅存在" : "❌不存在");
  
  // データを再設定
  if (questionWordData.text) {
    updateQuestionWordDisplay();
    console.log("✅ 表示を更新しました");
  }
  
  return true;
}

// 🧪 テスト用便利関数
function quickTest() {
  console.log("🧪 クイックテスト開始");
  debugQuestionWordArea();
  console.log("🔄 'What'を設定します");
  setQuestionWordData('What');
}

function quickReset() {
  console.log("🔄 クイックリセット");
  resetQuestionWordArea();
}

function quickDebug() {
  console.log("🔍 クイックデバッグ");
  return debugQuestionWordArea();
}

// 🔹 グローバル関数としてエクスポート
window.setQuestionWordData = setQuestionWordData;
window.updateQuestionWordDisplay = updateQuestionWordDisplay;
window.getQuestionWordVisibility = getQuestionWordVisibility;
window.toggleQuestionWordVisibility = toggleQuestionWordVisibility;
window.initializeQuestionWordArea = initializeQuestionWordArea;
window.resetQuestionWordArea = resetQuestionWordArea;
window.testQuestionWordFeatures = testQuestionWordFeatures;
window.debugQuestionWordArea = debugQuestionWordArea;
window.setupQuestionWordControlListeners = setupQuestionWordControlListeners;
window.forceFixQuestionWordArea = forceFixQuestionWordArea;
window.emergencyFixQuestionWordArea = emergencyFixQuestionWordArea;
window.emergencyFixQuestionWordArea = emergencyFixQuestionWordArea;

// テスト用便利関数もエクスポート
window.quickTest = quickTest;
window.quickReset = quickReset;
window.quickDebug = quickDebug;

// 🔄 ページ読み込み時の自動初期化
document.addEventListener('DOMContentLoaded', function() {
  console.log("🔄 分離疑問詞システムを初期化中...");
  
  // 少し遅らせて実行（他のシステムの初期化完了を待つ）
  setTimeout(() => {
    // 強制的に構造を修正
    forceFixQuestionWordArea();
    
    // 追加の確認と修復
    setTimeout(() => {
      const textElement = document.getElementById('question-word-text');
      const auxtextElement = document.getElementById('question-word-auxtext');
      
      if (!textElement || !auxtextElement) {
        console.log("⚠ 要素がまだ存在しないため、再度修復を実行します");
        forceFixQuestionWordArea();
      }
      
      initializeQuestionWordArea();
      setupQuestionWordControlListeners();
      
      // テスト用の疑問詞データを設定
      setQuestionWordData('What');
      
      console.log("✅ 分離疑問詞システムの初期化完了");
    }, 200);
    
  }, 500); // 500msに増加してより確実にする
});

console.log("✅ question_word_control.js が読み込まれました");
