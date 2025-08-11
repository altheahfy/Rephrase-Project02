# Pure Stanza Engine v3 アーキテクチャ設計仕様書

## 1. 基本設計原則

### 1.1 ゼロハードコーディング原則
- **絶対禁止**: 特定の単語、フレーズ、文構造のハードコーディング
- **必須**: 文法的依存関係パターンに基づく汎用的処理
- **目標**: 未知の文にも対応可能な体系的アルゴリズム

### 1.2 Rephraseスロット設計
```
上位スロット (10個):
M1, S, Aux, V, O1, O2, C1, C2, M2, M3

サブスロット (各8個):
sub-s, sub-aux, sub-v, sub-o1, sub-o2, sub-c1, sub-m2, sub-m3

入れ子制限: 単一レベルのみ（二重入れ子は扱わない）
```

## 2. Stanza→Rephrase翻訳体系

### 2.1 基本文型マッピング

#### 第1文型 (SV): Subject + Verb
```
Stanza Pattern: nsubj -> root(VERB)
Rephrase Mapping: S -> V
Example: "Birds fly" → S: Birds, V: fly
```

#### 第2文型 (SVC): Subject + Verb + Complement  
```
Stanza Pattern: nsubj -> root(ADJ/NOUN) + cop
Rephrase Mapping: S -> V(be) -> C1
Example: "He is happy" → S: He, V: is, C1: happy
```

#### 第3文型 (SVO): Subject + Verb + Object
```
Stanza Pattern: nsubj -> root(VERB) -> obj
Rephrase Mapping: S -> V -> O1
Example: "I like you" → S: I, V: like, O1: you
```

#### 第4文型 (SVOO): Subject + Verb + Object + Object
```
Stanza Pattern: nsubj -> root(VERB) -> obj + iobj
Rephrase Mapping: S -> V -> O1 -> O2
Example: "I gave him a book" → S: I, V: gave, O1: him, O2: a book
```

#### 第5文型 (SVOC): Subject + Verb + Object + Complement
```
Stanza Pattern: nsubj -> root(VERB) -> obj -> xcomp
Rephrase Mapping: S -> V -> O1 -> C2
Example: "We made him happy" → S: We, V: made, O1: him, C2: happy
```

### 2.2 修飾語マッピング

#### 形容詞修飾語 (amod)
```
Stanza: amod -> NOUN
Rephrase: サブスロット内で処理
```

#### 副詞修飾語 (advmod)
```
Stanza: advmod -> VERB/ADJ
Rephrase: M2スロット
```

#### 前置詞句修飾語 (nmod)
```
Stanza: case + nmod -> NOUN
Rephrase: 文脈に応じてM1/M2/M3
```

#### 限定詞 (det)
```
Stanza: det -> NOUN
Rephrase: サブスロット内で処理
```

## 3. アーキテクチャ設計

### 3.1 処理フロー
```
入力文
↓
Stanza解析 (依存関係取得)
↓
文型パターン識別
↓
基本スロット配置
↓
修飾語スロット配置  
↓
サブスロット処理
↓
出力 (Rephraseスロット構造)
```

### 3.2 コア処理モジュール

#### Pattern Recognition Engine
```python
class PatternRecognitionEngine:
    def identify_sentence_type(self, sent, root_verb)
    def get_core_arguments(self, sent, root_verb) 
    def get_modifiers(self, sent, root_verb)
```

#### Slot Mapping Engine  
```python
class SlotMappingEngine:
    def map_to_basic_slots(self, pattern, core_args)
    def map_modifiers_to_slots(self, modifiers)
    def extract_subslots(self, slot_content)
```

#### Dependency Analysis Engine
```python
class DependencyAnalysisEngine:
    def get_dependency_tree(self, sent)
    def find_dependency_pattern(self, sent, target_relations)
    def get_subtree_range(self, sent, root_word)
```

### 3.3 設定駆動アーキテクチャ

#### 依存関係ルールセット (JSON設定)
```json
{
  "sentence_patterns": {
    "SV": {
      "core_relations": ["nsubj", "root"],
      "slot_mapping": {"nsubj": "S", "root": "V"}
    },
    "SVC_be": {
      "core_relations": ["nsubj", "cop", "root"],
      "slot_mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
    },
    "SVO": {
      "core_relations": ["nsubj", "root", "obj"],
      "slot_mapping": {"nsubj": "S", "root": "V", "obj": "O1"}
    }
  },
  "modifier_mapping": {
    "advmod": "M2",
    "amod": "subslot",
    "det": "subslot",
    "nmod": "context_dependent"
  }
}
```

## 4. 実装方針

### 4.1 段階的開発
1. **Phase 1**: 基本5文型の完全対応
2. **Phase 2**: 修飾語処理の体系化  
3. **Phase 3**: サブスロット処理の統合

### 4.2 品質保証
- **全文型パターンの網羅的テスト**
- **未知文への対応力検証**
- **ゼロハードコーディング原則の厳格遵守**

### 4.3 拡張性
- **新文型パターンの設定追加のみで対応**
- **アルゴリズム本体の変更不要**
- **言語学的知見の容易な反映**

## 5. 設計制約

### 5.1 技術制約
- Stanza NLP Pipeline依存
- 単一レベル入れ子制限
- 依存関係解析精度に依存

### 5.2 品質制約  
- ハードコーディング絶対禁止
- 体系的パターン処理必須
- 高い汎用性要求

## 6. 成功基準

### 6.1 機能要件
- [ ] 基本5文型100%対応
- [ ] 修飾語配置の正確性
- [ ] サブスロット処理の統一性

### 6.2 品質要件
- [ ] ゼロハードコーディング達成
- [ ] 未知文への適応能力
- [ ] 設定駆動による拡張性
