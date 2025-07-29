/**
 * 🎤 シンプル録音・再生システム（Android用）
 * VoiceSystemに依存しない独立した録音・再生機能
 */

class SimpleRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.recordedBlob = null;
        this.isRecording = false;
        this.audioChunks = [];
        
        console.log('🎤 SimpleRecorder初期化');
        this.init();
    }
    
    async init() {
        try {
            // マイクアクセス許可を取得
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log('✅ マイクアクセス許可取得完了');
            
            // MediaRecorderを初期化
            this.mediaRecorder = new MediaRecorder(stream);
            this.setupRecorderEvents();
            this.setupButtons();
            
            console.log('✅ SimpleRecorder準備完了');
        } catch (error) {
            console.error('❌ SimpleRecorder初期化エラー:', error);
            alert('マイクアクセスが拒否されました。設定を確認してください。');
        }
    }
    
    setupRecorderEvents() {
        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.audioChunks.push(event.data);
                console.log('🎵 音声データ追加:', event.data.size, 'bytes');
            }
        };
        
        this.mediaRecorder.onstop = () => {
            console.log('🔴 録音停止 - データ処理中...');
            this.recordedBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
            console.log('✅ 録音データ作成完了:', this.recordedBlob.size, 'bytes');
            this.audioChunks = []; // リセット
            
            // 再生ボタンを有効化
            const playBtn = document.getElementById('voice-play-btn-android');
            if (playBtn) {
                playBtn.style.opacity = '1';
                playBtn.disabled = false;
            }
        };
    }
    
    setupButtons() {
        // 録音ボタン
        const recordBtn = document.getElementById('voice-record-btn-android');
        if (recordBtn) {
            recordBtn.addEventListener('click', () => {
                console.log('🎤 録音ボタンクリック');
                this.toggleRecording();
            });
            console.log('✅ 録音ボタン設定完了');
        } else {
            console.error('❌ 録音ボタンが見つかりません');
        }
        
        // 再生ボタン
        const playBtn = document.getElementById('voice-play-btn-android');
        if (playBtn) {
            playBtn.addEventListener('click', () => {
                console.log('🔊 再生ボタンクリック');
                this.playRecording();
            });
            playBtn.style.opacity = '0.5'; // 初期は無効状態
            playBtn.disabled = true;
            console.log('✅ 再生ボタン設定完了');
        } else {
            console.error('❌ 再生ボタンが見つかりません');
        }
    }
    
    toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            this.startRecording();
        }
    }
    
    startRecording() {
        if (!this.mediaRecorder) {
            console.error('❌ MediaRecorderが初期化されていません');
            return;
        }
        
        try {
            this.audioChunks = [];
            this.mediaRecorder.start();
            this.isRecording = true;
            
            // UIを更新
            const recordBtn = document.getElementById('voice-record-btn-android');
            if (recordBtn) {
                recordBtn.textContent = '⏹️ 停止';
                recordBtn.style.backgroundColor = '#f44336';
            }
            
            console.log('🔴 録音開始');
        } catch (error) {
            console.error('❌ 録音開始エラー:', error);
        }
    }
    
    stopRecording() {
        if (!this.mediaRecorder || !this.isRecording) {
            console.log('⚠️ 録音されていません');
            return;
        }
        
        try {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // UIを更新
            const recordBtn = document.getElementById('voice-record-btn-android');
            if (recordBtn) {
                recordBtn.textContent = '🎤 録音のみ';
                recordBtn.style.backgroundColor = '#2196F3';
            }
            
            console.log('⏹️ 録音停止');
        } catch (error) {
            console.error('❌ 録音停止エラー:', error);
        }
    }
    
    playRecording() {
        if (!this.recordedBlob) {
            console.log('⚠️ 録音データがありません');
            alert('先に録音を行ってください。');
            return;
        }
        
        try {
            const audioUrl = URL.createObjectURL(this.recordedBlob);
            const audio = new Audio(audioUrl);
            
            audio.play();
            console.log('▶️ 再生開始');
            
            audio.onended = () => {
                URL.revokeObjectURL(audioUrl);
                console.log('⏹️ 再生完了');
            };
            
        } catch (error) {
            console.error('❌ 再生エラー:', error);
        }
    }
}

// Android デバイスの場合のみ初期化
document.addEventListener('DOMContentLoaded', () => {
    const isAndroid = /Android/i.test(navigator.userAgent);
    if (isAndroid) {
        console.log('📱 Android検出 - SimpleRecorder初期化');
        window.simpleRecorder = new SimpleRecorder();
    }
});
