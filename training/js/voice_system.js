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
        
        // 🚀 Web Audio API録音関連（Android対応）
        this.microphoneSource = null;
        this.recordingProcessor = null;
        this.audioChunks = []; // Float32Array配列として使用
        this.isPlaying = false;
        
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
        
        // 🤖 パネル表示状態管理
        this.isPanelVisible = false;
        
        // 🤖 Android音声認識用状態変数
        this.isAndroidAnalyzing = false;      // Android分析中フラグ
        this.androidRecognition = null;       // Android音声認識インスタンス
        this.androidTimeoutId = null;         // Android音声認識タイムアウトID
        
        // ⏱️ 音声認識タイムスタンプ記録（発話速度改善用・実験的）
        this.speechTimestamps = [];           // 認識結果のタイムスタンプ配列
        this.firstWordTime = null;            // 最初の語の認識時刻
        this.lastWordTime = null;             // 最後の語の認識時刻
        
        // � サブスロット展開対応：短時間重複フィルタリング用変数
        this.lastRecognitionTime = null;      // 最後の認識時刻
        this.lastRecognizedPhrase = '';       // 最後に認識されたフレーズ
        
        // �📱 緊急デバッグ: コンストラクタ完了確認
        console.log('🔧 VoiceSystemコンストラクタ完了');
        // this.init(); // 手動で呼び出すため削除
    }
    
    async init() {
        // 📱 デバッグログ配列の初期化を最初に実行
        if (!this.debugLogs) {
            this.debugLogs = [];
        }
        
        this.addDebugLog('🎤 音声システム初期化開始...', 'info');
        
        // 🤖 Android検出とパネル選択
        this.isAndroid = this.detectAndroid();
        this.currentPanel = this.isAndroid ? 'voice-control-panel-android' : 'voice-control-panel';
        this.addDebugLog(`📱 デバイス検出: ${this.isAndroid ? 'Android' : 'その他'} - パネル: ${this.currentPanel}`, 'info');
        
        // 🔍 パネル存在確認
        const panel = document.getElementById(this.currentPanel);
        if (!panel) {
            console.error(`❌ 指定されたパネルが見つかりません: ${this.currentPanel}`);
            console.log('🔍 利用可能なパネルを検索中...');
            
            // フォールバック：利用可能なパネルを検索
            const fallbackPanel = document.getElementById(this.isAndroid ? 'voice-control-panel' : 'voice-control-panel-android');
            if (fallbackPanel) {
                console.log(`🔄 フォールバックパネルを使用: ${fallbackPanel.id}`);
                this.currentPanel = fallbackPanel.id;
                this.isAndroid = !this.isAndroid; // フラグも反転
            } else {
                console.error('❌ 音声パネルが全く見つかりません');
            }
        } else {
            console.log(`✅ パネル確認完了: ${this.currentPanel}`);
        }
        
        // 音声リストを読み込み
        this.loadVoices();
        
        // マイクアクセス許可を確認
        await this.checkMicrophonePermission();
        
        // 🔧 デバイス別音声認識初期化
        if (this.isAndroid) {
            this.addDebugLog('📱 Android専用音声認識：既存システム使用', 'info');
            // Android専用システムは既に startAndroidVoiceRecognition() で初期化
        } else {
            this.addDebugLog('💻 PC専用音声認識を初期化', 'info');
            await this.initPCSpeechRecognition();
        }
        
        // イベントリスナーを設定
        this.setupEventListeners();
        
        // 分析ボタンを非表示（リアルタイム認識では不要）
        this.hideAnalyzeButton();
        
        // 📱 初期化時にパネル位置を調整（特にモバイル）
        setTimeout(() => {
            const panel = document.getElementById(this.currentPanel);
            if (panel) {
                this.adjustPanelPosition();
            }
        }, 1000);
        
        console.log('✅ 音声システム初期化完了');
        
        // 🔧 デバッグ用: グローバルアクセス可能にする
        window.voiceSystemDebug = {
            showPanel: () => this.showVoicePanel(),
            hidePanel: () => this.hideVoicePanel(),
            togglePanel: () => this.toggleVoicePanel(),
            testMicrophonePermission: async () => {
                try {
                    alert('🎤 マイク権限確認を開始します...');
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    alert('✅ マイクアクセス許可: 成功！\n録音機能が利用できます。');
                    stream.getTracks().forEach(track => track.stop());
                    this.addDebugLog('✅ マイク権限確認成功', 'success');
                } catch (error) {
                    alert(`❌ マイクアクセス許可: 失敗\nエラー: ${error.message}\n\nブラウザの設定でマイクアクセスを許可してください。`);
                    this.addDebugLog(`❌ マイク権限確認失敗: ${error.message}`, 'error');
                }
            },
            testRecording: async () => {
                try {
                    alert('🔴 録音テストを開始します...\n3秒間録音されます。');
                    this.addDebugLog('🔴 録音テスト開始', 'info');
                    
                    // Android Chrome専用の音声設定
                    const audioConstraints = {
                        audio: {
                            sampleRate: 48000,
                            channelCount: 1,
                            volume: 1.0,
                            echoCancellation: true,
                            noiseSuppression: true,
                            autoGainControl: true
                        }
                    };
                    
                    const stream = await navigator.mediaDevices.getUserMedia(audioConstraints);
                    
                    // Android Chrome対応のMediaRecorderオプション
                    const recorderOptions = {
                        mimeType: 'audio/webm;codecs=opus'
                    };
                    
                    // フォールバック設定
                    if (!MediaRecorder.isTypeSupported(recorderOptions.mimeType)) {
                        recorderOptions.mimeType = 'audio/webm';
                        this.addDebugLog('⚠️ opus コーデックが利用できません。webmにフォールバック', 'warning');
                    }
                    
                    if (!MediaRecorder.isTypeSupported(recorderOptions.mimeType)) {
                        delete recorderOptions.mimeType;
                        this.addDebugLog('⚠️ webmも利用できません。デフォルト設定を使用', 'warning');
                    }
                    
                    const mediaRecorder = new MediaRecorder(stream, recorderOptions);
                    const chunks = [];
                    
                    mediaRecorder.ondataavailable = event => {
                        if (event.data.size > 0) {
                            chunks.push(event.data);
                            this.addDebugLog(`📦 録音データチャンク: ${event.data.size} bytes`, 'info');
                        }
                    };
                    
                    mediaRecorder.onstop = () => {
                        this.addDebugLog('🔴 録音停止完了', 'info');
                        
                        if (chunks.length === 0) {
                            alert('❌ 録音データが取得できませんでした');
                            this.addDebugLog('❌ 録音データチャンクが空です', 'error');
                            stream.getTracks().forEach(track => track.stop());
                            return;
                        }
                        
                        const mimeType = recorderOptions.mimeType || 'audio/webm';
                        const blob = new Blob(chunks, { type: mimeType });
                        this.addDebugLog(`📦 録音Blob作成: ${blob.size} bytes, type: ${blob.type}`, 'info');
                        
                        const url = URL.createObjectURL(blob);
                        const audio = new Audio(url);
                        
                        audio.oncanplay = () => {
                            this.addDebugLog('🔊 音声ファイル再生準備完了', 'success');
                            audio.play().then(() => {
                                alert('✅ 録音テスト完了！\n録音した音声を再生中です。');
                                this.addDebugLog('✅ 録音テスト完了・再生開始', 'success');
                            }).catch(error => {
                                alert(`❌ 再生エラー: ${error.message}`);
                                this.addDebugLog(`❌ 再生エラー: ${error.message}`, 'error');
                            });
                        };
                        
                        audio.onerror = (error) => {
                            alert(`❌ 音声ファイルエラー: ${error.message}`);
                            this.addDebugLog(`❌ 音声ファイルエラー: ${error.message}`, 'error');
                        };
                        
                        audio.onended = () => {
                            URL.revokeObjectURL(url);
                            this.addDebugLog('🔊 録音テスト再生完了', 'info');
                        };
                        
                        // 音声読み込み開始
                        audio.load();
                        
                        stream.getTracks().forEach(track => track.stop());
                    };
                    
                    mediaRecorder.onerror = (event) => {
                        alert(`❌ 録音エラー: ${event.error.message}`);
                        this.addDebugLog(`❌ MediaRecorderエラー: ${event.error.message}`, 'error');
                        stream.getTracks().forEach(track => track.stop());
                    };
                    
                    // 録音開始
                    mediaRecorder.start(100); // 100ms間隔でデータを取得
                    this.addDebugLog('🔴 MediaRecorder.start() 実行', 'info');
                    
                    setTimeout(() => {
                        if (mediaRecorder.state === 'recording') {
                            mediaRecorder.stop();
                            this.addDebugLog('⏱️ 3秒経過：録音停止', 'info');
                        }
                    }, 3000);
                    
                } catch (error) {
                    alert(`❌ 録音テスト失敗\nエラー: ${error.message}`);
                    this.addDebugLog(`❌ 録音テスト失敗: ${error.message}`, 'error');
                }
            },
            checkPanels: () => {
                console.log('🔍 パネル状況確認:');
                console.log(`  - Android検出: ${this.isAndroid}`);
                console.log(`  - 現在のパネル: ${this.currentPanel}`);
                
                const androidPanel = document.getElementById('voice-control-panel-android');
                const normalPanel = document.getElementById('voice-control-panel');
                
                console.log(`  - Android専用パネル: ${androidPanel ? '存在' : '不在'}`);
                console.log(`  - 通常パネル: ${normalPanel ? '存在' : '不在'}`);
                
                if (androidPanel) {
                    console.log(`    Android表示状態: ${androidPanel.style.display}`);
                }
                if (normalPanel) {
                    console.log(`    通常表示状態: ${normalPanel.style.display}`);
                }
                
                return { androidPanel, normalPanel, isAndroid: this.isAndroid };
            }
        };
        
        console.log('🔧 デバッグコマンド利用可能: window.voiceSystemDebug.checkPanels()');
    }
    
    /**
     * 🤖 Android デバイス検出
     */
    detectAndroid() {
        const userAgent = navigator.userAgent.toLowerCase();
        const isAndroid = /android/i.test(userAgent);
        
        console.log(`🔍 User Agent: ${navigator.userAgent.substring(0, 100)}...`);
        console.log(`🤖 Android検出結果: ${isAndroid}`);
        
        if (isAndroid) {
            console.log('🤖 Android専用音声システムを起動します');
            
            // Android専用パネルの存在確認
            const androidPanel = document.getElementById('voice-control-panel-android');
            if (androidPanel) {
                console.log('✅ Android専用パネルが見つかりました');
            } else {
                console.error('❌ Android専用パネルが見つかりません！HTMLにパネルが存在しない可能性があります');
            }
        } else {
            console.log('💻 通常デバイス用音声システムを起動します');
            
            // 通常パネルの存在確認
            const normalPanel = document.getElementById('voice-control-panel');
            if (normalPanel) {
                console.log('✅ 通常パネルが見つかりました');
            } else {
                console.error('❌ 通常パネルが見つかりません！');
            }
        }
        
        return isAndroid;
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

    /**
     * 🎯 上位スロットはwindow.loadedJsonData、サブスロットはwindow.lastSelectedSlotsから構築
     */
    buildSentenceFromOrderedData() {
        console.log('📊 混合データソースから例文を構築中...');
        
        // データソース確認
        const upperSlotData = window.loadedJsonData || [];
        const subSlotData = window.lastSelectedSlots || [];
        
        console.log(`📊 データソース: 上位スロット=${upperSlotData.length}件, サブスロット=${subSlotData.length}件`);
        
        const sentenceParts = [];
        
        // 疑問詞をチェック（上位スロットデータから）
        const questionWordData = upperSlotData.find(item => 
            item.DisplayAtTop === true && item.DisplayText
        );
        if (questionWordData) {
            console.log('✅ 疑問詞:', questionWordData.DisplayText);
            sentenceParts.push({
                order: -1,
                text: questionWordData.DisplayText,
                slot: 'question-word'
            });
        }
        
        // 🎯 混合アプローチ：各スロットの表示順序ごとに処理
        const slotOrderGroups = {};
        
        // 上位スロットをグループ化（window.loadedJsonDataから）
        upperSlotData.forEach(item => {
            const order = item.Slot_display_order;
            if (!slotOrderGroups[order]) {
                slotOrderGroups[order] = {
                    upperSlot: null,
                    subSlots: []
                };
            }
            
            if (!item.SubslotID) {
                slotOrderGroups[order].upperSlot = item;
            }
        });
        
        // サブスロットをグループ化（window.lastSelectedSlotsから）
        subSlotData.forEach(item => {
            const order = item.Slot_display_order;
            if (!slotOrderGroups[order]) {
                slotOrderGroups[order] = {
                    upperSlot: null,
                    subSlots: []
                };
            }
            
            if (item.SubslotID) {
                slotOrderGroups[order].subSlots.push(item);
            }
        });
        
        // 順序順に処理
        const sortedOrders = Object.keys(slotOrderGroups).sort((a, b) => parseInt(a) - parseInt(b));
        
        sortedOrders.forEach(order => {
            const group = slotOrderGroups[order];
            const upperSlot = group.upperSlot;
            const subSlots = group.subSlots;
            
            console.log(`🔍 order:${order} - 上位:${upperSlot ? upperSlot.Slot : 'なし'}, サブ:${subSlots.length}個`);
            
            // DisplayAtTopで分離表示されるスロットはスキップ
            if (upperSlot && upperSlot.DisplayAtTop === true) {
                console.log(`🚫 DisplayAtTop により ${upperSlot.Slot}(order:${order}) をスキップ`);
                return;
            }
            
            // 🎯 判定：上位スロットにテキストがあるかどうか
            if (upperSlot && upperSlot.SlotPhrase && upperSlot.SlotPhrase.trim()) {
                // 上位スロットにテキストがある場合：上位スロットを使用
                console.log(`✅ 上位スロット使用 ${upperSlot.Slot}(order:${order}): "${upperSlot.SlotPhrase}"`);
                sentenceParts.push({
                    order: parseInt(order),
                    text: upperSlot.SlotPhrase,
                    slot: upperSlot.Slot,
                    type: 'upper'
                });
            } else if (subSlots.length > 0) {
                // 上位スロットが空でサブスロットがある場合：サブスロットを使用
                console.log(`✅ サブスロット使用 (order:${order})`);
                subSlots
                    .filter(sub => sub.SubslotElement && sub.SubslotElement.trim())
                    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0))
                    .forEach(subSlot => {
                        const totalOrder = parseInt(order) * 1000 + (subSlot.display_order || 0);
                        console.log(`  - ${subSlot.SubslotID}(サブ:${subSlot.display_order}): "${subSlot.SubslotElement}"`);
                        sentenceParts.push({
                            order: totalOrder,
                            text: subSlot.SubslotElement,
                            slot: subSlot.SubslotID,
                            type: 'sub',
                            parent: subSlot.Slot
                        });
                    });
            }
        });
        
        // 最終的に順序でソート
        sentenceParts.sort((a, b) => a.order - b.order);
        
        console.log('📊 最終ソート結果:', sentenceParts.map(part => 
            `${part.slot}(${part.type || 'question'}, order:${part.order}): "${part.text}"`
        ));
        
        const sentence = sentenceParts.map(part => part.text).join(' ').trim();
        console.log(`📝 構築した例文: "${sentence}"`);
        
        return sentence;
    }

    /**
     * 動的エリアから現在表示されているスロットのテキストのみを抽出
     */
    extractCurrentSentenceFromDynamicArea() {
        console.log('🎯 動的記載エリアから表示中の音声用例文を抽出中...');
        
        const dynamicArea = document.getElementById('dynamic-slot-area');
        if (!dynamicArea) {
            console.warn('⚠️ 動的エリアが見つかりません');
            return '';
        }
        
        console.log('🔍 動的エリア詳細調査:');
        console.log('  - innerHTML:', dynamicArea.innerHTML.substring(0, 500) + '...');
        console.log('  - 子要素数:', dynamicArea.children.length);

        const sentenceParts = [];

        // 🔍 疑問詞をチェック（動的エリア内で特別扱い）
        const questionWordElement = dynamicArea.querySelector('.question-word-text, #dynamic-question-word .question-word-text');
        if (questionWordElement && this.isElementVisible(questionWordElement)) {
            const text = questionWordElement.textContent.trim();
            if (text) {
                console.log('✅ 疑問詞（動的エリア）:', text);
                sentenceParts.push({ order: -1, text: text, slot: 'question-word' });
            }
        }

        // 🔍 改良された動的スロット検出：ID ベースでの検出
        const slotNames = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
        
        slotNames.forEach(slotName => {
            // dynamic-slot-{slotName} の形式で検索
            const dynamicSlotElement = dynamicArea.querySelector(`#dynamic-slot-${slotName}, .slot[data-display-order]`);
            if (dynamicSlotElement) {
                const phraseElement = dynamicSlotElement.querySelector('.slot-phrase');
                if (phraseElement && this.isElementVisible(phraseElement)) {
                    const text = phraseElement.textContent.trim();
                    if (text && text !== 'N/A' && text !== '') {
                        // data-display-order から順序を取得、なければスロット名から推定
                        let displayOrder = parseInt(dynamicSlotElement.dataset.displayOrder);
                        if (!displayOrder) {
                            const slotOrderMap = { m1: 1, s: 2, aux: 3, m2: 4, v: 5, c1: 6, o1: 7, o2: 8, c2: 9, m3: 10 };
                            displayOrder = slotOrderMap[slotName] || 999;
                        }
                        
                        console.log(`✅ 動的スロット ${slotName.toUpperCase()} (order:${displayOrder}): "${text}"`);
                        sentenceParts.push({ 
                            order: displayOrder, 
                            text: text,
                            slot: slotName.toUpperCase(),
                            type: 'upper'
                        });
                    }
                }
            }
        });

        // 🔍 fallback: 汎用的な .slot クラス要素を検索
        if (sentenceParts.length === 0) {
            console.log('🔄 フォールバック: 汎用スロット要素を検索中...');
            const genericSlots = dynamicArea.querySelectorAll('.slot');
            console.log(`🔍 汎用スロット要素数: ${genericSlots.length}`);
            
            genericSlots.forEach((slotElement, index) => {
                const phraseElement = slotElement.querySelector('.slot-phrase');
                if (phraseElement && this.isElementVisible(phraseElement)) {
                    const text = phraseElement.textContent.trim();
                    if (text && text !== 'N/A' && text !== '') {
                        const displayOrder = parseInt(slotElement.dataset.displayOrder) || (index + 1);
                        const slotId = slotElement.id || `slot-${index}`;
                        
                        console.log(`✅ 汎用スロット ${slotId} (order:${displayOrder}): "${text}"`);
                        sentenceParts.push({ 
                            order: displayOrder, 
                            text: text,
                            slot: slotId,
                            type: 'generic'
                        });
                    }
                }
            });
        }

        // サブスロット検索（従来通り）
        const subSlotElements = dynamicArea.querySelectorAll('[data-subslot-id]');
        
        subSlotElements.forEach(subSlotElement => {
            const phraseElement = subSlotElement.querySelector('.slot-phrase');
            if (phraseElement && this.isElementVisible(phraseElement)) {
                const text = phraseElement.textContent.trim();
                if (text && text !== 'N/A' && text !== '') {
                    const subslotId = subSlotElement.dataset.subslotId;
                    const displayOrder = parseInt(subSlotElement.dataset.displayOrder) || 999;
                    
                    // 親スロットの情報を取得
                    const parentSlot = subSlotElement.closest('[data-slot]');
                    const parentSlotName = parentSlot ? parentSlot.dataset.slot : 'unknown';
                    const parentDisplayOrder = parentSlot ? parseInt(parentSlot.dataset.displayOrder) || 999 : 999;
                    
                    console.log(`✅ サブスロット ${subslotId} (parent:${parentSlotName}, parent_order:${parentDisplayOrder}, sub_order:${displayOrder}): "${text}"`);
                    
                    // 複合order：親スロットのorder * 1000 + サブスロットのorder
                    const compositeOrder = parentDisplayOrder * 1000 + displayOrder;
                    
                    sentenceParts.push({ 
                        order: compositeOrder, 
                        text: text,
                        slot: subslotId,
                        type: 'sub',
                        parentSlot: parentSlotName,
                        parentOrder: parentDisplayOrder,
                        subOrder: displayOrder
                    });
                }
            }
        });

        // Slot_display_order（上位スロット）とdisplay_order（サブスロット内）で順序をソート
        sentenceParts.sort((a, b) => a.order - b.order);
        
        console.log('📊 発見されたスロット数:', sentenceParts.length);
        console.log('📊 ソート後の順序:', sentenceParts.map(part => 
            `${part.slot}(${part.type}, order:${part.order}): "${part.text}"`
        ));

        const sentence = sentenceParts.map(part => part.text).join(' ').trim();

        console.log(`🎯 完成した例文: ${sentence}`);
        console.log(`📊 使用されたパーツ数: ${sentenceParts.length}`);
        
        return sentence;
    }

    /**
     * DOM要素が表示されているかどうかを判定
     */
    isElementVisible(element) {
        if (!element) return false;
        
        // CSSスタイルで非表示になっていないかチェック
        const style = window.getComputedStyle(element);
        if (style.display === 'none' || 
            style.visibility === 'hidden' || 
            style.opacity === '0') {
            return false;
        }
        
        // 親要素も確認
        let parent = element.parentElement;
        while (parent && parent !== document.body) {
            const parentStyle = window.getComputedStyle(parent);
            if (parentStyle.display === 'none' || 
                parentStyle.visibility === 'hidden') {
                return false;
            }
            parent = parent.parentElement;
        }
        
        return true;
    }
    
    /**
     * 🎤 音声専用データから例文を構築（推奨方法）
     */
    buildSentenceFromVoiceData() {
        console.log('🎤 音声専用データから例文を構築中...');
        console.log('利用可能な音声データ:', window.currentDisplayedSentence);
        console.log('音声データの件数:', window.currentDisplayedSentence.length);
        
        return this.buildSentenceFromData(window.currentDisplayedSentence, '音声専用データ');
    }
    
    /**
     * JSONデータから例文を構築（フォールバック）
     */
    buildSentenceFromJsonData() {
        console.log('📊 従来データから例文を構築中...');
        console.log('利用可能なスロットデータ:', window.lastSelectedSlots);
        console.log('スロットデータの件数:', window.lastSelectedSlots.length);
        
        return this.buildSentenceFromData(window.lastSelectedSlots, '従来データ');
    }
    
    /**
     * 共通の例文構築ロジック
     */
    buildSentenceFromData(slotData, dataSource) {
        console.log(`📝 ${dataSource}から例文を構築中...`);
        
        // データ構造の詳細ログ
        if (slotData.length > 0) {
            console.log('最初のスロットの構造:', slotData[0]);
            console.log('利用可能なキー:', Object.keys(slotData[0]));
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
                const subSlots = slotData
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
        console.log(`📝 ${dataSource}から構築した例文: "${sentence}"`);
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
            // 📱 Android対応: 詳細なデバッグ情報を追加
            console.log('🔍 マイクアクセス許可チェック開始...');
            console.log('📱 User Agent:', navigator.userAgent);
            console.log('🌐 Protocol:', window.location.protocol);
            console.log('🎤 MediaDevices available:', !!navigator.mediaDevices);
            console.log('🎤 getUserMedia available:', !!navigator.mediaDevices?.getUserMedia);
            
            // Permission API で事前確認（対応ブラウザのみ）
            if ('permissions' in navigator) {
                try {
                    const permission = await navigator.permissions.query({ name: 'microphone' });
                    console.log('🔐 マイク許可状態:', permission.state);
                } catch (permError) {
                    console.log('🔐 Permission API利用不可:', permError.message);
                }
            }
            
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 44100,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            this.isMicrophoneAllowed = true;
            stream.getTracks().forEach(track => track.stop()); // 即座に停止
            console.log('✅ マイクアクセス許可取得済み');
        } catch (error) {
            console.error('❌ マイクアクセス許可エラー:', error);
            console.error('❌ エラー名:', error.name);
            console.error('❌ エラーメッセージ:', error.message);
            
            // 📱 Android固有の問題を特定
            if (error.name === 'NotAllowedError') {
                console.log('🚫 ユーザーがマイクアクセスを拒否、またはHTTPS接続が必要');
            } else if (error.name === 'NotFoundError') {
                console.log('🔍 マイクが見つからない、または利用不可');
            } else if (error.name === 'NotSupportedError') {
                console.log('💻 ブラウザがgetUserMediaをサポートしていない');
            } else if (error.name === 'SecurityError') {
                console.log('🔒 セキュリティエラー: HTTPS接続が必要な可能性');
            }
            
            this.isMicrophoneAllowed = false;
        }
    }
    
    /**
     * イベントリスナーを設定
     */
    setupEventListeners() {
        this.addDebugLog('⚙️ イベントリスナー設定開始...', 'info');
        // 🤖 Android専用ボタンのイベントリスナー
        if (this.isAndroid) {
            this.addDebugLog('📱 Androidイベントリスナー設定中...', 'info');
            this.setupAndroidEventListeners();
        } else {
            this.addDebugLog('💻 標準イベントリスナー設定中...', 'info');
            this.setupStandardEventListeners();
        }
        
        // 共通のイベントリスナー
        this.addDebugLog('🔗 共通イベントリスナー設定中...', 'info');
        this.setupCommonEventListeners();
        this.addDebugLog('✅ 全イベントリスナー設定完了', 'success');
    }
    
    /**
     * 🤖 Android専用イベントリスナー設定
     */
    setupAndroidEventListeners() {
        this.addDebugLog('🤖 Android専用イベントリスナーを設定中...', 'info');
        
        // DOM全体をデバッグ情報として出力
        this.addDebugLog(`🔍 DOM読み込み状態: ${document.readyState}`, 'info');
        this.addDebugLog(`🔍 voice-control-panel-android存在: ${!!document.getElementById('voice-control-panel-android')}`, 'info');
        
        // Android専用録音ボタン（録音のみ）
        const recordBtnAndroid = document.getElementById('voice-record-btn-android');
        this.addDebugLog(`🔍 録音ボタン検索結果: ${recordBtnAndroid ? '見つかりました' : '見つかりません'}`, recordBtnAndroid ? 'success' : 'error');
        if (recordBtnAndroid) {
            recordBtnAndroid.addEventListener('click', () => {
                this.addDebugLog('🔥 Android録音ボタンがクリックされました', 'info');
                // 📱 透過モード有効化（スロット表示確保）- 他のボタンと同じ仕組み
                this.setVoicePanelTransparency(true);
                this.toggleRecordingAndroid();
            });
            this.addDebugLog('✅ Android専用録音ボタンのイベントリスナーを設定', 'success');
        } else {
            this.addDebugLog('❌ voice-record-btn-android要素が見つかりません', 'error');
            // 全てのボタン要素を検索してデバッグ
            const allButtons = document.querySelectorAll('button');
            this.addDebugLog(`🔍 ページ内の全ボタン数: ${allButtons.length}`, 'info');
            allButtons.forEach((btn, index) => {
                if (btn.id) {
                    this.addDebugLog(`  ボタン${index}: id="${btn.id}"`, 'info');
                }
            });
        }
        
        // Android専用再生ボタン
        const playBtnAndroid = document.getElementById('voice-play-btn-android');
        this.addDebugLog(`🔍 再生ボタン検索結果: ${playBtnAndroid ? '見つかりました' : '見つかりません'}`, playBtnAndroid ? 'success' : 'error');
        if (playBtnAndroid) {
            playBtnAndroid.addEventListener('click', () => {
                this.addDebugLog('🔥 Android再生ボタンがクリックされました', 'info');
                // 📱 透過モード有効化（スロット表示確保）
                this.setVoicePanelTransparency(true);
                this.playRecordingAndroid();
            });
            this.addDebugLog('✅ Android専用再生ボタンのイベントリスナーを設定', 'success');
        } else {
            this.addDebugLog('❌ voice-play-btn-android要素が見つかりません', 'error');
        }
        
        // Android専用音声合成ボタン（現行機能を使用）
        const ttsBtnAndroid = document.getElementById('voice-tts-btn-android');
        if (ttsBtnAndroid) {
            ttsBtnAndroid.addEventListener('click', () => {
                // 📱 透過モード有効化（スロット表示確保）
                this.setVoicePanelTransparency(true);
                this.speakSentence();
            });
            console.log('✅ Android専用音声合成ボタンのイベントリスナーを設定');
        }
        
        // Android専用分析ボタン
        const analyzeBtnAndroid = document.getElementById('voice-analyze-btn-android');
        if (analyzeBtnAndroid) {
            analyzeBtnAndroid.addEventListener('click', () => {
                // 📱 透過モード有効化（スロット表示確保）
                this.setVoicePanelTransparency(true);
                this.analyzeRecordingAndroid();
            });
            console.log('✅ Android専用分析ボタンのイベントリスナーを設定');
        }
        
        // Android専用パネル制御ボタン
        const closeBtnAndroid = document.getElementById('voice-panel-close-btn-android');
        if (closeBtnAndroid) {
            closeBtnAndroid.addEventListener('click', () => this.hideVoicePanelAndroid());
            console.log('✅ Android専用パネル閉じるボタンのイベントリスナーを設定');
        }
        
        // Android専用進捗ボタン
        const progressBtnAndroid = document.getElementById('voice-progress-btn-android');
        if (progressBtnAndroid) {
            progressBtnAndroid.addEventListener('click', () => this.showProgress());
            console.log('✅ Android専用進捗ボタンのイベントリスナーを設定');
        }
        
        // 🔧 Android専用デバッグボタン
        const debugBtnAndroid = document.getElementById('android-debug-btn');
        this.addDebugLog(`🔍 デバッグボタン検索結果: ${debugBtnAndroid ? '見つかりました' : '見つかりません'}`, debugBtnAndroid ? 'success' : 'warning');
        if (debugBtnAndroid) {
            debugBtnAndroid.addEventListener('click', () => {
                this.addDebugLog('🔧 Android デバッグボタンがクリックされました', 'info');
                this.addDebugLog('🔍 テスト: ボタンクリックイベント正常動作', 'success');
                // 音声認識のデバッグログを表示するため、showMobileDebugPanel()を呼び出し
                try {
                    this.showMobileDebugPanel();
                    this.addDebugLog('📱 デバッグパネル表示成功', 'success');
                } catch (error) {
                    this.addDebugLog(`❌ デバッグパネル表示エラー: ${error.message}`, 'error');
                }
            });
            this.addDebugLog('✅ Android専用デバッグボタンのイベントリスナーを設定', 'success');
        }
        
        // 📱 イベントリスナー設定完了テスト
        this.addDebugLog('🧪 テスト: setupAndroidEventListeners完了', 'info');
        this.addDebugLog(`🔍 現在時刻: ${new Date().toLocaleTimeString()}`, 'info');
    }
    
    /**
     * 💻 標準版イベントリスナー設定
     */
    setupStandardEventListeners() {
        console.log('💻 標準版イベントリスナーを設定中...');
        
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
    }
    
    /**
     * 共通イベントリスナー設定
     */
    setupCommonEventListeners() {
        
        // 🎤 音声学習パネル開くボタン（トグル機能）- 全デバイス共通
        const openBtn = document.getElementById('voice-panel-open-btn');
        if (openBtn) {
            // 🤖 Android用: ボタンの詳細情報をデバッグ表示
            if (this.isAndroid) {
                console.log('🤖 Android用デバッグ - 音声学習ボタン情報:');
                console.log(`  - ボタン要素: ${openBtn ? '存在' : '不在'}`);
                console.log(`  - ボタンのスタイル: ${openBtn.style.cssText}`);
                console.log(`  - ボタンのrect:`, openBtn.getBoundingClientRect());
                console.log(`  - ボタンのtouchAction: ${openBtn.style.touchAction}`);
                console.log(`  - ボタンのpointerEvents: ${openBtn.style.pointerEvents}`);
                
                // この行をコメントアウト: showAndroidClickFeedback('🔧 音声学習ボタンが検出されました', 'info');
            }
            
            openBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('🔘 音声パネル開くボタンがクリックされました');
                
                // 🤖 Android用: 視覚的フィードバック（コメントアウト）
                // if (this.isAndroid) {
                //     this.showAndroidClickFeedback('🔘 パネル開くボタンがクリックされました');
                // }
                
                this.toggleVoicePanel();
            });
            
            // 🤖 Android用: touchイベントも追加
            if (this.isAndroid) {
                openBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    console.log('👆 音声学習ボタン - touchstart');
                    // この行をコメントアウト: showAndroidClickFeedback('👆 touchstart検出', 'info');
                });
                
                openBtn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    console.log('👆 音声学習ボタン - touchend');
                    // この行をコメントアウト: showAndroidClickFeedback('👆 touchend検出', 'info');
                    
                    // touchendでも直接呼び出し
                    setTimeout(() => {
                        this.toggleVoicePanel();
                    }, 100);
                });
            }
            
            console.log('✅ 音声パネル開くボタンのイベントリスナーを設定しました');
        } else {
            console.error('❌ 音声パネル開くボタンが見つかりません (voice-panel-open-btn)');
            
            // 🤖 Android用: エラー表示（コメントアウト）
            // if (this.isAndroid) {
            //     this.showAndroidClickFeedback('❌ 開くボタンが見つかりません', 'error');
            // }
        }
        
        // 🎤 パネル閉じるボタン（通常版）
        const closeBtn = document.getElementById('voice-panel-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hideVoicePanel());
            console.log('✅ 通常パネル閉じるボタンのイベントリスナーを設定しました');
        }
        
        // 🤖 Android専用パネル閉じるボタン
        const closeBtnAndroid = document.getElementById('voice-panel-close-btn-android');
        if (closeBtnAndroid) {
            closeBtnAndroid.addEventListener('click', () => this.hideVoicePanel());
            console.log('✅ Android専用パネル閉じるボタンのイベントリスナーを設定しました');
        }
        
        // 📱 モバイルデバッグボタン
        const debugBtn = document.getElementById('mobile-debug-btn');
        if (debugBtn) {
            debugBtn.addEventListener('click', () => {
                try {
                    this.showMobileDebugPanel();
                } catch (error) {
                    console.error('デバッグパネル表示エラー:', error.message);
                }
            });
            console.log('✅ モバイルデバッグボタンのイベントリスナーを設定しました');
            
        } else {
            console.warn('⚠️ モバイルデバッグボタンが見つかりません');
        }
        
        // 📱 ウィンドウリサイズ・画面向き変更時のパネル位置調整
        window.addEventListener('resize', () => {
            const panel = document.getElementById('voice-control-panel');
            if (panel && panel.style.display === 'block') {
                setTimeout(() => {
                    this.adjustPanelPosition();
                }, 200); // レンダリング完了を待つ
            }
        });
        
        // 📱 画面向き変更対応
        window.addEventListener('orientationchange', () => {
            const panel = document.getElementById('voice-control-panel');
            if (panel && panel.style.display === 'block') {
                setTimeout(() => {
                    this.adjustPanelPosition();
                }, 500); // 向き変更のアニメーション完了を待つ
            }
        });
        
        // 学習進捗ボタン（動的に追加される可能性があるため遅延設定）
        this.setupProgressButtonListener();
        
        // 🔧 音声認識言語設定ボタン（動的に追加される可能性があるため遅延設定）
        this.setupVoiceLanguageButtonListener();
    }
    
    /**
     * 🚀 Android専用録音開始/停止（Web Audio API版）- 動作していた実装を完全移植
     */
    async toggleRecordingAndroid() {
        this.addDebugLog('� Web Audio API録音開始/停止', 'info');
        
        if (this.isRecording) {
            this.addDebugLog('📱 録音停止なので透過解除します', 'info');
            this.setVoicePanelTransparency(false);
            this.stopRecordingAndroidWebAudio();
        } else {
            await this.startRecordingAndroidWebAudio();
        }
    }

    /**
     * 🚀 Web Audio API録音開始（Android Chrome完全対応版）
     */
    async startRecordingAndroidWebAudio() {
        if (this.isRecording) {
            this.addDebugLog('⚠️ 既に録音中です', 'warning');
            // 📱 透過モード解除（既に録音中の場合）
            this.setVoicePanelTransparency(false);
            return;
        }

        this.addDebugLog('🎤 Web Audio API録音を開始します', 'info');
        this.updateStatus('🎤 マイクアクセス許可を要求中...', 'info');

        try {
            // AudioContext初期化
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                this.addDebugLog(`✅ AudioContext作成: sampleRate=${this.audioContext.sampleRate}Hz`, 'success');
            }

            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
                this.addDebugLog('🔧 AudioContext resumed', 'info');
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
            this.currentStream = stream;

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

                    // 録音進行表示（より頻繁に更新）
                    if (this.audioChunks.length % 5 === 0) {
                        const totalSamples = this.audioChunks.length * 4096;
                        const duration = totalSamples / this.audioContext.sampleRate;
                        this.updateStatus(`🎤 録音中... ${duration.toFixed(1)}秒`, 'recording');
                        
                        // Android専用タイマーも更新
                        const timerElement = document.getElementById('voice-recording-timer-android');
                        if (timerElement) {
                            const minutes = Math.floor(duration / 60);
                            const seconds = Math.floor(duration % 60);
                            timerElement.textContent = `⏱️ ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                        }
                    }
                }
            };

            // マイクからの音声をプロセッサに接続
            this.microphoneSource.connect(this.recordingProcessor);
            this.recordingProcessor.connect(this.audioContext.destination);

            this.isRecording = true;
            this.recordingStartTime = Date.now();
            this.updateRecordingUI(true);
            this.startRecordingTimer();
            this.setupVolumeMonitoring(stream);
            
            this.updateStatus('🎤 Web Audio API録音中... 0.0秒', 'recording');
            this.addDebugLog('✅ Web Audio API録音開始', 'success');

        } catch (error) {
            this.addDebugLog(`❌ Web Audio API録音開始エラー: ${error.message}`, 'error');
            this.updateStatus('❌ 録音開始失敗', 'error');
            this.isRecording = false;
        }
    }

    /**
     * 🚀 Web Audio API録音停止
     */
    stopRecordingAndroidWebAudio() {
        if (!this.isRecording) {
            this.addDebugLog('⚠️ 録音していません', 'warning');
            // 📱 透過モード解除（録音していない場合）
            this.setVoicePanelTransparency(false);
            return;
        }

        this.isRecording = false;
        this.addDebugLog('📱 録音フラグをfalseに設定', 'info');

        // Web Audio API録音停止
        if (this.recordingProcessor) {
            this.recordingProcessor.disconnect();
            this.recordingProcessor = null;
            this.addDebugLog('📱 recordingProcessor停止完了', 'info');
        }

        if (this.microphoneSource) {
            this.microphoneSource.disconnect();
            this.microphoneSource = null;
            this.addDebugLog('📱 microphoneSource停止完了', 'info');
        }

        // ストリーム停止
        if (this.currentStream) {
            this.currentStream.getTracks().forEach(track => track.stop());
            this.currentStream = null;
            this.addDebugLog('📱 currentStream停止完了', 'info');
        }

        this.addDebugLog('📱 stopVolumeMonitoring開始', 'info');
        this.stopVolumeMonitoring();
        this.addDebugLog('📱 stopRecordingTimer開始', 'info');
        this.stopRecordingTimer();
        this.addDebugLog('📱 updateRecordingUI開始', 'info');
        this.updateRecordingUI(false);

        this.addDebugLog('🛑 Web Audio API録音停止完了', 'success');
        
        // updateStatusをtry-catchで囲んで、エラーがあっても継続
        try {
            this.updateStatus('✅ 録音完了', 'success');
            this.addDebugLog('📱 updateStatus呼び出し成功', 'success');
        } catch (error) {
            this.addDebugLog(`❌ updateStatusエラー: ${error.message}`, 'error');
        }

        // 録音データ処理
        this.addDebugLog('📱 録音データ処理開始', 'info');
        if (this.audioChunks.length > 0) {
            const totalSamples = this.audioChunks.length * 4096;
            const duration = totalSamples / this.audioContext.sampleRate;
            this.addDebugLog(`🎵 録音データ保存: ${duration.toFixed(1)}秒`, 'success');
            this.addDebugLog('💾 録音データ保存完了（再生準備OK）', 'success');
        } else {
            this.addDebugLog('⚠️ 録音データが空です', 'warning');
        }
        this.addDebugLog('📱 録音データ処理完了', 'success');
        
        // 📱 透過モード解除（録音終了）
        this.addDebugLog('📱 録音停止 - 透過モード解除開始', 'info');
        this.setVoicePanelTransparency(false);
        this.addDebugLog('📱 録音停止 - 透過モード解除完了', 'success');
        
        // 📱 追加の強制リセット（100ms後に再実行）
        setTimeout(() => {
            this.addDebugLog('📱 強制透過リセット実行', 'info');
            this.setVoicePanelTransparency(false);
        }, 100);
    }

    /**
     * 🚀 Web Audio API録音データ再生機能（Android完全対応版）
     */
    async playRecordingAndroid() {
        this.addDebugLog('🔊 Web Audio API録音データ再生開始', 'info');
        
        if (!this.audioChunks || this.audioChunks.length === 0) {
            this.addDebugLog('❌ 再生する録音データがありません（先に録音してください）', 'error');
            this.updateStatus('❌ 再生する録音がありません', 'error');
            // 🔧 録音データがない場合も透明度をリセット
            this.setVoicePanelTransparency(false);
            return;
        }

        if (this.isPlaying) {
            this.addDebugLog('⚠️ 既に再生中です', 'warning');
            // 🔧 既に再生中の場合も透明度をリセット
            this.setVoicePanelTransparency(false);
            return;
        }

        this.addDebugLog('🔊 Web Audio API録音データ再生開始', 'info');
        await this.playWithWebAudioAPI();
    }

    /**
     * 🚀 Web Audio API録音データの再生
     */
    async playWithWebAudioAPI() {
        try {
            this.addDebugLog('🎵 Web Audio API再生を開始', 'info');

            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            // ユーザーインタラクション後にコンテキストを再開
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

            this.isPlaying = true;
            this.updateStatus(`🔊 再生中... (${audioBuffer.duration.toFixed(1)}秒)`, 'playing');

            source.onended = () => {
                this.isPlaying = false;
                this.updateStatus('✅ 再生完了', 'success');
                this.addDebugLog('🔊 Web Audio API再生完了', 'success');
                // 🔧 再生完了時に透明度をリセット
                this.setVoicePanelTransparency(false);
            };

            source.start(0);
            this.addDebugLog('🎵 Web Audio API再生開始', 'success');

        } catch (error) {
            this.addDebugLog(`❌ Web Audio API再生エラー: ${error.message}`, 'error');
            this.isPlaying = false;
            this.updateStatus('❌ 再生エラー', 'error');
            // 🔧 再生エラー時も透明度をリセット
            this.setVoicePanelTransparency(false);
            
            // フォールバック: WAVダウンロード
            this.addDebugLog('💾 ダウンロードリンクを生成します', 'info');
            this.createDownloadLink();
        }
    }

    /**
     * 🚀 Float32ArrayをWAVファイルに変換してダウンロード（フォールバック）
     */
    createDownloadLink() {
        try {
            this.addDebugLog('💾 ダウンロードリンクを生成します', 'info');

            if (!this.audioChunks || this.audioChunks.length === 0) {
                this.addDebugLog('❌ 録音データがありません', 'error');
                return;
            }

            // Float32ArrayをWAVファイルに変換
            const wavBlob = this.float32ArrayToWav(this.audioChunks, this.audioContext.sampleRate);
            const audioUrl = URL.createObjectURL(wavBlob);
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const filename = `rephrase_recording_${timestamp}.wav`;

            // ダウンロードリンク作成
            const downloadLink = document.createElement('a');
            downloadLink.href = audioUrl;
            downloadLink.download = filename;
            downloadLink.textContent = `📁 録音をダウンロード (${filename})`;
            downloadLink.style.cssText = `
                display: block;
                margin: 10px 0;
                padding: 10px;
                background: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
            `;

            // デバッグパネルに追加
            const debugPanel = document.getElementById('debug-panel');
            if (debugPanel) {
                debugPanel.appendChild(downloadLink);
            }

            this.addDebugLog(`💾 ダウンロードリンク作成完了: ${filename}`, 'success');

        } catch (error) {
            this.addDebugLog(`❌ ダウンロードリンク作成エラー: ${error.message}`, 'error');
        }
    }

    /**
     * 🚀 Float32ArrayをWAVファイルに変換
     */
    float32ArrayToWav(audioChunks, sampleRate) {
        // Float32Arrayデータを結合
        const totalSamples = audioChunks.length * 4096;
        const buffer = new Float32Array(totalSamples);
        let offset = 0;
        
        audioChunks.forEach(chunk => {
            buffer.set(chunk, offset);
            offset += chunk.length;
        });

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
        let offset2 = 44;
        for (let i = 0; i < length; i++) {
            const sample = Math.max(-1, Math.min(1, buffer[i]));
            view.setInt16(offset2, sample * 0x7FFF, true);
            offset2 += 2;
        }
        
        return new Blob([arrayBuffer], { type: 'audio/wav' });
    }

    /**
     * 🤖 Android専用パネル非表示
     */
    hideVoicePanelAndroid() {
        const panel = document.getElementById('voice-control-panel-android');
        if (panel) {
            panel.style.setProperty('display', 'none', 'important');
            this.isPanelVisible = false;
            console.log('🤖 Android音声パネルを非表示にしました');
        }
    }

    /**
     * 🤖 Android専用録音分析（リアルタイム音声認識版・押し直し停止対応）
     */
    analyzeRecordingAndroid() {
        console.log('🤖 Android: 分析ボタンがクリックされました');
        
        // 🔄 押し直し停止機能：すでに認識中の場合は停止
        if (this.isAndroidAnalyzing) {
            console.log('🛑 Android音声認識を停止します');
            this.stopAndroidVoiceRecognition();
            // 📱 透過モード解除（認識停止時）
            this.setVoicePanelTransparency(false);
            return;
        }
        
        console.log('🎤 リアルタイム音声認識を開始');
        this.updateStatus('🎤 Android音声認識準備中...', 'analyzing');
        
        // temp_working_voice_system.jsのtestVoiceRecognition()ベースの音声認識
        this.startAndroidVoiceRecognition();
    }

    /**
     * 🎤 Android用リアルタイム音声認識（temp_working_voice_system.jsから移植）
     */
    startAndroidVoiceRecognition() {
        this.addDebugLog('🎤 Android音声認識テストを開始します...', 'info');
        
        // 認識状態をセット
        this.isAndroidAnalyzing = true;
        
        // 認識結果をクリア
        this.recognizedText = '';
        this.addDebugLog('🔄 this.recognizedTextをクリアしました', 'info');
        
        // ⏱️ タイムスタンプ記録をリセット（実験的機能）
        this.speechTimestamps = [];
        this.firstWordTime = null;
        this.lastWordTime = null;
        
        // 🔧 サブスロット展開対応：重複フィルタリング変数もリセット
        this.lastRecognitionTime = null;
        this.lastRecognizedPhrase = '';
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('🚫 Web Speech API が利用できません', 'error');
            this.updateStatus('❌ 音声認識非対応', 'error');
            this.isAndroidAnalyzing = false;
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // 認識インスタンスを保存（停止用）
        this.androidRecognition = recognition;
        
        // 🔧 Android専用音声認識言語設定
        let androidLang = localStorage.getItem('voiceRecognitionLanguage_Android') || 'en-US';
        console.log(`🔍 Android専用音声認識言語設定: ${androidLang}`);
        
        // Android Chrome最適化設定
        const isAndroid = /Android/i.test(navigator.userAgent);
        if (isAndroid) {
            this.addDebugLog('📱 Android Chrome用設定を適用', 'info');
            // 🔧 実験的修正: 無音による自動停止を回避するため継続的認識を使用
            recognition.continuous = true;  // 無音自動停止回避のため継続的認識
            recognition.interimResults = true; // 途中結果も取得
            recognition.lang = androidLang; // Android専用言語設定
            recognition.maxAlternatives = 3; // 複数候補
            this.addDebugLog('🔧 実験的設定: 無音自動停止回避のため継続的認識を使用', 'warning');
            this.addDebugLog(`🔧 Android専用言語設定: ${androidLang}`, 'info');
        } else {
            this.addDebugLog('💻 PC/iPhone用設定を適用', 'info');
            recognition.continuous = false;  // 1回認識に変更
            recognition.interimResults = false;
            recognition.lang = 'en-US'; // PC版は別系統で管理
            recognition.maxAlternatives = 1;
        }
        
        this.addDebugLog(`🔧 認識準備: lang=${recognition.lang}`, 'info');
        
        // タイムアウト設定：継続的認識なので長めに設定
        const timeoutDuration = isAndroid ? 30000 : 25000; // 25-30秒
        this.androidTimeoutId = setTimeout(() => {
            this.addDebugLog(`⏰ 音声認識がタイムアウトしました (${timeoutDuration/1000}秒)`, 'warning');
            this.addDebugLog('🔄 分析ボタンを再度押して停止してください', 'info');
            // タイムアウト時は自動停止せず、ユーザーに停止を促す
            this.updateStatus('⏰ 長時間認識中... 分析ボタンを押して停止', 'recording');
        }, timeoutDuration);
        
        recognition.onstart = () => {
            this.recognitionStartTime = Date.now(); // 開始時刻を記録
            this.addDebugLog('✅ 音声認識start()コマンド送信完了', 'success');
            this.addDebugLog('🎤 音声認識開始イベント発生', 'info');
            this.updateStatus('🎤 話してください...（もう一度押すと停止）', 'recording');
        };
        
        recognition.onresult = (event) => {
            if (this.androidTimeoutId) {
                clearTimeout(this.androidTimeoutId);
            }
            
            // ⏱️ 認識結果タイムスタンプ記録（実験的・既存処理に影響なし）
            const resultTime = Date.now();
            
            this.addDebugLog('📝 音声認識結果イベント発生', 'info');
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript.trim();
                const confidence = result[0].confidence || 0;
                
                if (result.isFinal && transcript.length > 0) {
                    // 🔧 サブスロット展開対応：短時間重複フィルタリング
                    const now = Date.now();
                    const timeSinceLastRecognition = this.lastRecognitionTime ? (now - this.lastRecognitionTime) : 1000;
                    
                    // 500ms以内の連続認識で同じ内容の場合はスキップ（サブスロット展開時の間対策）
                    if (timeSinceLastRecognition < 500 && this.lastRecognizedPhrase === transcript) {
                        this.addDebugLog(`⚠️ サブスロット展開短時間重複をスキップ: "${transcript}" (${timeSinceLastRecognition}ms前)`, 'warning');
                        return;
                    }
                    
                    this.lastRecognitionTime = now;
                    this.lastRecognizedPhrase = transcript;
                    
                    // 高度な重複チェック：文章レベルでの重複を検出
                    const currentText = this.recognizedText || '';
                    
                    if (currentText.length === 0) {
                        // 初回の場合はそのまま設定
                        this.recognizedText = transcript;
                        this.addDebugLog(`✅ 初回認識結果: "${transcript}"`, 'success');
                    } else {
                        // 既存のテキストと新しいテキストの重複部分を検出
                        let overlap = this.findTextOverlap(currentText, transcript);
                        
                        // 末尾先頭重複がない場合、フレーズ全体重複をチェック
                        if (overlap.length === 0) {
                            overlap = this.findCompleteOverlap(currentText, transcript);
                        }
                        
                        if (overlap.length > 0) {
                            // 重複部分を除いた新しい部分のみを追加
                            const newPart = transcript.substring(overlap.length).trim();
                            if (newPart.length > 0) {
                                this.recognizedText += ' ' + newPart;
                                this.addDebugLog(`✅ 重複除去後追加: "${newPart}"`, 'success');
                                this.addDebugLog(`🔍 検出された重複: "${overlap}"`, 'info');
                            } else {
                                this.addDebugLog(`⚠️ 完全重複のためスキップ: "${transcript}"`, 'warning');
                            }
                        } else {
                            // 重複がない場合は通常の追加
                            this.recognizedText += ' ' + transcript;
                            this.addDebugLog(`✅ 新規追加: "${transcript}"`, 'success');
                        }
                    }
                    
                    // ⏱️ タイムスタンプ記録（実験的・既存処理完了後に安全に追加）
                    if (this.firstWordTime === null) {
                        this.firstWordTime = resultTime;
                    }
                    this.lastWordTime = resultTime;
                    this.speechTimestamps.push({
                        text: transcript,
                        time: resultTime,
                        relativeTime: this.recognitionStartTime ? (resultTime - this.recognitionStartTime) / 1000 : 0
                    });
                } else {
                    console.log(`� 認識結果 (途中): "${transcript}"`);
                }
            }
        };
        
        recognition.onend = () => {
            if (this.androidTimeoutId) {
                clearTimeout(this.androidTimeoutId);
                this.addDebugLog('🏁 音声認識終了イベント発生（タイムアウト前）', 'warning');
                this.addDebugLog('🔍 停止理由: Web Speech API内部の無音検出または発話終了判定', 'warning');
            } else {
                this.addDebugLog('🏁 音声認識終了イベント発生（タイムアウト後）', 'warning');
                this.addDebugLog('🔍 停止理由: 手動停止またはタイムアウト', 'info');
            }
            
            // 経過時間を計算
            const startTime = this.recognitionStartTime || Date.now();
            const endTime = Date.now();
            const elapsedSeconds = ((endTime - startTime) / 1000).toFixed(1);
            this.addDebugLog(`⏱️ 認識実行時間: ${elapsedSeconds}秒`, 'info');
            
            // 🔧 継続的認識の場合、手動停止以外は再開を試行
            if (isAndroid && this.isAndroidAnalyzing) {
                this.addDebugLog('🔄 継続的認識: 再開を試行', 'info');
                // 分析が継続中なら認識を再開
                setTimeout(() => {
                    if (this.isAndroidAnalyzing && this.androidRecognition) {
                        try {
                            this.androidRecognition.start();
                            this.addDebugLog('🔄 音声認識を再開しました', 'info');
                        } catch (error) {
                            this.addDebugLog(`❌ 再開エラー: ${error.message}`, 'error');
                            this.finishAndroidVoiceRecognition();
                        }
                    }
                }, 100);
            } else {
                // 1回認識なので、終了時は必ず分析完了処理を実行
                this.finishAndroidVoiceRecognition();
            }
        };
        
        recognition.onerror = (event) => {
            if (this.androidTimeoutId) {
                clearTimeout(this.androidTimeoutId);
            }
            this.addDebugLog(`❌ 音声認識エラー: ${event.error}`, 'error');
            this.updateStatus('❌ 音声認識エラー', 'error');
            this.finishAndroidVoiceRecognition();
        };
        
        // 音声認識開始
        try {
            recognition.start();
            this.addDebugLog('🎤 音声認識を開始しました', 'info');
        } catch (error) {
            this.addDebugLog(`❌ 音声認識開始エラー: ${error.message}`, 'error');
            this.updateStatus('❌ 音声認識開始失敗', 'error');
            this.isAndroidAnalyzing = false;
        }
    }

    /**
     * 🛑 Android音声認識を強制停止（即座に分析実行）
     */
    stopAndroidVoiceRecognition() {
        this.addDebugLog('🛑 Android音声認識を手動停止中...', 'warning');
        this.isAndroidAnalyzing = false;
        
        if (this.androidTimeoutId) {
            clearTimeout(this.androidTimeoutId);
            this.androidTimeoutId = null;
        }
        
        if (this.androidRecognition) {
            try {
                this.androidRecognition.stop();
                this.addDebugLog('✅ 音声認識停止コマンド送信完了', 'info');
            } catch (error) {
                this.addDebugLog(`⚠️ 音声認識停止エラー: ${error.message}`, 'error');
            }
        }
        
        // 停止時に即座に分析を実行
        this.addDebugLog('📊 手動停止時の分析を開始...', 'info');
        this.finishAndroidVoiceRecognition();
    }

    /**
     * 🏁 Android音声認識完了処理 + 評価分析（PC版と同じロジック）
     */
    finishAndroidVoiceRecognition() {
        this.addDebugLog('🏁 Android音声認識完了 - 評価分析開始', 'info');
        this.updateStatus('📊 分析中...', 'analyzing');
        
        // 認識状態をリセット
        this.isAndroidAnalyzing = false;
        
        try {
            // 期待される文章を取得
            const expectedSentence = this.getCurrentSentence();
            const recognizedText = this.recognizedText || '';
            
            console.log('🤖 Android分析開始:');
            console.log('  期待文:', expectedSentence);
            console.log('  認識文:', recognizedText);
            
            let analysisResult;
            
            if (!recognizedText || recognizedText.length === 0) {
                // 音声認識結果がない場合
                analysisResult = {
                    level: '❌ 音声未検出',
                    levelExplanation: '音声が認識されませんでした',
                    expectedSentence,
                    recognizedText: '',
                    contentAccuracy: 0,
                    verificationStatus: '音声認識失敗'
                };
            } else {
                // 正常に認識された場合の分析（PC版と同じロジック）
                const similarity = this.calculateTextSimilarity(expectedSentence, recognizedText);
                const expectedWordCount = expectedSentence ? expectedSentence.trim().split(/\s+/).length : 0;
                const actualWordCount = recognizedText.split(/\s+/).length;
                
                // 🕒 発話時間計算：タイムスタンプベース（利用可能時）→ 推定値（フォールバック）
                let speechDuration, calculationMethod;
                
                if (this.firstWordTime && this.lastWordTime && this.speechTimestamps.length > 0) {
                    // ⏱️ タイムスタンプベースの正確な発話時間計算
                    const rawTimeDiff = (this.lastWordTime - this.firstWordTime) / 1000;
                    speechDuration = Math.max(0.1, rawTimeDiff);
                    calculationMethod = 'タイムスタンプベース';
                    
                    // 詳細デバッグ情報
                    this.addDebugLog(`⏱️ タイムスタンプ詳細分析:`, 'info');
                    this.addDebugLog(`  - 認識回数: ${this.speechTimestamps.length}回`, 'info');
                    this.addDebugLog(`  - 最初の語時刻: ${((this.firstWordTime - this.recognitionStartTime) / 1000).toFixed(2)}秒後`, 'info');
                    this.addDebugLog(`  - 最後の語時刻: ${((this.lastWordTime - this.recognitionStartTime) / 1000).toFixed(2)}秒後`, 'info');
                    this.addDebugLog(`  - 計算された発話時間: ${speechDuration.toFixed(2)}秒`, 'info');
                    this.addDebugLog(`  - 語数: ${actualWordCount}語`, 'info');
                    this.addDebugLog(`  - 計算結果: ${(actualWordCount / speechDuration * 60).toFixed(1)}語/分`, 'info');
                    
                    // 異常値検出とフォールバック処理（改善版）
                    const preliminaryWordsPerMinute = (actualWordCount / speechDuration) * 60;
                    const isAbnormallyFast = preliminaryWordsPerMinute > 300; // 300語/分を超える場合は異常
                    const isAbnormallyShort = speechDuration < 0.5 && actualWordCount > 5; // 0.5秒未満で5語以上も異常
                    
                    if (isAbnormallyFast || isAbnormallyShort) {
                        this.addDebugLog(`⚠️ 異常値検出: ${preliminaryWordsPerMinute.toFixed(1)}語/分 (${speechDuration.toFixed(2)}秒で${actualWordCount}語)`, 'warning');
                        // 異常値の場合は推定値を使用
                        const fallbackDuration = actualWordCount / 3.0; // 平均3語/秒（より現実的）
                        this.addDebugLog(`🔄 フォールバックに切り替え: ${fallbackDuration.toFixed(2)}秒 → ${(actualWordCount / fallbackDuration * 60).toFixed(1)}語/分`, 'warning');
                        speechDuration = fallbackDuration;
                        calculationMethod = 'タイムスタンプベース→フォールバック（異常値検出）';
                    }
                } else {
                    // 🔄 フォールバック：従来の推定値計算
                    speechDuration = actualWordCount / 3.0; // 平均3語/秒に修正（より現実的）
                    calculationMethod = '推定値（フォールバック）';
                    this.addDebugLog(`⚠️ ${calculationMethod}: ${speechDuration.toFixed(2)}秒`, 'warning');
                }
                
                const wordsPerSecond = actualWordCount / speechDuration;
                const wordsPerMinute = wordsPerSecond * 60;
                
                console.log(`📊 Android発話速度分析（${calculationMethod}）:`, {
                    expectedWords: expectedWordCount,
                    actualWords: actualWordCount,
                    speechDuration: speechDuration.toFixed(2) + '秒',
                    wordsPerMinute: wordsPerMinute.toFixed(1) + '語/分',
                    method: calculationMethod
                });
                
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
                    // 内容が正しい場合のレベル評価（PC版と同じ基準）
                    if (wordsPerSecond < 1.33) {
                        level = '� 初心者レベル';
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
                    duration: speechDuration, // タイムスタンプベースまたは推定発話時間
                    calculationMethod, // 計算方法の記録
                    speechTimestamps: this.speechTimestamps, // タイムスタンプ詳細（デバッグ用）
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
            
            // 結果表示
            this.displayAndroidAnalysisResults(analysisResult);
            this.updateStatus('✅ Android分析完了', 'success');
            
        } catch (error) {
            console.error('🤖 Android分析エラー:', error);
            this.updateStatus(`❌ 分析エラー: ${error.message}`, 'error');
        }
    }

    /**
     * 📊 Android分析結果表示（PC版と同じ形式）
     */
    displayAndroidAnalysisResults(result) {
        console.log('📊 Android分析結果表示:', result);
        
        // PC版と同じ表示ロジック
        let contentVerificationHtml = '';
        
        if (!result.recognizedText) {
            // 音声認識失敗の場合
            contentVerificationHtml = `
                <div class="content-verification">
                    <div class="verification-item poor"><strong>認識失敗:</strong> 音声が認識されませんでした</div>
                    <div class="verification-item info"><strong>期待文章:</strong> "${result.expectedSentence}"</div>
                </div>
            `;
        } else {
            // 正常認識の場合（PC版と同じ）
            const accuracyClass = result.contentAccuracy >= 0.6 ? 'good' : 
                                 result.contentAccuracy >= 0.3 ? 'fair' : 'poor';
            
            contentVerificationHtml = `
                <div class="content-verification">
                    <div class="verification-item"><strong>期待文章:</strong> "${result.expectedSentence}"</div>
                    <div class="verification-item"><strong>認識結果:</strong> "${result.recognizedText}"</div>
                    <div class="verification-item ${accuracyClass}"><strong>一致度:</strong> ${(result.contentAccuracy * 100).toFixed(1)}%</div>
                </div>
            `;
        }
        
        // PC版と同じHTML構造（保存確認機能付き）
        const resultsHtml = `
            <div class="analysis-results">
                <h4>📊 発話分析結果 (Android)</h4>
                <div class="analysis-item">⏱️ 録音時間: ${result.duration ? result.duration.toFixed(2) : 'N/A'}秒</div>
                <div class="analysis-item">💬 単語数: ${result.expectedWordCount || 0} → ${result.actualWordCount || 0}</div>
                <div class="analysis-item">⚡ 発話速度: ${result.wordsPerMinute ? result.wordsPerMinute.toFixed(0) : 'N/A'} 語/分</div>
                <div class="analysis-item">🎯 評価: ${result.level} ${result.levelExplanation || ''}</div>
                ${contentVerificationHtml}
                <div class="progress-save-status">
                    <div id="progress-save-message-android">Android分析が完了しました</div>
                    <div class="save-confirmation-android" style="margin-top: 10px;">
                        <p style="margin: 5px 0; font-size: 12px; color: #555;">この結果を学習データに保存しますか？</p>
                        <div style="display: flex; gap: 8px; justify-content: center;">
                            <button id="save-yes-btn-android" class="voice-btn" style="background: #28a745; color: white; font-size: 11px; padding: 4px 12px;">✅ はい</button>
                            <button id="save-no-btn-android" class="voice-btn" style="background: #6c757d; color: white; font-size: 11px; padding: 4px 12px;">❌ いいえ</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Android用の結果表示エリアに表示
        const resultsContainer = document.getElementById('voice-analysis-results-android');
        if (resultsContainer) {
            resultsContainer.innerHTML = resultsHtml;
            console.log('✅ Android分析結果をHTML表示完了');
            
            // Android用保存確認ボタンのイベントリスナーを設定
            this.setupAndroidSaveConfirmationButtons(result);
        } else {
            console.warn('⚠️ voice-analysis-results-android要素が見つかりません');
            // フォールバックとして通常の結果エリアに表示
            const fallbackContainer = document.getElementById('voice-analysis-results');
            if (fallbackContainer) {
                fallbackContainer.innerHTML = resultsHtml;
                console.log('✅ フォールバック: 通常の結果エリアにAndroid分析結果を表示');
                
                // フォールバック時もイベントリスナーを設定
                this.setupAndroidSaveConfirmationButtons(result);
            }
        }
        
        // 📱 透過モード制御（分析モード継続中は透過を維持）
        const analyzeBtn = document.getElementById('voice-analyze-btn-android');
        const isAnalyzeMode = analyzeBtn && analyzeBtn.textContent === '停止';
        
        if (!isAnalyzeMode) {
            // 分析モードが終了した場合のみ透過解除
            this.setVoicePanelTransparency(false);
            console.log('📱 分析モード終了 - 透過解除');
        } else {
            console.log('📱 分析モード継続中 - 透過維持');
        }
    }

    /**
     * 📱 Android用保存確認ボタンのイベントリスナーを設定
     */
    setupAndroidSaveConfirmationButtons(analysisResult) {
        const saveYesBtn = document.getElementById('save-yes-btn-android');
        const saveNoBtn = document.getElementById('save-no-btn-android');
        const messageElement = document.getElementById('progress-save-message-android');
        
        if (saveYesBtn && saveNoBtn) {
            console.log('📱 Android保存確認ボタンのイベントリスナーを設定');
            
            // 「はい」ボタンのクリックイベント
            saveYesBtn.addEventListener('click', async () => {
                console.log('✅ Android: 学習データ保存を選択');
                
                // ボタンを無効化
                saveYesBtn.disabled = true;
                saveNoBtn.disabled = true;
                
                // 保存メッセージを更新
                if (messageElement) {
                    messageElement.innerHTML = '📊 Android学習データに保存中...';
                    messageElement.style.color = '#007bff';
                }
                
                // データを保存（PC版と同じメソッドを使用）
                await this.saveProgressData(analysisResult);
                
                // 確認ボタンを非表示
                const confirmationDiv = document.querySelector('.save-confirmation-android');
                if (confirmationDiv) {
                    confirmationDiv.style.display = 'none';
                }
            });
            
            // 「いいえ」ボタンのクリックイベント
            saveNoBtn.addEventListener('click', async () => {
                console.log('❌ Android: 学習データ保存をキャンセル');
                
                // ボタンを無効化
                saveYesBtn.disabled = true;
                saveNoBtn.disabled = true;
                
                // 保存しないメッセージを表示
                if (messageElement) {
                    messageElement.innerHTML = '❌ Android学習データには保存されませんでした';
                    messageElement.style.color = '#6c757d';
                }
                
                // 確認ボタンを非表示
                const confirmationDiv = document.querySelector('.save-confirmation-android');
                if (confirmationDiv) {
                    confirmationDiv.style.display = 'none';
                }
                
                // 🚫 一時的な分析結果データをクリア（PC版と同じ処理）
                await this.clearTemporaryAnalysisData(analysisResult);
                
                console.log('👋 Android: ユーザーが学習データ保存をキャンセルしました');
            });
        } else {
            console.warn('⚠️ Android保存確認ボタンが見つかりません');
        }
    }

    /**
     * 進捗ボタンのイベントリスナーを設定（動的対応）
     */
    setupProgressButtonListener() {
        const setupButton = () => {
            const progressBtn = document.getElementById('voice-progress-btn');
            this.addDebugLog(`🔍 PC進捗ボタン検索結果: ${progressBtn ? '見つかりました' : '見つかりません'}`, progressBtn ? 'success' : 'error');
            
            if (progressBtn && !progressBtn.hasAttribute('data-listener-added')) {
                progressBtn.addEventListener('click', () => {
                    this.addDebugLog('🎯 PC進捗ボタンがクリックされました！', 'info');
                    console.log('🎯 PC進捗ボタンクリック - showProgress()を呼び出します');
                    this.showProgress();
                });
                progressBtn.setAttribute('data-listener-added', 'true');
                console.log('✅ 学習進捗ボタンのイベントリスナーを設定しました');
                this.addDebugLog('✅ PC学習進捗ボタンのイベントリスナーを設定', 'success');
                return true;
            } else if (progressBtn && progressBtn.hasAttribute('data-listener-added')) {
                console.log('⚠️ PC進捗ボタンは既にイベントリスナーが設定済み');
                this.addDebugLog('⚠️ PC進捗ボタンは既にイベントリスナーが設定済み', 'warning');
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
     * 音声認識言語設定ボタンのイベントリスナーを設定（動的対応）
     */
    setupVoiceLanguageButtonListener() {
        const setupButton = () => {
            const languageBtn = document.getElementById('voice-language-btn');
            if (languageBtn && !languageBtn.hasAttribute('data-listener-added')) {
                languageBtn.addEventListener('click', () => this.showLanguageSettings());
                languageBtn.setAttribute('data-listener-added', 'true');
                console.log('✅ 音声言語設定ボタンのイベントリスナーを設定しました');
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
                        console.warn('⚠️ 音声言語設定ボタンが見つかりませんでした（最大試行回数に達しました）');
                    }
                }
            }, 500);
        }
    }
    
    /**
     * 🔧 音声言語設定パネルを表示
     */
    async showLanguageSettings() {
        console.log('🔧 音声言語設定パネルを表示します');
        
        const currentRecognitionLang = localStorage.getItem('voiceRecognitionLanguage') || 'en-US';
        const currentVoiceName = localStorage.getItem('selectedVoiceName') || 'デフォルト';
        
        const shouldChange = await this.showLanguageSettingsDialog(currentRecognitionLang, currentVoiceName);
        
        if (shouldChange) {
            // 設定変更が確認されたら、システムを再初期化
            console.log('🔄 音声システムを再初期化します');
            // 🔧 デバイス別音声認識再初期化
            if (this.isAndroid) {
                console.log('📱 Android用音声認識：再初期化はstartAndroidVoiceRecognitionで実行');
            } else {
                await this.initPCSpeechRecognition();
            }
            this.loadVoices();
        }
    }
    
    /**
     * 🔧 音声言語設定ダイアログ
     */
    showLanguageSettingsDialog(currentRecognitionLang, currentVoiceName) {
        return new Promise((resolve) => {
            // 既存のダイアログがある場合は削除
            const existingDialog = document.getElementById('language-settings-dialog');
            if (existingDialog) {
                existingDialog.remove();
            }

            const dialogHTML = `
                <div id="language-settings-dialog" style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0, 0, 0, 0.8); display: flex; align-items: center;
                    justify-content: center; z-index: 99999; font-family: Arial, sans-serif;
                ">
                    <div style="
                        background: white; padding: 25px; border-radius: 15px;
                        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); max-width: 90%; width: 450px;
                        text-align: center; margin: 20px;
                    ">
                        <div style="font-size: 50px; margin-bottom: 15px;">🔧</div>
                        <h3 style="margin: 0 0 20px 0; color: #333; font-size: 22px; font-weight: bold;">
                            音声言語設定
                        </h3>
                        <div style="text-align: left; margin-bottom: 25px;">
                            <div style="margin-bottom: 15px;">
                                <label style="display: block; margin-bottom: 8px; font-weight: bold; color: #555;">
                                    🎤 音声認識言語：
                                </label>
                                <select id="recognition-lang-select" style="
                                    width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;
                                    font-size: 14px; background: white;
                                ">
                                    <option value="en-US" ${currentRecognitionLang === 'en-US' ? 'selected' : ''}>
                                        🇺🇸 English (US) - 推奨
                                    </option>
                                    <option value="ja-JP" ${currentRecognitionLang === 'ja-JP' ? 'selected' : ''}>
                                        🇯🇵 日本語
                                    </option>
                                </select>
                            </div>
                            <div style="font-size: 12px; color: #666; margin-bottom: 20px;">
                                <strong>現在の音声合成：</strong> ${currentVoiceName}<br>
                                <small>※音声合成の変更は読み上げ時に自動で確認されます</small>
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; justify-content: center;">
                            <button id="save-language-settings-btn" style="
                                background: #007bff; color: white; border: none; padding: 12px 25px;
                                border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold;
                            ">💾 設定を保存</button>
                            <button id="cancel-language-settings-btn" style="
                                background: #6c757d; color: white; border: none; padding: 12px 25px;
                                border-radius: 8px; cursor: pointer; font-size: 16px;
                            ">❌ キャンセル</button>
                        </div>
                    </div>
                </div>
            `;

            document.body.insertAdjacentHTML('beforeend', dialogHTML);

            const saveBtn = document.getElementById('save-language-settings-btn');
            const cancelBtn = document.getElementById('cancel-language-settings-btn');
            const select = document.getElementById('recognition-lang-select');

            if (saveBtn) {
                saveBtn.addEventListener('click', () => {
                    const selectedLang = select.value;
                    localStorage.setItem('voiceRecognitionLanguage', selectedLang);
                    console.log(`💾 音声認識言語設定を保存: ${selectedLang}`);
                    
                    // 成功メッセージ
                    const successMsg = document.createElement('div');
                    successMsg.style.cssText = `
                        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        background: #28a745; color: white; padding: 15px 25px; border-radius: 8px;
                        z-index: 100000; font-size: 16px; font-weight: bold;
                    `;
                    successMsg.textContent = '✅ 設定を保存しました！';
                    document.body.appendChild(successMsg);
                    setTimeout(() => successMsg.remove(), 2000);
                    
                    document.getElementById('language-settings-dialog').remove();
                    resolve(true);
                });
            }

            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => {
                    document.getElementById('language-settings-dialog').remove();
                    resolve(false);
                });
            }
        });
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
            
            // 📏 前回の分析結果をクリアしパネルサイズをリセット
            const resultsContainer = document.getElementById('voice-analysis-results');
            if (resultsContainer) {
                resultsContainer.innerHTML = '';
            }
            this.resetPanelSize();
            
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true,
                    channelCount: 1
                    // sampleRateを削除: Android Chromeで問題を起こす可能性
                }
            });
            
            // � ストリーム参照を保存（Android対応）
            this.currentStream = stream;
            
            // �🔍 Android診断: stream詳細ログ
            console.log('🔍 Stream取得成功:', {
                streamId: stream.id,
                tracks: stream.getAudioTracks().map(track => ({
                    id: track.id,
                    label: track.label,
                    enabled: track.enabled,
                    readyState: track.readyState,
                    settings: track.getSettings()
                }))
            });
            
            // 🚨 Android Chrome特化: MediaRecorder設定最適化
            let mediaRecorderOptions = {};
            const isAndroidDevice = /Android/i.test(navigator.userAgent);
            
            if (isAndroidDevice) {
                // Android: mimeTypeを指定しない場合の方が安定することがある
                if (MediaRecorder.isTypeSupported('audio/webm')) {
                    mediaRecorderOptions.mimeType = 'audio/webm';
                } else {
                    console.log('🚨 Android: mimeTypeを指定せずにデフォルトを使用');
                    // mimeTypeを指定しない
                }
            } else {
                // PC/其他ブラウザ: より詳細なサポート診断
                console.log('🔍 PC版サポート状況診断:');
                const supportedTypes = [
                    'audio/webm;codecs=opus',
                    'audio/webm;codecs=vp8,opus',
                    'audio/webm',
                    'audio/mp4',
                    'audio/mpeg',
                    'audio/ogg;codecs=opus'
                ];
                
                supportedTypes.forEach(type => {
                    console.log(`  - ${type}: ${MediaRecorder.isTypeSupported(type)}`);
                });
                
                // 優先順位でmimeTypeを選択
                if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
                    mediaRecorderOptions.mimeType = 'audio/webm;codecs=opus';
                } else if (MediaRecorder.isTypeSupported('audio/webm')) {
                    mediaRecorderOptions.mimeType = 'audio/webm';
                } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                    mediaRecorderOptions.mimeType = 'audio/mp4';
                } else {
                    console.warn('⚠️ PC版: 適切なmimeTypeが見つかりません');
                    // mimeTypeを指定しない
                }
            }
            
            this.mediaRecorder = new MediaRecorder(stream, mediaRecorderOptions);
            
            // 🔍 Android診断: MediaRecorder設定確認
            console.log('🔍 MediaRecorder mimeType:', this.mediaRecorder.mimeType);
            console.log('🔍 MediaRecorder state:', this.mediaRecorder.state);
            
            // 🚨 Android緊急診断: サポート状況詳細チェック
            if (isAndroidDevice) {
                console.log('🚨 Android緊急診断開始:');
                console.log('  - webm;opus support:', MediaRecorder.isTypeSupported('audio/webm;codecs=opus'));
                console.log('  - webm support:', MediaRecorder.isTypeSupported('audio/webm'));
                console.log('  - mp4 support:', MediaRecorder.isTypeSupported('audio/mp4'));
                console.log('  - mpeg support:', MediaRecorder.isTypeSupported('audio/mpeg'));
                console.log('  - 最終選択mimeType:', this.mediaRecorder.mimeType);
                console.log('  - User Agent:', navigator.userAgent.substring(0, 100));
                
                // Android向け追加設定
                console.log('  - Stream active:', stream.active);
                console.log('  - Track count:', stream.getTracks().length);
            }
            
            // 🔧 新しい録音用のチャンク配列を初期化
            const audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                    console.log(`📦 PC版録音データチャンク受信: ${event.data.size} bytes, 合計: ${audioChunks.length}個`);
                } else {
                    console.warn('⚠️ PC版録音: 空のデータチャンクを受信');
                }
            };
            
            this.mediaRecorder.onstop = () => {
                // 🔧 MediaRecorderと同じmimeTypeでBlobを作成（Android対応）
                const mimeType = this.mediaRecorder.mimeType || 'audio/webm';
                this.recordedBlob = new Blob(audioChunks, { type: mimeType });
                
                console.log('🎤 PC版録音データ作成:', {
                    blobSize: this.recordedBlob.size,
                    blobType: this.recordedBlob.type,
                    chunksCount: audioChunks.length,
                    chunksDetails: audioChunks.map((chunk, index) => ({
                        index,
                        size: chunk.size,
                        type: chunk.type
                    }))
                });
                
                if (this.recordedBlob.size === 0) {
                    console.error('❌ PC版録音失敗: Blobサイズが0です');
                    this.updateStatus('❌ 録音データが空です', 'error');
                } else {
                    console.log('✅ PC版録音成功: 再生準備完了');
                    this.updateStatus('✅ 録音完了', 'success');
                }
                
                this.stopVolumeMonitoring();
                stream.getTracks().forEach(track => track.stop());
                this.updateRecordingUI(false);
                
                // 🎯 録音完了時に即座に分析実行
                this.analyzeRecording();
            };
            
            // Android Chrome向けエラーハンドリング
            this.mediaRecorder.onerror = (event) => {
                console.error('❌ MediaRecorder error:', event.error);
                this.updateStatus('録音エラーが発生しました', 'error');
                this.isRecording = false;
                this.updateRecordingUI(false);
            };
            
            // 録音開始
            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingStartTime = Date.now();
            
        // 🎤 録音専用音声認識を開始（testVoiceRecognition成功設定を移植）
        this.startRecordingVoiceRecognition();            // UI更新
            this.updateRecordingUI(true);
            this.startRecordingTimer();
            this.setupVolumeMonitoring(stream);
            
            this.updateStatus('🎤 録音・認識開始...', 'recording');
            
        } catch (error) {
            // 📱 Android対応: 詳細エラー診断
            console.error('❌ 録音開始エラー:', error);
            console.error('❌ エラー名:', error.name);
            console.error('❌ エラーメッセージ:', error.message);
            
            let userFriendlyMessage = '録音エラーが発生しました';
            
            if (error.name === 'NotAllowedError') {
                userFriendlyMessage = 'マイクアクセスが許可されていません。ブラウザの設定を確認してください。';
                console.log('🔧 対処法: Chromeの場合、アドレスバーの左のアイコンをタップしてマイクを許可してください');
                console.log('🔧 または設定 > サイト設定 > マイク でこのサイトを許可してください');
            } else if (error.name === 'NotFoundError') {
                userFriendlyMessage = 'マイクが見つかりません。デバイスにマイクが接続されているか確認してください。';
            } else if (error.name === 'NotSupportedError') {
                userFriendlyMessage = 'お使いのブラウザは音声録音をサポートしていません。';
                console.log('🔧 対処法: Chrome、Firefox、Safari等の最新版をお使いください');
            } else if (error.name === 'SecurityError') {
                userFriendlyMessage = 'セキュリティエラー: HTTPS接続が必要です。';
                console.log('🔧 現在のプロトコル:', window.location.protocol);
                console.log('🔧 対処法: https://でアクセスしてください');
            } else if (error.name === 'AbortError') {
                userFriendlyMessage = '録音が中断されました。';
            }
            
            // セキュアなエラーハンドリング
            if (window.errorHandler) {
                window.errorHandler.handleError(error, { action: 'voice_recording_start' }, 'system.microphone_error');
            } else {
                console.error('録音開始エラー:', error);
            }
            this.updateStatus(`❌ ${userFriendlyMessage}`, 'error');
            
            // マイクアクセス状態をリセット
            this.isMicrophoneAllowed = false;
        }
    }
    
    /**
     * 録音停止
     */
    stopRecording() {
        console.log('stopRecording called, MediaRecorder state:', this.mediaRecorder?.state);
        
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            // Android Chrome向けにstopイベントリスナーを設定
            this.mediaRecorder.addEventListener('stop', () => {
                console.log('✅ MediaRecorder stopped successfully');
                this.isRecording = false;
                
                // ストリームトラックも確実に停止
                if (this.currentStream) {
                    this.currentStream.getTracks().forEach(track => {
                        console.log('Stopping track:', track.kind, track.readyState);
                        track.stop();
                    });
                }
            }, { once: true });
            
            console.log('Stopping MediaRecorder...');
            this.mediaRecorder.stop();
            this.stopRecordingTimer();
        }
        
        // 🎤 録音用音声認識停止（testVoiceRecognition対応版）
        if (this.recordingRecognition && this.isRecognitionActive) {
            try {
                console.log('🔚 録音用音声認識停止コマンド送信');
                
                // タイムアウトをクリア
                if (this.recognitionTimeoutId) {
                    clearTimeout(this.recognitionTimeoutId);
                    this.recognitionTimeoutId = null;
                }
                
                this.recordingRecognition.stop();
                
                // ⏳ Android向け：認識結果受信の追加待機時間
                setTimeout(() => {
                    if (this.isRecognitionActive) {
                        console.log('🔚 音声認識がまだアクティブです。強制終了を実行');
                        this.isRecognitionActive = false;
                    }
                    
                    // 📊 認識結果の最終確認
                    console.log('🎯 最終認識結果確認:', {
                        text: this.recognizedText.trim(),
                        length: this.recognizedText ? this.recognizedText.length : 0,
                        platform: /Android/i.test(navigator.userAgent) ? 'Android' : 'PC'
                    });
                    
                    if (!this.recognizedText.trim()) {
                        console.warn('⚠️ 認識結果が空です - 原因調査が必要');
                    }
                }, 2000); // Android対応：2秒の追加待機
                
            } catch (error) {
                console.warn('⚠️ 録音用音声認識停止エラー:', error);
                this.isRecognitionActive = false;
            }
        }
        
        this.updateStatus('🔄 録音データ準備中...', 'info');
    }
    
    /**
     * 🎤 録音用音声認識（testVoiceRecognition成功設定を完全移植）
     * 🚨 緊急修正: testVoiceRecognitionの完全同期版 + 言語設定確認機能
     */
    async startRecordingVoiceRecognition() {
        this.addDebugLog('🗣️ 録音用音声認識を開始します...', 'info');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ Web Speech API が利用できません', 'error');
            return;
        }
        
        // 🔍 デバイス別音声認識言語設定を確認
        const isAndroid = /Android/i.test(navigator.userAgent);
        const storageKey = isAndroid ? 'voiceRecognitionLanguage_Android' : 'voiceRecognitionLanguage_PC';
        let recognitionLang = localStorage.getItem(storageKey) || 'en-US';
        console.log(`🔍 保存された${isAndroid ? 'Android' : 'PC'}音声認識言語: ${recognitionLang}`);
        
        // 🚨 日本語設定が保存されている場合の警告
        if (recognitionLang.startsWith('ja')) {
            console.log('🚨 日本語音声認識が設定されています！警告ダイアログを表示します');
            const shouldSwitchToEnglish = await this.showRecognitionLanguageWarningDialog();
            if (shouldSwitchToEnglish) {
                recognitionLang = 'en-US';
                localStorage.setItem(storageKey, 'en-US');
                console.log(`✅ ${isAndroid ? 'Android' : 'PC'}音声認識を英語に変更しました`);
            } else {
                console.log('👌 日本語音声認識を継続します');
            }
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recordingRecognition = new SpeechRecognition();
        
        // 🚨 緊急修正: testVoiceRecognitionと完全同一設定 + 速い話し方対応
        if (isAndroid) {
            this.addDebugLog('📱 Android Chrome用設定を適用', 'info');
            this.recordingRecognition.continuous = true; // 連続認識で速い話し方に対応
            this.recordingRecognition.interimResults = true;
            this.recordingRecognition.lang = recognitionLang;
            this.recordingRecognition.maxAlternatives = 5; // 候補数を増やして精度向上
        } else {
            this.recordingRecognition.continuous = true; // PC版も連続認識に変更
            this.recordingRecognition.interimResults = true;
            this.recordingRecognition.lang = recognitionLang;
            this.recordingRecognition.maxAlternatives = 3; // PC版も候補数を増加
        }
        
        // 📈 速い話し方対応のログ
        console.log('� 高速音声認識設定:', {
            continuous: this.recordingRecognition.continuous,
            interimResults: this.recordingRecognition.interimResults,
            maxAlternatives: this.recordingRecognition.maxAlternatives,
            lang: this.recordingRecognition.lang
        });
        
        this.addDebugLog(`🔍 認識状態: lang=${this.recordingRecognition.lang}, active=false`, 'info');
        
        // 🚨 タイムアウト設定: 速い話し方に対応
        const timeoutDuration = isAndroid ? 20000 : 15000; // Android: 20秒、PC: 15秒に延長
        this.recognitionTimeoutId = setTimeout(() => {
            this.recordingRecognition.stop();
            this.addDebugLog(`⏰ 音声認識がタイムアウトしました（${timeoutDuration/1000}秒）`, 'warning');
        }, timeoutDuration);
        
        // 🚨 緊急修正: testVoiceRecognitionのイベントハンドラーを完全複製
        this.recordingRecognition.onstart = () => {
            this.addDebugLog('✅ 音声認識start()コマンド送信完了', 'success');
            this.addDebugLog('🎤 音声認識開始イベント発生', 'success');
            this.isRecognitionActive = true;
            if (isAndroid) {
                this.addDebugLog('🎤 何か話してください（15秒以内）...', 'info');
            } else {
                this.addDebugLog('🎤 何か話してください（10秒以内）...', 'info');
            }
        };
        
        this.recordingRecognition.onresult = (event) => {
            clearTimeout(this.recognitionTimeoutId);
            
            this.addDebugLog('🎯 音声認識結果イベント発生', 'info');
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence || 0;
                
                if (result.isFinal) {
                    this.recognizedText = transcript; // 既存のシステムに合わせて保存
                    this.addDebugLog(`✅ 認識結果（確定）: "${transcript}"`, 'success');
                    this.addDebugLog(`📊 信頼度: ${(confidence * 100).toFixed(1)}%`, 'info');
                    
                    // 確定結果を確実に保存
                    console.log('✅ 確定結果保存:', transcript);
                } else {
                    this.addDebugLog(`🔄 認識結果（途中）: "${transcript}"`, 'info');
                    
                    // プラットフォーム別の中間結果処理
                    if (isAndroid) {
                        this.addDebugLog('📱 Android: 中間結果を記録', 'info');
                        // Android: 中間結果も保存（最終結果が来ない場合の対策）
                        if (!this.recognizedText || this.recognizedText.trim().length === 0) {
                            this.recognizedText = transcript;
                            console.log('� Android中間結果保存:', this.recognizedText);
                        }
                    } else {
                        // PC: 中間結果も一時保存
                        if (!this.recognizedText || this.recognizedText.trim().length === 0) {
                            this.recognizedText = transcript;
                            console.log('💻 PC中間結果保存:', this.recognizedText);
                        }
                    }
                }
            }
        };
        
        this.recordingRecognition.onend = () => {
            clearTimeout(this.recognitionTimeoutId);
            this.addDebugLog('🔚 音声認識終了イベント発生', 'info');
            this.isRecognitionActive = false;
            
            if (isAndroid) {
                this.addDebugLog('📱 Android: 認識終了時の特別チェック', 'info');
            }
            
            this.addDebugLog('🔚 音声認識終了処理完了', 'info');
        };
        
        this.recordingRecognition.onerror = (event) => {
            clearTimeout(this.recognitionTimeoutId);
            this.addDebugLog(`❌ 音声認識エラー: ${event.error}`, 'error');
            this.isRecognitionActive = false;
            
            if (isAndroid) {
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
        
        // 🚨 緊急修正: testVoiceRecognitionと同一の開始処理
        try {
            this.recordingRecognition.start();
            this.addDebugLog('🚀 録音用音声認識start()実行完了', 'success');
        } catch (error) {
            this.addDebugLog(`❌ 音声認識開始失敗: ${error.message}`, 'error');
        }
    }
    
    /**
     * 録音再生
     */
    playRecording() {
        // 📊 詳細デバッグ情報を表示
        console.log('🔍 PC版再生デバッグ情報:', {
            recordedBlob: this.recordedBlob,
            blobSize: this.recordedBlob ? this.recordedBlob.size : 'null',
            blobType: this.recordedBlob ? this.recordedBlob.type : 'null',
            audioChunks: this.audioChunks ? this.audioChunks.length : 'null',
            isAndroid: /Android/i.test(navigator.userAgent)
        });
        
        if (!this.recordedBlob) {
            this.updateStatus('❌ 再生する録音がありません', 'error');
            console.log('❌ PC版再生失敗: recordedBlobが存在しません');
            return;
        }
        
        if (this.recordedBlob.size === 0) {
            this.updateStatus('❌ 録音データが空です', 'error');
            console.log('❌ PC版再生失敗: recordedBlobのサイズが0です');
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
        
        // 🚨 PC版対応: Blobの内容詳細検証
        console.log('🔊 PC版Blob詳細検証:', {
            blobSize: this.recordedBlob.size,
            blobType: this.recordedBlob.type,
            audioUrl: audioUrl,
            userAgent: navigator.userAgent.substring(0, 80),
            supportedTypes: {
                webm: this.currentAudio.canPlayType('audio/webm'),
                webmOpus: this.currentAudio.canPlayType('audio/webm;codecs=opus'),
                ogg: this.currentAudio.canPlayType('audio/ogg'),
                mp4: this.currentAudio.canPlayType('audio/mp4')
            }
        });
        
        // 🔧 Blob URLの有効性テスト
        fetch(audioUrl).then(response => {
            return response.arrayBuffer();
        }).then(arrayBuffer => {
            console.log('✅ Blob URL読み込み成功:', {
                contentType: this.recordedBlob.type,
                dataSize: arrayBuffer.byteLength,
                firstBytes: new Uint8Array(arrayBuffer.slice(0, 16))
            });
        }).catch(error => {
            console.error('❌ Blob URL読み込み失敗:', error);
        });
        
        // 🚨 PC版対応: 詳細ログとエラーハンドリング
        console.log('🔊 PC版再生準備:', {
            blobSize: this.recordedBlob.size,
            blobType: this.recordedBlob.type,
            audioUrl: audioUrl.substring(0, 50) + '...',
            userAgent: navigator.userAgent.substring(0, 80)
        });
        
        this.currentAudio.onloadstart = () => {
            this.updateStatus('🔊 録音再生中...', 'playing');
            console.log('✅ PC版音声読み込み開始');
        };
        
        this.currentAudio.onloadedmetadata = () => {
            console.log('✅ PC版音声メタデータ読み込み完了:', {
                duration: this.currentAudio.duration,
                readyState: this.currentAudio.readyState
            });
        };
        
        this.currentAudio.oncanplay = () => {
            console.log('✅ PC版音声再生準備完了', {
                readyState: this.currentAudio.readyState,
                networkState: this.currentAudio.networkState
            });
        };
        
        this.currentAudio.oncanplaythrough = () => {
            console.log('✅ PC版音声完全読み込み完了');
        };
        
        this.currentAudio.onplaying = () => {
            console.log('✅ PC版音声再生開始');
        };
        
        this.currentAudio.onsuspend = () => {
            console.warn('⚠️ PC版音声読み込み一時停止');
        };
        
        this.currentAudio.onstalled = () => {
            console.warn('⚠️ PC版音声読み込み停止');
        };
        
        this.currentAudio.onabort = () => {
            console.warn('⚠️ PC版音声読み込み中断');
        };
        
        this.currentAudio.onended = () => {
            this.updateStatus('✅ 再生完了', 'success');
            console.log('✅ PC版音声再生完了');
            // 🔧 再生完了後にBlobURLを解放
            URL.revokeObjectURL(audioUrl);
            this.currentAudio = null;
        };
        
        this.currentAudio.onerror = (error) => {
            this.updateStatus('❌ 再生エラー', 'error');
            console.error('❌ PC版音声再生エラー:', error);
            console.error('❌ エラー詳細:', {
                error: error,
                audioElement: this.currentAudio,
                audioUrl: audioUrl,
                blobInfo: {
                    size: this.recordedBlob.size,
                    type: this.recordedBlob.type
                }
            });
            URL.revokeObjectURL(audioUrl);
            this.currentAudio = null;
        };
        
        // 音声読み込み開始
        this.currentAudio.load();
        
        // 再生開始
        this.currentAudio.play().then(() => {
            console.log('✅ PC版音声再生開始成功');
        }).catch(error => {
            console.error('❌ PC版音声再生開始失敗:', error);
            this.updateStatus('❌ 再生開始失敗', 'error');
        });
    }
    
    /**
     * 現在の例文を音声合成で読み上げ
     */
    async speakSentence() {
        // 🔍 デバッグ：動的エリアと静的スロットの内容を比較
        this.debugCompareAreas();
        
        const sentence = this.getCurrentSentence();
        
        if (!sentence) {
            this.updateStatus('❌ 読み上げる例文がありません', 'error');
            // 📱 透過モード解除（例文がない場合）
            this.setVoicePanelTransparency(false);
            return;
        }
        
        // 既存の音声を停止
        speechSynthesis.cancel();
        
        // 🔄 音声リストを確実に読み込む
        let availableVoices = speechSynthesis.getVoices();
        console.log(`🔍 初回音声取得: ${availableVoices.length}個`);
        
        // 音声が読み込まれていない場合、少し待つ
        if (availableVoices.length === 0) {
            console.log('⏳ 音声リストの読み込みを待機中...');
            await new Promise(resolve => {
                const checkVoices = () => {
                    availableVoices = speechSynthesis.getVoices();
                    if (availableVoices.length > 0) {
                        console.log(`✅ 音声リスト読み込み完了: ${availableVoices.length}個`);
                        resolve();
                    } else {
                        setTimeout(checkVoices, 100);
                    }
                };
                checkVoices();
            });
        }
        
        this.currentUtterance = new SpeechSynthesisUtterance(sentence);
        
        // 音声設定 - 女性の英語音声を優先選択
        console.log('🔍 利用可能な音声一覧:', availableVoices.map(v => `${v.name} (${v.lang}) - ${v.gender || 'unknown'}`));
        
        // 保存された音声設定を確認
        const savedVoiceName = localStorage.getItem('selectedVoiceName');
        let selectedVoice = null;
        
        console.log(`🔍 保存された音声名: ${savedVoiceName || 'なし'}`);
        
        if (savedVoiceName) {
            selectedVoice = availableVoices.find(voice => voice.name === savedVoiceName);
            if (selectedVoice) {
                console.log(`💾 保存された音声を使用: ${selectedVoice.name} (${selectedVoice.lang})`);
                
                // 🚨 日本語音声が選択されている場合の警告
                if (selectedVoice.lang.startsWith('ja')) {
                    console.log('🚨 日本語音声が検出されました！警告ダイアログを表示します');
                    const shouldSwitchToEnglish = await this.showLanguageWarningDialog();
                    if (shouldSwitchToEnglish) {
                        selectedVoice = null; // 英語音声を自動選択させる
                        localStorage.removeItem('selectedVoiceName'); // 保存された設定をクリア
                        console.log('✅ 英語音声に変更しました');
                    } else {
                        console.log('👌 日本語音声を継続します');
                    }
                }
            }
        }
        
        // 自動選択の場合の詳細ログ
        if (!selectedVoice) {
            console.log('🔍 自動音声選択を開始...');
            
            // デフォルト音声を確認
            const defaultVoice = availableVoices[0];
            if (defaultVoice) {
                console.log(`📢 デフォルト音声: ${defaultVoice.name} (${defaultVoice.lang})`);
                
                // デフォルト音声が日本語の場合の警告
                if (defaultVoice.lang.startsWith('ja')) {
                    console.log('🚨 デフォルト音声が日本語です！警告ダイアログを表示します');
                    const shouldSwitchToEnglish = await this.showLanguageWarningDialog();
                    if (!shouldSwitchToEnglish) {
                        selectedVoice = defaultVoice;
                        localStorage.setItem('selectedVoiceName', defaultVoice.name);
                        console.log('👌 日本語音声を継続し、保存しました');
                    }
                }
            }
        }
        
        // 英語音声を自動選択
        if (!selectedVoice) {
            // 女性の英語音声を最優先で探す
            selectedVoice = availableVoices.find(voice => 
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
                selectedVoice = availableVoices.find(voice => voice.lang.startsWith('en'));
            }
            
            // 英語音声を見つけた場合、保存しておく
            if (selectedVoice) {
                localStorage.setItem('selectedVoiceName', selectedVoice.name);
                console.log(`💾 英語音声を保存: ${selectedVoice.name}`);
            }
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
            // 📱 透過モード解除（読み上げ終了）
            this.setVoicePanelTransparency(false);
        };
        
        this.currentUtterance.onerror = (event) => {
            this.updateStatus(`❌ 読み上げエラー: ${event.error}`, 'error');
            // 📱 透過モード解除（読み上げエラー時）
            this.setVoicePanelTransparency(false);
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
        
        // 📱 透過モード解除（すべて停止時）
        this.setVoicePanelTransparency(false);
        
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
            
            // 🎤 音声認識結果の最終取得のため待機
            const isAndroid = /Android/i.test(navigator.userAgent);
            const waitTime = isAndroid ? 4000 : 1500; // Android: 4秒、PC: 1.5秒
            console.log(`⏳ 音声認識結果待機中... (${waitTime}ms, ${isAndroid ? 'Android' : 'PC'})`);
            await new Promise(resolve => setTimeout(resolve, waitTime));
            
            // 待機後の認識結果確認
            console.log('🔧 待機後認識結果:', {
                text: this.recognizedText,
                length: this.recognizedText ? this.recognizedText.length : 0,
                platform: isAndroid ? 'Android' : 'PC'
            });
            
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            const audioContext = new AudioContextClass();
            
            const arrayBuffer = await this.recordedBlob.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            // 期待される文章を取得
            const expectedSentence = this.getCurrentSentence();
            const recognizedText = this.recognizedText.trim();
            
            console.log('� 分析開始 - 基本情報:');
            console.log('�📝 期待文章:', expectedSentence);
            console.log('🎯 認識結果 (長さ: ' + recognizedText.length + '):', recognizedText);
            console.log('🎯 生の認識結果:', JSON.stringify(this.recognizedText));
            console.log('🎯 認識アクティブ状態:', this.isRecognitionActive);
            console.log('📱 デバイス情報:', navigator.userAgent.substring(0, 80));
            console.log('🎤 マイク許可状態:', this.isMicrophoneAllowed);
            
            // 🔍 音声認識失敗の詳細診断
            if (!recognizedText || recognizedText.length === 0) {
                console.warn('⚠️ 音声認識失敗の詳細診断を開始');
                console.log('🔍 診断項目:');
                console.log('  - 音声認識オブジェクト存在:', !!this.recognition);
                console.log('  - 最終認識状態:', this.isRecognitionActive);
                console.log('  - 録音データサイズ:', this.recordedBlob ? this.recordedBlob.size : 'なし');
                console.log('  - 期待文章存在:', !!expectedSentence && expectedSentence.length > 0);
                console.log('  - ブラウザサポート:', !!(window.SpeechRecognition || window.webkitSpeechRecognition));
                console.log('  - オンライン状態:', navigator.onLine);
                console.log('  - プロトコル:', window.location.protocol);
                
                if (/Android/i.test(navigator.userAgent)) {
                    console.log('📱 Android特有の診断:');
                    console.log('  - Chrome for Android:', /Chrome/i.test(navigator.userAgent));
                    console.log('  - WebView:', /wv/i.test(navigator.userAgent));
                    console.log('  - バージョン:', navigator.userAgent.match(/Chrome\/(\d+)/)?.[1] || '不明');
                }
            }
            
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
                
                // 🎯 実際の発話時間を計算（無音部分を除外）
                const speechDuration = this.calculateActualSpeechDuration(audioBuffer);
                const totalDuration = audioBuffer.duration; // 録音全体時間（比較用）
                
                console.log('🎯 発話時間分析:', {
                    totalRecordingTime: totalDuration.toFixed(2) + '秒',
                    actualSpeechTime: speechDuration.toFixed(2) + '秒',
                    silenceRatio: ((totalDuration - speechDuration) / totalDuration * 100).toFixed(1) + '%'
                });
                
                const expectedWordCount = expectedSentence ? expectedSentence.trim().split(/\s+/).length : 0;
                const actualWordCount = recognizedText.split(/\s+/).length;
                
                // 🚀 実際の発話時間で語数/分を計算
                const wordsPerSecond = actualWordCount / speechDuration;
                const wordsPerMinute = wordsPerSecond * 60;
                
                console.log('📊 発話速度分析:', {
                    expectedWords: expectedWordCount,
                    actualWords: actualWordCount,
                    speechDuration: speechDuration.toFixed(2) + '秒',
                    wordsPerMinute: wordsPerMinute.toFixed(1) + '語/分'
                });
                
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
                    duration: speechDuration, // 実際の発話時間
                    totalRecordingDuration: totalDuration, // 録音全体時間（参考用）
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
     * 🎯 実際の発話時間を計算（無音部分を除外）
     * 録音開始/終了時の無音を除いて、実際に話している時間のみを測定
     */
    calculateActualSpeechDuration(audioBuffer) {
        const channelData = audioBuffer.getChannelData(0);
        const sampleRate = audioBuffer.sampleRate;
        const totalSamples = channelData.length;
        
        // 音声検出の閾値（実験的に調整）
        const silenceThreshold = 0.01; // 無音判定の閾値
        const windowSize = Math.floor(sampleRate * 0.1); // 100msのウィンドウ
        
        // 開始点を検出（最初に音声が始まる点）
        let speechStart = 0;
        for (let i = 0; i < totalSamples - windowSize; i += windowSize) {
            let windowEnergy = 0;
            for (let j = i; j < i + windowSize; j++) {
                windowEnergy += Math.abs(channelData[j]);
            }
            const avgEnergy = windowEnergy / windowSize;
            
            if (avgEnergy > silenceThreshold) {
                speechStart = i;
                break;
            }
        }
        
        // 終了点を検出（最後に音声が終わる点）
        let speechEnd = totalSamples;
        for (let i = totalSamples - windowSize; i >= 0; i -= windowSize) {
            let windowEnergy = 0;
            for (let j = i; j < i + windowSize && j < totalSamples; j++) {
                windowEnergy += Math.abs(channelData[j]);
            }
            const avgEnergy = windowEnergy / windowSize;
            
            if (avgEnergy > silenceThreshold) {
                speechEnd = i + windowSize;
                break;
            }
        }
        
        // 実際の発話時間を計算
        const speechSamples = Math.max(0, speechEnd - speechStart);
        const speechDuration = speechSamples / sampleRate;
        
        console.log('🎯 発話時間検出詳細:', {
            totalDuration: (totalSamples / sampleRate).toFixed(2) + '秒',
            speechStart: (speechStart / sampleRate).toFixed(2) + '秒',
            speechEnd: (speechEnd / sampleRate).toFixed(2) + '秒',
            speechDuration: speechDuration.toFixed(2) + '秒',
            silenceThreshold: silenceThreshold
        });
        
        // 最小発話時間の保証（極端に短い場合は録音全体時間の30%を使用）
        const minDuration = (totalSamples / sampleRate) * 0.3;
        return Math.max(speechDuration, minDuration);
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
                    <div id="progress-save-message">分析が完了しました</div>
                    <div class="save-confirmation" style="margin-top: 10px;">
                        <p style="margin: 5px 0; font-size: 12px; color: #555;">この結果を学習データに保存しますか？</p>
                        <div style="display: flex; gap: 8px; justify-content: center;">
                            <button id="save-yes-btn" class="voice-btn" style="background: #28a745; color: white; font-size: 11px; padding: 4px 12px;">✅ はい</button>
                            <button id="save-no-btn" class="voice-btn" style="background: #6c757d; color: white; font-size: 11px; padding: 4px 12px;">❌ いいえ</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const resultsContainer = document.getElementById('voice-analysis-results');
        if (resultsContainer) {
            resultsContainer.innerHTML = resultsHtml;
        }
        
        // 🎯 分析結果表示後にパネル位置を調整
        this.adjustPanelPosition();
        
        // 📏 分析結果表示時にパネルを拡張
        this.expandPanelForResults();
        
        // 🎯 保存確認ボタンのイベントリスナーを設定
        this.setupSaveConfirmationButtons(analysis);
        
        this.updateStatus('✅ 分析完了', 'success');
    }
    
    /**
     * 保存確認ボタンのイベントリスナーを設定
     */
    setupSaveConfirmationButtons(analysisResult) {
        const saveYesBtn = document.getElementById('save-yes-btn');
        const saveNoBtn = document.getElementById('save-no-btn');
        const messageElement = document.getElementById('progress-save-message');
        
        if (saveYesBtn && saveNoBtn) {
            // 「はい」ボタンのクリックイベント
            saveYesBtn.addEventListener('click', async () => {
                // ボタンを無効化
                saveYesBtn.disabled = true;
                saveNoBtn.disabled = true;
                
                // 保存メッセージを更新
                if (messageElement) {
                    messageElement.innerHTML = '📊 学習データに保存中...';
                    messageElement.style.color = '#007bff';
                }
                
                // データを保存
                await this.saveProgressData(analysisResult);
                
                // 確認ボタンを非表示
                const confirmationDiv = document.querySelector('.save-confirmation');
                if (confirmationDiv) {
                    confirmationDiv.style.display = 'none';
                }
            });
            
            // 「いいえ」ボタンのクリックイベント
            saveNoBtn.addEventListener('click', async () => {
                // ボタンを無効化
                saveYesBtn.disabled = true;
                saveNoBtn.disabled = true;
                
                // 保存しないメッセージを表示
                if (messageElement) {
                    messageElement.innerHTML = '❌ 学習データには保存されませんでした';
                    messageElement.style.color = '#6c757d';
                }
                
                // 確認ボタンを非表示
                const confirmationDiv = document.querySelector('.save-confirmation');
                if (confirmationDiv) {
                    confirmationDiv.style.display = 'none';
                }
                
                // 🚫 一時的な分析結果データをクリア（グラフから除外するため）
                await this.clearTemporaryAnalysisData(analysisResult);
                
                console.log('👋 ユーザーが学習データ保存をキャンセルしました');
            });
        }
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
                messageElement.innerHTML = '✅ 学習データに保存完了しました！';
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
     * 音声パネルの位置を画面内に調整
     * 分析結果表示時に上に突き抜けないようにする
     */
    /**
     * 音声パネルの位置を画面内に調整
     * 📱 モバイル対応: 分析結果表示時に上に突き抜けないようにする
     */
    adjustPanelPosition() {
        const panel = document.getElementById('voice-control-panel');
        if (!panel) return;
        
        // 📱 モバイルデバイス検出
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                         window.innerWidth <= 768;
        
        console.log('📱 デバイス判定:', isMobile ? 'モバイル' : 'PC');
        console.log('🔍 画面サイズ:', window.innerWidth, 'x', window.innerHeight);
        
        // パネルの現在のサイズと位置を取得
        const panelRect = panel.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const windowWidth = window.innerWidth;
        
        console.log('📊 パネル位置:', {
            top: panelRect.top,
            bottom: panelRect.bottom,
            left: panelRect.left,
            right: panelRect.right,
            width: panelRect.width,
            height: panelRect.height
        });
        
        // 📱 モバイル専用調整
        if (isMobile) {
            // 縦画面と横画面で異なる配置
            const isPortrait = window.innerHeight > window.innerWidth;
            
            panel.style.position = 'fixed';
            panel.style.zIndex = '9999';
            
            if (isPortrait) {
                // 縦画面：右下に小さく配置
                panel.style.top = 'auto';
                panel.style.bottom = '20px';
                panel.style.left = 'auto';
                panel.style.right = '10px';
                panel.style.maxWidth = '140px';
                panel.style.maxHeight = '180px';
                console.log('📱 縦画面調整: right=10px, bottom=20px');
            } else {
                // 横画面：音声学習ボタンの下の行に配置
                panel.style.position = 'fixed';
                panel.style.top = '130px';     
                panel.style.bottom = 'auto';
                panel.style.left = 'auto';     
                panel.style.right = '20px';    
                panel.style.transform = 'none'; 
                panel.style.maxWidth = '250px';
                panel.style.maxHeight = `${windowHeight - 90}px`; // 4割縦に伸ばすため90pxに変更
                
                // 強制的にleftを無効化
                panel.style.removeProperty('left');
                panel.style.setProperty('right', '20px', 'important');
                panel.style.setProperty('top', '130px', 'important');
                panel.style.setProperty('max-height', `${windowHeight - 90}px`, 'important');
                
                console.log('📱 横画面調整完了: top=130px, right=20px, height=' + (windowHeight - 90) + 'px');
            }
            
            return;
        }
        
        // PC版の調整（従来通り）
        // パネルの上端が画面外に出ている場合
        if (panelRect.top < 0) {
            // 上端が0になるよう調整
            const currentTop = parseInt(panel.style.top || '120px');
            const adjustment = Math.abs(panelRect.top) + 10; // 10px余白
            panel.style.top = `${currentTop + adjustment}px`;
            
            console.log(`🎯 PC調整（上端）: ${currentTop}px → ${currentTop + adjustment}px`);
        }
        
        // パネルの下端が画面外に出ている場合
        if (panelRect.bottom > windowHeight) {
            const currentTop = parseInt(panel.style.top || '120px');
            const adjustment = panelRect.bottom - windowHeight + 10; // 10px余白
            const newTop = Math.max(10, currentTop - adjustment);
            panel.style.top = `${newTop}px`;
            
            console.log(`🎯 PC調整（下端）: ${currentTop}px → ${newTop}px`);
        }
        
        // パネルの左右端が画面外に出ている場合
        if (panelRect.left < 0) {
            panel.style.left = '10px';
            console.log('🎯 左端調整: 10pxに設定');
        }
        
        if (panelRect.right > windowWidth) {
            panel.style.right = '10px';
            panel.style.left = 'auto';
            console.log('🎯 右端調整: 右端10pxに設定');
        }
    }

    /**
     * 📏 分析結果表示時にパネルを拡張
     * 縦画面では上方向、横画面では下方向に拡張
     */
    expandPanelForResults() {
        const panel = document.getElementById('voice-control-panel');
        const resultsContainer = document.getElementById('voice-analysis-results');
        
        if (!panel || !resultsContainer) return;
        
        // 分析結果が表示されているかチェック
        if (!resultsContainer.innerHTML.trim()) return;
        
        // 📱 モバイルデバイス検出
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                         window.innerWidth <= 768;
        
        if (!isMobile) return; // PC版はスクロールのまま
        
        // 少し遅延させてDOMが更新されてから拡張処理を実行
        setTimeout(() => {
            const windowHeight = window.innerHeight;
            const windowWidth = window.innerWidth;
            const isPortrait = windowHeight > windowWidth;
            
            // パネル内のコンテンツの実際の高さを測定（現在のスタイルを一時的にリセットして測定）
            const originalOverflow = panel.style.overflow;
            const originalMaxHeight = panel.style.maxHeight;
            const originalHeight = panel.style.height;
            
            // 測定のために一時的にスタイルをリセット
            panel.style.overflow = 'visible';
            panel.style.maxHeight = 'none';
            panel.style.height = 'auto';
            
            const panelScrollHeight = panel.scrollHeight;
            const currentMaxHeight = isPortrait ? 180 : (windowHeight - 90);
            
            console.log('📏 パネル拡張チェック:', {
                scrollHeight: panelScrollHeight,
                currentMaxHeight: currentMaxHeight,
                isPortrait: isPortrait,
                windowHeight: windowHeight
            });
            
            // コンテンツがパネルサイズを超えている場合のみ拡張
            if (panelScrollHeight > currentMaxHeight) {
                if (isPortrait) {
                    // 縦画面：上方向に拡張（top位置を上げる）
                    const expandedHeight = Math.min(panelScrollHeight + 30, windowHeight * 0.85); // 最大85%、余白30px
                    const newTop = Math.max(10, windowHeight - expandedHeight - 30); // 下から30px余白
                    
                    panel.style.setProperty('position', 'fixed', 'important');
                    panel.style.setProperty('top', `${newTop}px`, 'important');
                    panel.style.setProperty('bottom', 'auto', 'important');
                    panel.style.setProperty('max-height', `${expandedHeight}px`, 'important');
                    panel.style.setProperty('height', `${expandedHeight}px`, 'important');
                    panel.style.setProperty('overflow-y', 'auto', 'important');
                    
                    console.log('📏 縦画面拡張: top=' + newTop + 'px, height=' + expandedHeight + 'px');
                } else {
                    // 横画面：下方向に拡張（max-heightを増やす）
                    const expandedHeight = Math.min(panelScrollHeight + 30, windowHeight - 130 - 30); // 最大で画面下まで-30px余白
                    
                    panel.style.setProperty('position', 'fixed', 'important');
                    panel.style.setProperty('top', '130px', 'important');
                    panel.style.setProperty('bottom', 'auto', 'important');
                    panel.style.setProperty('max-height', `${expandedHeight}px`, 'important');
                    panel.style.setProperty('height', `${expandedHeight}px`, 'important');
                    panel.style.setProperty('overflow-y', 'auto', 'important');
                    
                    console.log('📏 横画面拡張: height=' + expandedHeight + 'px');
                }
            } else {
                // 拡張不要の場合は元のスタイルを復元
                panel.style.overflow = originalOverflow;
                panel.style.maxHeight = originalMaxHeight;
                panel.style.height = originalHeight;
                
                console.log('📏 拡張不要: コンテンツが既に収まっています');
            }
        }, 100); // 100ms遅延
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
     * 音声パネルを表示（Android対応版）
     */
    showVoicePanel() {
        console.log('🔄 showVoicePanel が呼び出されました');
        
        // 🤖 Android用の視覚的フィードバック（コメントアウト）
        // if (this.isAndroid) {
        //     this.showAndroidClickFeedback('音声パネルを開いています...', 'info');
        // }
        
        // 🤖 Android検出に基づいてパネルを選択
        const panelId = this.isAndroid ? 'voice-control-panel-android' : 'voice-control-panel';
        const panel = document.getElementById(panelId);
        
        console.log(`📱 Android検出: ${this.isAndroid}`);
        console.log(`📱 選択されたパネルID: ${panelId}`);
        console.log(`📱 パネル要素取得結果: ${panel ? '成功' : '失敗'}`);
        
        if (panel) {
            console.log(`📱 ${this.isAndroid ? 'Android' : '通常'}パネルを表示: ${panelId}`);
            console.log(`📱 表示前のstyle.display: "${panel.style.display}"`);
            
            // 強制的にスタイルをリセット（!importantを上書き）
            panel.style.setProperty('display', 'block', 'important');
            panel.style.setProperty('visibility', 'visible', 'important');
            
            // 📱 透過状態の場合はopacityを変更しない
            if (!this.isVoicePanelTransparent) {
                panel.style.setProperty('opacity', '1', 'important');
            } else {
                console.log('📱 透過状態のためopacityは維持');
            }
            
            // さらに強制的に表示させるため、cssTextで直接書き換え
            if (this.isAndroid) {
                panel.style.cssText = panel.style.cssText.replace(/display\s*:\s*none\s*!important/gi, 'display: block !important');
            }
            
            // 📱 表示状態を更新
            this.isPanelVisible = true;
            
            console.log(`📱 表示後のstyle.display: "${panel.style.display}"`);
            console.log(`📱 表示後のvisibility: "${panel.style.visibility}"`);
            console.log(`📱 表示後のopacity: "${panel.style.opacity}"`);
            console.log(`📱 パネル状態管理フラグ: ${this.isPanelVisible}`);
            
            // 🤖 Android用成功フィードバック（コメントアウト）
            // if (this.isAndroid) {
            //     this.showAndroidClickFeedback('Android音声パネルが開きました！', 'info');
            // }
            
            // パネルの位置情報もログ出力
            const rect = panel.getBoundingClientRect();
            console.log(`📱 パネル位置情報:`, {
                top: rect.top,
                left: rect.left,
                width: rect.width,
                height: rect.height,
                visible: rect.width > 0 && rect.height > 0
            });
            
            // 📱 パネル表示直後の位置調整（より確実に）
            setTimeout(() => {
                this.adjustPanelPosition();
                this.setupProgressButtonListener();
            }, 50);
            
            // 📱 さらに少し遅れて再調整（レンダリング完了後）
            setTimeout(() => {
                this.adjustPanelPosition();
            }, 200);
        } else {
            console.error(`❌ パネルが見つかりません: ${panelId}`);
            
            // 🤖 Android用エラーフィードバック（コメントアウト）
            // if (this.isAndroid) {
            //     this.showAndroidClickFeedback('音声パネルが見つかりません！', 'error');
            // }
            
            // フォールバック: すべてのパネル要素を確認
            console.log('🔍 利用可能なパネル要素を確認中...');
            const allElements = document.querySelectorAll('[id*="voice-control-panel"]');
            if (allElements.length > 0) {
                console.log(`🔍 見つかった要素 (${allElements.length}個):`);
                allElements.forEach(el => {
                    console.log(`  - ${el.id}: display="${el.style.display}", class="${el.className}"`);
                });
            } else {
                console.error('❌ パネル要素が一つも見つかりません！');
                
                // 🤖 Android用重大エラーフィードバック（コメントアウト）
                // if (this.isAndroid) {
                //     this.showAndroidClickFeedback('パネル要素が見つかりません！', 'error');
                // }
            }
        }
    }
    
    /**
     * 音声パネルを非表示（Android対応版）
     */
    hideVoicePanel() {
        // 🤖 Android検出に基づいてパネルを選択
        const panelId = this.isAndroid ? 'voice-control-panel-android' : 'voice-control-panel';
        const panel = document.getElementById(panelId);
        
        if (panel) {
            console.log(`📱 ${this.isAndroid ? 'Android' : '通常'}パネルを非表示: ${panelId}`);
            panel.style.setProperty('display', 'none', 'important');
            
            // 📱 表示状態を更新
            this.isPanelVisible = false;
            console.log(`📱 パネル状態管理フラグ: ${this.isPanelVisible}`);
            
            // 分析結果もクリア（Android対応）
            const resultsContainerId = this.isAndroid ? 'voice-analysis-results-android' : 'voice-analysis-results';
            const resultsContainer = document.getElementById(resultsContainerId);
            if (resultsContainer) {
                resultsContainer.innerHTML = '';
            }
            
            // 📏 パネルサイズを初期状態にリセット
            this.resetPanelSize();
            
            // 📱 パネル位置を初期位置にリセット
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                             window.innerWidth <= 768;
            
            if (isMobile) {
                // 縦画面と横画面で異なる配置
                const isPortrait = window.innerHeight > window.innerWidth;
                
                panel.style.position = 'fixed';
                panel.style.zIndex = '9999';
                
                if (isPortrait) {
                    // 縦画面：右下に小さく配置
                    panel.style.top = 'auto';
                    panel.style.bottom = '20px';
                    panel.style.left = 'auto';
                    panel.style.right = '10px';
                    panel.style.transform = 'none';
                } else {
                    // 横画面：音声学習ボタンの下の行に配置
                    panel.style.top = '130px';     // 音声学習ボタンの下の行
                    panel.style.bottom = 'auto';
                    panel.style.left = 'auto';
                    panel.style.right = '20px';    // 音声学習ボタンと同じ右端位置
                    panel.style.transform = 'none';
                }
            } else {
                panel.style.position = 'fixed';
                panel.style.top = '120px';
                panel.style.right = '20px';
                panel.style.left = 'auto';
                panel.style.bottom = 'auto';
                panel.style.transform = 'none';
                panel.style.zIndex = '1000';
            }
        }
    }

    /**
     * 📏 パネルサイズを初期状態にリセット
     */
    resetPanelSize() {
        const panel = document.getElementById('voice-control-panel');
        if (!panel) return;
        
        // 📱 モバイルデバイス検出
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                         window.innerWidth <= 768;
        
        if (!isMobile) return; // PC版はリセット不要
        
        const windowHeight = window.innerHeight;
        const windowWidth = window.innerWidth;
        const isPortrait = windowHeight > windowWidth;
        
        console.log('📏 パネルサイズリセット開始');
        
        // 全てのカスタムサイズプロパティをリセット
        panel.style.removeProperty('height');
        panel.style.removeProperty('min-height');
        
        if (isPortrait) {
            // 縦画面：初期サイズに戻す
            panel.style.setProperty('position', 'fixed', 'important');
            panel.style.setProperty('top', 'auto', 'important');
            panel.style.setProperty('bottom', '20px', 'important');
            panel.style.setProperty('left', 'auto', 'important');
            panel.style.setProperty('right', '10px', 'important');
            panel.style.setProperty('max-width', '140px', 'important');
            panel.style.setProperty('max-height', '180px', 'important');
            panel.style.setProperty('overflow-y', 'auto', 'important');
            
            console.log('📏 縦画面リセット: bottom=20px, max-height=180px');
        } else {
            // 横画面：初期サイズに戻す
            panel.style.setProperty('position', 'fixed', 'important');
            panel.style.setProperty('top', '130px', 'important');
            panel.style.setProperty('bottom', 'auto', 'important');
            panel.style.setProperty('left', 'auto', 'important');
            panel.style.setProperty('right', '20px', 'important');
            panel.style.setProperty('max-width', '250px', 'important');
            panel.style.setProperty('max-height', `${windowHeight - 90}px`, 'important');
            panel.style.setProperty('overflow-y', 'auto', 'important');
            
            console.log('📏 横画面リセット: top=130px, max-height=' + (windowHeight - 90) + 'px');
        }
        
        console.log('📏 パネルサイズリセット完了');
    }
    
    /**
     * スマホ用デバッグ情報表示
     */
    showMobileDebugInfo(panel) {
        // 既存のデバッグ表示を削除
        const existingDebug = document.getElementById('mobile-debug-info');
        if (existingDebug) {
            existingDebug.remove();
        }
        
        // デバッグ情報を作成
        const debugDiv = document.createElement('div');
        debugDiv.id = 'mobile-debug-info';
        debugDiv.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid #ff0000;
            padding: 10px;
            font-size: 12px;
            z-index: 99999;
            max-width: 300px;
            border-radius: 5px;
        `;
        
        const rect = panel.getBoundingClientRect();
        const computedStyle = window.getComputedStyle(panel);
        
        debugDiv.innerHTML = `
            <div style="font-weight: bold; color: red;">📱 デバッグ情報</div>
            <div>画面: ${window.innerWidth}x${window.innerHeight}</div>
            <div>向き: ${window.innerHeight > window.innerWidth ? '縦' : '横'}</div>
            <div><strong>設定値:</strong></div>
            <div>・top: ${panel.style.top}</div>
            <div>・right: ${panel.style.right}</div>
            <div>・position: ${panel.style.position}</div>
            <div><strong>実際の位置:</strong></div>
            <div>・top: ${rect.top}px</div>
            <div>・right: ${window.innerWidth - rect.right}px</div>
            <div>・left: ${rect.left}px</div>
            <div><strong>computed:</strong></div>
            <div>・top: ${computedStyle.top}</div>
            <div>・right: ${computedStyle.right}</div>
            <button onclick="this.parentElement.remove()" style="margin-top: 5px; background: red; color: white; border: none; padding: 3px 6px;">閉じる</button>
        `;
        
        document.body.appendChild(debugDiv);
        
        // 5秒後に自動で消す
        setTimeout(() => {
            if (debugDiv.parentElement) {
                debugDiv.remove();
            }
        }, 10000);
    }

    /**
     * 音声パネルの表示/非表示を切り替え（Android対応版）
     */
    toggleVoicePanel() {
        console.log('🔄 toggleVoicePanel が呼び出されました');
        console.log(`📱 現在のデバイス: ${this.isAndroid ? 'Android' : 'その他'}`);
        console.log(`📱 現在のパネルID: ${this.currentPanel}`);
        
        // 🤖 Android検出に基づいてパネルを選択
        const panelId = this.isAndroid ? 'voice-control-panel-android' : 'voice-control-panel';
        const panel = document.getElementById(panelId);
        
        console.log(`🔍 取得しようとするパネル: ${panelId}`);
        console.log(`🔍 パネル要素の存在: ${panel ? 'あり' : 'なし'}`);
        
        if (panel) {
            // パネル表示状態を状態管理フラグで確認
            console.log(`📱 ${this.isAndroid ? 'Android' : '通常'}パネル切り替え: ${this.isPanelVisible ? '非表示' : '表示'}`);
            console.log(`📱 パネル状態管理フラグ: ${this.isPanelVisible}`);
            
            // コンピューテッドスタイルでも確認（デバッグ用）
            const computedStyle = window.getComputedStyle(panel);
            console.log(`📱 実際の表示状態 (computed): ${computedStyle.display}`);
            console.log(`📱 実際の表示状態 (style): ${panel.style.display}`);
            
            if (this.isPanelVisible) {
                this.hideVoicePanel();
            } else {
                this.showVoicePanel();
            }
        } else {
            console.error(`❌ パネルが見つかりません: ${panelId}`);
            
            // 🔍 詳細なデバッグ情報
            console.log('🔍 HTMLに存在するパネル要素を確認中...');
            const allPanels = document.querySelectorAll('[id*="voice-control-panel"]');
            if (allPanels.length > 0) {
                console.log(`🔍 見つかったパネル要素 (${allPanels.length}個):`);
                allPanels.forEach(p => console.log(`  - ${p.id} (display: ${p.style.display})`));
            } else {
                console.error('❌ 音声パネル要素が一つも見つかりません！');
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
            const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            // 通常のタイマー要素を更新
            const timerElement = document.getElementById('voice-recording-timer');
            if (timerElement) {
                timerElement.textContent = timeString;
            }
            
            // 🚀 Android専用タイマー要素も更新
            const androidTimerElement = document.getElementById('voice-recording-timer-android');
            if (androidTimerElement) {
                androidTimerElement.textContent = `⏱️ ${timeString}`;
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
        
        // 通常のタイマー要素をリセット
        const timerElement = document.getElementById('voice-recording-timer');
        if (timerElement) {
            timerElement.textContent = '00:00';
        }
        
        // 🚀 Android専用タイマー要素もリセット
        const androidTimerElement = document.getElementById('voice-recording-timer-android');
        if (androidTimerElement) {
            androidTimerElement.textContent = '⏱️ 00:00';
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
        
        // 🚀 Android専用録音ボタンも更新
        const androidRecordBtn = document.getElementById('voice-record-btn-android');
        if (androidRecordBtn) {
            androidRecordBtn.innerHTML = isRecording ? '⏸️ 停止' : '🎤 録音のみ';
            androidRecordBtn.style.backgroundColor = isRecording ? '#f44336' : '#2196F3';
        }
        
        // 録音ボタン自体が停止機能を持つため、別の停止ボタンは常に非表示
        if (stopBtn) {
            stopBtn.style.display = 'none';
        }
    }
    
    /**
     * ステータス表示を更新
     */
    /**
     * ステータス更新と📱モバイル対応パネル位置調整
     */
    updateStatus(message, type = 'info') {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `voice-status ${type}`;
        }
        
        // 🚀 Android専用ステータス表示も更新
        const androidStatusElement = document.getElementById('voice-status-android');
        if (androidStatusElement) {
            androidStatusElement.textContent = message;
            androidStatusElement.className = `voice-status-android ${type}`;
            
            // タイプに応じて背景色とテキスト色を変更
            let backgroundColor = 'rgba(200, 200, 200, 0.3)';
            let textColor = '#333';
            
            switch (type) {
                case 'recording':
                    backgroundColor = 'rgba(255, 107, 107, 0.2)';
                    textColor = '#d32f2f';
                    break;
                case 'playing':
                    backgroundColor = 'rgba(76, 175, 80, 0.2)';
                    textColor = '#388e3c';
                    break;
                case 'success':
                    backgroundColor = 'rgba(76, 175, 80, 0.2)';
                    textColor = '#2e7d32';
                    break;
                case 'error':
                    backgroundColor = 'rgba(244, 67, 54, 0.2)';
                    textColor = '#c62828';
                    break;
                case 'analyzing':
                    backgroundColor = 'rgba(233, 30, 99, 0.2)';
                    textColor = '#ad1457';
                    break;
                case 'speaking':
                    backgroundColor = 'rgba(156, 39, 176, 0.2)';
                    textColor = '#7b1fa2';
                    break;
                default:
                    backgroundColor = 'rgba(200, 200, 200, 0.3)';
                    textColor = '#333';
            }
            
            androidStatusElement.style.backgroundColor = backgroundColor;
            androidStatusElement.style.color = textColor;
        }
        
        // 📱 モバイル用状態表示は無効化（重複表示回避）
        // const mobileStatusElement = document.getElementById('mobile-voice-status');
        // if (mobileStatusElement) {
        //     mobileStatusElement.textContent = `🎤 ${message}`;
        //     mobileStatusElement.style.display = 'block';
        //     
        //     // タイプに応じて色を変更
        //     if (type === 'error') {
        //         mobileStatusElement.style.borderColor = '#dc3545';
        //         mobileStatusElement.style.backgroundColor = '#f8d7da';
        //     } else if (type === 'success') {
        //         mobileStatusElement.style.borderColor = '#28a745';
        //         mobileStatusElement.style.backgroundColor = '#d4edda';
        //     } else if (type === 'recording') {
        //         mobileStatusElement.style.borderColor = '#ff6b6b';
        //         mobileStatusElement.style.backgroundColor = '#ffe6e6';
        //     } else {
        //         mobileStatusElement.style.borderColor = '#007bff';
        //         mobileStatusElement.style.backgroundColor = '#f8f9fa';
        //     }
        // }
        
        console.log(`🎤 ${message}`);
        
        // 📱 ステータス更新時にパネル位置を調整（特にモバイル）
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                         window.innerWidth <= 768;
        
        if (isMobile) {
            // モバイルではステータス更新でパネルがずれる可能性があるため調整
            setTimeout(() => {
                this.adjustPanelPosition();
            }, 100);
        }
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
    /**
     * 💻 PC専用音声認識初期化（Android設定の影響を受けない独立システム）
     */
    async initPCSpeechRecognition() {
        console.log('💻 PC専用音声認識初期化開始...');
        this.updateStatus('🎤 PC用音声認識を初期化中...', 'info');
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('⚠️ このブラウザは音声認識をサポートしていません');
            console.log('📊 利用可能なAPI:', {
                SpeechRecognition: !!window.SpeechRecognition,
                webkitSpeechRecognition: !!window.webkitSpeechRecognition,
                userAgent: navigator.userAgent.substring(0, 100)
            });
            this.addDebugLog('❌ 音声認識APIが利用できません', 'error');
            this.updateStatus('❌ 音声認識をサポートしていません', 'error');
            return;
        }
        
        // 🔍 PC専用音声認識言語設定の確認
        let recognitionLang = localStorage.getItem('voiceRecognitionLanguage_PC');
        console.log(`🔍 保存されたPC音声認識言語設定: ${recognitionLang || 'なし'}`);
        
        // 初回利用時や日本語設定の場合の確認
        if (!recognitionLang) {
            // 初回利用時：ブラウザのデフォルト言語をチェック
            const browserLang = navigator.language || navigator.userLanguage || 'en-US';
            console.log(`🌐 ブラウザのデフォルト言語: ${browserLang}`);
            
            if (browserLang.startsWith('ja')) {
                console.log('🚨 ブラウザが日本語設定です！警告ダイアログを表示します');
                const shouldUseEnglish = await this.showRecognitionLanguageWarningDialog();
                recognitionLang = shouldUseEnglish ? 'en-US' : 'ja-JP';
            } else {
                recognitionLang = 'en-US'; // デフォルトは英語
            }
            
            localStorage.setItem('voiceRecognitionLanguage_PC', recognitionLang);
            console.log(`💾 PC音声認識言語設定を保存: ${recognitionLang}`);
        } else if (recognitionLang.startsWith('ja')) {
            // 既に日本語が保存されている場合の確認
            console.log('🚨 日本語音声認識が設定されています！警告ダイアログを表示します');
            const shouldSwitchToEnglish = await this.showRecognitionLanguageWarningDialog();
            if (shouldSwitchToEnglish) {
                recognitionLang = 'en-US';
                localStorage.setItem('voiceRecognitionLanguage_PC', 'en-US');
                console.log('✅ PC音声認識を英語に変更しました');
            }
        }
        
        this.recognition = new SpeechRecognition();
        this.recognition.lang = recognitionLang; // 🔧 PC専用設定を適用
        this.recognition.continuous = true;  // PC版：継続認識に復帰（サブスロット展開対応）
        this.recognition.interimResults = true; // 中間結果も取得（認識確実性向上）
        this.recognition.maxAlternatives = 3; // 複数候補で精度向上（Android同様）
        
        console.log(`🔧 PC専用音声認識言語設定完了: ${recognitionLang}`);
        console.log(`� PC専用設定: continuous=false, interimResults=true`);
        
        // 認識開始イベント
        this.recognition.onstart = () => {
            console.log('🎤 PC音声認識が開始されました');
            this.addDebugLog('🎤 PC音声認識開始', 'success');
            this.isRecognitionActive = true;
        };
        
        // 認識停止イベント
        this.recognition.onend = () => {
            console.log('🔚 PC音声認識が終了しました');
            this.addDebugLog('🔚 PC音声認識終了', 'info');
            this.isRecognitionActive = false;
        };
        
        // エラーイベント
        this.recognition.onerror = (event) => {
            console.error('❌ PC音声認識エラー:', event.error);
            this.addDebugLog(`❌ PC音声認識エラー: ${event.error}`, 'error');
            this.isRecognitionActive = false;
        };
        
        // 認識結果を受信
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            console.log('🎯 音声認識結果イベント発生');
            console.log('📊 イベント詳細:', {
                resultLength: event.results.length,
                resultIndex: event.resultIndex,
                timeStamp: event.timeStamp,
                type: event.type
            });
            console.log('📱 デバイス:', navigator.userAgent.substring(0, 100));
            
            // 全ての結果を詳細にログ出力
            for (let i = 0; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence || 'N/A';
                
                console.log(`📋 結果${i}:`, {
                    isFinal: result.isFinal,
                    transcript: `"${transcript}"`,
                    confidence: confidence,
                    alternatives: result.length
                });
                
                if (i >= event.resultIndex) {
                    if (result.isFinal) {
                        finalTranscript += transcript + ' ';
                        console.log(`✅ 最終結果に追加: "${transcript}"`);
                    } else {
                        interimTranscript += transcript + ' ';
                        console.log(`⏳ 中間結果: "${transcript}"`);
                    }
                }
            }
            
            // 最終結果があれば追加
            if (finalTranscript.trim()) {
                const beforeLength = this.recognizedText.length;
                this.recognizedText += finalTranscript;
                const afterLength = this.recognizedText.length;
                
                console.log('✅ 認識結果追加成功');
                console.log(`📊 追加内容: "${finalTranscript.trim()}"`);
                console.log(`📊 文字数変化: ${beforeLength} → ${afterLength}`);
                console.log(`📊 累積結果: "${this.recognizedText.trim()}"`);
            }
            
            // 📱 Android対応：中間結果も積極的に保存（final結果が来ない場合の対策）
            if (/Android/i.test(navigator.userAgent)) {
                console.log('📱 Android: 中間結果処理');
                console.log(`📱 中間結果内容: "${interimTranscript.trim()}"`);
                
                // Android Chromeでは中間結果が最終結果となる場合が多い
                if (interimTranscript.trim() && !finalTranscript.trim()) {
                    // 中間結果をメイン結果として採用
                    this.recognizedText += interimTranscript;
                    console.log('📱 Android: 中間結果をメイン結果として採用');
                    this.addDebugLog(`📱 中間結果採用: "${interimTranscript.trim()}"`, 'success');
                } else if (interimTranscript.trim()) {
                    console.log('📱 Android: 中間結果を補助として保存');
                }
            } else if (interimTranscript.trim()) {
                console.log(`⏳ 中間認識結果のみ: "${interimTranscript.trim()}"`);
            }
            
            // 結果が全く無い場合の詳細ログ
            if (!finalTranscript.trim() && !interimTranscript.trim()) {
                console.warn('⚠️ 認識結果が空です');
                console.log('🔍 空結果の詳細分析:', {
                    eventResultsLength: event.results.length,
                    eventResultIndex: event.resultIndex,
                    currentRecognizedText: this.recognizedText,
                    recognitionActive: this.isRecognitionActive
                });
            }
            
            // 現在の累積結果の状態をログ出力
            this.addDebugLog(`📊 累積認識結果 (長さ:${this.recognizedText.length}): "${this.recognizedText}"`, 'info');
        };
        
        // 認識開始
        this.recognition.onstart = () => {
            this.addDebugLog('🎤 音声認識開始イベント発生', 'success');
            this.addDebugLog(`📊 開始時状態: active=${this.isRecognitionActive}, textLen=${this.recognizedText.length}`, 'info');
            
            this.isRecognitionActive = true;
            this.recognizedText = ''; // 新しい認識セッション開始時にクリア
            this.addDebugLog('✅ 音声認識状態をアクティブに設定し、認識テキストをクリアしました', 'success');
        };
        
        // 認識終了
        this.recognition.onend = () => {
            this.addDebugLog('🔚 音声認識終了イベント発生', 'info');
            this.addDebugLog(`📊 終了時状態: text="${this.recognizedText.trim()}", len=${this.recognizedText.length}`, 'info');
            
            this.isRecognitionActive = false;
            
            // 📱 Android対応：認識終了時に最終結果を再確認
            if (/Android/i.test(navigator.userAgent)) {
                this.addDebugLog('📱 Android: 認識終了時の特別チェック', 'info');
                if (!this.recognizedText.trim()) {
                    this.addDebugLog('📱 Android: 認識結果が空です。マイクの権限や接続を確認してください', 'warning');
                } else {
                    this.addDebugLog(`📱 Android: 認識結果取得成功: ${this.recognizedText.trim()}`, 'success');
                }
            }
            
            this.addDebugLog('🔚 音声認識終了処理完了', 'info');
        };
        
        // 認識エラー
        this.recognition.onerror = (event) => {
            this.addDebugLog('❌ 音声認識エラーイベント発生', 'error');
            this.addDebugLog(`📊 エラー詳細: ${event.error} (${event.message || 'メッセージなし'})`, 'error');
            
            // 📱 Android対応：エラー詳細分析
            if (/Android/i.test(navigator.userAgent)) {
                this.addDebugLog('📱 Android: エラー詳細分析', 'warning');
                
                switch(event.error) {
                    case 'no-speech':
                        this.addDebugLog('📱 Android: 音声が検出されませんでした（マイクに向かって話してください）', 'warning');
                        break;
                    case 'audio-capture':
                        this.addDebugLog('📱 Android: 音声キャプチャエラー（マイクが使用できません）', 'error');
                        break;
                    case 'not-allowed':
                        console.log('📱 Android: マイクアクセスが拒否されました（ブラウザ設定を確認）');
                        break;
                    case 'network':
                        console.log('📱 Android: ネットワークエラー（インターネット接続を確認）');
                        break;
                    case 'service-not-allowed':
                        this.addDebugLog('📱 Android: 音声認識サービスが許可されていません', 'error');
                        break;
                    case 'bad-grammar':
                        this.addDebugLog('📱 Android: 音声認識の文法設定エラー', 'error');
                        break;
                    case 'language-not-supported':
                        this.addDebugLog('📱 Android: 言語がサポートされていません', 'error');
                        break;
                    default:
                        this.addDebugLog(`📱 Android: 不明なエラー: ${event.error}`, 'error');
                }
            }
            
            this.isRecognitionActive = false;
            this.addDebugLog('❌ 音声認識エラー処理完了 - 状態をリセットしました', 'warning');
        };
        
        console.log('✅ 音声認識初期化完了');
        console.log('📱 デバイス:', /Android/i.test(navigator.userAgent) ? 'Android' : /iPhone|iPad/i.test(navigator.userAgent) ? 'iOS' : 'その他');
        
        // 📱 モバイルデバイスでデバッグボタンを表示
        this.showMobileDebugButton();
    }
    
    /**
     * 📱 スマホ用デバッグログ機能
     */
    addDebugLog(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = {
            time: timestamp,
            message: message,
            type: type
        };
        
        // 📱 デバッグログ配列の初期化確認
        if (!this.debugLogs) {
            this.debugLogs = [];
        }
        
        this.debugLogs.push(logEntry);
        
        // 最大件数を超えた場合、古いログを削除
        if (this.debugLogs.length > this.maxDebugLogs) {
            this.debugLogs.shift();
        }
        
        // コンソールにも出力（確実に表示）
        console.log(`📱 [${timestamp}] ${message}`);
        
        // 🔧 デバッグパネル更新を試行（エラーでも続行）
        try {
            this.updateMobileDebugPanel();
        } catch (error) {
            console.log(`🔧 デバッグパネル更新エラー: ${error.message} - ログは保存済み`);
        }
    }
    
    /**
     * 📱 スマホ用診断パネルを表示
     */
    showMobileDebugPanel() {
        try {
            // 既存のパネルがあれば削除
            const existingPanel = document.getElementById('mobile-debug-panel');
            if (existingPanel) {
                existingPanel.remove();
            }
            
            const panel = document.createElement('div');
            panel.id = 'mobile-debug-panel';
            panel.style.cssText = `
                position: fixed;
                top: 10px;
                left: 10px;
                right: 10px;
                max-height: 50vh;
                background: rgba(0,0,0,0.9);
                color: #00ff00;
                font-family: monospace;
                font-size: 12px;
                padding: 10px;
                border-radius: 5px;
                z-index: 20000;
                overflow-y: auto;
                border: 2px solid #00ff00;
            `;
            
            // ヘッダー
            const header = document.createElement('div');
            header.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                padding-bottom: 5px;
                border-bottom: 1px solid #00ff00;
            `;
            header.innerHTML = `
                <span>📱 音声認識診断ログ v2025.7.27</span>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: #ff0000;
                    color: white;
                    border: none;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-size: 10px;
                ">✕</button>
            `;
            
            // テスト機能ボタンエリア
            const testButtons = document.createElement('div');
            testButtons.style.cssText = `
                margin-bottom: 10px;
                padding: 5px;
                background: rgba(0,255,0,0.1);
                border-radius: 3px;
                border: 1px solid #00ff00;
            `;
            testButtons.innerHTML = `
                <div style="margin-bottom: 5px; color: #00ff00; font-size: 11px;">🔧 診断テスト v2025.7.27</div>
                <button onclick="alert('マイクテストボタンがタップされました'); window.voiceSystem.testMicrophonePermission();" style="
                    background: #0066ff;
                    color: white;
                    border: none;
                    padding: 5px 8px;
                    margin: 2px;
                    border-radius: 3px;
                    font-size: 10px;
                ">🎤 マイク権限テスト</button>
                <button onclick="alert('音声認識テストボタンがタップされました'); window.voiceSystem.testVoiceRecognition();" style="
                    background: #00aa00;
                    color: white;
                    border: none;
                    padding: 5px 8px;
                    margin: 2px;
                    border-radius: 3px;
                    font-size: 10px;
                ">🗣️ 音声認識テスト</button>
                <button onclick="alert('ログクリアボタンがタップされました'); window.voiceSystem.clearDebugLogs();" style="
                    background: #666666;
                    color: white;
                    border: none;
                    padding: 5px 8px;
                    margin: 2px;
                    border-radius: 3px;
                    font-size: 10px;
                ">🗑️ ログクリア</button>
            `;
            
            // ログ表示エリア
            const logArea = document.createElement('div');
            logArea.id = 'mobile-debug-logs';
            
            panel.appendChild(header);
            panel.appendChild(testButtons);
            panel.appendChild(logArea);
            document.body.appendChild(panel);
            
            // 現在のログを表示
            this.updateMobileDebugPanel();
            
            return panel;
            
        } catch (error) {
            console.error('showMobileDebugPanelエラー:', error.message);
            throw error;
        }
    }
    
    /**
     * 📱 スマホ用診断パネルを更新
     */
    updateMobileDebugPanel() {
        const logArea = document.getElementById('mobile-debug-logs');
        if (!logArea) {
            // デバッグパネルが見つからない場合はコンソールにログ出力
            console.log('🔧 mobile-debug-logs要素が見つかりません - デバッグパネルが開かれていない可能性');
            return;
        }
        
        // 📱 デバッグログ配列の存在確認
        if (!this.debugLogs || !Array.isArray(this.debugLogs)) {
            console.log('🔧 debugLogs配列が存在しません');
            return;
        }
        
        const logHtml = this.debugLogs.map(log => {
            const color = log.type === 'error' ? '#ff0000' : 
                         log.type === 'warning' ? '#ffff00' : 
                         log.type === 'success' ? '#00ff00' : '#ffffff';
            
            return `<div style="color: ${color}; margin: 2px 0;">
                [${log.time}] ${log.message}
            </div>`;
        }).join('');
        
        logArea.innerHTML = logHtml;
        
        // 最新ログが見えるようにスクロール
        logArea.scrollTop = logArea.scrollHeight;
    }
    
    /**
     * 📱 モバイルデバイスでデバッグボタンを表示
     */
    showMobileDebugButton() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                         'ontouchstart' in window ||
                         window.innerWidth <= 768;
        
        if (isMobile) {
            const debugBtn = document.getElementById('mobile-debug-btn');
            if (debugBtn) {
                debugBtn.style.display = 'inline-block';
                console.log('📱 モバイルデバッグボタンを表示しました');
            }
        }
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
            // グローバルインスタンスを使用（既存のものがあれば再利用）
            let progressUI = window.currentProgressUI;
            
            if (!progressUI) {
                console.log('📊 新しいVoiceProgressUIインスタンスを作成');
                progressUI = new VoiceProgressUI();
                window.currentProgressUI = progressUI;
            }
            
            // 進捗パネルを表示
            progressUI.showProgressPanel();
            console.log('✅ 学習進捗パネルを表示しました');
            
        } catch (error) {
            console.error('❌ 進捗表示エラー:', error);
            alert('進捗表示でエラーが発生しました: ' + error.message);
        }
    }
    
    /**
     * 🔍 デバッグ用：動的エリアと静的スロットの内容を比較
     */
    debugCompareAreas() {
        console.log('🔍 ===== 動的エリア vs 静的スロット比較デバッグ =====');
        
        // 動的エリアの内容
        const dynamicArea = document.getElementById('dynamic-slot-area');
        console.log('📊 動的エリアの状態:');
        if (dynamicArea) {
            console.log('  - HTML:', dynamicArea.innerHTML.substring(0, 200) + '...');
            console.log('  - 子要素数:', dynamicArea.children.length);
            
            const dynamicSlots = dynamicArea.querySelectorAll('[data-slot]');
            console.log('  - 上位スロット数:', dynamicSlots.length);
            
            dynamicSlots.forEach(slot => {
                const slotName = slot.dataset.slot;
                const order = slot.dataset.displayOrder;
                const phraseEl = slot.querySelector('.slot-phrase');
                const phrase = phraseEl ? phraseEl.textContent.trim() : 'なし';
                console.log(`    ${slotName}(order:${order}): "${phrase}"`);
            });
            
            const dynamicSubslots = dynamicArea.querySelectorAll('[data-subslot-id]');
            console.log('  - サブスロット数:', dynamicSubslots.length);
            
            dynamicSubslots.forEach(subslot => {
                const subslotId = subslot.dataset.subslotId;
                const order = subslot.dataset.displayOrder;
                const phraseEl = subslot.querySelector('.slot-phrase');
                const phrase = phraseEl ? phraseEl.textContent.trim() : 'なし';
                console.log(`    sub-${subslotId}(order:${order}): "${phrase}"`);
            });
        } else {
            console.log('  - 動的エリアが見つかりません');
        }
        
        // 静的スロットの内容
        console.log('📊 静的スロットの状態:');
        const staticSlots = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
        
        staticSlots.forEach(slotName => {
            const staticSlot = document.getElementById(`slot-${slotName}`);
            if (staticSlot) {
                const phraseEl = staticSlot.querySelector('.slot-phrase');
                const phrase = phraseEl ? phraseEl.textContent.trim() : 'なし';
                console.log(`  static-${slotName}: "${phrase}"`);
            } else {
                console.log(`  static-${slotName}: 要素なし`);
            }
        });
        
        // 疑問詞の比較
        console.log('📊 疑問詞の状態:');
        const questionWordStatic = document.querySelector('#display-top-question-word .question-word-text');
        const questionWordDynamic = dynamicArea ? dynamicArea.querySelector('.question-word-text') : null;
        
        console.log(`  static疑問詞: "${questionWordStatic ? questionWordStatic.textContent.trim() : 'なし'}"`);
        console.log(`  dynamic疑問詞: "${questionWordDynamic ? questionWordDynamic.textContent.trim() : 'なし'}"`);
        
        console.log('🔍 ===== 比較デバッグ終了 =====');
    }

    /**
     * 📱 スマホ版音声パネル透過制御（スロット表示を確保）
     */
    setVoicePanelTransparency(transparent = true) {
        this.addDebugLog(`📱 透過モード変更要求: ${transparent ? '透過ON' : '透過OFF'}`, 'info');
        
        const panel = document.getElementById('voice-control-panel-android');
        if (panel) {
            if (transparent) {
                // 70%透過（30%不透明）でスロットが見えるように
                panel.style.opacity = '0.3';
                panel.style.pointerEvents = 'none'; // タッチ操作を下の要素に通す
                this.isVoicePanelTransparent = true; // 透過状態を追跡
                console.log('📱 音声パネルを透過モードに設定（30%不透明）');
                this.addDebugLog('📱 透過モード設定完了', 'success');
            } else {
                // 通常の不透明度に戻す
                panel.style.opacity = '1';
                panel.style.pointerEvents = 'auto';
                this.isVoicePanelTransparent = false; // 透過状態を解除
                console.log('📱 音声パネルを通常モードに戻しました');
                this.addDebugLog('📱 通常モード復帰完了', 'success');
            }
        } else {
            this.addDebugLog('❌ voice-control-panel-android要素が見つかりません', 'error');
        }
    }

    /**
     * 🔧 テキストの重複部分を検出するヘルパーメソッド（サブスロット展開対応版）
     */
    findTextOverlap(existingText, newText) {
        const existingWords = existingText.toLowerCase().split(' ').filter(w => w.trim());
        const newWords = newText.toLowerCase().split(' ').filter(w => w.trim());
        
        // 🔧 サブスロット展開対応：より柔軟な重複検出
        let maxOverlap = Math.min(existingWords.length, newWords.length);
        
        // 1. 既存テキストの末尾と新しいテキストの先頭で重複を検索
        for (let i = maxOverlap; i > 0; i--) {
            const existingTail = existingWords.slice(-i);
            const newHead = newWords.slice(0, i);
            
            if (existingTail.join(' ') === newHead.join(' ')) {
                // 重複部分を元の大文字小文字で返す
                console.log(`🔍 末尾先頭重複検出（${i}語）: "${newText.split(' ').slice(0, i).join(' ')}"`);
                return newText.split(' ').slice(0, i).join(' ');
            }
        }
        
        // 2. サブスロット展開時の中断・再開パターン対応
        // 新しいテキストが既存テキストの任意の位置から始まる場合を検出
        for (let startIdx = 0; startIdx < existingWords.length; startIdx++) {
            const maxLength = Math.min(existingWords.length - startIdx, newWords.length);
            for (let length = maxLength; length >= 2; length--) { // 2語以上の重複を検出
                const existingSegment = existingWords.slice(startIdx, startIdx + length);
                const newSegment = newWords.slice(0, length);
                
                if (existingSegment.join(' ') === newSegment.join(' ')) {
                    console.log(`🔍 中断再開重複検出（${length}語、位置${startIdx}）: "${newText.split(' ').slice(0, length).join(' ')}"`);
                    return newText.split(' ').slice(0, length).join(' ');
                }
            }
        }
        
        return ''; // 重複なし
    }

    /**
     * 📝 フレーズ全体の重複を検出する追加メソッド
     */
    findCompleteOverlap(existingText, newText) {
        const existingWords = existingText.toLowerCase().split(' ').filter(w => w.trim());
        const newWords = newText.toLowerCase().split(' ').filter(w => w.trim());
        
        // 新しいテキストが既存テキストの一部と完全に重複しているかチェック
        const existingStr = existingWords.join(' ');
        const newStr = newWords.join(' ');
        
        // 既存テキストの中に新しいテキストが含まれているかチェック
        if (existingStr.includes(newStr)) {
            console.log(`🔍 完全重複検出: "${newText}" は既存テキスト内に存在`);
            return newText; // 全体が重複
        }
        
        // 3単語以上の連続する重複を検索
        for (let startIdx = 0; startIdx <= existingWords.length - 3; startIdx++) {
            for (let length = Math.min(existingWords.length - startIdx, newWords.length); length >= 3; length--) {
                const existingPhrase = existingWords.slice(startIdx, startIdx + length).join(' ');
                const newPhrase = newWords.slice(0, length).join(' ');
                
                if (existingPhrase === newPhrase) {
                    console.log(`🔍 長いフレーズ重複検出: "${newPhrase}"`);
                    return newText.split(' ').slice(0, length).join(' ');
                }
            }
        }
        
        return ''; // 重複なし
    }

    /**
     * �🚨 音声認識言語警告ダイアログを表示
     */
    showRecognitionLanguageWarningDialog() {
        console.log('🚨 showRecognitionLanguageWarningDialog() を呼び出しました');
        
        return new Promise((resolve) => {
            // 既存のダイアログがある場合は削除
            const existingDialog = document.getElementById('recognition-language-warning-dialog');
            if (existingDialog) {
                existingDialog.remove();
            }

            // ダイアログのHTML
            const dialogHTML = `
                <div id="recognition-language-warning-dialog" style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 99999;
                    font-family: Arial, sans-serif;
                    touch-action: none;
                ">
                    <div style="
                        background: white;
                        padding: 20px;
                        border-radius: 15px;
                        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
                        max-width: 90%;
                        width: 400px;
                        text-align: center;
                        margin: 20px;
                    ">
                        <div style="
                            font-size: 60px;
                            margin-bottom: 20px;
                            line-height: 1;
                        ">🎤</div>
                        <h3 style="
                            margin: 0 0 20px 0;
                            color: #333;
                            font-size: 20px;
                            font-weight: bold;
                        ">音声認識言語の確認</h3>
                        <p style="
                            margin: 0 0 30px 0;
                            color: #666;
                            font-size: 16px;
                            line-height: 1.6;
                        ">🎯 <strong>より正確な発音練習のために</strong><br><br>
                        現在、音声認識が日本語に設定されています。<br>
                        英語の発音練習には英語での音声認識をお勧めします。<br><br>
                        <small style="color: #888;">※ワンクリックで英語音声認識に自動切り替えできます</small></p>
                        <div style="
                            display: flex;
                            flex-direction: column;
                            gap: 15px;
                            align-items: center;
                        ">
                            <button id="switch-recognition-to-english-btn" style="
                                background: #28a745;
                                color: white;
                                border: none;
                                padding: 15px 30px;
                                border-radius: 8px;
                                cursor: pointer;
                                font-size: 16px;
                                font-weight: bold;
                                width: 100%;
                                max-width: 250px;
                                touch-action: manipulation;
                                -webkit-tap-highlight-color: transparent;
                            ">🇺🇸 英語音声認識に切り替え（推奨）</button>
                            <button id="keep-japanese-recognition-btn" style="
                                background: #6c757d;
                                color: white;
                                border: none;
                                padding: 15px 30px;
                                border-radius: 8px;
                                cursor: pointer;
                                font-size: 16px;
                                width: 100%;
                                max-width: 250px;
                                touch-action: manipulation;
                                -webkit-tap-highlight-color: transparent;
                            ">🇯🇵 日本語音声認識を継続</button>
                        </div>
                    </div>
                </div>
            `;

            // ダイアログをDOMに追加
            document.body.insertAdjacentHTML('beforeend', dialogHTML);
            console.log('✅ 音声認識ダイアログをDOMに追加しました');

            // イベントリスナー
            const switchBtn = document.getElementById('switch-recognition-to-english-btn');
            const keepBtn = document.getElementById('keep-japanese-recognition-btn');
            
            if (switchBtn) {
                switchBtn.addEventListener('click', () => {
                    console.log('🇺🇸 英語音声認識に変更ボタンがクリックされました');
                    // 成功メッセージを一時表示
                    const successMsg = document.createElement('div');
                    successMsg.style.cssText = `
                        position: fixed; top: 50%; left: 50%; 
                        transform: translate(-50%, -50%); 
                        background: #28a745; color: white; 
                        padding: 15px 25px; border-radius: 8px; 
                        z-index: 100000; font-size: 16px; font-weight: bold;
                    `;
                    successMsg.textContent = '✅ 音声認識を英語に切り替えました！';
                    document.body.appendChild(successMsg);
                    setTimeout(() => successMsg.remove(), 2000);
                    
                    document.getElementById('recognition-language-warning-dialog').remove();
                    resolve(true);
                });
                
                // タッチイベントも追加
                switchBtn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    console.log('🇺🇸 英語音声認識に変更ボタンがタッチされました');
                    // 成功メッセージを一時表示
                    const successMsg = document.createElement('div');
                    successMsg.style.cssText = `
                        position: fixed; top: 50%; left: 50%; 
                        transform: translate(-50%, -50%); 
                        background: #28a745; color: white; 
                        padding: 15px 25px; border-radius: 8px; 
                        z-index: 100000; font-size: 16px; font-weight: bold;
                    `;
                    successMsg.textContent = '✅ 音声認識を英語に切り替えました！';
                    document.body.appendChild(successMsg);
                    setTimeout(() => successMsg.remove(), 2000);
                    
                    document.getElementById('recognition-language-warning-dialog').remove();
                    resolve(true);
                });
            }

            if (keepBtn) {
                keepBtn.addEventListener('click', () => {
                    console.log('🇯🇵 日本語音声認識を継続ボタンがクリックされました');
                    document.getElementById('recognition-language-warning-dialog').remove();
                    resolve(false);
                });
                
                // タッチイベントも追加
                keepBtn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    console.log('🇯🇵 日本語音声認識を継続ボタンがタッチされました');
                    document.getElementById('recognition-language-warning-dialog').remove();
                    resolve(false);
                });
            }

            // 背景クリックで閉じる
            const dialog = document.getElementById('recognition-language-warning-dialog');
            if (dialog) {
                dialog.addEventListener('click', (e) => {
                    if (e.target.id === 'recognition-language-warning-dialog') {
                        console.log('🔲 背景がクリックされました');
                        document.getElementById('recognition-language-warning-dialog').remove();
                        resolve(false);
                    }
                });
            }
            
            console.log('✅ 音声認識ダイアログのイベントリスナーを設定しました');
        });
    }
    
    /**
     * 🚨 言語警告ダイアログを表示（音声合成用）
     */
    showLanguageWarningDialog() {
        console.log('🚨 showLanguageWarningDialog() を呼び出しました');
        
        return new Promise((resolve) => {
            // 既存のダイアログがある場合は削除
            const existingDialog = document.getElementById('language-warning-dialog');
            if (existingDialog) {
                existingDialog.remove();
            }

            // ダイアログのHTML
            const dialogHTML = `
                <div id="language-warning-dialog" style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 99999;
                    font-family: Arial, sans-serif;
                    touch-action: none;
                ">
                    <div style="
                        background: white;
                        padding: 20px;
                        border-radius: 15px;
                        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
                        max-width: 90%;
                        width: 400px;
                        text-align: center;
                        margin: 20px;
                    ">
                        <div style="
                            font-size: 60px;
                            margin-bottom: 20px;
                            line-height: 1;
                        ">⚠️</div>
                        <h3 style="
                            margin: 0 0 20px 0;
                            color: #333;
                            font-size: 20px;
                            font-weight: bold;
                        ">音声言語の確認</h3>
                        <p style="
                            margin: 0 0 30px 0;
                            color: #666;
                            font-size: 16px;
                            line-height: 1.6;
                        ">🎯 <strong>より効果的な英語学習のために</strong><br><br>
                        現在、日本語音声が選択されています。<br>
                        英語の発音練習には英語音声の使用を強くお勧めします。<br><br>
                        <small style="color: #888;">※ワンクリックで最適な英語音声に自動切り替えできます</small></p>
                        <div style="
                            display: flex;
                            flex-direction: column;
                            gap: 15px;
                            align-items: center;
                        ">
                            <button id="switch-to-english-btn" style="
                                background: #007bff;
                                color: white;
                                border: none;
                                padding: 15px 30px;
                                border-radius: 8px;
                                cursor: pointer;
                                font-size: 16px;
                                font-weight: bold;
                                width: 100%;
                                max-width: 250px;
                                touch-action: manipulation;
                                -webkit-tap-highlight-color: transparent;
                            ">✨ 英語音声に自動切り替え（推奨）</button>
                            <button id="keep-japanese-btn" style="
                                background: #6c757d;
                                color: white;
                                border: none;
                                padding: 15px 30px;
                                border-radius: 8px;
                                cursor: pointer;
                                font-size: 16px;
                                width: 100%;
                                max-width: 250px;
                                touch-action: manipulation;
                                -webkit-tap-highlight-color: transparent;
                            ">🇯🇵 日本語音声を継続</button>
                        </div>
                    </div>
                </div>
            `;

            // ダイアログをDOMに追加
            document.body.insertAdjacentHTML('beforeend', dialogHTML);
            console.log('✅ ダイアログをDOMに追加しました');

            // イベントリスナー
            const switchBtn = document.getElementById('switch-to-english-btn');
            const keepBtn = document.getElementById('keep-japanese-btn');
            
            if (switchBtn) {
                switchBtn.addEventListener('click', () => {
                    console.log('🇺🇸 英語音声に変更ボタンがクリックされました');
                    // 成功メッセージを一時表示
                    const successMsg = document.createElement('div');
                    successMsg.style.cssText = `
                        position: fixed; top: 50%; left: 50%; 
                        transform: translate(-50%, -50%); 
                        background: #28a745; color: white; 
                        padding: 15px 25px; border-radius: 8px; 
                        z-index: 100000; font-size: 16px; font-weight: bold;
                    `;
                    successMsg.textContent = '✅ 英語音声に切り替えました！';
                    document.body.appendChild(successMsg);
                    setTimeout(() => successMsg.remove(), 2000);
                    
                    document.getElementById('language-warning-dialog').remove();
                    resolve(true);
                });
                
                // タッチイベントも追加
                switchBtn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    console.log('🇺🇸 英語音声に変更ボタンがタッチされました');
                    // 成功メッセージを一時表示
                    const successMsg = document.createElement('div');
                    successMsg.style.cssText = `
                        position: fixed; top: 50%; left: 50%; 
                        transform: translate(-50%, -50%); 
                        background: #28a745; color: white; 
                        padding: 15px 25px; border-radius: 8px; 
                        z-index: 100000; font-size: 16px; font-weight: bold;
                    `;
                    successMsg.textContent = '✅ 英語音声に切り替えました！';
                    document.body.appendChild(successMsg);
                    setTimeout(() => successMsg.remove(), 2000);
                    
                    document.getElementById('language-warning-dialog').remove();
                    resolve(true);
                });
            }

            if (keepBtn) {
                keepBtn.addEventListener('click', () => {
                    console.log('🇯🇵 日本語音声を継続ボタンがクリックされました');
                    document.getElementById('language-warning-dialog').remove();
                    resolve(false);
                });
                
                // タッチイベントも追加
                keepBtn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    console.log('🇯🇵 日本語音声を継続ボタンがタッチされました');
                    document.getElementById('language-warning-dialog').remove();
                    resolve(false);
                });
            }

            // 背景クリックで閉じる
            const dialog = document.getElementById('language-warning-dialog');
            if (dialog) {
                dialog.addEventListener('click', (e) => {
                    if (e.target.id === 'language-warning-dialog') {
                        console.log('🔲 背景がクリックされました');
                        document.getElementById('language-warning-dialog').remove();
                        resolve(false);
                    }
                });
            }
            
            console.log('✅ イベントリスナーを設定しました');
        });
    }
    
    /**
     * 一時的な分析結果データをクリア（保存キャンセル時）
     */
    async clearTemporaryAnalysisData(analysisResult) {
        try {
            console.log('🚫 一時的な分析結果データをクリア開始');
            
            // 進捗追跡システムが利用可能な場合、一時的に作成された可能性のあるデータをクリア
            if (window.voiceProgressTracker && window.voiceProgressTracker.clearTemporaryData) {
                await window.voiceProgressTracker.clearTemporaryData(analysisResult);
            }
            
            // 既に開いている進捗パネルがある場合、データを再読み込みして一時データを除外
            const progressPanel = document.querySelector('.voice-progress-panel');
            if (progressPanel && progressPanel.style.display !== 'none') {
                console.log('🔄 進捗パネルが開いているため、データを再読み込みします');
                
                // 進捗パネルのUIインスタンスを取得して再読み込み
                if (window.currentProgressUI && window.currentProgressUI.loadAndDisplayProgress) {
                    await window.currentProgressUI.loadAndDisplayProgress();
                    console.log('✅ 進捗パネルのデータを更新しました');
                }
            }
            
            console.log('✅ 一時的な分析結果データクリア完了');
            
        } catch (error) {
            console.error('❌ 一時データクリア失敗:', error);
        }
    }
    
    /**
     * 🎤 マイク権限テスト（Android対応強化版）
     */
    testMicrophonePermission() {
        this.addDebugLog('🎤 マイク権限テストを開始します...', 'info');
        
        // 権限状態をチェック
        if (navigator.permissions) {
            navigator.permissions.query({ name: 'microphone' })
                .then(permissionStatus => {
                    this.addDebugLog(`📋 マイク権限状態: ${permissionStatus.state}`, 'info');
                    
                    // 状態変更の監視
                    permissionStatus.onchange = () => {
                        this.addDebugLog(`📋 マイク権限が変更されました: ${permissionStatus.state}`, 'info');
                    };
                    
                    // 実際にマイクアクセスをテスト
                    this.performMicrophoneTest();
                })
                .catch(error => {
                    this.addDebugLog(`⚠️ 権限クエリエラー: ${error.message}`, 'warning');
                    this.performMicrophoneTest();
                });
        } else {
            this.addDebugLog('⚠️ navigator.permissions API が利用できません', 'warning');
            this.performMicrophoneTest();
        }
    }
    
    /**
     * 🎤 実際のマイクアクセステスト
     */
    performMicrophoneTest() {
        this.addDebugLog('🔍 getUserMedia APIでマイクアクセスをテスト中...', 'info');
        
        const constraints = {
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
                channelCount: 1,
                sampleRate: 16000
            }
        };
        
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                this.addDebugLog('✅ マイクアクセス成功！', 'success');
                
                // オーディオトラック情報を表示
                const audioTracks = stream.getAudioTracks();
                if (audioTracks.length > 0) {
                    const track = audioTracks[0];
                    const settings = track.getSettings();
                    this.addDebugLog(`🎵 オーディオトラック: ${track.label || 'Default'}`, 'info');
                    this.addDebugLog(`📊 サンプルレート: ${settings.sampleRate}Hz`, 'info');
                    this.addDebugLog(`🔊 チャンネル数: ${settings.channelCount}`, 'info');
                }
                
                // 音声レベルをテスト
                this.testAudioLevel(stream);
                
                // ストリームを停止
                setTimeout(() => {
                    stream.getTracks().forEach(track => track.stop());
                    this.addDebugLog('🛑 マイクストリームを停止しました', 'info');
                }, 3000);
            })
            .catch(error => {
                this.addDebugLog(`❌ マイクアクセス失敗: ${error.name} - ${error.message}`, 'error');
                
                // 詳細なエラー情報
                if (error.name === 'NotAllowedError') {
                    this.addDebugLog('🚫 マイク権限が拒否されています', 'error');
                    this.addDebugLog('💡 ブラウザの設定でマイク権限を許可してください', 'info');
                } else if (error.name === 'NotFoundError') {
                    this.addDebugLog('🎤 マイクデバイスが見つかりません', 'error');
                } else if (error.name === 'NotReadableError') {
                    this.addDebugLog('🔒 マイクが他のアプリで使用中です', 'error');
                }
            });
    }
    
    /**
     * 🔊 オーディオレベルテスト
     */
    testAudioLevel(stream) {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const analyser = audioContext.createAnalyser();
            const microphone = audioContext.createMediaStreamSource(stream);
            
            analyser.fftSize = 256;
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            microphone.connect(analyser);
            
            this.addDebugLog('🎵 音声レベル監視を開始...', 'info');
            
            let maxLevel = 0;
            const checkLevel = () => {
                analyser.getByteFrequencyData(dataArray);
                const average = dataArray.reduce((a, b) => a + b) / bufferLength;
                maxLevel = Math.max(maxLevel, average);
            };
            
            const interval = setInterval(checkLevel, 100);
            
            setTimeout(() => {
                clearInterval(interval);
                this.addDebugLog(`📊 最大音声レベル: ${maxLevel.toFixed(1)}/255`, 'info');
                if (maxLevel < 10) {
                    this.addDebugLog('⚠️ 音声レベルが低いです。マイクが正常に動作していない可能性があります', 'warning');
                } else {
                    this.addDebugLog('✅ 音声レベルが検出されました', 'success');
                }
                audioContext.close();
            }, 2500);
            
        } catch (error) {
            this.addDebugLog(`❌ オーディオレベルテスト失敗: ${error.message}`, 'error');
        }
    }
    
    /**
     * 🗣️ 音声認識テスト（Android Chrome強化版）
     */
    testVoiceRecognition() {
        this.addDebugLog('🗣️ 音声認識テストを開始します...', 'info');
        
        // 🔧 追加: 認識テスト開始時にthis.recognizedTextをクリア
        this.recognizedText = '';
        this.addDebugLog('🗑️ this.recognizedTextをクリアしました', 'info');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ Web Speech API が利用できません', 'error');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // デバイス別設定（分離された言語設定を使用）
        const isAndroid = /Android/i.test(navigator.userAgent);
        const storageKey = isAndroid ? 'voiceRecognitionLanguage_Android' : 'voiceRecognitionLanguage_PC';
        const deviceLang = localStorage.getItem(storageKey) || 'en-US';
        
        if (isAndroid) {
            this.addDebugLog('📱 Android Chrome用設定を適用', 'info');
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = deviceLang; // Android専用言語設定
            recognition.maxAlternatives = 3; // 複数候補
        } else {
            this.addDebugLog('💻 PC用設定を適用', 'info');
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = deviceLang; // PC専用言語設定
            recognition.maxAlternatives = 1;
        }
        
        this.addDebugLog(`🔍 認識状態: lang=${recognition.lang}, active=false`, 'info');
        
        // タイムアウト設定（Android用は少し長め）
        const timeoutDuration = isAndroid ? 15000 : 10000;
        let timeoutId = setTimeout(() => {
            recognition.stop();
            this.addDebugLog(`⏰ 音声認識がタイムアウトしました（${timeoutDuration/1000}秒）`, 'warning');
        }, timeoutDuration);
        
        recognition.onstart = () => {
            this.addDebugLog('✅ 音声認識start()コマンド送信完了', 'success');
            this.addDebugLog('🎤 音声認識開始イベント発生', 'success');
            if (isAndroid) {
                this.addDebugLog('🎤 何か話してください（10秒以内）...', 'info');
            } else {
                this.addDebugLog('🎤 何か話してください（10秒以内）...', 'info');
            }
        };
        
        recognition.onresult = (event) => {
            clearTimeout(timeoutId);
            
            this.addDebugLog('🎯 音声認識結果イベント発生', 'info');
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence || 0;
                
                if (result.isFinal) {
                    this.recognizedText = transcript; // 🔧 追加: testも同様にthis.recognizedTextに保存
                    this.addDebugLog(`✅ 認識結果（確定）: "${transcript}"`, 'success');
                    this.addDebugLog(`📊 信頼度: ${(confidence * 100).toFixed(1)}%`, 'info');
                    this.addDebugLog(`💾 this.recognizedText保存: "${this.recognizedText}"`, 'success');
                } else {
                    this.addDebugLog(`🔄 認識結果（途中）: "${transcript}"`, 'info');
                    
                    // Android Chrome: 中間結果も重要
                    if (isAndroid) {
                        this.addDebugLog('📱 Android: 中間結果を記録', 'info');
                        // 🔧 追加: Android中間結果もthis.recognizedTextに保存（録音機能と同様）
                        if (!this.recognizedText || this.recognizedText.trim().length === 0) {
                            this.recognizedText = transcript;
                            this.addDebugLog(`💾 Android中間結果保存: "${this.recognizedText}"`, 'info');
                        }
                    }
                }
            }
        };
        
        recognition.onend = () => {
            clearTimeout(timeoutId);
            this.addDebugLog('🔚 音声認識終了イベント発生', 'info');
            
            if (isAndroid) {
                this.addDebugLog('📱 Android: 認識終了時の特別チェック', 'info');
            }
            
            this.addDebugLog('🔚 音声認識終了処理完了', 'info');
        };
        
        recognition.onerror = (event) => {
            clearTimeout(timeoutId);
            this.addDebugLog(`❌ 音声認識エラー: ${event.error}`, 'error');
            
            if (isAndroid) {
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
        
        recognition.onend = () => {
            clearTimeout(timeoutId);
            this.addDebugLog('🛑 音声認識が終了しました', 'info');
        };
        
        try {
            recognition.start();
        } catch (error) {
            this.addDebugLog(`❌ 音声認識開始失敗: ${error.message}`, 'error');
        }
    }
    
    /**
     * 🗑️ デバッグログをクリア
     */
    clearDebugLogs() {
        this.debugLogs = [];
        this.addDebugLog('🗑️ ログをクリアしました', 'info');
        this.updateMobileDebugPanel();
    }
}

// グローバルインスタンス
let voiceSystem = null;

// DOMロード後に初期化
document.addEventListener('DOMContentLoaded', () => {
    // VoiceProgressTrackerが確実に読み込まれるまで少し待機
    setTimeout(() => {
        voiceSystem = new VoiceSystem();
        window.voiceSystem = voiceSystem;  // グローバルに公開
        console.log('✅ 音声システムを初期化しました');
        console.log('✅ window.voiceSystemが利用可能です');
    }, 500);
});

// 📱 Android対応: マイクアクセス診断用ヘルパー関数
window.diagnoseMicrophoneAccess = async function() {
    console.log('🔍 マイクアクセス診断開始...');
    
    // 基本情報
    console.log('📱 User Agent:', navigator.userAgent);
    console.log('🌐 URL:', window.location.href);
    console.log('🔒 Protocol:', window.location.protocol);
    console.log('🎤 MediaDevices:', !!navigator.mediaDevices);
    console.log('🎤 getUserMedia:', !!navigator.mediaDevices?.getUserMedia);
    
    // Permission API チェック
    if ('permissions' in navigator) {
        try {
            const micPermission = await navigator.permissions.query({ name: 'microphone' });
            console.log('🔐 マイク許可状態:', micPermission.state);
            
            micPermission.onchange = () => {
                console.log('🔄 マイク許可状態が変更されました:', micPermission.state);
            };
        } catch (e) {
            console.log('🔐 Permission API利用不可:', e.message);
        }
    }
    
    // 実際のマイクアクセステスト
    try {
        console.log('🧪 マイクアクセステスト開始...');
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        console.log('✅ マイクアクセス成功');
        
        // 利用可能な音声入力デバイス一覧
        const devices = await navigator.mediaDevices.enumerateDevices();
        const audioInputs = devices.filter(device => device.kind === 'audioinput');
        console.log('🎤 音声入力デバイス数:', audioInputs.length);
        audioInputs.forEach((device, index) => {
            console.log(`🎤 デバイス${index + 1}:`, device.label || `Unknown Device ${device.deviceId}`);
        });
        
        // ストリームを停止
        stream.getTracks().forEach(track => track.stop());
        return { success: true, message: 'マイクアクセス正常' };
        
    } catch (error) {
        console.error('❌ マイクアクセステスト失敗:', error);
        console.error('❌ エラー詳細:', error.name, error.message);
        
        let diagnosis = '';
        switch (error.name) {
            case 'NotAllowedError':
                diagnosis = 'ユーザーがマイクアクセスを拒否しています。ブラウザの設定を確認してください。';
                break;
            case 'NotFoundError':
                diagnosis = 'マイクが見つかりません。デバイスの音声入力設定を確認してください。';
                break;
            case 'NotSupportedError':
                diagnosis = 'ブラウザが音声機能をサポートしていません。';
                break;
            case 'SecurityError':
                diagnosis = 'セキュリティエラー。HTTPS接続が必要な可能性があります。';
                break;
            default:
                diagnosis = `不明なエラー: ${error.message}`;
        }
        
        return { success: false, error: error.name, message: diagnosis };
    }
};

console.log('🔧 マイクアクセス診断ツールが利用可能です: window.diagnoseMicrophoneAccess()');

// 📱 音声パネル位置調整デバッグ関数
window.debugVoicePanelPosition = function() {
    const panel = document.getElementById('voice-control-panel');
    if (!panel) {
        console.log('❌ 音声パネルが見つかりません');
        return;
    }
    
    const rect = panel.getBoundingClientRect();
    const styles = window.getComputedStyle(panel);
    
    console.log('📱 音声パネル位置情報:');
    console.log('🔍 BoundingRect:', {
        top: rect.top,
        bottom: rect.bottom,
        left: rect.left,
        right: rect.right,
        width: rect.width,
        height: rect.height
    });
    console.log('🎨 CSS Style:', {
        position: styles.position,
        top: styles.top,
        bottom: styles.bottom,
        left: styles.left,
        right: styles.right,
        transform: styles.transform,
        zIndex: styles.zIndex,
        display: styles.display
    });
    console.log('📺 画面情報:', {
        windowWidth: window.innerWidth,
        windowHeight: window.innerHeight,
        orientation: screen.orientation ? screen.orientation.angle : 'unknown'
    });
    
    // 位置調整を手動実行
    if (window.voiceSystem) {
        console.log('🔧 位置調整を実行中...');
        window.voiceSystem.adjustPanelPosition();
    }
};

// 📱 Android Chrome音声認識強化機能
window.voiceSystem = voiceSystem;

// 📱 Android Chrome用リトライ機能
voiceSystem.androidRetryRecognition = function(maxRetries = 3) {
    if (!/Android/i.test(navigator.userAgent)) {
        console.log('🔧 Android以外の端末ではリトライ機能を使用しません');
        return;
    }
    
    let retryCount = 0;
    const originalText = this.recognizedText;
    
    const attemptRecognition = () => {
        console.log(`📱 Android音声認識試行 ${retryCount + 1}/${maxRetries}`);
        this.addDebugLog(`📱 Android音声認識試行 ${retryCount + 1}/${maxRetries}`, 'info');
        
        // 認識失敗時のリトライ処理
        const originalOnEnd = this.recognition.onend;
        this.recognition.onend = (event) => {
            if (originalOnEnd) originalOnEnd.call(this, event);
            
            // 結果が空で、まだリトライ回数が残っている場合
            if (!this.recognizedText.trim() && retryCount < maxRetries - 1) {
                retryCount++;
                console.log(`📱 Android: 認識結果が空のため ${retryCount}回目のリトライを実行`);
                this.addDebugLog(`📱 Android: ${retryCount}回目のリトライを実行`, 'warning');
                
                setTimeout(() => {
                    this.recognition.start();
                }, 1000); // 1秒待ってからリトライ
            } else {
                // リトライ完了または成功
                this.recognition.onend = originalOnEnd; // 元のハンドラーに戻す
                if (this.recognizedText.trim()) {
                    this.addDebugLog(`📱 Android: 認識成功 (試行回数: ${retryCount + 1})`, 'success');
                } else {
                    this.addDebugLog(`📱 Android: 全ての試行が失敗しました`, 'error');
                }
            }
        };
        
        this.recognition.start();
    };
    
    attemptRecognition();
};

console.log('🔧 音声パネル位置デバッグが利用可能です: window.debugVoicePanelPosition()');

// 📱 スマホ用デバッグパネル表示機能をグローバルに追加
window.showMobileDebug = function() {
    if (window.voiceSystem) {
        window.voiceSystem.showMobileDebugPanel();
    } else {
        console.error('VoiceSystemが初期化されていません');
    }
};

console.log('📱 スマホ用デバッグパネル表示機能が利用可能です: window.showMobileDebug()');
