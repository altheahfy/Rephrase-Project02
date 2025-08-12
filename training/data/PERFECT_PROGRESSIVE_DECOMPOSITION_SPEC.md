# 完了進行形エンジン 分解パターン設計仕様書

## 📋 実装予定概要

**エンジン名**: Perfect Progressive Engine  
**実装日**: 2025年8月12日  
**統合アーキテクチャ**: Phase 2 高頻度構文パターン  
**処理対象**: 完了進行形構文の上位+サブスロット二重分解  

---

## 🎯 分解パターン詳細予定

### 1. 現在完了進行形 (Present Perfect Progressive)

#### **A. 基本現在完了進行形**
```
入力: "I have been working here for three years."
予定分解:
├── 上位スロット (独立文用)
│   ├── S: "I"
│   ├── V: "working"
│   ├── Aux: "have been"
│   ├── M1: "here"
│   └── M2: "for three years"
├── サブスロット (従属節用) ※同じ基本構造を維持
│   ├── sub-s: "I"
│   ├── sub-v: "working"
│   ├── sub-aux: "have been"
│   ├── sub-m1: "here"
│   └── sub-m2: "for three years"
└── 完了進行形メタ情報
    ├── tense_type: "present_perfect_progressive"
    ├── auxiliary: "have been"
    ├── main_verb: "working"
    ├── duration: "for three years"
    └── location: "here"
```

#### **B. 疑問文完了進行形**
```
入力: "How long have you been studying English?"
予定分解:
├── 上位スロット
│   ├── M1: "How long"
│   ├── Aux: "have been"
│   ├── S: "you"
│   ├── V: "studying"
│   └── O1: "English"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-m1: "How long"
│   ├── sub-aux: "have been"
│   ├── sub-s: "you"
│   ├── sub-v: "studying"
│   └── sub-o1: "English"
└── 完了進行形メタ情報
    ├── tense_type: "present_perfect_progressive"
    ├── sentence_type: "interrogative"
    ├── wh_word: "How long"
    └── auxiliary: "have been"
```

### 2. 過去完了進行形 (Past Perfect Progressive)

#### **A. 基本過去完了進行形**
```
入力: "She had been waiting for an hour when I arrived."
予定分解:
├── 上位スロット
│   ├── S: "She"
│   ├── Aux: "had been"
│   ├── V: "waiting"
│   ├── M1: "for an hour"
│   └── M2: "when I arrived"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "She"
│   ├── sub-aux: "had been"
│   ├── sub-v: "waiting"
│   ├── sub-m1: "for an hour"
│   └── sub-m2: "when I arrived"
└── 完了進行形メタ情報
    ├── tense_type: "past_perfect_progressive"
    ├── auxiliary: "had been"
    ├── duration: "for an hour"
    └── time_clause: "when I arrived"
```

#### **B. 理由・結果表現**
```
入力: "He was tired because he had been running all morning."
予定分解:
├── 上位スロット
│   ├── S: "He"
│   ├── V: "was"
│   ├── C1: "tired"
│   └── M1: "because he had been running all morning"
├── M1内部のサブスロット分解 ("he had been running all morning")
│   ├── sub-s: "he"
│   ├── sub-aux: "had been"
│   ├── sub-v: "running"
│   └── sub-m1: "all morning"
└── 完了進行形メタ情報
    ├── tense_type: "past_perfect_progressive"
    ├── context: "causal_relationship"
    └── duration: "all morning"
```

### 3. 未来完了進行形 (Future Perfect Progressive)

#### **A. 基本未来完了進行形**
```
入力: "By next year, I will have been living here for five years."
予定分解:
├── 上位スロット
│   ├── M1: "By next year"
│   ├── S: "I"
│   ├── Aux: "will have been"
│   ├── V: "living"
│   ├── M2: "here"
│   └── M3: "for five years"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-m1: "By next year"
│   ├── sub-s: "I"
│   ├── sub-aux: "will have been"
│   ├── sub-v: "living"
│   ├── sub-m2: "here"
│   └── sub-m3: "for five years"
└── 完了進行形メタ情報
    ├── tense_type: "future_perfect_progressive"
    ├── auxiliary: "will have been"
    ├── time_reference: "By next year"
    ├── duration: "for five years"
    └── location: "here"
```

### 4. 特殊完了進行形構文

#### **A. 受動完了進行形**
```
入力: "The project has been being developed since January."
予定分解:
├── 上位スロット
│   ├── S: "The project"
│   ├── Aux: "has been being"
│   ├── V: "developed"
│   └── M1: "since January"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "The project"
│   ├── sub-aux: "has been being"
│   ├── sub-v: "developed"
│   └── sub-m1: "since January"
└── 完了進行形メタ情報
    ├── tense_type: "present_perfect_progressive_passive"
    ├── auxiliary: "has been being"
    ├── voice: "passive"
    └── time_reference: "since January"
```

#### **B. 条件文内完了進行形**
```
入力: "If I had been studying harder, I would have passed the exam."
予定分解:
├── 上位スロット ※Rephraseは3重入れ子を扱わないため、これがサブスロットに入ることはない
│   ├── M1: "If I had been studying harder"
│   ├── S: "I"
│   ├── Aux: "would have"
│   ├── V: "passed"
│   └── O1: "the exam"
├── M1内部のサブスロット分解 ("I had been studying harder")
│   ├── sub-s: "I"
│   ├── sub-aux: "had been"
│   ├── sub-v: "studying"
│   └── sub-m1: "harder"
└── 完了進行形メタ情報
    ├── tense_type: "past_perfect_progressive_conditional"
    ├── sentence_type: "conditional"
    ├── condition_auxiliary: "had been"
    └── result_auxiliary: "would have"
```

---

## 🔧 技術実装予定

### Stanza依存関係分析パターン

#### **完了進行形検出パターン**
```python
# 想定される依存関係ラベル
- aux: 助動詞 ("have", "had", "will")
- aux:pass: 受動助動詞 ("been")  
- root: 主動詞 (現在分詞 "-ing")
- nsubj: 主語
- advmod: 副詞修飾 ("already", "just", "still")
- obl:tmod: 時間表現 ("for three years", "since January")
```

#### **助動詞連鎖パターン**
```python
# 完了進行形の助動詞パターン
present_perfect_progressive: "have/has + been + Ving"
past_perfect_progressive: "had + been + Ving"  
future_perfect_progressive: "will + have + been + Ving"
passive_perfect_progressive: "have/has + been + being + Ved"
```

### エンジン処理フロー予定

```python
class PerfectProgressiveEngine:
    def process(self, sentence):
        # 1. 完了進行形構文検出
        perfect_progressive_info = self._detect_perfect_progressive_structure(sentence)
        
        # 2. 時制分類
        if perfect_progressive_info['tense'] == 'present_perfect_progressive':
            return self._process_present_perfect_progressive(sentence, perfect_progressive_info)
        elif perfect_progressive_info['tense'] == 'past_perfect_progressive':
            return self._process_past_perfect_progressive(sentence, perfect_progressive_info)
        elif perfect_progressive_info['tense'] == 'future_perfect_progressive':
            return self._process_future_perfect_progressive(sentence, perfect_progressive_info)
        
        # 3. 統合アーキテクチャ分解
        return self._unified_decomposition(sentence, perfect_progressive_info)
    
    def process_as_subslot(self, sentence):
        # 従属節内完了進行形のサブスロット専用処理
        return self._process_perfect_progressive_as_subslot(sentence)
```

---

## 🎯 実装優先順位

### **Phase 1: 基本完了進行形**
1. 現在完了進行形 (`have/has been + Ving`)
2. 過去完了進行形 (`had been + Ving`) 
3. 未来完了進行形 (`will have been + Ving`)

### **Phase 2: 特殊完了進行形**
4. 疑問文完了進行形 (`How long have you been...?`)
5. 受動完了進行形 (`has been being + Ved`)
6. 否定完了進行形 (`haven't been + Ving`)

### **Phase 3: 複合完了進行形**
7. 条件文内完了進行形
8. 関係詞節内完了進行形
9. 接続詞節内完了進行形

---

## 📊 期待される処理結果例

### **統合例: 接続詞 + 完了進行形**
```
完全文: "Because I have been working here for three years, I understand the company culture well."

従属節処理:
├── Conjunction Engine → M1: "Because I have been working here for three years"
└── Perfect Progressive Engine (サブスロット処理):
    ├── sub-s: "I"
    ├── sub-aux: "have been"
    ├── sub-v: "working"
    ├── sub-m1: "here"
    └── sub-m2: "for three years"

最終統合結果:
├── M1: "Because I have been working here for three years" (上位)
├── S: "I", V: "understand", O1: "the company culture", M1: "well" (主節)
└── sub-s: "I", sub-aux: "have been", sub-v: "working", sub-m1: "here", sub-m2: "for three years" (サブ)
```

この詳細な分解パターン予定に基づいて、完了進行形エンジンの実装を開始しますか？
