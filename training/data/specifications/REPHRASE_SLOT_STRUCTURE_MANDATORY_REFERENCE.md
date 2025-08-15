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

### サブスロット（上位スロット内の階層構造）

**🔥 絶対理解事項：各上位スロットが独自のサブスロット群を持つ**

```
【S位置のサブスロット群】
S-sub-m1, S-sub-s, S-sub-aux, S-sub-m2, S-sub-v, S-sub-c1, S-sub-o1, S-sub-o2, S-sub-c2, S-sub-m3

【M1位置のサブスロット群】  
M1-sub-m1, M1-sub-s, M1-sub-aux, M1-sub-m2, M1-sub-v, M1-sub-c1, M1-sub-o1, M1-sub-o2, M1-sub-c2, M1-sub-m3

【M2位置のサブスロット群】
M2-sub-m1, M2-sub-s, M2-sub-aux, M2-sub-m2, M2-sub-v, M2-sub-c1, M2-sub-o1, M2-sub-o2, M2-sub-c2, M2-sub-m3

... (O1, O2, C1, C2, M3も同様)
```

**❌ 絶対に間違った理解：**
- `sub-m2` がM2のサブスロット ← **大間違い！**
- `sub-v` がVのサブスロット ← **大間違い！**
- 全スロットで共通のサブスロット群 ← **大間違い！**

**✅ 正しい理解：**
- `S-sub-m2` はSスロットのサブスロット
- `M2-sub-v` はM2スロットのサブスロット  
- `O1-sub-s` はO1スロットのサブスロット
- **各上位スロットが独立した10個のサブスロットを持つ**

### 🚨 **サブスロット → 上位スロット空化の絶対ルール**

**【絶対不変ルール】**
```
その上位スロットのサブスロット群に1つでも要素が入った場合
→ その上位スロットは必ず空文字列 ""
```

**具体例：**
- **S-sub-v に要素** → **S = ""** (Sを空化)
- **M2-sub-s に要素** → **M2 = ""** (M2を空化)
- **O1-sub-m1 に要素** → **O1 = ""** (O1を空化)

**❌ 間違った適用：**
- S-sub-m2 に要素 → M2を空化 ← **絶対間違い！**
- M1-sub-v に要素 → Vを空化 ← **絶対間違い！**

### 重要な制約
1. **Aux, V にはサブスロットは存在しない**
2. **各上位スロット毎に独立したサブスロット空間**  
3. **S-sub-s と M2-sub-s は完全に別のスロット**
4. **階層関係：上位スロット ←→ そのサブスロット群（10個）**

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
- **従属節：該当位置の上位スロットは空文字列 + その位置のサブスロットに格納**

**例：`"I think that he is genius."`**
```json
{
  "S": "I",
  "V": "think",
  "O1": "",                    // O1位置に従属節があるためO1は空
  
  // 【O1位置のサブスロット群】に従属節を格納
  "O1-sub-s": "he",           // 従属節の主語
  "O1-sub-v": "is",           // 従属節の動詞  
  "O1-sub-c1": "genius"       // 従属節の補語
}
```

**🔥 重要：上記の例では実装上 "sub-s", "sub-v", "sub-c1" と表記されているが、**
**概念的には "O1-sub-s", "O1-sub-v", "O1-sub-c1" である**

---

## 🎯 従属節（Type Clause）の扱い

従属節が存在する場合のみ、以下のルールが適用されます：

### 従属節の特徴
- **該当位置の上位スロットは空文字列 ""**
- **従属節の内容は全てサブスロットで表現**

**例：`"Because he was captured by bandits, I must go."`**
```json
{
  // 【M1位置に従属節】→ M1は空 + M1のサブスロット群に格納
  "M1": "",                      // M1位置に従属節があるためM1は空
  "M1-sub-m1": "because",        // 従属接続詞（M1のサブスロット）
  "M1-sub-s": "he",              // 従属節の主語（M1のサブスロット）
  "M1-sub-aux": "was",           // 従属節の助動詞（M1のサブスロット）
  "M1-sub-v": "captured",        // 従属節の動詞（M1のサブスロット）
  "M1-sub-c2": "by bandits",     // 従属節の前置詞句（M1のサブスロット）
  
  // 主文
  "S": "I",
  "Aux": "must", 
  "V": "go"
}
```

**🔥 実装上の表記：** `"sub-m1", "sub-s", "sub-aux", "sub-v", "sub-c2"`
**🔥 概念上の意味：** `"M1-sub-m1", "M1-sub-s", "M1-sub-aux", "M1-sub-v", "M1-sub-c2"`

**❌ 絶対に間違った理解：**
- `sub-v` があるからVを空化 ← **大間違い！** これはM1-sub-vです
- `sub-s` があるからSを空化 ← **大間違い！** これはM1-sub-sです

**✅ 正しい理解：**
- `M1-sub-v` があるからM1を空化 ← **正解！**
- `M1-sub-s` があるからM1を空化 ← **正解！**

### 🔥 **連続動詞構造の重要例（Test26パターン）**

**例文：`"The door opened slowly creaked loudly."`**
**構造：** "The door [which] opened slowly" + "creaked loudly"

```json
{
  // 【S位置に従属節】→ S空 + Sのサブスロット群に格納
  "S": "",                        // S位置に従属節があるためS空化
  "S-sub-v": "The door opened",   // 従属動詞句（Sのサブスロット）  
  "S-sub-m2": "slowly",           // 従属副詞（Sのサブスロット）
  
  // 主文
  "V": "creaked",                 // メイン動詞
  "M2": "loudly"                  // メイン副詞
}
```

**🔥 実装上の表記：** `"sub-v": "The door opened", "sub-m2": "slowly"`
**🔥 概念上の意味：** `"S-sub-v": "The door opened", "S-sub-m2": "slowly"`

**❌ 絶対に間違った理解：**
- `sub-m2` があるからM2を空化 ← **大間違い！** これはS-sub-m2です
- M2のサブスロットに要素がある ← **大間違い！** M2-sub-*は全て空です

**✅ 正しい理解：**  
- `S-sub-v` と `S-sub-m2` があるからSを空化 ← **正解！**
- M2のサブスロット群（M2-sub-*）は全て空なのでM2は"loudly"で保持 ← **正解！**
  
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
