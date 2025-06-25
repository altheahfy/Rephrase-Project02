# 分離疑問詞の疑問文表示設計仕様（Rephraseプロジェクト）

## 🎯 対象構文例

```
What do you think it is?
```

- 構造的には「what it is」が O1 スロットに対応する節。
- subslot構成：`what_sub-c1`, `it_sub-s`, `is_sub-v`
- しかし表示上、`what` は文頭、`it is` は文末に現れる。

---

## ✅ 暫定対応方針（表示仕様）

この構文においては、次のような **一時的な表示設計** を採用する：

| 要素      | 表示位置 | 表示方法                            | 備考 |
|-----------|----------|-------------------------------------|------|
| `what`    | 文頭     | 静的スロット外に**動的挿入**         | HTML上部に専用挿入領域を用意し、そこに動的記載 |
| `it is`   | 文末     | `subslot-o1-sub` に表示              | クリックで展開表示される |
| `slot-o1` | 中央     | 非表示 or `.slot-text = ""` のまま   | slot-o1 の静的DOM構造は保持するが中身は空欄 |

---

## 🔧 実装方法（暫定）

### 動的記載側（structure_builder / JSON出力）

```json
{
  "Slot": "O1",
  "DisplayText": "what",
  "DisplayAtTop": true
}
```

- `DisplayAtTop: true` が含まれるエントリは、特別なDOM位置に挿入される

### JavaScript処理（insert_test_data.js）

- `DisplayAtTop: true` フラグを持つエントリを検出
- 上部に用意した `<div id="display-top-question-word">` に `DisplayText` を挿入
- `slot-o1` への書き込みはスキップ
- `subslot-o1-sub` には `it` と `is` が通常どおり流し込まれる

---

## 📌 メリット

- 複雑な構文表示でもUIの整合性が壊れない
- 構文ID全体やsubslot構造に手を入れず、表示順だけ調整できる
- 将来 `structure_builder` 側を本格対応させた際に、そのまま移行できる

---

## 🔜 今後の発展方針

| フェーズ | 内容 |
|----------|------|
| ✅ 現在   | whatのみ動的挿入、subslotにit is、slot-o1は空欄 |
| 🔜 将来   | structure_builderで「subslot分離処理」も正式実装し、O1を文頭・文末に分離表示する構文パターンとして確立 |
