/**
 * 🚀 Rephrase モバイル専用音声システム v1.0
 * 段階的実装アプローチ - フェーズ1: 音声認識のみ
 * 
 * 実装戦略:
 * ✅ フェーズ1: testVoiceRecognition機能のみ（動作確認済み）
 * 🔄 フェーズ2: 録音機能追加（段階的テスト）
 * 🔄 フェーズ3: 音声再生機能（段階的テスト）
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
    
    /**
     * デバッグパネル初期化
     */
    initializeDebugPanel() {
        const debugPanel = document.getElementById('voice-debug-panel');
        if (!debugPanel) {
            console.log('⚠️ デバッグパネルが見つかりません');
            return;
        }
        
        // フェーズ1専用のシンプルなUI
        debugPanel.innerHTML = `
            <div class="debug-header">
                <h3>🎤 モバイル音声認識テスト (フェーズ1)</h3>
                <p>動作確認済みの音声認識機能のみ</p>
            </div>
            
            <div class="test-controls">
                <button id="mobile-voice-test-btn" class="voice-test-btn">
                    🎤 音声認識テスト
                </button>
            </div>
            
            <div class="voice-result-area">
                <h4>🎯 認識結果:</h4>
                <div id="mobile-voice-result" class="voice-result-text">
                    まだ認識されていません
                </div>
            </div>
            
            <div class="debug-log-area">
                <h4>📋 デバッグログ:</h4>
                <div id="mobile-debug-log" class="debug-log-content">
                    🔄 システム初期化中...
                </div>
            </div>
        `;
        
        // イベントリスナー設定
        const testBtn = document.getElementById('mobile-voice-test-btn');
        if (testBtn) {
            testBtn.addEventListener('click', () => {
                this.addDebugLog('🔘 音声認識テストボタンがタップされました', 'info');
                this.startVoiceRecognition();
            });
        }
        
        this.addDebugLog('✅ モバイル専用デバッグパネル初期化完了', 'success');
        
        // 🚨 修正: JSONデータロード完了を待つ
        this.waitForSystemReady();
    }
    
    /**
     * システム準備完了を待機
     */
    waitForSystemReady() {
        // slotDataが読み込まれるまで待機
        const checkReady = () => {
            if (window.slotData && Object.keys(window.slotData).length > 0) {
                this.addDebugLog('✅ JSONデータ読み込み完了 - システム準備完了', 'success');
                console.log('📱 モバイル音声システム: 完全初期化完了');
            } else {
                this.addDebugLog('⏳ JSONデータ読み込み待機中...', 'info');
                setTimeout(checkReady, 500); // 0.5秒後に再チェック
            }
        };
        
        // 初回チェック
        setTimeout(checkReady, 100);
    }
    
    /**
     * フェーズ1: 音声認識機能（testVoiceRecognition完全移植版）
     * 🚨 重要: この機能はAndroid Chromeで動作確認済み
     */
    startVoiceRecognition() {
        this.addDebugLog('🗣️ 音声認識テストを開始します...', 'info');
        
        // 認識テスト開始時にthis.recognizedTextをクリア
        this.recognizedText = '';
        this.addDebugLog('🗑️ recognizedTextをクリアしました', 'info');
        
        // Web Speech API対応チェック
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ Web Speech API が利用できません', 'error');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // Android Chrome最適化設定（動作確認済み設定）
        if (this.isAndroid) {
            this.addDebugLog('📱 Android Chrome用設定を適用', 'info');
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-US'; // 英語設定
            recognition.maxAlternatives = 3; // 複数候補
        } else {
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'ja-JP';
            recognition.maxAlternatives = 1;
        }
        
        this.addDebugLog(`🔍 認識設定: lang=${recognition.lang}, continuous=${recognition.continuous}`, 'info');
        
        // タイムアウト設定（Android用は少し長め）
        const timeoutDuration = this.isAndroid ? 15000 : 10000;
        let timeoutId = setTimeout(() => {
            recognition.stop();
            this.addDebugLog(`⏰ 音声認識がタイムアウトしました（${timeoutDuration/1000}秒）`, 'warning');
        }, timeoutDuration);
        
        // イベントハンドラー設定（動作確認済み設定を完全移植）
        recognition.onstart = () => {
            this.addDebugLog('✅ 音声認識start()コマンド送信完了', 'success');
            this.addDebugLog('🎤 音声認識開始イベント発生', 'success');
            
            const duration = this.isAndroid ? '15秒' : '10秒';
            this.addDebugLog(`🎤 何か話してください（${duration}以内）...`, 'info');
        };
        
        recognition.onresult = (event) => {
            clearTimeout(timeoutId);
            
            this.addDebugLog('🎯 音声認識結果イベント発生', 'info');
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence || 0;
                
                if (result.isFinal) {
                    this.recognizedText = transcript;
                    this.addDebugLog(`✅ 認識結果（確定）: "${transcript}"`, 'success');
                    this.addDebugLog(`📊 信頼度: ${(confidence * 100).toFixed(1)}%`, 'info');
                    this.addDebugLog(`💾 recognizedText保存: "${this.recognizedText}"`, 'success');
                    
                    // UI更新
                    this.updateVoiceResult(transcript, true);
                } else {
                    this.addDebugLog(`🔄 認識結果（途中）: "${transcript}"`, 'info');
                    
                    // Android Chrome: 中間結果も重要
                    if (this.isAndroid) {
                        this.addDebugLog('📱 Android: 中間結果を記録', 'info');
                        if (!this.recognizedText || this.recognizedText.trim().length === 0) {
                            this.recognizedText = transcript;
                            this.addDebugLog(`💾 Android中間結果保存: "${this.recognizedText}"`, 'info');
                        }
                        
                        // 中間結果もUI表示
                        this.updateVoiceResult(transcript, false);
                    }
                }
            }
        };
        
        recognition.onend = () => {
            clearTimeout(timeoutId);
            this.addDebugLog('🔚 音声認識終了イベント発生', 'info');
            
            if (this.isAndroid) {
                this.addDebugLog('📱 Android: 認識終了時の特別チェック', 'info');
            }
            
            this.addDebugLog('🔚 音声認識終了処理完了', 'info');
        };
        
        recognition.onerror = (event) => {
            clearTimeout(timeoutId);
            this.addDebugLog(`❌ 音声認識エラー: ${event.error}`, 'error');
            
            if (this.isAndroid) {
                this.addDebugLog('📱 Android: エラー詳細分析', 'warning');
            }
            
            switch (event.error) {
                case 'no-speech':
                    this.addDebugLog('🔇 音声が検出されませんでした', 'warning');
                    break;
                case 'audio-capture':
                    this.addDebugLog('🎤 マイクからの音声キャプチャに失敗', 'error');
                    break;
                case 'not-allowed':
                    this.addDebugLog('🚫 マイク権限が拒否されています', 'error');
                    break;
                case 'network':
                    this.addDebugLog('🌐 ネットワークエラーが発生しました', 'error');
                    break;
            }
        };
        
        // 音声認識開始
        try {
            recognition.start();
            this.addDebugLog('🚀 音声認識開始実行', 'info');
        } catch (error) {
            this.addDebugLog(`❌ 音声認識開始失敗: ${error.message}`, 'error');
        }
    }
    
    /**
     * 音声結果UI更新
     */
    updateVoiceResult(text, isFinal) {
        const resultDiv = document.getElementById('mobile-voice-result');
        if (resultDiv) {
            const prefix = isFinal ? '✅ 確定: ' : '🔄 途中: ';
            resultDiv.textContent = prefix + text;
            resultDiv.className = isFinal ? 'voice-result-text final' : 'voice-result-text interim';
        }
    }
    
    /**
     * デバッグログ追加
     */
    addDebugLog(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = `[${timestamp}] ${message}`;
        
        this.debugMessages.push({ message: logEntry, type });
        console.log(logEntry);
        
        // UI更新
        const logDiv = document.getElementById('mobile-debug-log');
        if (logDiv) {
            const logElement = document.createElement('div');
            logElement.className = `debug-log-item ${type}`;
            logElement.textContent = logEntry;
            
            logDiv.appendChild(logElement);
            logDiv.scrollTop = logDiv.scrollHeight;
            
            // ログが多すぎる場合は古いものを削除
            const logItems = logDiv.children;
            if (logItems.length > 20) {
                logDiv.removeChild(logItems[0]);
            }
        }
    }
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
    } else {
        console.log('💻 デスクトップデバイスのため、MobileVoiceSystemは初期化されません');
    }
});
