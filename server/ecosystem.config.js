// PM2 Ecosystem Configuration
// さくらインターネット本番環境対応

module.exports = {
  apps: [
    {
      name: 'rephrase-app',
      script: 'server.js',
      instances: process.env.NODE_ENV === 'production' ? 'max' : 1,
      exec_mode: 'cluster',
      
      // 本番環境設定
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000,
        JWT_SECRET: process.env.JWT_SECRET,
        DB_HOST: process.env.SAKURA_DB_HOST || 'localhost',
        DB_PORT: process.env.SAKURA_DB_PORT || 3306,
        DB_NAME: process.env.SAKURA_DB_NAME || 'rephrase_prod',
        DB_USER: process.env.SAKURA_DB_USER,
        DB_PASSWORD: process.env.SAKURA_DB_PASSWORD
      },
      
      // 開発環境設定
      env_development: {
        NODE_ENV: 'development',
        PORT: 3000,
        watch: true,
        ignore_watch: ['node_modules', 'logs', 'backups']
      },
      
      // メモリ・CPU制限
      max_memory_restart: '1G',
      max_restarts: 10,
      min_uptime: '10s',
      
      // ログ設定
      log_file: 'logs/pm2-combined.log',
      out_file: 'logs/pm2-out.log',
      error_file: 'logs/pm2-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      
      // 自動再起動設定
      autorestart: true,
      watch_delay: 1000,
      
      // 環境変数
      env: {
        NODE_ENV: 'development',
        PORT: 3000
      }
    },
    
    // 監視・メトリクス収集サービス
    {
      name: 'rephrase-monitor',
      script: 'scripts/monitor.js',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      max_memory_restart: '200M',
      
      env: {
        NODE_ENV: process.env.NODE_ENV || 'development',
        METRICS_PORT: 9090
      }
    },
    
    // バックアップサービス
    {
      name: 'rephrase-backup',
      script: 'scripts/backup.js',
      instances: 1,
      exec_mode: 'fork',
      autorestart: false,
      cron_restart: '0 2 * * *', // 毎日午前2時
      
      env: {
        NODE_ENV: process.env.NODE_ENV || 'development',
        BACKUP_ENABLED: true
      }
    }
  ],

  // デプロイ設定（さくらインターネット用）
  deploy: {
    production: {
      user: 'sakura-user',
      host: process.env.SAKURA_HOST,
      ref: 'origin/master',
      repo: 'https://github.com/your-username/rephrase-project.git',
      path: '/home/sakura-user/rephrase',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': 'apt-get update && apt-get install -y git nodejs npm'
    },
    
    staging: {
      user: 'sakura-user',
      host: process.env.SAKURA_STAGING_HOST,
      ref: 'origin/develop',
      repo: 'https://github.com/your-username/rephrase-project.git',
      path: '/home/sakura-user/rephrase-staging',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env staging'
    }
  }
};
