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
            
            <!-- 🔍 診断レポート専用エリア（最上部に固定） -->
            <div id="diagnostics-container" class="diagnostics-container">
                <!-- 診断レポートはここに動的に挿入されます -->
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
        
        try {
            if (!this.progressTracker) {
                console.error('❌ 進捗追跡システムが見つかりません');
                alert('進捗追跡システムが利用できません');
                return;
            }

            console.log('🔍 進捗追跡システム確認OK:', this.progressTracker);

            // パネルを表示
            const panel = document.getElementById('voice-progress-panel');
            if (panel) {
                panel.style.display = 'block';
                this.isVisible = true;
                console.log('✅ パネル表示完了');
                
                // 🔧 診断レポートを先に表示（エラーハンドリング強化）
                try {
                    console.log('🔍 診断レポート表示開始...');
                    await this.showDataDiagnostics();
                    console.log('✅ 診断レポート表示完了');
                } catch (diagError) {
                    console.error('❌ 診断レポート表示失敗:', diagError);
                    // 診断レポートが失敗しても続行
                }
                
                // その後、進捗データを表示
                try {
                    console.log('📊 進捗データ表示開始...');
                    await this.loadAndDisplayProgress();
                    console.log('✅ 進捗データ表示完了');
                } catch (progressError) {
                    console.error('❌ 進捗データ表示失敗:', progressError);
                    // 進捗データ表示が失敗しても続行
                }
                
                // 🔧 パネルを最上部にスクロール（診断レポートが見えるように）
                setTimeout(() => {
                    panel.scrollTop = 0;
                    
                    // 🔧 ページ全体もパネルが見えるようにスクロール
                    panel.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start',
                        inline: 'nearest'
                    });
                }, 100);
                
                console.log('✅ 進捗パネル表示完了（診断レポート付き）');
            } else {
                console.error('❌ 進捗パネルが見つかりません');
                alert('進捗パネルの作成に失敗しました');
            }
            
        } catch (error) {
            console.error('❌ 進捗表示失敗:', error);
            alert('進捗データの表示に失敗しました: ' + error.message);
        }
    }
            console.error('❌ 進捗表示失敗:', error);
            alert('進捗データの表示に失敗しました: ' + error.message);
        }
    }
    
    /**
     * 🔍 データ診断機能を表示
     */
    async showDataDiagnostics() {
        console.log('🔍 データ診断開始 - showDataDiagnostics()');
        
        try {
            console.log('🔍 データ診断を実行中...');
            
            // 進捗追跡システムの存在確認
            if (!this.progressTracker) {
                console.warn('⚠️ 進捗追跡システムが利用できません');
                return;
            }
            
            console.log('✅ progressTracker 確認OK');

            // データベース健全性チェック
            console.log('🔍 健全性チェック開始...');
            const healthCheck = await this.progressTracker.checkDatabaseHealth();
            console.log('✅ 健全性チェック完了:', healthCheck);
            
            // データ喪失レポート取得
            console.log('🔍 データ喪失レポート取得...');
            const lossReport = this.progressTracker.getDataLossReport();
            console.log('✅ データ喪失レポート取得完了:', lossReport);
            
            // ストレージ情報取得
            console.log('🔍 ストレージ情報取得...');
            const storageInfo = await this.progressTracker.estimateDbSize();
            console.log('✅ ストレージ情報取得完了:', storageInfo);
            
            console.log('🔍 診断データ:', { healthCheck, lossReport, storageInfo });
            
            // 診断結果を構築
            console.log('🔧 診断HTML構築開始...');
            let diagnosticsHtml = `
                <div class="data-diagnostics" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #007bff; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <h4 style="margin-top: 0; color: #495057; display: flex; align-items: center; gap: 8px;">
                        🔍 データ診断レポート 
                        <span style="font-size: 12px; background: #007bff; color: white; padding: 2px 6px; border-radius: 10px;">リアルタイム</span>
                    </h4>
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
                const backupData = JSON.parse(emergencyBackup);
                diagnosticsHtml += `
                    <div style="margin: 15px 0; padding: 15px; background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%); border-left: 4px solid #007bff; border-radius: 0 5px 5px 0;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            🛟 <strong>緊急バックアップ利用可能</strong>
                            <span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">READY</span>
                        </div>
                        <div style="font-size: 12px; color: #6c757d; margin-bottom: 10px;">
                            作成日時: ${new Date(backupTimestamp).toLocaleString()}<br>
                            復旧可能データ: セッション${backupData.sessionCount}件, 統計${backupData.dailyStatsCount}件
                        </div>
                        <button id="restore-emergency-backup" style="
                            padding: 8px 16px; 
                            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
                            color: white; 
                            border: none; 
                            border-radius: 20px; 
                            font-size: 12px; 
                            font-weight: bold;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            ">
                            🔄 緊急復旧実行
                        </button>
                    </div>
                `;
            } else {
                diagnosticsHtml += `
                    <div style="margin: 10px 0; padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107; color: #856404;">
                        💾 緊急バックアップ: 利用不可（まだ作成されていません）
                    </div>
                `;
            }
            
            diagnosticsHtml += `</div>`;
            
            console.log('📊 診断完了:', { healthCheck, lossReport, storageInfo });
            
            // 診断結果を専用コンテナに挿入
            console.log('🔧 診断レポートDOM挿入開始...');
            const diagnosticsContainer = document.getElementById('diagnostics-container');
            console.log('🔍 診断コンテナ検索結果:', diagnosticsContainer);
            
            if (diagnosticsContainer) {
                console.log('✅ 診断コンテナが見つかりました');
                
                // 既存の診断レポートをクリア
                diagnosticsContainer.innerHTML = '';
                
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = diagnosticsHtml;
                
                console.log('🔧 診断レポートをコンテナに追加...');
                diagnosticsContainer.appendChild(tempDiv.firstElementChild);
                console.log('✅ 診断レポート挿入完了');
                
                // 緊急復旧ボタンのイベントリスナー
                const restoreBtn = document.getElementById('restore-emergency-backup');
                if (restoreBtn) {
                    console.log('✅ 緊急復旧ボタンのイベントリスナー設定');
                    restoreBtn.addEventListener('click', async () => {
                        if (confirm('緊急バックアップからデータを復旧しますか？\n現在のデータは上書きされます。')) {
                            const success = await this.progressTracker.restoreFromEmergencyBackup();
                            if (success) {
                                alert('✅ データ復旧が完了しました');
                                this.showProgress(); // 表示を更新
                            } else {
                                alert('❌ データ復旧に失敗しました');
                            }
                console.log('🔧 診断レポートをコンテナに追加...');
                diagnosticsContainer.appendChild(tempDiv.firstElementChild);
                console.log('✅ 診断レポート挿入完了');
                
                // 緊急復旧ボタンのイベントリスナー
                const restoreBtn = document.getElementById('restore-emergency-backup');
                if (restoreBtn) {
                    console.log('✅ 緊急復旧ボタンのイベントリスナー設定');
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
            } else {
                console.warn('⚠️ 診断コンテナが見つかりません。フォールバック処理を実行...');
                
                // フォールバック：プログレスパネルに直接挿入
                const progressPanel = document.getElementById('voice-progress-panel');
                console.log('🔍 進捗パネル検索結果:', progressPanel);
                
                if (progressPanel) {
                    console.log('✅ 進捗パネルが見つかりました（フォールバック）');
                    
                    const existingDiagnostics = progressPanel.querySelector('.data-diagnostics');
                    if (existingDiagnostics) {
                        existingDiagnostics.remove();
                    }
                    
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = diagnosticsHtml;
                    
                    const contentArea = progressPanel.querySelector('.progress-panel-content');
                    if (contentArea) {
                        console.log('🔧 コンテンツエリアに診断レポートを挿入...');
                        contentArea.insertBefore(tempDiv.firstElementChild, contentArea.firstChild);
                    } else {
                        console.log('🔧 パネルの先頭に診断レポートを挿入...');
                        progressPanel.insertBefore(tempDiv.firstElementChild, progressPanel.firstChild.nextSibling);
                    }
                    
                    console.log('✅ フォールバック挿入完了');
                } else {
                    console.error('❌ 進捗パネルも見つかりません');
                }
            }
            
        } catch (error) {
            console.error('❌ データ診断失敗:', error);
            console.error('❌ エラースタック:', error.stack);
            
            // エラー時でも基本的な診断情報を表示
            const fallbackDiagnostics = `
                <div class="data-diagnostics" style="background: #f8d7da; border: 2px solid #dc3545; padding: 15px; margin: 10px 0; border-radius: 8px;">
                    <h4 style="margin-top: 0; color: #721c24;">❌ 診断エラー</h4>
                    <div style="color: #721c24; margin: 5px 0;">
                        診断機能でエラーが発生しました: ${error.message}
                    </div>
                    <div style="margin: 10px 0; padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107; color: #856404;">
                        💡 手動確認: 開発者コンソール（F12）でログを確認してください
                    </div>
                </div>
            `;
            
            // エラー時のフォールバック表示
            const diagnosticsContainer = document.getElementById('diagnostics-container');
            if (diagnosticsContainer) {
                diagnosticsContainer.innerHTML = fallbackDiagnostics;
                console.log('✅ エラー時のフォールバック診断を表示');
            } else {
                console.warn('⚠️ 診断コンテナが見つからないため、エラー表示をスキップ');
            }
        }
    }
}

// グローバルインスタンス
window.voiceProgressUI = new VoiceProgressUI();
                    }
                }
            }
            
        } catch (error) {
            console.error('❌ データ診断失敗:', error);
            
            // エラー時でも基本的な診断情報を表示
            const fallbackDiagnostics = `
                <div class="data-diagnostics" style="background: #f8d7da; border: 2px solid #dc3545; padding: 15px; margin: 10px 0; border-radius: 8px;">
                    <h4 style="margin-top: 0; color: #721c24;">❌ 診断エラー</h4>
                    <div style="color: #721c24; margin: 5px 0;">
                        診断機能でエラーが発生しました: ${error.message}
                    </div>
                    <div style="margin: 10px 0; padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107; color: #856404;">
                        💡 手動確認: 開発者コンソール（F12）でログを確認してください
                    </div>
                </div>
            `;
            
            const diagnosticsContainer = document.getElementById('diagnostics-container');
            if (diagnosticsContainer) {
                diagnosticsContainer.innerHTML = fallbackDiagnostics;
            }
        }
    }
}

// グローバルインスタンス
window.voiceProgressUI = new VoiceProgressUI();
