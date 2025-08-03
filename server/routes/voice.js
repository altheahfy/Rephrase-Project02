const express = require('express');
const router = express.Router();
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

// 音声API専用のレート制限（高負荷対応）
const voiceLimiter = rateLimit({
  windowMs: 60 * 1000, // 1分
  max: 30, // 1IPあたり1分間に30回（リアルタイム音声認識対応）
  message: { error: 'Voice API rate limit exceeded' },
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

// 全ルートに認証とレート制限適用
router.use(authenticateUser);
router.use(voiceLimiter);

// 音声認識エンドポイント
router.post('/recognize', 
  [
    body('audioData').isString().isLength({ min: 100 }),
    body('language').optional().isIn(['en-US', 'en-GB', 'en-AU']),
    body('context').optional().isString(),
    body('expectedText').optional().isString()
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
      const { audioData, language = 'en-US', context, expectedText } = req.body;
      
      // 音声認識実行
      const recognitionResult = await performSpeechRecognition(audioData, language, context);
      
      // 発音評価（期待テキストがある場合）
      let pronunciationScore = null;
      if (expectedText) {
        pronunciationScore = await evaluatePronunciation(recognitionResult.text, expectedText, audioData);
      }
      
      // 結果保存
      const recognitionRecord = {
        id: `recognition_${Date.now()}`,
        userId: userId,
        timestamp: new Date().toISOString(),
        recognizedText: recognitionResult.text,
        confidence: recognitionResult.confidence,
        language: language,
        context: context,
        expectedText: expectedText,
        pronunciationScore: pronunciationScore,
        audioLength: calculateAudioLength(audioData)
      };
      
      // 認識履歴保存
      const voiceRecognitions = global.voiceRecognitions || new Map();
      const userRecognitions = voiceRecognitions.get(userId) || [];
      userRecognitions.push(recognitionRecord);
      
      // 最新100件のみ保持
      if (userRecognitions.length > 100) {
        userRecognitions.splice(0, userRecognitions.length - 100);
      }
      
      voiceRecognitions.set(userId, userRecognitions);
      global.voiceRecognitions = voiceRecognitions;
      
      res.json({
        success: true,
        recognition: {
          text: recognitionResult.text,
          confidence: recognitionResult.confidence,
          pronunciationScore: pronunciationScore,
          suggestions: recognitionResult.suggestions || []
        }
      });
      
    } catch (error) {
      console.error('Speech recognition error:', error);
      res.status(500).json({ error: 'Failed to process speech recognition' });
    }
  }
);

// 発音評価エンドポイント
router.post('/pronunciation-score', 
  [
    body('audioData').isString().isLength({ min: 100 }),
    body('targetText').isString().isLength({ min: 1, max: 500 }),
    body('language').optional().isIn(['en-US', 'en-GB', 'en-AU']),
    body('focusPhonemes').optional().isArray()
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
      const { audioData, targetText, language = 'en-US', focusPhonemes } = req.body;
      
      // 詳細発音分析
      const analysisResult = await performDetailedPronunciationAnalysis(
        audioData, 
        targetText, 
        language,
        focusPhonemes
      );
      
      // 分析結果保存
      const analysisRecord = {
        id: `pronunciation_${Date.now()}`,
        userId: userId,
        timestamp: new Date().toISOString(),
        targetText: targetText,
        language: language,
        overallScore: analysisResult.overallScore,
        pronunciationScore: analysisResult.pronunciationScore,
        fluencyScore: analysisResult.fluencyScore,
        accuracyScore: analysisResult.accuracyScore,
        completenessScore: analysisResult.completenessScore,
        phonemeAnalysis: analysisResult.phonemeAnalysis,
        suggestions: analysisResult.suggestions,
        detectedIssues: analysisResult.detectedIssues
      };
      
      // 発音分析履歴保存
      const pronunciationAnalyses = global.pronunciationAnalyses || new Map();
      const userAnalyses = pronunciationAnalyses.get(userId) || [];
      userAnalyses.push(analysisRecord);
      
      // 最新50件のみ保持
      if (userAnalyses.length > 50) {
        userAnalyses.splice(0, userAnalyses.length - 50);
      }
      
      pronunciationAnalyses.set(userId, userAnalyses);
      global.pronunciationAnalyses = pronunciationAnalyses;
      
      res.json({
        success: true,
        analysis: analysisResult
      });
      
    } catch (error) {
      console.error('Pronunciation analysis error:', error);
      res.status(500).json({ error: 'Failed to analyze pronunciation' });
    }
  }
);

// 音声合成エンドポイント（TTS）
router.post('/synthesize', 
  [
    body('text').isString().isLength({ min: 1, max: 1000 }),
    body('voice').optional().isIn(['male', 'female', 'child']),
    body('speed').optional().isFloat({ min: 0.5, max: 2.0 }),
    body('language').optional().isIn(['en-US', 'en-GB', 'en-AU'])
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

      const { text, voice = 'female', speed = 1.0, language = 'en-US' } = req.body;
      
      // 音声合成実行
      const synthesizedAudio = await performTextToSpeech(text, voice, speed, language);
      
      res.json({
        success: true,
        audio: {
          data: synthesizedAudio.audioData,
          format: synthesizedAudio.format,
          duration: synthesizedAudio.duration,
          sampleRate: synthesizedAudio.sampleRate
        }
      });
      
    } catch (error) {
      console.error('Text-to-speech error:', error);
      res.status(500).json({ error: 'Failed to synthesize speech' });
    }
  }
);

// 音声特徴分析
router.post('/voice-features', 
  [
    body('audioData').isString().isLength({ min: 100 }),
    body('analysisType').optional().isIn(['pitch', 'formants', 'rhythm', 'all'])
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

      const { audioData, analysisType = 'all' } = req.body;
      
      // 音声特徴分析
      const features = await extractVoiceFeatures(audioData, analysisType);
      
      res.json({
        success: true,
        features: features
      });
      
    } catch (error) {
      console.error('Voice feature analysis error:', error);
      res.status(500).json({ error: 'Failed to analyze voice features' });
    }
  }
);

// 音声履歴取得
router.get('/history', async (req, res) => {
  try {
    const userId = req.user.id;
    const { type = 'all', limit = 20, offset = 0 } = req.query;
    
    let history = [];
    
    if (type === 'recognition' || type === 'all') {
      const recognitions = global.voiceRecognitions?.get(userId) || [];
      history = history.concat(recognitions.map(r => ({ ...r, type: 'recognition' })));
    }
    
    if (type === 'pronunciation' || type === 'all') {
      const pronunciations = global.pronunciationAnalyses?.get(userId) || [];
      history = history.concat(pronunciations.map(p => ({ ...p, type: 'pronunciation' })));
    }
    
    // 時間順ソート
    history.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    // ページネーション
    const paginatedHistory = history.slice(offset, offset + parseInt(limit));
    
    res.json({
      success: true,
      history: paginatedHistory,
      total: history.length,
      hasMore: offset + parseInt(limit) < history.length
    });
    
  } catch (error) {
    console.error('History fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch voice history' });
  }
});

// 音声統計取得
router.get('/stats', async (req, res) => {
  try {
    const userId = req.user.id;
    const { period = '7d' } = req.query;
    
    const stats = await generateVoiceStats(userId, period);
    
    res.json({
      success: true,
      stats: stats
    });
    
  } catch (error) {
    console.error('Voice stats error:', error);
    res.status(500).json({ error: 'Failed to generate voice statistics' });
  }
});

// 発音改善提案
router.get('/improvement-tips', async (req, res) => {
  try {
    const userId = req.user.id;
    
    const tips = await generateImprovementTips(userId);
    
    res.json({
      success: true,
      tips: tips
    });
    
  } catch (error) {
    console.error('Improvement tips error:', error);
    res.status(500).json({ error: 'Failed to generate improvement tips' });
  }
});

// ヘルパー関数

async function performSpeechRecognition(audioData, language, context) {
  // 実際の実装では Google Speech-to-Text、AWS Transcribe、Azure Speech Services 等を使用
  // ここでは簡易的なモック実装
  
  const mockTexts = [
    "Hello, how are you today?",
    "I would like to practice English pronunciation.",
    "The weather is beautiful today.",
    "Can you help me with my homework?",
    "I'm learning English through this application."
  ];
  
  const recognizedText = mockTexts[Math.floor(Math.random() * mockTexts.length)];
  const confidence = 0.85 + Math.random() * 0.14; // 85-99%の信頼度
  
  return {
    text: recognizedText,
    confidence: Math.round(confidence * 100) / 100,
    suggestions: [
      "Try speaking more clearly",
      "Slow down slightly for better recognition"
    ]
  };
}

async function evaluatePronunciation(recognizedText, expectedText, audioData) {
  // 発音評価アルゴリズム（実際はPhoneme-based analysis）
  const similarity = calculateTextSimilarity(recognizedText, expectedText);
  const audioQuality = analyzeAudioQuality(audioData);
  
  // 総合スコア計算
  const pronunciationScore = (similarity * 0.7 + audioQuality * 0.3) * 100;
  
  return Math.round(pronunciationScore);
}

async function performDetailedPronunciationAnalysis(audioData, targetText, language, focusPhonemes) {
  // 詳細発音分析（実際は音素レベル分析）
  const baseScore = 70 + Math.random() * 25; // 70-95の範囲
  
  return {
    overallScore: Math.round(baseScore),
    pronunciationScore: Math.round(baseScore + Math.random() * 10 - 5),
    fluencyScore: Math.round(baseScore + Math.random() * 10 - 5),
    accuracyScore: Math.round(baseScore + Math.random() * 10 - 5),
    completenessScore: Math.round(baseScore + Math.random() * 10 - 5),
    phonemeAnalysis: [
      { phoneme: '/θ/', score: 65, issue: 'tongue position' },
      { phoneme: '/r/', score: 80, issue: 'slight improvement needed' },
      { phoneme: '/l/', score: 95, issue: 'excellent' }
    ],
    suggestions: [
      "Practice tongue position for 'th' sounds",
      "Work on R pronunciation with tongue exercises",
      "Overall pronunciation is improving well"
    ],
    detectedIssues: ['th_sound', 'r_pronunciation']
  };
}

async function performTextToSpeech(text, voice, speed, language) {
  // TTS実装（実際は Google TTS、AWS Polly、Azure TTS 等を使用）
  // ここでは簡易的なモック
  
  return {
    audioData: `mock_audio_data_${Date.now()}`, // Base64エンコードされた音声データ
    format: 'mp3',
    duration: text.length * 100, // 文字数に基づく概算時間（ms）
    sampleRate: 22050
  };
}

async function extractVoiceFeatures(audioData, analysisType) {
  // 音声特徴抽出（実際はLibrosa、PRAAT等を使用）
  const features = {};
  
  if (analysisType === 'pitch' || analysisType === 'all') {
    features.pitch = {
      fundamental: 150 + Math.random() * 100, // Hz
      range: 50 + Math.random() * 50,
      stability: 0.7 + Math.random() * 0.3
    };
  }
  
  if (analysisType === 'formants' || analysisType === 'all') {
    features.formants = {
      f1: 500 + Math.random() * 300,
      f2: 1500 + Math.random() * 500,
      f3: 2500 + Math.random() * 500
    };
  }
  
  if (analysisType === 'rhythm' || analysisType === 'all') {
    features.rhythm = {
      tempo: 120 + Math.random() * 60, // BPM
      regularity: 0.6 + Math.random() * 0.4,
      pauses: Math.floor(Math.random() * 5)
    };
  }
  
  return features;
}

async function generateVoiceStats(userId, period) {
  // 音声統計生成
  const recognitions = global.voiceRecognitions?.get(userId) || [];
  const pronunciations = global.pronunciationAnalyses?.get(userId) || [];
  
  return {
    totalRecognitions: recognitions.length,
    totalPronunciationAnalyses: pronunciations.length,
    averageConfidence: 87.5,
    averagePronunciationScore: 78.2,
    improvementTrend: '+12.5%',
    mostPracticedSounds: ['th', 'r', 'l'],
    weakestSounds: ['th', 'v'],
    practiceTimeMinutes: 145
  };
}

async function generateImprovementTips(userId) {
  // 発音改善提案生成
  const pronunciations = global.pronunciationAnalyses?.get(userId) || [];
  
  return [
    {
      category: 'pronunciation',
      priority: 'high',
      title: 'TH Sound Practice',
      description: 'Focus on tongue placement between teeth',
      exercises: [
        'Repeat "think, thank, thought" slowly',
        'Practice tongue twisters with TH sounds'
      ]
    },
    {
      category: 'fluency',
      priority: 'medium',
      title: 'Speech Rhythm',
      description: 'Work on natural speech rhythm and pausing',
      exercises: [
        'Read aloud with emphasis on natural pauses',
        'Practice with metronome for consistent timing'
      ]
    }
  ];
}

function calculateTextSimilarity(text1, text2) {
  // 簡易的な文字列類似度計算
  const words1 = text1.toLowerCase().split(' ');
  const words2 = text2.toLowerCase().split(' ');
  
  const commonWords = words1.filter(word => words2.includes(word));
  const similarity = commonWords.length / Math.max(words1.length, words2.length);
  
  return similarity;
}

function analyzeAudioQuality(audioData) {
  // 音質分析の簡易実装
  return 0.8 + Math.random() * 0.2; // 80-100%の品質
}

function calculateAudioLength(audioData) {
  // 音声長計算の簡易実装
  return Math.floor(audioData.length / 1000); // 秒単位の概算
}

module.exports = router;
