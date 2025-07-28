/**
 * 🚀 Rephrase モバイル専用音声システム v1.1 - 再生機能付き
 * 段階的実装アプローチ
 * 
 * 実装戦略:
 * ✅ フェーズ1: testVoiceRecognition機能のみ（動作確認済み）
 * ✅ フェーズ2: 録音機能追加（段階的テスト）
 * 🚀 フェーズ3: 音声再生機能（Android Chrome対応）
 * 🔄 フェーズ4: 統合テスト
 */

class MobileVoiceSystem {
    constructor() {
        console.log('🚀 MobileVoiceSystem初期化開始');
        
        // モバイル検出
        this.isMobile = this.detectMobileDevice();
        this.isAndroid = /Android/i.test(navigator.userAgent);
        
        // 基本プロパティ
        this.recognizedText = '';
        this.debugMessages = [];
        
        // 🚀 フェーズ2: 録音関連プロパティ
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        
        // 🚀 フェーズ3: 再生関連プロパティ
        this.recordedAudio = null;
        this.audioContext = null;
        this.isPlaying = false;
        
        console.log('📱 モバイル検出結果:', {
            isMobile: this.isMobile,
            isAndroid: this.isAndroid,
            userAgent: navigator.userAgent
        });
        
        if (!this.isMobile) {
            console.log('⚠️ デスクトップデバイスが検出されました。このシステムはモバイル専用です。');
            return;
        }
        
        this.initializeDebugPanel();
        console.log('✅ MobileVoiceSystem初期化完了');
    }
    
    /**
     * モバイルデバイス検出
     */
    detectMobileDevice() {
        const userAgent = navigator.userAgent;
        const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
        const isTouchDevice = 'ontouchstart' in window;
        const isSmallScreen = window.innerWidth <= 768;
        
        return isMobileUA || isTouchDevice || isSmallScreen;
    }
    
    // [その他のメソッドは元ファイルと同じ...]
}

// グローバル変数として初期化
let mobileVoiceSystem = null;

// DOM読み込み完了後に初期化
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 MobileVoiceSystem DOM読み込み完了');
    
    // モバイルデバイスの場合のみ初期化
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                    'ontouchstart' in window ||
                    window.innerWidth <= 768;
    
    if (isMobile) {
        mobileVoiceSystem = new MobileVoiceSystem();
        console.log('✅ MobileVoiceSystem初期化完了');
        
        // グローバルアクセス用
        window.MobileVoiceSystem = mobileVoiceSystem;
    } else {
        console.log('💻 デスクトップデバイスのため、MobileVoiceSystemは初期化されません');
    }
});
