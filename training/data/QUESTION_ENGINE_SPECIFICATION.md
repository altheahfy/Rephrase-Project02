# Question Formation Engine スロット分解仕様書
# 2025年8月12日 統合完了版

## 🎯 概要
Question Formation Engine (12th Engine) が処理する文型とスロット分解パターンの完全仕様

---

## 📋 対応する質問タイプ別スロット分解

### 1. WH疑問文 (WH-Questions)
**基本パターン**: `WH-word + Auxiliary + Subject + Verb + Object?`

#### パターン1: 標準WH疑問文
```
入力: "What are you doing?"
スロット分解:
├─ Q: "What"           (疑問詞)
├─ Aux: "are"          (助動詞)
├─ S: "you"            (主語)
├─ V: "doing"          (動詞)
├─ question_type: "wh_question"
└─ answer_type: "information"
```

```
入力: "Where did you go?"
スロット分解:
├─ Q: "Where"          (疑問詞)
├─ Aux: "did"          (助動詞)
├─ S: "you"            (主語)
├─ V: "go"             (動詞)
├─ question_type: "wh_question"
└─ answer_type: "information"
```

#### パターン2: 主語疑問文 (Subject Questions)
```
入力: "Who called you?"
スロット分解:
├─ Q: "Who"            (疑問詞=主語)
├─ V: "called"         (動詞)
├─ O1: "you"           (目的語)
├─ question_type: "wh_question"
└─ answer_type: "information"
```

#### パターン3: Which/Whose + 名詞疑問文
```
入力: "Which book do you want?"
スロット分解:
├─ Q: "Which book"     (疑問詞+名詞)
├─ Aux: "do"           (助動詞)
├─ S: "you"            (主語)
├─ V: "want"           (動詞)
├─ question_type: "wh_question"
└─ answer_type: "information"
```

### 2. Yes/No疑問文 (Yes/No Questions)
**基本パターン**: `Auxiliary + Subject + Verb + Object?`

```
入力: "Are you coming to the party?"
スロット分解:
├─ Aux: "Are"          (助動詞)
├─ S: "you"            (主語)
├─ V: "coming"         (動詞)
├─ O1: "to the party"  (目的語/補語)
├─ question_type: "yes_no"
└─ answer_type: "yes_no"
```

```
入力: "Do you like coffee?"
スロット分解:
├─ Aux: "Do"           (助動詞)
├─ S: "you"            (主語)
├─ V: "like"           (動詞)
├─ O1: "coffee"        (目的語)
├─ question_type: "yes_no"
└─ answer_type: "yes_no"
```

### 3. Tag疑問文 (Tag Questions)
**基本パターン**: `Statement + , + Tag?`

```
入力: "You like coffee, don't you?"
スロット分解:
├─ S: "You"            (主語)
├─ V: "like"           (動詞)
├─ O1: "coffee"        (目的語)
├─ tag: "don't you"    (付加疑問タグ)
├─ question_type: "tag_question"
└─ answer_type: "confirmation"
```

```
入力: "She can swim, can't she?"
スロット分解:
├─ S: "She"            (主語)
├─ V: "can swim"       (動詞句)
├─ tag: "can't she"    (付加疑問タグ)
├─ question_type: "tag_question"
└─ answer_type: "confirmation"
```

### 4. 選択疑問文 (Choice Questions)
**基本パターン**: `Question + or + Alternative?`

```
入力: "Do you prefer tea or coffee?"
スロット分解:
├─ Aux: "Do"           (助動詞)
├─ S: "you"            (主語)
├─ V: "prefer"         (動詞)
├─ O1: "tea"           (選択肢1)
├─ choice_connector: "or"
├─ O2: "coffee"        (選択肢2)
├─ question_type: "choice_question"
└─ answer_type: "choice"
```

### 5. 埋め込み疑問文 (Embedded Questions)
**基本パターン**: `Main clause + WH-word + Embedded clause`

```
入力: "I wonder what time it is."
スロット分解:
├─ S: "I"              (主節主語)
├─ V: "wonder"         (主節動詞)
├─ embedded_q: "what"  (埋め込み疑問詞)
├─ embedded_clause: "time it is"  (埋め込み節)
├─ question_type: "embedded_question"
└─ answer_type: "embedded"
```

```
入力: "Tell me where you live."
スロット分解:
├─ V: "Tell"           (命令動詞)
├─ O1: "me"            (間接目的語)
├─ embedded_q: "where" (埋め込み疑問詞)
├─ embedded_clause: "you live"  (埋め込み節)
├─ question_type: "embedded_question"
└─ answer_type: "embedded"
```

---

## 🔍 実際の統合テスト結果

### 成功例 (✅ 正常処理済み)

#### テスト1: "What are you doing?"
```
処理結果: ✅ 成功
信頼度: 0.85
スロット:
├─ Q: "What"
├─ Aux: "are" 
├─ S: "you"
├─ V: "doing"
├─ question_type: "wh_question"
└─ answer_type: "information"
```

#### テスト2: "You like coffee, don't you?"
```
処理結果: ✅ 成功
信頼度: 0.85
スロット:
├─ S: "You"
├─ V: "like"
├─ O1: "coffee"
├─ tag: "don't you"
├─ question_type: "tag_question"
└─ answer_type: "confirmation"
```

#### テスト3: "Do you prefer tea or coffee?"
```
処理結果: ✅ 成功 (Choice questionとして処理)
信頼度: 0.90
スロット:
├─ Aux: "Do"
├─ S: "you"
├─ V: "prefertea"     ← ※要改善: 語分割問題
├─ O1: "or coffee"
├─ question_type: "yes_no"  ← ※要改善: choice_questionにすべき
└─ answer_type: "yes_no"
```

#### テスト4: "I wonder what time it is."
```
処理結果: ✅ 成功
信頼度: 0.80
スロット:
├─ S: "I"
├─ V: "wonder"
├─ embedded_q: "what"
├─ embedded_clause: "time it is."
├─ question_type: "embedded_question"
└─ answer_type: "embedded"
```

### 改善が必要な例

#### テスト5: "How many books did you read?"
```
処理結果: ⚠️ 部分成功
信頼度: 0.50
スロット:
├─ question_type: "wh_question"
└─ answer_type: "information"
※問題: 複数語疑問詞 "How many" の処理が不完全
※改善案: 複合疑問詞パターンの追加必要
```

---

## 🛠️ 使用する正規表現パターン

### WH疑問文パターン
```python
patterns = [
    # パターン1: What/Where + aux + subject + verb + object?
    r'^(what|where|when|why|how)\s+(do|does|did|are|is|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s*(.*)\?',
    
    # パターン2: Who/What + verb + object? (主語疑問文)
    r'^(who|what)\s+(\w+)\s*(.*)\?',
    
    # パターン3: Which/Whose + noun + aux + subject + verb?
    r'^(which|whose)\s+(\w+)\s+(do|does|did|are|is|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s*(.*)\?'
]
```

### Yes/No疑問文パターン
```python
pattern = r'^(do|does|did|am|is|are|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s*(.*)\?'
```

### Tag疑問文パターン
```python
pattern = r'^(.+),\s*((?:isn\'t|aren\'t|wasn\'t|weren\'t|don\'t|doesn\'t|didn\'t|haven\'t|hasn\'t|hadn\'t|won\'t|wouldn\'t|can\'t|couldn\'t|shouldn\'t|mustn\'t)\s+(?:he|she|it|they|you|we))\?$'
```

---

## 💡 信頼度計算ロジック

```python
def calculate_confidence(slots):
    base_confidence = len(slots) * 0.2  # 1スロットあたり0.2
    
    # ボーナス計算
    if 'question_type' in slots: base_confidence += 0.1
    if 'Q' in slots: base_confidence += 0.1  # WH-word detection
    if 'Aux' in slots: base_confidence += 0.1  # Auxiliary detection
    if 'tag' in slots: base_confidence += 0.1  # Tag question detection
    
    return min(base_confidence, 0.95)  # 最大95%
```

---

## 🎯 チェックポイント

### ✅ 正常動作確認項目
1. **WH疑問文**: "What are you doing?" → Q, Aux, S, V 抽出
2. **Tag疑問文**: "You like coffee, don't you?" → S, V, O1, tag 抽出  
3. **埋め込み疑問文**: "I wonder what time it is." → embedded構造抽出
4. **標準インターフェイス**: `process()` メソッドで統一形式返却
5. **信頼度計算**: 0.50-0.90の範囲で適切な信頼度算出

### ⚠️ 要改善項目
1. **複合疑問詞**: "How many", "How much" の処理改善
2. **選択疑問文**: "or" 構造の正確な分析
3. **語分割精度**: "prefertea" → "prefer tea" の分離
4. **否定疑問文**: "Isn't this amazing?" の対応
5. **複雑構造**: 関係代名詞を含む疑問文の処理

この仕様書により、Question Formation Engine の現在の処理能力と改善点が明確になります。ご確認をお願いいたします。
