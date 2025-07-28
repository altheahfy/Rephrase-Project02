/**
 * 音声学習進捗追跡システム
 * 学習者の発話判定データを保存・集計し、上達度を表示する
 */
class VoiceProgressTracker {
    constructor() {
        this.dbName = 'VoiceProgressDB';
        this.dbVersion = 1;
        this.db = null;
        
        // レベル定義
        this.levelMapping = {
            '初心者レベル': 1,
            '中級者レベル': 2,
            '上級者レベル': 3,
            '達人レベル': 4,
            '内容不一致': 0,
            '内容要改善': 0.5,
            '音質不良': 0,
            '音声未検出': 0
        };
        
        this.init();
    }
    
    /**
     * 初期化
     */
    async init() {
        try {
            await this.initDatabase();
            console.log('✅ 音声進捗追跡システム初期化完了');
        } catch (error) {
            console.error('❌ 音声進捗追跡システム初期化失敗:', error);
        }
    }
    
    /**
     * IndexedDBの初期化
     */
    initDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);
            
            request.onerror = () => {
                reject(new Error('データベース接続失敗'));
            };
            
            request.onsuccess = (event) => {
                this.db = event.target.result;
                console.log('✅ データベース接続成功');
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // 練習セッションテーブル
                if (!db.objectStoreNames.contains('sessions')) {
                    const sessionStore = db.createObjectStore('sessions', {
                        keyPath: 'id',
                        autoIncrement: true
                    });
                    
                    sessionStore.createIndex('timestamp', 'timestamp', { unique: false });
                    sessionStore.createIndex('level', 'level', { unique: false });
                    sessionStore.createIndex('date', 'date', { unique: false });
                    sessionStore.createIndex('levelScore', 'levelScore', { unique: false });
                }
                
                // 日別統計テーブル
                if (!db.objectStoreNames.contains('dailyStats')) {
                    const dailyStore = db.createObjectStore('dailyStats', {
                        keyPath: 'date'
                    });
                    
                    dailyStore.createIndex('averageLevel', 'averageLevel', { unique: false });
                    dailyStore.createIndex('sessionCount', 'sessionCount', { unique: false });
                }
                
                console.log('✅ データベーステーブル作成完了');
            };
        });
    }
    
    // [その他のメソッドはファイルの長さのため省略 - 実際のバックアップでは完全版を保存]
}

// グローバル初期化
let voiceProgressTracker = null;

document.addEventListener('DOMContentLoaded', () => {
    voiceProgressTracker = new VoiceProgressTracker();
    window.voiceProgressTracker = voiceProgressTracker;
});
