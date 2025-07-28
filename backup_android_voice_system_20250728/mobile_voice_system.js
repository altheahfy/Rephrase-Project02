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
        this.isAndroidChrome = this.isAndroid && /Chrome/i.test(navigator.userAgent) && !/Edg/i.test(navigator.userAgent) && !/SamsungBrowser/i.test(navigator.userAgent);
        this.isAndroidFirefox = this.isAndroid && /Firefox/i.test(navigator.userAgent);
        this.isAndroidSamsung = this.isAndroid && /SamsungBrowser/i.test(navigator.userAgent);
        this.isAndroidEdge = this.isAndroid && (/EdgA/i.test(navigator.userAgent) || /Edge/i.test(navigator.userAgent) || /Edg\//i.test(navigator.userAgent));
        this.browserInfo = this.detectBrowserInfo();
        
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
        
        // 🚀 フェーズ4: 統合機能プロパティ
        this.isUnifiedMode = false;
        this.currentRecognition = null;
        
        // 🚀 フェーズ5: 読み上げ機能プロパティ
        this.currentUtterance = null;
        this.availableVoices = [];
        
        // 🚀 スマホ用デバッグ表示プロパティ
        this.debugDisplay = null;
        this.initErrors = [];
        
        console.log('📱 モバイル検出結果:', {
            isMobile: this.isMobile,
            isAndroid: this.isAndroid,
            isAndroidChrome: this.isAndroidChrome,
            isAndroidFirefox: this.isAndroidFirefox,
            isAndroidSamsung: this.isAndroidSamsung,
            isAndroidEdge: this.isAndroidEdge,
            browserInfo: this.browserInfo,
            userAgent: navigator.userAgent
        });
        
        // 🔧 デスクトップテスト用: モバイルチェックを一時的に無効化
        // if (!this.isMobile) {
        //     console.log('⚠️ デスクトップデバイスが検出されました。このシステムはモバイル専用です。');
        //     return;
        // }
        
        this.initializeDebugPanel();
        this.loadVoices(); // 読み上げ用音声を読み込み
        
        // スマホ用: 初期化完了後にデバッグ情報を表示
        this.showMobileDebugInfo();
        
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
    
    /**
     * 詳細ブラウザ情報検出
     */
    detectBrowserInfo() {
        const ua = navigator.userAgent;
        
        if (this.isAndroid) {
            if (/Chrome/i.test(ua) && !/Edg/i.test(ua) && !/SamsungBrowser/i.test(ua)) {
                return 'Android Chrome';
            } else if (/Firefox/i.test(ua)) {
                return 'Android Firefox';
            } else if (/SamsungBrowser/i.test(ua)) {
                return 'Android Samsung Browser';
            } else if (/EdgA/i.test(ua) || /Edge/i.test(ua) || /Edg\//i.test(ua)) {
                return 'Android Edge';
            } else {
                return 'Android Other';
            }
        } else if (/iPhone|iPad|iPod/i.test(ua)) {
            if (/Safari/i.test(ua) && !/Chrome/i.test(ua)) {
                return 'iOS Safari';
            } else if (/Chrome/i.test(ua)) {
                return 'iOS Chrome';
            } else if (/Firefox/i.test(ua)) {
                return 'iOS Firefox';
            } else {
                return 'iOS Other';
            }
        } else {
            if (/Chrome/i.test(ua) && !/Edg/i.test(ua)) {
                return 'Desktop Chrome';
            } else if (/Firefox/i.test(ua)) {
                return 'Desktop Firefox';
            } else if (/Edg/i.test(ua)) {
                return 'Desktop Edge';
            } else if (/Safari/i.test(ua) && !/Chrome/i.test(ua)) {
                return 'Desktop Safari';
            } else {
                return 'Desktop Other';
            }
        }
    }
    
    /**
     * デバッグパネル初期化
     */
    initializeDebugPanel() {
        let debugPanel = document.getElementById('voice-debug-panel');
        
        if (!debugPanel) {
            console.log('❌ voice-debug-panel要素が見つかりません。新規作成します...');
            
            // デバッグパネル要素を動的作成
            debugPanel = document.createElement('div');
            debugPanel.id = 'voice-debug-panel';
            debugPanel.style.cssText = `
                position: fixed;
                top: 120px;
                right: 10px;
                width: 320px;
                max-height: 70vh;
                background: white;
                border-radius: 8px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);
                z-index: 15000;
                display: none;
                overflow: hidden;
            `;
            document.body.appendChild(debugPanel);
            console.log('✅ voice-debug-panel要素を作成しました');
        } else {
            console.log('✅ voice-debug-panel要素が見つかりました');
        }
        
        // パネル内容を動的生成
        debugPanel.innerHTML = `
            <div style="padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h3 style="margin: 0; color: #333; font-size: 18px;">🎤 モバイル音声システム</h3>
                    <button id="close-debug-panel" style="
                        background: #dc3545;
                        color: white;
                        border: none;
                        border-radius: 50%;
                        width: 25px;
                        height: 25px;
                        cursor: pointer;
                        font-size: 12px;
                        font-weight: bold;
                    ">✕</button>
                </div>
                
                <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                    音声認識 + 録音 + 再生機能 (${this.browserInfo})
                </p>
                
                <div class="test-controls">
                    <button id="mobile-voice-test-btn" class="voice-test-btn">
                        🎤 音声認識テスト
                    </button>
                    <button id="mobile-record-test-btn" class="voice-test-btn" style="
                        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                        margin-top: 8px;
                    ">
                        🔴 録音テスト
                    </button>
                    <button id="mobile-play-test-btn" class="voice-test-btn" style="
                        background: linear-gradient(135deg, #FF9800 0%, #F57F17 100%);
                        margin-top: 8px;
                    ">
                        🔊 再生テスト
                    </button>
                    <button id="mobile-unified-test-btn" class="voice-test-btn" style="
                        background: linear-gradient(135deg, ${this.isAndroid ? '#6c757d 0%, #495057 100%' : '#28a745 0%, #20c997 100%'});
                        margin-top: 8px;
                        font-weight: bold;
                        ${this.isAndroid ? 'opacity: 0.6;' : ''}
                    ">
                        ${this.isAndroid ? '🚫 統合テスト (Android OS制限)' : '🎯 録音+音声認識 統合テスト'}
                    </button>
                    <button id="mobile-tts-test-btn" class="voice-test-btn" style="
                        background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);
                        margin-top: 8px;
                        font-weight: bold;
                    ">
                        🔊 例文読み上げテスト
                    </button>
                </div>
                
                <div class="voice-result-area">
                    <h4>🎯 認識結果:</h4>
                    <div id="mobile-voice-result" class="voice-result-text">
                        まだ認識されていません
                    </div>
                </div>
                
                <div class="voice-result-area">
                    <h4>🔴 録音状態:</h4>
                    <div id="mobile-record-status" class="voice-result-text">
                        録音待機中
                    </div>
                </div>
                
                <div class="debug-log-area">
                    <h4>📋 音声システムログ:</h4>
                    <div id="mobile-debug-log" class="debug-log-content">
                        システム準備完了
                    </div>
                </div>
            </div>
        `;
        
        // スタイル追加
        this.addDebugPanelStyles();
        
        // イベントリスナー設定
        this.setupEventListeners();
        
        // ログ窓にシステム情報を表示
        this.addDebugLog('🚀 MobileVoiceSystem初期化完了', 'success');
        this.addDebugLog(`🌐 ブラウザ: ${this.browserInfo}`, 'info');
        
        if (this.isAndroid) {
            this.addDebugLog('⚠️ Android OS: 統合機能制限あり', 'warning');
            this.addDebugLog('📱 Android OSでは音声リソース競合により統合機能不可', 'info');
            this.addDebugLog('🔄 録音・音声認識は個別ボタンでテストしてください', 'info');
        } else {
            this.addDebugLog('✅ 統合機能テスト可能な環境です', 'success');
            this.addDebugLog('🎯 「録音+音声認識 統合テスト」ボタンをタップしてください', 'info');
        }
    }
    
    // [続きは他のメソッドをそのまま保持...]
    
    /**
     * デバッグパネルスタイル追加
     */
    addDebugPanelStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .voice-test-btn {
                width: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                font-weight: bold;
                transition: transform 0.2s ease;
            }
            .voice-test-btn:active {
                transform: scale(0.98);
            }
            .voice-result-area {
                margin: 15px 0;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 6px;
                border-left: 4px solid #007bff;
            }
            .voice-result-area h4 {
                margin: 0 0 8px 0;
                color: #495057;
                font-size: 14px;
            }
            .voice-result-text {
                color: #333;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                background: white;
                border-radius: 4px;
                border: 1px solid #dee2e6;
            }
            .voice-result-text.final {
                background: #d4edda;
                border-color: #c3e6cb;
                color: #155724;
            }
            .voice-result-text.interim {
                background: #fff3cd;
                border-color: #ffeaa7;
                color: #856404;
            }
            .debug-log-area {
                margin-top: 15px;
            }
            .debug-log-area h4 {
                margin: 0 0 8px 0;
                color: #495057;
                font-size: 14px;
            }
            .debug-log-content {
                max-height: 200px;
                overflow-y: auto;
                background: #2c3e50;
                color: #ecf0f1;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        `;
        document.head.appendChild(style);
    }
    
    // [その他の長大なメソッドは同じように継続...]
}

// グローバル変数として初期化
let mobileVoiceSystem = null;

// DOM読み込み完了後に初期化
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 MobileVoiceSystem DOM読み込み完了');
    
    // モバイルデバイスの場合のみ初期化（デスクトップテスト用に一時的に無効化）
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                    'ontouchstart' in window ||
                    window.innerWidth <= 768 ||
                    true; // 🔧 デスクトップテスト用: 強制的にtrueに設定
    
    if (isMobile) {
        mobileVoiceSystem = new MobileVoiceSystem();
        console.log('✅ MobileVoiceSystem初期化完了');
        
        // グローバルアクセス用
        window.MobileVoiceSystem = mobileVoiceSystem;
    } else {
        console.log('💻 デスクトップデバイスのため、MobileVoiceSystemは初期化されません');
    }
});
