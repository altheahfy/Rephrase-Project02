const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');
const winston = require('winston');

const router = express.Router();

// ロガー
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'logs/auth.log' })
  ]
});

// 認証専用レート制限（より厳しく）
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分
  max: 5, // 最大5回の認証試行
  message: 'Too many authentication attempts, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true
});

// 一時的なユーザーストレージ（開発用）
// 本番ではデータベースに置き換え
const users = new Map();
const sessions = new Map();

// バリデーションルール
const registerValidation = [
  body('username').isLength({ min: 3, max: 30 }).matches(/^[a-zA-Z0-9_]+$/),
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
  body('confirmPassword').custom((value, { req }) => {
    if (value !== req.body.password) {
      throw new Error('Password confirmation does not match password');
    }
    return true;
  })
];

const loginValidation = [
  body('username').trim().isLength({ min: 1 }),
  body('password').isLength({ min: 1 })
];

// JWT トークン生成
function generateTokens(userId) {
  const accessToken = jwt.sign(
    { userId, type: 'access' },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRE || '1h' }
  );

  const refreshToken = jwt.sign(
    { userId, type: 'refresh' },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_REFRESH_EXPIRE || '7d' }
  );

  return { accessToken, refreshToken };
}

// JWT トークン検証ミドルウェア
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
    if (err) {
      logger.warn(`Token verification failed: ${err.message}`);
      return res.status(403).json({ error: 'Invalid or expired token' });
    }

    if (decoded.type !== 'access') {
      return res.status(403).json({ error: 'Invalid token type' });
    }

    req.userId = decoded.userId;
    next();
  });
}

// ユーザー登録
router.post('/register', authLimiter, registerValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { username, email, password } = req.body;

    // ユーザー存在チェック
    if (users.has(username)) {
      return res.status(409).json({ error: 'Username already exists' });
    }

    // メール重複チェック
    for (const user of users.values()) {
      if (user.email === email) {
        return res.status(409).json({ error: 'Email already exists' });
      }
    }

    // パスワードハッシュ化
    const saltRounds = parseInt(process.env.BCRYPT_ROUNDS) || 12;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // ユーザー作成
    const userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const user = {
      id: userId,
      username,
      email,
      password: hashedPassword,
      createdAt: new Date().toISOString(),
      isActive: true,
      profile: {
        level: 'beginner',
        totalSessions: 0,
        lastLoginAt: null
      }
    };

    users.set(username, user);

    // トークン生成
    const { accessToken, refreshToken } = generateTokens(userId);

    // セッション保存
    sessions.set(userId, {
      refreshToken,
      createdAt: new Date().toISOString(),
      lastAccess: new Date().toISOString()
    });

    logger.info(`User registered: ${username}`);

    res.status(201).json({
      message: 'User registered successfully',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        profile: user.profile
      },
      tokens: {
        accessToken,
        refreshToken
      }
    });

  } catch (error) {
    logger.error('Registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ユーザーログイン
router.post('/login', authLimiter, loginValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { username, password } = req.body;

    // ユーザー確認
    const user = users.get(username);
    if (!user) {
      logger.warn(`Login attempt with non-existent username: ${username}`);
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    if (!user.isActive) {
      return res.status(401).json({ error: 'Account is deactivated' });
    }

    // パスワード確認
    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      logger.warn(`Failed login attempt for user: ${username}`);
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // トークン生成
    const { accessToken, refreshToken } = generateTokens(user.id);

    // セッション更新
    sessions.set(user.id, {
      refreshToken,
      createdAt: new Date().toISOString(),
      lastAccess: new Date().toISOString()
    });

    // ユーザー情報更新
    user.profile.lastLoginAt = new Date().toISOString();

    logger.info(`User logged in: ${username}`);

    res.json({
      message: 'Login successful',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        profile: user.profile
      },
      tokens: {
        accessToken,
        refreshToken
      }
    });

  } catch (error) {
    logger.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// トークンリフレッシュ
router.post('/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      return res.status(401).json({ error: 'Refresh token required' });
    }

    jwt.verify(refreshToken, process.env.JWT_SECRET, (err, decoded) => {
      if (err) {
        return res.status(403).json({ error: 'Invalid refresh token' });
      }

      if (decoded.type !== 'refresh') {
        return res.status(403).json({ error: 'Invalid token type' });
      }

      // セッション確認
      const session = sessions.get(decoded.userId);
      if (!session || session.refreshToken !== refreshToken) {
        return res.status(403).json({ error: 'Invalid session' });
      }

      // 新しいトークン生成
      const { accessToken, refreshToken: newRefreshToken } = generateTokens(decoded.userId);

      // セッション更新
      sessions.set(decoded.userId, {
        refreshToken: newRefreshToken,
        createdAt: session.createdAt,
        lastAccess: new Date().toISOString()
      });

      res.json({
        accessToken,
        refreshToken: newRefreshToken
      });
    });

  } catch (error) {
    logger.error('Token refresh error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ログアウト
router.post('/logout', authenticateToken, (req, res) => {
  try {
    // セッション削除
    sessions.delete(req.userId);

    logger.info(`User logged out: ${req.userId}`);

    res.json({ message: 'Logout successful' });

  } catch (error) {
    logger.error('Logout error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// プロフィール取得
router.get('/profile', authenticateToken, (req, res) => {
  try {
    // ユーザー検索
    let user = null;
    for (const u of users.values()) {
      if (u.id === req.userId) {
        user = u;
        break;
      }
    }

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        profile: user.profile,
        createdAt: user.createdAt
      }
    });

  } catch (error) {
    logger.error('Profile retrieval error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = { router, authenticateToken };
