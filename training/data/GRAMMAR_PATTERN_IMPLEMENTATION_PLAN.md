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

### 3. 統合エンジン (`pure_stanza_engine_v3_1_unified.py`)
- 複数パターンの統合処理

## 🎯 **次に実装すべきパターン**

### 優先度 A（高頻度・重要）
1. **分詞構文 (Participial Constructions)**
   - Present participle: "Running fast, he won" → sub-m1:"running fast", s:"he", v:"won"
   - Past participle: "Tired from work, she slept" → sub-m1:"tired from work", s:"she", v:"slept"
   
2. **不定詞構文 (Infinitive Constructions)**
   - Purpose: "He came to help" → s:"he", v:"came", sub-m1:"to help"
   - Subject: "To swim is fun" → sub-s:"to swim", aux:"is", c1:"fun"
   
3. **動名詞構文 (Gerund Constructions)**
   - Subject: "Swimming is fun" → s:"swimming", aux:"is", c1:"fun"
   - Object: "I enjoy swimming" → s:"I", v:"enjoy", o1:"swimming"

### 優先度 B（中頻度）
4. **比較構文 (Comparative Constructions)**
   - Comparative: "He is taller than she is" → s:"he", aux:"is", c1:"taller", sub-m2:"than she is"
   - Superlative: "He is the tallest in class" → s:"he", aux:"is", c1:"the tallest", m1:"in class"

5. **倒置構文 (Inversion Constructions)**
   - Negative inversion: "Never have I seen" → m1:"never", aux:"have", s:"I", v:"seen"
   - Question inversion: "Are you ready?" → aux:"are", s:"you", c1:"ready"

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
最初に**分詞構文エンジン**から実装開始することを提案。

---
作成日: 2025年8月12日  
担当: GitHub Copilot
