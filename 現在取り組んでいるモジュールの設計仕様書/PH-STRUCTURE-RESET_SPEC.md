
# PH-STRUCTURE-RESET 設計仕様書（改訂版）

## 目的
Rephrase-Project の構造UIを正しい大前提ルールに基づいて再設計し、適切なデータ反映・表示制御を実現することを目的とする。

## 上位スロット表示仕様

### 表示対象
| 条件 | SlotPhrase | SlotText | 補足表示 |
|-------|------------|----------|------------|
| PhraseType = word | 表示 | 表示 | なし |
| PhraseType = phrase | 非表示 | 非表示 | 展開ボタン・目印イラスト表示 |
| PhraseType = clause | 非表示 | 非表示 | 展開ボタン・目印イラスト表示 |

### 表示順序
- `Slot_display_order` に従って並べ替える

### 表示しないもの
- Slot（例：S, V などのスロット識別値そのもの）
- SubslotID（例：sub-s などのサブスロット識別値そのもの）

---

## 下位スロット表示仕様

### 表示対象
| 項目 | 表示対象 |
|-------|----------|
| SubslotElement | テキスト欄に表示 |
| SubslotText | 補助表示欄に表示 |

### 表示順序
- `display_order` に従って並べ替える

---

## 必須データ構造（slot_order_data.json）

### 上位スロット項目
- `Slot`: スロット識別子（例：S, V など）
- `SlotPhrase`: 表示対象テキスト（PhraseType = word の場合のみ表示）
- `SlotText`: 補助表示テキスト（PhraseType = word の場合のみ表示）
- `Slot_display_order`: 上位スロットの表示順序
- `PhraseType`: スロットの文要素種別（word / phrase / clause）

### 下位スロット項目
- `SubslotID`: サブスロット識別子
- `SubslotElement`: サブスロットの主要表示テキスト
- `SubslotText`: サブスロットの補助表示テキスト
- `display_order`: サブスロットの表示順序

---

## 描画制御の前提
- 上記仕様に基づき、コード内で適切な分岐・順序制御を行う。
- 指定のデータ項目が存在しない場合、表示は行わない。
- イラスト・目印は PhraseType = phrase / clause の場合のみ表示。
- **ランダマイズ結果（randomizer_all の出力データ）を前提とし、そのデータを受け取り描画すること。**
動的記載エリア → 静的DOM同期の仕組み
動的記載エリア（dynamic-slot-area）：読み取り専用エリア
MutationObserver：動的記載エリアの変更を監視
safeJsonSync関数：変更検出時に自動的に静的DOMに同期
つまり、個別ランダマイズは以下のように実装すべきです：

動的記載エリアのスロット内容のみを変更
MutationObserverが変更を検出
自動的にsafeJsonSyncが呼ばれて静的DOMに反映
---

## 補足
- 必ず最新の設計仕様ファイルをチャット開始時にアップロードし、作業根拠とすること。
- 会話やUIの見た目を根拠に推測実装することを禁止とする。
