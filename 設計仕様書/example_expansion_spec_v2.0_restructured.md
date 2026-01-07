# Rephraseプロジェクト例文増殖設計仕様書（v2.0 完全再構築版）

**作成日**: 2025-08-05（再構築: 2026-1-3）  
**作成者**: ChatGPT（再構築ClaudeSonnet4.5）  
**用途**: AI'sに例文増殖を依頼する際の標準仕様ガイド  
**重要更新**: 構成の完全再編成、重複削除、論理的な流れの確立

---

# Part 1: 導入・前提知識

## 1.1 目的

**属性固定型増殖**により、Rephraseランダマイズシステム用のスロット別データベースを構築する。

**核心原則**: 一つの増殖作業では一つの属性セット（gender, number等）のみを固定し、その属性内でのみ語彙パラフレーズを行う。

**効果**: 「He has gradually recovered her stamina.」等の文法破綻文の生成を根本的に防止し、スロット別個別ランダマイズに対応したデータを提供する。

---

## 1.2 なぜ属性固定型が必要か？

### 🔴 **無秩序増殖の問題**

**Rephraseランダマイズの仕組み**:
```
各スロットから独立して要素を選択
↓
組み合わせて文を生成
```

**無秩序増殖の場合**:
```
元文: "He has fully recovered his strength."
無秩序増殖結果（属性混在）:
1. He has fully recovered his strength.
2. She has completely recovered his confidence. ← ❌ 属性混在
3. They have gradually recovered her energy. ← ❌ 動詞変化+属性混在

↓ スロット別データベース化

S候補: [He, She, They]
O1候補: [his strength, his confidence, her energy]

↓ ランダマイズで組み合わせ

結果例:
× She + has + recovered + his strength（She + his 不整合）
× They + has + recovered + her energy（数不一致）
```

### 🟢 **属性固定型増殖の場合**

```
元文: "He has fully recovered his strength."
属性固定増殖（male/singular統一）:
1. He has fully recovered his strength.
2. My brother has completely recovered his confidence.
3. The man has gradually recovered his energy.
4. John has rapidly recovered his stamina.

↓ スロット別データベース化

S候補: [He, My brother, The man, John]（全てmale/singular）
O1候補: [his strength, his confidence, his energy, his stamina]（全てhis）

↓ ランダマイズで組み合わせ

結果: 全16通りが文法的に正しい ✅
```

---

## 1.3 核心原則

### 🔒 **一つの増殖=一つの属性統一**

- **核心ルール**: 一回の増殖作業では、主語（S）の属性（gender, number）を統一する
- **例**: 「He has fully recovered his strength.」→ male/singular統一で4例文生成
- **可能**: 別セッションでのI→You、He→She等への完全属性変更
- **禁止**: 同一増殖セッション内でのI/You/He/She/We/They等の属性混在

### 💡 **Aux・V完全固定原則**

- **核心ルール**: 助動詞・動詞は一切変更しない
- **例**: "lie" は "lie" のまま（"lies"、"lay"への変更禁止）
- **例**: "got" は "got" のまま（"get"、"gotten"への変更禁止）
- **理由**: 動詞形が変わると、主語の制約が変わり属性統一が破綻する

### 📊 **構造維持原則**

- **スロット構成完全固定**: 元例文にあるスロットのみ増殖対象（新規スロット追加・削除禁止）
- **品詞カテゴリ固定**: 各スロットの品詞カテゴリ（名詞句・副詞句・形容詞等）は維持
- **絶対順序維持**: スロットの順序は元文と完全一致

### 🎯 **絶対順序システム（オプショナル要素の自由組み合わせ）**

**目的**: 疑問詞・副詞等のオプショナル要素を独立に選択可能にする

**仕組み**:
1. **各スロットの出現位置を母集団内で固定**（例: M2は①と⑧、O2は②と⑦）
2. **空セルを許容**（スロットがオプショナルであることを表現）
3. **各スロットから独立にランダム選択**（縦横無尽の組み合わせ）

**効果例（疑問文母集団）**:
```
①M2-1   ②O2-2   ③Aux-3   ④S-4   ⑤V-5   ⑥O1-6   ⑦O2-7      ⑧M2-8
-        what     did      he     tell   her     -          at the store
-        -        did      he     tell   her     a secret   there
where    -        did      you    tell   me      a story    -

【組み合わせ例】
- ①"where" + ⑧空 → "Where did you tell me a story?"（疑問詞あり、副詞なし）
- ①空 + ⑧"there" → "Did he tell her a secret there?"（疑問詞なし、副詞あり）
- ①"where" + ⑧"there" → "Where did you tell me a story there?"（両方あり）
- ①空 + ⑧空 → "Did he tell her a secret?"（両方なし）

→ 2^n通りの構造バリエーション生成可能
```

**重要**: 絶対順序システムは**オプショナル要素を含む母集団にのみ適用**。通常の増殖（副詞なし・疑問詞なし）では不要。

---

## 1.4 絶対禁止事項（❌）

### 🚨 **この行為は即座に作業停止**

| 禁止事項 | 例 | 理由 |
|---------|---|------|
| **Aux・V変更** | "lie" → "lies", "got" → "get" | 動詞形と互換性のある主語が変わり、属性統一が破綻 |
| **属性混在** | 同一セッション内で "I" と "He" の混在 | ランダマイズ時に文法破綻を引き起こす |
| **構造変更** | スロット追加・削除、順序変更 | 元文との整合性が失われる |
| **同一人称組み合わせ** | "I told me", "You saw you", "We helped us" | 意味的に不自然（例外: "I like me"等の慣用表現） |

---

## 1.5 AI理解度確認（作業開始前必須）

**❗重要**: 以下の理解度確認に全問正解するまで作業開始禁止

### 📋 **必須理解チェック**

#### Q1: Aux・V完全固定ルールの理解

「I lie on the bed.」を4例文に拡張する場合、以下のうち**正しい**ものは？

```
A) I lie → She lies → They lie → We lay
   （動詞が lie/lies/lay に変化）

B) I lie → You lie → We lie → They lie  
   （動詞 "lie" を完全固定）

C) I lie → I rest → I sleep → I relax
   （主語固定で動詞変更）
```

**正解**: **B）** 動詞形を完全に固定し、その動詞形と互換性のある主語のみ選択

---

#### Q2: 4例文生成の必須要件

2例文「I lie on the bed. / I lie on the couch.」を4例文に拡張する**正しい**アプローチは？

```
A) I lie on the bed → I lie on the couch → I lie on the sofa → I lie on the floor
   （主語固定、場所のみ拡張）

B) I lie on the bed → You lie on the couch → We lie on the sofa → They lie on the floor
   （動詞固定、主語と場所を多様化）

C) I lie on the bed → I rest on the couch → I sleep on the sofa → I relax on the floor  
   （主語固定、動詞と場所を変更）
```

**正解**: **B）** Aux・V以外の全スロット（主語・場所等）で最大限の多様性を実現

---

#### Q3: 属性統一原則の理解

「He has fully recovered his strength.」を4例文に拡張する場合（**male/singular固定**として）、**正しい**アプローチは？

```
A) He → She → They → We
   （属性混在: male/female/pluralが混在）

B) He → My brother → The man → John
   （male/singular統一: 同じ属性内でのみ変更）

C) He → He → He → He
   （多様性不足: 主語が全く変わっていない）
```

**正解**: **B）** 同じ属性（male/singular）内でのみ主語を変更し、多様性を確保

---

#### Q4: 同一人称組み合わせ制約の理解

「I helped someone with the task.」を4例文に拡張する場合、**避けるべき**組み合わせは？

```
A) I helped him → You helped her → We helped them → She helped us
   （主語と目的語が異なる人称）

B) I helped me → You helped you → We helped us → They helped them
   （主語と目的語が同一人称: 意味的に不自然）

C) I helped → You helped → We helped → She helped
   （目的語を削除: 構造変更のため禁止）
```

**正解**: **A）** 主語と目的語が異なる人称の組み合わせのみ使用

**⚠️ 同一人称組み合わせが不自然な理由**:
- "I saw me" → 「私が私を見た」（鏡等の特殊文脈以外では不自然）
- "We show us an important message" → 「私たちが私たちに見せる」（意味的に矛盾）
- "You told you" → 「あなたがあなたに言った」（再帰的でない文脈では不自然）

**例外的に自然な場合**:
- "I like me." → 自己肯定的文脈では可能
- "You be you." → 慣用表現では可能

---

### ✅ **理解度確認通過条件**

- **4問全問正解**: 作業開始許可
- **1問でも不正解**: 仕様書再読後、再チャレンジ必須

### 🚨 **理解確認後の宣言**

理解度確認通過後、以下を明記してから作業開始：

```
✅ 理解度確認完了（Q1-Q4全問正解）
- Aux・V完全固定: 動詞形を一切変更しない
- 多様性原則: Aux・V以外の全スロットで多様化
- 属性統一原則: 同じ属性内でのみ主語を変更
- 同一人称制約: 主語と目的語が同一人称にならないよう注意
```

---

## 1.6 品質保証項目

**最終検証で必ず確認すべき項目**:

| 項目 | 確認内容 |
|------|---------|
| **属性統一性** | 全例文が同一属性（gender, number）で統一されている |
| **代名詞整合性** | 所有格代名詞が主語の属性と完全に一致している |
| **文法正確性** | 全文が文法的に正しく、自然に成立している |
| **Aux・V固定性** | 助動詞・動詞が元文と完全に一致している |
| **構造維持** | スロット構成・順序が元文と完全に一致している |
| **意味的自然性** | 同一人称組み合わせ等の不自然さがない |

---

# Part 2: 実行手順（Stage 0-5）

## 2.1 全体フロー

```
Stage 0: 属性統一宣言（属性の決定と宣言のみ）
  ↓
Stage 1: 構造分析（スロット分解と絶対順序の特定のみ）
  ↓
Stage 2: 語彙候補生成（固定属性内での候補生成のみ）
  ↓
Stage 3: 組み合わせ構築（有効な組み合わせ作成のみ）
  ↓
Stage 4: 最終構築・検証（文の組み立てと品質確認のみ）
  ↓
V_group_key決定（主語・目的語パターン分析と識別子割り当て）
  ↓
Stage 5: V_group_key分割増殖（別人称パターンでの追加増殖、オプション）
```

**重要**: 各Stageを独立して実行し、前Stage完了確認後に次Stageに進むこと。Stage 5はオプションで、増殖効率を上げたい場合に実施。

---

## 2.2 Stage 0: 属性統一宣言

### 🎯 **目的**
増殖対象属性の明確な決定と統一宣言

### 📋 **作業内容**
属性選択と統一宣言のみ

### 🚫 **禁止事項**
語彙変更・構造分析・増殖作業

### 📝 **手順**

1. 元文の主語（S）属性を特定
2. 増殖対象属性を選択（male/female/neutral × singular/plural）
3. 属性統一を明確に宣言（このセッション内での統一）
4. 増殖範囲の確認

### 📤 **出力例**

```
元文: "He has fully recovered his strength."
元文属性: S=male/singular

【属性統一宣言】
このセッションでは「male/singular」に属性を統一し、
この属性の範囲内でのみ語彙パラフレーズを実行します。

【重要】別セッションでの属性変更について:
- I→You、He→She等への変更は完全に可能
- このセッション内では属性混在を防ぐため統一を維持

【禁止事項確認】（このセッション内のみ）:
- 「She/Her」等のfemale要素は使用しない
- 「They/Their」等のplural要素は使用しない
- 「The patient/The child」等のneutral要素は使用しない
```

### ✅ **検証項目**

- [ ] 元文の属性が正確に特定されている
- [ ] 増殖対象属性が明確に選択されている
- [ ] 禁止事項が明確に理解されている

---

## 2.3 Stage 1: 構造分析

### 🎯 **目的**
元例文のスロット構成の完全把握

### 📋 **作業内容**
スロット分解と絶対順序の特定のみ

### 🚫 **禁止事項**
語彙変更・属性変更・増殖作業

### 📝 **手順**

1. 元例文を単語レベルで分析
2. 各要素のスロット番号を絶対順序で割り当て
3. Aux・Vを固定要素として特定
4. 属性依存スロット（M2, C1, O1等）の特定

### 📤 **出力例**

```
元文: "He has fully recovered his strength."
属性固定: male/singular

【構造分析結果】
- S-1: He (male/singular - 固定属性)
- Aux-2: has (完全固定)
- M2-3: fully (属性無関係)
- V-4: recovered (完全固定)
- O1-5: his strength (属性依存 - male/singularに固定)

【固定要素】
- Aux-2: has
- V-4: recovered

【可変要素】
- S-1: 属性依存（male/singular範囲内）
- M2-3: 属性無関係
- O1-5: 属性依存（male/singular所有格）
```

### ✅ **検証項目**

- [ ] 全単語がスロットに分類されている
- [ ] 絶対順序が正しい
- [ ] 固定要素(Aux・V)が特定されている
- [ ] 属性依存スロットが明確になっている

---

## 2.4 Stage 2: 語彙候補生成

### 🎯 **目的**
固定属性内での語彙候補の列挙

### 📋 **作業内容**
属性制約下でのパラフレーズ候補生成のみ

### 🚫 **禁止事項**
属性変更・整合性チェック・文構築

### 📝 **手順**

1. 固定要素(Aux・V)を除外
2. 属性無関係スロット（M1, M2等）の語彙候補生成
3. 属性依存スロット（S, O1等）の固定属性内候補生成
4. 同一人称制約チェック（主語-目的語の組み合わせで意味的不自然さがないか）
5. 各候補の属性整合性確認

### ⚠️ **同一人称制約チェック**

```
注意が必要な組み合わせ:
- 主語 "I" + 目的語 "me" → "I told me a secret." (意味的に不自然)
- 主語 "You" + 目的語 "you" → "You saw you." (再帰的でない文脈では不自然)
- 主語 "We" + 目的語 "us" → "We helped us." (意味的に不自然)

例外的に自然な場合:
- "I like me." → 自己肯定的文脈では可能
- "You be you." → 慣用表現では可能
```

### 📤 **出力例**

```
属性固定: male/singular

【S-1候補】（male/singularのみ）
- He
- My brother  
- The man
- John
- The male student

【M2-3候補】（属性無関係）
- fully
- completely
- gradually
- rapidly
- successfully

【O1-5語幹候補】（male/singular所有格固定）
- his strength
- his confidence
- his energy
- his stamina
- his mobility

⚠️ 同一人称チェック完了: 主語-目的語の意味的自然性確認済み
```

### ✅ **検証項目**

- [ ] 全候補が固定属性内に収まっている
- [ ] 属性違反の候補が含まれていない
- [ ] 同一人称による意味的不自然さが回避されている
- [ ] 固定要素が変更されていない
- [ ] 十分な候補数が確保されている

---

## 2.5 Stage 3: 組み合わせ構築

### 🎯 **目的**
固定属性内での有効な組み合わせ生成

### 📋 **作業内容**
属性制約下での組み合わせ作成のみ

### 🚫 **禁止事項**
新語彙追加・属性変更

### 📝 **手順**

1. 属性整合性の自動保証（同一属性のため）
2. 意味的自然性の確認
3. 疑問語重複チェック（必要に応じて）
4. 有効組み合わせの抽出
5. **（オプション）絶対順序テーブルの作成**
   - オプショナル要素（疑問詞・副詞）を含む場合のみ
   - 各スロットの出現位置を固定番号で定義
   - 空セルを含むテーブル構造を作成

### 📤 **出力例（通常形式）**

```
属性固定: male/singular
属性整合性: 自動保証（全てmale/singular）

【有効組み合わせ】
1. He + has + fully + recovered + his strength
2. My brother + has + completely + recovered + his confidence  
3. The man + has + gradually + recovered + his energy
4. John + has + rapidly + recovered + his stamina
```

### 📤 **出力例（絶対順序テーブル形式）** 🆕

**適用ケース**: 疑問詞・副詞等のオプショナル要素を含む母集団

```
【疑問文母集団: tellグループ】
V_group_key: "tell_question"

①M2-1   ②O2-2   ③Aux-3   ④S-4   ⑤V-5   ⑥O1-6   ⑦O2-7      ⑧M2-8
-        what     did      he     tell   her     -          at the store
-        -        did      he     tell   her     a secret   there
-        -        did      I      tell   him     a truth    in the kitchen
where    -        did      you    tell   me      a story    -

【ランダマイズ例】
- ①"where" + ②空 + ③"did" + ④"you" + ⑤"tell" + ⑥"her" + ⑦"a story" + ⑧"there"
  → "Where did you tell her a story there?"
  
- ①空 + ②"what" + ③"did" + ④"he" + ⑤"tell" + ⑥"her" + ⑦空 + ⑧"at the store"
  → "What did he tell her at the store?"

【効果】
- オプショナル要素の有無を独立に選択可能
- 2^n通りの構造バリエーション（n=オプショナルスロット数）
- 縦横無尽の組み合わせでも文法的整合性保証
```

**重要**: 絶対順序テーブルは通常の増殖では不要。疑問詞・副詞等のオプショナル要素を含む場合のみ作成。

### ✅ **検証項目**

- [ ] 全組み合わせが同一属性で構成されている
- [ ] 意味的に自然な組み合わせのみ抽出されている
- [ ] 疑問語重複がない（該当する場合）
- [ ] Aux・V固定性が維持されている
- [ ] （絶対順序テーブル使用時）空セルが適切に配置されている
- [ ] （絶対順序テーブル使用時）スロット番号が母集団内で一貫している

---

## 2.6 Stage 4: 最終構築・検証

### 🎯 **目的**
属性固定型完成文の構築と品質確認

### 📋 **作業内容**
文の組み立てと最終検証のみ

### 🚫 **禁止事項**
構造・語彙・属性の変更

### 📝 **手順**

1. 絶対順序での文構築
2. 属性整合性の最終確認
3. 文法的正確性の確認
4. 最終出力フォーマット整理

### 📤 **最終出力例**

```
【属性固定型増殖結果】（male/singular）

例文1: He has fully recovered his strength.
例文2: My brother has completely recovered his confidence.
例文3: The man has gradually recovered his energy.  
例文4: John has rapidly recovered his stamina.

【品質確認】
✓ 属性確認: 全例文がmale/singularで統一
✓ 代名詞整合: 全てhis/heで統一
✓ Aux・V固定: 全て"has recovered"で統一
✓ 構造維持: スロット構成が元文と一致
✓ 意味的自然性: 全文が自然に成立
```

### ✅ **最終検証項目（必須）**

- [ ] 全文が文法的に正しい
- [ ] 全文が同一属性で統一されている
- [ ] 構造が元文と同一
- [ ] 意味的に自然
- [ ] 絶対順序が維持されている
- [ ] Aux・Vが完全固定されている

---

## 2.7 V_group_key決定

### 🎯 **目的**
増殖した例文群を整合性パターンで分類し、V_group_keyを割り当てる

### 📋 **作業内容**
主語・目的語の人称パターンを分析し、V_group_keyを決定

### 🔑 **V_group_keyとは**

**定義**: 同じ動詞でも、主語・目的語の人称組み合わせパターンが異なる場合、別のV_group_keyを割り当てる識別子

**目的**: Rephraseランダマイズ時に、整合性のある例文群の中でのみランダマイズを実行するため

### 📝 **手順**

1. Stage 4で生成された4例文の主語・目的語パターンを分析
2. 人称パターンを特定（例: 三人称主語 + 三人称/一人称目的語）
3. V_group_keyを決定（例: `gave`, `gave_2`, `gave_3`）
4. 次のStage 5で別パターン増殖の必要性を判断

### 📤 **出力例**

```
【V_group_key決定】

元文: "She gave him a message."
Stage 4生成例文:
1. Yesterday, they gave us a secret.
2. Last weekend, Tom gave her curious friend an important message.
3. Earlier today, Emily gave me a warning.
4. She gave him a message.

【パターン分析】
- 主語: 三人称（they, Tom, Emily, She）
- 目的語: 三人称/一人称（us, her friend, me, him）

【V_group_key割り当て】
V_group_key: "gave"（三人称主語パターン）

【次のStage 5での増殖候補】
- V_group_key: "gave_2"（一人称主語パターン: I/We gave...）
- V_group_key: "gave_3"（二人称主語パターン: You gave...）
```

### ✅ **検証項目**

- [ ] 主語・目的語の人称パターンが明確に特定されている
- [ ] V_group_keyが適切に命名されている
- [ ] 次のStage 5での増殖候補が列挙されている

---

## 2.8 Stage 5: V_group_key分割増殖（オプション）

### 🎯 **目的**
整合性を保ちながら例文バリエーションを増やすため、別の人称パターンで追加増殖

### 📋 **作業内容**
Stage 4の例文をコピーし、主語・目的語のみを別の人称パターンに変更

### 🚫 **禁止事項**
Aux・V変更、構造変更、スロット順序変更

### 📝 **手順**

1. Stage 4で生成した4例文をコピー
2. 主語を新しい人称パターンに変更（例: 三人称 → 一人称）
3. 目的語を整合性のある人称に変更
4. 新しいV_group_keyを割り当て（例: `gave_2`）
5. 整合性と自然性を検証

### ⚠️ **整合性制約**

**必須ルール**: 主語と目的語が同一人称にならないよう注意

```
❌ 避けるべき組み合わせ:
- I gave me → 意味的に不自然
- We gave us → 意味的に不自然

✅ 推奨される組み合わせ:
- I gave him/her/them → 自然
- We gave you/him/her/them → 自然
```

### 📤 **出力例**

```
【Stage 5: V_group_key分割増殖】

元のV_group_key: "gave"（三人称主語パターン）
新しいV_group_key: "gave_2"（一人称主語パターン）

【Stage 4の例文】（gave）
1. Yesterday, they gave us a secret.
2. Last weekend, Tom gave her curious friend an important message.
3. Earlier today, Emily gave me a warning.
4. She gave him a message.

【Stage 5の例文】（gave_2）
1. Yesterday, we gave Tom a secret.
2. Last weekend, I gave her curious friend an important message.
3. Earlier today, we gave Emily a warning.
4. I gave him a message.

【変更内容】
- 主語: 三人称（they, Tom, Emily, She）→ 一人称（we, I, we, I）
- 目的語: そのまま維持（整合性確保）
- Aux・V: 完全固定（gave → gave）
- 構造: 維持
```

### ✅ **検証項目**

- [ ] 主語が新しい人称パターンに変更されている
- [ ] 目的語が主語と同一人称にならないことを確認
- [ ] Aux・Vが完全固定されている
- [ ] 構造が元文と同一
- [ ] 新しいV_group_keyが割り当てられている
- [ ] 全文が意味的に自然

### 🔄 **複数パターン展開例**

```
元文: "She gave him a message."

V_group_key: "gave"（三人称主語）
→ Stage 4で4例文生成

V_group_key: "gave_2"（一人称主語）
→ Stage 5で4例文生成

V_group_key: "gave_3"（二人称主語）
→ Stage 5で4例文生成

【合計】12例文（各V_group_key内で整合性保持）
→ Rephraseランダマイズ時、各V_group_key内でのみランダマイズ実行
```

### 💡 **Stage 5のメリット**

1. **増殖効率の向上**: 同じ動詞で複数パターンを作成可能
2. **整合性の保持**: 各V_group_key内で整合性が保証される
3. **作業の簡便性**: Stage 4の例文をコピーして主語・目的語のみ変更
4. **安全性**: Aux・V固定により文法破綻のリスクなし

---

# Part 3: 実践ガイド

## 3.1 ChatGPTへの指示例

### 📋 **Stage 0指示例（属性統一宣言）**

```
【Stage 0: 属性統一宣言】
この仕様書v2.0のStage 0に基づき、以下の例文の属性統一宣言を実行してください。
語彙変更・構造分析は行わず、属性の特定と統一宣言のみ行ってください。

例文: "He has fully recovered his strength."
指定属性: female/singular（male → femaleに変更して増殖）

出力形式:
元文属性: S=[gender]/[number]
属性統一宣言: このセッションでは「[指定属性]」に属性を統一し...
【重要】別セッションでの属性変更は完全に可能
禁止事項確認（このセッション内のみ）: [属性違反要素のリスト]
```

---

### 🔍 **Stage 1指示例（構造分析）**

```
【Stage 1: 構造分析】
Stage 0の属性固定宣言を受けて、Stage 1の構造分析のみを実行してください。
属性変更・語彙変更・増殖は行わず、スロット分解と絶対順序の特定のみ行ってください。

出力形式:
- S-X: [内容] ([固定属性] - 固定属性)
- Aux-X: [内容] (完全固定)
- [その他スロット]-X: [内容] (属性依存/属性無関係)
```

---

### 📝 **Stage 2指示例（語彙候補生成）**

```
【Stage 2: 語彙候補生成】
Stage 1の結果を受けて、Stage 2の固定属性内語彙候補生成のみを実行してください。
属性変更・組み合わせ作成は行わず、固定属性の範囲内での候補生成のみ行ってください。

⚠️ 重要制約:
1. 固定属性以外の要素は一切使用しない
2. 同一人称の主語-目的語組み合わせ（I+me, You+you, We+us）の意味的不自然さに注意
3. 動詞の性質を考慮した自然な組み合わせのみ生成

出力形式:
属性固定: [指定属性]
S-X候補（[指定属性]のみ）: [候補リスト]
[属性無関係スロット]候補: [候補リスト]
[属性依存スロット]候補（[指定属性]所有格固定）: [候補リスト]
⚠️ 同一人称チェック完了: [確認メッセージ]
```

---

### 🔗 **Stage 3-4指示例（組み合わせ・完成）**

```
【Stage 3: 組み合わせ構築】
Stage 2の語彙候補を受けて、Stage 3の組み合わせ構築のみを実行してください。
新語彙追加・属性変更は行わず、有効な組み合わせの作成のみ行ってください。

【Stage 4: 最終構築・検証】
Stage 3の組み合わせを受けて、Stage 4の最終構築・検証を実行してください。
構造・語彙・属性の変更は行わず、文の組み立てと品質確認のみ行ってください。

出力形式:
【属性固定型増殖結果】（[指定属性]）
例文1: [完成文]
例文2: [完成文]
例文3: [完成文]
例文4: [完成文]

【品質確認】
✓ 属性確認: [確認結果]
✓ 代名詞整合: [確認結果]
✓ Aux・V固定: [確認結果]
✓ 構造維持: [確認結果]
✓ 意味的自然性: [確認結果]
```

---

## 3.2 複数属性展開戦略

### 📊 **4属性完全カバー戦略**

```
元文: "He has fully recovered his strength."

【実行計画】
セッション1: male/singular固定 → 4例文生成
セッション2: female/singular固定 → 4例文生成  
セッション3: neutral/singular固定 → 4例文生成
セッション4: neutral/plural固定 → 4例文生成

【最終結果】
16例文の属性別データベース完成
→ Rephraseランダマイズシステムでの活用準備完了
```

### 🎯 **属性別データベース構築の実例**

**セッション1: male/singular固定**
```
1. He has fully recovered his strength.
2. My brother has completely recovered his confidence.
3. The man has gradually recovered his energy.
4. John has rapidly recovered his stamina.
```

**セッション2: female/singular固定**
```
1. She has fully recovered her strength.
2. My sister has completely recovered her confidence.
3. The woman has gradually recovered her energy.
4. Mary has rapidly recovered her stamina.
```

**セッション3: neutral/singular固定**
```
1. The patient has fully recovered their strength.
2. The athlete has completely recovered their stamina.
3. The child has gradually recovered their energy.
4. The student has successfully recovered their confidence.
```

**セッション4: neutral/plural固定**
```
1. They have fully recovered their strength.
2. The patients have completely recovered their stamina.
3. The athletes have gradually recovered their energy.
4. The students have successfully recovered their confidence.
```

---

## 3.3 最終提出フォーマット

```
【例文増殖完了報告】
元例文数: [数]
生成例文数: 4例文
実行Stage: Stage 0～4 全完了 ✅

【検証結果】
- Aux・V完全固定: ✅
- 属性統一維持: ✅  
- 文法整合性: ✅
- 多様性達成: ✅

【生成例文】
1. [例文1]
2. [例文2] 
3. [例文3]
4. [例文4]

【属性情報】
- 固定属性: [gender]/[number]
- 主語候補数: [数]
- 副詞候補数: [数]
- 目的語候補数: [数]
```

---

# Part 4: 補足

## 4.1 エラー検出・リカバリー

### 🚨 **致命的エラー検出アラート**

以下の行為は**即座に作業停止**し、仕様書再読を義務付ける：

```
❌ 【CRITICAL ERROR】Aux・V変更検出
検出例: "lie" → "lies", "got" → "get"
→ 🚨 作業即座停止、仕様書再読必須

❌ 【CRITICAL ERROR】属性混在検出  
検出例: 同一セッション内で "I" と "He" の混在
→ 🚨 作業即座停止、理解度確認再実行

❌ 【CRITICAL ERROR】Stage スキップ検出
検出例: Stage 0未完了での Stage 1実行
→ 🚨 作業即座停止、手順再確認
```

### 📋 **セルフチェック必須リスト**

各Stageで必ず以下を確認：

```
✅ 動詞形が一切変更されていない
✅ 主語の属性が統一されている  
✅ 前Stageの確認マークが存在する
✅ 文法破綻文が生成されていない
```

### 🔄 **理解失敗時のリカバリー手順**

```
1. 作業即座停止
2. 該当セクションの仕様書再読
3. 理解度確認再実行（Q1-Q3）
4. Stage 0から再開始
```

---

## 4.2 トラブルシューティング

### ❓ **よくある問題と対処法**

| 問題 | 原因 | 対処法 |
|------|------|-------|
| 属性が混在してしまう | Stage 0での属性宣言が不十分 | Stage 0を再実行し、禁止事項を明確化 |
| 動詞が変化してしまう | Aux・V固定原則の理解不足 | 理解度確認Q1を再実行 |
| 意味的に不自然な文 | 同一人称制約の見落とし | Stage 2の同一人称チェックを再実行 |
| 多様性が不足 | Aux・V以外のスロットで変化が少ない | Stage 2で候補数を増やす |

---

## 4.3 スロット構造リファレンス

### 🏗️ **標準スロット構成**

| スロット | 内容例 | 属性制約 | 増殖時の扱い |
|-----------|---------|----------|-------------|
| M1 | That afternoon, at the crucial point | time_place | 自由変更可能（属性無関係） |
| S | the manager, he, my brother | **gender, number** | **増殖時固定（核心属性）** |
| Aux | had to make, has, will | - | 完全固定（変更禁止） |
| V | make, recover, lie | - | 完全固定（変更禁止） |
| O1 | the committee, his strength | number, type | Sの属性に依存する場合のみ制約 |
| O2 | deliver the proposal | compatibleO1Type | O1との整合性維持 |
| M2 | fully, completely | - | 自由変更可能（属性無関係） |
| C1 | because he feared | **pronoun_owner** | **Sの属性に完全依存** |
| C2 | - | - | 必要に応じて |
| M3 | so the outcome would reflect | result_owner | 所有者に基づく属性整合 |

### 🔤 **属性固定の優先順位**

1. **最優先**: S（主語）の gender, number → これが全体の属性を決定
2. **従属**: M2, C1の代名詞 → Sの属性に完全従属
3. **独立**: M1, O2等 → 属性無関係で自由変更可能

---

## 4.4 次バージョン拡張予定（v3.0）

- 属性固定型スロット属性リストの詳細例（Excel/JSON）
- 複数属性同時管理マトリクス（advanced users向け）
- 属性固定型増殖の自動化スクリプト
- Rephraseシステムとの直接連携API

---

## 🔑 **保存用備考（v2.0完全再構築版）**

この仕様書を ChatGPT にアップロードし、属性固定型例文増殖依頼時の基準ファイルとする。

**v2.0完全再構築版の改善点**:
- ✅ 重複内容の完全削除（同じ説明が複数回登場する問題を解消）
- ✅ 論理的な構成（Part 1-4: 導入 → 手順 → 実践 → 補足）
- ✅ "Stage"への統一（"段階"との混在を解消）
- ✅ 読みやすさの向上（往復する流れを一方向に整理）

ファイル名推奨：`example_expansion_spec_v2.0_restructured.md`（完全再構築版）

---

**作成日**: 2025-08-05  
**再構築日**: 2025-12-31  
**次回更新予定**: v3.0（自動化機能統合）
