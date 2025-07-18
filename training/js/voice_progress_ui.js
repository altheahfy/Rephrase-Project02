/**
 * 音声学習進捗表示UI
 * 学習者の上達度を視覚的に表示する
 */
class VoiceProgressUI {
    constructor() {
        this.progressTracker = window.voiceProgressTracker;
        this.isVisible = false;
        this.currentPeriod = 'week';
        
        this.init();
    }
    
    /**
     * 初期化
     */
    init() {
        this.createProgressPanel();
        this.setupEventListeners();
        console.log('✅ 音声進捗表示UI初期化完了');
    }
    
    /**
     * 進捗パネルを作成
     */
    createProgressPanel() {
        // 既存のパネルがあれば削除
        const existingPanel = document.getElementById('voice-progress-panel');
        if (existingPanel) {
            existingPanel.remove();
        }
        
        const panel = document.createElement('div');
        panel.id = 'voice-progress-panel';
        panel.className = 'voice-progress-panel';
        panel.style.display = 'none';
        
        panel.innerHTML = `
            <div class="progress-panel-header">
                <h3>📊 音声学習進捗</h3>
                <button id="progress-close-btn" class="close-btn">×</button>
            </div>
            
            <div class="progress-panel-content">
                <!-- 期間選択タブ -->
                <div class="period-tabs">
                    <button class="period-tab active" data-period="week">1週間</button>
                    <button class="period-tab" data-period="month">1ヶ月</button>
                    <button class="period-tab" data-period="quarter">3ヶ月</button>
                    <button class="period-tab" data-period="year">1年</button>
                </div>
                
                <!-- メイン統計表示 -->
                <div class="progress-stats-container">
                    <div class="progress-loading">📊 データを読み込み中...</div>
                    <div class="progress-stats" style="display: none;">
                        <!-- 基本統計 -->
                        <div class="stats-row">
                            <div class="stat-card">
                                <div class="stat-label">練習回数</div>
                                <div class="stat-value" id="total-sessions">-</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-label">平均レベル</div>
                                <div class="stat-value" id="average-level">-</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-label">上達度</div>
                                <div class="stat-value" id="improvement">-</div>
                            </div>
                        </div>
                        
                        <!-- レベル分布 -->
                        <div class="level-distribution">
                            <h4>📈 レベル分布</h4>
                            <div class="level-bars">
                                <div class="level-bar">
                                    <span class="level-label">🐌 初心者</span>
                                    <div class="bar-container">
                                        <div class="bar beginner" id="bar-beginner"></div>
                                        <span class="bar-value" id="count-beginner">0</span>
                                    </div>
                                </div>
                                <div class="level-bar">
                                    <span class="level-label">📈 中級者</span>
                                    <div class="bar-container">
                                        <div class="bar intermediate" id="bar-intermediate"></div>
                                        <span class="bar-value" id="count-intermediate">0</span>
                                    </div>
                                </div>
                                <div class="level-bar">
                                    <span class="level-label">🚀 上級者</span>
                                    <div class="bar-container">
                                        <div class="bar advanced" id="bar-advanced"></div>
                                        <span class="bar-value" id="count-advanced">0</span>
                                    </div>
                                </div>
                                <div class="level-bar">
                                    <span class="level-label">⚡ 達人</span>
                                    <div class="bar-container">
                                        <div class="bar expert" id="bar-expert"></div>
                                        <span class="bar-value" id="count-expert">0</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- 進捗チャート -->
                        <div class="progress-chart-container">
                            <h4>📉 進捗推移</h4>
                            <canvas id="progress-chart" width="400" height="200"></canvas>
                        </div>
                        
                        <!-- 最高記録 -->
                        <div class="best-performance">
                            <h4>🏆 最高記録</h4>
                            <div id="best-day-info">データなし</div>
                        </div>
                        
                        <!-- データ管理 -->
                        <div class="data-management">
                            <h4>🔧 データ管理</h4>
                            <button id="clear-data-btn" class="danger-btn">全データクリア</button>
                            <button id="export-data-btn" class="secondary-btn">データエクスポート</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(panel);
    }
    
    /**
     * イベントリスナーを設定
     */
    setupEventListeners() {
        // 閉じるボタン
        const closeBtn = document.getElementById('progress-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hideProgressPanel());
        }
        
        // 期間選択タブ
        const periodTabs = document.querySelectorAll('.period-tab');
        periodTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                const period = e.target.dataset.period;
                this.selectPeriod(period);
            });
        });
        
        // データクリアボタン
        const clearBtn = document.getElementById('clear-data-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearAllData());
        }
        
        // データエクスポートボタン
        const exportBtn = document.getElementById('export-data-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportData());
        }
    }
    
    /**
     * 進捗パネルを表示
     */
    async showProgressPanel() {
        const panel = document.getElementById('voice-progress-panel');
        if (panel) {
            panel.style.display = 'block';
            this.isVisible = true;
            
            // データを読み込んで表示
            await this.loadAndDisplayProgress();
        }
    }
    
    /**
     * 進捗パネルを非表示
     */
    hideProgressPanel() {
        const panel = document.getElementById('voice-progress-panel');
        if (panel) {
            panel.style.display = 'none';
            this.isVisible = false;
        }
    }
    
    /**
     * 期間を選択
     */
    async selectPeriod(period) {
        this.currentPeriod = period;
        
        // タブの見た目を更新
        document.querySelectorAll('.period-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-period="${period}"]`).classList.add('active');
        
        // データを再読み込み
        await this.loadAndDisplayProgress();
    }
    
    /**
     * 進捗データを読み込んで表示
     */
    async loadAndDisplayProgress() {
        if (!this.progressTracker || !this.progressTracker.db) {
            console.error('❌ 進捗追跡システムが初期化されていません');
            return;
        }
        
        try {
            // ローディング表示
            this.showLoading(true);
            
            // データ取得
            const progressData = await this.progressTracker.getProgressData(this.currentPeriod);
            
            if (progressData) {
                this.displayProgressData(progressData);
            } else {
                this.displayNoData();
            }
            
        } catch (error) {
            console.error('❌ 進捗データ表示エラー:', error);
            this.displayError(error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    /**
     * ローディング表示を切り替え
     */
    showLoading(show) {
        const loading = document.querySelector('.progress-loading');
        const stats = document.querySelector('.progress-stats');
        
        if (loading && stats) {
            loading.style.display = show ? 'block' : 'none';
            stats.style.display = show ? 'none' : 'block';
        }
    }
    
    /**
     * 進捗データを表示
     */
    displayProgressData(data) {
        console.log('📊 進捗データ表示:', data);
        
        // 基本統計
        document.getElementById('total-sessions').textContent = data.totalSessions;
        document.getElementById('average-level').textContent = this.formatLevel(data.averageLevel);
        document.getElementById('improvement').textContent = this.formatImprovement(data.improvement);
        
        // レベル分布
        this.displayLevelDistribution(data.levelDistribution, data.totalSessions);
        
        // チャート
        this.displayChart(data.chartData);
        
        // 最高記録
        this.displayBestDay(data.bestDay);
    }
    
    /**
     * レベル値をフォーマット
     */
    formatLevel(level) {
        if (level === 0) return 'データなし';
        if (level < 1) return '要練習';
        if (level < 2) return '🐌 初心者';
        if (level < 3) return '📈 中級者';
        if (level < 4) return '🚀 上級者';
        return '⚡ 達人';
    }
    
    /**
     * 上達度をフォーマット
     */
    formatImprovement(improvement) {
        if (improvement === 0) return 'データ不足';
        const sign = improvement > 0 ? '+' : '';
        return `${sign}${improvement.toFixed(1)}%`;
    }
    
    /**
     * レベル分布を表示
     */
    displayLevelDistribution(distribution, total) {
        const levels = ['beginner', 'intermediate', 'advanced', 'expert'];
        
        levels.forEach(level => {
            const count = distribution[level] || 0;
            const percentage = total > 0 ? (count / total) * 100 : 0;
            
            const bar = document.getElementById(`bar-${level}`);
            const countElement = document.getElementById(`count-${level}`);
            
            if (bar && countElement) {
                bar.style.width = `${percentage}%`;
                countElement.textContent = count;
            }
        });
    }
    
    /**
     * 進捗チャートを表示
     */
    displayChart(chartData) {
        const canvas = document.getElementById('progress-chart');
        if (!canvas || !chartData || chartData.length === 0) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // キャンバスをクリア
        ctx.clearRect(0, 0, width, height);
        
        // データ準備
        const maxLevel = 4;
        const margin = 40;
        const chartWidth = width - margin * 2;
        const chartHeight = height - margin * 2;
        
        // 軸を描画
        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 1;
        
        // Y軸
        ctx.beginPath();
        ctx.moveTo(margin, margin);
        ctx.lineTo(margin, height - margin);
        ctx.stroke();
        
        // X軸
        ctx.beginPath();
        ctx.moveTo(margin, height - margin);
        ctx.lineTo(width - margin, height - margin);
        ctx.stroke();
        
        // データ点を描画
        if (chartData.length > 1) {
            ctx.strokeStyle = '#2196F3';
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            chartData.forEach((point, index) => {
                const x = margin + (index / (chartData.length - 1)) * chartWidth;
                const y = height - margin - (point.averageLevel / maxLevel) * chartHeight;
                
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            
            ctx.stroke();
            
            // データ点を丸で表示
            ctx.fillStyle = '#2196F3';
            chartData.forEach((point, index) => {
                const x = margin + (index / (chartData.length - 1)) * chartWidth;
                const y = height - margin - (point.averageLevel / maxLevel) * chartHeight;
                
                ctx.beginPath();
                ctx.arc(x, y, 3, 0, 2 * Math.PI);
                ctx.fill();
            });
        }
        
        // ラベル
        ctx.fillStyle = '#666';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('時間経過', width / 2, height - 10);
        
        ctx.save();
        ctx.translate(15, height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText('レベル', 0, 0);
        ctx.restore();
    }
    
    /**
     * 最高記録を表示
     */
    displayBestDay(bestDay) {
        const element = document.getElementById('best-day-info');
        if (!element) return;
        
        if (!bestDay) {
            element.innerHTML = 'まだ記録がありません';
            return;
        }
        
        const date = new Date(bestDay.date).toLocaleDateString('ja-JP');
        const level = this.formatLevel(bestDay.averageLevel);
        
        element.innerHTML = `
            <div class="best-day-card">
                <div class="best-day-date">📅 ${date}</div>
                <div class="best-day-level">🎯 ${level}</div>
                <div class="best-day-sessions">🔄 ${bestDay.sessionCount}回練習</div>
            </div>
        `;
    }
    
    /**
     * データなし表示
     */
    displayNoData() {
        const statsContainer = document.querySelector('.progress-stats');
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="no-data">
                    <h3>📊 データがありません</h3>
                    <p>音声練習を開始すると進捗が表示されます</p>
                </div>
            `;
        }
    }
    
    /**
     * エラー表示
     */
    displayError(message) {
        const statsContainer = document.querySelector('.progress-stats');
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="error-message">
                    <h3>❌ エラー</h3>
                    <p>${message}</p>
                </div>
            `;
        }
    }
    
    /**
     * 全データをクリア
     */
    async clearAllData() {
        // 🚨 強化された警告とデータ保護
        const healthCheck = await this.progressTracker.checkDatabaseHealth();
        const sessionCount = healthCheck.sessionCount || 0;
        
        if (sessionCount === 0) {
            alert('クリアするデータがありません');
            return;
        }
        
        const warningMessage = `⚠️ 警告: 学習進捗データの完全削除\n\n` +
                              `削除されるデータ:\n` +
                              `• セッション記録: ${sessionCount}件\n` +
                              `• 日別統計: ${healthCheck.dailyStatsCount || 0}件\n\n` +
                              `この操作は取り消せません。\n` +
                              `削除前に自動バックアップが作成されます。\n\n` +
                              `本当にすべてのデータを削除しますか？`;
        
        // 二段階確認
        if (!confirm(warningMessage)) {
            return;
        }
        
        if (!confirm('最終確認: 本当にすべての学習進捗を削除しますか？')) {
            return;
        }
        
        try {
            console.log('🗑️ ユーザーによる進捗データクリア実行...');
            
            await this.progressTracker.clearAllData();
            alert(`✅ 全ての進捗データ（${sessionCount}件）をクリアしました\n💾 削除前のバックアップが保存されています`);
            await this.loadAndDisplayProgress();
            
        } catch (error) {
            console.error('❌ データクリア失敗:', error);
            alert('❌ データクリアに失敗しました\n詳細: ' + error.message);
        }
    }
    
    /**
     * データをエクスポート
     */
    async exportData() {
        try {
            const data = await this.progressTracker.getProgressData('year');
            const jsonData = JSON.stringify(data, null, 2);
            
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `voice_progress_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            URL.revokeObjectURL(url);
            
        } catch (error) {
            console.error('❌ データエクスポート失敗:', error);
            alert('❌ データエクスポートに失敗しました');
        }
    }
    
    /**
     * 進捗分析とデータ管理パネルを表示
     */
    async showProgress() {
        console.log('📊 学習進捗データ表示を開始...');
        
        // 🔧 データ診断を先に実行
        await this.showDataDiagnostics();
        
        if (!this.progressTracker) {
            alert('進捗追跡システムが利用できません');
            return;
        }
        
        // 進捗パネルを表示
        this.showProgressPanel();
    }
    
    /**
     * 🔍 データ診断機能を表示
     */
    async showDataDiagnostics() {
        try {
            console.log('🔍 データ診断を実行中...');
            
            // データベース健全性チェック
            const healthCheck = await this.progressTracker.checkDatabaseHealth();
            
            // データ喪失レポート取得
            const lossReport = this.progressTracker.getDataLossReport();
            
            // ストレージ情報取得
            const storageInfo = await this.progressTracker.estimateDbSize();
            
            // 診断結果を構築
            let diagnosticsHtml = `
                <div class="data-diagnostics" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <h4 style="margin-top: 0; color: #495057;">🔍 データ診断レポート</h4>
            `;
            
            // 健全性チェック結果
            if (healthCheck.healthy) {
                diagnosticsHtml += `
                    <div style="color: #28a745; margin: 5px 0;">
                        ✅ データベース状態: 正常
                        <div style="font-size: 12px; color: #6c757d; margin-left: 20px;">
                            • セッション数: ${healthCheck.sessionCount}件<br>
                            • 日別統計: ${healthCheck.dailyStatsCount}件<br>
                            • 直近1週間: ${healthCheck.recentSessionCount}件
                        </div>
                    </div>
                `;
            } else {
                diagnosticsHtml += `
                    <div style="color: #dc3545; margin: 5px 0;">
                        ❌ データベース問題: ${healthCheck.issue}
                    </div>
                `;
            }
            
            // ストレージ情報
            if (storageInfo) {
                const usagePercent = ((storageInfo.usage / storageInfo.quota) * 100).toFixed(1);
                diagnosticsHtml += `
                    <div style="color: #17a2b8; margin: 5px 0;">
                        💾 ストレージ使用量: ${storageInfo.usageInMB}MB / ${storageInfo.quotaInMB}MB (${usagePercent}%)
                    </div>
                `;
            }
            
            // データ喪失履歴
            if (lossReport.totalIncidents > 0) {
                diagnosticsHtml += `
                    <div style="color: #ffc107; margin: 5px 0;">
                        ⚠️ データ喪失履歴: ${lossReport.totalIncidents}回（合計${lossReport.totalLostData}件）
                        <div style="font-size: 12px; color: #6c757d; margin-left: 20px;">
                            最新インシデント:
                `;
                
                lossReport.incidents.slice(-3).forEach(incident => {
                    diagnosticsHtml += `
                        <br>• ${new Date(incident.timestamp).toLocaleString()}: ${incident.lostCount}件喪失
                    `;
                });
                
                diagnosticsHtml += `</div></div>`;
            } else {
                diagnosticsHtml += `
                    <div style="color: #28a745; margin: 5px 0;">
                        ✅ データ喪失履歴: なし
                    </div>
                `;
            }
            
            // 最後のバックアップ情報
            const lastBackup = localStorage.getItem('voiceProgress_lastPeriodicBackup');
            if (lastBackup) {
                const backupDate = new Date(lastBackup);
                const hoursSinceBackup = (new Date() - backupDate) / (1000 * 60 * 60);
                
                diagnosticsHtml += `
                    <div style="color: ${hoursSinceBackup < 24 ? '#28a745' : '#ffc107'}; margin: 5px 0;">
                        💾 最後のバックアップ: ${backupDate.toLocaleString()} (${hoursSinceBackup.toFixed(1)}時間前)
                    </div>
                `;
            } else {
                diagnosticsHtml += `
                    <div style="color: #ffc107; margin: 5px 0;">
                        💾 最後のバックアップ: 未実行
                    </div>
                `;
            }
            
            // 復旧オプション
            const emergencyBackup = localStorage.getItem('voiceProgress_emergencyBackup');
            if (emergencyBackup) {
                const backupTimestamp = localStorage.getItem('voiceProgress_emergencyBackup_timestamp');
                diagnosticsHtml += `
                    <div style="margin: 10px 0; padding: 10px; background: #e7f3ff; border-left: 4px solid #007bff;">
                        🛟 緊急バックアップ利用可能: ${new Date(backupTimestamp).toLocaleString()}
                        <button id="restore-emergency-backup" style="margin-left: 10px; padding: 4px 8px; background: #007bff; color: white; border: none; border-radius: 3px; font-size: 11px;">
                            緊急復旧実行
                        </button>
                    </div>
                `;
            }
            
            diagnosticsHtml += `</div>`;
            
            console.log('📊 診断完了:', { healthCheck, lossReport, storageInfo });
            
            // 診断結果をプログレスパネルの先頭に挿入
            const progressPanel = document.getElementById('voice-progress-panel');
            if (progressPanel) {
                const existingDiagnostics = progressPanel.querySelector('.data-diagnostics');
                if (existingDiagnostics) {
                    existingDiagnostics.remove();
                }
                
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = diagnosticsHtml;
                
                progressPanel.insertBefore(tempDiv.firstElementChild, progressPanel.firstChild);
                
                // 緊急復旧ボタンのイベントリスナー
                const restoreBtn = document.getElementById('restore-emergency-backup');
                if (restoreBtn) {
                    restoreBtn.addEventListener('click', async () => {
                        if (confirm('緊急バックアップからデータを復旧しますか？\n現在のデータは上書きされます。')) {
                            const success = await this.progressTracker.restoreFromEmergencyBackup();
                            if (success) {
                                alert('✅ データ復旧が完了しました');
                                this.showProgress(); // 表示を更新
                            } else {
                                alert('❌ データ復旧に失敗しました');
                            }
                        }
                    });
                }
            }
            
        } catch (error) {
            console.error('❌ データ診断失敗:', error);
        }
    }
}

// グローバルインスタンス
window.voiceProgressUI = new VoiceProgressUI();
