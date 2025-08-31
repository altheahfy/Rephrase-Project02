# 段階的文法拡張開発プロセス

## 🎯 基本方針
**100%スコア維持しながら段階的に文法要素を追加していく健全な開発プロセス**

## 📂 ファイル構成

### メインテストデータ
- `final_54_test_data_with_absolute_order_corrected.json` - 現在実装済み範囲（112ケース・100%対応）

### バックアップ・予備データ  
- `final_54_test_data_with_absolute_order_corrected_BACKUP.json` - 元の全データ（120ケース）
- `current_implemented_test_data.json` - 実装済み範囲専用（112ケース）
- `future_unimplemented_test_data.json` - 未実装ケース（8ケース）

## 🚀 新文法ハンドラー開発プロセス

### ステップ1: 新文法要素の設計
1. **文法要素の選定** (例: NounClauseHandler)
2. **テストケース作成** (英文法教科書ベース)
3. **期待する分解結果設計**

### ステップ2: テストケース追加
```bash
# 新しい文法のテストケースを末尾に追加
python add_new_grammar_cases.py --handler NounClauseHandler --cases noun_clause_test_cases.json
```

### ステップ3: ハンドラー実装
1. **ハンドラークラス作成**
2. **パターン認識ロジック実装**
3. **CentralControllerとの統合**

### ステップ4: テスト・調整
```bash
# 新しく追加した範囲のみをテスト
python fast_test.py 113,114,115,116,117

# 全体回帰テスト
python fast_test.py
```

### ステップ5: 100%達成確認
- 新範囲が100%になるまで調整
- 既存範囲の回帰なし確認
- 完成したら次の文法へ

## 📋 英文法体系的実装順序

### 優先度1: 基本節構造
1. **NounClauseHandler** - 名詞節（that節・wh-節）
2. **AdverbialClauseHandler** - 副詞節（時・条件・理由等）

### 優先度2: 準動詞
3. **InfinitiveHandler** - 不定詞（名詞・形容詞・副詞用法）
4. **GerundHandler** - 動名詞

### 優先度3: 高度構文
5. **ComparativeHandler** - 比較構文
6. **InversionHandler** - 倒置構文
7. **EllipsisHandler** - 省略構文

## 💡 開発のメリット

### ✅ **品質保証**
- 常に100%スコア維持
- 回帰バグの即座検出
- 確実な進捗確認

### ✅ **開発効率**
- 小さな単位での集中開発
- デバッグ範囲の限定
- 段階的な複雑性管理

### ✅ **保守性**
- 各文法要素の独立性確保
- テストケースの体系的管理
- 将来の拡張性確保

## 🔧 ユーティリティスクリプト（今後作成予定）

### `add_new_grammar_cases.py`
新しい文法のテストケースを末尾に追加

### `validate_test_format.py`  
テストケース形式の妥当性検証

### `grammar_coverage_analyzer.py`
実装済み文法要素の網羅性分析

## 📊 現在の状況（2025年8月31日）
- **実装済み**: 112ケース（100%対応）
- **保留中**: 8ケース（ComplexConstructionHandler相当）
- **次期目標**: NounClauseHandler実装
- **最終目標**: 英文法完全制覇

この開発プロセスにより、確実かつ効率的に「モンスター級文法解析システム」を構築していきます。
