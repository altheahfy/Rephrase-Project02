// explanation_system.js - 解説モーダルダイアログシステム

/**
 * 解説システムクラス
 */
class ExplanationSystem {
  constructor() {
    this.modal = null;
    this.modalTitle = null;
    this.modalContent = null;
    this.modalVGroupKey = null;
    this.closeBtn = null;
    this.loadedJsonData = null;
    
    this.init();
  }
  
  /**
   * システム初期化
   */
  init() {
    // DOM要素を取得
    this.modal = document.getElementById('explanationModal');
    this.modalTitle = document.getElementById('explanationModalTitle');
    this.modalContent = document.getElementById('explanationContent');
    this.modalVGroupKey = document.getElementById('explanationVGroupKey');
    this.closeBtn = document.getElementById('explanationModalClose');
    
    if (!this.modal) {
      console.warn('⚠️ 解説モーダルのDOM要素が見つかりません');
      return;
    }
    
    // イベントリスナーを設定
    this.setupEventListeners();
    
    // スロットに解説ボタンを追加
    this.addExplanationButtons();
    
    console.log('✅ 解説システム初期化完了');
  }
  
  /**
   * イベントリスナーを設定
   */
  setupEventListeners() {
    // 閉じるボタン
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.hideModal());
    }
    
    // 背景クリックで閉じる
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) {
        this.hideModal();
      }
    });
    
    // ESCキーで閉じる
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.modal.classList.contains('show')) {
        this.hideModal();
      }
    });
  }
  
  /**
   * 例文シャッフルボタンの右横に解説ボタンを追加
   */
  addExplanationButtons() {
    // 既存の解説ボタンを削除
    document.querySelectorAll('.slot-explanation-btn').forEach(btn => btn.remove());
    
    // 例文シャッフルボタンを探す
    const randomizeBtn = document.getElementById('randomizeAll');
    if (!randomizeBtn) {
      console.warn('⚠️ 例文シャッフルボタンが見つかりません');
      return;
    }
    
    // 解説ボタンを作成
    const explanationBtn = document.createElement('button');
    explanationBtn.className = 'slot-explanation-btn';
    explanationBtn.textContent = '💡 解説';
    explanationBtn.title = '現在の例文の解説を表示';
    explanationBtn.style.marginLeft = '10px';
    
    // クリックイベント
    explanationBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.showCurrentExplanation();
    });
    
    // シャッフルボタンの右横に追加
    randomizeBtn.parentNode.insertBefore(explanationBtn, randomizeBtn.nextSibling);
    
    console.log('📝 例文シャッフルボタンの右横に解説ボタンを追加しました');
  }
  
  /**
   * 現在の例文の解説を表示
   */
  showCurrentExplanation() {
    console.log('💡 現在の例文の解説を表示');
    
    // JSONデータが読み込まれているかチェック
    if (!window.loadedJsonData || !Array.isArray(window.loadedJsonData)) {
      this.showErrorMessage('JSONデータが読み込まれていません。先にJSONファイルを読み込んでください。');
      return;
    }
    
    // 現在のV_group_keyを取得
    const currentVGroupKey = this.getCurrentVGroupKey();
    if (!currentVGroupKey) {
      this.showErrorMessage('現在のV_group_keyが特定できません。先に例文をシャッフルしてください。');
      return;
    }
    
    console.log(`🔍 V_group_key検索: ${currentVGroupKey}`);
    
    // 解説データを検索
    const explanationData = this.findExplanationData(currentVGroupKey);
    if (!explanationData) {
      this.showErrorMessage(`「${currentVGroupKey}」の解説データが見つかりません。`);
      return;
    }
    
    // モーダルに解説を表示
    this.showModal(explanationData);
  }
  
  /**
   * 特定のスロットの解説を表示（旧関数）
   * @param {string} slotId - スロットID
   */
  showExplanationForSlot(slotId) {
    this.showCurrentExplanation();
  }
  
  /**
   * 現在のV_group_keyを取得
   * @param {string} slotId - スロットID（オプション）
   * @returns {string|null} V_group_key
   */
  getCurrentVGroupKey(slotId = null) {
    // ランダマイザの状態から取得
    if (window.currentRandomizedState && window.currentRandomizedState.vGroupKey) {
      console.log(`✅ V_group_key取得成功（ランダマイザ状態）: ${window.currentRandomizedState.vGroupKey}`);
      return window.currentRandomizedState.vGroupKey;
    }
    
    // 別のグローバル変数をチェック
    if (window.lastSelectedVGroupKey) {
      console.log(`✅ V_group_key取得成功（lastSelected）: ${window.lastSelectedVGroupKey}`);
      return window.lastSelectedVGroupKey;
    }
    
    // Sスロット（動詞）から推測
    const sSlot = document.getElementById('slot-s');
    if (sSlot) {
      const phraseElement = sSlot.querySelector('.slot-phrase');
      if (phraseElement && phraseElement.textContent.trim()) {
        const phrase = phraseElement.textContent.trim();
        console.log(`🔍 Sスロットから動詞を検索: ${phrase}`);
        
        // JSONデータから該当するV_group_keyを検索
        const matchingData = window.loadedJsonData.find(item => 
          item.Slot === 'S' && item.SlotPhrase === phrase
        );
        if (matchingData && matchingData.V_group_key) {
          console.log(`✅ V_group_key取得成功（Sスロット）: ${matchingData.V_group_key}`);
          return matchingData.V_group_key;
        }
      }
    }
    
    // M1スロット（主語）から推測
    const m1Slot = document.getElementById('slot-m1');
    if (m1Slot) {
      const phraseElement = m1Slot.querySelector('.slot-phrase');
      if (phraseElement && phraseElement.textContent.trim()) {
        const phrase = phraseElement.textContent.trim();
        console.log(`🔍 M1スロットから推測: ${phrase}`);
        
        // JSONデータから該当するV_group_keyを検索
        const matchingData = window.loadedJsonData.find(item => 
          item.Slot === 'M1' && item.SlotPhrase === phrase
        );
        if (matchingData && matchingData.V_group_key) {
          console.log(`✅ V_group_key取得成功（M1スロット）: ${matchingData.V_group_key}`);
          return matchingData.V_group_key;
        }
      }
    }
    
    console.warn('⚠️ V_group_keyの取得に失敗');
    return null;
  }
  
  /**
   * 解説データを検索
   * @param {string} vGroupKey - V_group_key
   * @returns {Object|null} 解説データ
   */
  findExplanationData(vGroupKey) {
    if (!window.loadedJsonData) return null;
    
    console.log(`🔍 解説データ検索開始: ${vGroupKey}`);
    
    // 完全一致で検索
    let explanationData = window.loadedJsonData.find(item => 
      item.V_group_key === vGroupKey && 
      item.Slot === 'EXPLANATION'
    );
    
    if (explanationData) {
      console.log(`✅ 完全一致で解説データ発見: ${vGroupKey}`);
      return explanationData;
    }
    
    // 動詞の原形で検索（apologizes → apologize）
    const baseForm = vGroupKey.replace(/s$/, ''); // 単純にsを削除
    explanationData = window.loadedJsonData.find(item => 
      item.V_group_key === baseForm && 
      item.Slot === 'EXPLANATION'
    );
    
    if (explanationData) {
      console.log(`✅ 動詞原形で解説データ発見: ${baseForm}`);
      return explanationData;
    }
    
    // 部分一致で検索
    explanationData = window.loadedJsonData.find(item => 
      item.V_group_key && 
      (item.V_group_key.includes(vGroupKey) || vGroupKey.includes(item.V_group_key)) && 
      item.Slot === 'EXPLANATION'
    );
    
    if (explanationData) {
      console.log(`✅ 部分一致で解説データ発見: ${explanationData.V_group_key}`);
      return explanationData;
    }
    
    // 一般的な自動詞解説を検索
    explanationData = window.loadedJsonData.find(item => 
      item.V_group_key === 'intransitive_verbs' && 
      item.Slot === 'EXPLANATION'
    );
    
    if (explanationData) {
      console.log(`✅ 一般的な自動詞解説を表示: intransitive_verbs`);
      return explanationData;
    }
    
    console.warn(`⚠️ 解説データが見つかりません: ${vGroupKey}`);
    
    // デバッグ用：利用可能な解説データを表示
    const availableExplanations = window.loadedJsonData
      .filter(item => item.Slot === 'EXPLANATION')
      .map(item => item.V_group_key);
    console.log('📋 利用可能な解説データ:', availableExplanations);
    
    return null;
  }
  
  /**
   * モーダルに解説を表示
   * @param {Object} explanationData - 解説データ
   */
  showModal(explanationData) {
    if (!explanationData) return;
    
    // タイトルを設定
    this.modalTitle.textContent = explanationData.explanation_title || '解説';
    
    // V_group_keyを表示
    this.modalVGroupKey.textContent = explanationData.V_group_key || '';
    
    // 解説内容を設定
    const content = explanationData.explanation_content || '解説内容がありません。';
    
    // 改行を<br>に変換
    const formattedContent = content.replace(/\n/g, '<br>');
    this.modalContent.innerHTML = formattedContent;
    
    // モーダルを表示
    this.modal.classList.add('show');
    
    console.log(`✅ 解説モーダル表示: ${explanationData.V_group_key}`);
  }
  
  /**
   * エラーメッセージを表示
   * @param {string} message - エラーメッセージ
   */
  showErrorMessage(message) {
    this.modalTitle.textContent = 'エラー';
    this.modalVGroupKey.textContent = '';
    this.modalContent.innerHTML = `<p style="color: #f44336; font-weight: bold;">⚠️ ${message}</p>`;
    this.modal.classList.add('show');
  }
  
  /**
   * モーダルを非表示
   */
  hideModal() {
    this.modal.classList.remove('show');
    console.log('📴 解説モーダル非表示');
  }
  
  /**
   * JSONデータ更新時の処理
   */
  onJsonDataUpdated() {
    // 解説ボタンを再追加
    this.addExplanationButtons();
    console.log('🔄 JSONデータ更新により解説ボタンを再設定');
  }
}

// グローバルインスタンス
let explanationSystem = null;

// DOMContentLoadedイベントでシステムを初期化
document.addEventListener('DOMContentLoaded', () => {
  explanationSystem = new ExplanationSystem();
});

// JSONデータが更新された時に解説ボタンを再設定
document.addEventListener('jsonDataLoaded', () => {
  if (explanationSystem) {
    explanationSystem.onJsonDataUpdated();
  }
});

// 外部からアクセス可能な関数
window.showExplanation = function(vGroupKey) {
  if (explanationSystem) {
    const explanationData = explanationSystem.findExplanationData(vGroupKey);
    if (explanationData) {
      explanationSystem.showModal(explanationData);
    } else {
      explanationSystem.showErrorMessage(`「${vGroupKey}」の解説が見つかりません。`);
    }
  }
};

console.log('📚 解説システムスクリプト読み込み完了');
