# Phase 1 実装手順書 - 緊急修正
**実行期間**: 2025年8月16日-8月17日  
**目標**: 90%精度達成

---

## 🔧 Task 1.1: 関係詞節主語抽出の修正

### 問題の詳細
```
Input: "The car which we saw was red"
Current: S:"we", V:"", C1:"red" ❌
Expected: S:"The car which we saw", V:"was", C1:"red" ✅
```

### 修正箇所
**ファイル**: `simple_unified_rephrase_integrator.py`  
**メソッド**: `_extract_basic_elements()`  
**行数**: 約130-150行目

### 具体的修正コード
```python
def _extract_basic_elements(self, doc) -> Dict[str, str]:
    # 現在のsubtree処理を改善
    if root_verb:
        for child in root_verb.children:
            if child.dep_ in ['nsubj', 'nsubjpass']:
                # 🚨 修正: which節の主語解釈エラー対応
                subject_tokens = list(child.subtree)
                
                # 🔧 追加: 関係詞節の正しい範囲検出
                if any(token.text.lower() in ['which', 'that', 'who'] for token in subject_tokens):
                    # 関係詞節を含む完全な主語を構築
                    full_subject = self._build_complete_subject_with_relative(child, doc)
                    slots['S'] = full_subject
                else:
                    # 通常の主語処理
                    subject_tokens.sort(key=lambda x: x.i)
                    slots['S'] = ' '.join([token.text for token in subject_tokens])
```

### テスト方法
```python
# 修正後のテスト
test_cases = [
    "The car which we saw was red",
    "The book that I bought is good", 
    "The person who called me was John"
]
# 期待結果: すべてで正しい主語抽出
```

---

## 🔧 Task 1.2: 使役動詞"had"の検出追加

### 問題の詳細
```
Input: "He had me clean the room"
Current: S:"He", V:"had", O1:"the room" (使役動詞として未検出) ❌
Expected: 使役動詞構文として検出、適切なサブスロット分解 ✅
```

### 修正箇所
**ファイル**: `simple_unified_rephrase_integrator.py`  
**メソッド**: `_process_causative_construction()`

### 具体的修正コード
```python
def _has_causative_verb(self, doc) -> Optional[any]:
    causative_lemmas = ['make', 'let', 'have', 'help', 'get', 'force', 'cause']
    
    for token in doc:
        # 🔧 修正: "had"の特別処理追加
        if token.lemma_ in causative_lemmas:
            # "have"の場合は文脈確認
            if token.lemma_ == 'have':
                if self._is_causative_have_construction(token, doc):
                    return token
            else:
                return token
    return None

def _is_causative_have_construction(self, have_token, doc):
    """使役動詞のhave構文判定"""
    # 1. have + 人 + 動詞原形パターン
    # 2. 所有のhaveと区別
    for child in have_token.children:
        if child.dep_ == 'dobj':  # 目的語（人）
            for grandchild in child.children:
                if grandchild.pos_ == 'VERB' and grandchild.dep_ in ['xcomp', 'ccomp']:
                    return True
    return False
```

### テスト方法
```python
test_cases = [
    "He had me clean the room",  # 使役動詞
    "I had a car",  # 所有動詞（区別すること）
    "She made him study"  # 既存動作確認
]
```

---

## 🔧 Task 1.3: 時間・条件節のサブスロット分解強化

### 問題の詳細
```
Input: "When I arrived, he was sleeping"
Current: M1:"When", sub_slots:{} (サブスロット分解なし) ❌  
Expected: M1サブスロット に sub_M1:"When", sub_S:"I", sub_V:"arrived" ✅
```

### 修正箇所
**ファイル**: `sub_slot_decomposer.py`  
**メソッド**: `_decompose_adverbial_clause()`

### 具体的修正コード
```python
def _decompose_adverbial_clause(self, text: str) -> SubSlotResult:
    if not text.strip():
        return SubSlotResult("adverbial_clause", text, {}, 0.9)
    
    # 🔧 修正: 時間・条件節の詳細分解追加
    temporal_markers = ['when', 'while', 'before', 'after', 'since', 'until']
    conditional_markers = ['if', 'unless', 'as long as', 'provided that']
    
    # マーカー検出
    doc = self.nlp(text)
    marker_token = None
    
    for token in doc:
        if token.text.lower() in temporal_markers + conditional_markers:
            marker_token = token
            break
    
    if marker_token:
        # 🚨 追加: マーカー以降の部分を詳細分解
        remaining_text = text[marker_token.idx + len(marker_token.text):].strip()
        if remaining_text:
            # 簡易SVO分解
            sub_slots = self._simple_svo_decomposition(remaining_text)
            sub_slots['sub_M1'] = marker_token.text
            
            return SubSlotResult("adverbial_clause", text, sub_slots, 0.95)
    
    return SubSlotResult("adverbial_clause", text, {}, 0.9)

def _simple_svo_decomposition(self, text: str) -> Dict[str, str]:
    """簡易SVO分解"""
    doc = self.nlp(text)
    result = {}
    
    for token in doc:
        if token.dep_ in ['nsubj', 'nsubjpass']:
            result['sub_S'] = token.text
        elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
            result['sub_V'] = token.text
        elif token.dep_ in ['dobj', 'attr', 'acomp']:
            if 'sub_O1' not in result:
                result['sub_O1'] = token.text
    
    return result
```

---

## 📊 Phase 1 完了検証

### 検証スクリプト実行
```bash
python honest_system_evaluation.py
```

### 成功基準
- **全体精度**: 90%以上
- **関係詞節**: 100%正確
- **使役動詞**: 95%以上
- **時間・条件節**: 90%以上

### 問題発生時の対処
1. **個別テスト作成**: 問題ケースの詳細分析
2. **spaCy解析確認**: `debug_dependency.py`で構造確認
3. **段階的修正**: 小さな変更で影響範囲限定

---

## 📝 Phase 1 完了報告テンプレート

```markdown
## Phase 1 完了報告
**実行日**: 2025年8月XX日
**作業時間**: XX時間

### 修正内容
- [ ] Task 1.1: 関係詞節主語抽出修正
- [ ] Task 1.2: 使役動詞"had"検出追加  
- [ ] Task 1.3: 時間・条件節サブスロット強化

### 精度測定結果
- 全体精度: XX% (目標90%)
- 関係詞節: XX% (目標100%)
- 使役動詞: XX% (目標95%)

### 発見した追加課題
- [ ] 課題1: 詳細
- [ ] 課題2: 詳細

### Phase 2 準備状況
- [ ] 準備完了 / [ ] 追加作業必要
```

---

*Phase 1完了後、Phase 2の詳細手順書を作成します。*
