const fs = require('fs').promises;
const path = require('path');
const winston = require('winston');

// ロガー設定
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/backup.log' }),
    new winston.transports.Console()
  ]
});

class BackupManager {
  constructor() {
    this.backupPath = process.env.BACKUP_PATH || './backups';
    this.retentionDays = parseInt(process.env.BACKUP_RETENTION_DAYS) || 30;
    this.enabled = process.env.BACKUP_ENABLED === 'true';
  }

  async init() {
    try {
      await fs.mkdir(this.backupPath, { recursive: true });
      await fs.mkdir(path.join(this.backupPath, 'database'), { recursive: true });
      await fs.mkdir(path.join(this.backupPath, 'files'), { recursive: true });
      logger.info('Backup directories initialized');
    } catch (error) {
      logger.error('Failed to initialize backup directories:', error);
      throw error;
    }
  }

  async createBackup() {
    if (!this.enabled) {
      logger.info('Backup is disabled, skipping');
      return;
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupId = `backup_${timestamp}`;

    try {
      logger.info(`Starting backup: ${backupId}`);

      // データベースバックアップ（開発時はファイルベース）
      await this.backupDatabase(backupId);

      // ユーザーファイルバックアップ
      await this.backupUserFiles(backupId);

      // 設定ファイルバックアップ
      await this.backupConfig(backupId);

      // バックアップメタデータ
      await this.createBackupMetadata(backupId);

      // 古いバックアップ削除
      await this.cleanOldBackups();

      logger.info(`Backup completed successfully: ${backupId}`);
      return backupId;

    } catch (error) {
      logger.error(`Backup failed: ${backupId}`, error);
      throw error;
    }
  }

  async backupDatabase(backupId) {
    try {
      const dbBackupPath = path.join(this.backupPath, 'database', `${backupId}.json`);
      
      // 開発環境: メモリ内データをJSONとして保存
      // 本番環境: MySQLダンプコマンドを実行
      if (process.env.NODE_ENV === 'production') {
        // MySQLダンプ実行（さくらインターネット本番環境用）
        const { exec } = require('child_process');
        const dumpCommand = `mysqldump -h ${process.env.DB_HOST} -u ${process.env.DB_USER} -p${process.env.DB_PASSWORD} ${process.env.DB_NAME} > ${dbBackupPath.replace('.json', '.sql')}`;
        
        await new Promise((resolve, reject) => {
          exec(dumpCommand, (error, stdout, stderr) => {
            if (error) reject(error);
            else resolve(stdout);
          });
        });
      } else {
        // 開発環境: メモリデータバックアップ
        const backupData = {
          timestamp: new Date().toISOString(),
          version: '1.0',
          users: Array.from(global.users || []),
          sessions: Array.from(global.sessions || []),
          progress: Array.from(global.progressData || [])
        };

        await fs.writeFile(dbBackupPath, JSON.stringify(backupData, null, 2));
      }

      logger.info(`Database backup completed: ${backupId}`);
    } catch (error) {
      logger.error('Database backup failed:', error);
      throw error;
    }
  }

  async backupUserFiles(backupId) {
    try {
      const filesBackupPath = path.join(this.backupPath, 'files', backupId);
      await fs.mkdir(filesBackupPath, { recursive: true });

      // ユーザーアップロードファイル
      const uploadsPath = './uploads';
      try {
        await this.copyDirectory(uploadsPath, path.join(filesBackupPath, 'uploads'));
      } catch (error) {
        logger.warn('No uploads directory found, skipping user files backup');
      }

      // ログファイル
      const logsPath = './logs';
      try {
        await this.copyDirectory(logsPath, path.join(filesBackupPath, 'logs'));
      } catch (error) {
        logger.warn('No logs directory found, skipping logs backup');
      }

      logger.info(`User files backup completed: ${backupId}`);
    } catch (error) {
      logger.error('User files backup failed:', error);
      throw error;
    }
  }

  async backupConfig(backupId) {
    try {
      const configBackupPath = path.join(this.backupPath, 'files', backupId, 'config');
      await fs.mkdir(configBackupPath, { recursive: true });

      // 重要な設定ファイル
      const configFiles = [
        'package.json',
        'ecosystem.config.js',
        '.env.example'
      ];

      for (const file of configFiles) {
        try {
          const sourcePath = path.join('.', file);
          const destPath = path.join(configBackupPath, file);
          await fs.copyFile(sourcePath, destPath);
        } catch (error) {
          logger.warn(`Config file not found: ${file}`);
        }
      }

      logger.info(`Config backup completed: ${backupId}`);
    } catch (error) {
      logger.error('Config backup failed:', error);
      throw error;
    }
  }

  async createBackupMetadata(backupId) {
    try {
      const metadata = {
        id: backupId,
        timestamp: new Date().toISOString(),
        version: process.env.npm_package_version || '1.0.0',
        environment: process.env.NODE_ENV || 'development',
        size: await this.calculateBackupSize(backupId),
        files: await this.listBackupFiles(backupId)
      };

      const metadataPath = path.join(this.backupPath, `${backupId}.metadata.json`);
      await fs.writeFile(metadataPath, JSON.stringify(metadata, null, 2));

      logger.info(`Backup metadata created: ${backupId}`);
    } catch (error) {
      logger.error('Backup metadata creation failed:', error);
      throw error;
    }
  }

  async copyDirectory(source, destination) {
    await fs.mkdir(destination, { recursive: true });
    const entries = await fs.readdir(source, { withFileTypes: true });

    for (const entry of entries) {
      const srcPath = path.join(source, entry.name);
      const destPath = path.join(destination, entry.name);

      if (entry.isDirectory()) {
        await this.copyDirectory(srcPath, destPath);
      } else {
        await fs.copyFile(srcPath, destPath);
      }
    }
  }

  async calculateBackupSize(backupId) {
    // バックアップサイズ計算実装
    return 0;
  }

  async listBackupFiles(backupId) {
    // バックアップファイル一覧作成実装
    return [];
  }

  async cleanOldBackups() {
    try {
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - this.retentionDays);

      const files = await fs.readdir(this.backupPath);
      const metadataFiles = files.filter(file => file.endsWith('.metadata.json'));

      for (const metadataFile of metadataFiles) {
        const metadataPath = path.join(this.backupPath, metadataFile);
        const metadata = JSON.parse(await fs.readFile(metadataPath, 'utf8'));
        
        const backupDate = new Date(metadata.timestamp);
        if (backupDate < cutoffDate) {
          // 古いバックアップを削除
          await this.deleteBackup(metadata.id);
          logger.info(`Deleted old backup: ${metadata.id}`);
        }
      }
    } catch (error) {
      logger.error('Failed to clean old backups:', error);
    }
  }

  async deleteBackup(backupId) {
    try {
      // メタデータファイル削除
      const metadataPath = path.join(this.backupPath, `${backupId}.metadata.json`);
      await fs.unlink(metadataPath);

      // データベースバックアップ削除
      const dbBackupPath = path.join(this.backupPath, 'database', `${backupId}.json`);
      await fs.unlink(dbBackupPath).catch(() => {}); // ファイルが存在しない場合は無視

      // ファイルバックアップ削除
      const filesBackupPath = path.join(this.backupPath, 'files', backupId);
      await fs.rmdir(filesBackupPath, { recursive: true }).catch(() => {});

    } catch (error) {
      logger.error(`Failed to delete backup: ${backupId}`, error);
    }
  }

  async restoreBackup(backupId) {
    // バックアップ復元機能（将来実装）
    logger.info(`Restore functionality will be implemented for: ${backupId}`);
  }

  async listBackups() {
    try {
      const files = await fs.readdir(this.backupPath);
      const metadataFiles = files.filter(file => file.endsWith('.metadata.json'));
      
      const backups = [];
      for (const metadataFile of metadataFiles) {
        const metadataPath = path.join(this.backupPath, metadataFile);
        const metadata = JSON.parse(await fs.readFile(metadataPath, 'utf8'));
        backups.push(metadata);
      }

      return backups.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    } catch (error) {
      logger.error('Failed to list backups:', error);
      return [];
    }
  }
}

// スタンドアロン実行時
if (require.main === module) {
  (async () => {
    const backupManager = new BackupManager();
    await backupManager.init();
    await backupManager.createBackup();
  })().catch(error => {
    logger.error('Backup script failed:', error);
    process.exit(1);
  });
}

module.exports = BackupManager;
