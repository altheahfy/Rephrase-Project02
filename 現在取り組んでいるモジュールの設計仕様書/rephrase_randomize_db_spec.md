# Rephraseプロジェクト ランダマイズアルゴリズム・DB設計仕様書（改訂版）

## 目的
Rephraseプロジェクトにおけるランダマイズ処理の仕様、DB設計との関係、全体ランダマイズ・個別ランダマイズの詳細を記述し、実装・引き継ぎ時の基準文書とする。

---

## ランダマイズ母集団の設計
- 母集団キーは **構文ID + V_group_key (Aux＋V セット)**。
- V_group_key は助動詞＋動詞の組を一意に示すもの。
- 各スロットデータは V_group_key によってどの母集団に属するかが決まる。
## V_group_key 母集団の識別番号ランダマイズ仕様（追加）
- V_group_key 母集団内のスロットは、例文IDを手掛かりに親スロットとサブスロットをペアとして整理する。
- 各スロットは、例文IDを超えた混合母集団形成のため「識別番号」を付与し、例：M1-1, M1-2 のように管理する。
- ランダマイズは識別番号単位で行われ、選出された識別番号に対応する親スロットとそのサブスロットを一括で出力対象とする。
- ExampleID は識別番号付与後のランダマイズ処理では使用せず、スロット種間の自然な混合を保証する。
---

## 全体ランダマイズの流れ
- **randomizer_all が初回の V_group_key 母集団選択とスロット群決定を担当する。**
- 選ばれた V_group_key に属するスロット群からスロットをランダムに選択。

---

## 個別ランダマイズの流れ（統合仕様追加）
- 個別ランダマイズは randomizer_individual.js 内の `randomizeIndividual(slotId)` 関数で実装。
- 現在表示中の V_group_key 母集団データを流用。
- 該当 slotId に対応するスロット候補群を抽出し、その中からランダム選出。
- 選出したスロットデータを該当 slotId の表示にのみ反映し、他スロットには影響を与えない。
- 描画は既存の structure_builder.js の共通描画モジュールに委ねる。
（詳細）
個別ランダマイズとは、同じV_groupe_keyの中に複数の例文がある場合（makeならmakeを使った例文が３つなど）に、そのmakeグループの例文の中から、他のSセット、M1セットなどを含めた母集団に対して、一つを選ぶというもの。
例えば、You make me nervous. I make this project bigger one. She make it easy.という3つの例文があったとき、Sの個別ランダマイズボタンを押すと、You, I, Sheが入れ替わるということだ。もしそれらが複文構造になっていたら（The manager who tends to be nervous）、そのサブスロットの中身ごと入れ替わるということ。
window.loadedJsonDataは全体ランダマイズ（randomizer_all.js、structure_builder.js）の結果として現在表示中のデータセット。
個別ランダマイズは、slot_order_data.jsonをロードした時点で表示されいてる例文の個別上位スロット（例：Sスロット）だけを、同じV_group_key内の他の例文の同じ上位スロット（例：Sスロット）と入れ替える。母集団は、全体ランダマイズの結果としてrandomizer_all.js、structure_builder.jsからhtmlに渡されるwindow.slotsetsの中にある。
---

## DB構造との関係
- DB (slot_order_data.json) は V_group_key 単位でスロット群を構造化。
- ExampleID は不要。母集団キーとして Aux＋V セットで管理。

---

## 注意事項
- structure_builder.js は選択済のスロット群を受け取り描画するのみとする。
- randomizer_all が選択責任を持ち、構造モジュールは描画責任に集中。
- 個別ランダマイズデータも structure_builder.js がそのまま描画すること。
- 個別ランダマイズボタン（🎲）は slot-container 内で SlotPhrase ラベルの横に配置し、slot-text 内には配置しない。

---



## O1 表示特例仕様（追加）
- O1 スロットは以下の条件で subslot 制御をランダマイザーが担当する。
  - O1 に `Slot_display_order` が複数存在する場合（例：What do you think it is? の分離構造）は subslot を生成せず、slot-mark のみを出力データに含める。
  - 上記でない場合は、他のスロット同様に subslot データを出力対象に含める。
- Structure 側はランダマイザーから受け取ったデータをそのまま描画する。
- この仕様により、特例例文と一般例文の親子スロット構造が両立する。
