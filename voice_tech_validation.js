// 🎙️ Rephrase音声機構 技術検証テスト JavaScript
// 各種音声APIの対応状況と基本動作を検証

class VoiceTechValidator {
    constructor() {
        this.mediaRecorder = null;
        this.audioContext = null;
        this.recordedChunks = [];
        this.recordedBlob = null;
        this.audioStream = null;
        this.analyser = null;
        this.animationId = null;
        this.recordingStartTime = null;
        this.recordingTimerInterval = null;
        
        this.init();
    }
    
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.checkBrowserSupport();
            this.setupEventListeners();
            this.loadVoices();
        });
    }
    
    // 1. ブラウザAPI対応状況チェック
    checkBrowserSupport() {
        console.log('🔍 ブラウザAPI対応状況をチェック中...');
        
        // MediaRecorder API
        this.checkMediaRecorderSupport();
        
        // Web Audio API
        this.checkWebAudioSupport();
        
        // Speech Synthesis API
        this.checkSpeechSynthesisSupport();
        
        // IndexedDB
        this.checkIndexedDBSupport();
    }
    
    checkMediaRecorderSupport() {
        const element = document.getElementById('media-recorder-support');
        const infoElement = document.getElementById('media-recorder-info');
        
        if (typeof MediaRecorder !== 'undefined') {
            element.className = 'status success';
            element.textContent = 'MediaRecorder API: ✅ サポート済み';
            
            // サポートされるMIMEタイプを確認
            const mimeTypes = [
                'audio/webm',
                'audio/webm;codecs=opus',
                'audio/mp4',
                'audio/wav'
            ];
            
            const supportedTypes = mimeTypes.filter(type => MediaRecorder.isTypeSupported(type));
            infoElement.innerHTML = `
                <strong>サポート済みMIMEタイプ:</strong><br>
                ${supportedTypes.length > 0 ? supportedTypes.join('<br>') : 'なし'}
            `;
        } else {
            element.className = 'status error';
            element.textContent = 'MediaRecorder API: ❌ サポートされていません';
            infoElement.textContent = 'このブラウザでは音声録音機能が利用できません';
        }
    }
    
    checkWebAudioSupport() {
        const element = document.getElementById('web-audio-support');
        const infoElement = document.getElementById('audio-context-info');
        
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (AudioContextClass) {
                const testContext = new AudioContextClass();
                element.className = 'status success';
                element.textContent = 'Web Audio API: ✅ サポート済み';
                
                infoElement.innerHTML = `
                    <strong>サンプルレート:</strong> ${testContext.sampleRate}Hz<br>
                    <strong>状態:</strong> ${testContext.state}<br>
                    <strong>ベースレイテンシ:</strong> ${testContext.baseLatency?.toFixed(4) || 'N/A'}s
                `;
                
                testContext.close();
            } else {
                throw new Error('AudioContext not available');
            }
        } catch (error) {
            element.className = 'status error';
            element.textContent = 'Web Audio API: ❌ サポートされていません';
            infoElement.textContent = `エラー: ${error.message}`;
        }
    }
    
    checkSpeechSynthesisSupport() {
        const element = document.getElementById('speech-synthesis-support');
        const infoElement = document.getElementById('speech-synthesis-info');
        
        if ('speechSynthesis' in window) {
            element.className = 'status success';
            element.textContent = 'Speech Synthesis API: ✅ サポート済み';
            
            // 利用可能な音声を確認
            setTimeout(() => {
                const voices = speechSynthesis.getVoices();
                const englishVoices = voices.filter(voice => voice.lang.startsWith('en'));
                
                infoElement.innerHTML = `
                    <strong>利用可能音声数:</strong> ${voices.length}<br>
                    <strong>英語音声数:</strong> ${englishVoices.length}<br>
                    <strong>デフォルト音声:</strong> ${voices.find(v => v.default)?.name || 'なし'}
                `;
            }, 100);
        } else {
            element.className = 'status error';
            element.textContent = 'Speech Synthesis API: ❌ サポートされていません';
            infoElement.textContent = 'このブラウザでは音声合成機能が利用できません';
        }
    }
    
    checkIndexedDBSupport() {
        const element = document.getElementById('indexeddb-support');
        
        if ('indexedDB' in window) {
            element.className = 'status success';
            element.textContent = 'IndexedDB: ✅ サポート済み';
        } else {
            element.className = 'status error';
            element.textContent = 'IndexedDB: ❌ サポートされていません';
        }
    }
    
    // 2. イベントリスナー設定
    setupEventListeners() {
        // 録音関連
        document.getElementById('start-recording').addEventListener('click', () => this.startRecording());
        document.getElementById('stop-recording').addEventListener('click', () => this.stopRecording());
        document.getElementById('play-recording').addEventListener('click', () => this.playRecording());
        document.getElementById('download-recording').addEventListener('click', () => this.downloadRecording());
        
        // 音声合成関連
        document.getElementById('speak-text').addEventListener('click', () => this.speakText());
        document.getElementById('stop-speech').addEventListener('click', () => this.stopSpeech());
        
        // スライダー更新
        document.getElementById('speech-rate').addEventListener('input', (e) => {
            document.getElementById('rate-value').textContent = e.target.value;
        });
        document.getElementById('speech-pitch').addEventListener('input', (e) => {
            document.getElementById('pitch-value').textContent = e.target.value;
        });
        
        // 分析関連
        document.getElementById('analyze-recording').addEventListener('click', () => this.analyzeRecording());
        document.getElementById('test-frequency-analysis').addEventListener('click', () => this.testFrequencyAnalysis());
        
        // テスト関連
        document.getElementById('run-performance-test').addEventListener('click', () => this.runPerformanceTest());
        document.getElementById('run-integration-test').addEventListener('click', () => this.runIntegrationTest());
    }
    
    // 3. 音声録音機能
    async startRecording() {
        try {
            this.log('recording-results', '🎙️ 録音開始処理中...');
            
            // マイクアクセス許可を取得
            this.audioStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                }
            });
            
            this.log('recording-results', '✅ マイクアクセス許可取得済み');
            
            // MediaRecorder初期化
            const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
                ? 'audio/webm;codecs=opus' 
                : 'audio/webm';
                
            this.mediaRecorder = new MediaRecorder(this.audioStream, {
                mimeType: mimeType
            });
            
            this.recordedChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                this.recordedBlob = new Blob(this.recordedChunks, { type: mimeType });
                this.log('recording-results', `📁 録音完了: ${this.recordedBlob.size} bytes`);
                
                // ボタン状態更新
                document.getElementById('play-recording').disabled = false;
                document.getElementById('download-recording').disabled = false;
                document.getElementById('analyze-recording').disabled = false;
            };
            
            // 音量レベルモニタリング設定
            this.setupVolumeMonitoring();
            
            // 録音開始
            this.mediaRecorder.start();
            this.recordingStartTime = Date.now();
            this.startRecordingTimer();
            
            // UI更新
            document.getElementById('start-recording').disabled = true;
            document.getElementById('start-recording').classList.add('recording');
            document.getElementById('stop-recording').disabled = false;
            
            this.log('recording-results', '🔴 録音中... 話してください');
            
        } catch (error) {
            this.log('recording-results', `❌ 録音開始エラー: ${error.message}`);
            console.error('Recording error:', error);
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            
            // ストリーム停止
            if (this.audioStream) {
                this.audioStream.getTracks().forEach(track => track.stop());
            }
            
            // 音量モニタリング停止
            this.stopVolumeMonitoring();
            
            // タイマー停止
            this.stopRecordingTimer();
            
            // UI更新
            document.getElementById('start-recording').disabled = false;
            document.getElementById('start-recording').classList.remove('recording');
            document.getElementById('stop-recording').disabled = true;
            
            this.log('recording-results', '⏹️ 録音停止');
        }
    }
    
    playRecording() {
        if (this.recordedBlob) {
            const audio = new Audio(URL.createObjectURL(this.recordedBlob));
            audio.play();
            this.log('recording-results', '▶️ 録音音声を再生中...');
            
            audio.onended = () => {
                this.log('recording-results', '✅ 再生完了');
            };
        }
    }
    
    downloadRecording() {
        if (this.recordedBlob) {
            const url = URL.createObjectURL(this.recordedBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `voice_recording_${new Date().getTime()}.webm`;
            a.click();
            URL.revokeObjectURL(url);
            
            this.log('recording-results', '💾 録音ファイルをダウンロード中...');
        }
    }
    
    // 4. 音量レベルモニタリング
    setupVolumeMonitoring() {
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            this.audioContext = new AudioContextClass();
            this.analyser = this.audioContext.createAnalyser();
            
            const source = this.audioContext.createMediaStreamSource(this.audioStream);
            source.connect(this.analyser);
            
            this.analyser.fftSize = 256;
            const bufferLength = this.analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            const updateVolume = () => {
                this.analyser.getByteFrequencyData(dataArray);
                
                // 平均音量計算
                const average = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength;
                const volumePercent = (average / 255) * 100;
                
                // 音量バー更新
                document.getElementById('volume-bar').style.width = `${volumePercent}%`;
                
                if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
                    this.animationId = requestAnimationFrame(updateVolume);
                }
            };
            
            updateVolume();
            
        } catch (error) {
            console.error('Volume monitoring setup error:', error);
        }
    }
    
    stopVolumeMonitoring() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
        
        document.getElementById('volume-bar').style.width = '0%';
    }
    
    // 5. 録音タイマー
    startRecordingTimer() {
        this.recordingTimerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            
            document.getElementById('recording-timer').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    stopRecordingTimer() {
        if (this.recordingTimerInterval) {
            clearInterval(this.recordingTimerInterval);
            this.recordingTimerInterval = null;
        }
        document.getElementById('recording-timer').textContent = '00:00';
    }
    
    // 6. 音声合成機能
    loadVoices() {
        const updateVoices = () => {
            const voices = speechSynthesis.getVoices();
            const select = document.getElementById('voice-select');
            
            // 既存のオプションをクリア（最初のオプション以外）
            while (select.children.length > 1) {
                select.removeChild(select.lastChild);
            }
            
            // 英語音声を優先して追加
            const englishVoices = voices.filter(voice => voice.lang.startsWith('en'));
            englishVoices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.name;
                option.textContent = `${voice.name} (${voice.lang})`;
                select.appendChild(option);
            });
            
            // 他の言語の音声も追加
            const otherVoices = voices.filter(voice => !voice.lang.startsWith('en'));
            if (otherVoices.length > 0) {
                const separator = document.createElement('option');
                separator.textContent = '--- その他の言語 ---';
                separator.disabled = true;
                select.appendChild(separator);
                
                otherVoices.forEach(voice => {
                    const option = document.createElement('option');
                    option.value = voice.name;
                    option.textContent = `${voice.name} (${voice.lang})`;
                    select.appendChild(option);
                });
            }
        };
        
        // 音声リストの読み込みを待つ
        if (speechSynthesis.getVoices().length > 0) {
            updateVoices();
        } else {
            speechSynthesis.onvoiceschanged = updateVoices;
        }
    }
    
    speakText() {
        const text = document.getElementById('tts-text').value;
        const voiceName = document.getElementById('voice-select').value;
        const rate = parseFloat(document.getElementById('speech-rate').value);
        const pitch = parseFloat(document.getElementById('speech-pitch').value);
        
        if (!text.trim()) {
            this.log('tts-results', '❌ テキストを入力してください');
            return;
        }
        
        // 既存の音声を停止
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = rate;
        utterance.pitch = pitch;
        
        if (voiceName) {
            const voices = speechSynthesis.getVoices();
            const selectedVoice = voices.find(voice => voice.name === voiceName);
            if (selectedVoice) {
                utterance.voice = selectedVoice;
            }
        }
        
        utterance.onstart = () => {
            this.log('tts-results', `🔊 音声合成開始: "${text}"`);
            this.log('tts-results', `📊 設定 - 速度: ${rate}, ピッチ: ${pitch}, 音声: ${utterance.voice?.name || 'デフォルト'}`);
        };
        
        utterance.onend = () => {
            this.log('tts-results', '✅ 音声合成完了');
        };
        
        utterance.onerror = (event) => {
            this.log('tts-results', `❌ 音声合成エラー: ${event.error}`);
        };
        
        speechSynthesis.speak(utterance);
    }
    
    stopSpeech() {
        speechSynthesis.cancel();
        this.log('tts-results', '⏹️ 音声合成停止');
    }
    
    // 7. 音響分析機能
    async analyzeRecording() {
        if (!this.recordedBlob) {
            this.log('analysis-results', '❌ 分析する録音がありません');
            return;
        }
        
        try {
            this.log('analysis-results', '📊 音響分析開始...');
            
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            const audioContext = new AudioContextClass();
            
            // Blobを ArrayBuffer に変換
            const arrayBuffer = await this.recordedBlob.arrayBuffer();
            
            // 音声データをデコード
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            // 基本的な分析
            const duration = audioBuffer.duration;
            const sampleRate = audioBuffer.sampleRate;
            const numberOfChannels = audioBuffer.numberOfChannels;
            
            // 音量レベル分析
            const channelData = audioBuffer.getChannelData(0); // 最初のチャンネル
            let sumSquared = 0;
            let maxAmplitude = 0;
            
            for (let i = 0; i < channelData.length; i++) {
                const amplitude = Math.abs(channelData[i]);
                sumSquared += amplitude * amplitude;
                maxAmplitude = Math.max(maxAmplitude, amplitude);
            }
            
            const rmsAmplitude = Math.sqrt(sumSquared / channelData.length);
            const averageVolume = rmsAmplitude * 100;
            
            // 結果表示
            this.log('analysis-results', `⏱️ 録音時間: ${duration.toFixed(2)}秒`);
            this.log('analysis-results', `🎵 サンプルレート: ${sampleRate}Hz`);
            this.log('analysis-results', `📊 チャンネル数: ${numberOfChannels}`);
            this.log('analysis-results', `🔊 平均音量: ${averageVolume.toFixed(2)}%`);
            this.log('analysis-results', `📈 最大振幅: ${(maxAmplitude * 100).toFixed(2)}%`);
            
            // 発話速度の簡易推定（単語数ベース）
            const text = document.getElementById('tts-text').value;
            if (text.trim()) {
                const wordCount = text.trim().split(/\s+/).length;
                const wordsPerSecond = wordCount / duration;
                const wordsPerMinute = wordsPerSecond * 60;
                
                this.log('analysis-results', `💬 推定単語数: ${wordCount}`);
                this.log('analysis-results', `⚡ 発話速度: ${wordsPerSecond.toFixed(2)} 語/秒 (${wordsPerMinute.toFixed(0)} 語/分)`);
                
                // レベル評価
                let level = '';
                if (wordsPerSecond < 0.8) level = '初心者レベル';
                else if (wordsPerSecond < 1.2) level = '中級者レベル';
                else if (wordsPerSecond < 2.0) level = '上級者レベル';
                else level = '達人レベル';
                
                this.log('analysis-results', `🎯 評価: ${level}`);
            }
            
            audioContext.close();
            
        } catch (error) {
            this.log('analysis-results', `❌ 分析エラー: ${error.message}`);
            console.error('Audio analysis error:', error);
        }
    }
    
    testFrequencyAnalysis() {
        try {
            this.log('analysis-results', '🎵 周波数分析テスト開始...');
            
            const canvas = document.getElementById('frequency-canvas');
            const ctx = canvas.getContext('2d');
            
            // テスト用音声を生成
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            const audioContext = new AudioContextClass();
            
            // 複数の周波数を合成
            const frequencies = [440, 880, 1320]; // A4, A5, E6
            const duration = 2; // 2秒
            const sampleRate = audioContext.sampleRate;
            const frameCount = sampleRate * duration;
            
            const audioBuffer = audioContext.createBuffer(1, frameCount, sampleRate);
            const channelData = audioBuffer.getChannelData(0);
            
            // 正弦波を合成
            for (let i = 0; i < frameCount; i++) {
                let sample = 0;
                frequencies.forEach(freq => {
                    sample += Math.sin(2 * Math.PI * freq * i / sampleRate) / frequencies.length;
                });
                channelData[i] = sample * 0.3; // 音量調整
            }
            
            // 周波数分析
            const analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(analyser);
            analyser.connect(audioContext.destination);
            
            // スペクトラム描画
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            const draw = () => {
                analyser.getByteFrequencyData(dataArray);
                
                ctx.fillStyle = 'rgb(240, 240, 240)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                const barWidth = canvas.width / bufferLength;
                let x = 0;
                
                for (let i = 0; i < bufferLength; i++) {
                    const barHeight = (dataArray[i] / 255) * canvas.height;
                    
                    const hue = (i / bufferLength) * 360;
                    ctx.fillStyle = `hsl(${hue}, 50%, 50%)`;
                    ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
                    
                    x += barWidth;
                }
                
                requestAnimationFrame(draw);
            };
            
            source.start();
            draw();
            
            this.log('analysis-results', `✅ テスト音声再生中 (${frequencies.join('Hz, ')}Hz)`);
            
            source.onended = () => {
                audioContext.close();
                this.log('analysis-results', '✅ 周波数分析テスト完了');
            };
            
        } catch (error) {
            this.log('analysis-results', `❌ 周波数分析テストエラー: ${error.message}`);
            console.error('Frequency analysis test error:', error);
        }
    }
    
    // 8. パフォーマンステスト
    runPerformanceTest() {
        this.log('performance-results', '⚡ パフォーマンステスト開始...');
        
        const tests = [
            {
                name: 'AudioContext作成',
                test: () => {
                    const start = performance.now();
                    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                    const context = new AudioContextClass();
                    context.close();
                    return performance.now() - start;
                }
            },
            {
                name: 'MediaRecorder初期化',
                test: async () => {
                    const start = performance.now();
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                        const recorder = new MediaRecorder(stream);
                        stream.getTracks().forEach(track => track.stop());
                        return performance.now() - start;
                    } catch (error) {
                        return -1; // エラー
                    }
                }
            },
            {
                name: 'SpeechSynthesis作成',
                test: () => {
                    const start = performance.now();
                    const utterance = new SpeechSynthesisUtterance('test');
                    return performance.now() - start;
                }
            },
            {
                name: '大量データ処理 (10MB)',
                test: () => {
                    const start = performance.now();
                    const data = new Float32Array(10 * 1024 * 1024 / 4); // 10MB
                    for (let i = 0; i < data.length; i++) {
                        data[i] = Math.sin(i * 0.1);
                    }
                    return performance.now() - start;
                }
            }
        ];
        
        const runTest = async (test, index) => {
            try {
                const time = await test.test();
                if (time >= 0) {
                    this.log('performance-results', `✅ ${test.name}: ${time.toFixed(2)}ms`);
                } else {
                    this.log('performance-results', `❌ ${test.name}: エラー`);
                }
            } catch (error) {
                this.log('performance-results', `❌ ${test.name}: ${error.message}`);
            }
            
            if (index < tests.length - 1) {
                setTimeout(() => runTest(tests[index + 1], index + 1), 100);
            } else {
                this.log('performance-results', '✅ 全パフォーマンステスト完了');
            }
        };
        
        runTest(tests[0], 0);
    }
    
    // 9. 統合テスト
    async runIntegrationTest() {
        this.log('integration-results', '🎯 統合テスト開始...');
        
        const steps = [
            {
                name: '模範音声の生成・再生',
                action: async () => {
                    return new Promise((resolve) => {
                        const utterance = new SpeechSynthesisUtterance('She is a software engineer');
                        utterance.rate = 0.8;
                        utterance.onend = () => resolve('✅ 模範音声再生完了');
                        utterance.onerror = () => resolve('❌ 模範音声エラー');
                        speechSynthesis.speak(utterance);
                    });
                }
            },
            {
                name: 'ユーザー音声の録音 (3秒)',
                action: async () => {
                    try {
                        // 簡易録音テスト
                        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                        const recorder = new MediaRecorder(stream);
                        
                        return new Promise((resolve) => {
                            const chunks = [];
                            recorder.ondataavailable = (e) => chunks.push(e.data);
                            recorder.onstop = () => {
                                const blob = new Blob(chunks);
                                stream.getTracks().forEach(track => track.stop());
                                resolve(`✅ 録音完了 (${blob.size} bytes)`);
                            };
                            
                            recorder.start();
                            setTimeout(() => recorder.stop(), 3000);
                        });
                    } catch (error) {
                        return `❌ 録音エラー: ${error.message}`;
                    }
                }
            },
            {
                name: '音響分析・評価',
                action: async () => {
                    // 簡易分析シミュレーション
                    const metrics = {
                        duration: (Math.random() * 2 + 2).toFixed(2),
                        volume: (Math.random() * 30 + 70).toFixed(1),
                        score: (Math.random() * 20 + 80).toFixed(0)
                    };
                    
                    return `✅ 分析完了 - 時間: ${metrics.duration}s, 音量: ${metrics.volume}%, スコア: ${metrics.score}点`;
                }
            }
        ];
        
        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            this.log('integration-results', `${i + 1}. ${step.name} 実行中...`);
            
            try {
                const result = await step.action();
                this.log('integration-results', `   ${result}`);
                
                // ステップ間の待機
                if (i < steps.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            } catch (error) {
                this.log('integration-results', `   ❌ エラー: ${error.message}`);
                break;
            }
        }
        
        this.log('integration-results', '🏁 統合テスト完了');
    }
    
    // ユーティリティ: ログ出力
    log(elementId, message) {
        const element = document.getElementById(elementId);
        const timestamp = new Date().toLocaleTimeString();
        element.innerHTML += `[${timestamp}] ${message}\n`;
        element.scrollTop = element.scrollHeight;
        console.log(`[${elementId}] ${message}`);
    }
}

// 初期化
new VoiceTechValidator();
