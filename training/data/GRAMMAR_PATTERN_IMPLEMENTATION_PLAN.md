# 文法パターン実装計画 2025-08-12

## ✅ **実装済みパターン**

### 1. 関係代名詞 (`simple_relative_engine.py`)
- **objective**: "The book that he bought" → sub-o1:"The book that", sub-s:"he", sub-v:"bought"
- **subjective**: "The man who came" → sub-s:"The man who", sub-v:"came"
- **possessive**: "The girl whose book" → sub-s1:"The girl whose", sub-o1:"book"
- **relative adverbs**: "when", "where", "why", "how"
- **prepositional + relative**: "The house in which he lives"

### 2. 従属接続詞 (`stanza_based_conjunction_engine.py`)
- **理由**: "Because he is tired" → sub-m1:"because", sub-s:"he", sub-aux:"is", sub-c1:"tired"
- **条件**: "If you come" → sub-m1:"if", sub-s:"you", sub-v:"come"
- **時間**: "When he arrived" → sub-m3:"when", sub-s:"he", sub-v:"arrived"
- **譲歩**: "Although she tried" → sub-m2:"although", sub-s:"she", sub-v:"tried"

### 3. 分詞構文 (`participle_engine.py`) ✅ **NEW**
- **Present participle**: "Running fast, he won" → sub-v:"running", sub-m1:"fast", s:"he", v:"won"
- **Past participle**: "Tired from work, she slept" → sub-v:"tired", sub-m1:"from work", s:"she", v:"slept"
- **Perfect participle**: "Having finished homework, he went to bed" → sub-aux:"having", sub-v:"finished", sub-o1:"homework", s:"he", v:"went", m1:"to bed"

### 4. 不定詞構文 (`infinitive_engine.py`) ✅ **NEW**
- **Subject infinitive**: "To swim is fun" → sub-v:"to swim", c1:"fun", aux:"is"
- **Object infinitive**: "He wants to go" → s:"he", v:"wants", sub-v:"to go"
- **Complex object**: "I want him to come" → s:"I", v:"want", o1:"him", sub-v:"to come"
- **Adverbial purpose**: "He came to help" → s:"he", v:"came", sub-v:"to help"
- **Adjectival modifier**: "She has nothing to do" → s:"she", v:"has", o1:"nothing to do", sub-v:"to do"

### 5. 統合エンジン (`pure_stanza_engine_v3_1_unified.py`)
- 複数パターンの統合処理

## 🎯 **次に実装すべきパターン**

### 優先度 A（高頻度・重要）
1. **動名詞構文 (Gerund Constructions)** ← **次の実装対象**
   - Subject: "Swimming is fun" → s:"swimming", aux:"is", c1:"fun"
   - Object: "I enjoy swimming" → s:"I", v:"enjoy", o1:"swimming"
   - Preposition object: "He is good at swimming" → s:"he", aux:"is", c1:"good", sub-m1:"at swimming"

2. **受動態構文 (Passive Voice Constructions)**
   - Simple passive: "The book was read" → s:"the book", aux:"was", v:"read"
   - Passive with agent: "The book was read by him" → s:"the book", aux:"was", v:"read", sub-m1:"by him"

3. **比較構文 (Comparative Constructions)**
   - Comparative: "He is taller than she is" → s:"he", aux:"is", c1:"taller", sub-m2:"than she is"
   - Superlative: "He is the tallest in class" → s:"he", aux:"is", c1:"the tallest", m1:"in class"

### 優先度 B（中頻度）
4. **倒置構文 (Inversion Constructions)**
   - Negative inversion: "Never have I seen" → m1:"never", aux:"have", s:"I", v:"seen"
   - Question inversion: "Are you ready?" → aux:"are", s:"you", c1:"ready"

5. **完了進行形構文 (Perfect Progressive Constructions)**
   - Present perfect progressive: "He has been working" → s:"he", aux:"has been", v:"working"
   - Past perfect progressive: "He had been working" → s:"he", aux:"had been", v:"working"

### 優先度 C（低頻度・専門的）
6. **仮定法構文 (Subjunctive/Conditional)**
   - If-clause: "If I were you" → sub-m1:"if", sub-s:"I", sub-aux:"were", sub-o1:"you"
   - Wish-clause: "I wish I were rich" → s:"I", v:"wish", sub-s:"I", sub-aux:"were", sub-c1:"rich"

7. **強調構文 (Emphatic Constructions)**
   - It-cleft: "It is John who came" → s:"It", aux:"is", c1:"John", sub-s:"who", sub-v:"came"
   - What-cleft: "What I need is help" → sub-s:"What", sub-s:"I", sub-v:"need", aux:"is", c1:"help"

## 🚀 **実装方針**

### アプローチ
1. **Pattern-by-Pattern**: 1つずつ完璧に実装
2. **Stanza-Based**: 依存構造解析を最大活用
3. **Modular**: 独立エンジンとして実装後、統合

### 技術的考慮事項
- Stanzaの`xcomp`, `acl`, `nmod`関係の活用
- 分詞の`VBG`, `VBN`品詞タグ活用
- 不定詞の`mark`関係（"to"）の処理
- 動名詞とing動詞の区別

## 📋 **次のアクション**
次に**動名詞構文エンジン**の実装を提案。

### 実装アプローチ
1. **Stanza分析**: 動名詞の`VBG`品詞と`nsubj`, `dobj`依存関係
2. **分詞との区別**: 文法的役割による判定（主語・目的語・前置詞の目的語）
3. **Rephraseルール準拠**: 動名詞句の適切なスロット配置

---
作成日: 2025年8月12日（最終更新）  
担当: GitHub Copilot
