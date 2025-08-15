# Rephrase Parser Integration Design Principles
**Rephrase English Learning System**  
**作成日:** 2025年8月15日  
**バージョン:** v1.0  
**ステータス:** Core Design Document

## 🎯 基本設計原則

### 1. パーサー出力の保護原則
**原則**: StanzaやspaCyの解析結果を無理に変更してはならない

**理由**:
- 既存の正常ケースへの悪影響を防ぐ
- パーサーの設計思想を尊重
- システムの安定性確保

**実装方針**:
```python
# ❌ 間違ったアプローチ
def modify_parser_output(sentence):
    # パーサーの依存関係を強制変更
    if word.deprel == 'xcomp':
        word.deprel = 'acl:relcl'  # 危険！

# ✅ 正しいアプローチ  
def _apply_rephrase_rules(self, result, sentence):
    # パーサー出力は保持し、Rephraseルールで後処理
    return self._apply_consecutive_verb_rule(result, sentence)
```

### 2. Rephraseルール階層設計

**階層構造**:
1. **パーサー解析層** (Stanza/spaCy)
2. **基本ハンドラー層** (5文型、関係節、副詞など)
3. **Rephraseルール層** ← **特殊ケース処理**

**Rephraseルールの適用範囲**:
- パーサーが誤解析する特定構文
- 言語学的に複雑な省略構造
- 教育的観点からの分解が必要な構文

### 3. 安全性確保ガイドライン

**実装前チェック**:
- [ ] 既存テストケースへの影響確認
- [ ] パーサー出力の直接変更回避
- [ ] 新ルールの適用条件の厳密化
- [ ] フォールバック機能の実装

**テスト要件**:
- 新ルール追加時は既存全テストの回帰テスト必須
- 特殊ケースと通常ケースの両方でテスト

### 4. 具体的実装例

**Test26対応: 連続動詞構文**
```python
def _apply_consecutive_verb_rephrase_rule(self, result, sentence):
    """連続動詞パターンのRephraseルール
    
    対象: "The door opened slowly creaked loudly"
    意図: "The door [which] opened slowly creaked loudly"
    
    適用条件:
    - [名詞] [動詞1] [副詞] [動詞2] [副詞] パターン
    - 既存の関係節検出が失敗している場合のみ
    """
    # 安全性: 既存の関係節が検出されている場合はスキップ
    if result.get('sub_slots'):
        return result
        
    # パターン検出と変換処理
    # ...
```

## 🔧 実装チェックリスト

### 新ハンドラー追加時
- [ ] 既存パーサー出力を変更していないか
- [ ] 他のハンドラーとの競合がないか  
- [ ] 適用条件が十分に限定されているか
- [ ] フォールバック処理が実装されているか

### Rephraseルール追加時
- [ ] パーサー解析が失敗した場合のみ適用されるか
- [ ] 通常ケースに悪影響を与えないか
- [ ] 教育的価値があるか
- [ ] 保守性が確保されているか

## 📚 AI開発者向けガイド

**重要**: 新しい言語現象に対処する際は、必ずこの順序で検討せよ：

1. **既存ハンドラーの改善**で対応可能か？
2. **新ハンドラー**が必要か？
3. **Rephraseルール**での後処理が適切か？

**判断基準**:
- パーサーが正しく解析できる → 既存ハンドラー改善
- パーサーが一部誤解析 → 新ハンドラー
- パーサーが完全に誤解析 → Rephraseルール

この原則により、システムの安定性と拡張性を両立する。
