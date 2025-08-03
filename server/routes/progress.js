const express = require('express');
const router = express.Router();
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

// プログレス更新専用のレート制限（1万ユーザー対応）
const progressLimiter = rateLimit({
  windowMs: 60 * 1000, // 1分
  max: 20, // 1IPあたり1分間に20回の更新（リアルタイム学習対応）
  message: { error: 'Progress update rate limit exceeded' },
  standardHeaders: true,
  legacyHeaders: false
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

// 全ルートに認証と基本レート制限適用
router.use(authenticateUser);

// 学習プログレス取得
router.get('/', async (req, res) => {
  try {
    const userId = req.user.id;
    
    // 開発環境用プログレスデータストレージ
    const progressData = global.progressData || new Map();
    const userProgress = progressData.get(userId) || {
      totalSessions: 0,
      currentLevel: 1,
      experience: 0,
      streakDays: 0,
      weaknesses: [],
      strengths: [],
      recentSessions: [],
      voiceAnalysis: {
        pronunciationScore: 0,
        fluencyScore: 0,
        accuracyScore: 0,
        completenessScore: 0
      },
      grammarProgress: {
        basicTenses: 0,
        presentTense: 0,
        pastTense: 0,
        futureTense: 0,
        conditionals: 0,
        passiveVoice: 0
      },
      vocabularyProgress: {
        businessTerms: 0,
        dailyConversation: 0,
        academicWords: 0,
        idioms: 0
      }
    };
    
    res.json({
      success: true,
      progress: userProgress
    });
    
  } catch (error) {
    console.error('Progress fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch progress data' });
  }
});

// 学習セッション開始
router.post('/session/start', 
  progressLimiter,
  [
    body('lessonType').isIn(['grammar', 'vocabulary', 'pronunciation', 'conversation', 'listening']),
    body('difficulty').isIn(['beginner', 'intermediate', 'advanced']),
    body('estimatedDuration').optional().isInt({ min: 1, max: 180 })
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
      const { lessonType, difficulty, estimatedDuration = 30 } = req.body;
      
      // セッション作成
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const session = {
        id: sessionId,
        userId: userId,
        lessonType: lessonType,
        difficulty: difficulty,
        estimatedDuration: estimatedDuration,
        startTime: new Date().toISOString(),
        status: 'active',
        currentProgress: 0,
        exercises: [],
        voiceRecordings: [],
        scores: {}
      };
      
      // アクティブセッション保存
      const activeSessions = global.activeSessions || new Map();
      activeSessions.set(sessionId, session);
      global.activeSessions = activeSessions;
      
      res.json({
        success: true,
        message: 'Learning session started',
        session: session
      });
      
    } catch (error) {
      console.error('Session start error:', error);
      res.status(500).json({ error: 'Failed to start learning session' });
    }
  }
);

// 学習セッション更新
router.put('/session/:sessionId', 
  progressLimiter,
  [
    body('progress').optional().isFloat({ min: 0, max: 100 }),
    body('currentExercise').optional().isString(),
    body('answers').optional().isArray(),
    body('voiceData').optional().isObject()
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
      const { sessionId } = req.params;
      const updates = req.body;
      
      const activeSessions = global.activeSessions || new Map();
      const session = activeSessions.get(sessionId);
      
      if (!session || session.userId !== userId) {
        return res.status(404).json({ error: 'Session not found or access denied' });
      }
      
      // セッション更新
      Object.assign(session, updates, {
        lastUpdated: new Date().toISOString()
      });
      
      // 音声データがある場合の処理
      if (updates.voiceData) {
        session.voiceRecordings.push({
          timestamp: new Date().toISOString(),
          data: updates.voiceData,
          analysis: await analyzeVoiceData(updates.voiceData)
        });
      }
      
      activeSessions.set(sessionId, session);
      global.activeSessions = activeSessions;
      
      res.json({
        success: true,
        message: 'Session updated successfully',
        session: session
      });
      
    } catch (error) {
      console.error('Session update error:', error);
      res.status(500).json({ error: 'Failed to update session' });
    }
  }
);

// 学習セッション完了
router.post('/session/:sessionId/complete', 
  progressLimiter,
  [
    body('finalScore').optional().isFloat({ min: 0, max: 100 }),
    body('completedExercises').optional().isInt({ min: 0 }),
    body('timeSpent').optional().isInt({ min: 0 }),
    body('feedback').optional().isString()
  ],
  async (req, res) => {
    try {
      const userId = req.user.id;
      const { sessionId } = req.params;
      const { finalScore, completedExercises, timeSpent, feedback } = req.body;
      
      const activeSessions = global.activeSessions || new Map();
      const session = activeSessions.get(sessionId);
      
      if (!session || session.userId !== userId) {
        return res.status(404).json({ error: 'Session not found or access denied' });
      }
      
      // セッション完了処理
      session.status = 'completed';
      session.endTime = new Date().toISOString();
      session.finalScore = finalScore;
      session.completedExercises = completedExercises;
      session.actualDuration = timeSpent;
      session.feedback = feedback;
      
      // 学習進捗更新
      await updateUserProgress(userId, session);
      
      // 完了セッションを履歴に移動
      const completedSessions = global.completedSessions || new Map();
      const userCompletedSessions = completedSessions.get(userId) || [];
      userCompletedSessions.push(session);
      completedSessions.set(userId, userCompletedSessions);
      global.completedSessions = completedSessions;
      
      // アクティブセッションから削除
      activeSessions.delete(sessionId);
      global.activeSessions = activeSessions;
      
      // 経験値とレベル計算
      const experienceGained = calculateExperienceGain(session);
      const newLevel = await updateUserLevel(userId, experienceGained);
      
      res.json({
        success: true,
        message: 'Session completed successfully',
        results: {
          sessionId: sessionId,
          finalScore: finalScore,
          experienceGained: experienceGained,
          newLevel: newLevel,
          achievements: await checkAchievements(userId, session)
        }
      });
      
    } catch (error) {
      console.error('Session completion error:', error);
      res.status(500).json({ error: 'Failed to complete session' });
    }
  }
);

// 音声分析データ送信
router.post('/voice-analysis', 
  progressLimiter,
  [
    body('audioData').isString(),
    body('expectedText').isString(),
    body('sessionId').optional().isString()
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
      const { audioData, expectedText, sessionId } = req.body;
      
      // 音声分析実行（実際の実装では音声認識APIを使用）
      const analysisResult = await performVoiceAnalysis(audioData, expectedText);
      
      // 分析結果保存
      const voiceAnalyses = global.voiceAnalyses || new Map();
      const userAnalyses = voiceAnalyses.get(userId) || [];
      
      const analysisRecord = {
        id: `analysis_${Date.now()}`,
        timestamp: new Date().toISOString(),
        sessionId: sessionId,
        expectedText: expectedText,
        recognizedText: analysisResult.recognizedText,
        scores: analysisResult.scores,
        feedback: analysisResult.feedback
      };
      
      userAnalyses.push(analysisRecord);
      voiceAnalyses.set(userId, userAnalyses);
      global.voiceAnalyses = voiceAnalyses;
      
      res.json({
        success: true,
        analysis: analysisRecord
      });
      
    } catch (error) {
      console.error('Voice analysis error:', error);
      res.status(500).json({ error: 'Failed to analyze voice data' });
    }
  }
);

// 学習統計取得
router.get('/stats', async (req, res) => {
  try {
    const userId = req.user.id;
    const { period = '7d' } = req.query; // 7d, 30d, 90d, 1y
    
    const stats = await generateLearningStats(userId, period);
    
    res.json({
      success: true,
      stats: stats
    });
    
  } catch (error) {
    console.error('Stats generation error:', error);
    res.status(500).json({ error: 'Failed to generate statistics' });
  }
});

// 弱点分析
router.get('/weaknesses', async (req, res) => {
  try {
    const userId = req.user.id;
    
    const weaknesses = await analyzeUserWeaknesses(userId);
    
    res.json({
      success: true,
      weaknesses: weaknesses
    });
    
  } catch (error) {
    console.error('Weakness analysis error:', error);
    res.status(500).json({ error: 'Failed to analyze weaknesses' });
  }
});

// 推奨学習コンテンツ
router.get('/recommendations', async (req, res) => {
  try {
    const userId = req.user.id;
    
    const recommendations = await generateRecommendations(userId);
    
    res.json({
      success: true,
      recommendations: recommendations
    });
    
  } catch (error) {
    console.error('Recommendations error:', error);
    res.status(500).json({ error: 'Failed to generate recommendations' });
  }
});

// ヘルパー関数

async function analyzeVoiceData(voiceData) {
  // 音声データ分析の簡易実装（実際はWav2Vec、Whisper等を使用）
  return {
    pronunciationScore: Math.random() * 100,
    fluencyScore: Math.random() * 100,
    accuracyScore: Math.random() * 100,
    detectedIssues: ['r_sound', 'th_sound'],
    suggestions: ['Focus on tongue position for R sounds']
  };
}

async function updateUserProgress(userId, session) {
  const progressData = global.progressData || new Map();
  const userProgress = progressData.get(userId) || {
    totalSessions: 0,
    currentLevel: 1,
    experience: 0,
    streakDays: 0
  };
  
  userProgress.totalSessions++;
  userProgress.lastSessionDate = new Date().toISOString();
  
  // セッションタイプ別進捗更新
  if (session.lessonType === 'grammar') {
    userProgress.grammarProgress = userProgress.grammarProgress || {};
    // 文法進捗更新ロジック
  }
  
  progressData.set(userId, userProgress);
  global.progressData = progressData;
}

function calculateExperienceGain(session) {
  const baseExp = 100;
  const scoreMultiplier = (session.finalScore || 50) / 100;
  const timeMultiplier = Math.min(session.actualDuration / 30, 2);
  
  return Math.floor(baseExp * scoreMultiplier * timeMultiplier);
}

async function updateUserLevel(userId, experienceGained) {
  const progressData = global.progressData || new Map();
  const userProgress = progressData.get(userId) || { currentLevel: 1, experience: 0 };
  
  userProgress.experience += experienceGained;
  
  // レベルアップ計算
  const expNeeded = userProgress.currentLevel * 1000;
  if (userProgress.experience >= expNeeded) {
    userProgress.currentLevel++;
    userProgress.experience -= expNeeded;
  }
  
  progressData.set(userId, userProgress);
  global.progressData = progressData;
  
  return userProgress.currentLevel;
}

async function checkAchievements(userId, session) {
  // 実績チェックロジック
  return [];
}

async function performVoiceAnalysis(audioData, expectedText) {
  // 音声認識・分析の簡易実装
  return {
    recognizedText: expectedText, // 実際の実装では音声認識結果
    scores: {
      pronunciation: Math.random() * 100,
      fluency: Math.random() * 100,
      accuracy: Math.random() * 100
    },
    feedback: 'Good pronunciation overall'
  };
}

async function generateLearningStats(userId, period) {
  // 学習統計生成
  return {
    sessionsCompleted: 25,
    totalStudyTime: 1250,
    averageScore: 78.5,
    improvementRate: 15.2,
    streakDays: 7
  };
}

async function analyzeUserWeaknesses(userId) {
  // 弱点分析
  return [
    {
      area: 'pronunciation',
      specificIssues: ['r_sound', 'th_sound'],
      severity: 'medium',
      improvement: -5.2
    }
  ];
}

async function generateRecommendations(userId) {
  // 学習推奨コンテンツ生成
  return [
    {
      type: 'exercise',
      title: 'R Sound Practice',
      description: 'Focus on R pronunciation with tongue exercises',
      priority: 'high'
    }
  ];
}

module.exports = router;
