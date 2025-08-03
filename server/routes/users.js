const express = require('express');
const router = express.Router();
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

// レート制限設定（1万ユーザー対応）
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分
  max: 100, // 1IPあたり15分間に100リクエスト
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false
});

// プログレス更新の厳しいレート制限
const progressLimiter = rateLimit({
  windowMs: 60 * 1000, // 1分
  max: 10, // 1IPあたり1分間に10回の更新
  message: { error: 'Progress update rate limit exceeded' }
});

// ユーザー認証チェック
const authenticateUser = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication token required' });
  }

  try {
    const jwt = require('jsonwebtoken');
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid authentication token' });
  }
};

// 全ルートにレート制限適用
router.use(apiLimiter);

// ユーザープロファイル取得
router.get('/profile', authenticateUser, async (req, res) => {
  try {
    const userId = req.user.id;
    
    // 開発環境用の簡易データストレージ
    const users = global.users || new Map();
    const user = users.get(userId);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // パスワードを除外してレスポンス
    const { password, ...userProfile } = user;
    
    res.json({
      success: true,
      user: userProfile
    });
    
  } catch (error) {
    console.error('Profile fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch user profile' });
  }
});

// ユーザープロファイル更新
router.put('/profile', 
  authenticateUser,
  [
    body('displayName').optional().trim().isLength({ min: 1, max: 50 }),
    body('email').optional().isEmail(),
    body('nativeLanguage').optional().isIn(['japanese', 'korean', 'chinese', 'spanish', 'french']),
    body('learningGoal').optional().isIn(['business', 'travel', 'academic', 'conversation', 'exam'])
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation failed',
          details: errors.array()
        });
      }

      const userId = req.user.id;
      const updates = req.body;
      
      // 開発環境用データストレージ
      const users = global.users || new Map();
      const user = users.get(userId);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      // プロファイル更新
      Object.assign(user, updates, { updatedAt: new Date().toISOString() });
      users.set(userId, user);
      global.users = users;

      const { password, ...userProfile } = user;
      
      res.json({
        success: true,
        message: 'Profile updated successfully',
        user: userProfile
      });
      
    } catch (error) {
      console.error('Profile update error:', error);
      res.status(500).json({ error: 'Failed to update profile' });
    }
  }
);

// 学習統計取得
router.get('/stats', authenticateUser, async (req, res) => {
  try {
    const userId = req.user.id;
    
    // 開発環境用プログレスデータ
    const progressData = global.progressData || new Map();
    const userProgress = progressData.get(userId) || [];
    
    // 統計計算
    const stats = calculateLearningStats(userProgress);
    
    res.json({
      success: true,
      stats: stats
    });
    
  } catch (error) {
    console.error('Stats fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch learning statistics' });
  }
});

// 学習セッション一覧
router.get('/sessions', authenticateUser, async (req, res) => {
  try {
    const userId = req.user.id;
    const { page = 1, limit = 20, startDate, endDate } = req.query;
    
    // 開発環境用セッションデータ
    const sessions = global.sessions || new Map();
    let userSessions = sessions.get(userId) || [];
    
    // 日付フィルタリング
    if (startDate) {
      userSessions = userSessions.filter(session => 
        new Date(session.timestamp) >= new Date(startDate)
      );
    }
    
    if (endDate) {
      userSessions = userSessions.filter(session => 
        new Date(session.timestamp) <= new Date(endDate)
      );
    }
    
    // ページネーション
    const total = userSessions.length;
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + parseInt(limit);
    const paginatedSessions = userSessions.slice(startIndex, endIndex);
    
    res.json({
      success: true,
      sessions: paginatedSessions,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total: total,
        pages: Math.ceil(total / limit)
      }
    });
    
  } catch (error) {
    console.error('Sessions fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch sessions' });
  }
});

// 学習セッション詳細
router.get('/sessions/:sessionId', authenticateUser, async (req, res) => {
  try {
    const userId = req.user.id;
    const { sessionId } = req.params;
    
    const sessions = global.sessions || new Map();
    const userSessions = sessions.get(userId) || [];
    
    const session = userSessions.find(s => s.id === sessionId);
    
    if (!session) {
      return res.status(404).json({ error: 'Session not found' });
    }
    
    res.json({
      success: true,
      session: session
    });
    
  } catch (error) {
    console.error('Session fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch session details' });
  }
});

// ユーザー削除（GDPR対応）
router.delete('/account', authenticateUser, async (req, res) => {
  try {
    const userId = req.user.id;
    
    // 全データ削除
    const users = global.users || new Map();
    const sessions = global.sessions || new Map();
    const progressData = global.progressData || new Map();
    
    users.delete(userId);
    sessions.delete(userId);
    progressData.delete(userId);
    
    global.users = users;
    global.sessions = sessions;
    global.progressData = progressData;
    
    res.json({
      success: true,
      message: 'Account and all associated data deleted successfully'
    });
    
  } catch (error) {
    console.error('Account deletion error:', error);
    res.status(500).json({ error: 'Failed to delete account' });
  }
});

// アカウント設定取得
router.get('/settings', authenticateUser, async (req, res) => {
  try {
    const userId = req.user.id;
    
    // デフォルト設定
    const defaultSettings = {
      voiceSpeed: 1.0,
      audioQuality: 'high',
      autoSave: true,
      darkMode: false,
      notifications: {
        email: true,
        push: false,
        dailyReminder: true
      },
      privacy: {
        profilePublic: false,
        progressVisible: false,
        allowAnalytics: true
      }
    };
    
    // ユーザー設定（開発環境用簡易ストレージ）
    const userSettings = global.userSettings || new Map();
    const settings = userSettings.get(userId) || defaultSettings;
    
    res.json({
      success: true,
      settings: settings
    });
    
  } catch (error) {
    console.error('Settings fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch settings' });
  }
});

// アカウント設定更新
router.put('/settings', 
  authenticateUser,
  [
    body('voiceSpeed').optional().isFloat({ min: 0.5, max: 2.0 }),
    body('audioQuality').optional().isIn(['low', 'medium', 'high']),
    body('autoSave').optional().isBoolean(),
    body('darkMode').optional().isBoolean()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation failed',
          details: errors.array()
        });
      }

      const userId = req.user.id;
      const updates = req.body;
      
      const userSettings = global.userSettings || new Map();
      const currentSettings = userSettings.get(userId) || {};
      
      // 設定更新（ディープマージ）
      const updatedSettings = deepMerge(currentSettings, updates);
      userSettings.set(userId, updatedSettings);
      global.userSettings = userSettings;
      
      res.json({
        success: true,
        message: 'Settings updated successfully',
        settings: updatedSettings
      });
      
    } catch (error) {
      console.error('Settings update error:', error);
      res.status(500).json({ error: 'Failed to update settings' });
    }
  }
);

// ヘルパー関数
function calculateLearningStats(progressData) {
  const stats = {
    totalSessions: progressData.length,
    totalStudyTime: 0,
    averageScore: 0,
    streakDays: 0,
    wordsLearned: 0,
    grammarPointsMastered: 0,
    weakAreas: [],
    recentActivity: []
  };
  
  if (progressData.length === 0) {
    return stats;
  }
  
  // 学習時間計算
  stats.totalStudyTime = progressData.reduce((total, session) => {
    return total + (session.duration || 0);
  }, 0);
  
  // 平均スコア計算
  const scores = progressData.filter(session => session.score).map(session => session.score);
  if (scores.length > 0) {
    stats.averageScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
  }
  
  // 連続学習日数計算
  stats.streakDays = calculateStreakDays(progressData);
  
  // 学習単語数
  stats.wordsLearned = new Set(
    progressData.flatMap(session => session.wordsStudied || [])
  ).size;
  
  return stats;
}

function calculateStreakDays(progressData) {
  // 連続学習日数計算の簡易実装
  const dates = progressData.map(session => 
    new Date(session.timestamp).toDateString()
  );
  
  const uniqueDates = [...new Set(dates)].sort();
  let streak = 0;
  let currentDate = new Date();
  
  for (let i = uniqueDates.length - 1; i >= 0; i--) {
    const sessionDate = new Date(uniqueDates[i]);
    const daysDiff = Math.floor((currentDate - sessionDate) / (1000 * 60 * 60 * 24));
    
    if (daysDiff === streak) {
      streak++;
      currentDate = sessionDate;
    } else {
      break;
    }
  }
  
  return streak;
}

function deepMerge(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(result[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  
  return result;
}

module.exports = router;
