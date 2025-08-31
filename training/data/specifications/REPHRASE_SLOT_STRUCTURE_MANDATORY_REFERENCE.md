# REPHRASE スロット構造 - 絶対遵守リファレンス

## ⚠️ AI ASSISTANT 必読事項
**このドキュメントは、Rephraseプロジェクトに関わる全てのAIアシスタントが必ず参照しなければならない絶対的基準です。**
**スロット分解を行う前に、毎回このドキュメントを確認してください。**

---

## 🎯 **Rephraseの根本原理：スロット内容の並列表示**

### **⚡ 最重要理解事項**
**Rephraseでは、分解されたスロット内容をそのまま並べて例文を再構築表示します。**
**つまり、スロット分解の正確性は「並べたら元の例文に戻るか？」で判定されます。**

### **❌ 間違った分解による表示破綻例**

**例文：`"The man who runs fast is strong."`**

**❌ 先行詞重複パターン：**
```json
{
  "S": "The man",           // ← 先行詞重複！
  "sub-s": "The man who",   // ← また先行詞！
  "sub-v": "runs",
  "sub-m2": "fast",
  "V": "is",
  "C1": "strong"
}
```
**→ 表示結果：** `"The man The man who runs fast is strong"`  
**→ 問題：** "The man"が2回出現して不自然

**❌ 関係代名詞欠落パターン：**
```json
{
  "S": "",
  "sub-s": "The man",       // ← "who"が消失！
  "sub-v": "runs",
  "sub-m2": "fast",
  "V": "is",
  "C1": "strong"
}
```
**→ 表示結果：** `"The man runs fast is strong"`  
**→ 問題：** 関係代名詞"who"消失で文法破綻

**✅ 正しい分解：**
```json
{
  "S": "",                  // ← 空（重複回避）
  "sub-s": "The man who",   // ← 先行詞+関係代名詞セット
  "sub-v": "runs",
  "sub-m2": "fast",
  "V": "is",
  "C1": "strong"
}
```
**→ 表示結果：** `"The man who runs fast is strong"`  
**→ 結果：** 完璧に元の例文を再現！

### **🔥 スロット分解の3大原則**
1. **重複排除**: 同じ単語を複数スロットに入れない
2. **欠落防止**: 関係代名詞・接続詞等の機能語を必ず保持
3. **文法保持**: スロット内容を並べたら自然な英文になる

**→ この原則により、関係節では先行詞は上位スロットから除外し、サブスロットに「先行詞+関係代名詞」として格納する**

---

## 🏗️ Rephrase スロット構造（絶対不変の仕様）

### 上位スロット（固定10スロット）
```
M1, S, Aux, M2, V, C1, O1, O2, C2, M3
```
**これ以外のスロットは存在しない**

### Mスロット（M1, M2, M3）の超シンプル配置ルール【2025年8月確定版】
**⚠️ 重要：Mスロットは副詞の種類ではなく、文中での出現個数によって決定される**

### 🎯 **【革命的超シンプルルール】蒸し返し問題完全解決版**

**【問題の背景】**
副詞配置は、この例文システムの開発開始からずっと繰り返し蒸し返され、解決できない課題だった。
複雑なロジック（距離ベース、位置ベース、意味ベース等）を試みても全く解決できないため、
むしろ**超単純ルール**のほうがかえってRephraseロジックに近づくという結論に至った。

### 🔥 **【確定ルール：個数ベース配置】**

**【サルでも100％理解できる超明確ルール】**

**🟢 1個のみ使われているとき**
```
修飾語が1個だけ → 必ずM2に配置
位置は関係なし（動詞の前でも後でも）
```

**🟡 2個使われているとき【重要：動詞との距離で判定】**
```
ケース1: 受動態でAgent句（by句）がある場合
→ M2（動詞修飾語）, M3（Agent句）

ケース2: 修飾語が動詞の前後に分散している場合
→ M2（動詞に近い修飾語）, M1または M3（動詞から遠い修飾語）
　　- 動詞から遠い修飾語が前方 → M1
　　- 動詞から遠い修飾語が後方 → M3

ケース3: 修飾語が同じ側（前または後）に集中している場合
→ M1, M2（前方集中） または M2, M3（後方集中）
```

**🔴 3個使われているとき**
```
文中の出現順にM1, M2, M3
```

**【配置例：完全予測可能】**

**例1：1個パターン**
```
"I carefully work."       → M2: "carefully"
"I work carefully."       → M2: "carefully"  
"Carefully, I work."      → M2: "carefully"
```
**→ どこにあってもM2（位置無関係）**

**例2：2個パターン - ケース1（受動態 + Agent句）**
```
"The window was gently opened by the breeze."
修飾語: gently（動詞修飾語）, by the breeze（Agent句）
→ M2: "gently", M3: "by the breeze"
```

**例2：2個パターン - ケース2（前後分散）**
```
"Yesterday I work hard."
修飾語: Yesterday（動詞から遠い・前方）, hard（動詞に近い・後方）
→ M1: "Yesterday", M2: "hard"

"I carefully work by hand."
修飾語: carefully（動詞に近い・前方）, by hand（動詞から遠い・後方）
→ M2: "carefully", M3: "by hand"
```

**例2：2個パターン - ケース3（同側集中）**
```
"Yesterday morning I work."
修飾語2個とも前方集中 → M1: "Yesterday", M2: "morning"

"I work carefully by hand."
修飾語2個とも後方集中 → M2: "carefully", M3: "by hand"
```

``

**例3：3個パターン**
```
"Yesterday I quickly work hard."
→ M1: "Yesterday", M2: "quickly", M3: "hard"（位置順）
```

**【Agent句（by句）の特別扱い - 最優先ルール】**
```
受動態でAgent句（by句）がある場合は常に:
→ 他の修飾語をM2, Agent句をM3に配置

"The letter was written by John."
→ 修飾語1個 → M2: "by John"

"The window was gently opened by the breeze."
→ 修飾語2個（受動態+Agent句） → M2: "gently", M3: "by the breeze"

"The book was carefully and thoroughly reviewed by experts."
→ 修飾語3個（受動態+Agent句） → M1: "carefully", M2: "thoroughly", M3: "by experts"
```

**【重要】Agent句がある場合は距離ベース判定よりも優先される**

**❌ 従来の複雑ルール**：距離・意味・位置を複合判定
**✅ 新シンプルルール**：個数のみで機械的に判定

**【利点】**
- **100%予測可能**：個数を数えるだけ
- **蒸し返し防止**：単純すぎて議論の余地なし
- **実装簡単**：複雑なロジック不要
- **Rephrase精神**：直感的で分かりやすい

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

---

## 🔥 **【サルでも100％理解】M-スロット配置フローチャート**

### 📋 **STEP 1: 修飾語の個数を数える**
```
修飾語を全部リストアップ → 個数を数える
例: "I carefully work by hand." → ["carefully", "by hand"] → 2個
```

### 📋 **STEP 2: 個数別ルール適用**

#### 🟢 **1個の場合**
```
M2に配置 （位置無関係）
```

#### 🟡 **2個の場合**
```
STEP 2-1: 動詞の位置を特定
STEP 2-2: 動詞より前に修飾語があるかチェック

前にある？
├─ YES → ケース1: M1(前の修飾語), M2(残りの修飾語)
└─ NO  → ケース2: M2(最初の修飾語), M3(次の修飾語)
```

#### 🔴 **3個の場合**
```
文中の出現順に M1, M2, M3
```

### 💡 **超具体例で理解確認**

**Case 24: "The manager carefully managed the project by the manager."**
```
STEP 1: 修飾語 = ["carefully", "by the manager"] = 2個
STEP 2: 2個 → 動詞"managed"の前に"carefully"あり
結果: ケース1 → M1: "carefully", M2: "by the manager"
```

**期待値と一致！**
```json
{
  "M1": "carefully",
  "M2": "",  // ← 空（M1使用時）
  "M3": "by the manager"  // ← 実際はここに入る！
}
```

**⚠️ 間違いを発見！期待値が M1: carefully, M3: by the manager なら...**

### 🚨 **緊急修正：実際の期待値ルール**
```
Case 24の期待値: M1: carefully, M2: (なし), M3: by the manager

これは「前後分散配置ルール」
前に1つ、後に1つ → M1(前), M3(後), M2は空
```

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
- **🎯 最重要チェック**: スロット内容を並べたら元の例文に戻るか？
  - 重複する単語がないか？
  - 関係代名詞・接続詞が欠落していないか？
  - 文法的に自然な英文になるか？

---

## 📝 更新履歴
- 2025-08-13: 初版作成 - AI Assistant反復エラー防止のため
- 2025-08-14: 大幅リライト - 単文/複文の明確な区別を追加、Priority 15/16の具体例を追加
- 2025-08-14: Mスロット位置ベース配置ルールを明記 - 副詞の種類ではなく文中位置で決定するルールを詳細化
- **2025-08-17: Mスロット「文の中央からの距離」原理を明記** - M2優先使用、拡張可能性考慮、余裕のある配置ルールを詳細化
