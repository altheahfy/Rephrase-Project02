# UnifiedStanzaRephraseMapper v1.0 設計仕様書

**作成日**: 2025年8月16日  
**バージョン**: v1.0  
**ステータス**: 4ハンドラー実装完了、54例文対応版  

---

## 🏗️ **システム設計思想**

### **核心概念: プラグイン型同時処理方式**

```
🎯 設計原理:
全ての専門シェフが同時に厨房に入り、
各自の専門領域を見極めて同時並行処理を行う

🏢 従来方式との差異:
❌ 旧方式: 順次選択型（15個の個別エンジンから1つを選択）
✅ 新方式: 同時処理型（全ハンドラーが並行動作して協調）
```

### **アーキテクチャ構造**

```
┌─────────────────────────────────────────────┐
│ UnifiedStanzaRephraseMapper v1.0     ---

## 📋 **更新履歴**

### **v1.1 (2025年8月17日)**
- **5ハンドラー実装完了**:
  - ✅ basic_five_pattern (基本5文型)
  - ✅ relative_clause (関係節)
  - ✅ passive_voice (受動態)
  - ✅ adverbial_modifier (副詞修飾)
  - ✅ auxiliary_complex (複合助動詞)
- **CLIインターフェース実装完了**
- **バッチ処理機能追加** (53例文一括処理対応)
- **結果照合システム分離** (compare_results.py)
- **実証済みパフォーマンス**: 45.3%完全一致率、100%処理成功率
- **ファイル整理完了**: 開発用一時ファイルのアーカイブ化

### **v1.0 (2025年8月16日)**
- 初版リリース
- 4ハンドラー実装完了
- 54例文対応版構築
- プラグイン型同時処理方式確立

---

**次期更新予定**: v1.2 (M1/M2精度向上版 - 目標: 45.3% → 60%+)──────────────────────────────────────┤
│ 統合Stanza解析 + spaCyハイブリッド補正      │
├─────────────────────────────────────────────┤
│ プラグイン型ハンドラーシステム               │
│ ┌─────────────────────────────────────────┐ │
│ │ 全ハンドラー同時実行                    │ │
│ │ ✅ _handle_basic_five_pattern           │ │
│ │ ✅ _handle_relative_clause              │ │
│ │ ✅ _handle_passive_voice                │ │
│ │ ✅ _handle_adverbial_modifier           │ │
│ │ ✅ _handle_auxiliary_complex            │ │
│ │ 🚧 _handle_modal                        │ │
│ │ 🚧 _handle_progressive                  │ │
│ │ 🚧 _handle_infinitive                   │ │
│ │ 🚧 ... (拡張予定)                       │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 位置別サブスロット管理システム               │
├─────────────────────────────────────────────┤
│ 結果統合・重複解決・優先度処理               │
└─────────────────────────────────────────────┘
```

---

## 🎯 **実装完了ハンドラー詳細**

### **1. basic_five_pattern (基本5文型)**
- **責任範囲**: S, V, O1, O2, C1, C2, Aux の基本構造認識
- **対応例文**: 第1-5文型、助動詞、時制の基本形
- **実装状況**: ✅ 完了
- **例**: "I love you." → S:I, V:love, O1:you

### **2. relative_clause (関係節)**
- **責任範囲**: who, which, that, whose, where, when, why, how の関係節処理
- **対応例文**: 関係代名詞、関係副詞、省略関係代名詞
- **実装状況**: ✅ 完了
- **例**: "The man who runs is fast." → S:"", V:is, C1:fast + sub-slots

### **3. passive_voice (受動態)**
- **責任範囲**: be動詞 + 過去分詞の受動態構造認識
- **対応例文**: 能動態↔受動態変換、by句処理
- **実装状況**: ✅ 完了
- **例**: "The letter was written by John." → S:The letter, Aux:was, V:written, M1:by John

### **4. adverbial_modifier (副詞修飾)**
- **責任範囲**: 副詞、副詞句、時間・場所・方法表現
- **対応例文**: M1, M2, M3 修飾要素の適切な分類
- **実装状況**: ✅ 完了
- **例**: "She sings beautifully." → S:She, V:sings, M1:beautifully

### **5. auxiliary_complex (複合助動詞)**
- **責任範囲**: 複数助動詞の組み合わせ、完了形、受動態助動詞
- **対応例文**: have been, will have, might have been等の複合構造
- **実装状況**: ✅ 完了
- **例**: "He has been working." → S:He, Aux:has been, V:working

---

## 🔄 **処理フロー**

### **Phase 1: 統合解析**
1. **Stanza解析**: 基本的な品詞・依存関係分析
2. **spaCyハイブリッド補正**: 特定パターンの解析修正
3. **統一doc生成**: 全ハンドラー共通の解析結果

### **Phase 2: 並行ハンドラー処理**
```python
# 全アクティブハンドラーの同時実行
for handler_name in self.active_handlers:
    handler_method = getattr(self, f'_handle_{handler_name}')
    handler_result = handler_method(main_sentence, result.copy())
    
    if handler_result:
        result = self._merge_handler_results(result, handler_result, handler_name)
```

### **Phase 3: 結果統合**
1. **重複解決**: 複数ハンドラーからの競合結果を調整
2. **優先度適用**: ハンドラー固有の優先度ルール
3. **サブスロット統合**: 位置別サブスロット管理システムによる整理

---

## 📊 **現在の対応範囲**

### **✅ 実装済み機能 (54例文100%対応)**
- **基本5文型**: 20例文 (37%)
- **関係節**: 18例文 (33%)
- **受動態**: 11例文 (20%)
- **副詞修飾**: 5例文 (9%)

---

## 📊 **実装済みハンドラーパフォーマンス (2025年8月17日)**

### **実証済み精度（53例文バッチテスト）**
| ハンドラー | 適用例文数 | 貢献度 | 主な成功パターン |
|-----------|------------|---------|------------------|
| basic_five_pattern | 53/53 | 85% | SV, SVC, SVO, SVOO, SVOC |
| relative_clause | 8/53 | 12% | who, which, that, whose節 |
| passive_voice | 6/53 | 8% | be + 過去分詞構造 |
| adverbial_modifier | 25/53 | 47% | 副詞、前置詞句、時間・場所表現 |
| auxiliary_complex | 15/53 | 28% | have been, will have等複合助動詞 |

### **全体精度実績**
- **完全一致率**: 45.3% (24/53例文)
- **部分一致率**: 54.7% (29/53例文)
- **処理成功率**: 100% (53/53例文)
- **平均処理時間**: 0.12秒/例文

### **スロット別精度詳細**
- **S (主語)**: 88.7% (47/53)
- **V (動詞)**: 96.2% (51/53)
- **C1 (補語)**: 95.2% (20/21)
- **O1 (目的語)**: 84.0% (21/25)
- **Aux (助動詞)**: 86.7% (13/15)
- **M1/M2 (修飾語)**: 62.5% (要改善領域)

### **🚧 未実装機能**
- **助動詞系**: will, can, must, should等の詳細分類
- **時制系**: 完了形、進行形、完了進行形の細分化
- **準動詞系**: 不定詞、動名詞、分詞
- **特殊構文**: 比較級、倒置、仮定法

---

## 🧪 **テスト・検証システム**

### **CLIバッチ処理システム**
- **メインコマンド**: `python unified_stanza_rephrase_mapper.py --input [file] --output [file]`
- **精度分析**: `python compare_results.py --results [file]`
- **標準テストセット**: 53例文（final_test_system/final_54_test_data.json）

### **カスタムテスト環境**
- **高精度テスト**: カスタム5例文で100%精度達成
- **構成**: 実装済み5ハンドラー完全対応版
- **継続監視**: バッチ処理による定量的精度測定

---

## 🔧 **技術仕様**

### **依存関係**
```python
# 必須ライブラリ
import stanza              # 核心NLP解析
import spacy              # ハイブリッド補正（オプション）
import logging            # デバッグ・モニタリング
```

### **初期化パラメータ**
```python
UnifiedStanzaRephraseMapper(
    language='en',           # 処理言語
    enable_gpu=False,        # GPU使用フラグ
    log_level='INFO',        # ログレベル
    use_spacy_hybrid=True    # spaCyハイブリッド使用
)
```

### **ハンドラー管理API**
```python
# ハンドラー追加
mapper.add_handler('basic_five_pattern')
mapper.add_handler('relative_clause')
mapper.add_handler('passive_voice') 
mapper.add_handler('adverbial_modifier')

# ハンドラー状態確認
active_handlers = mapper.list_active_handlers()
stats = mapper.get_stats()
```

---

## 🚀 **開発ロードマップ（95%精度達成戦略）**

### **🧠 基本戦略: ハイブリッド解析システム**

#### **レイヤー1: Stanza/spaCy基盤解析**
- **役割**: 基本的な依存関係分析、品詞タグ付け、構文解析
- **得意領域**: 明確な文法構造、一般的な文型パターン
- **制約**: 曖昧性解決、文脈依存構造に限界

#### **レイヤー2: 人間文法ロジック**
- **役割**: NLP解析の曖昧性を文脈・位置・後続語で解決
- **核心技術**: パターンマッチング + 文法的推論
- **Rephraseの利点**: 3重入れ子なしで複雑度大幅軽減

### **🎯 段階別精度目標**

#### **Phase 2-5: 基本文法完全対応 (45.3% → 75%)**
```
現在の弱点を集中攻略:
• M1/M2副詞配置精度向上: 62.5% → 85%
• 接続詞・前置詞句の適切な分類
• 複合時制の正確な認識
• 不定詞・動名詞の文脈判断
```

#### **Phase 6-10: 曖昧性解決システム (75% → 90%)**
```
人間文法ロジック本格導入:
• Flying planes問題: 後続語分析で解決
• 動名詞vs現在分詞: 文中位置で判断
• 関係節省略: 文脈パターンで補完
• 比較級・最上級: 構造的特徴抽出
```

#### **Phase 11-15: エッジケース特化 (90% → 95%)**
```
残り5%の難解ケース:
• 慣用表現・固定句の辞書ベース処理
• 口語・省略形の正規化
• 倒置・強調構文の変換
• セマンティック妥当性チェック
```

### **🔧 人間文法ロジック実装戦略**

#### **文脈依存曖昧性解決システム**
```python
class ContextualDisambiguator:
    """Stanza解析を補完する文脈判断システム"""
    
    def resolve_flying_planes_ambiguity(self, tokens):
        """Flying planes問題の解決"""
        # "Flying planes can be dangerous."
        # → 後続に助動詞/動詞 → 複合主語として確定
        
        if self._detect_pattern("ing_noun_aux_verb"):
            return "compound_subject"
        elif self._detect_pattern("ing_noun_is_abstract"):
            return "gerund_phrase"
    
    def positional_grammar_logic(self, token_pos, sentence_structure):
        """位置ベース文法判断"""
        # 文頭+ing → 動名詞可能性高
        # 文中+ing+名詞+助動詞 → 複合主語
        # 前置詞後+ing → 動名詞確定
    
    def semantic_validity_check(self, interpretation):
        """意味的妥当性による最終判断"""
        # 複数解釈が可能な場合の意味的フィルタリング
```

#### **パターン認識ライブラリ**
```python
DISAMBIGUATION_PATTERNS = {
    # Flying planes問題
    "ing_noun_can": {
        "pattern": r"(\w+ing)\s+(\w+)\s+(can|will|may|might|should)",
        "resolution": "compound_subject",
        "confidence": 0.95
    },
    
    # 動名詞vs分詞判定
    "preposition_ing": {
        "pattern": r"(in|on|at|by|for)\s+(\w+ing)",
        "resolution": "gerund",
        "confidence": 0.98
    },
    
    # 関係節省略判定
    "implied_relative": {
        "pattern": r"(The\s+\w+)\s+(I|you|we|they)\s+(saw|met|know)",
        "resolution": "relative_clause_implied",
        "confidence": 0.90
    }
}
```

### **🎯 具体的実装計画**

#### **Phase 2: M1/M2精度向上 + 文脈解決基盤**
- **期間**: 1-2週間
- **目標精度**: 45.3% → 60%
- **実装内容**:
  - adverbial_modifierハンドラー強化
  - 基本的な文脈判断ロジック実装
  - Flying planes等の典型的曖昧性解決

#### **Phase 3-5: 文法ハンドラー拡張**
- **期間**: 4-6週間  
- **目標精度**: 60% → 75%
- **実装内容**:
  - 接続詞ハンドラー
  - 不定詞・動名詞ハンドラー
  - 比較級ハンドラー
  - 文脈解決システム本格運用

#### **Phase 6-10: 高度曖昧性解決**
- **期間**: 8-12週間
- **目標精度**: 75% → 90%
- **実装内容**:
  - セマンティック解析システム
  - 慣用表現辞書
  - 複合構造最適化
  - エラーケース分析・対策

#### **Phase 11-15: 完成度向上**
- **期間**: 6-8週間
- **目標精度**: 90% → 95%
- **実装内容**:
  - 残存エッジケース特化対策
  - パフォーマンス最適化
  - 包括的テストスイート
  - 商用レベル品質保証

### **🔄 継続改善サイクル**

```
各フェーズで実行:
1. 新ハンドラー実装
2. バッチテストによる精度測定
3. 失敗ケース分析・パターン抽出  
4. 文脈判断ロジック強化
5. 回帰テスト・品質確認
6. 次フェーズ計画調整
```

### **📊 成功要因**

- **基盤の堅牢性**: 現在のプラグイン型アーキテクチャが優秀
- **測定可能性**: CLIバッチ処理による定量的評価システム
- **Rephraseの制約**: 3重入れ子なしで複雑度管理可能
- **ハイブリッド手法**: NLP + 人間文法ロジックの相乗効果

---

## 🚀 **拡張計画**

### **Phase 5: 助動詞ハンドラー**
- **優先度**: 高
- **対象**: will, can, must, should, may, might等
- **期待効果**: 未来形、可能性表現の完全対応

### **Phase 6: 時制ハンドラー**
- **優先度**: 高
- **対象**: have/has/had + 過去分詞、be + ~ing
- **期待効果**: 完了形、進行形の完全対応

### **Phase 7: 準動詞ハンドラー**
- **優先度**: 中
- **対象**: to不定詞、動名詞、分詞構文
- **期待効果**: 複雑な準動詞構造への対応

---

## 🛡️ **運用・保守**

### **品質保証**
- **テスト駆動**: 正解想定チェックによる継続的品質確認
- **段階的拡張**: 1ハンドラーずつの慎重な機能追加
- **後方互換**: 既存ハンドラーへの影響最小化

### **パフォーマンス**
- **並行処理**: 全ハンドラー同時実行による高速化
- **キャッシュ**: Stanza解析結果の再利用
- **最適化**: spaCyハイブリッドの選択的使用

### **デバッグ・監視**
- **詳細ログ**: ハンドラー個別の成功・失敗追跡
- **統計情報**: 処理時間、成功率の継続的監視
- **エラー処理**: 個別ハンドラー失敗時の全体影響回避

---

## �️ **CLIインターフェース使用方法**

### **基本コマンド構文**

```bash
# 基本的な一括処理
python unified_stanza_rephrase_mapper.py --input [入力ファイル] --output [出力ファイル]

# 出力ファイル省略（自動生成）
python unified_stanza_rephrase_mapper.py --input [入力ファイル]

# テストモード（従来のPhase 0-2実行）
python unified_stanza_rephrase_mapper.py --test-mode

# ヘルプ表示
python unified_stanza_rephrase_mapper.py --help
```

### **結果分析コマンド**

```bash
# 基本的な精度分析
python compare_results.py --results [結果ファイル]

# 詳細分析（失敗ケース表示）
python compare_results.py --results [結果ファイル] --detail

# 分析レポート保存
python compare_results.py --results [結果ファイル] --save-report [レポートファイル]
```

### **入力データ形式**

#### **詳細形式（期待値付き）**
```json
{
  "meta": {
    "total_count": 5,
    "description": "カスタム例文テスト"
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
    }
  }
}
```

#### **シンプル形式（期待値なし）**
```json
[
  "She works carefully.",
  "The book is interesting.", 
  "I give him a book.",
  "He has finished his homework.",
  "The letter was written by John."
]
```

### **実用的な使用例**

#### **例1: 既存の53例文テストセットを使用**
```bash
# 53例文一括処理
cd training/data
python unified_stanza_rephrase_mapper.py --input final_test_system/final_54_test_data.json

# 結果確認
python compare_results.py --results batch_results_[タイムスタンプ].json
```

#### **例2: カスタム例文テスト**
```bash
# カスタム例文ファイル作成（上記JSON形式）
# my_test_sentences.json

# 処理実行
python unified_stanza_rephrase_mapper.py --input my_test_sentences.json --output my_results.json

# 結果分析
python compare_results.py --results my_results.json --detail
```

#### **例3: 簡単な文法チェック**
```bash
# シンプルな例文リスト作成
# simple_sentences.json: ["She works carefully.", "The book is red."]

# 処理実行
python unified_stanza_rephrase_mapper.py --input simple_sentences.json

# 結果確認（期待値なしのため、分析結果のみ）
python compare_results.py --results batch_results_[タイムスタンプ].json
```

### **出力ファイル構造**

#### **バッチ処理結果ファイル**
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
        "grammar_info": {
          "detected_patterns": ["basic_five_pattern"],
          "handler_contributions": {...}
        },
        "meta": {
          "processing_time": 0.129,
          "sentence_id": 1,
          "active_handlers": 5
        }
      },
      "expected": {...},
      "status": "success"
    }
  }
}
```

#### **精度分析レポート**
```
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
   S: 100.0% (5/5)
   V: 100.0% (5/5)
   M2: 100.0% (1/1)
   O1: 100.0% (2/2)
   Aux: 100.0% (2/2)
```

### **実証済みパフォーマンス**

| テストセット | 完全一致率 | 処理成功率 | 主要スロット精度 |
|------------|------------|------------|----------------|
| カスタム5例文 | 100.0% | 100.0% | S:100%, V:100%, M2:100% |
| 標準53例文 | 45.3% | 100.0% | S:88.7%, V:96.2%, C1:95.2% |

### **開発・デバッグ用途**

```bash
# 詳細ログ出力で実行
python unified_stanza_rephrase_mapper.py --input test.json 2>&1 | tee debug.log

# 特定例文のみテスト
echo '["She works carefully."]' > quick_test.json
python unified_stanza_rephrase_mapper.py --input quick_test.json

# 従来のテストモードとの比較
python unified_stanza_rephrase_mapper.py --test-mode
```

---

## �📋 **更新履歴**

### **v1.1 (2025年8月17日)**
- CLIインターフェース実装完了
- バッチ処理機能追加
- 結果照合システム分離
- 53例文一括処理対応
- カスタム例文テスト機能

### **v1.0 (2025年8月16日)**
- 初版リリース
- 4ハンドラー実装完了
- 54例文対応版構築
- プラグイン型同時処理方式確立

---

**次期更新予定**: v1.2 (M1/M2精度向上版)
