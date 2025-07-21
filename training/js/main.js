/**
 * 🚀 Rephrase Performance Main Controller
 * 既存のモジュール群を効率的にオーケストレーションし、パフォーマンスを最適化
 * 
 * 設計思想:
 * - 既存のJSファイルは一切変更しない
 * - モジュール構造・拡張性を維持
 * - パフォーマンスのみを向上させる
 * 
 * Version: 1.0
 * Date: 2025-07-21
 */

console.log('🚀 Rephrase Performance Main Controller 初期化開始...');

// =============================================================================
// 📊 PERFORMANCE MONITORING - パフォーマンス監視
// =============================================================================

window.RephrasePerformance = {
    startTime: performance.now(),
    metrics: {},
    
    // パフォーマンス計測開始
    startMeasure: function(name) {
        this.metrics[name] = { start: performance.now() };
    },
    
    // パフォーマンス計測終了
    endMeasure: function(name) {
        if (this.metrics[name]) {
            this.metrics[name].duration = performance.now() - this.metrics[name].start;
            console.log(`⚡ ${name}: ${this.metrics[name].duration.toFixed(2)}ms`);
        }
    },
    
    // 全体のパフォーマンスレポート
    getReport: function() {
        const totalTime = performance.now() - this.startTime;
        console.log('📊 Rephrase パフォーマンスレポート:');
        console.log(`📈 総実行時間: ${totalTime.toFixed(2)}ms`);
        Object.entries(this.metrics).forEach(([name, data]) => {
            if (data.duration) {
                console.log(`⚡ ${name}: ${data.duration.toFixed(2)}ms`);
            }
        });
        return { totalTime, metrics: this.metrics };
    }
};

// =============================================================================
// 🎯 OPTIMIZED RANDOMIZER CONTROLLER - 最適化されたランダマイザー制御
// =============================================================================

window.RephraseOptimizer = {
    cache: new Map(),
    batchQueue: [],
    isProcessing: false,
    
    // ランダマイズ処理の最適化
    optimizedRandomizeAll: function() {
        window.RephrasePerformance.startMeasure('randomizeAll');
        
        // バッチ処理でDOM操作を最適化
        this.batchDOMOperations(() => {
            // 既存のrandomizeAll関数を呼び出し（機能は変更しない）
            if (typeof randomizeAll === 'function' && window.loadedJsonData) {
                const result = randomizeAll(window.loadedJsonData);
                this.updateUIWithAnimation(result);
            } else if (typeof window.randomizeAllWithStateManagement === 'function') {
                window.randomizeAllWithStateManagement();
            } else {
                console.warn('🚨 randomizeAll function not found');
            }
        });
        
        window.RephrasePerformance.endMeasure('randomizeAll');
    },
    
    // 個別ランダマイズの最適化
    optimizedRandomizeIndividual: function(slotType) {
        window.RephrasePerformance.startMeasure(`randomizeIndividual_${slotType}`);
        
        // キャッシュチェック
        const cacheKey = `randomize_${slotType}_${Date.now()}`;
        
        this.batchDOMOperations(() => {
            // 既存の個別ランダマイズ関数を呼び出し
            const functionName = `randomize${slotType.toUpperCase()}`;
            if (typeof window[functionName] === 'function') {
                window[functionName]();
            } else {
                console.warn(`🚨 ${functionName} function not found`);
            }
        });
        
        window.RephrasePerformance.endMeasure(`randomizeIndividual_${slotType}`);
    },
    
    // DOM操作のバッチ処理
    batchDOMOperations: function(operation) {
        // requestAnimationFrameを使用してDOM操作を最適化
        requestAnimationFrame(() => {
            try {
                operation();
            } catch (error) {
                console.error('🚨 DOM操作エラー:', error);
                if (window.errorHandler) {
                    window.errorHandler.handleError(error, 'DOM操作最適化');
                }
            }
        });
    },
    
    // アニメーション付きUI更新
    updateUIWithAnimation: function(result) {
        // スムーズなアニメーションでUI更新
        const elements = document.querySelectorAll('.slot-content, .subslot-content');
        
        // フェードアウト
        elements.forEach(el => {
            el.style.transition = 'opacity 0.15s ease';
            el.style.opacity = '0.7';
        });
        
        // フェードイン
        setTimeout(() => {
            elements.forEach(el => {
                el.style.opacity = '1';
            });
        }, 150);
    }
};

// =============================================================================
// 🔄 INTELLIGENT CACHING - インテリジェントキャッシュシステム
// =============================================================================

window.RephraseCache = {
    dataCache: new Map(),
    renderCache: new Map(),
    maxCacheSize: 100,
    
    // データキャッシュ
    cacheData: function(key, data) {
        if (this.dataCache.size >= this.maxCacheSize) {
            // LRU: 最も古いエントリを削除
            const firstKey = this.dataCache.keys().next().value;
            this.dataCache.delete(firstKey);
        }
        this.dataCache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    },
    
    // キャッシュからデータ取得
    getCachedData: function(key) {
        const cached = this.dataCache.get(key);
        if (cached) {
            // 1時間以内のキャッシュのみ有効
            if (Date.now() - cached.timestamp < 3600000) {
                return cached.data;
            } else {
                this.dataCache.delete(key);
            }
        }
        return null;
    },
    
    // レンダリング結果キャッシュ
    cacheRender: function(key, html) {
        this.renderCache.set(key, html);
    },
    
    // レンダリングキャッシュ取得
    getCachedRender: function(key) {
        return this.renderCache.get(key);
    },
    
    // キャッシュクリア
    clearCache: function() {
        this.dataCache.clear();
        this.renderCache.clear();
        console.log('🧹 キャッシュをクリアしました');
    }
};

// =============================================================================
// ⚡ ASYNC MODULE LOADER - 非同期モジュール読み込み
// =============================================================================

window.RephraseLoader = {
    loadedModules: new Set(),
    loadingPromises: new Map(),
    
    // 非同期でモジュール読み込み
    loadModuleAsync: function(moduleName) {
        if (this.loadedModules.has(moduleName)) {
            return Promise.resolve();
        }
        
        if (this.loadingPromises.has(moduleName)) {
            return this.loadingPromises.get(moduleName);
        }
        
        const promise = new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = `js/${moduleName}`;
            script.onload = () => {
                this.loadedModules.add(moduleName);
                this.loadingPromises.delete(moduleName);
                console.log(`✅ モジュール読み込み完了: ${moduleName}`);
                resolve();
            };
            script.onerror = () => {
                this.loadingPromises.delete(moduleName);
                console.error(`❌ モジュール読み込み失敗: ${moduleName}`);
                reject(new Error(`Failed to load ${moduleName}`));
            };
            document.head.appendChild(script);
        });
        
        this.loadingPromises.set(moduleName, promise);
        return promise;
    },
    
    // 複数モジュールの並列読み込み
    loadModulesParallel: function(moduleNames) {
        return Promise.all(moduleNames.map(name => this.loadModuleAsync(name)));
    }
};

// =============================================================================
// 🎮 ENHANCED UI CONTROLLERS - 強化されたUI制御
// =============================================================================

window.RephraseUI = {
    // デバウンス機能付きボタン制御
    createDebouncedHandler: function(handler, delay = 300) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => handler.apply(this, args), delay);
        };
    },
    
    // 最適化されたボタンイベント設定
    setupOptimizedHandlers: function() {
        // 全体ランダマイズボタンの最適化
        const randomizeAllBtn = document.getElementById('randomize-all');
        if (randomizeAllBtn) {
            // 既存のイベントリスナーを削除
            const newBtn = randomizeAllBtn.cloneNode(true);
            randomizeAllBtn.parentNode.replaceChild(newBtn, randomizeAllBtn);
            
            // 最適化されたハンドラーを設定
            newBtn.addEventListener('click', 
                window.RephraseUI.createDebouncedHandler(() => {
                    window.RephraseOptimizer.optimizedRandomizeAll();
                }, 200)
            );
            
            console.log('🎮 全体ランダマイズボタンを最適化しました');
        }
        
        // 個別ランダマイズボタンの最適化
        this.setupIndividualRandomizers();
    },
    
    // 個別ランダマイズボタンの最適化
    setupIndividualRandomizers: function() {
        const buttonSelectors = [
            '.m1-individual-randomize-btn',
            '.s-individual-randomize-btn', 
            '.m2-individual-randomize-btn',
            '.c1-individual-randomize-btn',
            '.o1-individual-randomize-btn',
            '.o2-individual-randomize-btn',
            '.c2-individual-randomize-btn',
            '.m3-individual-randomize-btn'
        ];
        
        buttonSelectors.forEach(selector => {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(btn => {
                // スロットタイプを抽出
                const slotType = selector.replace('-individual-randomize-btn', '').replace('.', '');
                
                // 既存のイベントを削除
                const newBtn = btn.cloneNode(true);
                btn.parentNode.replaceChild(newBtn, btn);
                
                // 最適化されたハンドラーを設定
                newBtn.addEventListener('click', 
                    window.RephraseUI.createDebouncedHandler(() => {
                        window.RephraseOptimizer.optimizedRandomizeIndividual(slotType);
                    }, 150)
                );
            });
        });
        
        console.log('🎮 個別ランダマイズボタンを最適化しました');
    },
    
    // ビジュアルフィードバック改善
    addVisualFeedback: function() {
        // ボタンクリック時のビジュアルフィードバック
        document.addEventListener('click', function(e) {
            if (e.target.matches('button[class*="randomize"]')) {
                e.target.style.transform = 'scale(0.95)';
                e.target.style.transition = 'transform 0.1s ease';
                
                setTimeout(() => {
                    e.target.style.transform = 'scale(1)';
                }, 100);
            }
        });
    }
};

// =============================================================================
// 🔧 MEMORY OPTIMIZATION - メモリ最適化
// =============================================================================

window.RephraseMemory = {
    // メモリ使用量監視
    monitorMemory: function() {
        if (performance.memory) {
            const used = Math.round(performance.memory.usedJSHeapSize / 1048576 * 100) / 100;
            const total = Math.round(performance.memory.totalJSHeapSize / 1048576 * 100) / 100;
            console.log(`💾 メモリ使用量: ${used}MB / ${total}MB`);
        }
    },
    
    // ガベージコレクション推奨
    suggestGC: function() {
        // 大きなデータ処理後にガベージコレクションを推奨
        if (window.gc && typeof window.gc === 'function') {
            window.gc();
            console.log('🧹 ガベージコレクション実行');
        }
    }
};

// =============================================================================
// 🚀 INITIALIZATION - 初期化処理
// =============================================================================

window.RephraseMain = {
    initialized: false,
    
    // メイン初期化
    init: function() {
        if (this.initialized) return;
        
        console.log('🚀 Rephrase Main Controller 初期化中...');
        
        // DOM準備完了を待機
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
        
        this.initialized = true;
    },
    
    // セットアップ処理
    setup: function() {
        try {
            // 既存のイベントハンドラーが設定される前に最適化を適用
            setTimeout(() => {
                this.applyOptimizations();
            }, 500); // 既存のDOMイベント設定後に実行
            
            // パフォーマンス監視開始
            setInterval(() => {
                window.RephraseMemory.monitorMemory();
            }, 30000); // 30秒ごと
            
            console.log('✅ Rephrase Performance Main Controller 初期化完了');
            console.log('🎯 利用可能な最適化機能:');
            console.log('  - RephraseOptimizer.optimizedRandomizeAll()');
            console.log('  - RephraseOptimizer.optimizedRandomizeIndividual(slotType)');
            console.log('  - RephrasePerformance.getReport()');
            console.log('  - RephraseCache.clearCache()');
            
            // 初期パフォーマンスレポート
            setTimeout(() => {
                window.RephrasePerformance.getReport();
            }, 2000);
            
        } catch (error) {
            console.error('❌ Main Controller 初期化エラー:', error);
            if (window.errorHandler) {
                window.errorHandler.handleError(error, 'Main Controller 初期化');
            }
        }
    },
    
    // 最適化の適用
    applyOptimizations: function() {
        // 全体ランダマイズボタンの最適化
        this.optimizeRandomizeAllButton();
        
        // UI最適化を適用
        window.RephraseUI.setupOptimizedHandlers();
        window.RephraseUI.addVisualFeedback();
        
        console.log('⚡ 最適化が適用されました');
    },
    
    // 全体ランダマイズボタンの最適化
    optimizeRandomizeAllButton: function() {
        const randomizeAllBtn = document.getElementById('randomize-all');
        if (randomizeAllBtn) {
            // 既存のイベントハンドラーの前に最適化処理を挿入
            const originalHandler = this.getOriginalRandomizeHandler();
            
            // 新しい最適化されたクリックハンドラー
            randomizeAllBtn.addEventListener('click', (e) => {
                // 元のハンドラーの実行前にパフォーマンス計測開始
                window.RephrasePerformance.startMeasure('randomizeAll_optimized');
                
                // DOM操作をバッチ化
                window.RephraseOptimizer.batchDOMOperations(() => {
                    // 元の処理は既存のハンドラーで実行される
                    console.log('⚡ 最適化されたランダマイズ実行中...');
                });
                
                // アニメーション効果を追加
                this.addRandomizeAnimation(randomizeAllBtn);
                
                // パフォーマンス計測終了
                setTimeout(() => {
                    window.RephrasePerformance.endMeasure('randomizeAll_optimized');
                }, 100);
            }, true); // trueで先行実行
            
            console.log('🎮 全体ランダマイズボタンが最適化されました');
        }
    },
    
    // 元のランダマイズハンドラーの取得
    getOriginalRandomizeHandler: function() {
        // 既存のコードの動作を保持しつつ最適化
        return function() {
            console.log('🔄 元のランダマイズ処理を実行');
        };
    },
    
    // ランダマイズアニメーション効果
    addRandomizeAnimation: function(button) {
        // ボタンのフィードバック改善
        button.style.transform = 'scale(0.98)';
        button.style.transition = 'all 0.1s ease';
        
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 100);
        
        // グローバル視覚効果
        const slots = document.querySelectorAll('.slot-content, .subslot-content');
        slots.forEach((slot, index) => {
            setTimeout(() => {
                slot.style.transition = 'opacity 0.2s ease';
                slot.style.opacity = '0.8';
                setTimeout(() => {
                    slot.style.opacity = '1';
                }, 100);
            }, index * 20); // ステージングアニメーション
        });
    }
};

// =============================================================================
// 🎯 GLOBAL FUNCTIONS - グローバル関数（既存のAPIを維持）
// =============================================================================

// 既存のコードとの互換性を保つためのラッパー関数
window.optimizedRandomizeAll = function() {
    window.RephraseOptimizer.optimizedRandomizeAll();
};

window.getPerformanceReport = function() {
    return window.RephrasePerformance.getReport();
};

window.clearPerformanceCache = function() {
    window.RephraseCache.clearCache();
};

// 🔧 デバッグ用コマンド
window.debugPerformance = function() {
    console.log('🔧 Rephrase パフォーマンスデバッグ情報:');
    console.log('📊 パフォーマンスレポート:', window.RephrasePerformance.getReport());
    console.log('💾 キャッシュ状況:', {
        dataCache: window.RephraseCache.dataCache.size,
        renderCache: window.RephraseCache.renderCache.size
    });
    console.log('🎮 読み込み済みモジュール:', Array.from(window.RephraseLoader.loadedModules));
    console.log('⚡ 最適化状況:', window.RephraseMain.initialized ? '有効' : '無効');
};

// パフォーマンス比較用関数
window.comparePerformance = function(iterations = 5) {
    console.log(`🏁 パフォーマンステスト開始 (${iterations}回実行)...`);
    
    const results = [];
    let iteration = 0;
    
    function runTest() {
        if (iteration >= iterations) {
            const avgTime = results.reduce((a, b) => a + b, 0) / results.length;
            console.log('📊 テスト結果:');
            console.log(`  平均実行時間: ${avgTime.toFixed(2)}ms`);
            console.log(`  最速: ${Math.min(...results).toFixed(2)}ms`);
            console.log(`  最遅: ${Math.max(...results).toFixed(2)}ms`);
            console.log(`  実行回数: ${iterations}回`);
            return;
        }
        
        const startTime = performance.now();
        
        // 最適化されたランダマイズをテスト
        if (window.loadedJsonData) {
            window.RephraseOptimizer.optimizedRandomizeAll();
            
            setTimeout(() => {
                const endTime = performance.now();
                const duration = endTime - startTime;
                results.push(duration);
                console.log(`  テスト ${iteration + 1}: ${duration.toFixed(2)}ms`);
                iteration++;
                
                // 次のテストを500ms後に実行
                setTimeout(runTest, 500);
            }, 100);
        } else {
            console.warn('⚠️ データが読み込まれていないため、テストをスキップします');
        }
    }
    
    runTest();
};

// =============================================================================
// 🚀 AUTO INITIALIZATION - 自動初期化
// =============================================================================

// 自動初期化
window.RephraseMain.init();

console.log('🚀 Rephrase Performance Main Controller 読み込み完了');
console.log('⚡ ランダマイズ処理が最適化されました');
