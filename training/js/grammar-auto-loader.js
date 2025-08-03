/**
 * 文法項目自動選択システム - 動的説明ページロダー
 * 
 * 機能:
 * 1. URLパラメータから文法項目名を取得
 * 2. 文法項目名に基づく動的タイトル・コンテンツ生成
 * 3. トレーニングUIへの自動連携
 */

class GrammarAutoLoader {
  constructor() {
    this.grammarData = this.initializeGrammarData();
    this.currentGrammar = null;
  }

  /**
   * 文法項目データの初期化
   */
  initializeGrammarData() {
    return {
      "冠詞・定冠詞の付け方": {
        title: "冠詞・定冠詞の付け方",
        level: "レベル1（基本文型）",
        chunk: "名詞チャンク",
        jsonFile: "冠詞・定冠詞の付け方.json",
        content: {
          summary: "冠詞・定冠詞は日本人にとって最も理解・習得が難しい文法事項だと言われる。",
          sections: [
            {
              title: "（１）可算名詞と不可算名詞",
              content: "まず、定冠詞theや冠詞aをつけるべき名詞かどうかの識別（同様に複数形があるかどうかの識別）の前提としての、可算名詞と不可算名詞の定義について説明する。"
            }
          ]
        }
      },
      "V自動詞第1文型": {
        title: "V自動詞第1文型",
        level: "レベル1（基本文型）",
        chunk: "動詞チャンク",
        jsonFile: "V自動詞第1文型.json",
        content: {
          summary: "英語の基本5文型の中で最もシンプルな構造を持つ第1文型について学びます。",
          sections: [
            {
              title: "（１）第1文型の基本構造",
              content: "第1文型は「主語(S) + 動詞(V)」の最もシンプルな文型です。動詞は自動詞で、目的語を必要としません。"
            }
          ]
        }
      }
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
   * 文法項目データの取得
   */
  getGrammarData(grammarName) {
    return this.grammarData[grammarName] || null;
  }

  /**
   * 動的タイトル生成
   */
  updatePageTitle(grammarData) {
    if (!grammarData) return;
    
    // ページタイトル更新
    document.title = `${grammarData.title} - Rephrase 英語学習システム`;
    
    // ヘッダータイトル更新
    const headerTitle = document.querySelector('.page-header h1');
    if (headerTitle) {
      headerTitle.textContent = `📚 ${grammarData.title}`;
    }
    
    // サブタイトル更新
    const headerSubtitle = document.querySelector('.page-subtitle');
    if (headerSubtitle) {
      headerSubtitle.textContent = `${grammarData.chunk} - ${grammarData.level}`;
    }
  }

  /**
   * 動的コンテンツ生成
   */
  generateDynamicContent(grammarData) {
    if (!grammarData) {
      this.showGrammarNotFound();
      return;
    }

    const contentSection = document.querySelector('.content-section');
    if (!contentSection) return;

    // デフォルトコンテンツをクリア
    contentSection.innerHTML = '';

    // 動的コンテンツ生成
    const contentHTML = `
      <h2>${grammarData.title}</h2>
      
      <div class="key-point">
        <h4>要点解説</h4>
        <p>${grammarData.content.summary}</p>
      </div>

      ${grammarData.content.sections.map(section => `
        <h3>${section.title}</h3>
        <p>${section.content}</p>
      `).join('')}

      <div class="key-point">
        <h4>💡 学習のポイント</h4>
        <p>この文法項目を理解したら、実際のトレーニングで練習してみましょう。</p>
      </div>
    `;

    contentSection.innerHTML = contentHTML;
  }

  /**
   * 文法項目が見つからない場合の表示
   */
  showGrammarNotFound() {
    const contentSection = document.querySelector('.content-section');
    if (!contentSection) return;

    contentSection.innerHTML = `
      <h2>❌ 文法項目が見つかりません</h2>
      
      <div class="warning-box">
        <h4>お探しの文法項目は準備中です</h4>
        <p>申し訳ございませんが、お探しの文法項目の詳細説明は現在準備中です。</p>
        <p>他の文法項目から学習を開始するか、マトリクスページに戻って別の項目をお選びください。</p>
      </div>
    `;
  }

  /**
   * トレーニングUIボタンの更新
   */
  updateTrainingButton(grammarData) {
    const trainingButton = document.querySelector('.cta-section .btn-large');
    if (!trainingButton || !grammarData) return;

    // URLにgrammarパラメータを追加
    const trainingUrl = `../auth-check.html?grammar=${encodeURIComponent(grammarData.title)}`;
    trainingButton.href = trainingUrl;
    
    console.log(`🎯 トレーニングURL設定: ${trainingUrl}`);
  }

  /**
   * 成功メッセージ表示
   */
  showAutoLoadSuccess(grammarName) {
    console.log(`✅ ${grammarName} の詳細説明を読み込みました`);
    
    // 必要に応じてユーザーに通知
    const notification = document.createElement('div');
    notification.className = 'auto-load-notification';
    notification.innerHTML = `
      <div style="background: #e8f5e8; border: 1px solid #4CAF50; padding: 10px; margin: 10px 0; border-radius: 5px;">
        ✅ ${grammarName} の詳細説明を読み込みました
      </div>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
      container.insertBefore(notification, container.firstChild);
      
      // 3秒後に通知を削除
      setTimeout(() => {
        notification.remove();
      }, 3000);
    }
  }

  /**
   * メイン初期化処理
   */
  initialize() {
    // URLパラメータ解析
    const grammarParam = this.parseGrammarParameter();
    
    if (grammarParam) {
      // 文法項目データ取得
      const grammarData = this.getGrammarData(grammarParam);
      
      if (grammarData) {
        this.currentGrammar = grammarData;
        
        // 動的コンテンツ生成
        this.updatePageTitle(grammarData);
        this.generateDynamicContent(grammarData);
        this.updateTrainingButton(grammarData);
        this.showAutoLoadSuccess(grammarParam);
      } else {
        console.warn(`⚠️ 文法項目データが見つかりません: ${grammarParam}`);
        this.showGrammarNotFound();
      }
    } else {
      // パラメータがない場合はデフォルト表示（既存の静的コンテンツを維持）
      console.log('📄 静的コンテンツ表示モード');
    }
  }
}

// グローバルインスタンス
window.grammarAutoLoader = new GrammarAutoLoader();

// DOM読み込み完了時に初期化
document.addEventListener('DOMContentLoaded', function() {
  window.grammarAutoLoader.initialize();
});
