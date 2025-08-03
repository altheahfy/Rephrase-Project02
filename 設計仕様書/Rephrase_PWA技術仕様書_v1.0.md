# Rephrase PWA技術仕様書 v1.0

**作成日**: 2025年8月3日  
**対象**: Progressive Web App実装詳細  
**関連**: 本番デプロイメント総合仕様書

---

## 📋 PWA実装詳細

### 1. Service Worker仕様

#### 1.1 キャッシュ戦略
```javascript
const CACHE_NAME = 'rephrase-v1.0.0';

// キャッシュ対象ファイル
const urlsToCache = [
  '/',
  '/index.html',
  '/assets/styles/main.css',
  '/responsive.css',
  '/training/',
  '/training/index.html',
  '/training/js/auth.js',
  '/training/js/security.js',
  '/training/js/voice_system.js',
  '/training/matrix/',
  '/training/grammar/',
  '/manifest.json'
];
```

#### 1.2 ネットワーク戦略
- **Network First**: 最新データ優先、フォールバックでキャッシュ
- **404対応**: ネットワーク・キャッシュ両方で失敗時、カスタム404ページ表示

#### 1.3 キャッシュ更新
- **バージョン管理**: CACHE_NAME更新でキャッシュクリア
- **自動クリーンアップ**: 古いキャッシュ自動削除

### 2. Manifest仕様

#### 2.1 アプリケーション設定
```json
{
  "name": "Rephrase 英語学習システム",
  "short_name": "Rephrase",
  "description": "構文分析とスロットベースの革新的英語学習システム",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "scope": "/",
  "lang": "ja",
  "categories": ["education", "productivity"]
}
```

#### 2.2 テーマ・デザイン
```json
{
  "background_color": "#ffffff",
  "theme_color": "#667eea"
}
```

#### 2.3 アイコン設定
```json
{
  "icons": [
    {
      "src": "assets/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "assets/icon-512x512.png", 
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable any"
    }
  ]
}
```

### 3. インストール対応

#### 3.1 プラットフォーム別対応
- **iOS Safari**: Add to Home Screen
- **Android Chrome**: PWAインストールプロンプト
- **Desktop Chrome**: PWAインストール対応
- **Edge**: PWAサポート

#### 3.2 インストール促進
- **Install Prompt**: 今後実装予定
- **App Store配布**: 今後検討

### 4. オフライン機能

#### 4.1 利用可能機能
- **基本ページ閲覧**: ホーム、トレーニング選択
- **認証**: localStorage使用で継続
- **静的コンテンツ**: 文法説明など

#### 4.2 制限事項
- **音声認識**: オンライン必須
- **データ同期**: オンライン必須
- **新規ユーザー登録**: オンライン必須

---

**技術責任者**: [開発チーム]  
**最終更新**: 2025年8月3日
