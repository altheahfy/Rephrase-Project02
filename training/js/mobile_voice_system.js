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
        
        // 🚀 フェーズ4: 統合機能プロパティ
        this.isUnifiedMode = false;
        this.currentRecognition = null;
        
        console.log('📱 モバイル検出結果:', {
            isMobile: this.isMobile,
            isAndroid: this.isAndroid,
            userAgent: navigator.userAgent
        });
        
        // 🔧 デスクトップテスト用: モバイルチェックを一時的に無効化
        // if (!this.isMobile) {
        //     console.log('⚠️ デスクトップデバイスが検出されました。このシステムはモバイル専用です。');
        //     return;
        // }
        
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
                    <button id="mobile-unified-test-btn" class="voice-test-btn" style="
                        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                        margin-top: 8px;
                        font-weight: bold;
                    ">
                        🎯 録音+音声認識 統合テスト
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
        this.addDebugLog('📱 統合ボタンテスト準備完了', 'info');
        this.addDebugLog('🎯 「録音+音声認識 統合テスト」ボタンをタップしてください', 'info');
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
     * 🚀 フェーズ4: 録音+音声認識 統合実行
     */
    async startUnifiedRecordingAndRecognition() {
        if (this.isUnifiedMode) {
            this.stopUnifiedRecordingAndRecognition();
            return;
        }
        
        this.addDebugLog('🎯 録音+音声認識 統合モード開始', 'info');
        this.isUnifiedMode = true;
        
        try {
            // 1. 録音開始（Web Audio API）
            await this.startUnifiedRecording();
            
            // 2. 音声認識開始（SpeechRecognition API）
            this.startUnifiedVoiceRecognition();
            
            this.addDebugLog('✅ 録音+音声認識 同時実行開始成功', 'success');
            this.updateRecordStatus('🎯 録音+音声認識 同時実行中...');
            
        } catch (error) {
            this.addDebugLog(`❌ 統合モード開始エラー: ${error.message}`, 'error');
            this.isUnifiedMode = false;
        }
    }
    
    /**
     * 統合録音開始（Web Audio API版）
     */
    async startUnifiedRecording() {
        this.addDebugLog('🎤 統合モード: Web Audio API録音開始', 'info');
        
        // AudioContext初期化
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        
        if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }
        
        // マイクアクセス許可
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: false,
                noiseSuppression: false,
                autoGainControl: false,
                sampleRate: 44100
            } 
        });
        
        this.addDebugLog('✅ 統合モード: マイクアクセス許可取得完了', 'success');
        
        // Web Audio APIで録音処理
        this.microphoneSource = this.audioContext.createMediaStreamSource(stream);
        this.recordingProcessor = this.audioContext.createScriptProcessor(4096, 1, 1);
        this.audioChunks = [];
        
        // 録音データ処理
        this.recordingProcessor.onaudioprocess = (event) => {
            if (this.isUnifiedMode) {
                const inputBuffer = event.inputBuffer;
                const inputData = inputBuffer.getChannelData(0);
                this.audioChunks.push(new Float32Array(inputData));
                
                // 進行表示
                if (this.audioChunks.length % 10 === 0) {
                    const totalSamples = this.audioChunks.length * 4096;
                    const duration = totalSamples / this.audioContext.sampleRate;
                    this.updateRecordStatus(`🎯 統合実行中... 録音: ${duration.toFixed(1)}秒`);
                }
            }
        };
        
        // 接続
        this.microphoneSource.connect(this.recordingProcessor);
        this.recordingProcessor.connect(this.audioContext.destination);
        
        this.isRecording = true;
    }
    
    /**
     * 統合音声認識開始
     */
    startUnifiedVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ 音声認識APIが利用できません', 'error');
            return;
        }
        
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
            }
        };
        
        this.currentRecognition.onerror = (event) => {
            clearTimeout(timeoutId);
            this.addDebugLog(`❌ 統合モード: 音声認識エラー: ${event.error}`, 'error');
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
     * 統合モード停止
     */
    stopUnifiedRecordingAndRecognition() {
        this.addDebugLog('🔚 録音+音声認識 統合モード停止開始', 'info');
        
        this.isUnifiedMode = false;
        
        // 録音停止
        if (this.isRecording) {
            this.isRecording = false;
            
            if (this.recordingProcessor) {
                this.recordingProcessor.disconnect();
                this.recordingProcessor = null;
            }
            
            if (this.microphoneSource) {
                this.microphoneSource.disconnect();
                this.microphoneSource = null;
            }
            
            this.addDebugLog('✅ 統合モード: Web Audio API録音停止完了', 'success');
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
            const totalSamples = this.audioChunks.length * 4096;
            const duration = totalSamples / this.audioContext.sampleRate;
            this.addDebugLog(`🎵 統合モード完了: 録音データ ${duration.toFixed(1)}秒`, 'success');
        }
        
        if (this.recognizedText && this.recognizedText.trim().length > 0) {
            this.addDebugLog(`🎯 統合モード完了: 音声認識 "${this.recognizedText}"`, 'success');
        }
        
        this.updateRecordStatus('✅ 統合モード完了（録音+音声認識）');
        this.addDebugLog('🎉 録音+音声認識 統合テスト完了！', 'success');
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
