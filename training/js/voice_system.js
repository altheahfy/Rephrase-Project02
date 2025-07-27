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
        
        // 🎤 録音用音声認識（testVoiceRecognition完全移植版）
        this.recordingRecognition = null;
        this.recognitionTimeoutId = null;
        
        // 📱 スマホ用診断ログ
        this.debugLogs = [];
        this.maxDebugLogs = 50; // 最大50件のログを保持
        
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
        
        // 📱 初期化時にパネル位置を調整（特にモバイル）
        setTimeout(() => {
            const panel = document.getElementById('voice-control-panel');
            if (panel) {
                this.adjustPanelPosition();
            }
        }, 1000);
        
        console.log('✅ 音声システム初期化完了');
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
        
        // 📱 モバイルデバッグボタン
        const debugBtn = document.getElementById('mobile-debug-btn');
        if (debugBtn) {
            debugBtn.addEventListener('click', () => {
                alert('デバッグボタンv2025.7.27-rollback がタップされました！マイクテスト機能が利用可能です。');
                try {
                    this.showMobileDebugPanel();
                    alert('デバッグパネル表示を試行しました');
                } catch (error) {
                    alert('エラー: ' + error.message);
                }
            });
            console.log('✅ モバイルデバッグボタンのイベントリスナーを設定しました');
            
            // 📱 ボタンが正常に設定されたことを確認するためのテスト
            debugBtn.style.border = '2px solid red';
            setTimeout(() => {
                debugBtn.style.border = '';
            }, 2000);
            
        } else {
            console.warn('⚠️ モバイルデバッグボタンが見つかりません');
            alert('警告: モバイルデバッグボタンが見つかりません');
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
                    channelCount: 1,
                    sampleRate: 16000
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
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.isRecording = false;
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
                    console.log('🎯 最終認識結果確認:', this.recognizedText.trim());
                    
                    if (!this.recognizedText.trim()) {
                        console.warn('⚠️ 認識結果が空です。デバイス固有の問題の可能性があります');
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
     * 🚨 緊急修正: testVoiceRecognitionの完全同期版
     */
    startRecordingVoiceRecognition() {
        this.addDebugLog('🗣️ 録音用音声認識を開始します...', 'info');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ Web Speech API が利用できません', 'error');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recordingRecognition = new SpeechRecognition();
        
        // 🚨 緊急修正: testVoiceRecognitionと完全同一設定
        const isAndroid = /Android/i.test(navigator.userAgent);
        if (isAndroid) {
            this.addDebugLog('📱 Android Chrome用設定を適用', 'info');
            this.recordingRecognition.continuous = false;
            this.recordingRecognition.interimResults = true;
            this.recordingRecognition.lang = 'en-US'; // 英語設定
            this.recordingRecognition.maxAlternatives = 3; // 複数候補
        } else {
            this.recordingRecognition.continuous = false;
            this.recordingRecognition.interimResults = true;
            this.recordingRecognition.lang = 'ja-JP';
            this.recordingRecognition.maxAlternatives = 1;
        }
        
        this.addDebugLog(`🔍 認識状態: lang=${this.recordingRecognition.lang}, active=false`, 'info');
        
        // 🚨 緊急修正: testVoiceRecognitionと同一タイムアウト
        const timeoutDuration = isAndroid ? 15000 : 10000;
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
                    
                    // 🚨 Android緊急修正: 確実にrecognizedTextを保存
                    console.log('🔧 緊急修正: recognizedText確実保存 =', this.recognizedText);
                } else {
                    this.addDebugLog(`🔄 認識結果（途中）: "${transcript}"`, 'info');
                    
                    // Android Chrome: 中間結果も重要
                    if (isAndroid) {
                        this.addDebugLog('📱 Android: 中間結果を記録', 'info');
                        // 🚨 Android緊急修正: 中間結果も保存（最終結果が来ない場合の対策）
                        if (!this.recognizedText || this.recognizedText.trim().length === 0) {
                            this.recognizedText = transcript;
                            console.log('🔧 緊急修正: Android中間結果保存 =', this.recognizedText);
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
    async speakSentence() {
        // 🔍 デバッグ：動的エリアと静的スロットの内容を比較
        this.debugCompareAreas();
        
        const sentence = this.getCurrentSentence();
        
        if (!sentence) {
            this.updateStatus('❌ 読み上げる例文がありません', 'error');
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
            
            // 🎤 音声認識結果の最終取得のため待機（Android対応で時間延長）
            const waitTime = /Android/i.test(navigator.userAgent) ? 5000 : 1000; // Android: 5秒に延長
            console.log(`⏳ 音声認識結果待機中... (${waitTime}ms)`);
            await new Promise(resolve => setTimeout(resolve, waitTime));
            
            // 🚨 Android緊急修正: 待機後の認識結果最終確認
            console.log('🔧 緊急修正: 待機後認識結果確認 =', JSON.stringify(this.recognizedText));
            console.log('🔧 緊急修正: 認識結果長さ =', this.recognizedText ? this.recognizedText.length : 0);
            
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
     * 音声パネルを表示
     */
    showVoicePanel() {
        const panel = document.getElementById('voice-control-panel');
        if (panel) {
            panel.style.display = 'block';
            
            // 📱 パネル表示直後の位置調整（より確実に）
            setTimeout(() => {
                this.adjustPanelPosition();
                this.setupProgressButtonListener();
            }, 50);
            
            // 📱 さらに少し遅れて再調整（レンダリング完了後）
            setTimeout(() => {
                this.adjustPanelPosition();
            }, 200);
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
    initSpeechRecognition() {
        console.log('🎤 音声認識初期化開始...');
        this.updateStatus('🎤 音声認識を初期化中...', 'info');
        
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
        
        this.recognition = new SpeechRecognition();
        this.recognition.lang = 'en-US';
        this.recognition.continuous = true;  // 連続認識
        this.recognition.interimResults = true; // 中間結果も取得（認識確実性向上）
        this.recognition.maxAlternatives = 1;
        
        // 📱 Android対応：追加設定
        if (/Android/i.test(navigator.userAgent)) {
            console.log('📱 Android端末を検出：音声認識設定を最適化');
            this.addDebugLog('📱 Android端末を検出', 'info');
            this.recognition.continuous = false; // Android では false の方が安定
            this.recognition.interimResults = true; // 中間結果も取得（Android対応）
            this.recognition.maxAlternatives = 3; // 複数候補で精度向上
            
            // Android Chrome特有の設定
            console.log('📱 Android Chrome最適化設定適用');
            this.addDebugLog('📱 Android Chrome最適化設定適用', 'info');
        }
        
        // 認識開始イベント
        this.recognition.onstart = () => {
            console.log('🎤 音声認識が開始されました');
            this.addDebugLog('🎤 音声認識開始', 'success');
            this.isRecognitionActive = true;
        };
        
        // 認識停止イベント
        this.recognition.onend = () => {
            console.log('🔚 音声認識が終了しました');
            this.addDebugLog('🔚 音声認識終了', 'info');
            this.isRecognitionActive = false;
        };
        
        // エラーイベント
        this.recognition.onerror = (event) => {
            console.error('❌ 音声認識エラー:', event.error);
            this.addDebugLog(`❌ 音声認識エラー: ${event.error}`, 'error');
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
        
        this.debugLogs.push(logEntry);
        
        // 最大件数を超えた場合、古いログを削除
        if (this.debugLogs.length > this.maxDebugLogs) {
            this.debugLogs.shift();
        }
        
        // コンソールにも出力
        console.log(`📱 [${timestamp}] ${message}`);
        
        // スマホ用診断パネルが表示されている場合、リアルタイム更新
        this.updateMobileDebugPanel();
    }
    
    /**
     * 📱 スマホ用診断パネルを表示
     */
    showMobileDebugPanel() {
        try {
            alert('showMobileDebugPanel開始');
            
            // 既存のパネルがあれば削除
            const existingPanel = document.getElementById('mobile-debug-panel');
            if (existingPanel) {
                existingPanel.remove();
                alert('既存パネル削除完了');
            }
            
            alert('新しいパネル作成開始');
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
            
            alert('パネルスタイル設定完了');
            
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
            
            alert('ヘッダー作成完了');
            
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
            
            alert('テストボタン作成完了');
            
            // ログ表示エリア
            const logArea = document.createElement('div');
            logArea.id = 'mobile-debug-logs';
            
            panel.appendChild(header);
            panel.appendChild(testButtons);
            panel.appendChild(logArea);
            document.body.appendChild(panel);
            
            alert('パネルDOM追加完了');
            
            // 現在のログを表示
            this.updateMobileDebugPanel();
            
            alert('デバッグパネル表示完了');
            return panel;
            
        } catch (error) {
            alert('showMobileDebugPanelエラー: ' + error.message);
            throw error;
        }
    }
    
    /**
     * 📱 スマホ用診断パネルを更新
     */
    updateMobileDebugPanel() {
        const logArea = document.getElementById('mobile-debug-logs');
        if (!logArea) return;
        
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
            // VoiceProgressUIのインスタンスを作成して進捗パネルを表示
            const progressUI = new VoiceProgressUI();
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
     * 🚨 言語警告ダイアログを表示
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
                        ">現在、日本語音声が選択されています。<br>
                        英語学習のため、英語音声に変更することをお勧めします。</p>
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
                            ">🇺🇸 英語音声に変更</button>
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
                    document.getElementById('language-warning-dialog').remove();
                    resolve(true);
                });
                
                // タッチイベントも追加
                switchBtn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    console.log('🇺🇸 英語音声に変更ボタンがタッチされました');
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
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.addDebugLog('❌ Web Speech API が利用できません', 'error');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // Android Chrome最適化設定
        const isAndroid = /Android/i.test(navigator.userAgent);
        if (isAndroid) {
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
                    this.addDebugLog(`✅ 認識結果（確定）: "${transcript}"`, 'success');
                    this.addDebugLog(`📊 信頼度: ${(confidence * 100).toFixed(1)}%`, 'info');
                } else {
                    this.addDebugLog(`🔄 認識結果（途中）: "${transcript}"`, 'info');
                    
                    // Android Chrome: 中間結果も重要
                    if (isAndroid) {
                        this.addDebugLog('📱 Android: 中間結果を記録', 'info');
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
