/**
 * SystemManager - システム全体の統合管理
 * 
 * 各種Manager（ZoomControllerManager、ImageAutoHideManager、SubslotToggleManager等）を
 * 統合的に管理し、システム全体の初期化、状態管理、エラーハンドリングを行う
 * 
 * 主要機能:
 * - 各種Managerの初期化と管理
 * - システム全体の状態監視
 * - 統合エラーハンドリング
 * - パフォーマンス監視
 * - デバッグ支援
 * 
 * @version 1.0
 * @date 2025-08-02
 */

class SystemManager {
  constructor() {
    this.managers = new Map();
    this.initializationOrder = [
      'StateManager',
      'ZoomController',
      'ImageAutoHide',
      'SubslotToggle',
      'ControlPanel',
      'VoiceSystem',
      'ExplanationSystem'
    ];
    this.isInitialized = false;
    this.initializationStatus = new Map();
    this.errorHandlers = new Map();
    this.performanceMetrics = new Map();
    
    this.init();
  }

  /**
   * システム初期化
   */
  async init() {
    console.log('🚀 SystemManager初期化開始');
    
    try {
      // 基本設定
      this.setupErrorHandling();
      this.setupPerformanceMonitoring();
      
      // 状態管理システムとの連携
      this.connectToStateManager();
      
      // 各種Managerの初期化
      await this.initializeManagers();
      
      // システム統合検証
      this.verifySystemIntegration();
      
      this.isInitialized = true;
      console.log('🎉 SystemManager初期化完了');
      
      // 初期化完了イベントの発火
      this.dispatchSystemEvent('systemInitialized', {
        timestamp: new Date().toISOString(),
        managers: Array.from(this.managers.keys()),
        performance: this.getPerformanceMetrics()
      });
      
    } catch (error) {
      console.error('❌ SystemManager初期化失敗:', error);
      this.handleInitializationError(error);
    }
  }

  /**
   * 状態管理システムとの連携
   */
  connectToStateManager() {
    if (window.RephraseState) {
      this.stateManager = window.RephraseState;
      console.log('🔗 SystemManager: 状態管理システムと連携');
      
      // SystemManagerの状態を登録
      this.stateManager.updateState('systemManager', {
        isInitialized: false,
        managers: [],
        lastUpdate: new Date().toISOString()
      });
    } else {
      console.warn('⚠️ 状態管理システムが見つかりません - 代替システムを使用');
      this.setupFallbackStateManagement();
    }
  }

  /**
   * 代替状態管理システムのセットアップ
   */
  setupFallbackStateManagement() {
    this.fallbackState = {
      systemManager: {
        isInitialized: false,
        managers: [],
        lastUpdate: new Date().toISOString()
      }
    };
    
    this.stateManager = {
      updateState: (key, value) => {
        this.fallbackState[key] = value;
      },
      getState: (key) => {
        return this.fallbackState[key];
      }
    };
    
    console.log('🔄 代替状態管理システム設定完了');
  }

  /**
   * 各種Managerの初期化
   */
  async initializeManagers() {
    console.log('🔧 各種Manager初期化開始');
    
    for (const managerName of this.initializationOrder) {
      try {
        const startTime = performance.now();
        await this.initializeManager(managerName);
        const endTime = performance.now();
        
        this.performanceMetrics.set(managerName, {
          initTime: endTime - startTime,
          status: 'success',
          timestamp: new Date().toISOString()
        });
        
        console.log(`✅ ${managerName} 初期化完了 (${(endTime - startTime).toFixed(2)}ms)`);
        
      } catch (error) {
        console.error(`❌ ${managerName} 初期化失敗:`, error);
        this.initializationStatus.set(managerName, 'failed');
        this.performanceMetrics.set(managerName, {
          initTime: 0,
          status: 'failed',
          error: error.message,
          timestamp: new Date().toISOString()
        });
      }
    }
  }

  /**
   * 個別Managerの初期化
   */
  async initializeManager(managerName) {
    switch (managerName) {
      case 'StateManager':
        // 状態管理システムは既に連携済み
        this.initializationStatus.set('StateManager', 'success');
        break;
        
      case 'ZoomController':
        if (window.ZoomControllerManager) {
          const zoomManager = window.initZoomController();
          if (zoomManager) {
            this.managers.set('ZoomController', zoomManager);
            this.initializationStatus.set('ZoomController', 'success');
          } else {
            throw new Error('ZoomController初期化に失敗');
          }
        } else {
          throw new Error('ZoomControllerManager が見つかりません');
        }
        break;
        
      case 'ImageAutoHide':
        if (window.ImageAutoHideManager) {
          const imageManager = new window.ImageAutoHideManager();
          this.managers.set('ImageAutoHide', imageManager);
          this.initializationStatus.set('ImageAutoHide', 'success');
        } else {
          console.warn('⚠️ ImageAutoHideManager が見つかりません - スキップ');
          this.initializationStatus.set('ImageAutoHide', 'skipped');
        }
        break;
        
      case 'SubslotToggle':
        if (window.SubslotToggleManager) {
          const subslotManager = new window.SubslotToggleManager();
          this.managers.set('SubslotToggle', subslotManager);
          this.initializationStatus.set('SubslotToggle', 'success');
        } else {
          console.warn('⚠️ SubslotToggleManager が見つかりません - スキップ');
          this.initializationStatus.set('SubslotToggle', 'skipped');
        }
        break;
        
      case 'ControlPanel':
        // 既存のcontrol_panel_manager.jsとの統合
        if (window.initializeControlPanelManager) {
          await window.initializeControlPanelManager();
          this.initializationStatus.set('ControlPanel', 'success');
        } else {
          console.warn('⚠️ ControlPanelManager が見つかりません - スキップ');
          this.initializationStatus.set('ControlPanel', 'skipped');
        }
        break;
        
      case 'VoiceSystem':
        // 既存のvoice_system.jsとの統合
        if (window.voiceManager) {
          this.managers.set('VoiceSystem', window.voiceManager);
          this.initializationStatus.set('VoiceSystem', 'success');
        } else {
          console.warn('⚠️ VoiceSystem が見つかりません - スキップ');
          this.initializationStatus.set('VoiceSystem', 'skipped');
        }
        break;
        
      case 'ExplanationSystem':
        // 既存のexplanation_system.jsとの統合
        if (window.ExplanationSystem) {
          this.managers.set('ExplanationSystem', window.ExplanationSystem);
          this.initializationStatus.set('ExplanationSystem', 'success');
        } else {
          console.warn('⚠️ ExplanationSystem が見つかりません - スキップ');
          this.initializationStatus.set('ExplanationSystem', 'skipped');
        }
        break;
        
      default:
        console.warn(`⚠️ 不明なManager: ${managerName}`);
        this.initializationStatus.set(managerName, 'unknown');
    }
  }

  /**
   * システム統合検証
   */
  verifySystemIntegration() {
    console.log('🔍 システム統合検証開始');
    
    const verificationResults = {
      stateManager: !!this.stateManager,
      managersInitialized: this.managers.size,
      totalManagers: this.initializationOrder.length,
      successfulManagers: Array.from(this.initializationStatus.values()).filter(s => s === 'success').length,
      failedManagers: Array.from(this.initializationStatus.values()).filter(s => s === 'failed').length,
      skippedManagers: Array.from(this.initializationStatus.values()).filter(s => s === 'skipped').length
    };
    
    console.log('📊 統合検証結果:', verificationResults);
    
    // 状態管理システムに結果を保存
    if (this.stateManager) {
      this.stateManager.updateState('systemManager', {
        isInitialized: true,
        managers: Array.from(this.managers.keys()),
        initializationStatus: Object.fromEntries(this.initializationStatus),
        verificationResults,
        lastUpdate: new Date().toISOString()
      });
    }
    
    return verificationResults;
  }

  /**
   * エラーハンドリングの設定
   */
  setupErrorHandling() {
    // グローバルエラーハンドラー
    window.addEventListener('error', (event) => {
      this.handleGlobalError('JavaScript Error', event.error, event);
    });
    
    // Promise拒否ハンドラー
    window.addEventListener('unhandledrejection', (event) => {
      this.handleGlobalError('Unhandled Promise Rejection', event.reason, event);
    });
    
    console.log('🛡️ システムエラーハンドリング設定完了');
  }

  /**
   * パフォーマンス監視の設定
   */
  setupPerformanceMonitoring() {
    // パフォーマンス監視の開始
    this.performanceStartTime = performance.now();
    
    // メモリ使用量監視（可能な場合）
    if ('memory' in performance) {
      this.monitorMemoryUsage();
    }
    
    console.log('📈 パフォーマンス監視設定完了');
  }

  /**
   * メモリ使用量監視
   */
  monitorMemoryUsage() {
    const checkMemory = () => {
      if (performance.memory) {
        const memoryInfo = {
          used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024),
          total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024),
          limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024),
          timestamp: new Date().toISOString()
        };
        
        this.performanceMetrics.set('memory', memoryInfo);
        
        // メモリ使用量が制限の80%を超えた場合の警告
        if (memoryInfo.used / memoryInfo.limit > 0.8) {
          console.warn('⚠️ メモリ使用量が高くなっています:', memoryInfo);
        }
      }
    };
    
    // 30秒ごとにメモリ使用量をチェック
    setInterval(checkMemory, 30000);
    checkMemory(); // 初回実行
  }

  /**
   * グローバルエラーハンドラー
   */
  handleGlobalError(type, error, event) {
    const errorInfo = {
      type,
      message: error?.message || String(error),
      stack: error?.stack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    };
    
    console.error(`🚨 ${type}:`, errorInfo);
    
    // 状態管理システムにエラーを記録
    if (this.stateManager) {
      const currentErrors = this.stateManager.getState('systemErrors') || [];
      currentErrors.push(errorInfo);
      
      // 最新の50件のエラーのみ保持
      if (currentErrors.length > 50) {
        currentErrors.splice(0, currentErrors.length - 50);
      }
      
      this.stateManager.updateState('systemErrors', currentErrors);
    }
    
    // 開発環境でのみエラー詳細を表示
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      this.displayErrorInDevelopment(errorInfo);
    }
  }

  /**
   * 初期化エラーハンドラー
   */
  handleInitializationError(error) {
    console.error('🚨 システム初期化エラー:', error);
    
    // 部分的初期化の試行
    this.attemptPartialInitialization();
  }

  /**
   * 部分的初期化の試行
   */
  attemptPartialInitialization() {
    console.log('🔄 部分的初期化を試行');
    
    // 最低限必要な機能のみ初期化
    const essentialManagers = ['StateManager', 'ZoomController'];
    
    essentialManagers.forEach(async (managerName) => {
      if (this.initializationStatus.get(managerName) !== 'success') {
        try {
          await this.initializeManager(managerName);
          console.log(`✅ ${managerName} 部分初期化成功`);
        } catch (error) {
          console.error(`❌ ${managerName} 部分初期化失敗:`, error);
        }
      }
    });
  }

  /**
   * 開発環境でのエラー表示
   */
  displayErrorInDevelopment(errorInfo) {
    // エラー情報をコンソールに詳細表示
    console.group(`🚨 ${errorInfo.type} Details`);
    console.error('Message:', errorInfo.message);
    console.error('Stack:', errorInfo.stack);
    console.error('Timestamp:', errorInfo.timestamp);
    console.error('URL:', errorInfo.url);
    console.groupEnd();
  }

  /**
   * システムイベントの発火
   */
  dispatchSystemEvent(eventType, data) {
    const event = new CustomEvent(`rephrase:${eventType}`, {
      detail: data
    });
    window.dispatchEvent(event);
    
    console.log(`📡 システムイベント発火: ${eventType}`, data);
  }

  /**
   * パフォーマンスメトリクスの取得
   */
  getPerformanceMetrics() {
    const currentTime = performance.now();
    const totalInitTime = currentTime - this.performanceStartTime;
    
    return {
      totalInitializationTime: totalInitTime,
      managerMetrics: Object.fromEntries(this.performanceMetrics),
      memoryUsage: this.performanceMetrics.get('memory'),
      timestamp: new Date().toISOString()
    };
  }

  /**
   * システム状態の取得
   */
  getSystemStatus() {
    return {
      isInitialized: this.isInitialized,
      managers: Array.from(this.managers.keys()),
      initializationStatus: Object.fromEntries(this.initializationStatus),
      performanceMetrics: this.getPerformanceMetrics(),
      errors: this.stateManager?.getState('systemErrors') || [],
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 特定Managerの取得
   */
  getManager(name) {
    return this.managers.get(name);
  }

  /**
   * Managerの追加
   */
  addManager(name, manager) {
    this.managers.set(name, manager);
    this.initializationStatus.set(name, 'success');
    
    console.log(`➕ Manager追加: ${name}`);
    
    // 状態管理システムに反映
    if (this.stateManager) {
      const currentState = this.stateManager.getState('systemManager') || {};
      currentState.managers = Array.from(this.managers.keys());
      currentState.lastUpdate = new Date().toISOString();
      this.stateManager.updateState('systemManager', currentState);
    }
  }

  /**
   * Managerの削除
   */
  removeManager(name) {
    const manager = this.managers.get(name);
    
    // Managerに破棄メソッドがある場合は呼び出し
    if (manager && typeof manager.destroy === 'function') {
      try {
        manager.destroy();
      } catch (error) {
        console.error(`⚠️ ${name} 破棄時エラー:`, error);
      }
    }
    
    this.managers.delete(name);
    this.initializationStatus.delete(name);
    
    console.log(`➖ Manager削除: ${name}`);
  }

  /**
   * システム全体のリセット
   */
  async resetSystem() {
    console.log('🔄 システム全体リセット開始');
    
    // 全Managerの破棄
    for (const [name, manager] of this.managers) {
      this.removeManager(name);
    }
    
    // 初期化状態のリセット
    this.managers.clear();
    this.initializationStatus.clear();
    this.performanceMetrics.clear();
    this.isInitialized = false;
    
    // 再初期化
    await this.init();
    
    console.log('🔄 システム全体リセット完了');
  }

  /**
   * デバッグ情報の出力
   */
  debugInfo() {
    console.group('🔍 SystemManager デバッグ情報');
    console.log('システム状態:', this.getSystemStatus());
    console.log('Manager一覧:', Array.from(this.managers.keys()));
    console.log('初期化状態:', Object.fromEntries(this.initializationStatus));
    console.log('パフォーマンス:', this.getPerformanceMetrics());
    console.groupEnd();
  }

  /**
   * システムヘルスチェック
   */
  healthCheck() {
    const status = this.getSystemStatus();
    const health = {
      overall: 'healthy',
      issues: [],
      recommendations: []
    };
    
    // 初期化状態チェック
    if (!status.isInitialized) {
      health.overall = 'critical';
      health.issues.push('システムが初期化されていません');
      health.recommendations.push('システムの再初期化を実行してください');
    }
    
    // 失敗したManagerのチェック
    const failedManagers = Object.entries(status.initializationStatus)
      .filter(([_, status]) => status === 'failed')
      .map(([name, _]) => name);
      
    if (failedManagers.length > 0) {
      health.overall = health.overall === 'critical' ? 'critical' : 'warning';
      health.issues.push(`以下のManagerが失敗: ${failedManagers.join(', ')}`);
      health.recommendations.push('失敗したManagerの再初期化を試行してください');
    }
    
    // メモリ使用量チェック
    const memoryInfo = status.performanceMetrics.memoryUsage;
    if (memoryInfo && memoryInfo.used / memoryInfo.limit > 0.8) {
      health.overall = health.overall === 'critical' ? 'critical' : 'warning';
      health.issues.push(`メモリ使用量が高い: ${memoryInfo.used}MB / ${memoryInfo.limit}MB`);
      health.recommendations.push('不要なデータの削除やページの再読み込みを検討してください');
    }
    
    console.log('🏥 システムヘルスチェック結果:', health);
    return health;
  }

  /**
   * SystemManagerの破棄
   */
  destroy() {
    console.log('🗑️ SystemManager破棄開始');
    
    // 全Managerの破棄
    for (const [name, manager] of this.managers) {
      this.removeManager(name);
    }
    
    // イベントリスナーの削除
    window.removeEventListener('error', this.handleGlobalError);
    window.removeEventListener('unhandledrejection', this.handleGlobalError);
    
    console.log('🗑️ SystemManager破棄完了');
  }
}

// グローバルSystemManagerインスタンス
let globalSystemManager = null;

// 初期化関数
function initSystemManager() {
  if (!globalSystemManager) {
    globalSystemManager = new SystemManager();
    
    // グローバルAPIとして公開
    window.SystemManager = globalSystemManager;
    window.getSystemStatus = () => globalSystemManager.getSystemStatus();
    window.getManager = (name) => globalSystemManager.getManager(name);
    window.resetSystem = () => globalSystemManager.resetSystem();
    window.debugSystemManager = () => globalSystemManager.debugInfo();
    window.systemHealthCheck = () => globalSystemManager.healthCheck();
  }
  return globalSystemManager;
}

// DOMContentLoaded時の自動初期化（他のシステムより後に実行）
document.addEventListener('DOMContentLoaded', () => {
  // 少し遅延させて他のシステムの初期化を待つ
  setTimeout(() => {
    initSystemManager();
  }, 1000);
});

// モジュールとしてエクスポート
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SystemManager, initSystemManager };
}

// ES6モジュールとしてもエクスポート
if (typeof window !== 'undefined') {
  window.SystemManager = SystemManager;
  window.initSystemManager = initSystemManager;
}

console.log('🚀 SystemManager モジュール読み込み完了');
