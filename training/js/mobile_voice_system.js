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
                        background: linear-gradient(135deg, ${this.isAndroidChrome ? '#6c757d 0%, #495057 100%' : '#28a745 0%, #20c997 100%'});
                        margin-top: 8px;
                        font-weight: bold;
                        ${this.isAndroidChrome ? 'opacity: 0.6;' : ''}
                    ">
                        ${this.isAndroidChrome ? '🚫 統合テスト (Chrome制限)' : '🎯 録音+音声認識 統合テスト'}
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
        
        if (this.isAndroidChrome) {
            this.addDebugLog('⚠️ Android Chrome: 統合機能制限あり', 'warning');
            this.addDebugLog('📱 録音・音声認識は個別ボタンでテストしてください', 'info');
        } else {
            this.addDebugLog('✅ 統合機能テスト可能な環境です', 'success');
            this.addDebugLog('🎯 「録音+音声認識 統合テスト」ボタンをタップしてください', 'info');
        }
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
        
        // 🚀 フェーズ4: 統合テストボタンのイベントリスナー
        const unifiedTestBtn = document.getElementById('mobile-unified-test-btn');
        
        if (unifiedTestBtn) {
            unifiedTestBtn.addEventListener('click', () => {
                this.addDebugLog('🎯 録音+音声認識 統合テストボタンがタップされました', 'info');
                this.startUnifiedRecordingAndRecognition();
            });
            this.addDebugLog('✅ 統合テストボタンが正常に配置されました', 'success');
        } else {
            this.addDebugLog('❌ 統合テストボタン(mobile-unified-test-btn)が見つかりません', 'error');
            this.addDebugLog('⚠️ HTML生成で問題が発生した可能性があります', 'warning');
        }
        
        // 🚀 フェーズ5: 読み上げテストボタンのイベントリスナー
        const ttsTestBtn = document.getElementById('mobile-tts-test-btn');
        
        if (ttsTestBtn) {
            ttsTestBtn.addEventListener('click', () => {
                this.addDebugLog('🔊 例文読み上げテストボタンがタップされました', 'info');
                this.startTextToSpeechTest();
            });
            this.addDebugLog('✅ 読み上げテストボタンが正常に配置されました', 'success');
        } else {
            this.addDebugLog('❌ 読み上げテストボタン(mobile-tts-test-btn)が見つかりません', 'error');
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
        
        // 音声認識結果をクリア（新しい認識のため）
        this.recognizedText = '';
        this.updateVoiceResult('音声認識を開始します...', false);
        
        // 既存の音声認識を停止
        if (this.currentRecognition) {
            try {
                this.currentRecognition.stop();
                this.addDebugLog('🛑 既存の音声認識を停止しました', 'info');
            } catch (error) {
                this.addDebugLog(`⚠️ 既存認識停止エラー: ${error.message}`, 'warning');
            }
            this.currentRecognition = null;
        }
        
        this.addDebugLog('🚀 音声認識テスト開始', 'info');
        
        // SpeechRecognition設定（動作確認済み設定を完全移植）
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // 音声認識テスト用のインスタンスとして保存
        this.currentRecognition = recognition;
        
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
            
            // 認識インスタンスをクリア
            this.currentRecognition = null;
            
            if (this.recognizedText && this.recognizedText.trim().length > 0) {
                this.addDebugLog(`✅ 最終認識結果: "${this.recognizedText}"`, 'success');
            } else {
                this.addDebugLog('⚠️ 有効な音声認識結果がありません', 'warning');
            }
            
            this.addDebugLog('🔚 音声認識終了処理完了', 'info');
        };
        
        recognition.onerror = (event) => {
            clearTimeout(timeoutId);
            
            // 認識インスタンスをクリア
            this.currentRecognition = null;
            
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
     * 🚀 フェーズ2: Web Audio API録音機能（Chrome回避版）
     */
    async startRecordingTest() {
        if (this.isRecording) {
            this.stopRecording();
            return;
        }
        
        this.addDebugLog('🎤 マイクアクセス許可を要求中...', 'info');
        this.updateRecordStatus('🎤 マイクアクセス許可を要求中...');
        
        try {
            // AudioContext初期化
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
            }
            
            // マイクアクセス許可（Web Audio API用）
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: false,  // 録音品質重視
                    noiseSuppression: false,
                    autoGainControl: false,
                    sampleRate: 44100
                } 
            });
            
            this.addDebugLog('✅ Web Audio API マイクアクセス許可取得完了', 'success');
            
            // Web Audio APIで録音処理
            this.microphoneSource = this.audioContext.createMediaStreamSource(stream);
            this.recordingProcessor = this.audioContext.createScriptProcessor(4096, 1, 1);
            this.audioChunks = [];  // Float32Array配列として使用
            
            // 録音データ処理
            this.recordingProcessor.onaudioprocess = (event) => {
                if (this.isRecording) {
                    const inputBuffer = event.inputBuffer;
                    const inputData = inputBuffer.getChannelData(0);
                    
                    // Float32Arrayを録音データとして保存
                    this.audioChunks.push(new Float32Array(inputData));
                    
                    // 録音進行表示
                    if (this.audioChunks.length % 10 === 0) {
                        const totalSamples = this.audioChunks.length * 4096;
                        const duration = totalSamples / this.audioContext.sampleRate;
                        this.updateRecordStatus(`🎤 録音中... ${duration.toFixed(1)}秒`);
                    }
                }
            };
            
            // マイクからの音声をプロセッサに接続
            this.microphoneSource.connect(this.recordingProcessor);
            this.recordingProcessor.connect(this.audioContext.destination);
            
            this.isRecording = true;
            this.updateRecordStatus('🎤 Web Audio API録音中... 0.0秒');
            this.addDebugLog('✅ Web Audio API録音開始', 'success');
            
        } catch (error) {
            this.addDebugLog(`❌ Web Audio API録音開始エラー: ${error.message}`, 'error');
            this.updateRecordStatus('❌ 録音開始失敗');
        }
    }
    
    /**
     * 録音停止（Web Audio API版）
     */
    stopRecording() {
        if (this.isRecording) {
            this.isRecording = false;
            
            // Web Audio API録音停止
            if (this.recordingProcessor) {
                this.recordingProcessor.disconnect();
                this.recordingProcessor = null;
            }
            
            if (this.microphoneSource) {
                this.microphoneSource.disconnect();
                this.microphoneSource = null;
            }
            
            this.addDebugLog('� Web Audio API録音停止完了', 'success');
            this.updateRecordStatus('✅ 録音完了');
            
            // 録音データ処理
            if (this.audioChunks.length > 0) {
                const totalSamples = this.audioChunks.length * 4096;
                const duration = totalSamples / this.audioContext.sampleRate;
                this.addDebugLog(`🎵 録音データ保存: ${duration.toFixed(1)}秒`, 'success');
                this.addDebugLog('💾 録音データ保存完了（再生準備OK）', 'success');
            } else {
                this.addDebugLog('⚠️ 録音データが空です', 'warning');
            }
        }
    }
    
    /**
     * 🚀 フェーズ3: Web Audio API録音データ再生機能
     */
    async startPlaybackTest() {
        if (!this.audioChunks || this.audioChunks.length === 0) {
            this.addDebugLog('❌ 再生する録音データがありません（先に録音してください）', 'error');
            return;
        }
        
        if (this.isPlaying) {
            this.addDebugLog('⚠️ 既に再生中です', 'warning');
            return;
        }
        
        this.addDebugLog('🔊 Web Audio API録音データ再生開始', 'info');
        await this.playWithWebAudioAPI();
    }
    
    /**
     * Web Audio API録音データの再生
     */
    async playWithWebAudioAPI() {
        try {
            this.addDebugLog('🎵 Web Audio API再生を開始', 'info');
            
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
                this.addDebugLog('🔧 AudioContext resumed', 'info');
            }
            
            // Float32Array録音データをAudioBufferに変換
            const totalSamples = this.audioChunks.length * 4096;
            const audioBuffer = this.audioContext.createBuffer(
                1, // モノラル
                totalSamples,
                this.audioContext.sampleRate
            );
            
            const channelData = audioBuffer.getChannelData(0);
            let offset = 0;
            
            // Float32Arrayデータを結合
            this.audioChunks.forEach(chunk => {
                channelData.set(chunk, offset);
                offset += chunk.length;
            });
            
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
        }
    }
    
    /**
     * 🚀 フェーズ4: 録音+音声認識 統合実行（ブラウザ別対応版）
     */
    async startUnifiedRecordingAndRecognition() {
        if (this.isUnifiedMode) {
            this.stopUnifiedRecordingAndRecognition();
            return;
        }
        
        // ブラウザ種別による処理分岐
        if (this.isAndroidChrome) {
            this.addDebugLog('🚫 Android Chrome検出: 統合機能は制限されています', 'warning');
            this.addDebugLog('💡 Android Chrome ではマイクリソース競合により同時実行できません', 'info');
            this.addDebugLog('🔄 別々のボタンでテストしてください', 'info');
            this.updateRecordStatus('❌ Android Chrome: 統合機能制限');
            return;
        }
        
        this.addDebugLog(`🎯 録音+音声認識 統合モード開始 (${this.browserInfo})`, 'info');
        this.addDebugLog('🧪 非Android Chrome環境での統合テスト実行', 'info');
        this.isUnifiedMode = true;
        
        try {
            // マイクアクセス許可を取得
            this.addDebugLog('🎤 マイクアクセス許可を要求中...', 'info');
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true,
                    sampleRate: 44100
                } 
            });
            
            this.addDebugLog('✅ マイクアクセス許可取得完了', 'success');
            
            // 1. AudioWorklet APIで録音開始
            await this.startAudioWorkletRecording(stream);
            
            // 2. SpeechRecognition APIで音声認識開始
            this.startUnifiedVoiceRecognition();
            
            this.addDebugLog(`✅ ${this.browserInfo}: AudioWorklet + SpeechRecognition 同時実行開始成功`, 'success');
            this.updateRecordStatus(`🎯 ${this.browserInfo}: 録音+音声認識 同時実行中...`);
            
        } catch (error) {
            this.addDebugLog(`❌ ${this.browserInfo}: 統合モード開始エラー: ${error.message}`, 'error');
            
            // Android Chrome 以外でもエラーが発生した場合の詳細ログ
            if (!this.isAndroidChrome) {
                this.addDebugLog('⚠️ 予想外のエラー: Android Chrome以外でも統合機能が失敗', 'warning');
                this.addDebugLog('📊 ブラウザ情報をレポートに含めてください', 'info');
            }
            
            this.isUnifiedMode = false;
        }
    }
    
    /**
     * AudioWorklet録音開始（最新API版）
     */
    async startAudioWorkletRecording(stream) {
        this.addDebugLog('� AudioWorklet録音セットアップ開始', 'info');
        
        try {
            // AudioContext初期化
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
                this.addDebugLog('🔧 AudioContext resumed', 'info');
            }
            
            // AudioWorkletが利用可能かチェック
            if (!this.audioContext.audioWorklet) {
                this.addDebugLog('⚠️ AudioWorkletが利用できません。ScriptProcessorNodeを使用します', 'warning');
                return this.startScriptProcessorRecording(stream);
            }
            
            // AudioWorkletプロセッサーを読み込み（インライン定義）
            const processorCode = `
                class AudioRecorderWorklet extends AudioWorkletProcessor {
                    constructor() {
                        super();
                        this.isRecording = false;
                        this.port.onmessage = (event) => {
                            if (event.data.command === 'start') {
                                this.isRecording = true;
                            } else if (event.data.command === 'stop') {
                                this.isRecording = false;
                            }
                        };
                    }
                    
                    process(inputs, outputs) {
                        if (this.isRecording && inputs[0].length > 0) {
                            const input = inputs[0][0]; // モノラル
                            if (input) {
                                // 録音データを送信
                                this.port.postMessage({
                                    type: 'audioData',
                                    data: input
                                });
                            }
                        }
                        return true;
                    }
                }
                
                registerProcessor('audio-recorder-worklet', AudioRecorderWorklet);
            `;
            
            const blob = new Blob([processorCode], { type: 'application/javascript' });
            const workletURL = URL.createObjectURL(blob);
            
            await this.audioContext.audioWorklet.addModule(workletURL);
            this.addDebugLog('✅ AudioWorkletプロセッサー読み込み完了', 'success');
            
            // AudioWorkletNode作成
            this.audioWorkletNode = new AudioWorkletNode(this.audioContext, 'audio-recorder-worklet');
            this.audioChunks = [];
            
            // 録音データ受信
            this.audioWorkletNode.port.onmessage = (event) => {
                if (event.data.type === 'audioData' && this.isRecording) {
                    this.audioChunks.push(new Float32Array(event.data.data));
                    
                    // 録音進行表示
                    if (this.audioChunks.length % 10 === 0) {
                        const totalSamples = this.audioChunks.length * 128; // AudioWorkletは128サンプル単位
                        const duration = totalSamples / this.audioContext.sampleRate;
                        this.updateRecordStatus(`🎤 AudioWorklet録音中... ${duration.toFixed(1)}秒`);
                    }
                }
            };
            
            // MediaStreamSourceを作成してAudioWorkletに接続
            this.microphoneSource = this.audioContext.createMediaStreamSource(stream);
            this.microphoneSource.connect(this.audioWorkletNode);
            
            // 録音開始
            this.isRecording = true;
            this.audioWorkletNode.port.postMessage({ command: 'start' });
            
            this.addDebugLog('✅ AudioWorklet録音開始', 'success');
            
        } catch (error) {
            this.addDebugLog(`❌ AudioWorklet録音エラー: ${error.message}`, 'error');
            // フォールバック: ScriptProcessorNodeを使用
            this.addDebugLog('🔄 ScriptProcessorNodeへフォールバック', 'info');
            return this.startScriptProcessorRecording(stream);
        }
    }
    
    /**
     * ScriptProcessorNode録音（フォールバック版）
     */
    async startScriptProcessorRecording(stream) {
        this.addDebugLog('🎵 ScriptProcessorNode録音セットアップ開始（フォールバック）', 'info');
        
        try {
            // マイクからの音声をScriptProcessorで処理
            this.microphoneSource = this.audioContext.createMediaStreamSource(stream);
            this.recordingProcessor = this.audioContext.createScriptProcessor(4096, 1, 1);
            this.audioChunks = [];
            
            // 録音データ処理
            this.recordingProcessor.onaudioprocess = (event) => {
                if (this.isRecording) {
                    const inputBuffer = event.inputBuffer;
                    const inputData = inputBuffer.getChannelData(0);
                    
                    // Float32Arrayを録音データとして保存
                    this.audioChunks.push(new Float32Array(inputData));
                    
                    // 録音進行表示
                    if (this.audioChunks.length % 10 === 0) {
                        const totalSamples = this.audioChunks.length * 4096;
                        const duration = totalSamples / this.audioContext.sampleRate;
                        this.updateRecordStatus(`🎤 ScriptProcessor録音中... ${duration.toFixed(1)}秒`);
                    }
                }
            };
            
            // マイクからの音声をプロセッサに接続
            this.microphoneSource.connect(this.recordingProcessor);
            this.recordingProcessor.connect(this.audioContext.destination);
            
            this.isRecording = true;
            this.addDebugLog('✅ ScriptProcessorNode録音開始', 'success');
            
        } catch (error) {
            this.addDebugLog(`❌ ScriptProcessorNode録音エラー: ${error.message}`, 'error');
            throw error;
        }
    }
    
    /**
     * 統合音声認識開始
     */
    startUnifiedVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ 音声認識APIが利用できません', 'error');
            return;
        }
        
        // 統合モード専用: 認識結果をクリア
        this.recognizedText = '';
        this.updateVoiceResult('統合モード: 音声認識を開始します...', false);
        
        this.addDebugLog('🎤 統合モード: 音声認識開始', 'info');
        
        // SpeechRecognition設定
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.currentRecognition = new SpeechRecognition();
        
        // 統合モード最適化設定
        this.currentRecognition.continuous = true;  // 連続認識
        this.currentRecognition.interimResults = true;
        this.currentRecognition.maxAlternatives = 1;
        this.currentRecognition.lang = 'en-US';
        
        // タイムアウト設定（統合モードは長め）
        const timeoutDuration = 20000; // 20秒
        let timeoutId = setTimeout(() => {
            this.stopUnifiedRecordingAndRecognition();
            this.addDebugLog(`⏰ 統合モードがタイムアウトしました（${timeoutDuration/1000}秒）`, 'warning');
        }, timeoutDuration);
        
        // イベントハンドラー設定
        this.currentRecognition.onstart = () => {
            this.addDebugLog('✅ 統合モード: 音声認識開始イベント発生', 'success');
            this.addDebugLog('🎯 統合モード実行中: 同時に話してください（20秒以内）...', 'info');
        };
        
        this.currentRecognition.onresult = (event) => {
            this.addDebugLog('🎯 統合モード: 音声認識結果イベント発生', 'info');
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence || 0;
                
                if (result.isFinal) {
                    this.recognizedText = transcript;
                    this.addDebugLog(`✅ 統合モード: 認識結果（確定）: "${transcript}"`, 'success');
                    this.addDebugLog(`📊 統合モード: 信頼度: ${(confidence * 100).toFixed(1)}%`, 'info');
                    this.updateVoiceResult(transcript, true);
                } else {
                    this.addDebugLog(`🔄 統合モード: 認識結果（途中）: "${transcript}"`, 'info');
                    this.updateVoiceResult(transcript, false);
                }
            }
        };
        
        this.currentRecognition.onend = () => {
            clearTimeout(timeoutId);
            this.addDebugLog('🔚 統合モード: 音声認識終了イベント発生', 'info');
            
            if (this.recognizedText && this.recognizedText.trim().length > 0) {
                this.addDebugLog(`✅ 統合モード: 最終認識結果: "${this.recognizedText}"`, 'success');
            } else {
                this.addDebugLog('⚠️ 統合モード: 有効な音声認識結果がありません', 'warning');
            }
        };
        
        this.currentRecognition.onerror = (event) => {
            clearTimeout(timeoutId);
            this.addDebugLog(`❌ 統合モード: 音声認識エラー: ${event.error}`, 'error');
            this.currentRecognition = null;
        };
        
        // 音声認識開始
        try {
            this.currentRecognition.start();
            this.addDebugLog('🚀 統合モード: 音声認識開始実行', 'info');
        } catch (error) {
            this.addDebugLog(`❌ 統合モード: 音声認識開始失敗: ${error.message}`, 'error');
        }
    }
    
    /**
     * 統合モード停止（AudioWorklet対応版）
     */
    stopUnifiedRecordingAndRecognition() {
        this.addDebugLog('🔚 録音+音声認識 統合モード停止開始', 'info');
        
        this.isUnifiedMode = false;
        
        // 録音停止
        if (this.isRecording) {
            this.isRecording = false;
            
            // AudioWorklet停止
            if (this.audioWorkletNode) {
                this.audioWorkletNode.port.postMessage({ command: 'stop' });
                this.audioWorkletNode.disconnect();
                this.audioWorkletNode = null;
                this.addDebugLog('✅ 統合モード: AudioWorklet録音停止完了', 'success');
            }
            
            // ScriptProcessorNode停止（フォールバック）
            if (this.recordingProcessor) {
                this.recordingProcessor.disconnect();
                this.recordingProcessor = null;
                this.addDebugLog('✅ 統合モード: ScriptProcessor録音停止完了', 'success');
            }
            
            if (this.microphoneSource) {
                this.microphoneSource.disconnect();
                this.microphoneSource = null;
            }
        }
        
        // 音声認識停止
        if (this.currentRecognition) {
            try {
                this.currentRecognition.stop();
                this.addDebugLog('✅ 統合モード: 音声認識停止完了', 'success');
            } catch (error) {
                this.addDebugLog(`⚠️ 統合モード: 音声認識停止エラー: ${error.message}`, 'warning');
            }
            this.currentRecognition = null;
        }
        
        // 結果表示
        if (this.audioChunks.length > 0) {
            const sampleSize = this.audioWorkletNode ? 128 : 4096; // AudioWorkletは128サンプル、ScriptProcessorは4096サンプル
            const totalSamples = this.audioChunks.length * sampleSize;
            const duration = totalSamples / this.audioContext.sampleRate;
            this.addDebugLog(`🎵 統合モード完了: 録音データ ${duration.toFixed(1)}秒`, 'success');
        }
        
        if (this.recognizedText && this.recognizedText.trim().length > 0) {
            this.addDebugLog(`🎯 統合モード完了: 音声認識 "${this.recognizedText}"`, 'success');
        }
        
        this.updateRecordStatus('✅ 統合モード完了（録音+音声認識）');
        this.addDebugLog('🎉 AudioWorklet版 録音+音声認識 統合テスト完了！', 'success');
    }
    
    /**
     * 方法2: ダウンロードリンク生成（最終手段）
     */
    createDownloadLink() {
        try {
            this.addDebugLog('💾 ダウンロードリンクを生成します', 'info');
            
            if (!this.recordedAudioData || this.recordedAudioData.length === 0) {
                this.addDebugLog('❌ 録音データがありません', 'error');
                return;
            }
            
            // Float32ArrayをWAVファイルに変換
            const wavBlob = this.float32ArrayToWav(this.recordedAudioData, this.audioContext.sampleRate);
            const audioUrl = URL.createObjectURL(wavBlob);
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const filename = `rephrase_recording_${timestamp}.wav`;
            
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
     * Float32ArrayをWAVファイルに変換
     */
    float32ArrayToWav(buffer, sampleRate) {
        const length = buffer.length;
        const arrayBuffer = new ArrayBuffer(44 + length * 2);
        const view = new DataView(arrayBuffer);
        
        // WAVヘッダー書き込み
        const writeString = (offset, string) => {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        };
        
        writeString(0, 'RIFF');
        view.setUint32(4, 36 + length * 2, true);
        writeString(8, 'WAVE');
        writeString(12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, 1, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true);
        view.setUint16(34, 16, true);
        writeString(36, 'data');
        view.setUint32(40, length * 2, true);
        
        // 音声データ書き込み（Float32を16bit integerに変換）
        let offset = 44;
        for (let i = 0; i < length; i++) {
            const sample = Math.max(-1, Math.min(1, buffer[i]));
            view.setInt16(offset, sample * 0x7FFF, true);
            offset += 2;
        }
        
        return new Blob([arrayBuffer], { type: 'audio/wav' });
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
    
    /**
     * 🚀 フェーズ5: 例文読み上げテスト機能
     */
    async startTextToSpeechTest() {
        this.addDebugLog('🔊 例文読み上げテスト開始', 'info');
        
        // 現在の例文を取得
        const sentence = this.getCurrentSentence();
        
        if (!sentence || sentence.trim().length === 0) {
            this.addDebugLog('❌ 読み上げる例文がありません', 'error');
            this.addDebugLog('💡 メインの学習画面で例文を表示してからお試しください', 'info');
            return;
        }
        
        this.addDebugLog(`📝 読み上げ対象: "${sentence}"`, 'info');
        
        // 既存の音声を停止
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
            this.addDebugLog('🛑 既存の読み上げを停止しました', 'info');
        }
        
        // 音声リストの確保
        await this.ensureVoicesLoaded();
        
        // 読み上げ実行
        await this.speakSentence(sentence);
    }
    
    /**
     * 音声リストの読み込み確保
     */
    async ensureVoicesLoaded() {
        let voices = speechSynthesis.getVoices();
        
        if (voices.length === 0) {
            this.addDebugLog('⏳ 音声リストの読み込みを待機中...', 'info');
            await new Promise(resolve => {
                const checkVoices = () => {
                    voices = speechSynthesis.getVoices();
                    if (voices.length > 0) {
                        this.addDebugLog(`✅ 音声リスト読み込み完了: ${voices.length}個`, 'success');
                        resolve();
                    } else {
                        setTimeout(checkVoices, 100);
                    }
                };
                checkVoices();
            });
        } else {
            this.addDebugLog(`✅ 音声リスト準備済み: ${voices.length}個`, 'success');
        }
        
        this.availableVoices = voices;
    }
    
    /**
     * 例文を音声で読み上げ
     */
    async speakSentence(sentence) {
        this.addDebugLog('🎤 音声合成を開始します', 'info');
        
        // SpeechSynthesisUtterance作成
        this.currentUtterance = new SpeechSynthesisUtterance(sentence);
        
        // 女性の英語音声を優先選択
        const selectedVoice = this.selectBestVoice();
        
        if (selectedVoice) {
            this.currentUtterance.voice = selectedVoice;
            this.addDebugLog(`🗣️ 選択された音声: ${selectedVoice.name} (${selectedVoice.lang})`, 'success');
        } else {
            this.addDebugLog('⚠️ 適切な音声が見つかりません。デフォルト音声を使用します', 'warning');
        }
        
        // 音声パラメータ設定
        this.currentUtterance.rate = 0.8;  // 少しゆっくり
        this.currentUtterance.pitch = 1.0; // 標準ピッチ
        this.currentUtterance.volume = 1.0; // 最大音量
        
        // イベントハンドラー設定
        this.currentUtterance.onstart = () => {
            this.addDebugLog(`🔊 読み上げ開始: "${sentence}"`, 'success');
        };
        
        this.currentUtterance.onend = () => {
            this.addDebugLog('✅ 読み上げ完了', 'success');
        };
        
        this.currentUtterance.onerror = (event) => {
            this.addDebugLog(`❌ 読み上げエラー: ${event.error}`, 'error');
        };
        
        // 読み上げ実行
        speechSynthesis.speak(this.currentUtterance);
        this.addDebugLog('🚀 音声合成を実行しました', 'info');
    }
    
    /**
     * 最適な音声を選択（女性の英語音声を優先）
     */
    selectBestVoice() {
        const voices = this.availableVoices;
        
        if (!voices || voices.length === 0) {
            this.addDebugLog('❌ 利用可能な音声がありません', 'error');
            return null;
        }
        
        this.addDebugLog('🔍 最適な音声を選択中...', 'info');
        
        // 女性の英語音声を最優先で探す
        const femaleEnglishVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.toLowerCase().includes('female') || 
             voice.name.toLowerCase().includes('woman') ||
             voice.name.toLowerCase().includes('zira') ||    // Microsoft Zira (女性)
             voice.name.toLowerCase().includes('hazel') ||   // Microsoft Hazel (女性)
             voice.name.toLowerCase().includes('samantha') || // macOS Samantha (女性)
             voice.name.toLowerCase().includes('karen') ||   // macOS Karen (女性)
             voice.name.toLowerCase().includes('anna') ||    // Anna (女性)
             voice.name.toLowerCase().includes('linda') ||   // Linda (女性)
             voice.name.toLowerCase().includes('heather'))   // Heather (女性)
        );
        
        if (femaleEnglishVoice) {
            this.addDebugLog(`👩 女性英語音声を発見: ${femaleEnglishVoice.name}`, 'success');
            return femaleEnglishVoice;
        }
        
        // 女性音声が見つからない場合は、一般的な英語音声を選択
        const englishVoice = voices.find(voice => voice.lang.startsWith('en'));
        
        if (englishVoice) {
            this.addDebugLog(`🇺🇸 英語音声を選択: ${englishVoice.name}`, 'success');
            return englishVoice;
        }
        
        // 英語音声がない場合はデフォルト
        this.addDebugLog('⚠️ 英語音声が見つかりません。デフォルト音声を使用', 'warning');
        return voices[0] || null;
    }
    
    /**
     * 音声リストを読み込み
     */
    loadVoices() {
        const updateVoices = () => {
            const voices = speechSynthesis.getVoices();
            this.availableVoices = voices;
            
            if (voices.length > 0) {
                this.addDebugLog(`📢 音声リスト読み込み: ${voices.length}個`, 'success');
                
                // 英語音声をチェック
                const englishVoices = voices.filter(voice => voice.lang.startsWith('en'));
                if (englishVoices.length > 0) {
                    this.addDebugLog(`🇺🇸 英語音声: ${englishVoices.length}個見つかりました`, 'success');
                    
                    // 女性音声をチェック
                    const femaleVoices = englishVoices.filter(voice => 
                        voice.name.toLowerCase().includes('female') || 
                        voice.name.toLowerCase().includes('woman') ||
                        voice.name.toLowerCase().includes('zira') ||
                        voice.name.toLowerCase().includes('hazel') ||
                        voice.name.toLowerCase().includes('samantha') ||
                        voice.name.toLowerCase().includes('karen') ||
                        voice.name.toLowerCase().includes('anna') ||
                        voice.name.toLowerCase().includes('linda') ||
                        voice.name.toLowerCase().includes('heather')
                    );
                    
                    if (femaleVoices.length > 0) {
                        this.addDebugLog(`👩 女性英語音声: ${femaleVoices.length}個利用可能`, 'success');
                    }
                } else {
                    this.addDebugLog('⚠️ 英語音声が見つかりません', 'warning');
                }
            }
        };
        
        // 初回実行
        updateVoices();
        
        // 音声リストが更新された時のイベントリスナー
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = updateVoices;
        }
    }
    
    /**
     * 現在表示されている例文を取得
     */
    getCurrentSentence() {
        this.addDebugLog('📝 現在の例文取得を開始...', 'info');
        
        // 方法1: window.loadedJsonDataから構築
        if (window.loadedJsonData && Array.isArray(window.loadedJsonData)) {
            const sentence = this.buildSentenceFromData();
            if (sentence && sentence.trim().length > 0) {
                this.addDebugLog(`✅ データから例文を取得: "${sentence}"`, 'success');
                return sentence;
            }
        }
        
        // 方法2: DOMから直接取得
        const domSentence = this.buildSentenceFromDOM();
        if (domSentence && domSentence.trim().length > 0) {
            this.addDebugLog(`✅ DOMから例文を取得: "${domSentence}"`, 'success');
            return domSentence;
        }
        
        // 方法3: テスト用のサンプル文
        const testSentence = 'This is a test sentence for speech synthesis.';
        this.addDebugLog(`🧪 テスト例文を使用: "${testSentence}"`, 'info');
        return testSentence;
    }
    
    /**
     * データから例文を構築
     */
    buildSentenceFromData() {
        try {
            const words = [];
            
            // loadedJsonDataから順序通りに単語を取得
            if (window.loadedJsonData) {
                for (const item of window.loadedJsonData) {
                    if (item.text && item.text.trim()) {
                        words.push(item.text.trim());
                    }
                }
            }
            
            const sentence = words.join(' ');
            this.addDebugLog(`🔧 データ構築結果: "${sentence}"`, 'info');
            return sentence;
        } catch (error) {
            this.addDebugLog(`❌ データ構築エラー: ${error.message}`, 'error');
            return '';
        }
    }
    
    /**
     * DOMから例文を構築
     */
    buildSentenceFromDOM() {
        try {
            const words = [];
            
            // メインのスロットエリアから単語を取得
            const slots = document.querySelectorAll('.slot-content, .subslot-content, [data-slot-text]');
            
            slots.forEach(slot => {
                const text = slot.textContent || slot.innerText || '';
                if (text.trim() && !text.includes('(') && text !== '...') {
                    words.push(text.trim());
                }
            });
            
            // 重複除去と整理
            const uniqueWords = [...new Set(words)];
            const sentence = uniqueWords.join(' ');
            
            this.addDebugLog(`🔧 DOM構築結果: "${sentence}"`, 'info');
            return sentence;
        } catch (error) {
            this.addDebugLog(`❌ DOM構築エラー: ${error.message}`, 'error');
            return '';
        }
    }
    
    /**
     * 🚀 スマホ用デバッグ情報表示（コンソール不要版）
     */
    showMobileDebugInfo() {
        this.addMobileDebugInfo('🔧 スマホ用デバッグ表示を開始', 'info');
        
        // ブラウザ検出結果
        this.addMobileDebugInfo(`📱 デバイス検出: ${this.isMobile ? 'モバイル' : 'デスクトップ'}`, this.isMobile ? 'success' : 'warning');
        this.addMobileDebugInfo(`🌐 ブラウザ: ${this.browserInfo}`, 'info');
        this.addMobileDebugInfo(`🤖 User Agent: ${navigator.userAgent.substring(0, 80)}...`, 'info');
        
        // User Agent詳細検証（Edge検出用）
        this.addMobileDebugInfo('🔍 User Agent詳細解析:', 'info');
        const ua = navigator.userAgent;
        this.addMobileDebugInfo(`  🔸 Contains 'Android': ${/Android/i.test(ua)}`, 'info');
        this.addMobileDebugInfo(`  🔸 Contains 'Chrome': ${/Chrome/i.test(ua)}`, 'info');
        this.addMobileDebugInfo(`  🔸 Contains 'Edg': ${/Edg/i.test(ua)}`, 'info');
        this.addMobileDebugInfo(`  🔸 Contains 'EdgA': ${/EdgA/i.test(ua)}`, 'info');
        this.addMobileDebugInfo(`  🔸 Contains 'Edge': ${/Edge/i.test(ua)}`, 'info');
        this.addMobileDebugInfo(`  🔸 Contains 'Firefox': ${/Firefox/i.test(ua)}`, 'info');
        this.addMobileDebugInfo(`  🔸 Contains 'SamsungBrowser': ${/SamsungBrowser/i.test(ua)}`, 'info');
        
        // Android ブラウザ詳細
        if (this.isAndroid) {
            this.addMobileDebugInfo('📱 Android詳細:', 'info');
            this.addMobileDebugInfo(`  🔹 Chrome: ${this.isAndroidChrome ? 'はい' : 'いいえ'}`, this.isAndroidChrome ? 'success' : 'info');
            this.addMobileDebugInfo(`  🔹 Firefox: ${this.isAndroidFirefox ? 'はい' : 'いいえ'}`, this.isAndroidFirefox ? 'success' : 'info');
            this.addMobileDebugInfo(`  🔹 Samsung: ${this.isAndroidSamsung ? 'はい' : 'いいえ'}`, this.isAndroidSamsung ? 'success' : 'info');
            this.addMobileDebugInfo(`  🔹 Edge: ${this.isAndroidEdge ? 'はい' : 'いいえ'}`, this.isAndroidEdge ? 'success' : 'info');
            
            // 統合テスト利用可能性の表示
            this.addMobileDebugInfo(`  🎯 統合テスト: ${this.isAndroidChrome ? '制限あり (Chrome)' : '利用可能'}`, this.isAndroidChrome ? 'warning' : 'success');
        }
        
        // 重要な要素の検出状況
        const voiceDebugPanel = document.getElementById('voice-debug-panel');
        this.addMobileDebugInfo(`🎯 voice-debug-panel要素: ${voiceDebugPanel ? '見つかりました' : '見つかりません'}`, voiceDebugPanel ? 'success' : 'error');
        
        if (voiceDebugPanel) {
            this.addMobileDebugInfo(`  📏 表示状態: ${voiceDebugPanel.style.display || 'デフォルト'}`, 'info');
            this.addMobileDebugInfo(`  👁️ 可視性: ${voiceDebugPanel.offsetWidth > 0 ? '表示中' : '非表示'}`, voiceDebugPanel.offsetWidth > 0 ? 'success' : 'warning');
        }
        
        // 音声API対応状況（詳細版）
        this.addMobileDebugInfo('🎤 音声API詳細対応状況:', 'info');
        
        // SpeechRecognition詳細チェック
        const speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.addMobileDebugInfo(`  🔹 SpeechRecognition: ${window.SpeechRecognition ? 'あり' : 'なし'}`, window.SpeechRecognition ? 'success' : 'warning');
        this.addMobileDebugInfo(`  🔹 webkitSpeechRecognition: ${window.webkitSpeechRecognition ? 'あり' : 'なし'}`, window.webkitSpeechRecognition ? 'success' : 'warning');
        this.addMobileDebugInfo(`  🔹 統合判定: ${speechRecognition ? '利用可能' : '利用不可'}`, speechRecognition ? 'success' : 'error');
        
        // その他のAPI
        this.addMobileDebugInfo(`  🔹 音声合成: ${speechSynthesis ? '対応' : '非対応'}`, speechSynthesis ? 'success' : 'error');
        this.addMobileDebugInfo(`  🔹 MediaDevices: ${navigator.mediaDevices ? '対応' : '非対応'}`, navigator.mediaDevices ? 'success' : 'error');
        this.addMobileDebugInfo(`  🔹 AudioContext: ${window.AudioContext || window.webkitAudioContext ? '対応' : '非対応'}`, (window.AudioContext || window.webkitAudioContext) ? 'success' : 'error');
        
        // セキュリティ関連チェック
        this.addMobileDebugInfo('🔒 セキュリティ・接続状況:', 'info');
        this.addMobileDebugInfo(`  🔹 HTTPS: ${location.protocol === 'https:' ? 'はい' : 'いいえ（HTTPSが必要）'}`, location.protocol === 'https:' ? 'success' : 'error');
        this.addMobileDebugInfo(`  🔹 Localhost: ${location.hostname === 'localhost' || location.hostname === '127.0.0.1' ? 'はい' : 'いいえ'}`, (location.hostname === 'localhost' || location.hostname === '127.0.0.1') ? 'success' : 'info');
        this.addMobileDebugInfo(`  🔹 現在のURL: ${location.href}`, 'info');
        
        // ブラウザ機能制限チェック
        this.addMobileDebugInfo('🚫 ブラウザ制限チェック:', 'info');
        this.addMobileDebugInfo(`  🔹 プライベートモード: ${this.detectPrivateMode() ? '可能性あり' : '通常モード'}`, this.detectPrivateMode() ? 'warning' : 'success');
        
        // 初期化エラーがある場合は表示
        if (this.initErrors.length > 0) {
            this.addMobileDebugInfo('⚠️ 初期化エラー:', 'warning');
            this.initErrors.forEach(error => {
                this.addMobileDebugInfo(`  ❌ ${error}`, 'error');
            });
        } else {
            this.addMobileDebugInfo('✅ 初期化エラーなし', 'success');
        }
        
        // Firefox特有の問題チェック
        if (this.isAndroidFirefox) {
            this.addMobileDebugInfo('🔥 Firefox固有チェック:', 'info');
            this.addMobileDebugInfo('  🔍 パネル開閉問題の調査を開始', 'warning');
            
            // Firefox での voice-debug-panel の状態詳細
            if (voiceDebugPanel) {
                const computedStyle = window.getComputedStyle(voiceDebugPanel);
                this.addMobileDebugInfo(`  📊 z-index: ${computedStyle.zIndex}`, 'info');
                this.addMobileDebugInfo(`  📊 position: ${computedStyle.position}`, 'info');
                this.addMobileDebugInfo(`  📊 visibility: ${computedStyle.visibility}`, 'info');
                this.addMobileDebugInfo(`  📊 opacity: ${computedStyle.opacity}`, 'info');
            }
        }
        
        this.addMobileDebugInfo('🎉 スマホ用デバッグ表示完了', 'success');
    }
    
    /**
     * プライベートモード検出
     */
    detectPrivateMode() {
        try {
            // localStorage アクセステスト
            localStorage.setItem('__privatetest', 'test');
            localStorage.removeItem('__privatetest');
            return false; // 通常モード
        } catch (e) {
            return true; // プライベートモードの可能性
        }
    }
    
    /**
     * スマホ用デバッグ情報をパネルに追加
     */
    addMobileDebugInfo(message, type = 'info') {
        // デバッグパネルが存在しない場合は、代替表示エリアを作成
        let debugArea = document.getElementById('mobile-debug-log');
        
        if (!debugArea) {
            // デバッグパネルが見つからない場合、直接body に追加
            debugArea = document.createElement('div');
            debugArea.id = 'mobile-debug-info';
            debugArea.style.cssText = `
                position: fixed;
                top: 10px;
                left: 10px;
                right: 10px;
                max-height: 300px;
                overflow-y: auto;
                background: rgba(0,0,0,0.9);
                color: white;
                padding: 10px;
                border-radius: 5px;
                z-index: 10000;
                font-size: 12px;
                font-family: monospace;
                line-height: 1.3;
            `;
            document.body.appendChild(debugArea);
            
            // 閉じるボタンを追加
            const closeBtn = document.createElement('button');
            closeBtn.textContent = '✕';
            closeBtn.style.cssText = `
                position: absolute;
                top: 5px;
                right: 5px;
                background: red;
                color: white;
                border: none;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                cursor: pointer;
                font-size: 10px;
            `;
            closeBtn.onclick = () => debugArea.remove();
            debugArea.appendChild(closeBtn);
        }
        
        // メッセージ追加
        const timestamp = new Date().toLocaleTimeString();
        const logMessage = `[${timestamp}] ${message}`;
        
        const logItem = document.createElement('div');
        logItem.textContent = logMessage;
        logItem.style.marginBottom = '2px';
        
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
        
        debugArea.appendChild(logItem);
        debugArea.scrollTop = debugArea.scrollHeight;
        
        // ログが多すぎる場合は古いものを削除
        const logItems = debugArea.children;
        if (logItems.length > 30) {
            debugArea.removeChild(logItems[1]); // 閉じるボタンは保持
        }
    }
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
