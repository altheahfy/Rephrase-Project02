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
   * 各スロットに解説ボタンを追加
   */
  addExplanationButtons() {
    // 既存の解説ボタンを削除
    document.querySelectorAll('.slot-explanation-btn').forEach(btn => btn.remove());
    
    // 全スロットコンテナを取得
    const slotContainers = document.querySelectorAll('.slot-container');
    
    slotContainers.forEach(container => {
      // 既に解説ボタンがある場合はスキップ
      if (container.querySelector('.slot-explanation-btn')) {
        return;
      }
      
      // スロットID取得
      const slotId = container.id;
      
      // 解説ボタンを作成
      const explanationBtn = document.createElement('button');
      explanationBtn.className = 'slot-explanation-btn';
      explanationBtn.textContent = '💡 解説';
      explanationBtn.title = 'この項目の解説を表示';
      
      // クリックイベント
      explanationBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.showExplanationForSlot(slotId);
      });
      
      // スロットコンテナのヘッダー部分に追加
      const slotHeader = container.querySelector('.slot-header') || container;
      if (slotHeader) {
        slotHeader.appendChild(explanationBtn);
      }
    });
    
    console.log(`📝 ${slotContainers.length} 個のスロットに解説ボタンを追加しました`);
  }
  
  /**
   * 特定のスロットの解説を表示
   * @param {string} slotId - スロットID
   */
  showExplanationForSlot(slotId) {
    console.log(`💡 スロット ${slotId} の解説を表示`);
    
    // JSONデータが読み込まれているかチェック
    if (!window.loadedJsonData || !Array.isArray(window.loadedJsonData)) {
      this.showErrorMessage('JSONデータが読み込まれていません。先にJSONファイルを読み込んでください。');
      return;
    }
    
    // 現在のV_group_keyを取得
    const currentVGroupKey = this.getCurrentVGroupKey(slotId);
    if (!currentVGroupKey) {
      this.showErrorMessage('現在のV_group_keyが特定できません。');
      return;
    }
    
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
   * 現在のV_group_keyを取得
   * @param {string} slotId - スロットID
   * @returns {string|null} V_group_key
   */
  getCurrentVGroupKey(slotId) {
    // ランダマイザの状態から取得
    if (window.currentRandomizedState && window.currentRandomizedState.vGroupKey) {
      return window.currentRandomizedState.vGroupKey;
    }
    
    // スロットのデータから推測
    const slotContainer = document.getElementById(slotId);
    if (slotContainer) {
      const phraseElement = slotContainer.querySelector('.slot-phrase');
      if (phraseElement && phraseElement.textContent.trim()) {
        // JSONデータから該当するV_group_keyを検索
        const matchingData = window.loadedJsonData.find(item => 
          item.SlotPhrase === phraseElement.textContent.trim()
        );
        if (matchingData) {
          return matchingData.V_group_key;
        }
      }
    }
    
    return null;
  }
  
  /**
   * 解説データを検索
   * @param {string} vGroupKey - V_group_key
   * @returns {Object|null} 解説データ
   */
  findExplanationData(vGroupKey) {
    if (!window.loadedJsonData) return null;
    
    // 完全一致で検索
    let explanationData = window.loadedJsonData.find(item => 
      item.V_group_key === vGroupKey && 
      item.Slot === 'EXPLANATION'
    );
    
    // 見つからない場合は部分一致で検索
    if (!explanationData) {
      explanationData = window.loadedJsonData.find(item => 
        item.V_group_key && 
        item.V_group_key.includes(vGroupKey) && 
        item.Slot === 'EXPLANATION'
      );
    }
    
    // 一般的な解説を検索（intransitive_verbsなど）
    if (!explanationData) {
      explanationData = window.loadedJsonData.find(item => 
        item.V_group_key === 'intransitive_verbs' && 
        item.Slot === 'EXPLANATION'
      );
    }
    
    return explanationData;
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
