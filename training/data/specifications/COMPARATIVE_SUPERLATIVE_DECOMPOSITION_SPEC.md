# 比較級・最上級エンジン 分解パターン設計仕様書

## 📋 実装予定概要

**エンジン名**: Comparative/Superlative Engine  
**実装日**: 2025年8月12日  
**統合アーキテクチャ**: Phase 2 高頻度構文パターン  
**処理対象**: 比較級・最上級構文の上位+サブスロット二重分解  

---

## 🎯 分解パターン詳細予定

### 1. 比較級パターン (Comparative)

#### **A. 形容詞比較級**
```
入力: "This book is more interesting than that one."
予定分解:
├── 上位スロット (独立文用)
│   ├── S: "This book"
│   ├── V: "is" 
│   ├── C1: "more interesting"
│   └── M2: "than that one"
├── サブスロット (従属節用) ※同じ基本構造を維持
│   ├── sub-s: "This book"
│   ├── sub-v: "is"
│   ├── sub-c1: "more interesting"
│   └── sub-m2: "than that one"
└── 比較構造メタ情報
    ├── comparison_type: "adjective_comparative"
    ├── base_form: "interesting"
    ├── comparative_form: "more interesting"
    └── comparison_object: "that one"
```

#### **B. 副詞比較級**
```
入力: "She runs faster than him."
予定分解:
├── 上位スロット
│   ├── S: "She"
│   ├── V: "runs"
│   ├── M1: "faster"
│   └── M2: "than him"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "She"
│   ├── sub-v: "runs" 
│   ├── sub-m1: "faster"
│   └── sub-m2: "than him"
└── 比較構造メタ情報
    ├── comparison_type: "adverb_comparative"
    ├── base_form: "fast"
    ├── comparative_form: "faster"
    └── comparison_object: "him"
```

#### **C. 数量比較級**
```
入力: "I have more money than you."
予定分解:
├── 上位スロット
│   ├── S: "I"
│   ├── V: "have"
│   ├── O1: "more money"
│   └── M2: "than you"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "I"
│   ├── sub-v: "have"
│   ├── sub-o1: "more money"
│   └── sub-m2: "than you"
└── 比較構造メタ情報
    ├── comparison_type: "quantity_comparative"
    ├── quantity_word: "more"
    ├── base_noun: "money"
    └── comparison_object: "you"
```

### 2. 最上級パターン (Superlative)

#### **A. 形容詞最上級**
```
入力: "This is the most beautiful flower in the garden."
予定分解:
├── 上位スロット
│   ├── S: "This"
│   ├── V: "is"
│   ├── C1: "the most beautiful flower"
│   └── M2: "in the garden"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "This"
│   ├── sub-v: "is"
│   ├── sub-c1: "the most beautiful flower"
│   └── sub-m2: "in the garden"
└── 最上級構造メタ情報
    ├── superlative_type: "adjective_superlative"
    ├── base_form: "beautiful"
    ├── superlative_form: "most beautiful"
    ├── noun: "flower"
    └── scope: "in the garden"
```

#### **B. 副詞最上級**
```
入力: "She speaks English most fluently among all students."
予定分解:
├── 上位スロット
│   ├── S: "She"
│   ├── V: "speaks"
│   ├── O1: "English"
│   ├── M1: "most fluently"
│   └── M2: "among all students"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "She"
│   ├── sub-v: "speaks"
│   ├── sub-o1: "English"
│   ├── sub-m1: "most fluently"
│   └── sub-m2: "among all students"
└── 最上級構造メタ情報
    ├── superlative_type: "adverb_superlative"
    ├── base_form: "fluent"
    ├── superlative_form: "most fluently"
    └── scope: "among all students"
```

### 3. 特殊比較構文

#### **A. as...as構文 (同等比較)**
```
入力: "He is as tall as his brother."
予定分解:
├── 上位スロット
│   ├── S: "He"
│   ├── V: "is"
│   ├── C1: "as tall"
│   └── M2: "as his brother"
├── サブスロット ※同じ基本構造を維持
│   ├── sub-s: "He"
│   ├── sub-v: "is"
│   ├── sub-c1: "as tall"
│   └── sub-m2: "as his brother"
└── 同等比較メタ情報
    ├── comparison_type: "equal_comparison"
    ├── adjective: "tall"
    └── comparison_object: "his brother"
```

#### **B. the...the構文 (比例比較)**
```
入力: "The harder you work, the more successful you become."
予定分解:
├── 上位スロット ※Rephraseは3重入れ子を扱わないため、これがサブスロットに入ることはない
│   ├── M1: "The harder you work"
│   ├── M2: "the more"
│   ├── C1: "successful"
│   ├── S: "you"
│   └── V: "become"
├── M1内部のサブスロット分解 ("The harder you work")
│   ├── sub-m1: "the harder"
│   ├── sub-s: "you"
│   └── sub-v: "work"
└── 比例比較メタ情報
    ├── comparison_type: "proportional_comparison"
    ├── condition_clause: "The harder you work"
    ├── result_clause: "the more successful you become"
    ├── comparative1: "harder"
    └── comparative2: "more successful"
```

---

## 🔧 技術実装予定

### Stanza依存関係分析パターン

#### **比較級検出パターン**
```python
# 想定される依存関係ラベル
- amod: 形容詞修飾 ("more interesting book")
- advmod: 副詞修飾 ("runs faster")
- mark: 比較接続詞 ("than")
- nmod: 比較対象 ("than him")
- det: 限定詞 ("the most")
```

#### **最上級検出パターン**  
```python
# 想定される依存関係ラベル
- det: 定冠詞 ("the")
- amod: 最上級形容詞 ("most beautiful")  
- nmod: 範囲句 ("in the garden")
- case: 前置詞 ("in", "among", "of")
```

### エンジン処理フロー予定

```python
class ComparativeSuperlativeEngine:
    def process(self, sentence):
        # 1. 比較構文検出
        comparative_info = self._detect_comparative_structure(sentence)
        
        # 2. パターン分類
        if comparative_info['type'] == 'comparative':
            return self._process_comparative(sentence, comparative_info)
        elif comparative_info['type'] == 'superlative':
            return self._process_superlative(sentence, comparative_info)
        elif comparative_info['type'] == 'equal':
            return self._process_equal_comparison(sentence, comparative_info)
        
        # 3. 統合アーキテクチャ分解
        return self._unified_decomposition(sentence, comparative_info)
    
    def process_as_subslot(self, sentence):
        # 従属節内比較構文のサブスロット専用処理
        return self._process_comparative_as_subslot(sentence)
```

---

## 🎯 実装優先順位

### **Phase 1: 基本比較構文**
1. 形容詞比較級 (`more/er + than`)
2. 形容詞最上級 (`most/est`)
3. 副詞比較級・最上級

### **Phase 2: 特殊比較構文**  
4. as...as構文 (同等比較)
5. 数量比較 (more/less)
6. the...the構文 (比例比較)

### **Phase 3: 複合比較構文**
7. 比較級 + 関係詞節
8. 比較級 + 分詞構文  
9. 比較級 + 不定詞句

---

## 📊 期待される処理結果例

### **統合例: 複合比較構文**
```
完全文: "Because this method is more efficient than the traditional approach, we should adopt it."

従属節処理:
├── Conjunction Engine → M1: "Because this method is more efficient than the traditional approach"
└── Comparative Engine (サブスロット処理):
    ├── sub-s: "this method"
    ├── sub-v: "is" 
    ├── sub-c1: "more efficient"
    └── sub-m2: "than the traditional approach"

最終統合結果:
├── M1: "Because this method is more efficient than the traditional approach" (上位)
├── S: "we", V: "should adopt", O1: "it" (主節)
└── sub-s: "this method", sub-c1: "more efficient", sub-m2: "than the traditional approach" (サブ)
```

この詳細な分解パターン予定に基づいて、比較級・最上級エンジンの実装を開始しますか？
