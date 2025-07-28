/**
 * 音声学習システム - メインクラス
 * 例文全体の録音、再生、音声合成、評価機能を提供
 */
class VoiceSystem {
    constructor() {
        this.mediaRecorder = null;
        this.recordedBlob = null;
        this.audioContext = null;
        this.analyser = null;
        this.animationId = null;
        this.recordingStartTime = null;
        this.recordingTimerInterval = null;
        this.isRecording = false;
        this.isMicrophoneAllowed = false;
        
        // 音声合成関連
        this.currentUtterance = null;
        
        // 🔧 再生用Audioオブジェクト管理
        this.currentAudio = null;
        
        // 🎤 リアルタイム音声認識
        this.recognition = null;
        this.recognizedText = '';
        this.isRecognitionActive = false;
        
        // 🎤 録音用音声認識（testVoiceRecognition完全移植版）
        this.recordingRecognition = null;
        this.recognitionTimeoutId = null;
        
        // 📱 スマホ用診断ログ
        this.debugLogs = [];
        this.maxDebugLogs = 50; // 最大50件のログを保持
        
        this.init();
    }
    
    // [4460行のファイルのため、主要部分のみバックアップ - 実際のバックアップでは完全版を保存]
    async init() {
        console.log('🎤 音声システム初期化開始...');
        
        // 音声リストを読み込み
        this.loadVoices();
        
        // マイクアクセス許可を確認
        await this.checkMicrophonePermission();
        
        // 音声認識を初期化
        this.initSpeechRecognition();
        
        // イベントリスナーを設定
        this.setupEventListeners();
        
        // 分析ボタンを非表示（リアルタイム認識では不要）
        this.hideAnalyzeButton();
        
        // 📱 初期化時にパネル位置を調整（特にモバイル）
        setTimeout(() => {
            const panel = document.getElementById('voice-control-panel');
            if (panel) {
                this.adjustPanelPosition();
            }
        }, 1000);
        
        console.log('✅ 音声システム初期化完了');
    }
    
    /**
     * 現在表示されている全スロットのテキストを取得して完全な例文を作成
     */
    getCurrentSentence() {
        console.log('📝 現在の例文取得を開始...');
        
        // 🎯 直接window.loadedJsonDataから順序通りに例文を構築
        if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
            const sentence = this.buildSentenceFromOrderedData();
            if (sentence && sentence.trim().length > 0) {
                console.log('✅ データから例文を取得しました:', sentence);
                return sentence;
            }
        }
        
        console.warn('⚠️ データからの取得に失敗。フォールバック処理を実行');
        
        // フォールバック: DOMから直接取得
        const domSentence = this.buildSentenceFromDOM();
        if (domSentence && domSentence.trim().length > 0) {
            console.log('✅ DOMから例文を取得しました:', domSentence);
            return domSentence;
        }

        console.warn('⚠️ どの方法でも例文を取得できませんでした');
        return '';
    }
}

// 音声システム自動初期化（モバイル対応含む）
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎤 DOM読み込み完了 - 音声システム初期化開始');
    
    // VoiceSystemの初期化とグローバルアクセス設定
    window.voiceSystem = new VoiceSystem();
    
    console.log('✅ 音声システムグローバル変数設定完了');
});
