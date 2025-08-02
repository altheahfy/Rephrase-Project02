/**
 * 📚 解説システム - state-manager.js統合版
 * RephraseStateManagerとの統合
 * - explanation.modal.visible: モーダル表示状態
 * - explanation.data.explanationData: 解説データ配列
 * - explanation.ui.buttons.explanation: 解説ボタン表示状態
 * - explanation.context.currentVGroupKey: 現在のV_group_key
 */

class ExplanationSystem {
  constructor() {
    // RephraseStateManagerのインスタンスを取得または作成
    this.stateManager = window.stateManager || new window.RephraseStateManager();
    
    // グローバルにインスタンスを保存（他のマネージャーとの共用）
    if (!window.stateManager) {
      window.stateManager = this.stateManager;
    }
    
    this.modal = null;
    this.isInitialized = false;
    
    // State paths for RephraseStateManager
    this.STATE_PATHS = {
      MODAL_VISIBLE: 'explanation.modal.visible',
      EXPLANATION_DATA: 'explanation.data.explanationData',
      BUTTON_VISIBLE: 'explanation.ui.buttons.explanation',
      CURRENT_V_GROUP_KEY: 'explanation.context.currentVGroupKey',
      INITIALIZATION_STATUS: 'explanation.system.isInitialized'
    };
    
    console.log('🎯 ExplanationSystem初期化開始');
    this.initializeState();
  }

  // 初期状態の設定
  initializeState() {
    const defaultState = {
      explanation: {
        modal: {
          visible: false
        },
        data: {
          explanationData: []
        },
        ui: {
          buttons: {
            explanation: true
          }
        },
        context: {
          currentVGroupKey: null
        },
        system: {
          isInitialized: false
        }
      }
    };
    
    // デフォルト状態をstate-managerに設定
    this.stateManager.setState('explanation', defaultState.explanation);
    console.log('✅ ExplanationSystem初期状態設定完了');
  }

  // 初期化処理
  async initialize() {
    try {
      console.log('📚 解説システム初期化中...');
      
      // モーダル要素の取得
      this.modal = document.getElementById('explanationModal');
      if (!this.modal) {
        console.error('❌ 解説モーダルが見つかりません');
        return false;
      }

      // モーダルイベントリスナーの設定
      this.setupModalEvents();
      
      // JSONデータの読み込み
      await this.loadExplanationData();
      
      // 初期化完了をstate-managerに記録
      this.stateManager.setState(this.STATE_PATHS.INITIALIZATION_STATUS, true);
      this.isInitialized = true;
      console.log('✅ 解説システム初期化完了');
      
      // 解説ボタンの自動配置を開始
      this.addExplanationButtons();
      
      return true;
      
    } catch (error) {
      console.error('❌ 解説システム初期化エラー:', error);
      this.stateManager.setState(this.STATE_PATHS.INITIALIZATION_STATUS, false);
      return false;
    }
  }

  // JSONデータの読み込み
  async loadExplanationData() {
    try {
      const response = await fetch('data/V自動詞第1文型.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const allData = await response.json();
      
      // 解説データのみをフィルタリング
      const explanationData = allData.filter(item => 
        item.explanation && item.explanation.trim() !== ""
      );
      
      // state-managerに解説データを保存
      this.stateManager.setState(this.STATE_PATHS.EXPLANATION_DATA, explanationData);
      console.log(`✅ 解説データ読み込み完了: ${explanationData.length}件`);
      
    } catch (error) {
      console.error('❌ 解説データ読み込みエラー:', error);
      // エラー時は空配列をstate-managerに設定
      this.stateManager.setState(this.STATE_PATHS.EXPLANATION_DATA, []);
    }
  }

  // モーダルイベントの設定
  setupModalEvents() {
    // 閉じるボタンのイベント
    const closeBtn = this.modal.querySelector('.explanation-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.closeModal());
    }

    // モーダル背景クリックで閉じる
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) {
        this.closeModal();
      }
    });

    // ESCキーで閉じる
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isModalOpen()) {
        this.closeModal();
      }
    });
  }

  // モーダルを開く
  openModal(title, content) {
    if (!this.modal) return;

    try {
      const titleElement = this.modal.querySelector('#explanationTitle');
      const contentElement = this.modal.querySelector('#explanationContent');

      if (titleElement) titleElement.textContent = title;
      if (contentElement) contentElement.innerHTML = content;

      this.modal.style.display = 'flex';
      // アニメーション用の遅延
      setTimeout(() => {
        this.modal.classList.add('show');
      }, 10);

      // state-managerにモーダル表示状態を記録
      this.stateManager.setState(this.STATE_PATHS.MODAL_VISIBLE, true);
      console.log('📖 解説モーダル開いた:', title);
      
    } catch (error) {
      console.error('❌ モーダル表示エラー:', error);
    }
  }

  // モーダルを閉じる
  closeModal() {
    if (!this.modal) return;

    this.modal.classList.remove('show');
    setTimeout(() => {
      this.modal.style.display = 'none';
    }, 300);

    // state-managerにモーダル非表示状態を記録
    this.stateManager.setState(this.STATE_PATHS.MODAL_VISIBLE, false);
    console.log('📖 解説モーダル閉じた');
  }

  // モーダルが開いているかチェック
  isModalOpen() {
    // state-managerから状態を取得
    return this.stateManager.getState(this.STATE_PATHS.MODAL_VISIBLE) || false;
  }

  // テスト用の解説表示
  showTestExplanation() {
    const testTitle = "解説システムテスト";
    const testContent = `
      <h4>✅ システム動作確認</h4>
      <p>解説モーダルが正常に動作しています。</p>
      <p><strong>読み込み済み解説データ:</strong> ${this.explanationData.length}件</p>
      <h4>📚 次のフェーズ</h4>
      <ul>
        <li>V_group_key検出機能の実装</li>
        <li>解説ボタンの自動配置</li>
        <li>実際の解説内容の表示</li>
      </ul>
    `;
    
    this.openModal(testTitle, testContent);
  }

  // 現在のV_group_keyを検出
  getCurrentVGroupKey() {
    try {
      console.log('🔍 V_group_key検出開始');
      
      // 新機能: window.lastSelectedSlotsから現在表示中のV_group_keyを取得
      if (window.lastSelectedSlots && window.lastSelectedSlots.length > 0) {
        const vSlot = window.lastSelectedSlots.find(slot => slot.Slot === 'V');
        if (vSlot && vSlot.V_group_key) {
          console.log('✅ window.lastSelectedSlots(Vスロット)から取得:', vSlot.V_group_key);
          return vSlot.V_group_key;
        }
        const anySlot = window.lastSelectedSlots.find(slot => slot.V_group_key);
        if (anySlot && anySlot.V_group_key) {
          console.log('✅ window.lastSelectedSlotsから取得:', anySlot.V_group_key);
          return anySlot.V_group_key;
        }
      }
      
      // 既存のロジック: 現在のランダム化状態からV_group_keyを取得
      if (window.currentRandomizedState && window.currentRandomizedState.vGroupKey) {
        console.log('✅ window.currentRandomizedState.vGroupKeyから取得:', window.currentRandomizedState.vGroupKey);
        return window.currentRandomizedState.vGroupKey;
      }
      
      // フォールバック: メインエリアの全てのスロット要素を検索
      const slotElements = document.querySelectorAll('.slot-container');
      console.log('📋 見つかったスロット数:', slotElements.length);
      
      for (const slot of slotElements) {
        console.log('🎯 スロット確認:', slot.id, slot.className);
        
        // data-v-group-key属性をチェック
        const vGroupKey = slot.getAttribute('data-v-group-key');
        if (vGroupKey) {
          console.log('🔍 V_group_key検出:', vGroupKey);
          return vGroupKey;
        }
        
        // 動詞スロット（slot-v）から動詞テキストを取得
        if (slot.id === 'slot-v') {
          const slotPhrase = slot.querySelector('.slot-phrase');
          console.log('🎯 Vスロット発見:', slotPhrase);
          if (slotPhrase) {
            const verbText = slotPhrase.textContent.trim();
            console.log('📝 動詞テキスト:', verbText);
            if (verbText) {
              console.log('🔍 動詞スロットから推測:', verbText);
              const inferredKey = this.inferVGroupKeyFromVerb(verbText);
              console.log('🎯 推測されたV_group_key:', inferredKey);
              return inferredKey;
            }
          }
        }
      }

      // 代替方法：全スロットから動詞を探す
      console.log('🔍 代替検索開始');
      const allSlotPhrases = document.querySelectorAll('.slot-phrase');
      console.log('📋 全slot-phrase数:', allSlotPhrases.length);
      
      for (const phrase of allSlotPhrases) {
        const text = phrase.textContent.trim();
        console.log('📝 検査中のテキスト:', text);
        if (text && this.isVerb(text)) {
          console.log('🔍 全スロット検索から動詞発見:', text);
          const inferredKey = this.inferVGroupKeyFromVerb(text);
          console.log('🎯 推測されたV_group_key:', inferredKey);
          return inferredKey;
        }
      }
      
      console.log('❓ V_group_keyが見つかりません');
      return null;
      
    } catch (error) {
      console.error('❌ V_group_key検出エラー:', error);
      return null;
    }
  }

  // 単語が動詞かどうかを簡易判定
  isVerb(word) {
    console.log('🔍 動詞判定チェック:', word);
    // 簡易的な動詞判定（解説データに存在するV_group_keyと一致するかチェック）
    const verbForms = [
      'recover', 'recovered', 'go', 'goes', 'went', 'pay', 'paid',
      'believe', 'believed', 'lie', 'lay', 'lies', 'apologize', 'apologized',
      'listen', 'listened', 'leave', 'left', 'stand', 'stood', 'mind', 'minded',
      'start', 'starts', 'started'
    ];
    const isVerbResult = verbForms.includes(word.toLowerCase());
    console.log('🎯 動詞判定結果:', word, '→', isVerbResult);
    return isVerbResult;
  }

  // 動詞テキストからV_group_keyを推測
  inferVGroupKeyFromVerb(verbText) {
    console.log('🔍 V_group_key推測開始:', verbText);
    // 基本形への変換ロジック（簡易版）
    const baseFormMap = {
      'recovered': 'recover',
      'goes': 'go',
      'went': 'go',
      'paid': 'pay',
      'believed': 'believe',
      'lay': 'lie',
      'lies': 'lie',
      'apologized': 'apologize',
      'listened': 'listen',
      'left': 'leave',
      'stood': 'stand',
      'minded': 'mind',
      'starts': 'start',
      'started': 'start'
    };
    
    const result = baseFormMap[verbText] || verbText.toLowerCase();
    console.log('🎯 推測結果:', verbText, '→', result);
    return result;
  }

  // V_group_keyに対応する解説データを検索
  findExplanationByVGroupKey(vGroupKey) {
    if (!vGroupKey) return null;
    
    // state-managerから解説データを取得
    const explanationData = this.stateManager.getState(this.STATE_PATHS.EXPLANATION_DATA) || [];
    if (!explanationData.length) return null;
    
    const explanation = explanationData.find(item => 
      item.V_group_key === vGroupKey
    );
    
    if (explanation) {
      console.log('📖 解説データ発見:', explanation.explanation_title);
      // 現在のV_group_keyをstate-managerに記録
      this.stateManager.setState(this.STATE_PATHS.CURRENT_V_GROUP_KEY, vGroupKey);
    } else {
      console.log('❓ 解説データなし:', vGroupKey);
    }
    
    return explanation;
  }

  // 現在のコンテキストに基づいて解説を表示
  showContextualExplanation() {
    console.log('🔍 解説表示開始');
    
    // デバッグ: 現在の解説データ一覧を表示
    console.log('📊 利用可能な解説データ:', this.explanationData.map(item => ({
      V_group_key: item.V_group_key,
      title: item.explanation_title
    })));
    
    const vGroupKey = this.getCurrentVGroupKey();
    console.log('🎯 検出されたV_group_key:', vGroupKey);
    
    if (!vGroupKey) {
      this.openModal('解説情報なし', '<p>現在表示されている内容に対応する解説が見つかりません。<br>デバッグ情報をコンソールで確認してください。</p>');
      return;
    }

    const explanation = this.findExplanationByVGroupKey(vGroupKey);
    if (!explanation) {
      // 元の動詞テキストを取得してカスタムメッセージを表示
      const originalVerb = this.getOriginalVerbText();
      const debugInfo = `
        <p>「${originalVerb || vGroupKey}」に対応する解説が見つかりません。</p>
        <h4>🔍 デバッグ情報</h4>
        <p><strong>検出されたV_group_key:</strong> ${vGroupKey}</p>
        <p><strong>元の動詞:</strong> ${originalVerb}</p>
        <p><strong>利用可能な解説:</strong></p>
        <ul>
          ${this.explanationData.map(item => 
            `<li>${item.V_group_key}: ${item.explanation_title}</li>`
          ).join('')}
        </ul>
      `;
      this.openModal('解説情報なし', debugInfo);
      return;
    }

    this.showExplanation(explanation);
  }

  // 元の動詞テキストを取得
  getOriginalVerbText() {
    try {
      // 動詞スロット（slot-v）から動詞テキストを取得
      const vSlot = document.getElementById('slot-v');
      if (vSlot) {
        const slotPhrase = vSlot.querySelector('.slot-phrase');
        if (slotPhrase) {
          return slotPhrase.textContent.trim();
        }
      }

      // 代替方法：全スロットから動詞を探す
      const allSlotPhrases = document.querySelectorAll('.slot-phrase');
      for (const phrase of allSlotPhrases) {
        const text = phrase.textContent.trim();
        if (text && this.isVerb(text)) {
          return text;
        }
      }
      
      return null;
    } catch (error) {
      console.error('❌ 元動詞テキスト取得エラー:', error);
      return null;
    }
  }

  // 解説データを表示
  showExplanation(explanationData) {
    const title = explanationData.explanation_title || '解説';
    const content = this.formatExplanationContent(explanationData);
    this.openModal(title, content);
  }

  // 解説コンテンツをHTMLフォーマット
  formatExplanationContent(data) {
    let html = '';
    
    if (data.explanation_content) {
      html += `<div class="explanation-main">${data.explanation_content}</div>`;
    }
    
    if (data.explanation_examples) {
      html += `
        <h4>📝 例文</h4>
        <div class="explanation-examples">${data.explanation_examples}</div>
      `;
    }
    
    if (data.explanation_notes) {
      html += `
        <h4>💡 補足説明</h4>
        <div class="explanation-notes">${data.explanation_notes}</div>
      `;
    }
    
    return html || '<p>解説内容が登録されていません。</p>';
  }

  // 解説ボタンを例文シャッフルボタンの右横に追加
  addExplanationButtons() {
    try {
      console.log('🔧 解説ボタン配置開始');
      
      // 例文シャッフルボタンを検索
      const shuffleBtn = document.getElementById('randomize-all');
      if (!shuffleBtn) {
        console.log('❓ 例文シャッフルボタンが見つかりません');
        return;
      }

      // 既存の解説ボタンを削除
      const existingBtn = document.getElementById('explanation-btn');
      if (existingBtn) {
        existingBtn.remove();
      }

      // 解説ボタンを作成
      const explanationBtn = document.createElement('button');
      explanationBtn.id = 'explanation-btn';
      explanationBtn.className = 'explanation-btn';
      explanationBtn.textContent = '💡 例文解説';
      explanationBtn.title = '文法解説を表示';
      
      // スタイルを例文シャッフルボタンと調和させる
      explanationBtn.style.cssText = `
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
        margin-left: 10px;
      `;
      
      // ホバーエフェクトを追加
      explanationBtn.addEventListener('mouseover', () => {
        explanationBtn.style.transform = 'scale(1.05)';
      });
      explanationBtn.addEventListener('mouseout', () => {
        explanationBtn.style.transform = 'scale(1)';
      });
      
      // クリックイベントを追加
      explanationBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.showContextualExplanation();
      });

      // シャッフルボタンの右横に配置
      shuffleBtn.insertAdjacentElement('afterend', explanationBtn);
      console.log('✅ 例文シャッフルボタンの右横に解説ボタン追加完了');
      
    } catch (error) {
      console.error('❌ 解説ボタン配置エラー:', error);
    }
  }

  // ボタンを更新（データ読み込み後などに呼ぶ）
  updateExplanationButtons() {
    if (this.isInitialized) {
      this.addExplanationButtons();
    }
  }
}

// グローバル変数として解説システムインスタンスを作成
let explanationSystem = null;

// DOMContentLoaded後に初期化
document.addEventListener('DOMContentLoaded', async () => {
  try {
    explanationSystem = new ExplanationSystem();
    await explanationSystem.initialize();
    
    // テスト用: コンソールから呼び出し可能にする
    window.testExplanation = () => {
      if (explanationSystem && explanationSystem.isInitialized) {
        explanationSystem.showTestExplanation();
      } else {
        console.log('❌ 解説システムが初期化されていません');
      }
    };

    // コンテキスト解説テスト用
    window.showExplanation = () => {
      if (explanationSystem && explanationSystem.isInitialized) {
        explanationSystem.showContextualExplanation();
      } else {
        console.log('❌ 解説システムが初期化されていません');
      }
    };
    
  } catch (error) {
    console.error('❌ 解説システム初期化失敗:', error);
  }
});
