# 移行用クリーンフォルダ
# Migration Clean Folder for New Workspace

このフォルダは新しいワークスペースへの移行用に、既存ハンドラーの
**完全ハードコーディング除去版**を作成・保管するためのフォルダです。

## 📁 フォルダの目的

1. **既存資産の保護**: 元のハンドラーはそのまま維持
2. **ハードコーディング完全除去**: 各ハンドラーの汎用化
3. **新ワークスペース準備**: クリーンなコードベースの構築
4. **段階的移行**: 一つずつ丁寧にクリーン版を作成

## 🎯 作成予定のクリーンハンドラー

### Phase 1: 基礎ハンドラー
- [ ] `basic_five_pattern_handler_clean.py`
- [ ] `adverb_handler_clean.py`
- [ ] `relative_clause_handler_clean.py`
- [ ] `passive_voice_handler_clean.py`

### Phase 2: 専門ハンドラー
- [ ] `modal_handler_clean.py`
- [ ] `conditional_handler_clean.py`
- [ ] `infinitive_handler_clean.py`
- [ ] `gerund_handler_clean.py`

### Phase 3: 高度ハンドラー
- [ ] `noun_clause_handler_clean.py`
- [ ] `question_handler_clean.py`
- [ ] `imperative_handler_clean.py`

## 🚨 ハードコーディング除去原則

### 禁止事項
- ❌ 固定語彙リスト（動詞分類、助動詞リストなど）
- ❌ 品詞タグ直接比較（`token.pos_ == 'VERB'`）
- ❌ 特定単語条件分岐（`if word == 'that'`）
- ❌ 固定信頼度値（`confidence = 0.8`）

### 必須事項
- ✅ 設定ファイルベースの語彙管理
- ✅ 汎用的パターンマッチング
- ✅ 動的信頼度計算
- ✅ 標準化インターフェース準拠

## 📋 移行プロセス

1. **元ハンドラー分析**: 既存コードの機能抽出
2. **ハードコーディング特定**: 固定値・条件の洗い出し
3. **汎用化設計**: 設定ファイル・パターン化
4. **クリーン実装**: 新しいアーキテクチャで再実装
5. **テスト検証**: 機能維持の確認

## 🔄 使用方法

新しいワークスペースでは、このフォルダ内のクリーンハンドラーを
`central_controller_v3_generic.py`と組み合わせて使用します。

既存の全機能を維持しながら、ハードコーディング皆無の
真の汎用システムを実現します。
