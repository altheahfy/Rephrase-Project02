const os = require('os');
const fs = require('fs').promises;
const winston = require('winston');

// ロガー設定
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/monitoring.log' }),
    new winston.transports.Console()
  ]
});

class SystemMonitor {
  constructor() {
    this.alertThresholds = {
      cpu: parseFloat(process.env.CPU_ALERT_THRESHOLD) || 80,
      memory: parseFloat(process.env.MEMORY_ALERT_THRESHOLD) || 80,
      disk: parseFloat(process.env.DISK_ALERT_THRESHOLD) || 85,
      responseTime: parseInt(process.env.RESPONSE_TIME_THRESHOLD) || 5000
    };
    
    this.checkInterval = parseInt(process.env.MONITOR_INTERVAL) || 60000; // 1分
    this.metrics = {
      requests: 0,
      errors: 0,
      responseTime: [],
      uptime: Date.now(),
      lastCheck: Date.now()
    };
    
    this.isRunning = false;
  }

  start() {
    if (this.isRunning) {
      logger.warn('Monitor already running');
      return;
    }

    this.isRunning = true;
    logger.info('System monitoring started');
    
    // 定期チェック開始
    this.monitorInterval = setInterval(() => {
      this.performHealthCheck();
    }, this.checkInterval);

    // プロセス終了時の処理
    process.on('SIGINT', () => this.stop());
    process.on('SIGTERM', () => this.stop());
  }

  stop() {
    if (this.monitorInterval) {
      clearInterval(this.monitorInterval);
      this.monitorInterval = null;
    }
    
    this.isRunning = false;
    logger.info('System monitoring stopped');
  }

  async performHealthCheck() {
    try {
      const health = await this.collectSystemMetrics();
      await this.checkAlerts(health);
      await this.logMetrics(health);
      
      this.metrics.lastCheck = Date.now();
    } catch (error) {
      logger.error('Health check failed:', error);
    }
  }

  async collectSystemMetrics() {
    const now = Date.now();
    
    // CPU使用率
    const cpuUsage = await this.getCpuUsage();
    
    // メモリ使用率
    const memoryStats = this.getMemoryStats();
    
    // ディスク使用率
    const diskStats = await this.getDiskStats();
    
    // プロセス情報
    const processStats = this.getProcessStats();
    
    // アプリケーション統計
    const appStats = this.getAppStats();
    
    return {
      timestamp: now,
      cpu: cpuUsage,
      memory: memoryStats,
      disk: diskStats,
      process: processStats,
      application: appStats,
      uptime: now - this.metrics.uptime
    };
  }

  async getCpuUsage() {
    const cpus = os.cpus();
    let totalIdle = 0;
    let totalTick = 0;

    cpus.forEach(cpu => {
      for (type in cpu.times) {
        totalTick += cpu.times[type];
      }
      totalIdle += cpu.times.idle;
    });

    const usage = 100 - ~~(100 * totalIdle / totalTick);
    return {
      usage: usage,
      cores: cpus.length,
      model: cpus[0].model
    };
  }

  getMemoryStats() {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;
    const usagePercent = (usedMem / totalMem) * 100;

    const processMemory = process.memoryUsage();

    return {
      total: Math.round(totalMem / 1024 / 1024), // MB
      used: Math.round(usedMem / 1024 / 1024),
      free: Math.round(freeMem / 1024 / 1024),
      usagePercent: Math.round(usagePercent),
      process: {
        rss: Math.round(processMemory.rss / 1024 / 1024),
        heapTotal: Math.round(processMemory.heapTotal / 1024 / 1024),
        heapUsed: Math.round(processMemory.heapUsed / 1024 / 1024),
        external: Math.round(processMemory.external / 1024 / 1024)
      }
    };
  }

  async getDiskStats() {
    try {
      // Windowsでの簡易ディスク容量チェック
      const stats = await fs.stat('.');
      return {
        available: 'N/A', // Windows環境では簡易実装
        used: 'N/A',
        total: 'N/A',
        usagePercent: 0
      };
    } catch (error) {
      logger.warn('Could not get disk stats:', error.message);
      return {
        available: 'Error',
        used: 'Error',
        total: 'Error',
        usagePercent: 0
      };
    }
  }

  getProcessStats() {
    return {
      pid: process.pid,
      uptime: Math.round(process.uptime()),
      nodeVersion: process.version,
      platform: os.platform(),
      arch: os.arch(),
      loadAverage: os.loadavg()
    };
  }

  getAppStats() {
    const avgResponseTime = this.metrics.responseTime.length > 0 
      ? this.metrics.responseTime.reduce((a, b) => a + b, 0) / this.metrics.responseTime.length 
      : 0;

    const errorRate = this.metrics.requests > 0 
      ? (this.metrics.errors / this.metrics.requests) * 100 
      : 0;

    return {
      requests: this.metrics.requests,
      errors: this.metrics.errors,
      errorRate: Math.round(errorRate * 100) / 100,
      averageResponseTime: Math.round(avgResponseTime),
      activeConnections: global.activeConnections || 0,
      authenticatedUsers: global.authenticatedUsers || 0
    };
  }

  async checkAlerts(health) {
    const alerts = [];

    // CPU使用率アラート
    if (health.cpu.usage > this.alertThresholds.cpu) {
      alerts.push({
        type: 'CPU_HIGH',
        level: 'warning',
        message: `CPU usage is ${health.cpu.usage}% (threshold: ${this.alertThresholds.cpu}%)`,
        value: health.cpu.usage,
        threshold: this.alertThresholds.cpu
      });
    }

    // メモリ使用率アラート
    if (health.memory.usagePercent > this.alertThresholds.memory) {
      alerts.push({
        type: 'MEMORY_HIGH',
        level: 'warning',
        message: `Memory usage is ${health.memory.usagePercent}% (threshold: ${this.alertThresholds.memory}%)`,
        value: health.memory.usagePercent,
        threshold: this.alertThresholds.memory
      });
    }

    // レスポンス時間アラート
    if (health.application.averageResponseTime > this.alertThresholds.responseTime) {
      alerts.push({
        type: 'RESPONSE_TIME_HIGH',
        level: 'warning',
        message: `Average response time is ${health.application.averageResponseTime}ms (threshold: ${this.alertThresholds.responseTime}ms)`,
        value: health.application.averageResponseTime,
        threshold: this.alertThresholds.responseTime
      });
    }

    // エラー率アラート
    if (health.application.errorRate > 5) {
      alerts.push({
        type: 'ERROR_RATE_HIGH',
        level: 'error',
        message: `Error rate is ${health.application.errorRate}% (threshold: 5%)`,
        value: health.application.errorRate,
        threshold: 5
      });
    }

    // アラート処理
    for (const alert of alerts) {
      await this.handleAlert(alert);
    }
  }

  async handleAlert(alert) {
    logger.warn(`ALERT [${alert.type}]: ${alert.message}`);
    
    // 将来的にはSlack、メール、webhook等への通知を実装
    if (process.env.ALERT_WEBHOOK_URL) {
      try {
        // Webhook通知の実装例
        await this.sendWebhookAlert(alert);
      } catch (error) {
        logger.error('Failed to send webhook alert:', error);
      }
    }
  }

  async sendWebhookAlert(alert) {
    // Webhook実装は将来追加
    logger.info(`Webhook alert would be sent: ${alert.type}`);
  }

  async logMetrics(health) {
    logger.info('System Health Check', {
      cpu: health.cpu.usage + '%',
      memory: health.memory.usagePercent + '%',
      requests: health.application.requests,
      errors: health.application.errors,
      avgResponseTime: health.application.averageResponseTime + 'ms',
      uptime: Math.round(health.uptime / 1000) + 's'
    });

    // メトリクス履歴保存（開発時は簡易ファイル保存）
    if (process.env.NODE_ENV !== 'production') {
      await this.saveMetricsToFile(health);
    }
  }

  async saveMetricsToFile(health) {
    try {
      const logsDir = './logs';
      await fs.mkdir(logsDir, { recursive: true });
      
      const metricsFile = `${logsDir}/metrics-${new Date().toISOString().split('T')[0]}.jsonl`;
      const metricsLine = JSON.stringify({
        timestamp: health.timestamp,
        cpu: health.cpu.usage,
        memory: health.memory.usagePercent,
        requests: health.application.requests,
        errors: health.application.errors,
        responseTime: health.application.averageResponseTime
      }) + '\n';
      
      await fs.appendFile(metricsFile, metricsLine);
    } catch (error) {
      logger.error('Failed to save metrics to file:', error);
    }
  }

  recordRequest(responseTime) {
    this.metrics.requests++;
    this.metrics.responseTime.push(responseTime);
    
    // 直近100件のレスポンス時間のみ保持
    if (this.metrics.responseTime.length > 100) {
      this.metrics.responseTime = this.metrics.responseTime.slice(-100);
    }
  }

  recordError() {
    this.metrics.errors++;
  }

  getHealthStatus() {
    return {
      status: this.isRunning ? 'healthy' : 'stopped',
      uptime: Date.now() - this.metrics.uptime,
      lastCheck: this.metrics.lastCheck,
      metrics: this.metrics
    };
  }
}

// Express.js用ミドルウェア
function createMonitoringMiddleware(monitor) {
  return (req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
      const responseTime = Date.now() - start;
      monitor.recordRequest(responseTime);
      
      if (res.statusCode >= 400) {
        monitor.recordError();
      }
    });
    
    next();
  };
}

// スタンドアロン実行時
if (require.main === module) {
  const monitor = new SystemMonitor();
  monitor.start();
  
  // 1万ユーザー対応のテストデータ生成
  setInterval(() => {
    // 擬似的なリクエスト記録
    monitor.recordRequest(Math.random() * 1000);
    
    // 擬似的なエラー（5%の確率）
    if (Math.random() < 0.05) {
      monitor.recordError();
    }
    
    // アクティブユーザー数シミュレーション
    global.activeConnections = Math.floor(Math.random() * 1000);
    global.authenticatedUsers = Math.floor(Math.random() * 500);
  }, 1000);
}

module.exports = { SystemMonitor, createMonitoringMiddleware };
