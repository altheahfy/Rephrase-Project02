# REPHRASE スロット構造 - 絶対遵守リファレンス

## ⚠️ AI ASSISTANT 必読事項
**このドキュメントは、Rephraseプロジェクトに関わる全てのAIアシスタントが必ず参照しなければならない絶対的基準です。**
**スロット分解を行う前に、毎回このドキュメントを確認してください。**

---

## 🏗️ Rephrase スロット構造（絶対不変の仕様）

### 上位スロット（固定10スロット）
```
M1, S, Aux, M2, V, C1, O1, O2, C2, M3
```
**これ以外のスロットは存在しない**

### サブスロット（上位スロット内の入れ子構造）
```
各上位スロット（Aux, V を除く）内に同じ構造が入れ子で存在：
sub-m1, sub-s, sub-aux, sub-m2, sub-v, sub-c1, sub-o1, sub-o2, sub-c2, sub-m3
```

### 重要な制約
1. **Aux, V にはサブスロットは存在しない**
2. **各上位スロット毎に独立したサブスロット空間**
3. **M1のsub-s と M2のsub-s は完全に別のスロット**
4. **サブスロットには sub-aux, sub-v も含まれる**

---

## 🎯 Type Clause の扱い

### Type Clause の特徴
- **上位スロットは空文字列 ""**
- **内容は全てサブスロットで表現**

### 例：Because clause
```
M1: ""  （上位は空）
sub-m1: "because"
sub-s: "he" 
sub-aux: "was"
sub-v: "captured"
sub-m2: "by bandits"
```

---

## ❌ 絶対にしてはいけない間違い

### 1. 存在しないスロットの創造
```
❌ sub-m1-conj
❌ sub-m1-aux  
❌ sub-m1-agent
❌ sub-m3-rel-s
❌ その他の独自スロット
```

### 2. サブスロットの重複を恐れる
```
❌ 「sub-sが重複する」という誤解
✅ M1のsub-s と M2のsub-s は別物
```

### 3. Type Clause で上位スロットに内容を入れる
```
❌ M1: "Because he was captured"
✅ M1: ""  （空文字列）
```

---

## ✅ 正しい分解例

### 例文：Because he was captured by bandits, I must go to the mountain where they live.

```json
{
    // 主節
    "S": "I",
    "Aux": "must",
    "V": "go",
    
    // M1位置のType Clause (Because節)
    "M1": "",
    "sub-m1": "because",
    "sub-s": "he",
    "sub-aux": "was", 
    "sub-v": "captured",
    "sub-m2": "by bandits",
    
    // M2位置のType Clause (前置詞句+関係節)
    "M2": "",
    "sub-m3": "to the mountain where",
    "sub-s": "they",
    "sub-v": "live"
}
```

---

## 🚨 AI Assistant への指示

### 必須チェック項目
1. **分解前にこのドキュメントを確認**
2. **上位スロットが正確か？（M1,S,Aux,M2,V,C1,O1,O2,C2,M3のみ）**
3. **存在しないスロットを作っていないか？**
4. **Type Clauseで上位スロットを空にしているか？**
5. **各上位スロット毎のサブスロット独立性を理解しているか？**

### エラー時の対応
- スロット分解で迷ったら、このドキュメントに戻る
- ユーザーに確認を求める前に、まずこの仕様を確認
- 独自のスロット名を絶対に創造しない

---

## 📝 更新履歴
- 2025-08-13: 初版作成 - AI Assistant反復エラー防止のため
