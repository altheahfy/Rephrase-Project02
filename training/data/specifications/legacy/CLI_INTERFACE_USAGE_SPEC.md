# Unified Stanza-Rephrase Mapper CLIインターフェース仕様書

## 概要
53例文一括処理システムのCLIインターフェース使用方法とバッチ処理仕様

**作成日**: 2025年8月17日  
**バージョン**: v1.0  
**対応システム**: Unified Stanza-Rephrase Mapper v1.0

---

## 1. 基本使用方法

### 1.1 コマンド形式

```bash
# 基本形式
python unified_stanza_rephrase_mapper.py --input [入力ファイル] --output [出力ファイル]

# 出力ファイル省略時（自動生成）
python unified_stanza_rephrase_mapper.py --input [入力ファイル]

# ヘルプ表示
python unified_stanza_rephrase_mapper.py --help

# 旧テストモード実行
python unified_stanza_rephrase_mapper.py --test-mode
```

### 1.2 結果分析コマンド

```bash
# 基本精度分析
python compare_results.py --results [結果ファイル]

# 詳細分析（失敗ケース表示）
python compare_results.py --results [結果ファイル] --detail

# レポート保存
python compare_results.py --results [結果ファイル] --save-report [レポートファイル]
```

---

## 2. 入力データ形式

### 2.1 詳細形式（期待値付き）

```json
{
  "meta": {
    "total_count": 3,
    "description": "テスト例文セット"
  },
  "data": {
    "1": {
      "sentence": "She works carefully.",
      "expected": {
        "main_slots": {
          "S": "She",
          "V": "works",
          "M2": "carefully"
        },
        "sub_slots": {}
      }
    },
    "2": {
      "sentence": "The book is interesting.",
      "expected": {
        "main_slots": {
          "S": "The book",
          "V": "is",
          "C1": "interesting"
        },
        "sub_slots": {}
      }
    },
    "3": {
      "sentence": "He has finished his homework.",
      "expected": {
        "main_slots": {
          "S": "He",
          "Aux": "has",
          "V": "finished",
          "O1": "his homework"
        },
        "sub_slots": {}
      }
    }
  }
}
```

### 2.2 シンプル形式（期待値なし）

```json
[
  "She works carefully.",
  "The book is interesting.",
  "He has finished his homework.",
  "The letter was written by John.",
  "The man who runs fast is strong."
]
```

---

## 3. 実行例

### 3.1 既存53例文テストセット実行

```bash
# 53例文一括処理
cd training/data
python unified_stanza_rephrase_mapper.py --input final_test_system/final_54_test_data.json

# 精度確認（自動生成されたファイル名を使用）
python compare_results.py --results batch_results_20250817_143000.json
```

### 3.2 カスタム例文テスト

```bash
# カスタム例文処理
python unified_stanza_rephrase_mapper.py --input my_test_sentences.json --output my_results.json

# 結果分析
python compare_results.py --results my_results.json
```

### 3.3 簡易テスト（期待値なし）

```bash
# シンプル形式で処理
python unified_stanza_rephrase_mapper.py --input simple_sentences.json

# 結果確認（期待値なしなので基本情報のみ）
python compare_results.py --results batch_results_[タイムスタンプ].json
```

---

## 4. 出力形式

### 4.1 処理結果ファイル構造

```json
{
  "meta": {
    "input_file": "my_test_sentences.json",
    "processed_at": "2025-08-17T14:50:00.000000",
    "total_sentences": 5,
    "success_count": 5,
    "error_count": 0
  },
  "results": {
    "1": {
      "sentence": "She works carefully.",
      "analysis_result": {
        "sentence": "She works carefully.",
        "slots": {
          "S": "She",
          "V": "works",
          "M2": "carefully"
        },
        "sub_slots": {},
        "grammar_info": {...},
        "meta": {...}
      },
      "expected": {...},
      "status": "success"
    }
  }
}
```

### 4.2 精度分析レポート

```
============================================================
📊 精度分析レポート
============================================================
📁 対象ファイル: my_results.json
⏰ 分析時刻: 2025-08-17T14:50:10.616823

📈 全体統計:
   総ケース数: 5
   完全一致: 5
   部分一致: 0
   失敗: 0
   🎯 完全一致率: 100.0%

🔍 スロット別精度:
   Aux: 100.0% (2/2)
   C1: 100.0% (1/1)
   M1: 100.0% (1/1)
   M2: 100.0% (1/1)
   O1: 100.0% (2/2)
   S: 100.0% (5/5)
   V: 100.0% (5/5)
```

---

## 5. スロット型定義

### 5.1 メインスロット

| スロット | 説明 | 例 |
|---------|------|-----|
| S | 主語 | "She", "The car" |
| V | 動詞 | "works", "is" |
| O1 | 目的語1 | "you", "the book" |
| O2 | 目的語2 | "a book" |
| C1 | 補語1 | "red", "interesting" |
| C2 | 補語2 | - |
| Aux | 助動詞 | "has", "was", "is being" |
| M1 | 前置詞句 | "by John", "in the park" |
| M2 | 副詞 | "carefully", "quickly" |
| M3 | その他修飾語 | - |
| Adv | 副詞節 | - |

### 5.2 サブスロット（関係節用）

| スロット | 説明 | 例 |
|---------|------|-----|
| sub-s | 関係節主語 | "The man who" |
| sub-v | 関係節動詞 | "runs" |
| sub-o1 | 関係節目的語 | - |
| sub-c1 | 関係節補語 | "red" |
| sub-m1 | 関係節前置詞句 | - |
| sub-m2 | 関係節副詞 | "fast" |
| sub-aux | 関係節助動詞 | "was" |

---

## 6. パフォーマンス実績

### 6.1 実証済み精度（2025年8月17日時点）

| テストセット | 完全一致率 | 処理成功率 | 備考 |
|------------|-----------|----------|------|
| カスタム5例文 | 100.0% (5/5) | 100.0% | 基本文型中心 |
| 53例文フルセット | 45.3% (24/53) | 100.0% | 複雑構文含む |

### 6.2 スロット別精度（53例文セット）

| スロット | 精度 | 正解数/総数 | 状況 |
|---------|------|------------|------|
| V (動詞) | 96.2% | 51/53 | ✨ 優秀 |
| C1 (補語) | 95.2% | 20/21 | ✨ 優秀 |
| Aux (助動詞) | 94.7% | 18/19 | ✨ 優秀 |
| S (主語) | 88.7% | 47/53 | ✅ 良好 |
| O1 (目的語) | 75.0% | 6/8 | ✅ 良好 |
| M2 (副詞) | 53.8% | 14/26 | ⚠️ 改善要 |
| M1 (前置詞句) | 42.9% | 6/14 | ⚠️ 改善要 |

---

## 7. トラブルシューティング

### 7.1 よくあるエラー

#### エラー: `FileNotFoundError`
```bash
❌ エラー: ファイルが見つかりません - test.json
```
**対処法**: 入力ファイルのパスを確認してください。

#### エラー: `JSON解析エラー`
```bash
❌ JSON解析エラー: Expecting ',' delimiter: line 5 column 3
```
**対処法**: JSONファイルの形式を確認してください。

#### エラー: `循環参照エラー`
```bash
❌ 保存エラー: Circular reference detected
```
**対処法**: システム内部で自動修正されます。再実行してください。

### 7.2 パフォーマンス

- **初期化時間**: 約4秒（Stanza + spaCy読み込み）
- **処理速度**: 約0.1-0.3秒/文
- **メモリ使用量**: 約1GB（Stanzaモデル含む）

---

## 8. システム要件

### 8.1 必要パッケージ

```bash
# Python 3.8+
pip install stanza spacy torch

# 言語モデル
python -c "import stanza; stanza.download('en')"
python -m spacy download en_core_web_sm
```

### 8.2 ファイル構成

```
training/data/
├── unified_stanza_rephrase_mapper.py  # メインシステム
├── compare_results.py                 # 分析ツール
├── final_test_system/
│   └── final_54_test_data.json       # 53例文テストセット
├── my_test_sentences.json            # カスタム例文（期待値付き）
├── simple_sentences.json             # シンプル例文
└── [結果ファイル群]
```

---

## 9. 更新履歴

| 日付 | バージョン | 更新内容 |
|------|-----------|---------|
| 2025-08-17 | v1.0 | 初版作成、CLIインターフェース実装 |

---

## 10. 関連ドキュメント

- `REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md` - スロット配置ルール
- `Rephrase_リファクタリング統合設計仕様書_進捗反映版.md` - システム全体設計
- `unified_stanza_rephrase_mapper.py` - ソースコード

---

**作成者**: Unified Stanza-Rephrase Mapper Development Team  
**最終更新**: 2025年8月17日
