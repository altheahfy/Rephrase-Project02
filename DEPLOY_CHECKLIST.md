# 🚀 Rephrase デプロイチェックリスト

## ✅ デプロイ前必須確認事項

### 1. 設定ファイル確認
- [ ] `.htaccess`ファイルがルートディレクトリにある
- [ ] `training/index.html`の`SKIP_AUTH_FOR_DEVELOPMENT = false`に設定済み
- [ ] セキュリティヘッダーが有効になっている

### 2. ファイル・フォルダ構造確認
```
Rephrase-Project/
├── .htaccess                     ✅ セキュリティ設定
├── index.html                    ✅ メインページ
├── README.md                     ✅ ドキュメント
├── assets/                       ✅ CSSリソース
│   └── styles/
├── training/                     ✅ メイン機能
│   ├── index.html               ✅ トレーニングUI
│   ├── js/                      ✅ JavaScript機能
│   ├── css/                     ✅ スタイル
│   ├── data/                    ✅ JSONデータ
│   └── slot_images/             ✅ 学習用画像
└── commercial/                   ✅ 商用機能
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

すべての項目をクリアしたら、デプロイ準備完了です！

- [ ] 全ファイルアップロード完了
- [ ] 権限設定完了  
- [ ] HTTPS動作確認完了
- [ ] 音声機能動作確認完了
- [ ] モバイル表示確認完了
- [ ] データ読み込み確認完了

## 🗑️ デプロイ時削除対象ファイル・フォルダ

### ⚠️ セキュリティリスク高：必須削除項目

#### 1. 設計・開発ドキュメント（機密情報含む）
```
設計仕様書/                     ❌ 全フォルダ削除必須
├── 認証システム設計仕様書_v2.0.md    ❌ 認証情報漏洩リスク
├── SECURITY_PERFORMANCE_IMPROVEMENTS_2025-07-21.md ❌ セキュリティ情報
├── Rephrase_本番デプロイメント総合仕様書_v1.0.md ❌ インフラ情報
└── その他すべての設計書            ❌ システム構造暴露リスク
```

#### 2. 商用・運用情報（機密）
```
commercial/                     ❌ 全フォルダ削除必須
├── サクラインターネット運用手順書.md   ❌ サーバー接続情報
├── 課金システム実装ガイド.md         ❌ 決済システム情報
├── サクラインターネット商用展開計画.md  ❌ ビジネス機密
└── 明日からの商用展開実行計画_2025年8月3日開始.md ❌ 戦略情報
```

#### 3. 管理者専用ツール
```
training/explanation/
├── admin-panel.html           ❌ 管理者パネル（重大セキュリティリスク）
├── generator.js              ❌ 文法解説生成システム
└── template.html             ❌ テンプレート編集機能
```

#### 4. データベース作成システム
```
training/data/
├── Excel_Generator.py         ❌ DB作成システム（外部公開禁止）
├── Rephrase_Parsing_Engine.py ❌ 構文解析エンジン（ソースコード）
├── 例文入力元.xlsx           ❌ 元データファイル（編集用）
├── 例文入力元_分解結果_v2.xlsx ❌ 開発用データ
├── 新規例文セット追加方法.md    ❌ 管理者向けマニュアル
└── rephrase_rules_v1.0.json  ❌ ルール辞書（編集可能版）
```

#### 5. 開発・Git関連ファイル
```
.git/                         ❌ Git履歴（全削除）
.github/                      ❌ GitHub設定
.gitignore                    ❌ Git設定ファイル
.vscode/                      ❌ VS Code設定
README.md                     ❌ 開発者向け説明
DEPLOY_CHECKLIST.md           ❌ このファイル自体も削除
DEPLOYMENT_SPEC.md            ❌ デプロイ仕様書
```

### 削除実行コマンド（デプロイ前実行）
```powershell
# 【重要】必ずバックアップを取ってから実行

# 1. 設計書フォルダ削除（機密情報）
Remove-Item -Path "設計仕様書" -Recurse -Force

# 2. 商用情報フォルダ削除（機密）
Remove-Item -Path "commercial" -Recurse -Force

# 3. 管理者ツール削除
Remove-Item -Path "training/explanation/admin-panel.html" -Force
Remove-Item -Path "training/explanation/generator.js" -Force
Remove-Item -Path "training/explanation/template.html" -Force

# 4. データベース作成システム削除
Remove-Item -Path "training/data/Excel_Generator.py" -Force
Remove-Item -Path "training/data/Rephrase_Parsing_Engine.py" -Force
Remove-Item -Path "training/data/例文入力元.xlsx" -Force
Remove-Item -Path "training/data/例文入力元_分解結果_v2.xlsx" -Force
Remove-Item -Path "training/data/新規例文セット追加方法.md" -Force
Remove-Item -Path "training/data/rephrase_rules_v1.0.json" -Force

# 5. 開発関連ファイル削除
Remove-Item -Path ".git" -Recurse -Force
Remove-Item -Path ".github" -Recurse -Force
Remove-Item -Path ".gitignore" -Force
Remove-Item -Path ".vscode" -Recurse -Force
Remove-Item -Path "README.md" -Force
Remove-Item -Path "DEPLOY_CHECKLIST.md" -Force
Remove-Item -Path "DEPLOYMENT_SPEC.md" -Force
```

### 本番環境最小構成（セキュア版）
```
Rephrase-Project/
├── .htaccess                    ✅ セキュリティ設定
├── index.html                   ✅ メインページ
├── manifest.json                ✅ PWA設定
├── sw.js                       ✅ Service Worker
├── robots.txt                  ✅ SEO設定
├── sitemap.xml                 ✅ SEO設定
├── 404.html                    ✅ エラーページ
├── assets/                     ✅ CSS・画像リソース
└── training/                   ✅ メイン機能
    ├── index.html              ✅ トレーニングUI
    ├── auth.html               ✅ 認証ページ
    ├── auth-check.html         ✅ 認証チェック
    ├── style.css               ✅ メインスタイル
    ├── mobile-split-view-simple.css ✅ モバイル対応
    ├── js/                     ✅ JavaScript機能（認証・UI制御）
    ├── css/                    ✅ 詳細スタイル
    ├── data/                   ✅ 例文JSONデータのみ
    │   ├── preset_config.json
    │   ├── slot_order_data.json
    │   ├── V自動詞第1文型.json
    │   └── 第3,4文型.json
    ├── explanation/            ✅ 文法解説ページ（表示のみ）
    │   ├── articles-definite.html
    │   ├── v-intransitive-type1.html
    │   └── 他動詞第3,4文型.html
    ├── grammar/                ✅ 文法学習機能
    ├── matrix/                 ✅ マトリックス機能
    └── slot_images/           ✅ 学習用画像
```

### ⚠️ セキュリティ警告
1. **admin-panel.html**: 管理者パネルへのアクセスは重大なセキュリティ違反
2. **設計仕様書フォルダ**: システム構造・認証情報の暴露リスク
3. **commercialフォルダ**: サーバー接続情報・ビジネス機密の漏洩リスク
4. **Excel_Generator.py等**: ソースコードへの直接アクセスでシステム解析可能
5. **Git履歴**: コミット履歴から開発過程・機密情報が判明する危険性

### 段階的削除推奨手順
```
【Phase 1】機密情報削除
→ 設計仕様書/, commercial/, .git/ 削除

【Phase 2】管理者ツール削除  
→ admin-panel.html, generator.js, template.html削除

【Phase 3】データベース作成システム削除
→ Python scripts, 元データExcel削除

【Phase 4】動作テスト
→ ユーザー機能のみでの動作確認

【Phase 5】最終クリーンアップ
→ 開発用ファイル(.gitignore, README.md等)削除
```

---

**🎉 デプロイ成功後は、快適な英語学習環境をお楽しみください！**
