# Rephraseプロジェクト例文増殖設計仕様書（v4.0）

作成日: 2025-08-07  
作成者: ChatGPT（Rephraseプロジェクト参謀本部）  
用途: ChatGPT に例文増殖を依頼する際の標準仕様ガイド  
重要更新: スロット別要素生成への根本転換（Rephraseランダマイズアルゴリズム完全対応）

---

## 🎯 **目的**

**スロット別要素生成**により、Rephraseランダマイズシステム用のスロット別データベースを構築する。  

**核心原則**: 
- 各スロットの要素を独立して生成し、どの組み合わせでも文法的に正しい文が構成できるようにする
- **Aux・V（助動詞・動詞）は完全固定**、その他スロットのみ多様化対象  
- 完成文の生成ではなく、ランダマイズ時の組み合わせ材料となるスロット要素の多様化が目標

---

## 🏗️ **Rephraseランダマイズアルゴリズムの理解**

### ⚡ **スロット別独立ランダマイズの仕組み**
```
例: 元文 "We lie on the couch."

スロット分解:
- S候補: [We, I, They, She, He, The student] ← 多様化対象
- V候補: [lie] ← 完全固定（変更しない）
- 場所候補: [on the couch, on the bed, in the room] ← 多様化対象

ランダマイズ実行:
- I + lie + on the couch = "I lie on the couch."
- They + lie + on the bed = "They lie on the bed."  
- She + lie + in the room = "She lies in the room."

🎯 重要: 
- Aux・V（助動詞・動詞）は一切変更しない
- その他のスロット要素のみ多様化
- どの組み合わせでも文法的に成立することが前提
```

### 🔒 **固定要素 vs 多様化要素**

| 要素タイプ | 扱い | 例 | 理由 |
|-----------|------|----|----|
| **Aux（助動詞）** | **完全固定** | has, will, can | 文法構造の核心 |
| **V（動詞）** | **完全固定** | recovered, lie, make | 文の意味的核心 |
| **S（主語）** | **多様化** | I, We, She, The student | 人称・数の多様性 |
| **O（目的語）** | **多様化** | the book, Mark, it | 対象の多様性 |
| **M（修飾語）** | **多様化** | fully, yesterday, quickly | 表現の多様性 |
| **場所・時間** | **多様化** | on the couch, in the room | 状況の多様性 |

---

## 🌱 **スロット別要素生成3段階プロセス**

### 🎯 **段階1: スロット構造分析**

**目的**: 元文のスロット構造と固定要素の特定  
**作業**: 文法的機能別のスロット分解

**手順**:
1. 元文の基本文型を特定（SVO, SVC等）
2. 各要素をスロット別に分解
3. **Aux・V を固定要素として明確に特定**
4. その他を多様化対象として確認

**出力例**:
```
元文分析: "We lie on the couch."
基本文型: S + V + 前置詞句

スロット分解:
- S: "We" (主語・複数人称代名詞) → 多様化対象
- V: "lie" (動詞・現在形・自動詞) → 完全固定  
- 場所: "on the couch" (前置詞句・場所表現) → 多様化対象

固定要素: V="lie"（一切変更しない）
多様化要素: S、場所
```

---

### 🔤 **段階2: スロット別要素生成**

**目的**: 各スロットの多様な候補要素を独立生成  
**作業**: 固定要素を除く各スロットの豊富なバリエーション作成

**重要原則**:
- **Aux・V は一切変更しない**（同義語も禁止）
- 他スロットは完全独立で多様化
- 代名詞整合性はRephraseシステムの動的補正に委ねる

**出力例**:
```
元文: "We lie on the couch."

スロット別要素生成:

【固定要素】
V候補: [lie] ← 固定（変更禁止）

【多様化要素】
S候補（主語・20個目安）:
- I, You, He, She, We, They
- The student, My friend, Everyone, The children
- John, Sarah, The team, My family
- The patient, The visitor, A stranger

場所候補（場所表現・25個目安）:
- on the couch, on the bed, on the sofa
- in the room, in the garden, on the floor
- under the tree, by the window, in the chair
- on the carpet, in the corner, near the fireplace
```

**代名詞を含む複雑な例**:
```
元文: "He has fully recovered his strength."

【固定要素】
- Aux: [has] ← 固定（変更禁止）
- V: [recovered] ← 固定（変更禁止）

【多様化要素】  
- S候補: [He, She, I, We, They, The patient, John, Sarah, ...]
- M候補: [fully, completely, gradually, rapidly, successfully, ...]
- O候補: [his strength, her confidence, my energy, their focus, ...]

🎯 重要: 代名詞不整合（"He + her strength"等）は
Rephraseシステムが自動補正するため考慮不要
```

---

### ✅ **段階3: 組み合わせ検証**

**目的**: 全組み合わせでの文法的正確性の確認  
**作業**: ランダムサンプリングによる組み合わせテスト

**手順**:
1. ランダムに10-20パターンの組み合わせを生成
2. 各組み合わせの基本文法正確性をチェック
3. 問題のある要素を特定・修正
4. 最終的なスロット要素リストを確定

**出力例**:
```
組み合わせ検証（サンプル）:

1. "I lie in the garden." ✓
2. "The children lie on the bed." ✓
3. "She lies by the window." ✓
4. "Everyone lies on the carpet." ✓
5. "The team lies in the room." ✓

検証結果: 全組み合わせで基本文法正確性確認 ✓
問題要素: なし

最終確認: 
- 固定要素 V="lie" が全文で維持されている ✓
- 主語動詞一致が保たれている ✓
- 基本文型が維持されている ✓
```

---

## 🎯 **重要ルール**

### ✅ **絶対遵守事項**
1. **Aux・V完全固定**: 助動詞・動詞は一切変更しない（同義語も禁止）
2. **構造維持**: 基本文型パターンは完全保持
3. **スロット独立性**: 各スロットの要素を独立して生成
4. **組み合わせ保証**: 全てのスロット要素の組み合わせが文法的に成立

### 🔧 **Rephraseシステム依存事項**
- **代名詞整合性**: "He + her strength" → "He + his strength" の自動補正
- **主語動詞一致**: "She + lie" → "She + lies" の自動調整
- **時制調整**: 必要に応じた動詞活用の自動変更

### ❌ **禁止事項**
- Aux・V の変更（recovered → regained 等も禁止）
- 文型構造の変更（SVO → SVC 等の変更禁止）
- 新しいスロットの追加・削除
- 完成文の個別作成（スロット要素のみ生成）

---

## 💾 **ChatGPTへの実行指示例**

### 📋 **基本指示テンプレート**
```
【スロット別要素生成 v4.0】
以下の例文からスロット別要素生成を実行してください。

例文: "[元文]"

指示:
1. 段階1: スロット構造分析（固定要素特定）
2. 段階2: スロット別要素生成（Aux・V固定、他多様化）  
3. 段階3: 組み合わせ検証（10パターンテスト）

重要制約:
- Aux・V は一切変更禁止
- 代名詞整合性はシステム依存
- 全組み合わせでの文法的成立を保証
```

### 🎯 **具体例**
```
【実行例】
例文: "I got the book yesterday."

期待する出力:
段階1: S="I", V="got"(固定), O="the book", M="yesterday"
段階2: S候補[I,You,He,She,We,They,...], V候補[got](固定), O候補[the book,a pen,help,...], M候補[yesterday,today,quickly,...]
段階3: 検証サンプル "She got help today." ✓
```

---

## 🚀 **運用効果**

この仕様書v4.0により：

✅ **Rephraseアルゴリズム完全対応**: スロット別独立ランダマイズに最適化  
✅ **文法破綻の防止**: Aux・V固定により基本構造を保証  
✅ **組み合わせ爆発の活用**: 豊富なスロット要素で膨大な文パターン生成  
✅ **システム連携**: 動的補正機能との完全な分業体制  
✅ **作業効率化**: 3段階の明確なプロセスで迷いなく実行可能

---

**ファイル名推奨**: `example_expansion_spec_v4.0.md`（スロット別要素生成型）  
**更新履歴**: v1.2→v2.0→v3.0→**v4.0（スロット別要素生成への根本転換）**
