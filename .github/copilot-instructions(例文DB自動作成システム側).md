０．このシステムの目的
（１） アウトプット用文法.md（9,721行）
   ├─ 各文法解説（使役動詞、不定詞、関係節等）
   └─ 豊富な例文群（数百～数千）
   
（２）AI増殖（パラフレーズ・ランダマイズ）
   └─ 各例文を多様なバリエーションに拡張
   
（３） このシステムで自動分解
   ├─ 統一汎用パイプラインで文法解析
   ├─ Rephrase的スロット分解
   └─ Golden Test検証
   
（４）DB出力（完全トレーニングUI用）
   └─ ユーザーの学習データとして利用

１．全体フロー
以下は全て、CentralControllerに記述された「統一汎用パイプライン」で動かす。CentralController自身が実施することもあれば、チャンカーやハンドラーなど別スクリプトを呼ぶこともある。
（１）チャンク合体
チャンカーが、入力された例文に対して、spaCy等UDの依存関係を使って単語と単語の修飾・被修飾の関係性とどの単語が核なのかを特定し、「名詞」「動詞」「副詞」の3種類のチャンクにまとめる。形容詞チャンクは常に名詞チャンクと合体する。（例：a sleeping babyで名詞チャンク、など）
※ この際、依存関係が誤っているケースについてはspaCy自体を修正する。

（２）入れ子内の処理
入れ子構造を生む文法が無い例文は（４）からスタート。
①入れ子節・句の特定
CentralControllerが、（１）の結果や、spaCy等UDの言語ライブラリ、Rephraseライブラリを用いて、入れ子構造を持つ節（主語動詞以降の構造がある）・句（動詞以降の構造があり、主語は無い）を特定。
**入れ子トリガー検出**: 前置詞+VBG、関係詞、不定詞、接続詞を検出
**境界特定**: トリガーから文法的矛盾（上位動詞（ROOT依存関係を持つVERB_CHUNK）出現）または文末まで
**トリガー種別**:
- `prep_gerund`: 前置詞+VBG（after leaving、for helping等）
- `relative`: 関係詞（who/which/that/whose/whom）
- `infinitive`: 不定詞（to + VERB）
- `conjunction`: 従属接続詞（if/when/because/while/although等）

例文: "I became a writer after leaving a company."

親スロットレベル（主節処理）:
  ✅ 求められる動作: M1 = "after leaving a company" （1つに合体）
  ✅ NESTED_MERGE必要: PREP + VBG + NOUN → 1 PREP_CHUNK

サブスロットレベル（埋め込み節処理）:
  ✅ 求められる動作: sub-v="after leaving", sub-o1="a company" （分解）
  ❌ NESTED_MERGEが邪魔: "after leaving a company" → 1 PREP_CHUNK（分解不可）
```

**解決策**: `is_embedded` パラメータで2段階チャンク合体を制御

#### 必須実装パターン

```python
# ✅ 正解: 埋め込み節処理で is_embedded=True を強制指定
def _process_embedded_clause(self, tokens, parent_slot):
    """埋め込み節処理（is_embedded=True を自動設定）"""
    embedded_doc = self.nlp(segment_text)
    
    # ✅ is_embedded=True を強制（NESTED_MERGE抑制）
    result = self._execute_unified_pipeline(
        sentence=segment_text,
        doc=embedded_doc,
        is_embedded=True  # ← 必須！
    )
    
    # または
    chunks = self.chunker.chunk(embedded_doc, is_embedded=True)  # ← 必須！
```

#### ❌ 違反パターン（AST Linter検出）

```python
# ❌ 間違い: is_embedded指定なし
def _process_embedded_clause(self, tokens, parent_slot):
    embedded_doc = self.nlp(segment_text)
    
    # ❌ is_embedded=False（デフォルト）→ NESTED_MERGE実行 → 分解失敗
    result = self._execute_unified_pipeline(
        sentence=segment_text,
        doc=embedded_doc
        # ← is_embedded=True がない！


②文法検出
CentralControllerが、（１）の結果や、spaCy等UDの言語ライブラリ、Rephraseライブラリを用いて、入れ子内に使われている文法を検出する。文法検出するのはハンドラーではない。ハンドラーは呼ばれる側。

③ハンドラー招集
検出された文法の専門ハンドラーを招集する。5文型の部分（S, V, C1, O1, O2, C2）はCentralControllerが自ら担当する。

④claim
CentralControllerと各文法ハンドラーがそのチャンクに適したスロット（M1,S,Aux,M2,V,C1,O1,O2,C2,M3）をclaimする。その際には、Rephraseライブラリを用いて、パターンマッチングする。Rephraseライブラリは、あらかじめ例文・期待値のjsonからチャンクの語順のパターンとそのスロットを抽出し、登録しておく。その際、入れ子構造の文法が使われている例文については、（４）のプロセスに備えてマスク簡略化した主節レベル文のパターンも忘れずに登録しておく。なお、Rephraseライブラリのチャンク語順と権威ライブラリの依存関係は明確に分け、この段階では依存関係は使わないことに注意。
※【5文型判定の特別ルール】
✅ 基本: Rephraseライブラリ（チャンク語順パターン）
✅ 補助1: VerbNet（4,580動詞の文型情報）
✅ 補助2: 閉じた集合（LINKING_VERBS等、15-20語）
✅ 補助3: UD依存関係（C1 vs O1 vs O1O2 vs O1C2の明確な区別）

理由: 5文型判定の複雑性（動詞が複数文型を取る、品詞だけで区別不可）
承認: copilot-instructions.md "補助的に依存関係を使うのもOK"

※以下は実装例
【L1: 核検出】ROOT起点 + 埋め込み節
  - Universal Dependencies の依存構造（.dep_）で文の主述核を特定
  - ROOT（主動詞）、ccomp/xcomp/acl（埋め込み節）を検出
  - cop（コピュラ）の特殊処理（be動詞→Aux、述語側→V）
  
【L2: 修飾吸収】境界ルール厳守
  - 依存関係（det, amod, aux, nmod等）で修飾要素を1つのChunkに吸収
  - 名詞核: det/amod/compound/nummod吸収
  - 動詞核: aux/neg/prt/advmod吸収
  - ストッパー（独立チャンク化）: ccomp/xcomp/acl/relcl → サブスロット

【L2.3: 入れ子境界検出・チャンク合体】🆕 2025-11-12実装
  - 入れ子トリガー検出: 前置詞+VBG、関係詞、不定詞、接続詞
  - 境界特定: トリガーから文法的矛盾（上位スロット要素）または文末まで
  - チャンク合体: 境界内を1つのPREP_CHUNK/REL_CHUNK/INF_CHUNKに統合
  - 上位スロット: 個別チャンク維持（S/V/O/C）
  - 実装場所: src/chunking/phrase_chunker.py Line 237-468
  
【L3-A: UD→仮スロット決定木】
  - Universal Dependencies依存関係から仮スロットへマッピング
  - nsubj → S、iobj → O1、obj → O1/O2、obl → M等
  - 語彙枠（20動詞程度の最小辞書）で与格交替・必須前置詞判定
  
【L3-B: Rephraseパターン確定】
  - 仮スロットをRephraseライブラリ（Golden Test期待値）で最終確定・上書き
  - 既存 analyze_sentence() を改造して統合

**よくある間違い**:
- 固定トークンパターン（"It + VERB + ADJ + of + PRON + to + VERB"）では、語彙・修飾語の変化に対応不可
- Test 004失敗: "kind of her" → "very kind of her" で破綻（"very"のせいで順序が崩れる）
- パターン網羅性40%（6/15例文）の根本原因

**解決策**: チャンクベース設計
```
固定トークンパターン（従来、❌禁止）:
  "It" + "VERB" + "ADJ" + "of" + "PRON" + "to" + "VERB"
  → "very kind of her" に対応不可（"very"が入ると破綻）

チャンクベースパターン（新方式、✅必須）:
  PRON_CHUNK + VERB_CHUNK + [ADV_CHUNK]* + ADJ_CHUNK + [PREP_CHUNK]? + INF_CHUNK
  → "kind of her" も "very kind of her" も同じパターンで処理可能
  → 副詞は位置不問（[ADV_CHUNK]*）、前置詞はオプショナル（[PREP_CHUNK]?）
```

（３）マスク簡略化
CentralControllerは、claimまで完了した入れ子節・句内に対して、代表語句のみに絞るか（The man who has a red carなら「Tha man」）、「Masked_infinitive」などのプレイスホルダーに変え、上位スロットの主節レベル文を処理するための下地を作る。（例：The man who has a red car lives here.なら、The man lives here.　It is kind of her to help me.なら、It is kind of her Maskedinfinitive.）

（４）上位スロット主節レベル文の再帰処理
マスクで簡略化された箇所を含む上位スロット主節レベル文に対して、（２）②③④の処理を再帰的に繰り返す。（２）④で述べたように、Rephraseライブラリにはこのためのプレイスホルダーを持つパターンが登録されている。(It:S_1 is:V kind:C1 of her:M1 Maskedinfinitive:S_2.→副詞はどこに入ってもいいよう、パターンには副詞許容力を持たせる必要あり。)

（５）スコアリングシステムによる判断と最終承認
CentralControllerは様々な情報に重みづけをしたArbiterのスコアリングシステムにより、自らや各文法ハンドラーが出したclaimに対して最終判断し、承認となれば各チャンクに対してスロット名を決定する。

１-A．段階的リリース戦略（2025-12-19確立） 🚀 **市場タイミング重視**

**背景**: AI市場の急速な普及とChatGPTアプリ展開を踏まえ、完全実装を待たずに段階的リリースを実施する。

### フォールバック機構の設計原則

**（A）UI破綻防止の絶対ルール**: 埋め込み節（sub-slot表示対象）について、1箇所でも sub-slot が確定できないなら、埋め込み節全体を sub-slot化しない。代わりに 埋め込み節"全文"を、上位スロット（親スロット）に1塊で格納する（例：M1 なら M1 に全文）。「一部だけフォールバック塊」や「sub-slotから要素が抜ける」ことは禁止。

**（B）親スロット決定タイミング**: 親スロット（例：不定詞の _parent_slot）を 埋め込み節だけで確定しない。親スロットは マスク簡略化後の上位スロット主節レベル文（masked_doc）を Rephrase判定した結果（placeholder_slot / main_slots のプレースホルダー位置）で確定する。したがって、埋め込み節処理 _process_embedded_clause() は「sub-slot化に成功したか否か」だけを返し、親スロット確定は既存の⑨/⑩（統合側）で行う。

### 実装方針（最小工事で通す）

大工事は不要。既存の構造（_process_embedded_clause → *_embedded_result → _merge_embedded_sub_slots / _apply_infinitive_embedded_merge）に "完全性判定フラグ" を追加し、統合時に分岐させる。

### UI対応と段階的進化

**フォールバック状態の表示**:
```javascript
// training UI側
if (result.metadata.expansion_status === 'fallback') {
  // 例: S = "The man who has a red car" （サブスロット: 未対応）
} else {
  // 例: S = "The man", sub-s = "who", sub-v = "has", sub-o1 = "a red car"
}
```

**段階的進化の流れ**:
1. ハンドラー未実装時: 埋め込み節全文が親スロットに格納
2. ハンドラー実装・登録: 同じパイプラインで自動的にサブスロット展開が実行される
3. metadata['expansion_status'] が 'fallback' → 'full' に変化

**受け入れ条件**:
- Case A（破綻防止）: "the man who is playing the piano" で進行形ハンドラー未実装の場合、sub-slotは一切作られず、親スロット（S）に全文で入る。"the man who the piano" のような欠損が絶対に起きない。
- Case B（親スロット決定）: "I want to buy milk." で埋め込み節が部分失敗なら "to buy milk" が O1 に全文で入る（sub-slotなし）。親スロット決定は masked_doc 側の placeholder 位置で行う。

**詳細実装**: `UNIFIED_PIPELINE_ARCHITECTURE.md` Section 3 Phase ④-A（フォールバック機構）参照


２．各コンポーネントの役割
（CentralController）
統一汎用パイプラインを持ち、当該システムの処理全体を統括する。チャンカーやハンドラーを招集して動かし、claimをスコアリングシステムで最終承認する。
（チャンカー）
spaCy等UDの依存関係を手掛かりに、単語を品詞ごとのチャンクに合体するとともに、核を特定して品詞を決定する。
（ハンドラー）
5文型以外の文法を担当し、そのチャンクに対してスロット名をclaimする。It is kind of her to help me.ならto helpが不定詞ハンドラーの担当。of herは副詞ハンドラーの担当。It, is, kind, meはCentralControllerの5文型処理。
（Rephraseライブラリ）
ユーザー執筆の文法書「アウトプット用文法」から抽出した例文・期待値からチャンクの語順のパターンを抽出し登録したjsonと読み取って適用するためのスクリプト。入れ子内のパターンと入れ子内マスク簡略化後の上位スロット主節レベル文のパターンの2つから成る。

**🆕 V2生成器の設計思想（2025-12-08確立、期待値直接活用方式）**:
- **原則**: 「答えがあるのに改めてチャンク合致を試みるなど意味不明なことはしない」
- **方式**: Golden Test期待値（main_slots, sub_slots）から直接SLOT_TO_CHUNK_TYPE変換でパターン生成
- **文法ごとの分割JSON**: 各文法カテゴリが独立したJSONを持つ
  - `config/rephrase_basic_5_patterns.json` - 基本5文型
  - `config/rephrase_infinitive.json` - 不定詞構文
  - `config/rephrase_simple_adverbs.json` - 副詞パターン
  - `config/rephrase_causative.json` - 使役構文
  - `config/rephrase_gerund.json` - 動名詞
- **3原則**:
  1. **チャンクベースパターン必須**: トークンレベル固定パターン（"It + VERB + ADJ"）禁止 → 汎用性40%で破綻
  2. **副詞許容力**: ADV_CHUNKをパターンキーから除外（副詞はどこでも挿入可能）
  3. **2段階パターン**: 埋め込み節（sub_slots）と親スロット（main_slots with MASKED_XXX）の両方を登録
- **効果**: パターン汎用性40% → 100%、basic_5_patterns 100%達成、simple_adverbs 100%達成
- **詳細**: `docs/HANDLER_DEVELOPMENT_GUIDE.md` Line 382-450（革命的原則）

（ClaimArbiter）
CentralControllerに実装されるメソッド。権利ライブラリ、Rephraseライブラリ、チャンク合体結果、各ハンドラーのclaim、重複チェック、職務分掌違反チェック、などの情報に重みづけして点数を加算し、最も点数の大きい結果を承認するスコアリングシステム。


３．職務分掌

**🔥 重要原則（2025-12-24確立）: 埋め込み節内でも職務分掌は変わらない**

埋め込み節（不定詞句、関係節、動名詞句等）の内部においても、スロット割り当ての職務分掌は**親スロットと全く同じ**である。

❌ **誤った理解（AIがよく陥る誤解）**:
- 「InfinitiveHandlerは不定詞句内の全要素を担当する」
- 「埋め込み節を検出したハンドラーがその内部を全て分解する」
- 「埋め込み節内ではCentralControllerや副詞ハンドラーは動作しない」

✅ **正しい理解**:
- 埋め込み節内でも、5文型要素（sub-s, sub-v, sub-o1, sub-c1等）は**CentralControllerの再帰処理**が担当
- 埋め込み節内でも、副詞（sub-m1, sub-m2, sub-m3）は**AdverbHandler**が担当
- InfinitiveHandlerは**不定詞動詞（sub-v: to do, to swim等）のみ**を担当

**職務分掌一覧**:
・5文型に登場するSV,SVC1,SVO1,SVO1O2,SVO1C2はCentralControllerがclaimする。
  - **親スロット**: S, V, O1, O2, C1, C2, Aux
  - **埋め込み節内**: sub-s, sub-v, sub-o1, sub-o2, sub-c1, sub-c2, sub-aux
  - **職務範囲**: 埋め込み節内であっても、5文型要素は全てCentralControllerの再帰処理が担当
・Mは副詞ハンドラーが担当する。
  - **親スロット**: M1, M2, M3
  - **埋め込み節内**: sub-m1, sub-m2, sub-m3
  - **職務範囲**: 埋め込み節内であっても、副詞は全てAdverbHandlerが担当
・疑問文の場合の疑問詞のclaim、do,does,didなどの助動詞のclaim, be動詞の語順変化などはClauseFormハンドラーが担当する（念のため現状の実装を確認）。
・使役構文の際のC2内の動詞や不定詞はCausativeハンドラーが担当する（要確認：Vのmake,help,seeなどは5文型でいいか？）
・**不定詞ハンドラーは不定詞動詞（sub-v）のみを担当する**（2025-12-24確立）
  - **職務範囲**: to do, to swim等の不定詞動詞形式（sub-v）のみ
  - **管轄外**: sub-o1（目的語）、sub-c1（補語）、sub-m1（副詞）、sub-aux（助動詞）
  - **CAPABILITIES**: `[ClaimType.SUB_VERB]` のみ
・度名詞のdoingは動名詞ハンドラーが担当する。
・助動詞は助動詞ハンドラーが担当する。
・仮定法のIfと、If節内のVの変化、取設のwould+vは仮定法ハンドラーが担当する（念のため現状の実装を確認）

**職務分掌の具体例**:
```
例文: "I want to help me."
埋め込み節: "to help me"

❌ 誤った職務分掌:
- InfinitiveHandlerが全て担当 → sub-v="to help", sub-o1="me" を両方claim

✅ 正しい職務分掌:
- InfinitiveHandler: sub-v="to help" のみclaim
- CentralController（再帰処理）: sub-o1="me" をclaim
```

**実装上の強制**:
- `InfinitiveHandler.CAPABILITIES = [ClaimType.SUB_VERB]` のみ
- AST Linter検証26: CAPABILITIES違反をコミット時に検出
- AST Linter検証27: CAPABILITIES定義自体が正しいかホワイトリストで検証
- Runtime validation: `validate_claim_capability()` が実行時に検出


４．禁止事項
これまでに発生した違反の例を示す。いずれも、「入れ子内→上位スロット主節レベルの再帰処理」というロジックを理解できていない証拠である。

・サブスロット内のスパンを計測する仕組が無かった（サブスロット内にも5文型が展開されいて分解処理が必要である認識が無かったのか？）
・不定詞ハンドラー（入れ子の中を処理するハンドラー）が、最初から解答を与えられるかのようにRephraseライブラリから親スロットの識別（metadata）を与える仕様になっていた。親スロットがどこで、そのスロットがSなのかCなのかOなのか、ということは親スロットを処理してはじめてわかることで、完全な設計違反である（当該システムは既存の文に既存の解答を表示するシステムではなく、パターンを活用して未知の文を解析するシステムである。）。
**「埋め込み文脈ハンドラーは、入れ子の句だけを与えられても、それが上位スロットの中の何の要素（O1/C2/M1等）かは分からない。最も俯瞰的にそれが分かる立場なのはCentralControllerだ。」**
>
> 例: "to help me" という不定詞句が、主節の動詞 "want" の後にある場合 → C2（補語）
> 同じ句が "afford" の後にある場合 → O1（目的語）
> **埋め込み節だけ見ても判別不可能 → 主文の動詞の文型情報が必要**
・埋め込み節パターンに_parent_slotが含まれている（InfinitiveHandlerが見てはいけない情報）、親スロット判定用のパターンが存在しない（"He seems [PLACEHOLDER]." → C1という判定材料がない）、など、Rephraseライブラリが入れ子処理の設計思想に沿っていない。
・マスク処理の際、「不定詞_placeholder」などとせず、単に削除していた。そんなマスク文では親スロットはまともに分解処理できない。サブスロットが全体でひとつの親スロットを占めるという認識もなかったのか？
・「to play」などの目的語や修飾語のない単独名詞の扱いが厳密に定まっていなかった。これは入れ子ではなく単なる名詞。不定詞ハンドラーがsub-vのclaimをしないよう分岐処理することで、統一汎用パイプラインへの修正を最小限にした。
・簡略化した後のMasked infinitiveがspaCy依存関係で無視されているためチャンク合体が失敗していたが、spaCyを修正することで名詞、副詞、形容詞いずれかのチャンクとして認識されるようにした。
・そもそもRephraseライブラリで、「Masked〇〇」のチャンクに対してスロットの割り当てパターンを登録していない。当該システムの原理やプロセスを全く理解できていないと思われる。それでは主節・親スロットレベルの処理ができない。
・当たり前の話だが、Rephraseライブラリに登録されるすべてのパターンには、可能性のあるすべての箇所に副詞を受け入れる汎用的許容力を持っている必要がある。しかし実際には副詞があるとパターンマッチが破綻するような構造だった。
・CentralControllerがArbiterのスコアリングシステムを使わず、ハンドラーのclaimを無条件でそのままスロットに入れていた。
・文法ハンドラーの原則
- ✅ 中央管理システムとのみ通信
- ✅ 独自に情報取得はしない（必要な情報は中央管理システムが与える）
- ✅ 出力は中央管理システムに対してのみ
- ✅ 文法の担当領域を守る（例：動名詞ハンドラーが勝手に副詞を処理しても、中央管理システムが排除）
- ✅ Rephrase的スロット分解のフォーマットに完全準拠
・Rephraseライブラリについて
 ❌ **固定トークンパターン**: `if doc[0].text == "It" and doc[1].pos_ == "VERB" and doc[2].pos_ == "ADJ"` ← **最重要違反**
- ❌ **1対1ハードコーディング**: `if sentence == "It surprised me...": return {...}`
- ❌ **独自spaCy解析**: 期待値を無視して独自推測（パターン網羅性0%の原因）
- ❌ **期待値にないスロット名**: `'verb'` → 正: `'sub-v'`
・CentralControllerが検出した文法のハンドラーではなく、常に全てのハンドラーを呼ぶのは設計違反
・


５．フローに関する補足
UIには影響ない（微細な変更で済む）ことを確認したうえで、上位スロットが複数個所に跨るケース（形式主語のS、What do you think it is？のO1など）はS_1,S_2など番号制とした。その際、何か複雑なこと（複数スロットを検出したり番号を振ったり）をして失敗の連続だったので、「単にRephraseライブラリに登録されているスロットをそのまま表示」のようにしたら成功。


６．その他開発体制
（１）構造化ロギング完全追跡システム
エラーが発生した際、どこが原因なのかを即座に特定するため、情報の入力と出力に対して透明性が必要。
- **適用箇所**: 7ハンドラー（`@log_claim_generation()`）+ 2システム（`@log_method_entry_exit()`）
   - **追跡内容**: Claim生成経路、ClaimArbiter調停、Claim→スロット変換
   - **AST Linter**: 3パターン自動検出（違反時commitブロック）
   - **効果**: デバッグ時間7-18倍高速化（35-90分 → 5分）
   - **🆕 Trace ID機能**（2025-12-18実装）:
     - **目的**: Test単位での完全追跡、デバッグ時間2時間 → 5分（24倍高速化）
     - **仕組み**: 各Test実行時に一意のTrace ID（例: `test_012_20251218_195022`）を付与
     - **ログ記録**: 全ログエントリに`"trace_id"`フィールドを自動追加
     - **ビューアーツール**: `python tools/view_test_trace.py <trace_id>` でTest単位のログを抽出・ツリー表示
     - **使用例**: 
       ```bash
       # Golden Test実行（Trace IDが表示される）
       python golden_snapshots.py --category=basic_5_patterns
       # 出力: [Test]: 012 [Trace ID: 012_20251218_195022]
       
       # 特定TestのTrace ID指定でログ表示
       python tools/view_test_trace.py 012_20251218_195022
       # → Test 012の全処理フロー（Claim生成、調停、スロット変換）をツリー構造で表示
       ```
     - **実装場所**: 
       - `src/systems/structured_logging.py`: Trace IDコンテキスト管理（Thread-local変数）
       - `golden_snapshots.py`: Test実行時に`set_trace_id()`呼び出し
       - `tools/view_test_trace.py`: ログビューアーツール（新規作成）
   - **詳細**: `HANDLER_DEVELOPMENT_GUIDE.md` Part 7（構造化ロギング必須化）

（２）Fail and Recover自動統合システム
修正履歴を自動記録し、類似ケースを検索するシステム。手動記録の負担を75-82%削減。
- **適用箇所**: `golden_snapshots.py` の `_handle_fail_and_recover_integration()`
   - **追跡内容**: 失敗→成功の遷移検出、類似過去修正の自動検索、Git diff自動抽出
   - **コアヘルパー**: `tools/fail_and_recover_helper.py` (297行)
   - **効果**: 記録時間15-28分 → 3-5分（75-82%削減、root_cause/design_rationaleのみ手動）
   - **🆕 自動機能**（2025-12-21実装）:
     - **失敗時ヒント表示**: テスト失敗時に類似過去修正TOP3を自動表示
       - スコアリング: カテゴリ一致 +10点、ファイル一致 +20点/ファイル、キーワード +5点/語
     - **成功時記録プロンプト**: 前回失敗→今回成功を検出し、記録確認プロンプト表示
       - 'y'入力でテンプレート自動生成、`Fail and Recover.md`に追記
       - テンプレート内容: Git diff、精度改善、タイムスタンプ（自動）+ root_cause、design_rationale（手動3-5分）
     - **テスト状態管理**: `test_states_cache.json`でテスト状態を永続化（passed/failed、精度）
     - **CIモード対応**: `--ci`または`--no-fail-recover-prompt`でプロンプトスキップ
   - **使用例**: 
     ```bash
     # 通常実行（自動プロンプト有効）
     python golden_snapshots.py --category=infinitive_constructions --include-extensions
     # → 失敗時: 類似ケースヒント表示
     # → 成功時: "修正を記録しますか? (y/n):" プロンプト
     
     # プロンプトスキップ
     python golden_snapshots.py --category=basic_5_patterns --no-fail-recover-prompt
     ```
   - **実装場所**: 
     - `golden_snapshots.py` Line 1563-1729: 統合メソッド（テスト状態管理、プロンプト、記録）
     - `tools/fail_and_recover_helper.py`: コアヘルパー（類似検索、テンプレート生成、追記）
     - `test_states_cache.json`: テスト状態キャッシュ（自動生成）
   - **詳細**: 本ファイル Section 6（開発体制）、`tools/fail_and_recover_helper.py` docstring

（３）Ast LinterとRephraseライブラリLinter
設計違反のコードを検出し、AIによる勝手な設計変更を防ぐ。RephraseライブラリLinterはRephraseライブラリが上記で述べているような構造になっているかどうかに対するチェック。

**実績**（2025-12-06確立）:
- ✅ **検証8（単語テキスト禁止）**: 267違反検出 → 0違反達成（100%準拠）
- ✅ **検証9（副詞許容力）**: 0違反（ADV_CHUNKがパターンに含まれない）
- ✅ **検証10（2段階パターン）**: 0違反（sub_slotsもインデックス化）
- ✅ **チャンクインデックス方式への完全移行**
- ✅ **3原則の完全実装確認**（品詞チャンク必須・副詞許容力・2段階パターン）
- ✅ **パターン汎用性**: 40% → 100%（理論値）
- ✅ **Golden Test精度**: 46.9% → 81.2% (+34.4%) → **84.4%** (+3.2%, 2025-12-06 20:30)
- ✅ **🆕 スロット語順シグネチャ対応**（2025-12-06 20:30確立）:
  - **目的**: 同一文型での語順変化対応（通常文 vs 疑問文、倒置構文等）
  - **実装**: パターンキー = `{chunk_sequence}_{pattern_type}_{slot_signature}`
  - **効果**: Test 8 (S-V-C1) と Test 13 (C1-V-S) の衝突解決
  - **例**: 
    - `NOUN_CHUNK_AUX_CHUNK_NOUN_CHUNK_SVC_C12-S0-V1` (通常文: Greg is a worker)
    - `NOUN_CHUNK_AUX_CHUNK_NOUN_CHUNK_SVC_C10-S2-V1` (疑問文: What is it?)
  - **影響範囲**: すべての語順変化パターン（疑問文、倒置、強調構文等）に対応可能
  - **パターン数**: 47 → 53 (+6パターン、語順変化分を追加登録)
  - **詳細**: `tools/generate_unified_rephrase_patterns.py` Line 107-115, `src/integrators/rephrase_basic_five_patterns_integrator.py` Line 147-168

**AST Linter** - 抽象構文木によるコードパターン検出
   - 統一データ違反検査
   - ハードコーディング検査
   - 中央管理違反検査
   - 無条件ハンドラー招集検査（2025-10-22実装）
   - **🆕 構造化ロギング違反検査**（2025-11-16実装）
     - `MISSING_LOG_DECORATOR_IN_HANDLER`: ハンドラーprocess_unified()デコレーター欠落
     - `MISSING_LOG_DECORATOR_IN_ARBITER`: ClaimArbiter._arbitrate_claims()デコレーター欠落
     - `MISSING_LOG_DECORATOR_IN_CONVERTER`: _convert_claims_to_slots()デコレーター欠落
     - 違反時Exit Code 1でcommitブロック
   - **🆕 Rephraseライブラリ違反検査**（2025-10-25実装）
     - `MISSING_REPHRASE_LIBRARY_INIT`: self.rephrase_lib初期化漏れ
     - `SPACY_BEFORE_REPHRASE`: Rephrase前にspaCy使用
     - `REPHRASE_RESULT_IGNORED`: Rephraseマッチ後にspaCy上書き
     - `HARDCODED_CONFIDENCE_WITHOUT_REPHRASE`: Rephrase判定なしconfidence固定
     - `MISSING_REPHRASE_CALL_IN_DETECTION`: _detect_xxx内でRephrase未使用
   - **🆕 spaCy API違反検査**（2025-10-25実装）
     - `SPACY_API_DIRECT_ACCESS`: ハンドラーでのspaCy直接使用
     - `SPACY_ITERATION_IN_HANDLER`: ハンドラーでのspaCy子要素イテレーション
   - JSON化された統一データ定義を動的に参照
    **mypy/pyright** - 型チェッカー（2025-11-16統合）
   - 仮想環境Python自動検出（`.venv/Scripts/python.exe` or `.venv/bin/python`）
   - 型ヒント違反を開発中・コミット前に検出
   - 3層防御体制（Layer 1: 静的解析、Layer 2: 実行時検証、Layer 3: 防御的）
　　**CI** - GitHubデスクトップのChangesに違反があればコミット阻止

（４）Goldenテスト
スナップショットをそなえたテストシステム。いつ何が退化したか分かりやすい。
**🆕 Fail and Recover自動統合**（2025-12-21）により、テスト失敗→修正→成功のサイクルで自動的に記録プロンプトが表示される。
　　レポートの場所

　　quality_reports/
　　 ├─ golden_test_diff_basic_5_patterns_YYYYMMDD_HHMMSS.txt  ← ① 差分詳細レポート
　　 ├─ unified_test_report_basic_5_patterns_YYYYMMDD_HHMMSS.txt  ← ② 統合レポート
　　 └─ test_states_cache.json  ← ③ テスト状態キャッシュ（Fail and Recover用）

（５）コードスナップショットシステム
Goldenテスト実施時、**AST Linter v3実施時**に自動的に全コードのスナップショットを時刻付で保存するシステム。Goldenテストのログと照合すれば、退化の原因を素早く特定できる。

**実装状況**（2025-11-30現在）:
- ✅ **Golden Test**: スナップショット記録実装済み（golden_snapshots.py）
- ✅ **AST Linter v3**: スナップショット記録実装済み（unified_ast_linter_v3.py Line 11-17, 702-714）
- 📁 **保存場所**: `.snapshots/snapshot_YYYYMMDD_HHMMSS.json`
- 🔍 **追跡**: tools/snapshot_tracker.py（CodeSnapshotTracker）

（６）閉じた集合のハードコーディングについて
### ✅ **承認済み：閉じた集合のハードコーディング**

**条件**（すべて満たす必要あり）:
1. **閉じた集合**: 有限で文法的に決定的（≤50語）
2. **文法的役割**: 連結動詞、授与動詞、助動詞など
3. **品詞だけで区別不可**: NOUN補語 vs NOUN目的語は動詞知識が必要
4. **承認コメント**: `# APPROVED: Closed set of [role] (grammatically definitive, ~N words)` 必須

**例**:
```python
# APPROVED: Closed set of linking verbs (grammatically definitive, ~15 words)
# Rationale: 第2文型を取る動詞は文法的に限定される閉じた集合
# Necessity: NOUN補語 vs NOUN目的語 cannot distinguish by POS alone
LINKING_VERBS = {
    'be', 'become', 'seem', 'appear', 'remain', 'stay',
    'look', 'sound', 'feel', 'taste', 'smell', 'grow', 'turn', 'prove', 'get'
}

# APPROVED: Closed set of ditransitive verbs (grammatically definitive, ~20 words)
# Rationale: 第4文型を取る動詞は文法的に限定される閉じた集合
# Necessity: SVOO vs SVOC cannot distinguish without verb knowledge
DITRANSITIVE_VERBS = {
    'give', 'tell', 'show', 'send', 'buy', 'bring', 'lend',
    'teach', 'pay', 'offer', 'sell', 'pass', 'hand', 'throw'
}
```

### ❌ **禁止：開かれた集合のハードコーディング**

- **開かれた語彙**: 形容詞、名詞、一般動詞（無限集合）
- **大規模セット**: >50語
- **内容語**: 品詞パターンで検出可能（`if token.pos_ == 'ADJ'`）

**例（禁止）**:
```python
# ❌ 無限集合
ADJECTIVES = {'happy', 'sad', 'angry', ...}  # 代わりに: if token.pos_ == 'ADJ'
```

### ハイブリッド戦略（Pure Text Pattern + 承認済みハードコーディング）

```python
# ✅ 正解: 品詞パターン（ADJ）+ 動詞リスト（NOUN補語用）
if doc[i].pos_ == 'ADJ' or doc[i].tag_ in {'VBN', 'VBD'}:
    complement_idx = i  # 品詞で検出可能
elif doc[i].pos_ in {'NOUN', 'PROPN'} and doc[verb_idx].lemma_ in LINKING_VERBS:
    complement_idx = i  # 品詞だけでは不十分→動詞知識必要

（７）情報統一システム
**情報統一システム方式の設計理念**:
> **「全ての情報はCentralControllerを通し、統一された形式で入手・処理・保存する」**
目的：取り扱いがバラバラになって情報の受け渡しがどこかで止まったり、トラブル時にどこが原因か分かりにくくなったりすることを防ぐ

この理念を実現するため、**3層防御体制**を採用：

#### Layer 1: 静的解析（開発時）
- **mypy**（型チェッカー、型推論）← 🆕 2025-11-08追加
- **pyright**（VS Code統合型チェッカー）← 🆕 2025-11-08追加
- AST Linter（パターン検出）
- 動的基準システム（`dynamic_standards_registry.json`）

**mypy/pyright実行方法**:
```bash
# mypy: コマンドライン/CI用
mypy src/ --config-file=mypy.ini

# pyright: VS Code統合（自動）
pyright src/
```

**型チェック実行タイミング**:
1. **開発中**: pyright（Pylance）がリアルタイムチェック（VS Code）
2. **コミット前**: mypy実行（pre-commit hook、推奨）
3. **CI**: GitHub Actions（自動、将来実装予定）

#### Layer 2: 実行時検証（実行時）🆕
- `__setattr__`型チェック（`CentralProcessingResult`等）
- Dict/List型混同を即座に検出
- デバッグ時間を35-90分 → 5分に短縮（**7-18倍高速化**）

#### Layer 3: 防御的プログラミング（処理時）
- `isinstance()`チェック
- try-exceptエラーハンドリング

**ハンドラー開発時の厳守事項**:
```python
# ✅ 正しい: Dict型で代入 + 型ヒント
def analyze_structure(
    self, 
    doc: Doc,  # 型ヒント必須（mypy/pyrightチェック）
    context: CentralAnalysisContext
) -> CentralProcessingResult:  # 戻り値型必須
    result = create_standard_result(...)
    
    sub_slots: Dict[str, str] = {'sub-v': 'to fly'}  # 型ヒント推奨
    result.sub_slots = sub_slots  # ✅ Dict型（Layer 2が検証）
    
    return result  # ✅ 正しい型（Layer 1が検証）

# ❌ 間違い: List型で代入（Layer 2が即座にTypeError）
result.sub_slots = ['sub-v', 'sub-o1']  # TypeError!

# ❌ 間違い: 型ヒントなし（Layer 1 mypyが警告）
def analyze_structure(self, doc, context):  # ← 型ヒントなし
    return ['sub-v']  # ← mypyが戻り値型違反を検出
```

**3層防御の効果**:

| 検出タイミング | Layer 1（mypy/pyright） | Layer 2（Runtime） | Layer 3（Defensive） |
|--------------|----------------------|-------------------|---------------------|
| **開発中** | ✅ リアルタイム波線表示 | - | - |
| **コミット前** | ✅ mypy自動実行 | - | - |
| **実行時** | - | ✅ 即座にTypeError | ✅ 防御的処理 |
| **検出率** | 85-90% | 95% | 99% |

**型エラー検出率の向上**:
- AST Linterのみ: 70-80%
- + mypy/pyright: **95%+**（+15-25%向上）
**🆕 Runtime Type Safety** - 実行時型安全性システム（2025-11-03導入）
   - `__setattr__`オーバーライドによる型強制
   - Dict/List型混同を即座に検出（従来：数時間後 → 新：即座）
   - デバッグ時間を35-90分 → 5分に短縮（7-18倍高速化）
   - **3層防御体制**: Layer 1（静的解析） → Layer 2（実行時検証） → Layer 3（防御的）
   - **適用範囲**: CentralProcessingResult.sub_slots, main_slots等
   - **詳細**: `UNIFIED_PIPELINE_ARCHITECTURE.md` Section 10、`HANDLER_DEVELOPMENT_GUIDE.md` Part 7


**詳細**: `UNIFIED_PIPELINE_ARCHITECTURE.md` Section 10（特にSection 10.5 静的型チェッカー統合）、`HANDLER_DEVELOPMENT_GUIDE.md` Part 7

（７）統一汎用パイプライン
**統一汎用パイプラインとは何か？（誤解がないか？）を完全に理解してください。**

**【実装調査時の注意】**:
- ✅ **設計仕様書**: `Phase ①` `Phase ②` `Phase ③` `Phase ④` という表記
- ✅ **CentralController実装**: `Phase ① 特殊構造処理` `Phase ② 基本構造分析` `Phase ③ 拡張ハンドラー` `Phase ④ 統合・検証` という表記
- ⚠️ grep検索時: `Phase ①` だけでは実装が見つからない（日本語説明が付いているため）
- ✅ **正しい検索パターン**: `Phase ① 特殊構造|Phase ② 基本構造|Phase ③ 拡張ハンドラー|Phase ④ 統合` または `① 文法検出|②③ 埋め込み節|⑧ マスク|⑨ 上位文|⑤⑥ Claim`
- 📍 **実装場所**: `src/controllers/central_controller_v14_chunk_system.py` の `_execute_unified_pipeline()` メソッド（Line 1374-2044）

#### 🎯 統一汎用パイプラインの本質

**定義**: 各ハンドラーが個別にパイプラインを持つのではなく、**全文法が共通プロセス①-⑩を選択的に使用する**単一のパイプライン。

**比喩**: 
- ❌ **間違った理解**: 文法ごとに専用の工場を持つ（関係節工場、不定詞工場、動名詞工場）
- ✅ **正しい理解**: **1つの工場で全文法を処理**。違いは「原材料（トリガー）」だけ。

| 文法 | トリガー（5%の違い） | 共通プロセス（95%同じ） |
|------|---------------------|----------------------|
| 関係節 | 先行詞 + 関係詞（who/which/that） | ②-⑩を実行 |
| 不定詞 | to do | ②-⑩を実行 |
| 動名詞 | doing | ②-⑩を実行 |

#### 🔑 共通プロセス①-⑩（全文法共通）

❌ 間違ったアプローチ（if-elif分岐）:
┌──────────────────────────────────────┐
│ _execute_universal_pipeline()       │
├──────────────────────────────────────┤
│ if has_relative:                     │
│   ┌────────────────────────────┐    │
│   │ 関係節専用パイプライン（200行）│    │
│   │ ②-⑩を独自実装             │    │  ← 600行の重複！
│   └────────────────────────────┘    │
│ elif has_infinitive:                 │
│   ┌────────────────────────────┐    │
│   │ 不定詞専用パイプライン（200行）│    │
│   │ ②-⑩を独自実装（95%同じ！）│    │
│   └────────────────────────────┘    │
│ elif has_gerund:                     │
│   ┌────────────────────────────┐    │
│   │ 動名詞専用パイプライン（200行）│    │
│   │ ②-⑩を独自実装（95%同じ！）│    │
│   └────────────────────────────┘    │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ _execute_universal_pipeline()       │
├──────────────────────────────────────┤
│ ② トリガー検出（5-10行）             │
│   ├─ 関係節: "先行詞+関係詞"         │
│   ├─ 不定詞: "to do"                │
│   └─ 動名詞: "doing"                │  ← 違いはここだけ！
├──────────────────────────────────────┤
│ ③-⑩ 共通プロセス（200行）           │
│   │ 全文法で100%再利用              │  ← 1つのコードで全対応！
│   ├─ ③ 切り分け                     │
│   ├─ ④ 再帰処理                     │
│   ├─ ⑥ Claim収集                    │
│   ├─ ⑦ ClaimArbiter調停            │
│   ├─ ⑧ マスキング                   │
│   ├─ ⑨ 上位処理                     │
│   └─ ⑩ 統合・正規化                 │
└──────────────────────────────────────┘
```

✅ 正しいアプローチ（統一パイプライン + Pure Text/フォールバックspaCy完全分離）:

**🔥 重要な設計思想（2025-10-30確立）**:

例えば関係節のプロセスが「①②③④⑤」で、不定詞プロセスはこのうち②と④が違う、という場合。
「①②③④⑤」
「①②'③④'⑤」
のように2つを作るのではなく、
①→ ② →③→ ④→⑤
　⤵②'⤴ ⤵④'⤴
のように、パイプライン自体は1つで、②と④のところだけが分岐し、①③⑤は同じ箇所を通る（コピーするのではない）ということを意味します。

（８） **Claim**
 - ハンドラーの出力を安全な提案式に（CentralControllerが承認）

（９）**🆕 Capabilities（職務分掌徹底）**
 - ハンドラーに明確な能力定義（2025-10-25強化）
   - 各ハンドラーは`CAPABILITIES`でClaim Type白リストを宣言
   - 宣言外のClaimを生成すると`CapabilityViolationError`
   - ハンドラー間競合を検出
   - CentralControllerがどのハンドラーを呼ぶかのラベルにもなる

（１０）権威ライブラリ
UD、spaCy, Penn, Wordnet

### ✅ VerbNet Full Dictionary統合完了（2025-11-21）

**革命的統合**: VerbNet 3.4の全データ（329 XMLファイル）を統一JSON辞書に変換し、システムに統合完了。

**統合成果**:
- **動詞カバー**: 4,580動詞（従来5動詞の**916倍**）
- **フレーム数**: 39,436フレーム（従来5フレームの**7,887倍**）
- **新規検出可能**: 'owe'等の授与動詞、従来検出不可能だった動詞
- **辞書サイズ**: 8.66 MB（verbnet_full_dictionary.json）
- **ライセンス**: GPL-3.0 / CC BY-SA 3.0（VERBNET_LICENSE.txt含む）

**技術実装**:
- VerbNetParser新フォーマット対応（list of class dicts per verb）
- get_frames_for_verb()メソッド追加（全verb classのframe統合）
- 後方互換性維持（旧5動詞辞書も読み込み可能）

**品質保証**:
- ✅ Golden Test: 100%維持（basic_5_patterns 32/32、simple_adverbs 20/20）
- ✅ AST Linter: 0違反達成（DeprecationWarning完全削除）
- ✅ 機能テスト: 9動詞で検証（give→19 frames、tell→17、show→33、owe→4等）

**効果**:
- 動詞判別精度: 推定10-15%向上（未検証、将来測定予定）
- カバレッジ: 英語動詞の90%+をカバー（VerbNet公式数値）
- 保守性: 言語学的根拠により将来にわたって安定

**詳細**: `src/core/verbnet_parser.py`、`tests/data/VERBNET_LICENSE.txt`参照



７． 完成目標

（１）**🔄 UIのアーキテクチャを大幅改善（例文DB自動作成システムで培った高度アーキテクチャ思想を適用）
（２）**🔄 仮主語S分離の仕組み実装**（Extraposition完全対応）・スロット番号制対応スロット重複問題の完全解決（S='It' + S='to see...'等をS_1,S_2とする。が、それは内部IDで、UI上はS仮、S真のようなほうが分かりやすい）
（３）**🔄 サルでもわかるUI改善**（直感的インターフェース）


**目的**: 

**実装内容**（training/js/structure_builder.js、推定20-30行）:
①. スロット表示ラベル生成関数（10-15行）
   ```javascript
   function getSlotDisplayLabel(slotName) {
     // "O1_1" → "O1 (1)", "O1_2" → "O1 (2)"
     const match = slotName.match(/^([A-Z]+\d?)_(\d+)$/);
     if (match) return `${match[1]} (${match[2]})`;
     return slotName;  // "O1" → "O1" (後方互換)
   }
   ```
②. renderSlot()内でラベル適用（5行）
③. 音声読み上げ順序調整（10-20行、番号順ソート）

**重要**: データ構造はそのまま使用可能（`Slot_display_order`で表示順序制御）

## 📊 現在の進捗状況

**🎉 歴史的マイルストーン達成**（2025-12-26）:
- **不定詞名詞的用法100%達成**: 入れ子処理完成第一号
- **20回のスクラップアンドビルド**: K-MAD確立までの道のり
- **統一汎用パイプライン実証**: 全文法を吸収する設計の成功
- **AST Linter違反0達成**: 厳格なゼロトレランス方針の完全実施

**現在の精度**:
- infinitive_constructions: **100.0%（14/14）** ← 🆕 Phase 5完成
- basic_5_patterns: 100.0%（32/32）
- simple_adverbs: 100.0%（20/20）
- relative_clauses: 100.0%（12/12、Pure Text Pattern）
- passive_with_relative_clauses: 100.0%（11/11、Pure Text Pattern）
- passive_voice: 100.0%（20/20、Pure Text Pattern）


### 🔄 ハンドラー実装状況と計画（2025-11-29時点）

1. **🔄 CentralController v14**（最優先）
   - PhraseChunker
     - ✅ **ピリオド吸収修正完了**（2025-12-13、Line 1287-1300）
       - **問題**: absorbed_tokens順序が吸収順（['by', 'morning', 'tomorrow']）で文中順と異なる
       - **原因**: `_recursive_absorb`が子要素を再帰的に吸収するため、順序が保証されない
       - **解決**: `absorbed_tokens[-1].i` → `max(t.i for t in absorbed_tokens)` で文末判定
       - **効果**: "by tomorrow morning." → ピリオド含むPREP_CHUNK生成成功
   - チャンクベース文法検出

2. **🔄 基本5文型ハンドラー→必要なし。CentralController自身が担当する**（100%）
   **🔄 副詞ハンドラー**（100%）

3. **✅ 不定詞ハンドラー（InfinitiveHandlerV1Gen3）**
   - **実装状況**: Phase 5完成 - **名詞的用法100%達成**（2025-12-26）🎉
   - **Rephraseライブラリ**: infinitive_constructions.json（14例文、名詞的用法完全対応）
   - **🏆 歴史的マイルストーン達成**（2025-12-26）:
     - **入れ子処理完成第一号**: 20回のスクラップアンドビルドを経て達成
     - **K-MAD確立**: Knowledge-Minimal Architecture Designの完成
     - **統一汎用パイプライン実証**: 全文法を吸収する設計の実証成功
     - **意義**: 当該システム最大の困難である入れ子処理の突破口
     - **影響**: 今後の全文法ハンドラー実装の参考モデルとなる
   - **段階的拡張計画**（Option A: 1統合ハンドラー方式採用）:
     ```
     Phase 5（✅完了 2025-12-26）: 名詞的用法14例文 → **100%達成**
       ├─ 形式主語構文（It ... to ...）: 7例文 ✅ 7/7完全成功
       │   ├─ Test 004成功（2025-12-12、Rule 1.4）
       │   ├─ Test 005成功（2025-12-12、Rule 1.5 "of her"）
       │   └─ Test 006成功（2025-12-13、ピリオド吸収修正）
       ├─ 目的語用法（want to do）: 5例文 ✅ 5/5完全成功
       └─ 補語用法（seem to be）: 2例文 ✅ 2/2完全成功（Test 013, 015）

     Phase 6（次回）: 形容詞的・副詞的用法追加 → 不定詞完全対応（0％）
       ├─ 形容詞的用法（後置修飾）: +10例文
       │   └─ "something to eat", "the first man to climb"等
       ├─ 副詞的用法（目的・結果・判断根拠・感情原因）: +10例文
       │   └─ "to study", "to be a doctor", "to say that"等
       └─ 合計30-40例文 → CAPABILITIES拡張（POST_MODIFIER, MODIFIER_PHRASE）
     ```
   
   - **実装の核心技術**（Phase 5で確立、今後の全文法に適用）:
     - **埋め込み節検出**: トリガー（to + VERB）→ 境界特定 → 切り分け
     - **再帰処理**: サブスロット分解 → マスク簡略化 → 親スロット処理
     - **2段階Rephraseライブラリ**: 埋め込み節パターン + 親スロットパターン
     - **フォールバック機構**: 未対応文法は埋め込み節全体を親スロットに格納
     - **職務分掌徹底**: InfinitiveHandlerは`sub-v`のみ、`sub-o1/sub-m1`はCentralController/AdverbHandler
   
   - **品詞判定ロジック**（Phase 6実装時の核心）:
     ```
     Step 1: 主節の動詞の文型を判定
       - Rephraseライブラリ: 期待値から直接取得（最優先、100点）
       - VerbNet: get_frames_for_verb()でフレーム解析（4,580動詞対応）
       - 動詞リスト: INFINITIVE_OBJECT_VERBS等（フォールバック）
     
     Step 2: 文型から不定詞の位置を特定
       - SVOO（第4文型）: O1/O2の位置 → 名詞的 or 形容詞的（名詞修飾）
         例（形容詞的）: "I gave him something to eat." → "to eat"がsomething修飾 → 形容詞的
       - SVO（第3文型）: Oの後 → 形容詞的（O修飾）or 副詞的（V修飾）
         例: "I bought a book to read." → O修飾 → 形容詞的
         例: "I came here to study." → V修飾 → 副詞的
       - SV（第1文型）: Vの後 → 副詞的用法確定
         例: "She went to the store to buy milk." → V修飾 → 副詞的
       - SVC（第2文型）: Cの位置 → 名詞的用法確定
         例: "My goal is to become a doctor." → C位置 → 名詞的
     
     Step 3: 判定責任の分担（Option A推奨）
       - Option A: CentralControllerが文型情報を付与
         └─ InfinitiveHandlerが品詞判定（context.metadata['verb_pattern']参照）
       - Option B: CentralController自身が判定
         └─ InfinitiveHandlerに用法を指示（context.metadata['infinitive_usage']）
     ```
   
   - **実装例**（Option A: ハンドラー側で判定）:
     ```python
     # CentralController（切り分け時）
     context.metadata['verb_pattern'] = 'SVOO'  # VerbNetから取得
     context.metadata['verb_lemma'] = 'give'
     context.metadata['infinitive_position'] = 'O2'  # 不定詞の位置
     
     # InfinitiveHandler
     def _determine_infinitive_usage(self, context):
         """主節の文型から不定詞の品詞を判定"""
         pattern = context.metadata.get('verb_pattern', '')
         position = context.metadata.get('infinitive_position', '')
         
         # 優先度1: Rephraseライブラリ（100点）
         rephrase_result = self.rephrase_lib.analyze_infinitive_pattern(
             context.spacy_doc,
             verb_pattern=pattern
         )
         if rephrase_result and 'usage' in rephrase_result:
             return rephrase_result['usage']  # 'noun'/'adjective'/'adverb'
         
         # 優先度2: 文型ベース推論
         if pattern == 'SVOO' and position in {'O1', 'O2'}:
             return 'noun'  # 名詞的用法確定
         elif pattern == 'SVC' and position == 'C2':
             return 'noun'  # 名詞的用法確定
         elif pattern == 'SVO':
             # O修飾 or V修飾を文脈で判断
             return 'adjective' if self._modifies_object(context) else 'adverb'
         elif pattern == 'SV':
             return 'adverb'  # 副詞的用法確定
         
         # デフォルト: 名詞的用法（Phase 5との互換性）
         return 'noun'
     ```
   
   - **設計判断根拠**:
     - ✅ 1つの統合ハンドラーが3用法すべてを担当（トリガーは全て "to + VERB" で同じ）
     - ✅ 段階的拡張により「動くものをまず作る」→「完成度を上げる」（アジャイル開発）
     - ✅ 開発速度3倍向上（3ハンドラー分割案を回避）
     - ❌ 3分割案（InfinitiveNounHandler等）は開発時間3倍・保守地獄のため却下
   - **詳細**: `HANDLER_DEVELOPMENT_GUIDE.md` Part 0（新方式）、`infinitive_constructions.json` meta参照

4. **🔄 使役構文ハンドラー（CausativeHandlerV1Gen3）**（基本実装完了、チャンクベース移行待ち）
   - **対象構文**:
     - have/make/let + O + 原形不定詞（裸不定詞）
     - get/tell/ask + O + to不定詞
   - **対象Test**: Test 30, 32
   - **実装状況**: ✅ Rephraseライブラリによる基本実装完了
   - **⚠️ TODO (CRITICAL)**: チャンクベース設計への移行必須
     - 現状: RephrasePatternAnalyzerのみ使用（トークンレベル品詞パターン、汎用性40%）
     - 必要: `context.metadata['chunks']`を使用したチャンクベースパターンマッチング
     - 理由: トークンレベル処理は修飾語の挿入で破綻（"very happy"と"happy"で別パターン）
     - 期限: Phase 6完了前
   - **優先度**: 中（不定詞完全対応後）

4.5. **🔄 動名詞ハンドラー（GerundHandlerV1Gen3）**（基本実装完了、チャンクベース移行待ち）
   - **対象構文**: VBG形式の動名詞句（"Smoking is bad for health."等）
   - **実装状況**: ✅ Rephraseライブラリによる基本実装完了
   - **⚠️ TODO (CRITICAL)**: チャンクベース設計への移行必須
     - 現状: RephrasePatternAnalyzerのみ使用（トークンレベル品詞パターン）
     - 必要: `context.metadata['chunks']`を使用したチャンクベースパターンマッチング
     - 理由: トークンレベル処理は修飾語の挿入で破綻
     - 期限: Phase 6完了前
   - **優先度**: 低（基本5文型完成後）

4.6. **🔄 進行形ハンドラー（ProgressiveHandlerV1Gen3）**（基本実装完了、チャンクベース移行待ち）
   - **対象構文**: be + VBG形式の進行形（"I am reading a book."等）
   - **実装状況**: ✅ Rephraseライブラリによる基本実装完了
   - **⚠️ TODO (CRITICAL)**: チャンクベース設計への移行必須
     - 現状: RephrasePatternAnalyzerのみ使用（トークンレベル品詞パターン）
     - 必要: `context.metadata['chunks']`を使用したチャンクベースパターンマッチング
     - 理由: トークンレベル処理は修飾語の挿入で破綻
     - 期限: Phase 6完了前
   - **優先度**: 低（基本5文型完成後）

5. **🔄 節形式ハンドラー（ClauseFormHandlerV1Gen3）**（Phase A完了、2025-11-10）
   - **実装状況**: ハンドラー本体完成、CentralController統合完了

   - **Phase A（基本疑問文・実装完了）**: Pure Text Pattern、Rephraseライブラリ不要
     - **目的**: Test 13/15修正 → 基本5文型カテゴリ93.75%達成
     - **実装内容**:
       - 単純疑問文のみ対応（What is it? / Where did you get it?）
       - 疑問詞スロット割り当て: What/Who → S or C1（be動詞チェック）、Where/When/Why/How → M1
       - 3段階検出: 疑問詞（文頭）、助動詞倒置（AUX + ?）、命令文（動詞文頭）
     - **対象**: 基本5文型カテゴリ内の疑問文（Test 13/15）
     - **効果**: 87.5% → 93.75% (+6.25%、2例文修正)
     - **Status**: ✅ 実装完了、Golden Test検証待ち

   - **Phase B（間接疑問文・次フェーズ）**: Rephraseライブラリ生成必要
     - **目的**: "What do you think it is?"等の複雑な疑問文対応
     - **対象単元**: アウトプット用文法.md「**14.間接疑問文と関係代名詞what、複合関係詞を用いる場合**」（Line 2494-）
     - **実装計画**:
       - 間接疑問文専用カテゴリ作成（`indirect_questions`）
       - Rephraseライブラリ生成（10-15例文）
       - 疑問詞2箇所出現パターン対応
     - **期待値例文**:
       - "Can you guess how much I weigh?" （間接疑問文）
       - "She has to blurt out what she thinks." （関係代名詞what）
       - "What do you think she did on finding the letter?" （疑問詞 + think + SV）
     - **Status**: ⏳ 未実装（Phase A完了後に着手）

   - **Phase C（完全対応・将来実装）**:
     - **目的**: すべての疑問形式を網羅
     - **対象**:
       - 付加疑問文（Tag questions）: "You like apples, don't you?"
       - 選択疑問文（Alternative questions）: "Do you like tea or coffee?"
       - 否定疑問文（Negative questions）: "Didn't you go there?"
       - 修辞疑問文（Rhetorical questions）: "Who knows?"
     - **Status**: ⏳ 後回し可（Phase A/B優先）

   - **設計判断根拠**:
     - ✅ Phase A: コスト最小（ライブラリ不要、Pure Text Patternのみ）
     - ✅ Phase B: アウトプット用文法.mdに専門単元あり（ライブラリ作成可能）
     - ✅ Phase C: 後回し可（基本5文型・間接疑問文が優先）
     - ⚠️ 疑問文は「動詞チャンクの運用上の結果」として散発的に登場（専門単元なし）
   
   - **アウトプット用文法.md調査結果**（2025-11-10）:
     - ❌ 疑問文専門単元は存在しない（散発的に登場）
     - ✅ 間接疑問文専門単元あり（Line 2494-、30+ matches）
     - ✅ 疑問文は基本5文型・助動詞・時制等の「運用上の結果」

6. **🔄 助動詞ハンドラー**（0% - 未着手）
7. **🔄 仮定法ハンドラー**（0% - 未着手）

### 保守モードのハンドラー（Pure Text Pattern化済み、Generation 3移行待ち）
- ✅ 受動態ハンドラー（20/20例文）
- ✅ 関係節ハンドラー（12/12例文）
- ✅ 受動態を含む関係節ハンドラー（11/11例文）

**注**: これらは旧システムでPure Text Pattern化済みだが、Generation 3（チャンク分解）には未対応

### ⚠️ チャンクベース移行必須ハンドラー（2025-11-30現在）

**システム設計の大前提**: Rephraseライブラリによる**チャンクベースパターンマッチング**（汎用性100%）

以下の3ハンドラーは基本実装完了しているが、トークンレベル品詞パターン（汎用性40%）のため、Phase 6完了前に**チャンクベース設計への移行必須**:

1. **CausativeHandlerV1Gen3** (`src/handlers/causative_handler_v1_gen3.py`)
   - 現状: RephrasePatternAnalyzerのみ（トークンレベル）
   - 問題: "very happy"と"happy"で別パターン → 汎用性40%止まり
   - 必要: `context.metadata['chunks']`使用 → ADJ_CHUNKで統一
   - TODO: Line 7-11にマーク済み

2. **GerundHandlerV1Gen3** (`src/handlers/gerund_handler_v1_gen3.py`)
   - 現状: RephrasePatternAnalyzerのみ（トークンレベル）
   - 問題: 修飾語の挿入で破綻
   - 必要: `context.metadata['chunks']`使用
   - TODO: Line 7-11にマーク済み

3. **ProgressiveHandlerV1Gen3** (`src/handlers/progressive_handler_v1_gen3.py`)
   - 現状: RephrasePatternAnalyzerのみ（トークンレベル）
   - 問題: 修飾語の挿入で破綻
   - 必要: `context.metadata['chunks']`使用
   - TODO: Line 7-11にマーク済み

**チャンクベース設計の本質**:
- ✅ **汎用性100%**: "to see his picture"も"to eat an apple"も同じパターン（VERB_CHUNK+NOUN_CHUNK）
- ❌ **現状の問題**: トークンレベル（PART+VERB+PRON+NOUN）→ 修飾語1つで破綻
- 🎯 **解決策**: Rephraseライブラリのチャンク語順パターンでマッチング

**AST Linter対応**:
- ✅ TODOコメント検出で警告スキップ（2025-11-30実装）
- ✅ コミット自動ブロック回避（違反0達成）
- ⚠️ Phase 6完了前に移行必須（システム設計の大前提）



### 🔄 その他の注意事項（2025-11-29時点）
`create_standard_result()` の引数順序ミス

**問題**: 引数の順序を間違えると型エラーで動作しない

**❌ 間違った実装**:
```python
return create_standard_result(
    claims=claims,  # ← 最初に書いてはダメ！第1引数はsuccess（bool）
    handler_name=self.__class__.__name__
)
```

**結果**: 第1引数 `success` が `claims` (list) になり、型エラー

**✅ 正しい実装**:
```python
return create_standard_result(
    success=True,  # 第1引数（必須）
    handler_name=self.__class__.__name__,  # 第2引数（必須）
    processing_time=time.time() - start_time,  # 第3引数（必須）
    confidence=self.confidence_success,  # 第4引数（必須）
    claims=claims,  # ← 最後に書く！
    metadata={"note": "..."}
)
```

**教訓**: 
- 必ず **InfinitiveHandler の実装をコピペしてから修正** すること
- 動名詞ハンドラーで1時間デバッグした実例あり（2025-10-24）

#### 3.2 `_register_extension_handlers()` メソッドの配置ミス

**問題**: メソッドがクラスの最後尾にあると、登録漏れや発見困難の原因になる

**❌ 間違った配置**: クラスの最後尾（11,000行目等）
```python
class CentralControllerV13DesignCompliant:
    def __init__(self, config_manager=None):
        self._register_extension_handlers(registry)
    
    # ... 10,000行以上のメソッド ...
    
    def _register_extension_handlers(self, registry):  # ← 最後尾（NG）
        ...
```

**結果**:
- メソッドが見つからない（検索困難）
- 登録漏れのリスク（新規ハンドラー追加時に既存コードが見えない）
- デバッグ困難（登録漏れか検出失敗か判別しにくい）

**✅ 正しい配置**: `__init__()` の直後（クラスの先頭付近）
```python
class CentralControllerV13DesignCompliant:
    def __init__(self, config_manager=None):
        self._register_extension_handlers(registry)
    
    def _register_extension_handlers(self, registry):  # ← __init__直後に配置
        """拡張ハンドラーの登録"""
        from gerund_handler_unified_pipeline import GerundHandlerUnifiedPipeline
        gerund_handler = registry.get_handler('gerund_unified') or GerundHandlerUnifiedPipeline(self.config_manager)
        if registry.register_handler(gerund_handler):
            self.logger.info(f"✅ GerundHandler登録完了")
    
    # ... 他のメソッド ...
```

**教訓**:
- 新規ハンドラー追加時は必ず `_register_extension_handlers()` を検索
- メソッドが見つからない場合は `__init__()` 直後を確認
- 動名詞ハンドラーで1時間デバッグした実例あり（2025-10-24）

**詳細**: `HANDLER_DEVELOPMENT_GUIDE.md` Part 1, Step 2 参照

---

## 🔍 AI調査時の必須プロトコル（絶対厳守）

### Rule 1: 実装調査の3ステップ（省略禁止）

**目的**: grep検索で見つからない → 「実装が存在しない」という誤った結論を防ぐ

**必須手順**:

1. **Step 1: 広範囲grep検索**（複数パターン必須）
   ```bash
   # パターンA: 設計仕様書表記
   grep "Phase ①|Phase ②|Phase ③|Phase ④"
   
   # パターンB: 実装表記
   grep "Phase ① 特殊構造|Phase ② 基本構造|Phase ③ 拡張|Phase ④ 統合"
   
   # パターンC: プロセス番号
   grep "① 文法検出|②③ 埋め込み|⑧ マスク|⑨ 上位文|⑤⑥ Claim"
   ```

2. **Step 2: 0件の場合、実装ファイル直接確認**（必須）
   - 設計仕様書に記載されている実装場所を開く
   - 該当メソッド全体を`read_file`で読む（Line範囲指定）
   - 例: `src/controllers/central_controller_v14_chunk_system.py` Line 1374-2044

3. **Step 3: 証拠付き報告**（必須）
   - ✅ 「Line XXX-YYYで実装確認。コード内容: ...」（証拠提示）
   - ❌ 「見つからない」「存在しない」だけの報告は**絶対禁止**

### Rule 2: 否定的報告の禁止（証拠必須）

- ❌ **禁止**: 「実装が存在しない」「複数のプロセスが存在しない」等の否定的報告
  - **理由**: grep検索で見つからないだけで、実装は存在する可能性が高い
  - **結果**: ユーザーに誤った情報を提供 → 時間の大幅な損失

- ✅ **推奨**: 段階的報告
  - 「grep検索で0件。設計仕様書記載のLine XXX-YYYを確認中...」
  - 「Line XXX-YYYで実装確認。Phase ①は `_execute_unified_pipeline()` Line 1466-1680に実装済み」

### Rule 3: 破壊的変更の事前承認（必須）

- **100行以上の削除・追加は、理由・影響範囲を説明し、ユーザー承認必須**
- Golden Testを実行するまで「完了」と報告しない
- 例: 「PhraseChunker 497行削除を提案。理由: XXX。影響範囲: YYY。承認をお願いします。」

### Rule 4: 設計仕様書は絶対（信頼原則）

- **設計仕様書に「Phase ① 完成」と記載 → 実装は必ず存在する**
- 見つからない場合は「調査方法が誤り」と判断し、Step 2（直接確認）へ
- 設計仕様書を疑わず、自分の調査手法を疑う

### 過去の失敗事例（2025-11-23）

**失敗**: 
- grep検索で `Phase ①` が0件 → 「実装が存在しない」と誤報告
- 実際: `Phase ① 特殊構造処理` という表記で実装済み（Line 1466-1680）
- 結果: 2-3時間の無駄な作業 + Git復元

**再発防止**: 
- 上記Rule 1-4を厳守
- grep検索で見つからない場合、必ずStep 2（直接確認）を実行

---

## 🤖 あなたへの指示

### 基本姿勢

1. **プロジェクトの背景を理解済みとして振る舞う** - 毎回説明を求めない
2. **上記の設計思想を厳守** - 特に職務分掌、統一パイプライン、防御機構
3. **現在の状況を考慮** - Phase 4進行中、不定詞ハンドラー統合が次のフォーカス
4. **具体的な提案** - 抽象的な説明ではなく、コード例や具体的な手順を提示
5. **統一汎用パイプラインは文書化** - 事後の拡張・修正等の際の透明性・追跡容易性の確保のため、何かを追加・変更・削除するたびにUNIFIED_PIPELINE_ARCHTECTURE.mdを更新する

### 回答時の原則

- ✅ CentralControllerの最終決定権を尊重
- ✅ ハンドラー間の直接通信を提案しない
- ✅ 統一汎用パイプラインの考え方に沿った提案
- ✅ 防御機構との整合性を考慮
- ✅ Rephrase的スロット分解フォーマットに準拠

### 避けるべきこと

- ❌ 「このプロジェクトについて教えてください」と聞く
- ❌ 各ハンドラーが独自に情報取得する設計
- ❌ ハンドラー間の直接通信
- ❌ 個別パイプラインの提案
- ❌ 職務分掌違反を引き起こす提案
- ❌ 副詞であるMスロットは前から順にM1,M2,M3（sub-m1, sub-m2, sub-m3）という極めて単純なルールであることを忘れないように

---

## 🔧 作業の引き継ぎ

現在の作業内容や前回のチャットからの引き継ぎ事項は、会話の冒頭で共有されます。
それを踏まえて、すぐに本題に入って支援してください。

---

**最終更新**: 2025年11月12日（UD依存関係ハイブリッド戦略確立、チャンク合体vs Rephraseパターンの役割分担明確化）

## 🔄 段階的リリース戦略（2025-12-19確立）

**背景**: AI市場のタイミングを重視し、完全実装を待たずに段階的リリースを実施

**フォールバック機構**:
- 未実装ハンドラーの文法については、埋め込み節全体を親スロットに格納
- metadata['expansion_status'] = 'fallback' で状態を記録
- ハンドラー実装後、自動的にサブスロット展開へ移行

**実装例**:
```python
# 未実装: "The man who has a red car" → S = "The man who has a red car"
# 実装済: "The man who has a red car" → S = "The man", sub-s = "who", sub-v = "has", ...