# AbsoluteOrderManager システム 引き継ぎ書

**作成日**: 2025年8月28日  
**状況**: 実装完了だが出力結果に重大な問題あり  
**緊急度**: 🚨 高（設計根本から見直し必要）

---

## 🚨 現在の重大な問題

### 問題1: 絶対順序の期待値と実際の出力が全く異なる

#### 期待値（テストデータより）
```json
Case 83: "What did he tell her at the store?"
期待値: {
  "O2": 1,    // What → position 1
  "Aux": 3,   // did → position 3  
  "S": 4,     // he → position 4
  "V": 5,     // tell → position 5
  "O1": 6,    // her → position 6
  "M3": 8     // at the store → position 8
}
```

#### 実際の出力
```
📍 絶対位置: Aux(did)_2 → S(he)_3 → V(tell)_4 → O1(her)_5 → O2(What)_6 → M3(at the store)_7
```

**問題点**:
- O2(What)が期待値1に対して実際は6
- Aux(did)が期待値3に対して実際は2
- 位置番号が連続（1,2,3,4,5,6,7）になっているが、期待値は飛び番（1,3,4,5,6,8）
- **根本的にアルゴリズムが異なる**

---

## 🔍 問題の原因分析

### 現在の実装の問題点

1. **連続位置付与システム**
   - 現在: 実在スロットに1,2,3...と連続番号付与
   - 期待: 固定位置テーブルに基づく飛び番号付与

2. **Universal Relative Order Systemの設計ミス**
   - 現在の相対順序リストは実装者の推測
   - 実際の期待値とは全く異なるルール

3. **文法グループ分類の不一致**
   - tellグループの処理が期待値と不整合
   - wh-word配置ルールの根本的な誤解

---

## 📋 正しい仕様の解析

### Case 83-86の期待値パターン分析

| Case | 文 | 期待される絶対位置 |
|------|---|-------------------|
| 83 | What did he tell her at the store? | O2:1, Aux:3, S:4, V:5, O1:6, M3:8 |
| 84 | Did he tell her a secret there? | Aux:3, S:4, V:5, O1:6, O2:7, M3:8 |
| 85 | Did I tell him a truth in the kitchen? | Aux:3, S:4, V:5, O1:6, O2:7, M3:8 |
| 86 | Where did you tell me a story? | M2:1, Aux:3, S:4, V:5, O1:6, O2:7 |

#### パターン発見:
1. **wh-word → position 1**（疑問詞が文頭）
2. **Aux → position 3**（固定位置）
3. **S → position 4**（固定位置）
4. **V → position 5**（固定位置）
5. **O1 → position 6**（固定位置）
6. **O2 → position 7**（疑問詞がない場合の標準位置）
7. **M3 → position 8**（場所・時間の固定位置）

**重要**: 位置2は使用されていない（予約済み？）

---

## 🛠️ 必要な修正内容

### 1. 絶対位置テーブルの再設計

```python
# 正しい絶対位置テーブル（tellグループ）
TELL_ABSOLUTE_POSITIONS = {
    'wh_word': 1,      # What, Where, When, Why, How
    'position_2': None, # 予約済み（未使用）
    'Aux': 3,          # did, do, does, will, would
    'S': 4,            # 主語
    'V': 5,            # 動詞
    'O1': 6,           # 間接目的語
    'O2': 7,           # 直接目的語（標準位置）
    'M3': 8            # 場所・時間・方法
}
```

### 2. wh-word特別処理

```python
def apply_wh_word_override(slots, positions):
    """
    wh-wordがある場合の特別処理
    - wh-wordを含むスロットを position 1 に移動
    - 該当スロットの元の位置は空ける
    """
    for slot, value in slots.items():
        if self.is_wh_word(value):
            positions[slot] = 1  # 強制的に position 1
            break
```

### 3. 固定位置システムの実装

```python
def get_fixed_position(self, slot_type, v_group_key):
    """
    スロットタイプに基づく固定位置取得
    グループごとの固定位置テーブルを参照
    """
    position_table = self.FIXED_POSITIONS[v_group_key]
    return position_table.get(slot_type, 999)  # フォールバック
```

---

## 📝 次のアクションプラン

### 🎯 Phase 1: 緊急修正（1-2時間）

1. **固定位置テーブル作成**
   - tellグループの正確な位置マッピング作成
   - 他グループの期待値調査・マッピング作成

2. **アルゴリズム全面書き換え**
   - 連続位置付与 → 固定位置テーブル参照に変更
   - Universal Relative Order System廃止

3. **wh-word特別処理実装**
   - position 1への強制配置機能

### 🎯 Phase 2: 全面検証（2-3時間）

1. **全テストケース検証**
   - Cases 1-86の期待値vs実際値比較
   - 各文法グループの固定位置パターン発見

2. **固定位置テーブル完成**
   - 10グループ全ての正確なマッピング

### 🎯 Phase 3: 最終調整（1時間）

1. **エラーハンドリング強化**
2. **設計仕様書更新**
3. **検証レポート作成**

---

## 🔧 技術的な修正ポイント

### 現在のファイル状況
```
training/data/
├── absolute_order_manager.py                    # 基本実装（問題あり）
├── absolute_order_manager_fixed.py              # バグ修正版（問題あり）
├── absolute_order_manager_group_fixed.py        # 最新版（問題あり）
├── test_real_data_to_file.py                    # 検証スクリプト
└── final_54_test_data_with_absolute_order.json  # 正しい期待値データ
```

### 修正が必要なコア機能

1. **`apply_absolute_order`メソッド**
   - 連続位置付与ロジックを固定位置参照に変更

2. **`UNIVERSAL_RELATIVE_ORDER`辞書**
   - 完全廃止、`FIXED_POSITIONS`辞書に置き換え

3. **`calculate_positions`メソッド**
   - 全面書き換え必要

---

## ⚠️ 重要な注意事項

### データの信頼性
- `final_54_test_data_with_absolute_order.json`の期待値が正解
- 現在の実装は推測ベースで作成されており、実際の仕様と乖離

### 作業優先度
1. **最優先**: tellグループ（Cases 83-86）の修正
2. **高優先**: 基本5文型（Cases 1-17）の検証
3. **中優先**: 副詞グループ（Cases 18-42）の検証
4. **低優先**: 関係節・複合構文（Cases 43-82）の検証

### リスクファクター
- 全10文法グループで同様の問題が発生している可能性
- 設計思想そのものの変更が必要
- 既存のUniversal Relative Order System は使用不可

---

## 📞 引き継ぎ時の確認事項

1. **期待値データの最新性確認**
   - `final_54_test_data_with_absolute_order.json`が最新版か
   - 他に参照すべき仕様書があるか

2. **固定位置テーブルの正確性**
   - tellグループ以外の期待値パターン調査
   - position 2が全グループで未使用かの確認

3. **wh-word処理の詳細**
   - position 1への配置が全文法グループ共通ルールか
   - 例外的なケースがあるか

---

**緊急連絡先**: システム設計者  
**Next Action**: 固定位置テーブル作成から開始  
**Deadline**: 緊急対応として24時間以内の修正完了が必要
