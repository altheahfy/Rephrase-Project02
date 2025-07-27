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
    
    /**
     * デバッグパネル初期化
     */
    initializeDebugPanel() {
        const debugPanel = document.getElementById('voice-debug-panel');
        if (!debugPanel) {
            console.log('❌ voice-debug-panel要素が見つかりません');
            return;
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
                    音声認識 + 録音 + 再生機能
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
    }
    
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
    
    /**
     * イベントリスナー設定
     */
    setupEventListeners() {
        // 閉じるボタン
        const closeBtn = document.getElementById('close-debug-panel');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                const panel = document.getElementById('voice-debug-panel');
                if (panel) {
                    panel.style.display = 'none';
                }
            });
        }
        
        // 🚀 フェーズ1: 音声認識テストボタンのイベントリスナー
        const voiceTestBtn = document.getElementById('mobile-voice-test-btn');
        if (voiceTestBtn) {
            voiceTestBtn.addEventListener('click', () => {
                this.addDebugLog('🎤 音声認識テストボタンがタップされました', 'info');
                this.startVoiceRecognitionTest();
            });
        }
        
        // 🚀 フェーズ2: 録音テストボタンのイベントリスナー
        const recordTestBtn = document.getElementById('mobile-record-test-btn');
        if (recordTestBtn) {
            recordTestBtn.addEventListener('click', () => {
                this.addDebugLog('🔴 録音テストボタンがタップされました', 'info');
                this.startRecordingTest();
            });
        }
        
        // 🚀 フェーズ3: 再生テストボタンのイベントリスナー
        const playTestBtn = document.getElementById('mobile-play-test-btn');
        if (playTestBtn) {
            playTestBtn.addEventListener('click', () => {
                this.addDebugLog('🔊 再生テストボタンがタップされました', 'info');
                this.startPlaybackTest();
            });
        }
    }
    
    /**
     * 🚀 フェーズ1: 音声認識テスト（動作確認済みロジック完全移植）
     */
    startVoiceRecognitionTest() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ 音声認識APIが利用できません', 'error');
            return;
        }
        
        this.addDebugLog('🚀 音声認識テスト開始', 'info');
        
        // SpeechRecognition設定（動作確認済み設定を完全移植）
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // Android Chrome最適化設定
        recognition.continuous = this.isAndroid ? true : false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        recognition.lang = 'en-US';
        
        this.addDebugLog('⚙️ 音声認識設定完了', 'info');
        this.addDebugLog(`📱 Android最適化: continuous=${recognition.continuous}`, 'info');
        
        // タイムアウト設定
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
                    }
                    
                    // UI更新
                    this.updateVoiceResult(transcript, false);
                }
            }
        };
        
        recognition.onend = () => {
            clearTimeout(timeoutId);
            this.addDebugLog('🔚 音声認識終了イベント発生', 'info');
            
            if (this.recognizedText && this.recognizedText.trim().length > 0) {
                this.addDebugLog(`✅ 最終認識結果: "${this.recognizedText}"`, 'success');
            } else {
                this.addDebugLog('⚠️ 有効な音声認識結果がありません', 'warning');
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
     * 🚀 フェーズ2: シンプルな録音テスト機能
     */
    async startRecordingTest() {
        if (this.isRecording) {
            this.stopRecording();
            return;
        }
        
        this.addDebugLog('🎤 マイクアクセス許可を要求中...', 'info');
        this.updateRecordStatus('🎤 マイクアクセス許可を要求中...');
        
        try {
            // マイクアクセス許可
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } 
            });
            
            this.addDebugLog('✅ マイクアクセス許可取得完了', 'success');
            
            // Android Chrome対応のmimeType設定
            const mimeTypes = [
                'audio/webm;codecs=opus',
                'audio/webm',
                'audio/mp4',
                'audio/mpeg',
                ''  // フォールバック
            ];
            
            let selectedMimeType = '';
            for (const mimeType of mimeTypes) {
                if (MediaRecorder.isTypeSupported(mimeType)) {
                    selectedMimeType = mimeType;
                    this.addDebugLog(`📋 対応mimeType: ${mimeType || 'デフォルト'}`, 'info');
                    break;
                }
            }
            
            // MediaRecorder初期化
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: selectedMimeType
            });
            
            this.audioChunks = [];
            
            // イベントハンドラー設定
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                    this.addDebugLog(`📊 音声データ受信: ${event.data.size}バイト`, 'info');
                }
            };
            
            this.mediaRecorder.onstop = () => {
                this.addDebugLog('🛑 録音停止完了', 'success');
                this.updateRecordStatus('✅ 録音完了');
                
                // 録音データ処理
                if (this.audioChunks.length > 0) {
                    const audioBlob = new Blob(this.audioChunks, { 
                        type: selectedMimeType || 'audio/webm' 
                    });
                    this.addDebugLog(`🎵 録音ファイル作成: ${audioBlob.size}バイト`, 'success');
                    
                    // 🚀 フェーズ3: 録音データを保存（再生用）
                    this.recordedAudio = audioBlob;
                    this.addDebugLog('💾 録音データ保存完了（再生準備OK）', 'success');
                } else {
                    this.addDebugLog('⚠️ 録音データが空です', 'warning');
                }
                
                // ストリーム停止
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.onerror = (event) => {
                this.addDebugLog(`❌ 録音エラー: ${event.error}`, 'error');
                this.updateRecordStatus('❌ 録音エラー');
            };
            
            // 録音開始
            this.isRecording = true;
            this.mediaRecorder.start();
            this.addDebugLog('🔴 録音開始', 'success');
            this.updateRecordStatus('🔴 録音中... (再度タップで停止)');
            
        } catch (error) {
            this.addDebugLog(`❌ 録音開始エラー: ${error.message}`, 'error');
            this.updateRecordStatus('❌ 録音開始失敗');
        }
    }
    
    /**
     * 録音停止
     */
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.addDebugLog('🛑 録音停止要求送信', 'info');
            this.updateRecordStatus('🛑 録音停止処理中...');
        }
    }
    
    /**
     * 🚀 フェーズ3: Android Chrome対応 再生テスト機能
     */
    async startPlaybackTest() {
        if (!this.recordedAudio) {
            this.addDebugLog('❌ 再生する録音データがありません（先に録音してください）', 'error');
            return;
        }
        
        if (this.isPlaying) {
            this.addDebugLog('⚠️ 既に再生中です', 'warning');
            return;
        }
        
        this.addDebugLog('🔊 Android Chrome対応再生機能を開始します', 'info');
        
        // 方法1: Web Audio API を使用（Android Chrome推奨）
        await this.playWithWebAudioAPI();
    }
    
    /**
     * 方法1: Web Audio API を使用した再生（Android Chrome対応）
     */
    async playWithWebAudioAPI() {
        try {
            this.addDebugLog('🎵 Web Audio API再生を開始', 'info');
            
            // AudioContext初期化
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            // ユーザーインタラクション後にコンテキストを再開
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
                this.addDebugLog('🔧 AudioContext resumed', 'info');
            }
            
            // Blob to ArrayBuffer
            const arrayBuffer = await this.recordedAudio.arrayBuffer();
            this.addDebugLog(`📊 ArrayBuffer作成: ${arrayBuffer.byteLength}バイト`, 'info');
            
            // AudioBuffer作成
            const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
            this.addDebugLog(`🎼 AudioBuffer作成: ${audioBuffer.duration.toFixed(2)}秒`, 'success');
            
            // AudioBufferSourceNode作成
            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioContext.destination);
            
            // 再生開始
            this.isPlaying = true;
            source.start();
            this.addDebugLog('✅ Web Audio API再生開始', 'success');
            
            // 再生終了の監視
            source.onended = () => {
                this.isPlaying = false;
                this.addDebugLog('🔚 Web Audio API再生完了', 'success');
            };
            
        } catch (error) {
            this.addDebugLog(`❌ Web Audio API再生エラー: ${error.message}`, 'error');
            this.isPlaying = false;
            
            // HTML5 Audioで再試行
            this.addDebugLog('🔄 HTML5 Audioで再試行します', 'info');
            this.playWithHTML5Audio();
        }
    }
    
    /**
     * 方法2: 標準HTML5 Audio要素での再生
     */
    playWithHTML5Audio() {
        try {
            this.addDebugLog('🎵 HTML5 Audio再生を開始', 'info');
            
            // Blob URL作成
            const audioUrl = URL.createObjectURL(this.recordedAudio);
            this.addDebugLog(`🔗 Blob URL作成: ${audioUrl}`, 'info');
            
            // Audio要素作成
            const audio = new Audio(audioUrl);
            
            // イベントハンドラー設定
            audio.oncanplay = () => {
                this.addDebugLog('✅ HTML5 Audio再生可能', 'success');
                this.isPlaying = true;
                audio.play().catch(err => {
                    this.addDebugLog(`❌ HTML5 Audio再生失敗: ${err.message}`, 'error');
                    this.isPlaying = false;
                    this.createDownloadLink();
                });
            };
            
            audio.onended = () => {
                this.isPlaying = false;
                this.addDebugLog('🔚 HTML5 Audio再生完了', 'success');
                URL.revokeObjectURL(audioUrl);
            };
            
            audio.onerror = () => {
                this.addDebugLog('❌ HTML5 Audioエラー', 'error');
                this.isPlaying = false;
                URL.revokeObjectURL(audioUrl);
                this.createDownloadLink();
            };
            
            // 読み込み開始
            audio.load();
            
        } catch (error) {
            this.addDebugLog(`❌ HTML5 Audio再生エラー: ${error.message}`, 'error');
            this.isPlaying = false;
            this.createDownloadLink();
        }
    }
    
    /**
     * 方法3: ダウンロードリンク生成（最終手段）
     */
    createDownloadLink() {
        try {
            this.addDebugLog('💾 ダウンロードリンクを生成します', 'info');
            
            const audioUrl = URL.createObjectURL(this.recordedAudio);
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const filename = `rephrase_recording_${timestamp}.webm`;
            
            // ダウンロードリンク作成
            const downloadLink = document.createElement('a');
            downloadLink.href = audioUrl;
            downloadLink.download = filename;
            downloadLink.textContent = `📥 録音ファイルをダウンロード`;
            downloadLink.style.cssText = `
                display: block;
                background: #007bff;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-decoration: none;
                margin: 10px 0;
                text-align: center;
            `;
            
            // デバッグパネルに追加
            const debugPanel = document.getElementById('voice-debug-panel');
            if (debugPanel) {
                debugPanel.appendChild(downloadLink);
                this.addDebugLog('✅ ダウンロードリンクを作成しました', 'success');
            }
            
        } catch (error) {
            this.addDebugLog(`❌ ダウンロードリンク作成エラー: ${error.message}`, 'error');
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
     * 録音状態表示更新
     */
    updateRecordStatus(message) {
        const statusDiv = document.getElementById('mobile-record-status');
        if (statusDiv) {
            statusDiv.textContent = message;
        }
    }
    
    /**
     * デバッグログ追加
     */
    addDebugLog(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logMessage = `[${timestamp}] ${message}`;
        
        console.log(logMessage);
        this.debugMessages.push(logMessage);
        
        // ログ表示エリア更新
        const logDiv = document.getElementById('mobile-debug-log');
        if (logDiv) {
            const logItem = document.createElement('div');
            logItem.textContent = logMessage;
            
            // ログタイプによる色分け
            switch (type) {
                case 'success':
                    logItem.style.color = '#2ecc71';
                    break;
                case 'error':
                    logItem.style.color = '#e74c3c';
                    break;
                case 'warning':
                    logItem.style.color = '#f39c12';
                    break;
                default:
                    logItem.style.color = '#ecf0f1';
            }
            
            logDiv.appendChild(logItem);
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
        
        // グローバルアクセス用
        window.MobileVoiceSystem = mobileVoiceSystem;
    } else {
        console.log('💻 デスクトップデバイスのため、MobileVoiceSystemは初期化されません');
    }
});
