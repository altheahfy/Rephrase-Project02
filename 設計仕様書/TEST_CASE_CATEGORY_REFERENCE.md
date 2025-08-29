# テストケース カテゴリ参照仕様書

## 対象テストケース範囲（固定）

### 基本テスト対象カテゴリ
以下の6つのカテゴリが基本テスト対象：

1. **basic_5_patterns**: ケース1-17（基本5文型）
2. **basic_adverbs**: ケース18-42（基本副詞）
3. **relative_clauses**: ケース43-65（関係節）
4. **passive_voice**: ケース66-69（受動態）
5. **perfect_tense**: ケース70（現在完了 - エラー予想）
6. **absolute_order_test**: ケース83-86（tellグループ疑問文）

### 対象外カテゴリ
- **complex_constructions**: ケース71-82（複合構文）

## テスト実行コマンド

### 基本対象ケース全実行
```bash
# 基本テスト範囲（tellグループ含む）
python fast_test.py 1-70,83-86

# または個別に
python fast_test.py 1-70
python fast_test.py 83-86
```

### カテゴリ別実行
```bash
# 基本5文型のみ
python fast_test.py 1-17

# 基本副詞のみ
python fast_test.py 18-42

# 関係節のみ
python fast_test.py 43-65

# 受動態のみ
python fast_test.py 66-69

# 現在完了のみ（エラー予想）
python fast_test.py 70

# tellグループのみ
python fast_test.py 83-86
```

## 成功目標
- **Case 70（現在完了）のみエラー** が許容される
- その他全ケース（1-69, 83-86）は成功が必須
- tellグループ（83-86）は疑問文処理が必要

## 注意事項
- tellグループ（83-86）は疑問文で、QuestionHandlerが処理
- 基本5文型、関係節、基本副詞、受動態、tellグループが主要テスト対象
- Case 70は現在完了で、助動詞ハンドラーが未実装のためエラーが予想される
- complex_constructions（71-82）は高度な構文で、基本テスト対象外

## tellグループ詳細（83-86）
- Case 83: "What did he tell her at the store?"
- Case 84: "Did he tell her a secret there?"  
- Case 85: "Did I tell him a truth in the kitchen?"
- Case 86: "Where did you tell me a story?"

---
*最終更新: 2025年8月29日*
