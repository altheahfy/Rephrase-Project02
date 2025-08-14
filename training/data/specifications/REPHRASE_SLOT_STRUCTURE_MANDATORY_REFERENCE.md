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

### Mスロット（M1, M2, M3）の位置ベース配置ルール
**⚠️ 重要：Mスロットは副詞の種類ではなく、文中での出現位置によって決定される**

- **M1**: 文頭近くの修飾語（文の最初の方に現れる副詞・副詞句）
- **M2**: 文の中間部の修飾語（動詞周辺に現れる副詞・副詞句）
- **M3**: 文尾近くの修飾語（文の最後の方に現れる副詞・副詞句）

**位置ベース配置の利点**：
- 複数の同種副詞（例：時間副詞が2つ）があってもバッティングしない
- 文中での自然な語順が保持される
- 機械的な配置ルールで一貫性が保たれる

**配置例**：
```
"Yesterday, I carefully finished my work early."
M1: "Yesterday"    ← 文頭位置
M2: "carefully"    ← 動詞周辺位置
M3: "early"        ← 文尾位置
```

**❌ 間違った考え方**：種類別分類
```
時間副詞 → M1？M3？ ← バッティングする
方法副詞 → M2？     ← 曖昧
```

**✅ 正しい考え方**：位置別分類  
```
文頭に現れる → M1
中間に現れる → M2  
文尾に現れる → M3
```

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

## 🚨 **最重要：単文 vs 複文の明確な区別**

### **単文（Simple Sentence）**
- **上位スロットに内容を直接格納**
- **サブスロットは使用しない**

**例：`"There are many students."`**
```json
{
  "S": "There",
  "V": "are", 
  "C1": "many students"
}
```

**例：`"Go home!"`**
```json
{
  "V": "Go",
  "M2": "home"
}
```

### **複文（Complex Sentence）**
- **主文：上位スロットに格納**
- **従属節：該当位置の上位スロットは空文字列 + サブスロットに格納**

**例：`"I think that he is genius."`**
```json
{
  "S": "I",
  "V": "think",
  "O1": "",          // 上位は空（従属節があるため）
  "sub-s": "that he", // 従属節の主語
  "sub-v": "is",      // 従属節の動詞
  "sub-c1": "genius"  // 従属節の補語
}
```

---

## 🎯 従属節（Type Clause）の扱い

従属節が存在する場合のみ、以下のルールが適用されます：

### 従属節の特徴
- **該当位置の上位スロットは空文字列 ""**
- **従属節の内容は全てサブスロットで表現**

**例：`"Because he was captured by bandits, I must go."`**
```json
{
  // M1位置の従属節（Because clause）
  "M1": "",              // 上位は空（従属節があるため）
  "sub-m1": "because",   // 従属接続詞
  "sub-s": "he",         // 従属節の主語
  "sub-aux": "was",      // 従属節の助動詞
  "sub-v": "captured",   // 従属節の動詞
  "sub-c2": "by bandits", // 従属節の前置詞句
  
  // 主文
  "S": "I",
  "Aux": "must", 
  "V": "go"
}
```

---

## ✅ 正しい分解例

### 【単文例1】存在文
**例文：`"There are many students in the classroom."`**
```json
{
  "S": "There",
  "V": "are",
  "C1": "many students",
  "C2": "in the classroom"
}
```

### 【単文例2】命令文
**例文：`"Give me the book quickly!"`**
```json
{
  "V": "Give",
  "O2": "me",
  "O1": "the book", 
  "M3": "quickly"
}
```

### 【単文例3】否定命令文
**例文：`"Don't go home!"`**
```json
{
  "Aux": "Don't",
  "V": "go",
  "C2": "home"
}
```

### 【単文例4】存在文（位置情報付き）
**例文：`"There is a book on the table."`**
```json
{
  "S": "There",
  "V": "is",
  "C1": "a book",
  "M3": "on the table"
}
```
**注意**: `"on the table"` は文尾近くの位置情報なので M3 に配置

### 【単文例5】複数修飾語の位置ベース配置
**例文：`"Yesterday, I carefully finished my work early."`**
```json
{
  "M1": "Yesterday",
  "S": "I", 
  "M2": "carefully",
  "V": "finished",
  "O1": "my work",
  "M3": "early"
}
```
**解説**: 3つの修飾語が文中位置に基づいて M1, M2, M3 に自然に配置される

### 【複文例1】that節を含む文
**例文：`"I think that he is genius."`**
```json
{
  // 主文
  "S": "I",
  "V": "think",
  
  // O1位置の従属節
  "O1": "",              // 上位は空（従属節があるため）
  "sub-s": "that he",    // 従属節の主語
  "sub-v": "is",         // 従属節の動詞  
  "sub-c1": "genius"     // 従属節の補語
}
```

### 【複文例2】副詞節を含む文
**例文：`"Because he was captured by bandits, I must go to the mountain where they live."`**
```json
{
  // M1位置の従属節（Because節）
  "M1": "",
  "sub-m1": "because",
  "sub-s": "he",
  "sub-aux": "was",
  "sub-v": "captured", 
  "sub-c2": "by bandits",
  
  // 主文
  "S": "I",
  "Aux": "must",
  "V": "go",
  
  // C2位置の従属節（関係節を含む前置詞句）
  "C2": "",
  "sub-c2": "to the mountain",
  "sub-s": "they",
  "sub-v": "live"
}
```

---

## ❌ 絶対にしてはいけない間違い

### 1. 単文で上位スロットを空にする
```
❌ 単文："There are many students."
   S: ""           ← 間違い
   sub-s: "There"  ← 間違い

✅ 単文："There are many students."
   S: "There"      ← 正しい
```

### 2. 複文で従属節を上位スロットに入れる
```
❌ 複文："I think that he is genius."
   O1: "that he is genius"  ← 間違い

✅ 複文："I think that he is genius."
   O1: ""                   ← 正しい（空文字列）
   sub-s: "that he"         ← 正しい
   sub-v: "is"              ← 正しい
   sub-c1: "genius"         ← 正しい
```

### 3. 存在しないスロットの創造
```
❌ sub-m1-conj
❌ sub-m1-aux  
❌ sub-m1-agent
❌ sub-m3-rel-s
❌ その他の独自スロット名
```

### 4. サブスロットの重複を恐れる
```
❌ 「sub-sが重複する」という誤解
✅ M1のsub-s と O1のsub-s は完全に別のスロット
```

---

## 🔍 判定フローチャート

### ステップ1：文構造の判定
```
単文？（主文のみ） → 上位スロットに直接格納
複文？（従属節あり）→ ステップ2へ
```

### ステップ2：従属節の位置特定
```
従属節がM1位置？ → M1=""、M1のサブスロットに格納
従属節がO1位置？ → O1=""、O1のサブスロットに格納  
従属節がC2位置？ → C2=""、C2のサブスロットに格納
以下同様...
```

### ステップ3：主文の処理
```
主文の要素 → 上位スロットに格納
```

---

## 🚨 AI Assistant への指示

### 必須チェック項目
1. **単文か複文かを最初に判定する**
2. **単文なら：上位スロットに直接格納（サブスロット不使用）**
3. **複文なら：主文は上位スロット + 従属節は該当位置を空にしてサブスロットに格納**
4. **上位スロットが正確か？（M1,S,Aux,M2,V,C1,O1,O2,C2,M3のみ）**
5. **存在しないスロットを作っていないか？**

### Priority 15 (ImperativeEngine) - 命令文の注意点
- **基本的に単文** → 上位スロットに直接格納
- **修飾語の位置判定が重要**: 文中での出現位置に基づいてM1/M2/M3を決定
- **例**: `"Don't go!"` → `{"Aux": "Don't", "V": "go"}`
- **例**: `"Give me the book quickly!"` → `{"V": "Give", "O2": "me", "O1": "the book", "M3": "quickly"}`
- **例**: `"Carefully open the door."` → `{"M1": "Carefully", "V": "open", "O1": "the door"}`

### Priority 16 (ExistentialThereEngine) - 存在文の注意点  
- **基本的に単文** → 上位スロットに直接格納
- **場所・時間の修飾語**: 文尾に現れる場合は M3 に配置（M2 ではない）
- **例**: `"There are many students."` → `{"S": "There", "V": "are", "C1": "many students"}`
- **例**: `"There is a book on the table."` → `{"S": "There", "V": "is", "C1": "a book", "M3": "on the table"}`
- **例**: `"Yesterday, there were problems."` → `{"M1": "Yesterday", "S": "There", "V": "were", "C1": "problems"}`
- **注意**: `C1`は主語補語（存在するもの）、`O1`ではない

### エラー時の対応
- スロット分解で迷ったら、まず**単文/複文を判定**
- 単文なのにサブスロットを使っていないか確認
- 複文なのに従属節を上位スロットに入れていないか確認

---

## 📝 更新履歴
- 2025-08-13: 初版作成 - AI Assistant反復エラー防止のため
- 2025-08-14: 大幅リライト - 単文/複文の明確な区別を追加、Priority 15/16の具体例を追加
- 2025-08-14: Mスロット位置ベース配置ルールを明記 - 副詞の種類ではなく文中位置で決定するルールを詳細化
