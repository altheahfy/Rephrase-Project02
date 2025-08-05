# Rephraseプロジェクト例文増殖設計仕様書（v2.0）

作成日: 2025-08-05  
作成者: ChatGPT（Rephraseプロジェクト参謀本部）  
用途: ChatGPT に例文増殖を依頼する際の標準仕様ガイド  
重要更新: 属性固定型増殖への全面転換

---

## 🎯 **目的**

**属性固定型増殖**により、Rephraseランダマイズシステム用のスロット別データベースを構築する。  
**核心原則**: 一つの増殖作業では一つの属性セット（gender, number等）のみを固定し、その属性内でのみ語彙パラフレーズを行う。  
これにより「He has gradually recovered her stamina.」等の文法破綻文の生成を根本的に防止し、スロット別個別ランダマイズに対応したデータを提供する。

---

## � **属性固定型増殖の核心原則**

### 🔒 **一つの増殖=一つの属性固定**
- **絶対ルール**: 一回の増殖作業では、主語（S）の属性（gender, number）を固定する
- **例**: 「He has fully recovered his strength.」の増殖では、male/singularの属性のみで増殖
- **禁止**: 同一増殖内でmale/female、singular/pluralの混在は一切行わない

### 🎯 **属性別独立増殖戦略**
```
元文: "He has fully recovered his strength."

増殖A（male/singular固定）:
- He has fully recovered his strength.
- My brother has completely recovered his stamina.
- The man has gradually recovered his energy.
- John has successfully recovered his confidence.

増殖B（female/singular固定）:
- She has fully recovered her strength.
- My sister has completely recovered her stamina.
- The woman has gradually recovered her energy.
- Mary has successfully recovered her confidence.

増殖C（neutral/singular固定）:
- The patient has fully recovered their strength.
- The athlete has completely recovered their stamina.
- The child has gradually recovered their energy.
- The student has successfully recovered their confidence.
```

### ⚡ **Rephraseランダマイズ対応設計**
- **スロット別データベース**: 各スロットが独立してランダム選択される仕組みに対応
- **属性整合性保証**: 同一属性内の要素のみが組み合わされるため文法破綻を防止
- **代名詞自動補正**: ランダマイズ時の動的補正処理で正しい代名詞に変換

## 📝 **スロット構造と属性仕様**

### 🏗️ **標準スロット構成**
各例文は以下の標準スロットで構成する。属性固定型増殖では、これらのスロットが属性整合性を保ったまま増殖される。

| スロット | 内容例 | 属性制約 | 増殖時の扱い |
|-----------|---------|----------|-------------|
| M1 | That afternoon at the crucial point | time_place | 自由変更可能（属性無関係） |
| S | the manager who had recently taken charge | **gender, number** | **増殖時固定（核心属性）** |
| Aux | had to make | - | 完全固定（変更禁止） |
| V | make | - | 完全固定（変更禁止） |
| O1 | the committee responsible for implementation | number, type | Sの属性に依存する場合のみ制約 |
| O2 | deliver the final proposal flawlessly | compatibleO1Type | O1との整合性維持 |
| M2 | even though he was under intense pressure | **pronoun_owner** | **Sの属性に完全依存** |
| C1 | because he feared upsetting her | **pronoun_owner** | **Sの属性に完全依存** |
| C2 | - | - | 必要に応じて |
| M3 | so the outcome would reflect their full potential | result_owner | 所有者に基づく属性整合 |

### 🔤 **属性固定の優先順位**
1. **最優先**: S（主語）の gender, number → これが全体の属性を決定
2. **従属**: M2, C1の代名詞 → Sの属性に完全従属
3. **独立**: M1, O2等 → 属性無関係で自由変更可能

### � **QuestionType（疑問語）制約**
| 属性値 | 増殖時の制約 | 対処法 |
|--------|-------------|--------|
| wh-word | 1文につき1つまで | 疑問語候補は属性とは独立して管理 |
| - | 制約なし | 通常のパラフレーズ対象 |

---

## 🧩 **属性固定型増殖のフローチャート**

### 📋 **増殖前の属性決定フェーズ**
```
STEP 1: 元文の主語（S）属性を特定
├── gender: male/female/neutral
├── number: singular/plural
└── animacy: animate/inanimate

STEP 2: 増殖対象属性を決定
├── Option A: 同一属性で増殖（male/singular → male/singular）
├── Option B: 性別変更増殖（male/singular → female/singular）
├── Option C: 数変更増殖（male/singular → male/plural）
└── Option D: 中性化増殖（male/singular → neutral/singular）

STEP 3: 属性固定宣言
例: 「この増殖ではfemale/singularに固定して実行する」
```

### 🔄 **属性別データベース構築戦略**
```
元文: "He has fully recovered his strength."

戦略1: 4回の独立増殖
├── 増殖A: male/singular固定 → 4例文生成
├── 増殖B: female/singular固定 → 4例文生成
├── 増殖C: neutral/singular固定 → 4例文生成
└── 増殖D: neutral/plural固定 → 4例文生成

結果: 16例文のデータベース（各属性4例文ずつ）
→ Rephraseランダマイズ時の組み合わせ爆発に対応
```

### ⚡ **Rephraseシステムでの活用フロー**
```
ランダマイズ実行時:
1. 各スロットから独立して要素を選択
2. 選択されたSの属性を確認
3. 他スロットの代名詞を動的補正
4. 文法的に整合した文を出力

例: S="The woman" + M2="fully" + O1="his strength"
→ 自動補正: "The woman has fully recovered her strength."
```

---

## 🌱 **属性固定型5段階増殖プロセス**

**❗重要**: 属性固定宣言後、各段階を独立実行し、前段階完了確認後に次段階進行。

### 🎯 **段階0: 属性固定宣言フェーズ**

**目的**: 増殖対象属性の明確な決定と宣言  
**作業内容**: 属性選択と固定宣言のみ  
**禁止事項**: 語彙変更・構造分析・増殖作業

**手順**:
1. 元文の主語（S）属性を特定
2. 増殖対象属性を選択（male/female/neutral × singular/plural）
3. 属性固定を明確に宣言
4. 増殖範囲の確認

**出力例**:
```
元文: "He has fully recovered his strength."
元文属性: S=male/singular

増殖宣言: 
このセッションでは「male/singular」に属性を固定し、
この属性の範囲内でのみ語彙パラフレーズを実行します。

禁止事項確認:
- 「She/Her」等のfemale要素は一切使用しない
- 「They/Their」等のplural要素は一切使用しない
- 「The patient/The child」等のneutral要素は一切使用しない
```

**検証項目**:
- [ ] 元文の属性が正確に特定されている
- [ ] 増殖対象属性が明確に選択されている
- [ ] 禁止事項が明確に理解されている

---

### 🔍 **段階1: 構造分析フェーズ**

**目的**: 元例文のスロット構成の完全把握  
**作業内容**: スロット分解と絶対順序の特定のみ  
**禁止事項**: 語彙変更・属性変更・増殖作業

**手順**:
1. 元例文を単語レベルで分析
2. 各要素のスロット番号を絶対順序で割り当て
3. Aux・Vを固定要素として特定
4. 属性依存スロット（M2, C1等）の特定

**出力例**:
```
元文: "He has fully recovered his strength."
属性固定: male/singular

構造分析結果:
- S-1: He (male/singular - 固定属性)
- Aux-2: has (完全固定)
- M2-3: fully (属性無関係)
- V-4: recovered (完全固定)
- O1-5: his strength (属性依存 - male/singularに固定)
```

**検証項目**:
- [ ] 全単語がスロットに分類されている
- [ ] 絶対順序が正しい
- [ ] 固定要素(Aux・V)が特定されている
- [ ] 属性依存スロットが明確になっている

---

### � **段階2: 属性内語彙候補生成フェーズ**

**目的**: 固定属性内での語彙候補の列挙  
**作業内容**: 属性制約下でのパラフレーズ候補生成のみ  
**禁止事項**: 属性変更・整合性チェック・文構築

**手順**:
1. 固定要素(Aux・V)を除外
2. 属性無関係スロット（M1, M2等）の語彙候補生成
3. 属性依存スロット（S, O1等）の固定属性内候補生成
4. 各候補の属性整合性確認

**出力例**:
```
属性固定: male/singular

S-1候補（male/singularのみ）:
- He
- My brother  
- The man
- John
- The male student

M2-3候補（属性無関係）:
- fully, completely, gradually, rapidly, successfully

O1-5語幹候補（male/singular所有格固定）:
- his strength, his confidence, his energy, his stamina, his mobility
```

**検証項目**:
- [ ] 全候補が固定属性内に収まっている
- [ ] 属性違反の候補が含まれていない
- [ ] 固定要素が変更されていない
- [ ] 十分な候補数が確保されている

---

### 🔗 **段階3: 属性内組み合わせ構築フェーズ**

**目的**: 固定属性内での有効な組み合わせ生成  
**作業内容**: 属性制約下での組み合わせ作成のみ  
**禁止事項**: 新語彙追加・属性変更

**手順**:
1. 属性整合性の自動保証（同一属性のため）
2. 意味的自然性の確認
3. 疑問語重複チェック（必要に応じて）
4. 有効組み合わせの抽出

**出力例**:
```
属性固定: male/singular
属性整合性: 自動保証（全てmale/singular）

有効組み合わせ:
1. He + fully + his strength
2. My brother + completely + his confidence  
3. The man + gradually + his energy
4. John + rapidly + his stamina
```

**検証項目**:
- [ ] 全組み合わせが同一属性で構成されている
- [ ] 意味的に自然な組み合わせのみ抽出されている
- [ ] 疑問語重複がない（該当する場合）

---

### ✅ **段階4: 最終構築・検証フェーズ**

**目的**: 属性固定型完成文の構築と品質確認  
**作業内容**: 文の組み立てと最終検証のみ  
**禁止事項**: 構造・語彙・属性の変更

**手順**:
1. 絶対順序での文構築
2. 属性整合性の最終確認
3. 文法的正確性の確認
4. 最終出力フォーマット整理

**最終出力例**:
```
属性固定型増殖結果（male/singular）:

例文1: He has fully recovered his strength.
例文2: My brother has completely recovered his confidence.
例文3: The man has gradually recovered his energy.  
例文4: John has rapidly recovered his stamina.

属性確認: 全例文がmale/singularで統一 ✓
代名詞整合: 全てhis/heで統一 ✓
```

**最終検証項目**:
- [ ] 全文が文法的に正しい
- [ ] 全文が同一属性で統一されている
- [ ] 構造が元文と同一
- [ ] 意味的に自然
- [ ] 絶対順序が維持されている

### � **属性固定原則（最重要）**
- **核心ルール**: 一回の増殖作業では、主語（S）の属性（gender, number）を絶対に変更しない
- **例**: 「He has fully recovered his strength.」→ male/singularで固定し、全例文がmale/singular
- **厳格禁止**: 「He/She/They」の混在は同一増殖内では一切行わない

### �💡 **構造維持原則**
- **スロット構成は完全固定**: 元例文にあるスロットのみ増殖対象。新規スロット追加・削除禁止
- **Aux・V完全固定**: 助動詞・動詞は一切変更しない。時制・語法・文型を維持
- **品詞カテゴリ固定**: 各スロットの品詞カテゴリ（名詞句・副詞句・形容詞等）は維持

### � **パラフレーズ原則**
- **属性内語彙パラフレーズ**: 固定された属性の範囲内でのみ語彙を置き換える
- **代名詞完全整合**: 属性が固定されているため、代名詞の一致は自動的に保証される
- **意味的自然性**: パラフレーズ後も文全体が自然で論理的に成立

### 🎯 **ランダマイズ対応設計**
- **スロット別データベース**: 各属性別に整理されたスロット要素のデータベース構築
- **動的補正準備**: ランダマイズ時の代名詞補正のための属性情報付与
- **組み合わせ爆発対応**: 属性別データにより、より多様な組み合わせパターンを提供

---

## 🌱 **段階分割型例文増殖プロセス**

**❗重要**: 各段階を独立して実行し、前段階の完了確認後に次段階に進むこと。

### 🔍 **段階1: 構造分析フェーズ**

**目的**: 元例文のスロット構成の完全把握  
**作業内容**: スロット分解と絶対順序の特定のみ  
**禁止事項**: 語彙変更・属性定義・増殖作業

**手順**:
1. 元例文を単語レベルで分析
2. 各要素のスロット番号を絶対順序で割り当て
3. Aux・Vを固定要素として特定
4. スロット構成の完全性をチェック

**出力例**:
```
元文: "He has fully recovered his strength."
分析結果:
- S-2: He
- Aux-3: has (固定)
- M2-5: fully  
- V-4: recovered (固定)
- O1-6: his strength
```

**検証項目**:
- [ ] 全単語がスロットに分類されている
- [ ] 絶対順序が正しい
- [ ] 固定要素(Aux・V)が特定されている

---

### 📝 **段階2: 属性定義フェーズ**

**目的**: 各スロットの文法属性の正確な定義  
**作業内容**: 属性タグの付与のみ  
**禁止事項**: 語彙変更・増殖作業

**手順**:
1. Sの基本属性定義 (number, gender, animacy)
2. 所有関係の特定 (owner属性)
3. QuestionType属性の確認
4. 依存関係マップの作成

**出力例**:
```
S-2: He
- number: singular
- gender: male  
- animacy: animate

M2-5: fully
- QuestionType: - (疑問語以外)

O1-6: his strength  
- owner: S (所有格はSに依存)
- type: individual
```

**検証項目**:
- [ ] 全スロットに必要属性が付与されている
- [ ] 依存関係が明確になっている
- [ ] QuestionType属性が適切に設定されている

---

### 🔤 **段階3: 語彙候補生成フェーズ**

**目的**: スロット別語彙候補の列挙  
**作業内容**: パラフレーズ候補の生成のみ  
**禁止事項**: 整合性チェック・文構築

**手順**:
1. 固定要素(Aux・V)を除外
2. 変更可能スロットの語彙候補を独立生成
3. 各候補に同じ属性構造を付与
4. 候補数の妥当性確認

**出力例**:
```
S-2候補:
- He (gender: male, number: singular)
- She (gender: female, number: singular)  
- The patient (gender: neutral, number: singular)
- My brother (gender: male, number: singular)

M2-5候補:
- fully, completely, gradually, rapidly, successfully

O1-6語幹候補:
- strength, confidence, energy, stamina, mobility
```

**検証項目**:
- [ ] 各スロットに十分な候補がある
- [ ] 候補の属性が統一されている
- [ ] 固定要素が変更されていない

---

### � **段階4: 整合性マトリクス適用フェーズ**

**目的**: 文法的整合性を保つ組み合わせの生成  
**作業内容**: 属性ルールに基づく組み合わせ作成  
**禁止事項**: 新しい語彙の追加

**手順**:
1. 所有格補正ルールの適用
2. 疑問語重複チェック
3. 属性整合性の検証
4. 有効な組み合わせの抽出

**所有格補正ルール**:
| S.gender | S.number | 所有格 |
|----------|----------|-------|
| male     | singular | his   |
| female   | singular | her   |
| neutral  | singular | their |
| any      | plural   | their |

**出力例**:
```
組み合わせ1: He + fully + his strength
組み合わせ2: She + completely + her confidence  
組み合わせ3: The patient + gradually + their energy
組み合わせ4: My brother + rapidly + his stamina
```

**検証項目**:
- [ ] 所有格が主語と一致している
- [ ] 疑問語が1つ以下
- [ ] 全ての属性ルールが遵守されている

---

### ✅ **段階5: 最終構築・検証フェーズ**

**目的**: 完成文の構築と品質確認  
**作業内容**: 文の組み立てと最終検証  
**禁止事項**: 構造・語彙の変更

**手順**:
1. 絶対順序での文構築
2. 文法的正確性の確認
3. 自然性の検証
4. 最終出力フォーマット整理

**最終出力例**:
```
例文1: He has fully recovered his strength.
例文2: She has completely recovered her confidence.
例文3: The patient has gradually recovered their energy.  
例文4: My brother has rapidly recovered his stamina.
```

**最終検証項目**:
- [ ] 全文が文法的に正しい
- [ ] 構造が元文と同一
- [ ] 意味的に自然
- [ ] 絶対順序が維持されている

---

---

### 🚨 **段階間の移行ルール（属性固定版）**

1. **属性固定確認**: 段階0で属性が明確に固定され、全段階を通じて変更されない
2. **前段階完了確認**: 検証項目の全てにチェックが入ってから次段階へ
3. **属性違反時の停止**: 固定属性以外の要素が混入した場合は即座に停止・修正
4. **段階スキップ禁止**: 必ず順番通りに実行（段階0から段階4まで）
5. **並行処理禁止**: 複数段階を同時に実行しない

---

## ⚠ **属性固定型増殖の留意点**

### 🔒 **絶対禁止事項**
- **属性混在**: 同一増殖内でのmale/female、singular/pluralの混在は絶対禁止
- **代名詞破綻**: 「He has recovered her strength.」等の属性不整合文の生成禁止
- **構造変更**: スロット構成・Aux/V・品詞カテゴリの変更禁止

### 💡 **品質保証項目**
- **属性統一性**: 全例文が同一属性（gender, number）で統一されている
- **代名詞整合**: 所有格代名詞が主語の属性と完全に一致している
- **文法正確性**: 全文が文法的に正しく、自然に成立している
- **パラフレーズ適切性**: 語彙レベルでの適切な置き換えのみ実行されている

### 🎯 **Rephraseシステム連携**
- **スロット別データベース**: 各属性別に整理されたスロット要素データベース
- **動的補正対応**: ランダマイズ時の代名詞補正処理への適切な情報提供
- **組み合わせ最適化**: 属性固定により、より安全で多様な組み合わせ生成

---

## 💾 **ChatGPTへの属性固定型段階的指示例**

### 📋 **段階0指示例（属性固定宣言）**
```
【段階0: 属性固定宣言】
この仕様書v2.0の段階0に基づき、以下の例文の属性固定宣言を実行してください。
語彙変更・構造分析は行わず、属性の特定と固定宣言のみ行ってください。

例文: "He has fully recovered his strength."
指定属性: female/singular（male → femaleに変更して増殖）

出力形式:
元文属性: S=[gender]/[number]
増殖宣言: このセッションでは「[指定属性]」に属性を固定し...
禁止事項確認: [属性違反要素のリスト]
```

### 🔍 **段階1指示例（構造分析）**
```
【段階1: 構造分析】
段階0の属性固定宣言を受けて、段階1の構造分析のみを実行してください。
属性変更・語彙変更・増殖は行わず、スロット分解と絶対順序の特定のみ行ってください。

出力形式:
- S-X: [内容] ([固定属性] - 固定属性)
- Aux-X: [内容] (完全固定)
- [その他スロット]-X: [内容] (属性依存/属性無関係)
```

### 📝 **段階2指示例（語彙候補生成）**
```
【段階2: 属性内語彙候補生成】
段階1の結果を受けて、段階2の固定属性内語彙候補生成のみを実行してください。
属性変更・組み合わせ作成は行わず、固定属性の範囲内での候補生成のみ行ってください。

出力形式:
属性固定: [指定属性]
S-X候補（[指定属性]のみ）: [候補リスト]
[属性無関係スロット]候補: [候補リスト]
[属性依存スロット]候補（[指定属性]所有格固定）: [候補リスト]
```

### 🔗 **段階3-4指示例（組み合わせ・完成）**
```
【段階3: 属性内組み合わせ構築】
【段階4: 最終構築・検証】
※同様に属性固定制約下での実行を指示
```

---

## 🎯 **複数属性展開の実行例**

### 📊 **4属性完全カバー戦略**
```
元文: "He has fully recovered his strength."

実行計画:
セッション1: male/singular固定 → 4例文生成
セッション2: female/singular固定 → 4例文生成  
セッション3: neutral/singular固定 → 4例文生成
セッション4: neutral/plural固定 → 4例文生成

最終結果: 16例文の属性別データベース完成
→ Rephraseランダマイズシステムでの活用準備完了
```

---

## 🛠 **次バージョン拡張予定（v3.0）**
- 属性固定型スロット属性リストの詳細例（Excel/JSON）
- 複数属性同時管理マトリクス（advanced users向け）
- 属性固定型増殖の自動化スクリプト
- Rephraseシステムとの直接連携API

---

## 🔑 **保存用備考（v2.0更新）**
この仕様書を ChatGPT にアップロードし、属性固定型例文増殖依頼時の基準ファイルとする。
**重要**: v1.2からv2.0への根本的転換により、文法破綻防止が実現された。
ファイル名推奨：`example_expansion_spec_v2.0.md`（属性固定型）

---

## 🤖 **ML Model 活用方針（2025年8月5日更新）**

### 📊 **属性固定型増殖でのML活用可能性**
- **現状評価**: 属性固定により文法破綻リスクが大幅減少、ML学習データの品質向上
- **学習対象**: 属性別パラフレーズパターンの自動学習
- **予測精度**: 属性制約により予測対象が明確化、精度向上が期待される

### 🎯 **属性固定型段階的活用戦略**
```
フェーズ1（現在）: 属性固定型手動増殖の確立
├── 各属性別での安定した例文生成プロセス構築
├── 品質保証基準の確立
└── Rephraseシステムとの連携テスト

フェーズ2（データ蓄積期）: 
├── 属性別例文データベースの体系的構築
├── 各属性での生成パターン分析
└── 属性間の一貫性検証

フェーズ3（ML統合期）:
├── 属性固定型ML学習モデルの開発
├── 属性別自動パラフレーズ生成
└── 品質保証付き自動増殖システム
```

### 💡 **属性固定がMLに与える利点**
- **学習データ品質**: 属性整合性が保証された高品質データセット
- **予測制約明確化**: 属性固定により学習対象が明確で過学習リスク減少
- **評価基準統一**: 属性別評価により客観的な品質測定が可能
