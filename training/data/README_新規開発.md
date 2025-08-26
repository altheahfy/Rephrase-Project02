# 新規システム開発エリア

**🎯 目標**: Rephrase文法分解システム 完全新規実装  
**📋 設計仕様**: `NEW_SYSTEM_DESIGN_SPECIFICATION.md` に厳密準拠  
**🔥 開発方針**: Zero Technical Debt

---

## 📁 開発環境構成

### ✅ 開発用ファイル
- `NEW_SYSTEM_DESIGN_SPECIFICATION.md` - **必読設計仕様書**
- `slot_order_data.json` - Rephraseスロット構造定義
- `official_test_results.json` - テストケース・期待値
- `rephrase_rules_v2.0.json` - 基本ルール定義

### 🗂️ 参考システム/
- **⚠️ 既存システム群（参考のみ、使用禁止）**
- コード流用・継承・依存は絶対禁止
- 設計コンセプトの参考のみ許可

### 📊 データファイル
- `my_test_sentences.json` - テスト用例文
- `*.xlsx` - 例文データベース
- `*.json` - 各種文型データ

---

## 🚀 開発開始手順

### Phase 1: Central Controller + BasicFivePatternHandler
```bash
# 1. 新規ファイル作成
touch central_controller.py
touch basic_five_pattern_handler.py
touch boundary_expansion_lib_new.py

# 2. spaCy環境確認
python -c "import spacy; print(spacy.__version__)"

# 3. 初期テスト実行
python test_basic_five_patterns.py
```

### Phase 2: RelativeClauseHandler追加
```bash
touch relative_clause_handler.py
python test_relative_clauses.py
```

### Phase 3: PassiveVoiceHandler追加
```bash
touch passive_voice_handler.py
python test_passive_voice.py
```

---

## 🔧 技術制約

### ✅ 使用許可
- **spaCy**: POS解析のみ（pos_, tag_）
- **パターンマッチング**: 人間文法認識ベース
- **境界拡張**: 新規実装

### ❌ 使用禁止
- **spaCy依存関係解析**: dep_, head, children等
- **既存コード**: 流用・継承・import
- **Stanza**: 一切使用禁止
- **ハードコーディング**: 個別事例対応

---

## 📖 必読ドキュメント

1. `NEW_SYSTEM_DESIGN_SPECIFICATION.md` - **最重要**
2. `参考システム/README.md` - 禁止事項確認
3. `slot_order_data.json` - スロット構造理解

**成功の鍵**: 設計仕様の完全理解 + 禁止事項の厳守
