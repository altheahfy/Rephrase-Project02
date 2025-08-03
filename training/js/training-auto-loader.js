/**
 * 文法項目自動選択システム - トレーニングUI自動JSON読み込み
 * 
 * 機能:
 * 1. URLパラメータから文法項目名を取得
 * 2. 文法項目名→JSONファイル名の自動マッピング
 * 3. 該当JSONファイルの自動読み込み
 */

class TrainingAutoLoader {
  constructor() {
    this.grammarToJsonMapping = this.initializeGrammarMapping();
  }

  /**
   * 文法項目→JSONファイルのマッピング初期化
   */
  initializeGrammarMapping() {
    return {
      // 名詞チャンク
      "冠詞・定冠詞の付け方": "冠詞・定冠詞の付け方.json",
      
      // 動詞チャンク
      "V自動詞第1文型": "V自動詞第1文型.json",
      "V他動詞第3文型": "V他動詞第3文型.json",
      "V授与動詞第4文型": "V授与動詞第4文型.json",
      "V使役動詞第5文型": "V使役動詞第5文型.json",
      
      // 助動詞関連
      "助動詞can": "助動詞can.json",
      "助動詞will": "助動詞will.json",
      "助動詞must": "助動詞must.json",
      
      // 時制関連
      "現在完了": "現在完了.json",
      "過去完了": "過去完了.json",
      "未来完了": "未来完了.json",
      
      // 疑問文関連
      "疑問詞what": "疑問詞what.json",
      "疑問詞where": "疑問詞where.json",
      "疑問詞when": "疑問詞when.json"
    };
  }

  /**
   * URLパラメータから文法項目名を取得
   */
  parseGrammarParameter() {
    const urlParams = new URLSearchParams(window.location.search);
    const grammarParam = urlParams.get('grammar');
    
    if (grammarParam) {
      console.log(`🎯 自動読み込み対象: ${grammarParam}`);
      return grammarParam;
    }
    return null;
  }

  /**
   * 文法項目名からJSONファイル名を取得
   */
  getJsonFileName(grammarName) {
    return this.grammarToJsonMapping[grammarName] || null;
  }

  /**
   * 自動JSON読み込み
   */
  async autoLoadGrammar(grammarName) {
    try {
      // 1. マッピングテーブルから対応JSONファイル取得
      const jsonFile = this.getJsonFileName(grammarName);
      
      if (!jsonFile) {
        console.error(`❌ 対応するJSONファイルが見つかりません: ${grammarName}`);
        this.showGrammarNotFoundError(grammarName);
        return;
      }
      
      // 2. JSONファイルの存在確認
      const jsonPath = `data/${jsonFile}`;
      const response = await fetch(jsonPath);
      
      if (!response.ok) {
        console.warn(`⚠️ JSONファイルが見つかりません: ${jsonPath}`);
        this.showJsonNotFoundError(grammarName, jsonFile);
        return;
      }
      
      // 3. 既存のJSON読み込み機能を活用
      console.log(`📁 ${grammarName} → ${jsonFile} を読み込み中...`);
      
      // 既存のloadJSONFile関数が存在する場合は使用
      if (typeof window.loadJSONFile === 'function') {
        await window.loadJSONFile(jsonPath);
      } else {
        // 直接読み込み
        const data = await response.json();
        console.log(`✅ JSONデータ読み込み完了:`, data.length, '件');
      }
      
      this.showAutoLoadSuccess(grammarName);
      
    } catch (error) {
      console.error(`❌ JSON読み込みエラー:`, error);
      this.showLoadError(grammarName, error);
    }
  }

  /**
   * 文法項目未対応エラー表示
   */
  showGrammarNotFoundError(grammarName) {
    this.showNotification(`❌ ${grammarName} は現在準備中です`, 'error');
  }

  /**
   * JSONファイル未存在エラー表示
   */
  showJsonNotFoundError(grammarName, jsonFile) {
    this.showNotification(`⚠️ ${grammarName} のトレーニングデータ（${jsonFile}）は準備中です`, 'warning');
  }

  /**
   * 読み込みエラー表示
   */
  showLoadError(grammarName, error) {
    this.showNotification(`❌ ${grammarName} の読み込みでエラーが発生しました`, 'error');
  }

  /**
   * 成功メッセージ表示
   */
  showAutoLoadSuccess(grammarName) {
    this.showNotification(`✅ ${grammarName} のトレーニングデータを読み込みました`, 'success');
  }

  /**
   * 通知表示共通関数
   */
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `auto-load-notification ${type}`;
    
    const bgColor = {
      'success': '#e8f5e8',
      'warning': '#fff3cd',
      'error': '#f8d7da',
      'info': '#d1ecf1'
    }[type] || '#d1ecf1';
    
    const borderColor = {
      'success': '#4CAF50',
      'warning': '#FF9800',
      'error': '#f44336',
      'info': '#2196F3'
    }[type] || '#2196F3';
    
    notification.innerHTML = `
      <div style="background: ${bgColor}; border: 1px solid ${borderColor}; padding: 15px; margin: 10px 0; border-radius: 5px; font-weight: bold;">
        ${message}
      </div>
    `;
    
    // 通知を表示
    const targetElement = document.querySelector('.container') || document.body;
    if (targetElement) {
      targetElement.insertBefore(notification, targetElement.firstChild);
      
      // 5秒後に通知を削除
      setTimeout(() => {
        notification.remove();
      }, 5000);
    }
    
    console.log(message);
  }

  /**
   * メイン初期化処理
   */
  initialize() {
    // 認証チェック後に実行
    const checkAuthAndLoad = () => {
      // URLパラメータ解析
      const grammarParam = this.parseGrammarParameter();
      
      if (grammarParam) {
        // 自動JSON読み込み
        this.autoLoadGrammar(grammarParam);
      } else {
        console.log('📄 手動JSON選択モード');
      }
    };

    // 認証システムの初期化を待つ
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        setTimeout(checkAuthAndLoad, 1000); // 認証システムの初期化を待つ
      });
    } else {
      setTimeout(checkAuthAndLoad, 1000);
    }
  }
}

// グローバルインスタンス
window.trainingAutoLoader = new TrainingAutoLoader();

// 初期化実行
window.trainingAutoLoader.initialize();
