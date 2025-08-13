# ファイル整理計画 2025-08-12

## 🎯 整理目標
- アクティブエンジンの明確化
- 開発履歴の保存
- テストファイルの整理
- ディレクトリ構造の最適化

## 📁 新しいディレクトリ構造

### engines/ （メインエンジン）
- `simple_relative_engine.py` - 関係代名詞エンジン（完成）
- `stanza_based_conjunction_engine.py` - 従属接続詞エンジン（NEW）
- `pure_stanza_engine_v3_1_unified.py` - 統合エンジン

### archived_engines/ （過去バージョン）
- `subordinate_conjunction_engine.py` - 旧接続詞エンジン
- `pure_stanza_engine_v3.py`
- `pure_stanza_engine_v4.py`
- `simple_relative_clause.py`
- `step18_complete_8slot.py`

### tests/ （テスト関連）
- `test_relative_clause_v2.py`
- `test_advanced_sublevel.py`  
- `test_unified_nesting.py`
- `test_v4_evaluation.py`

### debug/ （デバッグ・分析）
- `debug_relative_clause.py`
- `debug_stanza_nesting.py`
- `analyze_relative_clauses.py`

### data/ （データファイル）
- JSONファイル
- Excelファイル
- 設定ファイル

## 🔄 移動計画

### Phase 1: ディレクトリ作成
- [x] engines/
- [x] archived_engines/
- [x] debug/
- [ ] 実行予定

### Phase 2: アクティブエンジン移動
- `simple_relative_engine.py` → `engines/`
- `stanza_based_conjunction_engine.py` → `engines/`
- `pure_stanza_engine_v3_1_unified.py` → `engines/`

### Phase 3: アーカイブ
- 旧エンジンを `archived_engines/` へ
- デバッグファイルを `debug/` へ

### Phase 4: テスト整理
- tests/ ディレクトリ内を整理
- 動作しないテストの確認・修正

## 📊 整理後の状態
```
training/data/
├── engines/                    # メインエンジン（3個）
├── archived_engines/           # 過去バージョン
├── debug/                      # デバッグ・分析
├── tests/                      # テストファイル
├── preset_config.json          # 設定ファイル
├── *.json                      # データファイル
└── *.xlsx                      # Excel文書
```
