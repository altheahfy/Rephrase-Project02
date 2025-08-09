# 🚀 Rephrase デプロイチェックリスト

## 🗑️ デプロイ前ファイル除外リスト（重要）

### 除外対象フォルダ・ファイル（本番環境にアップロード禁止）

#### 1. 開発・設計仕様書フォルダ（全体除外）
```
❌ 設計仕様書/                    # 設計ドキュメント類（全ファイル）
```

#### 2. 例文DB作成システムファイル
```
❌ training/data/Excel_Generator.py              # Excel生成システム
❌ training/data/Rephrase_Parsing_Engine.py     # 文法解析エンジン  
❌ training/data/rephrase_rules_v1.0.json       # ルール定義ファイル
❌ training/data/__pycache__/                    # Pythonキャッシュ
❌ training/data/.gitignore                      # Git設定ファイル
❌ training/data/例文入力元.xlsx                 # Excel入力ファイル
❌ training/data/例文入力元_分解結果_v2.xlsx     # 分解結果ファイル
❌ training/data/新規例文セット追加方法.md       # 開発手順書
❌ training/data/本番導入ガイド.md               # 開発ガイド
❌ training/data/（小文字化した最初の5文型フルセット）例文入力元.xlsx
❌ training/data/（第4文型）例文入力元.xlsx
```

#### 3. 文法解説ページ作成システム
```
❌ training/explanation/                         # 文法解説生成システム（全体）
   ├── admin-panel.html                         # 管理パネル  
   ├── generator.js                             # 生成システム
   ├── template.html                            # テンプレート
   ├── grammar-metadata.json                    # メタデータ
   ├── articles-definite.html                   # 生成済み解説
   ├── v-intransitive-type1.html               # 生成済み解説
   └── 他動詞第3,4文型.html                    # 生成済み解説
```

#### 4. 商用展開関連ドキュメント
```
❌ commercial/サクラインターネット商用展開計画.md
❌ commercial/サクラインターネット運用手順書.md  
❌ commercial/明日からの商用展開実行計画_2025年8月3日開始.md
❌ commercial/課金システム実装ガイド.md
```

### デプロイ可能ファイルのみ（アップロード対象）

#### ✅ ルートレベル
```
✅ index.html                     # メインページ
✅ 404.html                       # エラーページ
✅ manifest.json                  # PWA設定
✅ sw.js                          # Service Worker
✅ robots.txt                     # SEO設定
✅ sitemap.xml                    # サイトマップ
✅ README.md                      # プロジェクト説明
✅ DEPLOY_CHECKLIST.md           # このファイル
✅ DEPLOYMENT_SPEC.md            # デプロイ仕様書
```

#### ✅ assetsフォルダ
```
✅ assets/favicon.svg
✅ assets/images/features/
✅ assets/js/production-error-handler.js
✅ assets/styles/main.css
✅ assets/styles/grammar.css
```

#### ✅ trainingフォルダ（本番機能のみ）
```
✅ training/index.html                        # メイン学習UI
✅ training/auth.html                         # 認証ページ
✅ training/auth-check.html                   # 認証チェック
✅ training/style.css                         # メインスタイル
✅ training/mobile-split-view-simple.css      # モバイル対応
✅ training/image_meta_tags.json              # 画像メタデータ

✅ training/css/                              # スタイル（最適化版のみ）
   ├── voice_progress.css
   ├── voice-panel-mobile.css
   └── optimized/

✅ training/js/                               # JavaScript機能
✅ training/grammar/                          # 文法学習機能
✅ training/matrix/                           # マトリックス機能
✅ training/slot_images/                      # 学習用画像

✅ training/data/（JSONデータのみ）
   ├── preset_config.json                    # プリセット設定
   ├── slot_order_data.json                  # スロット表示設定
   ├── V自動詞第1文型.json                   # 文法データ
   └── 第3,4文型.json                        # 文法データ
```

#### ✅ serverフォルダ（必要に応じて）
```
✅ server/                        # サーバー機能（別途サーバーで使用）
```

## ✅ デプロイ前必須確認事項

### 1. 設定ファイル確認
- [ ] `.htaccess`ファイルがルートディレクトリにある
- [ ] `training/index.html`の`SKIP_AUTH_FOR_DEVELOPMENT = false`に設定済み
- [ ] セキュリティヘッダーが有効になっている

### 2. ファイル・フォルダ構造確認（デプロイ版）

#### 本番環境構造（除外ファイルを削除後）
```
Rephrase-Project/
├── .htaccess                     ✅ セキュリティ設定
├── index.html                    ✅ メインページ
├── 404.html                      ✅ エラーページ
├── manifest.json                 ✅ PWA設定
├── sw.js                         ✅ Service Worker
├── robots.txt                    ✅ SEO設定
├── sitemap.xml                   ✅ サイトマップ
├── README.md                     ✅ ドキュメント
├── DEPLOY_CHECKLIST.md          ✅ デプロイ手順
├── DEPLOYMENT_SPEC.md           ✅ デプロイ仕様書
├── assets/                       ✅ 静的リソース
│   ├── favicon.svg              ✅ ファビコン
│   ├── images/features/         ✅ 機能画像
│   ├── js/production-error-handler.js ✅ エラーハンドラー
│   └── styles/                  ✅ CSSスタイル
│       ├── main.css
│       └── grammar.css
├── training/                     ✅ メイン機能
│   ├── index.html               ✅ トレーニングUI
│   ├── auth.html                ✅ 認証ページ
│   ├── auth-check.html          ✅ 認証チェック
│   ├── style.css                ✅ メインスタイル
│   ├── mobile-split-view-simple.css ✅ モバイル対応
│   ├── image_meta_tags.json     ✅ 画像メタデータ
│   ├── css/                     ✅ スタイル
│   │   ├── voice_progress.css
│   │   ├── voice-panel-mobile.css
│   │   └── optimized/
│   ├── js/                      ✅ JavaScript機能
│   ├── grammar/                 ✅ 文法学習
│   ├── matrix/                  ✅ マトリックス機能
│   ├── slot_images/             ✅ 学習用画像
│   └── data/                    ✅ JSONデータのみ
│       ├── preset_config.json
│       ├── slot_order_data.json
│       ├── V自動詞第1文型.json
│       └── 第3,4文型.json
└── server/                       ✅ サーバー機能（別途配置）
    ├── server.js
    ├── package.json
    ├── ecosystem.config.js
    ├── routes/
    └── scripts/
```

#### ⚠️ 除外確認（これらがないことを確認）
```
❌ 設計仕様書/                   # 設計ドキュメント（フォルダごと）
❌ commercial/                   # 商用展開ドキュメント
❌ training/explanation/         # 解説生成システム
❌ training/data/*.py           # Python開発ファイル
❌ training/data/*.xlsx         # Excel開発ファイル
❌ training/data/__pycache__/   # Pythonキャッシュ
❌ training/data/*.md           # 開発手順書
```

### 3. さくらインターネット デプロイ手順

#### Step 1: ファイルアップロード
1. FTPクライアント（FileZilla推奨）でサーバーに接続
2. `/home/[ユーザー名]/www/`ディレクトリに全ファイルをアップロード
3. ファイル権限を適切に設定

#### Step 2: 権限設定（重要）
```bash
# ディレクトリ権限（さくらレンタルサーバー）
chmod 755 training/
chmod 755 training/data/
chmod 755 training/slot_images/
chmod 755 assets/

# ファイル権限
chmod 644 *.html
chmod 644 training/data/*.json
chmod 644 .htaccess
```

#### Step 3: 動作確認
1. **メインページ**: `https://[ドメイン]/index.html`
2. **トレーニング**: `https://[ドメイン]/training/`
3. **音声機能**: HTTPS環境で音声認識テスト
4. **画像表示**: スロット画像の正常表示確認
5. **JSON読み込み**: データ選択機能の動作確認

### 4. 本番環境での必須テスト項目

#### 🔒 セキュリティ確認
- [ ] HTTPSアクセスが強制されている
- [ ] セキュリティヘッダーが有効
- [ ] 不要なファイルへのアクセスが制限されている

#### 🎤 音声機能確認（重要）
- [ ] PC Chromeで音声認識が動作
- [ ] Androidで音声認識が動作
- [ ] 録音・再生機能が正常
- [ ] 音声分析結果が表示される

#### 📱 モバイル対応確認
- [ ] スマートフォンで正常表示
- [ ] タッチ操作が適切に動作
- [ ] レスポンシブデザインが機能

#### 📊 データ機能確認
- [ ] プリセットJSONデータの読み込み
- [ ] ランダマイズ機能の動作
- [ ] スロット表示制御の動作
- [ ] 解説システムの動作

### 5. パフォーマンス最適化確認
- [ ] 画像が遅延読み込みされている
- [ ] JavaScriptの圧縮・最適化
- [ ] CSSの最適化
- [ ] Gzip圧縮が有効

### 6. 緊急時対応準備
- [ ] バックアップファイルの保存
- [ ] エラーログの確認方法
- [ ] 設定戻し手順の確認

## 🆘 よくある問題と解決法

### Q1: 音声認識が動作しない
**A**: HTTPSでアクセスし、ブラウザのマイク許可を確認

### Q2: 画像が表示されない  
**A**: `training/slot_images/`の権限を755に設定

### Q3: JSONデータが読み込めない
**A**: `training/data/`の権限を755に設定、CORSエラー確認

### Q4: .htaccessが効かない
**A**: さくらレンタルサーバーの設定でmod_rewriteが有効か確認

## 📞 技術サポート

### 自動エラー監視機能
- エラーハンドリング: 自動エラー記録
- レート制限監視: 過負荷検出
- セキュリティ監視: 不正アクセス検出

### デバッグ方法
1. ブラウザ開発者ツール（F12）でコンソール確認
2. ネットワークタブでリソース読み込み確認
3. `training/`ページで📱デバッグボタン利用

## ✅ 最終チェック

### デプロイ前ファイル除外確認
- [ ] `設計仕様書/`フォルダが削除されている
- [ ] `commercial/`フォルダが削除されている  
- [ ] `training/explanation/`フォルダが削除されている
- [ ] `training/data/`内のPythonファイル（*.py）が削除されている
- [ ] `training/data/`内のExcelファイル（*.xlsx）が削除されている
- [ ] `training/data/__pycache__/`フォルダが削除されている
- [ ] `training/data/`内の開発用マークダウンファイル（*.md）が削除されている
- [ ] `training/data/.gitignore`が削除されている

#### PowerShell一括削除コマンド（参考）
```powershell
# プロジェクトルートディレクトリで実行
Remove-Item "設計仕様書" -Recurse -Force
Remove-Item "commercial" -Recurse -Force  
Remove-Item "training\explanation" -Recurse -Force
Remove-Item "training\data\*.py" -Force
Remove-Item "training\data\*.xlsx" -Force
Remove-Item "training\data\__pycache__" -Recurse -Force
Remove-Item "training\data\*.md" -Force
Remove-Item "training\data\.gitignore" -Force
```

### 本番機能確認
すべての項目をクリアしたら、デプロイ準備完了です！

- [ ] 除外ファイル削除確認完了
- [ ] 本番用ファイルのみ残存確認完了
- [ ] 全ファイルアップロード完了
- [ ] 権限設定完了  
- [ ] HTTPS動作確認完了
- [ ] 音声機能動作確認完了
- [ ] モバイル表示確認完了
- [ ] データ読み込み確認完了

---

**🎉 デプロイ成功後は、快適な英語学習環境をお楽しみください！**
