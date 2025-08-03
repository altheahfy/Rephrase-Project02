# Rephrase 認証システム設計仕様書 v1.0

## 📋 概要

本仕様書は、Rephrase英語学習システムの認証システムについて、現在の実装状況と本番環境移行時の手順を詳細に記載しています。

---

## 🎯 実装方式の選択

### 現在採用している方式：**段階的アプローチ**

1. **フェーズ1（現在）**: localStorage版認証システム - 即座デプロイ可能
2. **フェーズ2（将来）**: サーバーサイド版認証システム - 本格運用

---

## 📊 フェーズ1：localStorage版認証システム（現在の実装）

### ✅ 実装済み機能

#### 1. 認証システム基盤
- **ファイル**: `training/js/auth.js` (456行)
- **機能**: ユーザー登録、ログイン、セッション管理
- **暗号化**: SHA-256によるパスワードハッシュ化
- **セキュリティ**: レート制限、アカウントロック機能

#### 2. ユーザーデータ管理
- **保存先**: ブラウザのlocalStorage
- **暗号化**: `security.js`による暗号化保存
- **データ形式**:
```javascript
{
  id: "user_1234567890_abc123",
  username: "ユーザー名",
  email: "email@example.com",
  passwordHash: "暗号化されたパスワード",
  salt: "ソルト値",
  createdAt: "2025-08-03T10:00:00.000Z",
  lastLogin: "2025-08-03T11:00:00.000Z",
  loginAttempts: 0,
  lockedUntil: null,
  isActive: true
}
```

#### 3. セキュリティ機能
- **ファイル**: `training/js/security.js`
- **機能**: 
  - 暗号化localStorage操作
  - CSRF保護
  - 入力値サニタイズ
  - XSS防止

#### 4. 認証フロー
```
1. ユーザーがトレーニングページにアクセス
   ↓
2. training/index.html で認証状態チェック
   ↓
3. 未ログインの場合 → training/auth.html にリダイレクト
   ↓
4. ログイン/登録完了 → training/index.html に戻る
   ↓
5. 学習システム利用可能
```

### 📁 関連ファイル一覧

```
training/
├── auth.html              # ログイン・登録画面
├── index.html             # メイン学習画面（認証チェック実装済み）
└── js/
    ├── auth.js            # 認証システム本体
    ├── security.js        # セキュリティユーティリティ
    ├── error-handler.js   # エラーハンドリング
    └── rate-limiter.js    # レート制限
```

### ⚙️ 現在の設定状態

#### 認証モード設定
```javascript
// training/index.html 369行目
const SKIP_AUTH_FOR_DEVELOPMENT = false; // 本番モード有効
```

#### 認証チェック実装箇所
```javascript
// training/index.html 390行目付近
if (!isLoggedIn) {
    console.log('未ログイン - auth.htmlにリダイレクト');
    window.location.href = './auth.html';
}
```

---

## 🌟 フェーズ1の特徴・制限事項

### ✅ メリット
- **即座デプロイ可能**: サーバー設定不要、静的ホスティングで動作
- **コスト効率**: データベースサーバー不要
- **シンプル運用**: 複雑なサーバー管理不要
- **セキュリティ**: 基本的なセキュリティ機能は実装済み

### ⚠️ 制限事項
- **デバイス間同期不可**: PC登録 → スマホでは別ユーザー扱い
- **データ永続性**: ブラウザデータクリア時にアカウント消失
- **課金システム連携不可**: 支払い状況の管理ができない
- **ユーザー管理制限**: パスワードリセット等のサポート機能なし

---

## 🚀 フェーズ2：サーバーサイド版認証システム（準備済み）

### 📦 準備済みサーバー環境

#### 1. サーバー構成
- **フレームワーク**: Express.js (Node.js)
- **認証方式**: JWT (JSON Web Token)
- **パスワード暗号化**: bcrypt
- **データベース**: SQLite（開発用） / MariaDB（本番用）

#### 2. 実装済み機能
```
server/
├── server.js              # メインサーバー
├── routes/
│   ├── auth.js            # 認証API
│   ├── users.js           # ユーザー管理API
│   ├── progress.js        # 学習進捗API
│   └── voice.js           # 音声機能API
├── package.json           # 依存関係定義
├── .env.example           # 環境設定テンプレート
└── ecosystem.config.js    # PM2設定（本番運用）
```

#### 3. API仕様（準備済み）
- `POST /auth/register` - ユーザー登録
- `POST /auth/login` - ログイン
- `POST /auth/logout` - ログアウト
- `GET /auth/verify` - トークン検証
- `POST /auth/refresh` - トークン更新

---

## 📋 本番環境移行手順

### Step 1: ホスティング環境の選択

#### Option A: 静的ホスティング（フェーズ1継続）
**推奨サービス**:
- さくらインターネット（スタンダード以上）
- Netlify
- Vercel
- GitHub Pages

**手順**:
1. GitHubリポジトリからファイルをダウンロード
2. ホスティングサービスにアップロード
3. ドメイン設定
4. SSL証明書設定

#### Option B: VPSサーバー（フェーズ2移行）
**推奨サービス**:
- さくらVPS
- ConoHa VPS
- AWS EC2
- DigitalOcean

### Step 2: 環境別設定

#### 🔧 静的ホスティング設定
```bash
# アップロード対象ファイル
- index.html
- training/ フォルダ全体
- assets/ フォルダ全体
- .htaccess（セキュリティ設定）
```

#### 🔧 VPSサーバー設定
```bash
# 1. Node.js環境構築
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. データベース設定
sudo apt-get install mariadb-server

# 3. アプリケーションデプロイ
git clone https://github.com/altheahfy/Rephrase-Project02.git
cd Rephrase-Project02/server
npm install
cp .env.example .env
# .env ファイルを編集（データベース設定等）
npm start
```

---

## 🔐 セキュリティ設定

### 現在実装済みセキュリティ機能

#### 1. 認証セキュリティ
- パスワードハッシュ化（SHA-256 + ソルト）
- セッションタイムアウト（24時間）
- ログイン試行制限（5回失敗で15分ロック）
- レート制限（API呼び出し制限）

#### 2. Webセキュリティ
```apache
# .htaccess（実装済み）
Header always set X-Frame-Options "DENY"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000"
```

#### 3. データ保護
- localStorage暗号化
- CSRF トークン保護
- 入力値サニタイズ
- XSS フィルタリング

---

## 📊 運用・監視

### ログ出力
```javascript
// 認証関連ログ（実装済み）
console.log('🔐 認証チェック開始');
console.log('ログイン成功:', username);
console.warn('ログイン失敗:', error.message);
```

### エラーハンドリング
- 詳細エラーログ記録
- ユーザーフレンドリーなエラーメッセージ
- セキュリティ上重要なエラーの通知

---

## 📈 将来の拡張計画

### Phase 3: 本格商用機能
1. **決済システム連携**
   - Stripe / PayPal 統合
   - サブスクリプション管理
   - 課金状況連携認証

2. **多デバイス対応**
   - JWT トークンベース認証
   - リアルタイム進捗同期
   - オフライン対応

3. **管理機能**
   - 管理者ダッシュボード
   - ユーザー管理画面
   - 学習分析レポート

---

## 🚨 トラブルシューティング

### よくある問題と解決方法

#### 1. 認証が効かない
**確認点**:
```javascript
// training/index.html の設定確認
const SKIP_AUTH_FOR_DEVELOPMENT = false; // falseになっているか
```

#### 2. auth.html が見つからない
**確認点**:
- `training/auth.html` ファイルが存在するか
- パーミッション設定が正しいか

#### 3. ユーザーデータが消える
**原因**: ブラウザのlocalStorageクリア
**対策**: フェーズ2への移行を検討

---

## 📞 サポート情報

### 開発チーム連絡先
- **プロジェクト**: Rephrase English Learning System
- **リポジトリ**: https://github.com/altheahfy/Rephrase-Project02
- **最終更新**: 2025年8月3日

### 緊急時対応
1. **認証システム無効化**:
   ```javascript
   // 緊急時のみ：training/index.html 369行目
   const SKIP_AUTH_FOR_DEVELOPMENT = true; // 一時的に無効化
   ```

2. **バックアップからの復元**:
   - `開発過程保管庫_2025-08-01/` フォルダ内にバックアップ保存済み

---

## ✅ チェックリスト

### デプロイ前確認事項
- [ ] 認証システム有効化確認（SKIP_AUTH_FOR_DEVELOPMENT = false）
- [ ] auth.html ファイル存在確認
- [ ] セキュリティ設定ファイル（.htaccess）確認
- [ ] SSL証明書設定
- [ ] ドメイン設定
- [ ] バックアップ体制確認

### 本番運用開始後
- [ ] ユーザー登録テスト
- [ ] ログイン/ログアウトテスト
- [ ] セキュリティテスト
- [ ] パフォーマンステスト
- [ ] 監視体制構築

---

*本仕様書は Rephrase 英語学習システム v2025.07.27-1 に基づいて作成されています。*
