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
- **randomizer_all.js が初回の V_group_key 母集団選択とスロット群決定を担当する。**
- 選ばれた V_group_key に属するスロット群からスロットをランダムに選択。
- **重要**: 全体ランダマイズ実行時に `window.fullSlotPool` を作成し、個別ランダマイズの母集団として利用可能にする。

---

## 個別ランダマイズの流れ（実装済み仕様）
- **実行**: `randomizer_individual.js` 内の各個別ランダマイズ関数（`randomizeSlotSIndividual()`, `randomizeSlotM1Individual()` 等）
- **他スロット個別ランダマイズ**: 将来的に水平展開予定（V, O, C等）。
- 現在表示中の V_group_key 母集団データ（`window.fullSlotPool`）を流用。
- 該当スロットに対応するスロット候補群を抽出し、その中からランダム選出。
- 選出したスロットデータを該当スロットの表示にのみ反映し、他スロットには影響を与えない。
- **データフロー**:
  1. 個別ランダマイズ実行 → `randomizer_individual.js`
  2. 動的エリア更新 → `buildStructure(data)` in `structure_builder.js`
  3. 静的エリア同期 → `syncUpperSlotsFromJson(data)` + `syncSubslotsFromJson(data)` in `insert_test_data_clean.js`
- **重要**: `structure_builder.js`は動的エリアのみ担当、静的エリアは`insert_test_data_clean.js`が担当
- **注意**: 両方の同期処理が必要。`structure_builder.js`のみでは静的エリアは更新されない

---

## DB構造との関係
- DB (slot_order_data.json) は V_group_key 単位でスロット群を構造化。
- ExampleID は不要。母集団キーとして Aux＋V セットで管理。

---

## 注意事項
- **ファイル責任分担**:
  - `structure_builder.js`: 動的記載エリア（dynamic-slot-area）への描画のみ
  - `insert_test_data_clean.js`: 静的記載エリア（static-slot-area）への同期処理を担当
- **重要**: 完全な表示更新には両方のファイルでの処理が必要
- randomizer_all.js が選択責任を持ち、構造モジュールは描画責任に集中。
- 個別ランダマイズボタン（🎲）は slot-container 内で SlotPhrase ラベルの横に配置し、slot-text 内には配置しない。
- **同期処理**: 個別ランダマイズでは `syncUpperSlotsFromJson()` と `syncSubslotsFromJson()` を使用。`syncDynamicToStatic()` も実装されており利用可能。

---



## O1 表示特例仕様（追加）
- O1 スロットは以下の条件で subslot 制御をランダマイザーが担当する。
  - O1 に `Slot_display_order` が複数存在する場合（例：What do you think it is? の分離構造）は subslot を生成せず、slot-mark のみを出力データに含める。
  - 上記でない場合は、他のスロット同様に subslot データを出力対象に含める。
- Structure 側はランダマイザーから受け取ったデータをそのまま描画する。
- この仕様により、特例例文と一般例文の親子スロット構造が両立する。

---

## 【2025年6月30日実装】Sスロット個別ランダマイズ機構 詳細仕様

### 概要
- **目的**: 既存の全体ランダマイズ機能を壊さず、Sスロット（主語）のみを安全に個別ランダマイズする
- **実装ファイル**: `randomizer_individual.js`
- **対象スロット**: Sスロット（メイン＋サブスロット）のみ
- **データソース**: `window.fullSlotPool`（全体ランダマイズで作成される母集団）

### 技術的実装詳細

#### データフロー
```
1. 全体ランダマイズ実行 → window.fullSlotPool作成（randomizer_all.js）
2. Sスロット個別ランダマイズ実行 → window.fullSlotPoolから候補取得（randomizer_individual.js）
3. 動的エリア更新 → buildStructure() で再構築（structure_builder.js）
4. 静的エリア同期 → syncUpperSlotsFromJson() + syncSubslotsFromJson()（insert_test_data_clean.js）
```

#### 核心となる関数
- **メイン関数**: `randomizeSlotSIndividual()`
- **データソース**: `window.fullSlotPool`（配列形式）
- **同期関数**: `syncUpperSlotsFromJson(data)`, `syncSubslotsFromJson(data)`

#### 処理ステップ
1. **前提条件チェック**
   - `window.fullSlotPool`の存在確認
   - `window.lastSelectedSlots`の存在確認

2. **候補抽出**
   ```javascript
   const sCandidates = window.fullSlotPool.filter(entry => 
     entry.Slot === "S" && !entry.SubslotID
   );
   ```

3. **重複排除**
   - 現在表示中のSスロット（例文ID）を除外
   - 候補が2個以上ある場合のみ実行

4. **ランダム選択**
   - 利用可能候補からランダムに1つ選択
   - 選択されたSスロットの例文IDに対応するサブスロットを一括取得

5. **データ更新**
   ```javascript
   // Sスロット関連を削除
   const filteredSlots = window.lastSelectedSlots.filter(slot => slot.Slot !== "S");
   
   // 新しいSスロット＋サブスロットを追加
   const newSSlots = [chosenS, ...relatedSubslots];
   filteredSlots.push(...newSSlots);
   
   // 更新
   window.lastSelectedSlots = filteredSlots;
   ```

6. **表示更新**
   - `buildStructure(data)`: 動的エリア再構築（structure_builder.js）
   - `syncUpperSlotsFromJson(data)`: メインスロット同期（insert_test_data_clean.js）
   - `syncSubslotsFromJson(data)`: サブスロット同期（insert_test_data_clean.js）

### 安全性設計

#### 既存機能への影響なし
- 全体ランダマイズ機能：変更なし
- 動的記載エリア表示機能：変更なし
- 他スロット（V, O, C等）：影響なし

#### エラーハンドリング
- 母集団データ不在時：エラーメッセージ表示
- 候補不足時：アラート表示
- 関数不在時：コンソールエラー出力

### スコープ制限
- **対象**: Sスロットのみ
- **母集団**: 同一V_group_key内の例文のみ
- **更新範囲**: Sメインスロット＋Sサブスロット群

### 拡張性
この実装パターンは他スロット（V, O, C等）への**水平展開**が可能：
- 関数名の変更（例：`randomizeSlotVIndividual()`）
- フィルタ条件の変更（例：`entry.Slot === "V"`）
- 基本的なデータフロー・同期処理は同一

### デバッグ機能
実装時に追加されたデバッグ関数群：
- `window.checkFullSlotPool()`: 母集団データ確認
- `window.checkAllSSlotSources()`: 全データソース確認
- `window.checkCurrentSelection()`: 現在選択データ確認

### 学習ポイント
1. **スモールステップアプローチ**の有効性
2. **既存の仕組み理解**の重要性（sync関数名等）
3. **段階的検証**による安全な実装
4. **データソース調査**の必要性（fullSlotPoolの構造確認）
