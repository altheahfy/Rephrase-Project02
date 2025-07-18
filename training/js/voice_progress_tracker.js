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
            VoiceProgressTracker.Logger.info('INIT', 'システム初期化開始');
            
            await this.initDatabase();
            
            // 🔍 データ整合性チェックを追加
            await this.performDataIntegrityCheck();
            
            VoiceProgressTracker.Logger.info('INIT', 'システム初期化完了');
        } catch (error) {
            VoiceProgressTracker.Logger.error('INIT', 'システム初期化失敗', error);
        }
    }

    /**
     * 🔍 データ整合性チェック（データ喪失の早期検出）
     */
    async performDataIntegrityCheck() {
        try {
            console.log('🔍 データ整合性チェック開始...');
            
            // セッションデータの存在確認
            const sessionCount = await this.getSessionCount();
            const dailyStatsCount = await this.getDailyStatsCount();
            
            console.log(`📊 保存されているデータ: セッション${sessionCount}件, 日別統計${dailyStatsCount}件`);
            
            // localStorage にバックアップ情報があるかチェック
            const lastBackupInfo = localStorage.getItem('voiceProgress_lastBackup');
            const lastSessionCount = localStorage.getItem('voiceProgress_lastSessionCount');
            
            if (lastSessionCount && parseInt(lastSessionCount) > sessionCount) {
                console.warn(`⚠️ データ喪失の可能性: 前回${lastSessionCount}件 → 現在${sessionCount}件`);
                this.logDataLossIncident(lastSessionCount, sessionCount);
            }
            
            // 現在の状態をバックアップ情報として保存
            localStorage.setItem('voiceProgress_lastSessionCount', sessionCount.toString());
            localStorage.setItem('voiceProgress_lastBackup', new Date().toISOString());
            
        } catch (error) {
            console.error('❌ データ整合性チェック失敗:', error);
        }
    }

    /**
     * セッション数を取得
     */
    getSessionCount() {
        return new Promise((resolve, reject) => {
            if (!this.db) {
                resolve(0);
                return;
            }
            
            const transaction = this.db.transaction(['sessions'], 'readonly');
            const store = transaction.objectStore('sessions');
            const request = store.count();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 日別統計数を取得
     */
    getDailyStatsCount() {
        return new Promise((resolve, reject) => {
            if (!this.db) {
                resolve(0);
                return;
            }
            
            const transaction = this.db.transaction(['dailyStats'], 'readonly');
            const store = transaction.objectStore('dailyStats');
            const request = store.count();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 🚨 データ喪失インシデントを記録
     */
    logDataLossIncident(previousCount, currentCount) {
        const incident = {
            timestamp: new Date().toISOString(),
            previousCount: parseInt(previousCount),
            currentCount: parseInt(currentCount),
            lostCount: parseInt(previousCount) - parseInt(currentCount),
            userAgent: navigator.userAgent,
            url: window.location.href
        };
        
        // 🔧 新しいログシステムを使用
        VoiceProgressTracker.Logger.error('DATA_LOSS', 
            `進捗データ${incident.lostCount}件が喪失しました`, incident);
        
        // localStorageに記録（IndexedDBが信頼できない場合のため）
        const incidents = JSON.parse(localStorage.getItem('voiceProgress_dataLossIncidents') || '[]');
        incidents.push(incident);
        
        // 最新10件のみ保持
        if (incidents.length > 10) {
            incidents.shift();
        }
        
        localStorage.setItem('voiceProgress_dataLossIncidents', JSON.stringify(incidents));
        
        // ユーザーに通知
        this.notifyDataLoss(incident);
    }

    /**
     * 📢 データ喪失をユーザーに通知
     */
    notifyDataLoss(incident) {
        const message = `⚠️ 学習進捗データの喪失を検出しました\n` +
                       `喪失データ数: ${incident.lostCount}件\n` +
                       `発生時刻: ${new Date(incident.timestamp).toLocaleString()}\n\n` +
                       `考えられる原因:\n` +
                       `• ブラウザのデータクリア\n` +
                       `• プライベートモード使用\n` +
                       `• ストレージ容量不足\n\n` +
                       `今後のデータ保護のため、定期的なエクスポートをお勧めします。`;
        
        // 控えめな通知（コンソールと状態表示）
        console.warn(message);
        
        // 可能であればUI通知を表示
        if (typeof this.updateStatus === 'function') {
            this.updateStatus(`⚠️ 進捗データ${incident.lostCount}件が喪失しました`, 'warning');
        }
    }

    /**
     * 🔧 データ喪失インシデントレポートを取得
     */
    getDataLossReport() {
        const incidents = JSON.parse(localStorage.getItem('voiceProgress_dataLossIncidents') || '[]');
        const lastBackup = localStorage.getItem('voiceProgress_lastBackup');
        const lastSessionCount = localStorage.getItem('voiceProgress_lastSessionCount');
        
        return {
            incidents,
            lastBackup,
            lastSessionCount,
            totalIncidents: incidents.length,
            totalLostData: incidents.reduce((sum, incident) => sum + incident.lostCount, 0)
        };
    }
    
    /**
     * 音声分析結果を保存
     * @param {Object} analysisResult - 音声分析結果
     */
    async saveVoiceSession(analysisResult) {
        if (!this.db) {
            console.error('❌ データベースが初期化されていません');
            return;
        }

        try {
            // 🔧 保存前にバックアップを作成（定期的）
            await this.createPeriodicBackup();

            const timestamp = new Date();
            const date = timestamp.toISOString().split('T')[0]; // YYYY-MM-DD
            
            // レベルからスコアに変換
            const levelScore = this.convertLevelToScore(analysisResult.level);
            
            // セッションデータ作成
            const sessionData = {
                timestamp: timestamp.toISOString(),
                date: date,
                level: this.cleanLevelText(analysisResult.level),
                levelScore: levelScore,
                duration: analysisResult.duration || 0,
                wordsPerMinute: analysisResult.wordsPerMinute || 0,
                contentAccuracy: analysisResult.contentAccuracy || 0,
                expectedSentence: analysisResult.expectedSentence || '',
                recognizedText: analysisResult.recognizedText || '',
                verificationStatus: analysisResult.verificationStatus || 'unknown'
            };
            
            // セッションを保存
            await this.saveToStore('sessions', sessionData);
            
            // 🔧 保存成功をトラッキング
            localStorage.setItem('voiceProgress_lastSaveSuccess', timestamp.toISOString());
            
            console.log('✅ セッションデータ保存完了:', sessionData);
            
            // 日別統計を更新
            await this.updateDailyStats(date);
            
            return sessionData;
            
        } catch (error) {
            console.error('❌ 音声セッション保存失敗:', error);
            throw error;
        }
    }
    
    /**
     * レベルテキストをスコアに変換
     */
    convertLevelToScore(levelText) {
        // 絵文字やその他の記号を除去してクリーンなレベル名を抽出
        const cleanLevel = this.cleanLevelText(levelText);
        
        // 部分マッチでレベルを判定
        if (cleanLevel.includes('達人')) return 4;
        if (cleanLevel.includes('上級者')) return 3;
        if (cleanLevel.includes('中級者')) return 2;
        if (cleanLevel.includes('初心者')) return 1;
        if (cleanLevel.includes('内容不一致') || cleanLevel.includes('音質不良') || cleanLevel.includes('音声未検出')) return 0;
        if (cleanLevel.includes('内容要改善')) return 0.5;
        
        return 0; // デフォルト
    }
    
    /**
     * レベルテキストをクリーンアップ
     */
    cleanLevelText(levelText) {
        if (!levelText) return 'unknown';
        
        // 絵文字と特殊文字を除去
        return levelText.replace(/[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu, '')
                       .replace(/[❌⚠️⚡🚀📈🐌]/g, '')
                       .trim();
    }
    
    /**
     * データストアに保存
     */
    saveToStore(storeName, data) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.add(data);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * データストアを更新
     */
    updateStore(storeName, data) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.put(data);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * 日別統計を更新
     */
    async updateDailyStats(date) {
        try {
            // その日のセッションを取得
            const sessions = await this.getSessionsByDate(date);
            
            if (sessions.length === 0) return;
            
            // 統計計算
            const validSessions = sessions.filter(s => s.levelScore > 0);
            const averageLevel = validSessions.length > 0 
                ? validSessions.reduce((sum, s) => sum + s.levelScore, 0) / validSessions.length 
                : 0;
            
            const totalDuration = sessions.reduce((sum, s) => sum + (s.duration || 0), 0);
            const averageWPM = sessions.filter(s => s.wordsPerMinute > 0).length > 0
                ? sessions.filter(s => s.wordsPerMinute > 0).reduce((sum, s) => sum + s.wordsPerMinute, 0) / sessions.filter(s => s.wordsPerMinute > 0).length
                : 0;
            
            const dailyStats = {
                date: date,
                sessionCount: sessions.length,
                validSessionCount: validSessions.length,
                averageLevel: averageLevel,
                totalDuration: totalDuration,
                averageWordsPerMinute: averageWPM,
                lastUpdated: new Date().toISOString()
            };
            
            await this.updateStore('dailyStats', dailyStats);
            console.log(`✅ 日別統計更新完了 (${date}):`, dailyStats);
            
        } catch (error) {
            console.error('❌ 日別統計更新失敗:', error);
        }
    }
    
    /**
     * 指定日付のセッションを取得
     */
    getSessionsByDate(date) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['sessions'], 'readonly');
            const store = transaction.objectStore('sessions');
            const index = store.index('date');
            const request = index.getAll(date);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * 期間別の進捗データを取得
     * @param {string} period - 'week', 'month', 'quarter', 'year'
     * @param {Date} endDate - 終了日（デフォルト: 今日）
     */
    async getProgressData(period = 'week', endDate = new Date()) {
        try {
            const startDate = this.calculateStartDate(period, endDate);
            const sessions = await this.getSessionsInRange(startDate, endDate);
            
            return this.calculateProgressMetrics(sessions, period, startDate, endDate);
            
        } catch (error) {
            console.error('❌ 進捗データ取得失敗:', error);
            return null;
        }
    }
    
    /**
     * 期間の開始日を計算
     */
    calculateStartDate(period, endDate) {
        const start = new Date(endDate);
        
        switch (period) {
            case 'week':
                start.setDate(start.getDate() - 7);
                break;
            case 'month':
                start.setMonth(start.getMonth() - 1);
                break;
            case 'quarter':
                start.setMonth(start.getMonth() - 3);
                break;
            case 'year':
                start.setFullYear(start.getFullYear() - 1);
                break;
            default:
                start.setDate(start.getDate() - 7);
        }
        
        return start;
    }
    
    /**
     * 期間内のセッションを取得
     */
    getSessionsInRange(startDate, endDate) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['sessions'], 'readonly');
            const store = transaction.objectStore('sessions');
            const index = store.index('timestamp');
            
            const range = IDBKeyRange.bound(
                startDate.toISOString(),
                endDate.toISOString()
            );
            
            const request = index.getAll(range);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * 進捗メトリクスを計算
     */
    calculateProgressMetrics(sessions, period, startDate, endDate) {
        const validSessions = sessions.filter(s => s.levelScore > 0);
        
        if (sessions.length === 0) {
            return {
                period,
                startDate: startDate.toISOString(),
                endDate: endDate.toISOString(),
                totalSessions: 0,
                validSessions: 0,
                averageLevel: 0,
                improvement: 0,
                levelDistribution: { beginner: 0, intermediate: 0, advanced: 0, expert: 0 },
                dailyAverage: 0,
                bestDay: null,
                chartData: []
            };
        }
        
        // 基本的な統計
        const totalSessions = sessions.length;
        const validSessionCount = validSessions.length;
        const averageLevel = validSessionCount > 0 
            ? validSessions.reduce((sum, s) => sum + s.levelScore, 0) / validSessionCount 
            : 0;
        
        // レベル分布
        const levelDistribution = {
            beginner: sessions.filter(s => s.levelScore >= 0.5 && s.levelScore < 1.5).length,
            intermediate: sessions.filter(s => s.levelScore >= 1.5 && s.levelScore < 2.5).length,
            advanced: sessions.filter(s => s.levelScore >= 2.5 && s.levelScore < 3.5).length,
            expert: sessions.filter(s => s.levelScore >= 3.5).length
        };
        
        // 上達度計算（期間前半vs後半の比較）
        const improvement = this.calculateImprovement(validSessions);
        
        // 日別平均
        const dayCount = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
        const dailyAverage = totalSessions / dayCount;
        
        // 最高パフォーマンス日
        const bestDay = this.findBestDay(sessions);
        
        // チャートデータ
        const chartData = this.generateChartData(sessions, startDate, endDate);
        
        return {
            period,
            startDate: startDate.toISOString(),
            endDate: endDate.toISOString(),
            totalSessions,
            validSessions: validSessionCount,
            averageLevel,
            improvement,
            levelDistribution,
            dailyAverage,
            bestDay,
            chartData
        };
    }
    
    /**
     * 上達度を計算（期間前半vs後半）
     */
    calculateImprovement(sessions) {
        if (sessions.length < 4) return 0;
        
        const midPoint = Math.floor(sessions.length / 2);
        const firstHalf = sessions.slice(0, midPoint);
        const secondHalf = sessions.slice(midPoint);
        
        const firstAverage = firstHalf.reduce((sum, s) => sum + s.levelScore, 0) / firstHalf.length;
        const secondAverage = secondHalf.reduce((sum, s) => sum + s.levelScore, 0) / secondHalf.length;
        
        return ((secondAverage - firstAverage) / firstAverage) * 100;
    }
    
    /**
     * 最高パフォーマンス日を特定
     */
    findBestDay(sessions) {
        const dailyStats = {};
        
        sessions.forEach(session => {
            const date = session.date;
            if (!dailyStats[date]) {
                dailyStats[date] = { sessions: [], total: 0, average: 0 };
            }
            dailyStats[date].sessions.push(session);
        });
        
        let bestDay = null;
        let bestAverage = 0;
        
        Object.keys(dailyStats).forEach(date => {
            const dayData = dailyStats[date];
            const validSessions = dayData.sessions.filter(s => s.levelScore > 0);
            
            if (validSessions.length > 0) {
                const average = validSessions.reduce((sum, s) => sum + s.levelScore, 0) / validSessions.length;
                
                if (average > bestAverage) {
                    bestAverage = average;
                    bestDay = {
                        date,
                        averageLevel: average,
                        sessionCount: dayData.sessions.length
                    };
                }
            }
        });
        
        return bestDay;
    }
    
    /**
     * チャート用データを生成
     */
    generateChartData(sessions, startDate, endDate) {
        const chartData = [];
        const dailyData = {};
        
        // 日別にグループ化
        sessions.forEach(session => {
            const date = session.date;
            if (!dailyData[date]) {
                dailyData[date] = [];
            }
            dailyData[date].push(session);
        });
        
        // 期間内の全日付について
        const currentDate = new Date(startDate);
        while (currentDate <= endDate) {
            const dateStr = currentDate.toISOString().split('T')[0];
            const daySessions = dailyData[dateStr] || [];
            const validSessions = daySessions.filter(s => s.levelScore > 0);
            
            const averageLevel = validSessions.length > 0 
                ? validSessions.reduce((sum, s) => sum + s.levelScore, 0) / validSessions.length 
                : 0;
            
            chartData.push({
                date: dateStr,
                averageLevel,
                sessionCount: daySessions.length,
                validSessionCount: validSessions.length
            });
            
            currentDate.setDate(currentDate.getDate() + 1);
        }
        
        return chartData;
    }
    
    /**
     * 定期バックアップの実行
     */
    async createPeriodicBackup() {
        const lastBackup = localStorage.getItem('voiceProgress_lastPeriodicBackup');
        const now = new Date();
        
        // 24時間ごとにバックアップ
        if (!lastBackup || (now - new Date(lastBackup)) > 24 * 60 * 60 * 1000) {
            console.log('📅 定期バックアップを実行中...');
            await this.createBackup();
            localStorage.setItem('voiceProgress_lastPeriodicBackup', now.toISOString());
        }
    }

    /**
     * 全データをクリア（開発・テスト用）
     * 🔧 安全性強化：データ喪失防止
     */
    async clearAllData() {
        if (!this.db) return;
        
        try {
            // 🚨 クリア前に緊急バックアップを作成
            console.log('🚨 データクリア前に緊急バックアップを作成...');
            const backup = await this.createBackup();
            
            if (backup) {
                // 明示的にクリアのログを記録
                const clearEvent = {
                    timestamp: new Date().toISOString(),
                    type: 'manual_clear',
                    sessionCount: backup.sessionCount,
                    dailyStatsCount: backup.dailyStatsCount,
                    userAgent: navigator.userAgent
                };
                
                const clearEvents = JSON.parse(localStorage.getItem('voiceProgress_clearEvents') || '[]');
                clearEvents.push(clearEvent);
                
                // 最新5件のみ保持
                if (clearEvents.length > 5) {
                    clearEvents.shift();
                }
                
                localStorage.setItem('voiceProgress_clearEvents', JSON.stringify(clearEvents));
                console.log('📝 データクリアイベントを記録:', clearEvent);
            }
            
            await this.clearStore('sessions');
            await this.clearStore('dailyStats');
            console.log('✅ 全進捗データをクリアしました');
            
        } catch (error) {
            console.error('❌ データクリア失敗:', error);
        }
    }
    
    /**
     * ストアをクリア
     */
    clearStore(storeName) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.clear();
            
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 🔧 データ自動バックアップ機能
     */
    async createBackup() {
        try {
            console.log('💾 進捗データバックアップ作成開始...');
            
            const sessions = await this.getAllSessions();
            const dailyStats = await this.getAllDailyStats();
            
            const backup = {
                timestamp: new Date().toISOString(),
                version: this.dbVersion,
                sessionCount: sessions.length,
                dailyStatsCount: dailyStats.length,
                sessions,
                dailyStats
            };
            
            // localStorageにも保存（緊急時用）
            localStorage.setItem('voiceProgress_emergencyBackup', JSON.stringify(backup));
            localStorage.setItem('voiceProgress_emergencyBackup_timestamp', backup.timestamp);
            
            console.log(`✅ バックアップ作成完了: セッション${sessions.length}件, 統計${dailyStats.length}件`);
            return backup;
            
        } catch (error) {
            console.error('❌ バックアップ作成失敗:', error);
            return null;
        }
    }

    /**
     * 🔧 緊急時データ復旧
     */
    async restoreFromEmergencyBackup() {
        try {
            const backupData = localStorage.getItem('voiceProgress_emergencyBackup');
            const backupTimestamp = localStorage.getItem('voiceProgress_emergencyBackup_timestamp');
            
            if (!backupData) {
                console.warn('⚠️ 緊急バックアップが見つかりません');
                return false;
            }
            
            const backup = JSON.parse(backupData);
            console.log(`🔄 緊急バックアップから復旧開始: ${backupTimestamp}`);
            console.log(`📊 復旧データ: セッション${backup.sessionCount}件, 統計${backup.dailyStatsCount}件`);
            
            // 現在のデータを一旦クリア
            await this.clearAllData();
            
            // セッションデータを復旧
            for (const session of backup.sessions) {
                delete session.id; // 自動インクリメントのため削除
                await this.saveToStore('sessions', session);
            }
            
            // 日別統計を復旧
            for (const dailyStat of backup.dailyStats) {
                await this.saveToStore('dailyStats', dailyStat);
            }
            
            console.log('✅ 緊急バックアップからの復旧完了');
            return true;
            
        } catch (error) {
            console.error('❌ 緊急復旧失敗:', error);
            return false;
        }
    }

    /**
     * データベースの健全性チェック
     */
    async checkDatabaseHealth() {
        try {
            if (!this.db) {
                return { healthy: false, issue: 'データベース未接続' };
            }
            
            const sessionCount = await this.getSessionCount();
            const dailyStatsCount = await this.getDailyStatsCount();
            
            // 基本的な健全性チェック
            const lastWeekDate = new Date();
            lastWeekDate.setDate(lastWeekDate.getDate() - 7);
            
            const recentSessions = await this.getSessionsSince(lastWeekDate.toISOString());
            
            return {
                healthy: true,
                sessionCount,
                dailyStatsCount,
                recentSessionCount: recentSessions.length,
                dbSize: await this.estimateDbSize()
            };
            
        } catch (error) {
            return { healthy: false, issue: error.message };
        }
    }

    /**
     * データベースサイズの推定
     */
    async estimateDbSize() {
        if ('storage' in navigator && 'estimate' in navigator.storage) {
            try {
                const estimate = await navigator.storage.estimate();
                return {
                    usage: estimate.usage,
                    quota: estimate.quota,
                    usageInMB: (estimate.usage / 1024 / 1024).toFixed(2),
                    quotaInMB: (estimate.quota / 1024 / 1024).toFixed(2)
                };
            } catch (error) {
                console.warn('ストレージサイズ取得失敗:', error);
            }
        }
        return null;
    }

    /**
     * 指定日時以降のセッションを取得
     */
    getSessionsSince(timestamp) {
        return new Promise((resolve, reject) => {
            if (!this.db) {
                resolve([]);
                return;
            }
            
            const transaction = this.db.transaction(['sessions'], 'readonly');
            const store = transaction.objectStore('sessions');
            const index = store.index('timestamp');
            const range = IDBKeyRange.lowerBound(timestamp);
            const request = index.getAll(range);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 全セッションを取得
     */
    getAllSessions() {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['sessions'], 'readonly');
            const store = transaction.objectStore('sessions');
            const request = store.getAll();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 全日別統計を取得
     */
    getAllDailyStats() {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['dailyStats'], 'readonly');
            const store = transaction.objectStore('dailyStats');
            const request = store.getAll();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 🔧 Webアプリケーション向けログ管理システム
     */
    static Logger = {
        /**
         * ログレベル定義
         */
        LEVELS: {
            ERROR: 0,   // エラー
            WARN: 1,    // 警告
            INFO: 2,    // 情報
            DEBUG: 3    // デバッグ
        },

        /**
         * 現在のログレベル（プロダクション環境では INFO 推奨）
         */
        currentLevel: 2, // INFO

        /**
         * ログエントリの最大保持数
         */
        maxLogEntries: 1000,

        /**
         * 統一ログ記録
         */
        log(level, category, message, data = null) {
            if (level > this.currentLevel) return;

            const timestamp = new Date().toISOString();
            const logEntry = {
                timestamp,
                level: Object.keys(this.LEVELS)[level],
                category,
                message,
                data,
                url: window.location.href,
                userAgent: navigator.userAgent.substring(0, 100) // 短縮版
            };

            // 1. Console出力（開発者向け）
            this.outputToConsole(logEntry);

            // 2. LocalStorage保存（永続化）
            this.saveToLocalStorage(logEntry);

            // 3. IndexedDB保存（大容量データ用）
            this.saveToIndexedDB(logEntry);

            // 4. 重要ログの場合、ユーザー通知
            if (level <= this.LEVELS.WARN) {
                this.notifyUser(logEntry);
            }
        },

        /**
         * Console出力（レベル別）
         */
        outputToConsole(logEntry) {
            const emoji = {
                'ERROR': '❌',
                'WARN': '⚠️',
                'INFO': 'ℹ️',
                'DEBUG': '🔍'
            }[logEntry.level] || 'ℹ️';

            const message = `${emoji} [${logEntry.category}] ${logEntry.message}`;
            
            switch (logEntry.level) {
                case 'ERROR':
                    console.error(message, logEntry.data);
                    break;
                case 'WARN':
                    console.warn(message, logEntry.data);
                    break;
                case 'DEBUG':
                    console.debug(message, logEntry.data);
                    break;
                default:
                    console.log(message, logEntry.data);
            }
        },

        /**
         * LocalStorage保存（軽量ログ用）
         */
        saveToLocalStorage(logEntry) {
            try {
                const logs = JSON.parse(localStorage.getItem('voiceProgress_logs') || '[]');
                logs.push(logEntry);

                // 古いログを削除（容量制限）
                if (logs.length > this.maxLogEntries) {
                    logs.splice(0, logs.length - this.maxLogEntries);
                }

                localStorage.setItem('voiceProgress_logs', JSON.stringify(logs));
            } catch (error) {
                console.warn('LocalStorageログ保存失敗:', error);
            }
        },

        /**
         * IndexedDB保存（詳細ログ用）
         */
        async saveToIndexedDB(logEntry) {
            try {
                if (window.voiceProgressTracker && window.voiceProgressTracker.db) {
                    // ログ専用テーブルがあれば保存
                    // 現在は sessions テーブルに重要ログのみ保存
                    if (logEntry.level === 'ERROR' || logEntry.category === 'DATA_LOSS') {
                        const logData = {
                            timestamp: logEntry.timestamp,
                            date: logEntry.timestamp.split('T')[0],
                            level: `LOG_${logEntry.level}`,
                            levelScore: 0,
                            duration: 0,
                            wordsPerMinute: 0,
                            contentAccuracy: 0,
                            expectedSentence: logEntry.category,
                            recognizedText: logEntry.message,
                            verificationStatus: 'system_log'
                        };

                        await window.voiceProgressTracker.saveToStore('sessions', logData);
                    }
                }
            } catch (error) {
                console.warn('IndexedDBログ保存失敗:', error);
            }
        },

        /**
         * ユーザー通知（重要ログのみ）
         */
        notifyUser(logEntry) {
            if (logEntry.level === 'ERROR' || logEntry.category === 'DATA_LOSS') {
                // UI通知（控えめに）
                const notification = document.createElement('div');
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: ${logEntry.level === 'ERROR' ? '#dc3545' : '#ffc107'};
                    color: white;
                    padding: 10px 15px;
                    border-radius: 5px;
                    font-size: 12px;
                    z-index: 9999;
                    max-width: 300px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                `;
                notification.textContent = `${logEntry.category}: ${logEntry.message}`;
                
                document.body.appendChild(notification);
                
                // 5秒後に自動削除
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 5000);
            }
        },

        /**
         * ログ取得（デバッグ・診断用）
         */
        getLogs(level = null, category = null, hours = 24) {
            try {
                const logs = JSON.parse(localStorage.getItem('voiceProgress_logs') || '[]');
                const cutoffTime = new Date();
                cutoffTime.setHours(cutoffTime.getHours() - hours);

                return logs.filter(log => {
                    const logTime = new Date(log.timestamp);
                    const timeMatch = logTime >= cutoffTime;
                    const levelMatch = !level || log.level === level;
                    const categoryMatch = !category || log.category === category;
                    
                    return timeMatch && levelMatch && categoryMatch;
                });
            } catch (error) {
                console.error('ログ取得失敗:', error);
                return [];
            }
        },

        /**
         * ログエクスポート（ダウンロード）
         */
        exportLogs(filename = null) {
            try {
                const logs = this.getLogs();
                const exportData = {
                    exportTime: new Date().toISOString(),
                    totalLogs: logs.length,
                    logs: logs
                };

                const blob = new Blob([JSON.stringify(exportData, null, 2)], {
                    type: 'application/json'
                });

                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename || `voice_progress_logs_${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);

                this.log(this.LEVELS.INFO, 'EXPORT', `ログをエクスポートしました: ${logs.length}件`);
            } catch (error) {
                this.log(this.LEVELS.ERROR, 'EXPORT', 'ログエクスポート失敗', error);
            }
        },

        /**
         * ログクリア
         */
        clearLogs() {
            try {
                localStorage.removeItem('voiceProgress_logs');
                this.log(this.LEVELS.INFO, 'MAINTENANCE', 'ログをクリアしました');
            } catch (error) {
                console.error('ログクリア失敗:', error);
            }
        },

        /**
         * 便利なショートカットメソッド
         */
        error(category, message, data) { this.log(this.LEVELS.ERROR, category, message, data); },
        warn(category, message, data) { this.log(this.LEVELS.WARN, category, message, data); },
        info(category, message, data) { this.log(this.LEVELS.INFO, category, message, data); },
        debug(category, message, data) { this.log(this.LEVELS.DEBUG, category, message, data); }
    };

        });
    }
}

/**
 * 🔧 Webアプリケーション向けログ管理システム
 */
VoiceProgressTracker.Logger = {
    /**
     * ログレベル定義
     */
    LEVELS: {
        ERROR: 0,   // エラー
        WARN: 1,    // 警告
        INFO: 2,    // 情報
        DEBUG: 3    // デバッグ
    },

    /**
     * 現在のログレベル（プロダクション環境では INFO 推奨）
     */
    currentLevel: 2, // INFO

    /**
     * ログエントリの最大保持数
     */
    maxLogEntries: 1000,

    /**
     * 統一ログ記録
     */
    log(level, category, message, data = null) {
        if (level > this.currentLevel) return;

        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            level: Object.keys(this.LEVELS)[level],
            category,
            message,
            data,
            url: window.location.href,
            userAgent: navigator.userAgent.substring(0, 100) // 短縮版
        };

        // 1. Console出力（開発者向け）
        this.outputToConsole(logEntry);

        // 2. LocalStorage保存（永続化）
        this.saveToLocalStorage(logEntry);

        // 3. IndexedDB保存（大容量データ用）
        this.saveToIndexedDB(logEntry);

        // 4. 重要ログの場合、ユーザー通知
        if (level <= this.LEVELS.WARN) {
            this.notifyUser(logEntry);
        }
    },

    /**
     * Console出力（レベル別）
     */
    outputToConsole(logEntry) {
        const emoji = {
            'ERROR': '❌',
            'WARN': '⚠️',
            'INFO': 'ℹ️',
            'DEBUG': '🔍'
        }[logEntry.level] || 'ℹ️';

        const message = `${emoji} [${logEntry.category}] ${logEntry.message}`;
        
        switch (logEntry.level) {
            case 'ERROR':
                console.error(message, logEntry.data);
                break;
            case 'WARN':
                console.warn(message, logEntry.data);
                break;
            case 'DEBUG':
                console.debug(message, logEntry.data);
                break;
            default:
                console.log(message, logEntry.data);
        }
    },

    /**
     * LocalStorage保存（軽量ログ用）
     */
    saveToLocalStorage(logEntry) {
        try {
            const logs = JSON.parse(localStorage.getItem('voiceProgress_logs') || '[]');
            logs.push(logEntry);

            // 古いログを削除（容量制限）
            if (logs.length > this.maxLogEntries) {
                logs.splice(0, logs.length - this.maxLogEntries);
            }

            localStorage.setItem('voiceProgress_logs', JSON.stringify(logs));
        } catch (error) {
            console.warn('LocalStorageログ保存失敗:', error);
        }
    },

    /**
     * IndexedDB保存（詳細ログ用）
     */
    async saveToIndexedDB(logEntry) {
        try {
            if (window.voiceProgressTracker && window.voiceProgressTracker.db) {
                // ログ専用テーブルがあれば保存
                // 現在は sessions テーブルに重要ログのみ保存
                if (logEntry.level === 'ERROR' || logEntry.category === 'DATA_LOSS') {
                    const logData = {
                        timestamp: logEntry.timestamp,
                        date: logEntry.timestamp.split('T')[0],
                        level: `LOG_${logEntry.level}`,
                        levelScore: 0,
                        duration: 0,
                        wordsPerMinute: 0,
                        contentAccuracy: 0,
                        expectedSentence: logEntry.category,
                        recognizedText: logEntry.message,
                        verificationStatus: 'system_log'
                    };

                    await window.voiceProgressTracker.saveToStore('sessions', logData);
                }
            }
        } catch (error) {
            console.warn('IndexedDBログ保存失敗:', error);
        }
    },

    /**
     * ユーザー通知（重要ログのみ）
     */
    notifyUser(logEntry) {
        if (logEntry.level === 'ERROR' || logEntry.category === 'DATA_LOSS') {
            // UI通知（控えめに）
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${logEntry.level === 'ERROR' ? '#dc3545' : '#ffc107'};
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 9999;
                max-width: 300px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            `;
            notification.textContent = `${logEntry.category}: ${logEntry.message}`;
            
            document.body.appendChild(notification);
            
            // 5秒後に自動削除
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 5000);
        }
    },

    /**
     * ログ取得（デバッグ・診断用）
     */
    getLogs(level = null, category = null, hours = 24) {
        try {
            const logs = JSON.parse(localStorage.getItem('voiceProgress_logs') || '[]');
            const cutoffTime = new Date();
            cutoffTime.setHours(cutoffTime.getHours() - hours);

            return logs.filter(log => {
                const logTime = new Date(log.timestamp);
                const timeMatch = logTime >= cutoffTime;
                const levelMatch = !level || log.level === level;
                const categoryMatch = !category || log.category === category;
                
                return timeMatch && levelMatch && categoryMatch;
            });
        } catch (error) {
            console.error('ログ取得失敗:', error);
            return [];
        }
    },

    /**
     * ログエクスポート（ダウンロード）
     */
    exportLogs(filename = null) {
        try {
            const logs = this.getLogs();
            const exportData = {
                exportTime: new Date().toISOString(),
                totalLogs: logs.length,
                logs: logs
            };

            const blob = new Blob([JSON.stringify(exportData, null, 2)], {
                type: 'application/json'
            });

            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename || `voice_progress_logs_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.log(this.LEVELS.INFO, 'EXPORT', `ログをエクスポートしました: ${logs.length}件`);
        } catch (error) {
            this.log(this.LEVELS.ERROR, 'EXPORT', 'ログエクスポート失敗', error);
        }
    },

    /**
     * ログクリア
     */
    clearLogs() {
        try {
            localStorage.removeItem('voiceProgress_logs');
            this.log(this.LEVELS.INFO, 'MAINTENANCE', 'ログをクリアしました');
        } catch (error) {
            console.error('ログクリア失敗:', error);
        }
    },

    /**
     * 便利なショートカットメソッド
     */
    error(category, message, data) { this.log(this.LEVELS.ERROR, category, message, data); },
    warn(category, message, data) { this.log(this.LEVELS.WARN, category, message, data); },
    info(category, message, data) { this.log(this.LEVELS.INFO, category, message, data); },
    debug(category, message, data) { this.log(this.LEVELS.DEBUG, category, message, data); }
};

// グローバルインスタンス
window.voiceProgressTracker = new VoiceProgressTracker();

/**
 * 🔧 グローバルログ便利関数（開発者コンソールからも使用可能）
 */
window.VoiceLogger = VoiceProgressTracker.Logger;

/**
 * 📊 ログ管理の便利関数
 */
window.LogManager = {
    /**
     * ログ統計表示
     */
    showStats() {
        const logs = VoiceProgressTracker.Logger.getLogs();
        const stats = {
            total: logs.length,
            byLevel: {},
            byCategory: {},
            last24h: logs.filter(log => {
                const logTime = new Date(log.timestamp);
                const dayAgo = new Date();
                dayAgo.setHours(dayAgo.getHours() - 24);
                return logTime >= dayAgo;
            }).length
        };

        logs.forEach(log => {
            stats.byLevel[log.level] = (stats.byLevel[log.level] || 0) + 1;
            stats.byCategory[log.category] = (stats.byCategory[log.category] || 0) + 1;
        });

        console.log('📊 ログ統計:', stats);
        return stats;
    },

    /**
     * エラーログのみ表示
     */
    showErrors(hours = 24) {
        const errorLogs = VoiceProgressTracker.Logger.getLogs('ERROR', null, hours);
        console.log(`❌ 過去${hours}時間のエラーログ:`, errorLogs);
        return errorLogs;
    },

    /**
     * データ喪失関連ログ表示
     */
    showDataLossLogs() {
        const dataLossLogs = VoiceProgressTracker.Logger.getLogs(null, 'DATA_LOSS', 168); // 1週間
        console.log('🚨 データ喪失関連ログ:', dataLossLogs);
        return dataLossLogs;
    },

    /**
     * ログダウンロード
     */
    downloadLogs() {
        VoiceProgressTracker.Logger.exportLogs();
    },

    /**
     * ログクリア（注意して使用）
     */
    clearAllLogs() {
        if (confirm('本当にすべてのログを削除しますか？この操作は取り消せません。')) {
            VoiceProgressTracker.Logger.clearLogs();
        }
    }
};

// 📝 使用例をコンソールに表示
VoiceProgressTracker.Logger.info('SYSTEM', 'ログシステムが利用可能です');
console.log(`
🔧 ログシステム使用方法:

// 基本的なログ記録
VoiceLogger.info('CATEGORY', 'メッセージ');
VoiceLogger.warn('CATEGORY', '警告メッセージ');
VoiceLogger.error('CATEGORY', 'エラーメッセージ', errorObject);

// ログ管理
LogManager.showStats();           // ログ統計表示
LogManager.showErrors();          // エラーログ表示
LogManager.showDataLossLogs();    // データ喪失ログ表示
LogManager.downloadLogs();        // ログダウンロード
LogManager.clearAllLogs();        // ログクリア（注意）

// 直接アクセス
VoiceProgressTracker.Logger.getLogs('ERROR', 'DATA_LOSS', 48);
`);
