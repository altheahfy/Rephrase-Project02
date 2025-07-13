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
        
        this.init();
    }
    
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
        
        console.log('✅ 音声システム初期化完了');
    }
    
    /**
     * 現在表示されている全スロットのテキストを取得して完全な例文を作成
     */
    getCurrentSentence() {
        console.log('🔍 例文テキスト取得を開始...');
        
        // デバッグ: 利用可能なグローバル変数をチェック
        console.log('🔍 window.lastSelectedSlots:', window.lastSelectedSlots);
        console.log('🔍 window.loadedJsonData:', window.loadedJsonData ? '存在' : '未定義');
        console.log('🔍 window.fullSlotPool:', window.fullSlotPool ? '存在' : '未定義');
        
        // JSONデータから現在の例文を構築する方法を試す
        if (window.lastSelectedSlots && Array.isArray(window.lastSelectedSlots) && window.lastSelectedSlots.length > 0) {
            return this.buildSentenceFromJsonData();
        }
        
        console.log('⚠️ JSONデータが利用できません。DOMから取得を試行します。');
        // フォールバック: DOMから取得
        return this.buildSentenceFromDOM();
    }
    
    /**
     * JSONデータから例文を構築（推奨方法）
     */
    buildSentenceFromJsonData() {
        console.log('📊 JSONデータから例文を構築中...');
        console.log('利用可能なスロットデータ:', window.lastSelectedSlots);
        console.log('スロットデータの件数:', window.lastSelectedSlots.length);
        
        // データ構造の詳細ログ
        if (window.lastSelectedSlots.length > 0) {
            console.log('最初のスロットの構造:', window.lastSelectedSlots[0]);
            console.log('利用可能なキー:', Object.keys(window.lastSelectedSlots[0]));
        }
        
        const sentenceParts = [];
        
        // 疑問詞を最初にチェック
        const questionWordSlot = window.lastSelectedSlots.find(slot => 
            slot.Slot === 'question-word' || slot.Slot === 'WH' || slot.Slot === 'wh'
        );
        console.log('🔍 疑問詞スロット検索結果:', questionWordSlot);
        
        if (questionWordSlot && questionWordSlot.SlotPhrase) {
            console.log(`疑問詞: "${questionWordSlot.SlotPhrase}"`);
            sentenceParts.push({
                text: questionWordSlot.SlotPhrase,
                order: -1, // 疑問詞は最初
                slot: 'question-word'
            });
        }
        
        // 上位スロットを Slot_display_order 順にソート
        const upperSlots = window.lastSelectedSlots
            .filter(slot => !slot.SubslotID && slot.Slot !== 'question-word' && slot.Slot !== 'WH' && slot.Slot !== 'wh')
            .sort((a, b) => (a.Slot_display_order || 0) - (b.Slot_display_order || 0));
        
        console.log('� 上位スロットの順序:', upperSlots.map(slot => 
            `${slot.Slot}(order:${slot.Slot_display_order})`
        ));
        
        upperSlots.forEach(slot => {
            if (slot.SlotPhrase) {
                console.log(`${slot.Slot} (order:${slot.Slot_display_order}): "${slot.SlotPhrase}"`);
                sentenceParts.push({
                    text: slot.SlotPhrase,
                    order: slot.Slot_display_order || 0,
                    slot: slot.Slot
                });
            } else {
                console.log(`⚠️ ${slot.Slot} の上位スロットにSlotPhraseがありません。サブスロットを確認します。`);
                
                // このスロットのサブスロットから構築を試す
                const subSlots = window.lastSelectedSlots
                    .filter(subSlot => 
                        subSlot.SubslotID && subSlot.SubslotID.startsWith(slot.Slot + '-')
                    )
                    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
                
                console.log(`🔍 ${slot.Slot} のサブスロット順序:`, subSlots.map(subSlot => 
                    `${subSlot.Slot}(order:${subSlot.display_order})`
                ));
                
                if (subSlots.length > 0) {
                    const subSentenceParts = [];
                    
                    subSlots.forEach(subSlot => {
                        if (subSlot.SlotPhrase) {
                            console.log(`  ${subSlot.Slot} (サブ, order:${subSlot.display_order}): "${subSlot.SlotPhrase}"`);
                            subSentenceParts.push(subSlot.SlotPhrase);
                        }
                    });
                    
                    if (subSentenceParts.length > 0) {
                        const subSentence = subSentenceParts.join(' ');
                        console.log(`${slot.Slot} (サブスロットから): "${subSentence}"`);
                        sentenceParts.push({
                            text: subSentence,
                            order: slot.Slot_display_order || 0,
                            slot: slot.Slot
                        });
                    }
                }
            }
        });
        
        // 最終的に order でソートして例文を構築
        sentenceParts.sort((a, b) => a.order - b.order);
        
        const finalParts = sentenceParts.map(part => part.text);
        const sentence = finalParts.join(' ').trim();
        
        console.log(`📝 ソート後の順序:`, sentenceParts.map(part => 
            `${part.slot}(${part.order}): "${part.text}"`
        ));
        console.log(`📝 JSONから構築した例文: "${sentence}"`);
        console.log(`📝 例文パーツ数: ${finalParts.length}`);
        console.log(`📝 例文パーツ詳細:`, finalParts);
        
        if (sentence && !sentence.endsWith('.') && !sentence.endsWith('?') && !sentence.endsWith('!')) {
            return sentence + '.';
        }
        
        return sentence;
    }
    
    /**
     * DOMから例文を構築（フォールバック）
     */
    buildSentenceFromDOM() {
        console.log('🌐 DOMから例文を構築中...');
        
        const slotOrder = ['question-word', 'm1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
        const sentenceParts = [];
        
        // 疑問詞を最初にチェック（英語テキスト部分を取得）
        const questionWordElement = document.querySelector('#display-top-question-word .question-word-text');
        console.log('🔍 疑問詞要素:', questionWordElement);
        console.log('🔍 疑問詞テキスト:', questionWordElement ? questionWordElement.textContent : 'なし');
        
        if (questionWordElement && questionWordElement.textContent.trim()) {
            const text = questionWordElement.textContent.trim();
            console.log(`疑問詞: "${text}"`);
            sentenceParts.push(text);
        }
        
        // 各スロットの英語例文（slot-phrase）を順番に取得
        slotOrder.forEach(slotName => {
            if (slotName === 'question-word') return; // 既に処理済み
            
            // 上位スロットの英語例文を取得
            const slotElement = document.querySelector(`#slot-${slotName} .slot-phrase`);
            console.log(`🔍 ${slotName} .slot-phrase 要素:`, slotElement);
            console.log(`🔍 ${slotName} .slot-phrase テキスト:`, slotElement ? slotElement.textContent : 'なし');
            
            if (slotElement && slotElement.textContent.trim()) {
                const text = slotElement.textContent.trim();
                console.log(`${slotName}: "${text}"`);
                sentenceParts.push(text);
            } else {
                // .slot-text も試してみる
                const slotTextElement = document.querySelector(`#slot-${slotName} .slot-text`);
                console.log(`🔍 ${slotName} .slot-text 要素:`, slotTextElement);
                console.log(`🔍 ${slotName} .slot-text テキスト:`, slotTextElement ? slotTextElement.textContent : 'なし');
                
                if (slotTextElement && slotTextElement.textContent.trim()) {
                    const text = slotTextElement.textContent.trim();
                    console.log(`${slotName} (slot-text): "${text}"`);
                    sentenceParts.push(text);
                }
            }
        });
        
        const sentence = sentenceParts.join(' ').trim();
        console.log(`📝 DOMから構築した例文: "${sentence}"`);
        console.log(`📝 例文パーツ数: ${sentenceParts.length}`);
        console.log(`📝 例文パーツ詳細:`, sentenceParts);
        
        if (sentence && !sentence.endsWith('.') && !sentence.endsWith('?') && !sentence.endsWith('!')) {
            return sentence + '.';
        }
        
        return sentence;
    }
    
    /**
     * マイクアクセス許可を確認
     */
    async checkMicrophonePermission() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.isMicrophoneAllowed = true;
            stream.getTracks().forEach(track => track.stop()); // 即座に停止
            console.log('✅ マイクアクセス許可取得済み');
        } catch (error) {
            console.warn('⚠️ マイクアクセス許可が必要です:', error.message);
            this.isMicrophoneAllowed = false;
        }
    }
    
    /**
     * イベントリスナーを設定
     */
    setupEventListeners() {
        // 録音ボタン
        const recordBtn = document.getElementById('voice-record-btn');
        if (recordBtn) {
            recordBtn.addEventListener('click', () => this.toggleRecording());
        }
        
        // 再生ボタン
        const playBtn = document.getElementById('voice-play-btn');
        if (playBtn) {
            playBtn.addEventListener('click', () => this.playRecording());
        }
        
        // 音声合成ボタン
        const ttsBtn = document.getElementById('voice-tts-btn');
        if (ttsBtn) {
            ttsBtn.addEventListener('click', () => this.speakSentence());
        }
        
        // 停止ボタン
        const stopBtn = document.getElementById('voice-stop-btn');
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopAll());
        }
        
        // パネル開くボタン（トグル機能）
        const openBtn = document.getElementById('voice-panel-open-btn');
        if (openBtn) {
            openBtn.addEventListener('click', () => this.toggleVoicePanel());
        }
        
        // パネル閉じるボタン
        const closeBtn = document.getElementById('voice-panel-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hideVoicePanel());
        }
        
        // 学習進捗ボタン（動的に追加される可能性があるため遅延設定）
        this.setupProgressButtonListener();
    }
    
    /**
     * 進捗ボタンのイベントリスナーを設定（動的対応）
     */
    setupProgressButtonListener() {
        const setupButton = () => {
            const progressBtn = document.getElementById('voice-progress-btn');
            if (progressBtn && !progressBtn.hasAttribute('data-listener-added')) {
                progressBtn.addEventListener('click', () => this.showProgress());
                progressBtn.setAttribute('data-listener-added', 'true');
                console.log('✅ 学習進捗ボタンのイベントリスナーを設定しました');
                return true;
            }
            return false;
        };
        
        // 即座に試行
        if (!setupButton()) {
            // ボタンが見つからない場合、定期的にチェック
            let attempts = 0;
            const maxAttempts = 10;
            
            const checkInterval = setInterval(() => {
                attempts++;
                if (setupButton() || attempts >= maxAttempts) {
                    clearInterval(checkInterval);
                    if (attempts >= maxAttempts) {
                        console.warn('⚠️ 学習進捗ボタンが見つかりませんでした（最大試行回数に達しました）');
                    }
                }
            }, 500);
        }
    }
    
    /**
     * 録音開始/停止の切り替え
     */
    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }
    
    /**
     * 録音開始
     */
    async startRecording() {
        if (!this.isMicrophoneAllowed) {
            await this.checkMicrophonePermission();
            if (!this.isMicrophoneAllowed) {
                this.updateStatus('❌ マイクアクセスが許可されていません', 'error');
                return;
            }
        }
        
        try {
            // 🔧 前回の録音データと認識結果をクリア
            this.recordedBlob = null;
            this.recognizedText = '';
            
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 44100,
                    channelCount: 1,
                    volume: 1.0
                }
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            // 🔧 新しい録音用のチャンク配列を初期化
            const audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                // 🔧 新しいBlobとして確実に上書き
                this.recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
                console.log('🎤 新しい録音データ作成:', this.recordedBlob.size, 'bytes');
                
                this.stopVolumeMonitoring();
                stream.getTracks().forEach(track => track.stop());
                this.updateRecordingUI(false);
                
                // 🎯 録音完了時に即座に分析実行
                this.analyzeRecording();
            };
            
            // 録音開始
            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingStartTime = Date.now();
            
            // 🎤 音声認識も同時開始
            if (this.recognition && !this.isRecognitionActive) {
                try {
                    this.recognition.start();
                } catch (error) {
                    console.warn('⚠️ 音声認識開始失敗:', error.message);
                }
            }
            
            // UI更新
            this.updateRecordingUI(true);
            this.startRecordingTimer();
            this.setupVolumeMonitoring(stream);
            
            this.updateStatus('🎤 録音・認識開始...', 'recording');
            
        } catch (error) {
            console.error('録音開始エラー:', error);
            this.updateStatus(`❌ 録音エラー: ${error.message}`, 'error');
        }
    }
    
    /**
     * 録音停止
     */
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.stopRecordingTimer();
        }
        
        // 🎤 音声認識も停止
        if (this.recognition && this.isRecognitionActive) {
            try {
                this.recognition.stop();
            } catch (error) {
                console.warn('⚠️ 音声認識停止失敗:', error.message);
            }
        }
    }
    
    /**
     * 録音再生
     */
    playRecording() {
        if (!this.recordedBlob) {
            this.updateStatus('❌ 再生する録音がありません', 'error');
            return;
        }
        
        // 🔧 前回の再生を停止（既存のAudioオブジェクトをクリア）
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
        
        // 🔧 新しいBlobURLを作成（前回のを確実にクリア）
        const audioUrl = URL.createObjectURL(this.recordedBlob);
        this.currentAudio = new Audio(audioUrl);
        
        console.log('🔊 再生開始:', this.recordedBlob.size, 'bytes');
        
        this.currentAudio.onloadstart = () => this.updateStatus('🔊 録音再生中...', 'playing');
        this.currentAudio.onended = () => {
            this.updateStatus('✅ 再生完了', 'success');
            // 🔧 再生完了後にBlobURLを解放
            URL.revokeObjectURL(audioUrl);
            this.currentAudio = null;
        };
        this.currentAudio.onerror = () => {
            this.updateStatus('❌ 再生エラー', 'error');
            URL.revokeObjectURL(audioUrl);
            this.currentAudio = null;
        };
        
        this.currentAudio.play();
    }
    
    /**
     * 現在の例文を音声合成で読み上げ
     */
    speakSentence() {
        const sentence = this.getCurrentSentence();
        
        if (!sentence) {
            this.updateStatus('❌ 読み上げる例文がありません', 'error');
            return;
        }
        
        // 既存の音声を停止
        speechSynthesis.cancel();
        
        this.currentUtterance = new SpeechSynthesisUtterance(sentence);
        
        // 音声設定 - 女性の英語音声を優先選択
        const voices = speechSynthesis.getVoices();
        console.log('🔍 利用可能な音声一覧:', voices.map(v => `${v.name} (${v.lang}) - ${v.gender || 'unknown'}`));
        
        // 女性の英語音声を最優先で探す
        let selectedVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.toLowerCase().includes('female') || 
             voice.name.toLowerCase().includes('woman') ||
             voice.name.toLowerCase().includes('zira') ||  // Microsoft Zira (女性)
             voice.name.toLowerCase().includes('hazel') || // Microsoft Hazel (女性)
             voice.name.toLowerCase().includes('samantha') || // macOS Samantha (女性)
             voice.name.toLowerCase().includes('karen') ||    // macOS Karen (女性)
             voice.name.toLowerCase().includes('anna') ||     // Anna (女性)
             voice.name.toLowerCase().includes('linda') ||    // Linda (女性)
             voice.name.toLowerCase().includes('heather'))    // Heather (女性)
        );
        
        // 女性音声が見つからない場合は、一般的な英語音声を選択
        if (!selectedVoice) {
            selectedVoice = voices.find(voice => voice.lang.startsWith('en'));
        }
        
        if (selectedVoice) {
            this.currentUtterance.voice = selectedVoice;
            console.log(`🗣️ 選択された音声: ${selectedVoice.name} (${selectedVoice.lang})`);
        } else {
            console.log('⚠️ 英語音声が見つかりません。デフォルト音声を使用します。');
        }
        
        this.currentUtterance.rate = 0.8; // 少しゆっくり
        this.currentUtterance.pitch = 1.0;
        this.currentUtterance.volume = 1.0;
        
        // イベントハンドラー
        this.currentUtterance.onstart = () => {
            this.updateStatus(`🔊 読み上げ中: "${sentence}"`, 'speaking');
        };
        
        this.currentUtterance.onend = () => {
            this.updateStatus('✅ 読み上げ完了', 'success');
        };
        
        this.currentUtterance.onerror = (event) => {
            this.updateStatus(`❌ 読み上げエラー: ${event.error}`, 'error');
        };
        
        speechSynthesis.speak(this.currentUtterance);
    }
    
    /**
     * すべての音声を停止
     */
    stopAll() {
        // 録音停止
        if (this.isRecording) {
            this.stopRecording();
        }
        
        // 🔧 録音再生停止
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
        
        // 音声合成停止
        speechSynthesis.cancel();
        
        // 🎤 音声認識停止
        if (this.recognition && this.isRecognitionActive) {
            try {
                this.recognition.stop();
            } catch (error) {
                console.warn('⚠️ 音声認識停止失敗:', error.message);
            }
        }
        
        // ボリュームモニタリング停止
        this.stopVolumeMonitoring();
        
        this.updateStatus('⏹️ すべて停止', 'stopped');
    }
    
    /**
     * 録音の分析（リアルタイム音声認識結果を使用）
     */
    async analyzeRecording() {
        if (!this.recordedBlob) {
            this.updateStatus('❌ 分析する録音がありません', 'error');
            return;
        }
        
        try {
            this.updateStatus('📊 分析中...', 'analyzing');
            
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            const audioContext = new AudioContextClass();
            
            const arrayBuffer = await this.recordedBlob.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            // 期待される文章を取得
            const expectedSentence = this.getCurrentSentence();
            const recognizedText = this.recognizedText.trim();
            
            console.log('� 期待文章:', expectedSentence);
            console.log('🎯 認識結果:', recognizedText);
            
            // 音声品質チェック（最低限のみ）
            const qualityCheck = this.checkAudioQuality(audioBuffer);
            
            let analysisResult;
            
            if (!qualityCheck.isAcceptable) {
                // 音質が悪すぎる場合
                analysisResult = {
                    level: '❌ 音質不良',
                    levelExplanation: '録音品質が悪すぎて判定できません',
                    expectedSentence,
                    recognizedText: '',
                    contentAccuracy: 0,
                    verificationStatus: '音質不良により判定不可',
                    duration: audioBuffer.duration,
                    qualityIssue: qualityCheck.issue
                };
            } else if (!recognizedText || recognizedText.length === 0) {
                // 音声認識結果がない場合
                analysisResult = {
                    level: '❌ 音声未検出',
                    levelExplanation: '音声が認識されませんでした',
                    expectedSentence,
                    recognizedText: '',
                    contentAccuracy: 0,
                    verificationStatus: '音声認識失敗',
                    duration: audioBuffer.duration
                };
            } else {
                // 正常に認識された場合の分析
                const similarity = this.calculateTextSimilarity(expectedSentence, recognizedText);
                const duration = audioBuffer.duration;
                const expectedWordCount = expectedSentence ? expectedSentence.trim().split(/\s+/).length : 0;
                const actualWordCount = recognizedText.split(/\s+/).length;
                const wordsPerSecond = actualWordCount / duration;
                const wordsPerMinute = wordsPerSecond * 60;
                
                let level, levelExplanation, verificationStatus;
                
                if (similarity < 0.3) {
                    level = '❌ 内容不一致';
                    levelExplanation = '発話内容が大きく異なります';
                    verificationStatus = '内容要確認';
                } else if (similarity < 0.6) {
                    level = '⚠️ 内容要改善';
                    levelExplanation = '発話内容に改善の余地があります';
                    verificationStatus = '部分的一致';
                } else {
                    // 内容が正しい場合のレベル評価
                    if (wordsPerSecond < 1.33) {
                        level = '🐌 初心者レベル';
                        levelExplanation = '(80語/分以下)';
                    } else if (wordsPerSecond < 2.17) {
                        level = '📈 中級者レベル';
                        levelExplanation = '(130語/分以下)';
                    } else if (wordsPerSecond < 2.5) {
                        level = '🚀 上級者レベル';
                        levelExplanation = '(150語/分以下)';
                    } else {
                        level = '⚡ 達人レベル';
                        levelExplanation = '(150語/分超)';
                    }
                    verificationStatus = '内容一致確認';
                }
                
                analysisResult = {
                    duration,
                    expectedWordCount,
                    actualWordCount,
                    wordsPerSecond,
                    wordsPerMinute,
                    level,
                    levelExplanation,
                    expectedSentence,
                    recognizedText,
                    contentAccuracy: similarity,
                    verificationStatus
                };
            }
            
            this.displayAnalysisResults(analysisResult);
            await audioContext.close();
            
        } catch (error) {
            console.error('分析エラー:', error);
            this.updateStatus(`❌ 分析エラー: ${error.message}`, 'error');
        }
    }
    
    /**
     * 音響分析を実行（内容検証機能付き）
     */
    async performAcousticAnalysis(audioBuffer) {
        const duration = audioBuffer.duration;
        const sampleRate = audioBuffer.sampleRate;
        const channelData = audioBuffer.getChannelData(0);
        
        // 音量分析
        let sumSquared = 0;
        let maxAmplitude = 0;
        
        for (let i = 0; i < channelData.length; i++) {
            const amplitude = Math.abs(channelData[i]);
            sumSquared += amplitude * amplitude;
            maxAmplitude = Math.max(maxAmplitude, amplitude);
        }
        
        const rmsAmplitude = Math.sqrt(sumSquared / channelData.length);
        const averageVolume = rmsAmplitude * 100;
        
        // 期待される文章を取得
        const expectedSentence = this.getCurrentSentence();
        const expectedWordCount = expectedSentence ? expectedSentence.trim().split(/\s+/).length : 0;
        
        // 🔍 音声認識による内容検証を試行
        let recognizedText = '';
        let contentAccuracy = 0.8; // デフォルトを音声認識なしでも妥当な値に設定
        let verificationStatus = '時間ベース評価';
        let recognitionError = '';
        
        console.log('🔍 音声内容の評価を開始...');
        console.log('📊 期待文章:', expectedSentence);
        
        // 🎯 改良: 音声認識は試行するが、エラー時は時間ベース評価を使用
        console.log('⚠️ 注意: Web Speech APIの制限により、録音データからの直接音声認識は技術的に困難です');
        console.log('🔄 代替として、録音時間と音声品質による評価を実行します');
        
        // 🔄 時間ベース + 音質ベースの包括的評価
        const durationBasedAccuracy = this.calculateDurationBasedAccuracy(duration, expectedWordCount);
        const qualityBasedAccuracy = this.calculateAudioQualityScore(averageVolume, maxAmplitude, duration);
        
        console.log(`📊 時間ベース妥当性: ${(durationBasedAccuracy * 100).toFixed(1)}%`);
        console.log(`📊 音質ベース妥当性: ${(qualityBasedAccuracy * 100).toFixed(1)}%`);
        
        // 時間と音質を組み合わせた総合評価
        contentAccuracy = (durationBasedAccuracy * 0.7) + (qualityBasedAccuracy * 0.3);
        
        if (contentAccuracy >= 0.8) {
            verificationStatus = '高品質発話 (時間・音質良好)';
        } else if (contentAccuracy >= 0.6) {
            verificationStatus = '標準品質発話 (時間・音質普通)';
        } else if (contentAccuracy >= 0.4) {
            verificationStatus = '要改善発話 (時間・音質に課題)';
        } else {
            verificationStatus = '不適切発話 (時間・音質不良)';
        }
        
        // 🎯 オプション: 将来的な音声認識の実装準備
        if (false) { // 現在は無効化
            try {
                console.log('🔬 実験的音声認識を試行中...');
                recognizedText = await this.recognizeSpeechFromBlob(this.recordedBlob);
                
                if (recognizedText && recognizedText.trim().length > 0) {
                    const speechAccuracy = this.calculateTextSimilarity(expectedSentence, recognizedText);
                    contentAccuracy = (contentAccuracy * 0.4) + (speechAccuracy * 0.6); // 音声認識結果を重視
                    verificationStatus = speechAccuracy >= 0.7 ? '内容一致確認' : '内容要確認';
                    console.log(`✅ 音声認識成功 - 内容一致度: ${(speechAccuracy * 100).toFixed(1)}%`);
                }
            } catch (error) {
                console.log('ℹ️ 音声認識は利用できませんが、時間・音質ベース評価で継続します');
                recognitionError = `音声認識未対応 (${error.message})`;
            }
        } else {
            recognitionError = '音声認識は現在無効化されています (時間・音質ベース評価を使用)';
        }
        
        // 発話速度分析（認識された内容または期待される内容を使用）
        let actualWordCount = expectedWordCount;
        if (recognizedText && contentAccuracy >= 0.5) {
            actualWordCount = recognizedText.trim().split(/\s+/).length;
        }
        
        const wordsPerSecond = actualWordCount / duration;
        const wordsPerMinute = wordsPerSecond * 60;
        
        // 🎯 改良された評価システム
        let level = '';
        let levelExplanation = '';
        
        if (contentAccuracy < 0.5) {
            level = '❌ 内容不一致';
            levelExplanation = '発話内容が期待される文章と大きく異なります';
        } else if (contentAccuracy < 0.7) {
            level = '⚠️ 内容要改善';
            levelExplanation = '発話内容に改善の余地があります';
        } else {
            // 内容が正しい場合のみ速度評価
            const adjustedSpeed = wordsPerSecond * contentAccuracy; // 精度で補正
            
            if (adjustedSpeed < 1.33) {
                level = '🐌 初心者レベル';
                levelExplanation = '(80語/分以下)';
            } else if (adjustedSpeed < 2.17) {
                level = '📈 中級者レベル';
                levelExplanation = '(130語/分以下)';
            } else if (adjustedSpeed < 2.5) {
                level = '🚀 上級者レベル';
                levelExplanation = '(150語/分以下)';
            } else {
                level = '⚡ 達人レベル';
                levelExplanation = '(150語/分超)';
            }
        }
        
        return {
            duration,
            sampleRate,
            averageVolume,
            maxAmplitude: maxAmplitude * 100,
            expectedWordCount,
            actualWordCount,
            wordsPerSecond,
            wordsPerMinute,
            level,
            levelExplanation,
            expectedSentence,
            recognizedText,
            contentAccuracy,
            verificationStatus,
            recognitionError
        };
    }

    /**
     * 音声品質の基本チェック（録音品質が悪すぎる場合のみ判定）
     */
    checkAudioQuality(audioBuffer) {
        const channelData = audioBuffer.getChannelData(0);
        const duration = audioBuffer.duration;
        
        // 音量分析
        let sumSquared = 0;
        let maxAmplitude = 0;
        
        for (let i = 0; i < channelData.length; i++) {
            const amplitude = Math.abs(channelData[i]);
            sumSquared += amplitude * amplitude;
            maxAmplitude = Math.max(maxAmplitude, amplitude);
        }
        
        const rmsAmplitude = Math.sqrt(sumSquared / channelData.length);
        const averageVolume = rmsAmplitude * 100;
        
        // 録音品質が悪すぎる場合のみチェック
        if (duration < 0.3) {
            return {
                isAcceptable: false,
                issue: '録音時間が短すぎます（0.3秒未満）'
            };
        }
        
        if (averageVolume < 0.1) {
            return {
                isAcceptable: false,
                issue: '音量が極めて低く、音声が検出されません'
            };
        }
        
        if (maxAmplitude < 0.001) {
            return {
                isAcceptable: false,
                issue: '音声信号が検出されません'
            };
        }
        
        return {
            isAcceptable: true
        };
    }
    
    /**
     * 録音時間から内容の妥当性を推定（音声認識の代替手段）
     */
    calculateDurationBasedAccuracy(actualDuration, expectedWordCount) {
        // 一般的な発話速度の範囲
        // 初心者: 1-2語/秒, 中級者: 2-3語/秒, 上級者: 3-4語/秒, 達人: 4-5語/秒
        const minWordsPerSecond = 0.5; // 最低速度
        const maxWordsPerSecond = 6.0;  // 最高速度
        
        const minExpectedDuration = expectedWordCount / maxWordsPerSecond; // 最短時間
        const maxExpectedDuration = expectedWordCount / minWordsPerSecond; // 最長時間
        
        console.log(`⏰ 期待時間範囲: ${minExpectedDuration.toFixed(2)}秒 - ${maxExpectedDuration.toFixed(2)}秒`);
        console.log(`⏰ 実際の時間: ${actualDuration.toFixed(2)}秒`);
        
        if (actualDuration >= minExpectedDuration && actualDuration <= maxExpectedDuration) {
            // 妥当な範囲内
            return 1.0;
        } else if (actualDuration < minExpectedDuration) {
            // 短すぎる（早口すぎる、または内容不足）
            const ratio = actualDuration / minExpectedDuration;
            return Math.max(0, ratio); // 0-1の範囲
        } else {
            // 長すぎる（遅すぎる、または無関係な発話）
            const ratio = maxExpectedDuration / actualDuration;
            return Math.max(0, ratio); // 0-1の範囲
        }
    }

    /**
     * 音声品質によるスコア計算
     */
    calculateAudioQualityScore(averageVolume, maxAmplitude, duration) {
        console.log(`🔊 音質評価開始:`);
        console.log(`📊 平均音量: ${averageVolume.toFixed(2)}`);
        console.log(`📊 最大振幅: ${maxAmplitude.toFixed(2)}`);
        console.log(`📊 録音時間: ${duration.toFixed(2)}秒`);
        
        let qualityScore = 1.0;
        
        // 1. 音量レベルの評価
        let volumeScore = 1.0;
        if (averageVolume < 1.0) {
            volumeScore = 0.3; // 音量が低すぎる
            console.log('⚠️ 音量が低すぎます (マイクに近づいてください)');
        } else if (averageVolume < 5.0) {
            volumeScore = 0.6; // やや低い音量
            console.log('📢 音量がやや低めです');
        } else if (averageVolume > 50.0) {
            volumeScore = 0.7; // 音量が高すぎる
            console.log('⚠️ 音量が高すぎます (マイクから離れてください)');
        } else {
            volumeScore = 1.0; // 適切な音量
            console.log('✅ 音量レベル良好');
        }
        
        // 2. 録音時間の評価
        let durationScore = 1.0;
        if (duration < 0.5) {
            durationScore = 0.2; // 短すぎる
            console.log('⚠️ 録音時間が短すぎます');
        } else if (duration < 1.0) {
            durationScore = 0.5; // やや短い
            console.log('📏 録音時間がやや短めです');
        } else if (duration > 20.0) {
            durationScore = 0.6; // 長すぎる
            console.log('⚠️ 録音時間が長すぎます');
        } else {
            console.log('✅ 録音時間適切');
        }
        
        // 3. 音声の動的範囲（ダイナミックレンジ）
        let dynamicRangeScore = 1.0;
        const dynamicRange = maxAmplitude - (averageVolume / 100);
        if (dynamicRange < 10) {
            dynamicRangeScore = 0.7; // 単調な音声
            console.log('📊 音声の変化が少ないです');
        } else {
            console.log('✅ 音声の変化良好');
        }
        
        // 総合音質スコア
        qualityScore = (volumeScore * 0.5) + (durationScore * 0.3) + (dynamicRangeScore * 0.2);
        
        console.log(`📊 音量スコア: ${(volumeScore * 100).toFixed(1)}%`);
        console.log(`📊 時間スコア: ${(durationScore * 100).toFixed(1)}%`);
        console.log(`📊 変化スコア: ${(dynamicRangeScore * 100).toFixed(1)}%`);
        console.log(`📊 総合音質スコア: ${(qualityScore * 100).toFixed(1)}%`);
        
        return qualityScore;
    }
    
    /**
     * 分析結果を表示（簡潔版）
     */
    async displayAnalysisResults(analysis) {
        let contentVerificationHtml = '';
        
        if (analysis.qualityIssue) {
            // 音質不良の場合
            contentVerificationHtml = `
                <div class="content-verification">
                    <div class="verification-item poor"><strong>品質問題:</strong> ${analysis.qualityIssue}</div>
                </div>
            `;
        } else if (!analysis.recognizedText) {
            // 音声認識失敗の場合
            contentVerificationHtml = `
                <div class="content-verification">
                    <div class="verification-item poor"><strong>認識失敗:</strong> 音声が認識されませんでした</div>
                    <div class="verification-item info"><strong>期待文章:</strong> "${analysis.expectedSentence}"</div>
                </div>
            `;
        } else {
            // 正常認識の場合
            const accuracyClass = analysis.contentAccuracy >= 0.6 ? 'good' : 
                                 analysis.contentAccuracy >= 0.3 ? 'fair' : 'poor';
            
            contentVerificationHtml = `
                <div class="content-verification">
                    <div class="verification-item"><strong>期待文章:</strong> "${analysis.expectedSentence}"</div>
                    <div class="verification-item"><strong>認識結果:</strong> "${analysis.recognizedText}"</div>
                    <div class="verification-item ${accuracyClass}"><strong>一致度:</strong> ${(analysis.contentAccuracy * 100).toFixed(1)}%</div>
                </div>
            `;
        }
        
        const resultsHtml = `
            <div class="analysis-results">
                <h4>📊 発話分析結果</h4>
                <div class="analysis-item">⏱️ 録音時間: ${analysis.duration.toFixed(2)}秒</div>
                <div class="analysis-item">💬 単語数: ${analysis.expectedWordCount || 0} → ${analysis.actualWordCount || 0}</div>
                <div class="analysis-item">⚡ 発話速度: ${(analysis.wordsPerMinute || 0).toFixed(0)} 語/分</div>
                <div class="analysis-item">🎯 評価: ${analysis.level} ${analysis.levelExplanation || ''}</div>
                ${contentVerificationHtml}
                <div class="progress-save-status">
                    <div id="progress-save-message">📊 進捗データを保存中...</div>
                </div>
            </div>
        `;
        
        const resultsContainer = document.getElementById('voice-analysis-results');
        if (resultsContainer) {
            resultsContainer.innerHTML = resultsHtml;
        }
        
        // 🎯 進捗追跡システムにデータを自動保存
        await this.saveProgressData(analysis);
        
        this.updateStatus('✅ 分析完了', 'success');
    }
    
    /**
     * 分析結果を進捗追跡システムに保存
     */
    async saveProgressData(analysisResult) {
        try {
            // 進捗追跡システムが利用可能かチェック
            if (!window.voiceProgressTracker || !window.voiceProgressTracker.db) {
                console.log('⚠️ 進捗追跡システムが利用できません');
                const messageElement = document.getElementById('progress-save-message');
                if (messageElement) {
                    messageElement.innerHTML = '⚠️ 進捗追跡システムが無効です';
                }
                return;
            }
            
            console.log('💾 進捗データ保存開始:', analysisResult);
            
            // 分析結果を保存
            const savedSession = await window.voiceProgressTracker.saveVoiceSession(analysisResult);
            
            console.log('✅ 進捗データ保存完了:', savedSession);
            
            // UI更新
            const messageElement = document.getElementById('progress-save-message');
            if (messageElement) {
                messageElement.innerHTML = '✅ 進捗データを保存しました';
                messageElement.style.color = '#28a745';
            }
            
            // 進捗表示ボタンを表示（まだ存在しない場合）
            this.showProgressButton();
            
        } catch (error) {
            console.error('❌ 進捗データ保存失敗:', error);
            
            const messageElement = document.getElementById('progress-save-message');
            if (messageElement) {
                messageElement.innerHTML = '❌ 進捗データ保存失敗';
                messageElement.style.color = '#dc3545';
            }
        }
    }
    
    /**
     * 進捗表示ボタンを音声パネルに追加
     */
    showProgressButton() {
        // 既にボタンが存在するかチェック
        if (document.getElementById('voice-progress-btn')) {
            return;
        }
        
        // ボタンを作成
        const progressButton = document.createElement('button');
        progressButton.id = 'voice-progress-btn';
        progressButton.innerHTML = '📊 進捗表示';
        progressButton.className = 'voice-btn secondary';
        progressButton.style.marginTop = '10px';
        progressButton.style.width = '100%';
        
        // イベントリスナーを追加
        progressButton.addEventListener('click', () => {
            if (window.voiceProgressUI) {
                window.voiceProgressUI.showProgressPanel();
            } else {
                alert('⚠️ 進捗表示システムが初期化されていません');
            }
        });
        
        // 音声分析結果エリアに追加
        const resultsContainer = document.getElementById('voice-analysis-results');
        if (resultsContainer) {
            resultsContainer.appendChild(progressButton);
        }
    }

    /**
     * 音声認識でBlobから文章を認識（修正版）
     */
    async recognizeSpeechFromBlob(audioBlob) {
        console.log('🎤 音声認識処理開始...');
        console.log('📊 音声Blobサイズ:', audioBlob.size, 'bytes');
        console.log('📊 音声Blobタイプ:', audioBlob.type);
        
        return new Promise((resolve, reject) => {
            // 🔍 ブラウザサポート確認
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            
            if (!SpeechRecognition) {
                console.error('❌ このブラウザは音声認識をサポートしていません');
                reject(new Error('このブラウザは音声認識をサポートしていません'));
                return;
            }
            
            console.log('✅ SpeechRecognition API利用可能');
            
            // 🎵 修正: Web Speech APIは録音データを直接処理できないため、
            // より確実な方法として、録音データを無音で再生しながらマイクで認識
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.maxAlternatives = 5; // より多くの候補を取得
            
            let timeoutId = null;
            let hasResult = false;
            let audioUrl = null;
            let audio = null;
            
            console.log('🔧 音声認識設定完了');
            console.log('📍 言語設定:', recognition.lang);
            console.log('📍 最大候補数:', recognition.maxAlternatives);
            
            // 🎯 代替方法: MediaSource APIを使用した音声データの直接処理を試行
            this.tryDirectAudioRecognition(audioBlob)
                .then(result => {
                    console.log('✅ 直接音声認識成功:', result);
                    resolve(result);
                })
                .catch(directError => {
                    console.log('⚠️ 直接音声認識失敗、フォールバック方式を使用:', directError.message);
                    
                    // フォールバック: 従来の方法だが改良版
                    recognition.onstart = () => {
                        console.log('🎤 音声認識開始...');
                        console.log('⏰ 15秒のタイムアウトを設定');
                        timeoutId = setTimeout(() => {
                            console.log('⏰ 音声認識タイムアウト');
                            recognition.stop();
                            if (audio) {
                                audio.pause();
                                URL.revokeObjectURL(audioUrl);
                            }
                            if (!hasResult) {
                                reject(new Error('音声認識タイムアウト (15秒)'));
                            }
                        }, 15000);
                    };
                    
                    recognition.onresult = (event) => {
                        console.log('🎯 音声認識結果受信!');
                        if (timeoutId) clearTimeout(timeoutId);
                        hasResult = true;
                        
                        if (audio) {
                            audio.pause();
                            URL.revokeObjectURL(audioUrl);
                        }
                        
                        console.log('📊 認識結果数:', event.results.length);
                        
                        // すべての候補を詳細ログ出力
                        for (let i = 0; i < event.results.length; i++) {
                            console.log(`📝 結果グループ${i+1}:`, event.results[i]);
                            for (let j = 0; j < event.results[i].length; j++) {
                                const alternative = event.results[i][j];
                                console.log(`  - 候補${j+1}: "${alternative.transcript}" (信頼度: ${(alternative.confidence * 100).toFixed(1)}%)`);
                            }
                        }
                        
                        if (event.results.length > 0 && event.results[0].length > 0) {
                            // 最も信頼度の高い結果を選択
                            let bestResult = event.results[0][0];
                            let bestConfidence = bestResult.confidence || 0;
                            
                            // 全候補から最高信頼度を探す
                            for (let i = 0; i < event.results.length; i++) {
                                for (let j = 0; j < event.results[i].length; j++) {
                                    const alternative = event.results[i][j];
                                    const confidence = alternative.confidence || 0;
                                    if (confidence > bestConfidence) {
                                        bestResult = alternative;
                                        bestConfidence = confidence;
                                    }
                                }
                            }
                            
                            console.log(`✅ 最終選択結果: "${bestResult.transcript}" (信頼度: ${(bestConfidence * 100).toFixed(1)}%)`);
                            resolve(bestResult.transcript);
                        } else {
                            console.log('⚠️ 音声認識結果が空です');
                            reject(new Error('音声認識結果が空です'));
                        }
                    };
                    
                    recognition.onerror = (event) => {
                        console.error('❌ 音声認識エラー発生:', event);
                        console.error('エラータイプ:', event.error);
                        
                        if (timeoutId) clearTimeout(timeoutId);
                        if (audio) {
                            audio.pause();
                            URL.revokeObjectURL(audioUrl);
                        }
                        
                        let errorMessage = '音声認識エラー';
                        switch (event.error) {
                            case 'no-speech':
                                errorMessage = '音声が検出されませんでした';
                                break;
                            case 'audio-capture':
                                errorMessage = '音声キャプチャエラー';
                                break;
                            case 'not-allowed':
                                errorMessage = 'マイクアクセスが許可されていません';
                                break;
                            case 'network':
                                errorMessage = 'ネットワークエラー';
                                break;
                            case 'service-not-allowed':
                                errorMessage = '音声認識サービスが許可されていません';
                                break;
                            default:
                                errorMessage = `音声認識エラー: ${event.error}`;
                        }
                        
                        reject(new Error(errorMessage));
                    };
                    
                    recognition.onend = () => {
                        console.log('🔚 音声認識処理終了');
                        if (timeoutId) clearTimeout(timeoutId);
                        if (audio) {
                            audio.pause();
                            URL.revokeObjectURL(audioUrl);
                        }
                        
                        if (!hasResult) {
                            console.log('⚠️ 結果なしで音声認識が終了しました');
                            reject(new Error('音声認識結果なし'));
                        }
                    };
                    
                    // 🔊 録音音声を小音量で再生しながら認識開始
                    try {
                        console.log('🔊 録音音声の再生準備...');
                        audioUrl = URL.createObjectURL(audioBlob);
                        audio = new Audio(audioUrl);
                        
                        // 音量を最小に設定（スピーカーからの音漏れを防止）
                        audio.volume = 0.1;
                        audio.muted = false; // 完全にミュートすると認識されない
                        
                        audio.oncanplaythrough = () => {
                            console.log('🔊 音声再生準備完了、音声認識開始');
                            try {
                                recognition.start();
                                audio.play();
                            } catch (startError) {
                                console.error('❌ 音声認識開始エラー:', startError);
                                reject(new Error(`音声認識開始失敗: ${startError.message}`));
                            }
                        };
                        
                        audio.onerror = (error) => {
                            console.error('🔊 音声再生エラー:', error);
                            reject(new Error('音声再生エラー'));
                        };
                        
                        // 音声ファイル読み込み開始
                        audio.load();
                        
                    } catch (error) {
                        console.error('❌ 音声再生+認識の初期化エラー:', error);
                        reject(new Error(`初期化エラー: ${error.message}`));
                    }
                });
        });
    }

    /**
     * 直接音声認識を試行（実験的）
     */
    async tryDirectAudioRecognition(audioBlob) {
        // 🔬 実験: より高度な音声認識手法
        // 注意: この方法は全てのブラウザでサポートされていない可能性があります
        
        return new Promise((resolve, reject) => {
            try {
                // AudioContext を使用して音声データを解析
                const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                const audioContext = new AudioContextClass();
                
                audioBlob.arrayBuffer().then(arrayBuffer => {
                    return audioContext.decodeAudioData(arrayBuffer);
                }).then(audioBuffer => {
                    console.log('🔬 AudioBuffer取得成功');
                    console.log('📊 サンプルレート:', audioBuffer.sampleRate);
                    console.log('📊 チャンネル数:', audioBuffer.numberOfChannels);
                    console.log('📊 長さ:', audioBuffer.duration, '秒');
                    
                    // 🎯 より高品質な音声認識のため、AudioBufferを最適化
                    const optimizedBuffer = this.optimizeAudioForRecognition(audioBuffer, audioContext);
                    
                    // AudioBufferからBlobを再作成
                    this.audioBufferToBlob(optimizedBuffer, audioContext)
                        .then(optimizedBlob => {
                            console.log('✅ 音声最適化完了');
                            // 最適化された音声で再度認識を試行
                            reject(new Error('直接認識は現在開発中です'));
                        })
                        .catch(error => {
                            reject(error);
                        });
                    
                }).catch(error => {
                    console.error('AudioBuffer生成エラー:', error);
                    reject(error);
                });
                
            } catch (error) {
                console.error('直接音声認識エラー:', error);
                reject(error);
            }
        });
    }

    /**
     * 音声認識用に音声を最適化
     */
    optimizeAudioForRecognition(audioBuffer, audioContext) {
        // 🔧 音声認識精度向上のための処理
        const sampleRate = audioBuffer.sampleRate;
        const length = audioBuffer.length;
        const numberOfChannels = Math.min(audioBuffer.numberOfChannels, 1); // モノラルに統一
        
        // 新しいバッファを作成
        const optimizedBuffer = audioContext.createBuffer(numberOfChannels, length, sampleRate);
        
        // チャンネルデータをコピー（ノイズ除去、音量正規化）
        for (let channel = 0; channel < numberOfChannels; channel++) {
            const inputData = audioBuffer.getChannelData(channel);
            const outputData = optimizedBuffer.getChannelData(channel);
            
            // 音量正規化とノイズ除去
            let maxAmplitude = 0;
            for (let i = 0; i < length; i++) {
                maxAmplitude = Math.max(maxAmplitude, Math.abs(inputData[i]));
            }
            
            const normalizationFactor = maxAmplitude > 0 ? 0.8 / maxAmplitude : 1;
            
            for (let i = 0; i < length; i++) {
                let sample = inputData[i] * normalizationFactor;
                
                // 簡単なノイズゲート（小さすぎる信号をカット）
                if (Math.abs(sample) < 0.01) {
                    sample = 0;
                }
                
                outputData[i] = sample;
            }
        }
        
        return optimizedBuffer;
    }

    /**
     * AudioBufferをBlobに変換
     */
    async audioBufferToBlob(audioBuffer, audioContext) {
        // この機能は現在開発中です
        return Promise.reject(new Error('AudioBuffer to Blob 変換は現在開発中です'));
    }

    /**
     * 2つのテキストの類似度を計算（改良版）
     */
    calculateTextSimilarity(expected, actual) {
        if (!expected || !actual) return 0;
        
        console.log('🔍 類似度計算開始');
        console.log('期待文章:', expected);
        console.log('実際文章:', actual);
        
        // 大文字小文字を統一し、句読点を除去して正規化
        const normalizeText = (text) => {
            return text.toLowerCase()
                      .replace(/[^\w\s]/g, '') // 句読点除去
                      .replace(/\s+/g, ' ')    // 複数スペースを1つに
                      .trim()
                      .split(/\s+/);
        };
        
        const expectedWords = normalizeText(expected);
        const actualWords = normalizeText(actual);
        
        console.log('🔍 正規化後の期待単語:', expectedWords);
        console.log('🔍 正規化後の実際単語:', actualWords);
        
        // 🎯 複数の類似度指標を計算して総合評価
        
        // 1. 単語レベルの一致度（Jaccard係数）
        const expectedSet = new Set(expectedWords);
        const actualSet = new Set(actualWords);
        
        const intersection = new Set([...expectedSet].filter(x => actualSet.has(x)));
        const union = new Set([...expectedSet, ...actualSet]);
        
        const jaccardSimilarity = union.size > 0 ? intersection.size / union.size : 0;
        console.log(`📊 Jaccard類似度: ${(jaccardSimilarity * 100).toFixed(1)}%`);
        console.log(`📊 一致単語:`, [...intersection]);
        
        // 2. 順序を考慮した類似度（Longest Common Subsequence）
        const lcsSimilarity = this.calculateLCS(expectedWords, actualWords);
        console.log(`📊 LCS類似度: ${(lcsSimilarity * 100).toFixed(1)}%`);
        
        // 3. 編集距離ベースの類似度（Levenshtein距離）
        const editSimilarity = this.calculateEditSimilarity(expected, actual);
        console.log(`📊 編集距離類似度: ${(editSimilarity * 100).toFixed(1)}%`);
        
        // 4. 部分文字列の一致度
        const substringMatch = this.calculateSubstringMatch(expectedWords, actualWords);
        console.log(`📊 部分一致度: ${(substringMatch * 100).toFixed(1)}%`);
        
        // 🎯 重み付き総合評価
        const weights = {
            jaccard: 0.3,      // 単語の重複
            lcs: 0.25,         // 順序の重要性
            edit: 0.25,        // 全体的な類似性
            substring: 0.2     // 部分一致
        };
        
        const weightedSimilarity = 
            (jaccardSimilarity * weights.jaccard) +
            (lcsSimilarity * weights.lcs) +
            (editSimilarity * weights.edit) +
            (substringMatch * weights.substring);
        
        // 🔧 長さ補正を適用
        const lengthRatio = Math.min(expectedWords.length, actualWords.length) / 
                           Math.max(expectedWords.length, actualWords.length);
        const lengthPenalty = 1 - Math.abs(1 - lengthRatio) * 0.3; // 長さ差によるペナルティを緩和
        
        const finalSimilarity = Math.max(0, Math.min(1, weightedSimilarity * lengthPenalty));
        
        console.log(`📊 重み付き類似度: ${(weightedSimilarity * 100).toFixed(1)}%`);
        console.log(`📊 長さ補正係数: ${(lengthPenalty * 100).toFixed(1)}%`);
        console.log(`📊 最終類似度: ${(finalSimilarity * 100).toFixed(1)}%`);
        
        return finalSimilarity;
    }

    /**
     * Longest Common Subsequence による類似度計算
     */
    calculateLCS(arr1, arr2) {
        if (arr1.length === 0 || arr2.length === 0) return 0;
        
        const m = arr1.length;
        const n = arr2.length;
        const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));
        
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (arr1[i-1] === arr2[j-1]) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        
        const lcsLength = dp[m][n];
        const maxLength = Math.max(m, n);
        
        return maxLength > 0 ? lcsLength / maxLength : 0;
    }

    /**
     * 編集距離による類似度計算
     */
    calculateEditSimilarity(str1, str2) {
        const editDistance = this.levenshteinDistance(str1.toLowerCase(), str2.toLowerCase());
        const maxLength = Math.max(str1.length, str2.length);
        
        return maxLength > 0 ? 1 - (editDistance / maxLength) : 0;
    }

    /**
     * Levenshtein距離の計算
     */
    levenshteinDistance(str1, str2) {
        const m = str1.length;
        const n = str2.length;
        const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));
        
        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;
        
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (str1[i-1] === str2[j-1]) {
                    dp[i][j] = dp[i-1][j-1];
                } else {
                    dp[i][j] = Math.min(
                        dp[i-1][j] + 1,     // 削除
                        dp[i][j-1] + 1,     // 挿入
                        dp[i-1][j-1] + 1    // 置換
                    );
                }
            }
        }
        
        return dp[m][n];
    }

    /**
     * 部分文字列一致度の計算
     */
    calculateSubstringMatch(words1, words2) {
        if (words1.length === 0 && words2.length === 0) return 1;
        if (words1.length === 0 || words2.length === 0) return 0;
        
        let matches = 0;
        const usedIndices = new Set();
        
        // 各単語について、部分一致を探す
        for (const word1 of words1) {
            for (let i = 0; i < words2.length; i++) {
                if (usedIndices.has(i)) continue;
                
                const word2 = words2[i];
                
                // 完全一致
                if (word1 === word2) {
                    matches += 1;
                    usedIndices.add(i);
                    break;
                }
                
                // 部分一致（3文字以上の単語に対して）
                if (word1.length >= 3 && word2.length >= 3) {
                    if (word1.includes(word2) || word2.includes(word1)) {
                        matches += 0.7;
                        usedIndices.add(i);
                        break;
                    }
                    
                    // 語幹の類似性（最初の3文字が一致）
                    if (word1.substring(0, 3) === word2.substring(0, 3)) {
                        matches += 0.5;
                        usedIndices.add(i);
                        break;
                    }
                }
            }
        }
        
        return matches / Math.max(words1.length, words2.length);
    }
    
    /**
     * 音声パネルを表示
     */
    showVoicePanel() {
        const panel = document.getElementById('voice-control-panel');
        if (panel) {
            panel.style.display = 'block';
            
            // パネルが表示されたので、進捗ボタンのイベントリスナーを再設定
            setTimeout(() => {
                this.setupProgressButtonListener();
            }, 100);
        }
    }
    
    /**
     * 音声パネルを非表示
     */
    hideVoicePanel() {
        const panel = document.getElementById('voice-control-panel');
        if (panel) {
            panel.style.display = 'none';
            // 分析結果もクリア
            const resultsContainer = document.getElementById('voice-analysis-results');
            if (resultsContainer) {
                resultsContainer.innerHTML = '';
            }
        }
    }
    
    /**
     * 音声パネルの表示/非表示を切り替え
     */
    toggleVoicePanel() {
        const panel = document.getElementById('voice-control-panel');
        if (panel) {
            const isVisible = panel.style.display === 'block';
            if (isVisible) {
                this.hideVoicePanel();
            } else {
                this.showVoicePanel();
            }
        }
    }
    
    /**
     * 音量モニタリングを設定
     */
    setupVolumeMonitoring(stream) {
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            this.audioContext = new AudioContextClass();
            this.analyser = this.audioContext.createAnalyser();
            
            const source = this.audioContext.createMediaStreamSource(stream);
            source.connect(this.analyser);
            
            this.analyser.fftSize = 256;
            const bufferLength = this.analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            const updateVolume = () => {
                if (!this.isRecording) return;
                
                this.analyser.getByteFrequencyData(dataArray);
                
                let sum = 0;
                for (let i = 0; i < bufferLength; i++) {
                    sum += dataArray[i];
                }
                const average = sum / bufferLength;
                const volume = (average / 255) * 100;
                
                const volumeBar = document.getElementById('voice-volume-bar');
                if (volumeBar) {
                    volumeBar.style.width = `${volume}%`;
                }
                
                this.animationId = requestAnimationFrame(updateVolume);
            };
            
            updateVolume();
            
        } catch (error) {
            console.error('音量モニタリング設定エラー:', error);
        }
    }
    
    /**
     * 音量モニタリングを停止
     */
    stopVolumeMonitoring() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
        
        const volumeBar = document.getElementById('voice-volume-bar');
        if (volumeBar) {
            volumeBar.style.width = '0%';
        }
    }
    
    /**
     * 録音タイマーを開始
     */
    startRecordingTimer() {
        this.recordingTimerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            
            const timerElement = document.getElementById('voice-recording-timer');
            if (timerElement) {
                timerElement.textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        }, 1000);
    }
    
    /**
     * 録音タイマーを停止
     */
    stopRecordingTimer() {
        if (this.recordingTimerInterval) {
            clearInterval(this.recordingTimerInterval);
            this.recordingTimerInterval = null;
        }
        
        const timerElement = document.getElementById('voice-recording-timer');
        if (timerElement) {
            timerElement.textContent = '00:00';
        }
    }
    
    /**
     * 録音UI状態を更新
     */
    updateRecordingUI(isRecording) {
        const recordBtn = document.getElementById('voice-record-btn');
        const stopBtn = document.getElementById('voice-stop-btn');
        
        if (recordBtn) {
            recordBtn.innerHTML = isRecording ? '⏸️ 停止' : '🎤 録音';
            recordBtn.className = isRecording ? 'voice-btn recording' : 'voice-btn';
        }
        
        if (stopBtn) {
            stopBtn.style.display = isRecording ? 'inline-block' : 'none';
        }
    }
    
    /**
     * ステータス表示を更新
     */
    updateStatus(message, type = 'info') {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `voice-status ${type}`;
        }
        
        console.log(`🎤 ${message}`);
    }
    
    /**
     * 音声リストを読み込み
     */
    loadVoices() {
        const updateVoices = () => {
            const voices = speechSynthesis.getVoices();
            console.log(`📢 利用可能な音声: ${voices.length}個`);
            
            // 英語音声を優先して選択
            const englishVoices = voices.filter(voice => voice.lang.startsWith('en'));
            if (englishVoices.length > 0) {
                console.log(`🇺🇸 英語音声: ${englishVoices.length}個見つかりました`);
                console.log('📋 英語音声一覧:');
                englishVoices.forEach(voice => {
                    const isFemale = voice.name.toLowerCase().includes('female') || 
                                   voice.name.toLowerCase().includes('woman') ||
                                   voice.name.toLowerCase().includes('zira') ||
                                   voice.name.toLowerCase().includes('hazel') ||
                                   voice.name.toLowerCase().includes('samantha') ||
                                   voice.name.toLowerCase().includes('karen') ||
                                   voice.name.toLowerCase().includes('anna') ||
                                   voice.name.toLowerCase().includes('linda') ||
                                   voice.name.toLowerCase().includes('heather');
                    
                    const gender = isFemale ? '👩 女性' : '👨 男性/不明';
                    console.log(`  - ${voice.name} (${voice.lang}) ${gender}`);
                });
                
                // 女性音声をハイライト
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
                    console.log(`👩 女性の英語音声: ${femaleVoices.length}個見つかりました`);
                    console.log('🎯 優先使用される女性音声:', femaleVoices[0].name);
                } else {
                    console.log('⚠️ 女性の英語音声が見つかりませんでした。利用可能な英語音声を使用します。');
                }
            } else {
                console.log('⚠️ 英語音声が見つかりませんでした。');
            }
        };
        
        if (speechSynthesis.getVoices().length > 0) {
            updateVoices();
        } else {
            speechSynthesis.onvoiceschanged = updateVoices;
        }
    }
    
    /**
     * 音声認識を初期化
     */
    initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('⚠️ このブラウザは音声認識をサポートしていません');
            return;
        }
        
        this.recognition = new SpeechRecognition();
        this.recognition.lang = 'en-US';
        this.recognition.continuous = true;  // 連続認識
        this.recognition.interimResults = false; // 最終結果のみ
        this.recognition.maxAlternatives = 1;
        
        // 認識結果を受信
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + ' ';
                }
            }
            
            if (finalTranscript.trim()) {
                this.recognizedText += finalTranscript;
                console.log('🎯 認識結果追加:', finalTranscript.trim());
                console.log('🎯 累積認識結果:', this.recognizedText.trim());
            }
        };
        
        // 認識開始
        this.recognition.onstart = () => {
            console.log('🎤 音声認識開始');
            this.isRecognitionActive = true;
        };
        
        // 認識終了
        this.recognition.onend = () => {
            console.log('🔚 音声認識終了');
            this.isRecognitionActive = false;
        };
        
        // 認識エラー
        this.recognition.onerror = (event) => {
            console.warn('⚠️ 音声認識エラー:', event.error);
            this.isRecognitionActive = false;
        };
        
        console.log('✅ 音声認識初期化完了');
    }
    
    /**
     * 分析ボタンを非表示にする（リアルタイム認識では不要）
     */
    hideAnalyzeButton() {
        const analyzeBtn = document.getElementById('voice-analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.style.display = 'none';
            console.log('🔧 分析ボタンを非表示にしました（自動分析のため不要）');
        }
    }
    
    /**
     * 学習進捗を表示
     */
    showProgress() {
        console.log('📊 学習進捗表示を開始');
        
        // VoiceProgressUIが利用可能かチェック
        if (typeof VoiceProgressUI === 'undefined') {
            console.error('❌ VoiceProgressUI クラスが読み込まれていません');
            alert('エラー: 進捗表示システムが読み込まれていません。\nページを再読み込みしてください。');
            return;
        }
        
        try {
            // VoiceProgressUIのインスタンスを作成して進捗パネルを表示
            const progressUI = new VoiceProgressUI();
            progressUI.showProgressPanel();
            console.log('✅ 学習進捗パネルを表示しました');
        } catch (error) {
            console.error('❌ 進捗表示エラー:', error);
            alert('進捗表示でエラーが発生しました: ' + error.message);
        }
    }
}

// グローバルインスタンス
let voiceSystem = null;

// DOMロード後に初期化
document.addEventListener('DOMContentLoaded', () => {
    // VoiceProgressTrackerが確実に読み込まれるまで少し待機
    setTimeout(() => {
        voiceSystem = new VoiceSystem();
        console.log('✅ 音声システムを初期化しました');
    }, 500);
});
