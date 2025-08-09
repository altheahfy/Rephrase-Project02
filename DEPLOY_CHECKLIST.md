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

### 必須削除項目（本番環境には不要）

#### 開発・デバッグ用ファイル
```
training/data/
├── analyze_code.py          ❌ コード分析スクリプト
├── debug_spacy.py          ❌ spaCyデバッグ用
├── quality_verification.py ❌ 品質検証用
├── rule_analysis.py        ❌ ルール分析用
├── test_coverage.py        ❌ テストカバレッジ検証
├── test_parsing.py         ❌ パース機能テスト
├── test_revert.py          ❌ リバート機能テスト
├── test_simple.py          ❌ シンプルテスト
├── test_spacy_vocab.py     ❌ spaCy語彙テスト
└── __pycache__/            ❌ Pythonキャッシュフォルダ
```

#### Git関連一時ファイル
```
.git-rewrite/               ❌ Git操作一時ファイル
```

#### 重複・古いバージョンファイル
```
training/js/
└── subslot_visibility_control.js  ❌ 古いバージョン
    (※ subslot_visibility_control_clean.js が正式版)
```

### 削除実行コマンド（デプロイ前実行）
```powershell
# training/dataフォルダのデバッグファイル削除
Remove-Item -Path "training/data/analyze_code.py", "training/data/debug_spacy.py", "training/data/quality_verification.py", "training/data/rule_analysis.py", "training/data/test_coverage.py", "training/data/test_parsing.py", "training/data/test_revert.py", "training/data/test_simple.py", "training/data/test_spacy_vocab.py" -Force

# キャッシュフォルダ削除
Remove-Item -Path "training/data/__pycache__" -Recurse -Force

# Git一時ファイル削除
Remove-Item -Path ".git-rewrite" -Recurse -Force
```

### 本番環境保持ファイル（重要）
```
training/data/
├── Excel_Generator.py           ✅ Excel生成エンジン
├── Rephrase_Parsing_Engine.py   ✅ メイン構文解析エンジン
├── preset_config.json           ✅ プリセット設定
├── slot_order_data.json         ✅ スロット順序データ
├── rephrase_rules_v1.0.json    ✅ ルール辞書
├── V自動詞第1文型.json         ✅ 例文データ
├── 第3,4文型.json              ✅ 例文データ
├── 例文入力元.xlsx             ✅ 元データ
├── 例文入力元_分解結果_v2.xlsx ✅ 分解済みデータ
└── 新規例文セット追加方法.md    ✅ ドキュメント
```

### ⚠️ 削除前注意事項
1. **必ずバックアップを取る**: `.zip`ファイルで全体をアーカイブ保存
2. **段階的削除**: 一度にすべて削除せず、動作確認しながら実行
3. **本番テスト**: 削除後に必ずローカル環境で動作テスト実行

---

**🎉 デプロイ成功後は、快適な英語学習環境をお楽しみください！**
