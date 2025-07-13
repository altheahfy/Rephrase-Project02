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
        
        this.init();
    }
    
    async init() {
        console.log('🎤 音声システム初期化開始...');
        
        // 音声リストを読み込み
        this.loadVoices();
        
        // マイクアクセス許可を確認
        await this.checkMicrophonePermission();
        
        // イベントリスナーを設定
        this.setupEventListeners();
        
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
        
        // 分析ボタン
        const analyzeBtn = document.getElementById('voice-analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.analyzeRecording());
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
            // 🔧 前回の録音データを完全にクリア
            this.recordedBlob = null;
            
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
                this.updateStatus('✅ 録音完了', 'success');
            };
            
            // 録音開始
            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingStartTime = Date.now();
            
            // UI更新
            this.updateRecordingUI(true);
            this.startRecordingTimer();
            this.setupVolumeMonitoring(stream);
            
            this.updateStatus('🎤 録音開始...', 'recording');
            
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
        
        // ボリュームモニタリング停止
        this.stopVolumeMonitoring();
        
        this.updateStatus('⏹️ すべて停止', 'stopped');
    }
    
    /**
     * 録音の音響分析
     */
    async analyzeRecording() {
        if (!this.recordedBlob) {
            this.updateStatus('❌ 分析する録音がありません', 'error');
            return;
        }
        
        try {
            this.updateStatus('📊 音響分析中...', 'analyzing');
            
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            const audioContext = new AudioContextClass();
            
            const arrayBuffer = await this.recordedBlob.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            // 🔄 非同期分析に変更
            const analysis = await this.performAcousticAnalysis(audioBuffer);
            this.displayAnalysisResults(analysis);
            
            await audioContext.close();
            
        } catch (error) {
            console.error('音響分析エラー:', error);
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
        let contentAccuracy = 1.0; // デフォルトは100%（音声認識が利用できない場合）
        let verificationStatus = '音声認識未実行';
        
        try {
            recognizedText = await this.recognizeSpeechFromBlob(this.recordedBlob);
            console.log(`🎯 期待文章: "${expectedSentence}"`);
            console.log(`🎤 認識結果: "${recognizedText}"`);
            
            if (recognizedText) {
                contentAccuracy = this.calculateTextSimilarity(expectedSentence, recognizedText);
                verificationStatus = contentAccuracy >= 0.7 ? '内容一致' : '内容不一致';
                console.log(`📊 内容一致度: ${(contentAccuracy * 100).toFixed(1)}%`);
            } else {
                verificationStatus = '音声認識失敗';
            }
        } catch (error) {
            console.log('⚠️ 音声認識エラー:', error.message);
            verificationStatus = '音声認識エラー';
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
            verificationStatus
        };
    }
    
    /**
     * 分析結果を表示（改良版）
     */
    displayAnalysisResults(analysis) {
        const contentVerificationHtml = analysis.recognizedText ? `
            <div class="content-verification">
                <h5>🔍 発話内容検証</h5>
                <div class="verification-item"><strong>期待文章:</strong> "${analysis.expectedSentence}"</div>
                <div class="verification-item"><strong>認識結果:</strong> "${analysis.recognizedText}"</div>
                <div class="verification-item"><strong>一致度:</strong> ${(analysis.contentAccuracy * 100).toFixed(1)}% (${analysis.verificationStatus})</div>
            </div>
        ` : `
            <div class="content-verification">
                <div class="verification-item">⚠️ 音声認識による内容検証は実行されませんでした</div>
            </div>
        `;
        
        const resultsHtml = `
            <div class="analysis-results">
                <h4>📊 音響分析結果</h4>
                <div class="analysis-item">⏱️ 録音時間: ${analysis.duration.toFixed(2)}秒</div>
                <div class="analysis-item">💬 期待単語数: ${analysis.expectedWordCount} / 実際: ${analysis.actualWordCount}</div>
                <div class="analysis-item">⚡ 発話速度: ${analysis.wordsPerSecond.toFixed(2)} 語/秒 (${analysis.wordsPerMinute.toFixed(0)} 語/分)</div>
                <div class="analysis-item">🎯 評価: ${analysis.level} ${analysis.levelExplanation}</div>
                ${contentVerificationHtml}
            </div>
        `;
        
        const resultsContainer = document.getElementById('voice-analysis-results');
        if (resultsContainer) {
            resultsContainer.innerHTML = resultsHtml;
        }
        
        this.updateStatus('✅ 分析完了', 'success');
    }

    /**
     * 音声認識でBlobから文章を認識
     */
    async recognizeSpeechFromBlob(audioBlob) {
        return new Promise((resolve, reject) => {
            // Web Speech API の SpeechRecognition を使用
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            
            if (!SpeechRecognition) {
                reject(new Error('このブラウザは音声認識をサポートしていません'));
                return;
            }
            
            // AudioオブジェクトでBlobを再生し、その間に音声認識を実行
            const audio = new Audio();
            const audioUrl = URL.createObjectURL(audioBlob);
            audio.src = audioUrl;
            
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            let timeoutId = null;
            
            recognition.onstart = () => {
                console.log('🎤 音声認識開始...');
                // 5秒でタイムアウト
                timeoutId = setTimeout(() => {
                    recognition.stop();
                    reject(new Error('音声認識タイムアウト'));
                }, 5000);
            };
            
            recognition.onresult = (event) => {
                if (timeoutId) clearTimeout(timeoutId);
                
                const result = event.results[0][0];
                const transcript = result.transcript;
                const confidence = result.confidence;
                
                console.log(`🎯 認識結果: "${transcript}" (信頼度: ${(confidence * 100).toFixed(1)}%)`);
                
                URL.revokeObjectURL(audioUrl);
                resolve(transcript);
            };
            
            recognition.onerror = (event) => {
                if (timeoutId) clearTimeout(timeoutId);
                console.error('音声認識エラー:', event.error);
                URL.revokeObjectURL(audioUrl);
                reject(new Error(`音声認識エラー: ${event.error}`));
            };
            
            recognition.onend = () => {
                if (timeoutId) clearTimeout(timeoutId);
                console.log('🔚 音声認識終了');
            };
            
            // 録音音声を再生しながら認識を開始
            try {
                audio.play();
                recognition.start();
            } catch (error) {
                URL.revokeObjectURL(audioUrl);
                reject(error);
            }
        });
    }

    /**
     * 2つのテキストの類似度を計算（簡易版）
     */
    calculateTextSimilarity(expected, actual) {
        if (!expected || !actual) return 0;
        
        // 大文字小文字を統一し、句読点を除去
        const normalizeText = (text) => {
            return text.toLowerCase()
                      .replace(/[^\w\s]/g, '') // 句読点除去
                      .trim()
                      .split(/\s+/);
        };
        
        const expectedWords = normalizeText(expected);
        const actualWords = normalizeText(actual);
        
        console.log('🔍 期待単語:', expectedWords);
        console.log('🔍 実際単語:', actualWords);
        
        // 単語レベルでの一致度計算
        let matchCount = 0;
        const expectedSet = new Set(expectedWords);
        const actualSet = new Set(actualWords);
        
        // 期待される単語のうち、実際に含まれているものの数
        for (let word of expectedSet) {
            if (actualSet.has(word)) {
                matchCount++;
            }
        }
        
        // レーベンシュタイン距離も考慮した類似度
        const maxLength = Math.max(expectedWords.length, actualWords.length);
        const lengthPenalty = Math.abs(expectedWords.length - actualWords.length) / maxLength;
        
        // 基本一致度から長さペナルティを差し引く
        const wordMatchRatio = expectedSet.size > 0 ? matchCount / expectedSet.size : 0;
        const similarity = Math.max(0, wordMatchRatio - lengthPenalty * 0.5);
        
        console.log(`📊 単語一致数: ${matchCount}/${expectedSet.size}, 長さペナルティ: ${(lengthPenalty * 100).toFixed(1)}%, 最終類似度: ${(similarity * 100).toFixed(1)}%`);
        
        return similarity;
    }
    
    /**
     * 音声パネルを表示
     */
    showVoicePanel() {
        const panel = document.getElementById('voice-control-panel');
        if (panel) {
            panel.style.display = 'block';
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
}

// グローバルインスタンス
let voiceSystem = null;

// DOMロード後に初期化
document.addEventListener('DOMContentLoaded', () => {
    voiceSystem = new VoiceSystem();
});
