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
                <h3>📊 学習データ管理</h3>
                <button id="progress-close-btn" class="close-btn">×</button>
            </div>
            
            <div class="progress-panel-content">
                <!-- データ管理セクション -->
                <div class="data-management-section">
                    <h4>� データバックアップ・復元</h4>
                    
                    <!-- ダウンロード -->
                    <div class="backup-row">
                        <div class="backup-info">
                            <span class="backup-icon">⬇️</span>
                            <div class="backup-text">
                                <strong>学習データをダウンロード</strong>
                                <small>現在の学習進捗をJSONファイルで保存</small>
                            </div>
                        </div>
                        <button id="export-data-btn" class="action-btn primary">ダウンロード</button>
                    </div>
                    
                    <!-- アップロード -->
                    <div class="backup-row">
                        <div class="backup-info">
                            <span class="backup-icon">⬆️</span>
                            <div class="backup-text">
                                <strong>学習データをアップロード</strong>
                                <small>保存した学習進捗を復元</small>
                            </div>
                        </div>
                        <div class="upload-container">
                            <input type="file" id="import-data-input" accept=".json" style="display: none;">
                            <button id="import-data-btn" class="action-btn secondary">ファイル選択</button>
                        </div>
                    </div>
                    
                    <!-- 現在のデータ情報 -->
                    <div class="current-data-info">
                        <h5>📈 現在のデータ</h5>
                        <div id="data-summary">データを読み込み中...</div>
                    </div>
                    
                    <!-- 危険操作 -->
                    <div class="danger-section">
                        <h5>⚠️ 危険操作</h5>
                        <button id="clear-data-btn" class="action-btn danger">全データ削除</button>
                        <small>※この操作は取り消せません</small>
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
        
        // データエクスポート
        const exportBtn = document.getElementById('export-data-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportData());
        }
        
        // データインポート
        const importBtn = document.getElementById('import-data-btn');
        const importInput = document.getElementById('import-data-input');
        
        if (importBtn && importInput) {
            importBtn.addEventListener('click', () => {
                importInput.click();
            });
            
            importInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.importData(file);
                }
            });
        }
        
        // 全データクリア
        const clearBtn = document.getElementById('clear-data-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearAllData());
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
            
            // 現在のデータ情報を表示
            await this.loadDataSummary();
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
        console.log('🎯 loadAndDisplayProgress開始');
        console.log('📊 progressTracker:', this.progressTracker);
        console.log('📊 progressTracker.db:', this.progressTracker?.db);
        
        if (!this.progressTracker) {
            console.error('❌ progressTrackerが見つかりません');
            this.displayError('進捗追跡システムが初期化されていません');
            return;
        }
        
        if (!this.progressTracker.db) {
            console.error('❌ データベースが初期化されていません');
            this.displayError('データベースが初期化されていません');
            return;
        }
        
        try {
            console.log('✅ ローディング表示開始');
            // ローディング表示
            this.showLoading(true);
            
            console.log('📊 データ取得開始 - 期間:', this.currentPeriod);
            // データ取得
            const progressData = await this.progressTracker.getProgressData(this.currentPeriod);
            console.log('📊 取得したデータ:', progressData);
            
            if (progressData) {
                console.log('✅ データ表示処理開始');
                this.displayProgressData(progressData);
            } else {
                console.log('⚠️ データなし - NoData表示');
                this.displayNoData();
            }
            
        } catch (error) {
            console.error('❌ 進捗データ表示エラー:', error);
            console.error('❌ エラースタック:', error.stack);
            this.displayError(error.message);
        } finally {
            console.log('🏁 ローディング非表示');
            this.showLoading(false);
        }
    }
    
    /**
     * ローディング表示を切り替え
     */
    showLoading(show) {
        console.log(`🔄 showLoading(${show}) 開始`);
        const loading = document.querySelector('.progress-loading');
        const stats = document.querySelector('.progress-stats');
        
        console.log('🔍 loading要素:', loading);
        console.log('🔍 stats要素:', stats);
        
        if (loading && stats) {
            loading.style.display = show ? 'block' : 'none';
            stats.style.display = show ? 'none' : 'block';
            console.log(`✅ ローディング${show ? '表示' : '非表示'}完了`);
        } else {
            console.error('❌ ローディング要素またはstats要素が見つかりません');
            if (!loading) console.error('❌ .progress-loading が見つかりません');
            if (!stats) console.error('❌ .progress-stats が見つかりません');
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
        if (!confirm('本当に全ての進捗データを削除しますか？この操作は取り消せません。')) {
            return;
        }
        
        try {
            await this.progressTracker.clearAllData();
            alert('✅ 全データを削除しました');
            await this.loadAndDisplayProgress();
        } catch (error) {
            console.error('❌ データクリア失敗:', error);
            alert('❌ データクリアに失敗しました');
        }
    }
    
    /**
     * データをエクスポート
     */
    async exportData() {
        try {
            const data = await this.progressTracker.getAllData();
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
     * データをインポート
     */
    async importData(file) {
        try {
            const text = await file.text();
            const data = JSON.parse(text);
            
            if (!data.sessions || !data.dailyStats) {
                throw new Error('無効なデータ形式です');
            }
            
            if (confirm(`${data.sessions.length}個のセッションデータを復元しますか？\n現在のデータは上書きされます。`)) {
                await this.progressTracker.importData(data);
                alert('✅ データの復元が完了しました');
                
                // 概要を更新
                await this.loadDataSummary();
            }
            
        } catch (error) {
            console.error('データインポートエラー:', error);
            alert('❌ データの復元に失敗しました: ' + error.message);
        }
    }
    
    /**
     * 現在のデータ概要を表示
     */
    async loadDataSummary() {
        const summaryDiv = document.getElementById('data-summary');
        if (!summaryDiv) return;
        
        try {
            if (!this.progressTracker || !this.progressTracker.db) {
                summaryDiv.innerHTML = '❌ データベースが初期化されていません';
                return;
            }
            
            const allData = await this.progressTracker.getAllData();
            const sessions = allData.sessions || [];
            const stats = allData.dailyStats || [];
            
            summaryDiv.innerHTML = `
                <div class="summary-item">
                    <strong>学習セッション:</strong> ${sessions.length}回
                </div>
                <div class="summary-item">
                    <strong>日別統計:</strong> ${stats.length}日分
                </div>
                <div class="summary-item">
                    <strong>最終更新:</strong> ${sessions.length > 0 ? new Date(sessions[sessions.length - 1].timestamp).toLocaleString() : '未実施'}
                </div>
            `;
            
        } catch (error) {
            console.error('データ概要取得エラー:', error);
            summaryDiv.innerHTML = '❌ データの読み込みに失敗しました';
        }
    }
}

// グローバルインスタンス
window.voiceProgressUI = new VoiceProgressUI();
