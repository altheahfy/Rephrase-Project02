/**
 * 音声学習進捗表示UI
 * 学習者の上達度を視覚的に表示する
 */
class VoiceProgressUI {
    constructor() {
        this.progressTracker = window.voiceProgressTracker;
        this.isVisible = false;
        this.currentPeriod = 'week';
        
        // グローバルインスタンスとして登録
        window.currentProgressUI = this;
        
        // 初期化のタイミングをずらす
        if (this.progressTracker) {
            this.init();
        } else {
            // ProgressTrackerが読み込まれるまで待つ
            setTimeout(() => {
                this.progressTracker = window.voiceProgressTracker;
                if (this.progressTracker) {
                    this.init();
                } else {
                    console.error('❌ VoiceProgressTrackerが見つかりません');
                }
            }, 1000);
        }
    }
    
    /**
     * 初期化
     */
    init() {
        this.createProgressPanel();
        this.setupEventListeners();
        console.log('✅ 音声進捗表示UI初期化完了');
    }
    
    /**
     * 進捗パネルを作成
     */
    createProgressPanel() {
        // 既存のパネルがあれば削除
        const existingPanel = document.getElementById('voice-progress-panel');
        if (existingPanel) {
            existingPanel.remove();
        }
        
        const panel = document.createElement('div');
        panel.id = 'voice-progress-panel';
        panel.className = 'voice-progress-panel';
        panel.style.display = 'none';
        
        // [669行のファイルのため詳細は省略 - 完全なパネルHTML]
        
        document.body.appendChild(panel);
        
        // CSS スタイルを追加
        this.addProgressPanelStyles();
    }
    
    // [その他のメソッドはファイルの長さのため省略 - 実際のバックアップでは完全版を保存]
}

// グローバル初期化
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        if (window.voiceProgressTracker) {
            window.voiceProgressUI = new VoiceProgressUI();
        }
    }, 2000);
});
