// 🚀 Rephrase Training UI - Optimized Bundle
// Performance optimized JavaScript bundle
// Version: 2.0
// Date: 2025-07-21

console.log('🚀 Rephraseトレーニング最適化バンドル読み込み開始...');

// =============================================================================
// 📦 CORE MODULES - Essential functionality first
// =============================================================================

// 🔒 Security Module (Critical - Load First)
window.securityModule = {
    escapeHtml: function(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    sanitizeInput: function(input) {
        if (typeof input !== 'string') return '';
        return input.replace(/<script[^>]*>.*?<\/script>/gi, '')
                   .replace(/javascript:/gi, '')
                   .replace(/on\w+\s*=/gi, '');
    },
    
    validateDataStructure: function(data) {
        return data && typeof data === 'object' && !Array.isArray(data);
    }
};

// 🛡️ Rate Limiter (Essential for stability)
window.rateLimiter = {
    limits: new Map(),
    
    isAllowed: function(action, maxRequests = 60, windowMs = 60000) {
        const now = Date.now();
        const key = action;
        
        if (!this.limits.has(key)) {
            this.limits.set(key, { count: 1, resetTime: now + windowMs });
            return true;
        }
        
        const limit = this.limits.get(key);
        if (now > limit.resetTime) {
            limit.count = 1;
            limit.resetTime = now + windowMs;
            return true;
        }
        
        if (limit.count >= maxRequests) {
            return false;
        }
        
        limit.count++;
        return true;
    }
};

// ⚠️ Error Handler (Critical for user experience)
window.errorHandler = {
    errorLog: [],
    
    handleError: function(error, context = '') {
        const errorData = {
            timestamp: new Date().toISOString(),
            message: error.message || String(error),
            context: context,
            stack: error.stack || '',
            userAgent: navigator.userAgent
        };
        
        this.errorLog.push(errorData);
        console.error('🚨 Error captured:', errorData);
        
        // User-friendly display
        this.showUserFriendlyError(error.code || 'system.unknown', errorData.message);
    },
    
    showUserFriendlyError: function(errorCode, details) {
        const userMessages = {
            'auth.invalid_credentials': 'ログイン情報が正しくありません',
            'system.network_error': 'ネットワーク接続を確認してください',
            'system.unknown': 'システムエラーが発生しました',
            'data.load_failed': 'データの読み込みに失敗しました'
        };
        
        const message = userMessages[errorCode] || 'エラーが発生しました';
        this.showModal('エラーが発生しました', message);
    },
    
    showModal: function(title, message) {
        // Remove existing modal
        const existing = document.getElementById('errorModal');
        if (existing) existing.remove();
        
        const modal = document.createElement('div');
        modal.id = 'errorModal';
        modal.innerHTML = `
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 10000; display: flex; align-items: center; justify-content: center;">
                <div style="background: white; padding: 20px; border-radius: 8px; max-width: 400px; margin: 20px;">
                    <h3 style="margin: 0 0 10px 0; color: #d32f2f;">⚠️ ${title}</h3>
                    <p style="margin: 0 0 20px 0;">${message}</p>
                    <button onclick="document.getElementById('errorModal').remove()" style="background: #1976d2; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">OK</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },
    
    getErrorLog: function(limit = 100) {
        return this.errorLog.slice(-limit);
    }
};

// =============================================================================
// 🎮 UI CONTROLS - Core interaction functionality
// =============================================================================

// 🔄 Toggle Controller (Subslot visibility)
window.toggleController = {
    init: function() {
        console.log('🔄 Toggle Controller initialized');
    },
    
    toggleSubslot: function(slotId) {
        try {
            const element = document.getElementById(slotId);
            if (!element) return;
            
            const isVisible = element.style.display !== 'none';
            element.style.display = isVisible ? 'none' : 'block';
            
            // Update button text
            const button = document.querySelector(`[onclick*="${slotId}"]`);
            if (button) {
                button.textContent = isVisible ? '展開' : '折り畳み';
            }
        } catch (error) {
            window.errorHandler.handleError(error, 'toggleSubslot');
        }
    }
};

// 🖼️ Image System (Optimized for performance)
window.imageSystem = {
    cache: new Map(),
    
    init: function() {
        console.log('🖼️ Image System initialized');
        this.preloadCriticalImages();
    },
    
    preloadCriticalImages: function() {
        // Implement intelligent preloading based on usage patterns
        const criticalImages = [
            'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><rect width="1" height="1" fill="%23f0f0f0"/></svg>'
        ];
        
        criticalImages.forEach(src => this.preloadImage(src));
    },
    
    preloadImage: function(src) {
        if (this.cache.has(src)) return Promise.resolve();
        
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.cache.set(src, img);
                resolve(img);
            };
            img.onerror = reject;
            img.src = src;
        });
    },
    
    loadImage: function(element, src) {
        if (!src || !element) return;
        
        // Use cached image if available
        if (this.cache.has(src)) {
            element.src = src;
            return;
        }
        
        // Show loading placeholder
        element.style.opacity = '0.5';
        
        this.preloadImage(src).then(() => {
            element.src = src;
            element.style.opacity = '1';
        }).catch(error => {
            console.warn('Image load failed:', src, error);
            element.style.display = 'none';
        });
    }
};

// =============================================================================
// 🎯 PERFORMANCE OPTIMIZATIONS
// =============================================================================

// ⚡ Debounce utility for performance
window.debounce = function(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func.apply(this, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(this, args);
    };
};

// 🚀 Lazy loading for non-critical components
window.lazyLoader = {
    loaded: new Set(),
    
    loadModule: function(moduleName, loader) {
        if (this.loaded.has(moduleName)) return Promise.resolve();
        
        return new Promise((resolve, reject) => {
            try {
                const result = loader();
                this.loaded.add(moduleName);
                resolve(result);
            } catch (error) {
                reject(error);
            }
        });
    }
};

// =============================================================================
// 🎵 AUDIO SYSTEM (Lazy loaded)
// =============================================================================

window.audioSystem = {
    initialized: false,
    audioCache: new Map(),
    
    init: function() {
        if (this.initialized) return;
        
        console.log('🎵 Audio System initialized (lazy)');
        this.initialized = true;
    },
    
    loadAudio: function(src) {
        if (this.audioCache.has(src)) {
            return Promise.resolve(this.audioCache.get(src));
        }
        
        return new Promise((resolve, reject) => {
            const audio = new Audio();
            audio.preload = 'metadata';
            audio.oncanplaythrough = () => {
                this.audioCache.set(src, audio);
                resolve(audio);
            };
            audio.onerror = reject;
            audio.src = src;
        });
    },
    
    playAudio: function(src) {
        this.loadAudio(src).then(audio => {
            audio.currentTime = 0;
            audio.play().catch(error => {
                console.warn('Audio play failed:', error);
            });
        });
    }
};

// =============================================================================
// 🎲 RANDOMIZER SYSTEM (Core functionality)
// =============================================================================

window.randomizerSystem = {
    init: function() {
        console.log('🎲 Randomizer System initialized');
    },
    
    randomizeSlot: function(slotId) {
        try {
            if (!window.rateLimiter.isAllowed('randomize', 30, 60000)) {
                window.errorHandler.showUserFriendlyError('system.rate_limit', 'ランダム化の頻度が高すぎます');
                return;
            }
            
            // Implementation placeholder - will be populated with actual randomization logic
            console.log('🎲 Randomizing slot:', slotId);
            
        } catch (error) {
            window.errorHandler.handleError(error, 'randomizeSlot');
        }
    }
};

// =============================================================================
// 🚀 INITIALIZATION
// =============================================================================

// Initialize core modules immediately
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 DOM Ready - Initializing optimized bundle...');
    
    try {
        // Initialize critical modules first
        window.toggleController.init();
        window.imageSystem.init();
        window.randomizerSystem.init();
        
        console.log('✅ Optimized bundle initialization complete');
        
        // Set up global error handling
        window.addEventListener('error', function(event) {
            window.errorHandler.handleError(event.error, 'Global error');
        });
        
        window.addEventListener('unhandledrejection', function(event) {
            window.errorHandler.handleError(event.reason, 'Unhandled promise rejection');
        });
        
    } catch (error) {
        console.error('❌ Bundle initialization failed:', error);
        window.errorHandler.handleError(error, 'Bundle initialization');
    }
});

console.log('🚀 Rephraseトレーニング最適化バンドル読み込み完了');
