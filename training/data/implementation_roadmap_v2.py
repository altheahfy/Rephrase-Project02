#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rephrase Rule Dictionary v2.0 実装計画書
===========================================
作成日: 2025年8月10日
現状分析結果を基にした完全な実装ロードマップ

【現状の問題点】
1. CompleteRephraseParsingEngine (3,100行): パターンマッチング型とspaCy構造解析の設計矛盾
2. Rule Dictionary v1.0 (25ルール): サブスロット自動生成機能が完全に不足
3. "ago/for duplication problem": 時間副詞の重複分類問題
4. 関係詞節・複文構造の手動処理: "The boy who plays tennis" → サブスロット分解不可

【5文型フルセット分析結果】
- 有効メインスロット: 273個
- サブスロット要素: 192個  
- clause型処理パターン: 44個
- 必須サブスロット種類: 9種類 ['sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
"""

# ================================================================
# フェーズ1: Rule Dictionary v2.0 基盤設計 (優先度: 最高)
# ================================================================

PHASE_1_FOUNDATION = {
    "目標": "spaCy完全連携の新ルール辞書基盤を構築",
    "期間": "1-2日",
    "成果物": [
        "rephrase_rules_v2.0.json",
        "RuleDictionaryV2.py",
        "SpacyRephraseParser.py"
    ],
    "実装内容": {
        "1.1_基本アーキテクチャ設計": {
            "説明": "パターンマッチングからspaCy構造解析への完全移行",
            "技術要件": [
                "spaCy依存構造解析 (doc._, token.dep_)",
                "エンティティ認識との連携 (doc.ents)",
                "句構造解析 (noun_chunks, 前置詞句)",
                "関係詞節の自動認識"
            ],
            "具体的実装": [
                "class SpacyRephraseParser:",
                "  def parse_sentence_structure(self, doc)",
                "  def identify_main_slots(self, doc)", 
                "  def generate_subslots(self, slot, tokens)",
                "  def resolve_clause_structure(self, clause_tokens)"
            ]
        },
        "1.2_サブスロット生成エンジン": {
            "説明": "spaCy構造解析に基づく9種類のサブスロット自動生成システム",
            "必須機能": [
                "sub-s: nsubj/nsubjpass依存関係による主語抽出 (関係詞処理はdep_='relcl')",
                "sub-aux: aux/auxpass依存ラベルによる助動詞認識",
                "sub-v: ROOT/ccomp/relclでの動詞核抽出",
                "sub-o1/o2: dobj/iobj/pobj構造による目的語階層処理",
                "sub-c1/c2: acomp/xcomp/attr による補語認識",
                "sub-m1/m2/m3: advmod/prep/npadvmod による修飾句分類"
            ],
            "構造的判定原理": [
                "表現マッチング全面禁止",
                "依存構造ラベル(token.dep_)による分類",
                "品詞タグ(token.pos_)と係り受け(token.head)の組み合わせ判定",
                "文法的役割に基づく自動分類"
            ]
        },
        "1.3_clause型処理システム": {
            "説明": "spaCy依存関係による複文・関係詞節の階層構造解析",
            "対象構造_依存ラベル": [
                "関係詞節: dep_='relcl' (relative clause)",
                "時間副詞節: dep_='advcl' + mark='when/while'",
                "理由副詞節: dep_='advcl' + mark='because/since'", 
                "結果副詞節: dep_='advcl' + mark='so'",
                "対比副詞節: dep_='advcl' + mark='although'"
            ],
            "実装方針": "依存関係グラフ(doc._, token.children)からの構造的抽出のみ",
            "禁止事項": "文字列マッチング ('who', 'because' 等の具体語検索禁止)"
        }
    }
}

# ================================================================
# フェーズ2: CompleteRephraseParsingEngine改修 (優先度: 高)
# ================================================================

PHASE_2_ENGINE_REFACTOR = {
    "目標": "既存3,100行エンジンのspaCy完全連携化",
    "期間": "2-3日", 
    "前提条件": "フェーズ1完了",
    "改修対象": "CompleteRephraseParsingEngine.py",
    "主要変更点": {
        "2.1_パターンマッチング除去": {
            "削除対象": [
                "正規表現ベースのルール適用",
                "文字列パターンマッチング", 
                "手動の句構造認識"
            ],
            "置換方法": "SpacyRephraseParser クラスへの完全移行"
        },
        "2.2_ago/for重複問題解決": {
            "問題": "時間副詞の重複分類 (M2:['ago', 'ago met'] + M3:['a few days ago'])",
            "解決方針": [
                "spaCy依存関係による一意分類",
                "時間副詞の階層優先順位設定",
                "重複チェック機能の実装"
            ]
        },
        "2.3_品質保証システム統合": {
            "統合対象": "quality_checker.py の全チェック機能",
            "自動化範囲": [
                "check_aux_order(): 助動詞順序検証",
                "check_possessive_pronouns(): 所有格処理", 
                "check_articles(): 冠詞処理",
                "check_time_expressions(): 時間表現重複防止"
            ]
        }
    }
}

# ================================================================
# フェーズ3: 高度機能実装 (優先度: 中)
# ================================================================

PHASE_3_ADVANCED_FEATURES = {
    "目標": "複雑な文法構造への対応拡充",
    "期間": "3-4日",
    "実装機能": {
        "3.1_分離疑問詞処理": {
            "対象": "文頭に移動する疑問詞・感嘆詞のサブスロット",
            "例": [
                "'What do you think it is?' → order:1 O1:'what' + order:5 O1:'it is'",
                "'What cruelty people are capable of!' → order:1 O1:'what cruelty'"
            ],
            "技術": "語順変化とサブスロット分離の処理",
            "特殊性": "上位スロットのorderで制御、同一スロット内の要素分離"
        },
        "3.2_入れ子構造処理": {
            "対象": "関係詞節内の関係詞節、複合修飾句",
            "例": "'the manager who supervised the project that everyone had been waiting for'",
            "技術": "再帰的構造解析"
        },
        "3.3_語順最適化": {
            "対象": "V_group_key内の絶対順序ルール",
            "現状": "44-66%の数値的無駄",
            "改善": "効率的順序アルゴリズム"
        },
        "3.4_例文生成支援": {
            "機能": "新しい文法パターンの自動例文生成",
            "連携": "Excel_Generator.pyとの統合"
        }
    }
}

# ================================================================
# フェーズ4: システム統合・本番投入 (優先度: 中)
# ================================================================

PHASE_4_PRODUCTION = {
    "目標": "本番環境での安定運用",
    "期間": "2-3日",
    "作業内容": {
        "4.1_性能最適化": {
            "対象": "大量例文処理の高速化",
            "目標": "1000例文/分以上",
            "手法": "spaCy並列処理、キャッシュ機能"
        },
        "4.2_エラーハンドリング": {
            "機能": "未知構文の安全な処理",
            "フォールバック": "v1.0ルール辞書への自動切り替え"
        },
        "4.3_本番データ移行": {
            "対象": "既存例文DBの全面再処理",
            "検証": "品質チェッカーによる全件検査"
        }
    }
}

# ================================================================
# 実装優先順位と継続性
# ================================================================

IMPLEMENTATION_PRIORITY = [
    {
        "順位": 1,
        "フェーズ": "Phase 1.2 - サブスロット生成エンジン",
        "理由": "現在最も不足している核心機能",
        "即座に着手可能": True,
        "継続性": "他チャットでも独立して実装可能"
    },
    {
        "順位": 2, 
        "フェーズ": "Phase 1.3 - clause型処理システム",
        "理由": "関係詞節処理が最重要課題",
        "継続性": "明確な仕様とテストケース完備"
    },
    {
        "順位": 3,
        "フェーズ": "Phase 2.2 - ago/for重複問題解決", 
        "理由": "既知の具体的バグ修正",
        "継続性": "test_time_adverbs.pyで再現可能"
    },
    {
        "順位": 4,
        "フェーズ": "Phase 3.1 - 分離疑問詞処理",
        "理由": "特殊な語順変化パターン、上位スロット制御が必要",
        "継続性": "ex009, ex010で具体例確認済み",
        "技術的特徴": "同一スロット内要素の分離処理"
    }
]

# ================================================================
# 次チャット継続用の重要情報
# ================================================================

CONTINUATION_INFO = {
    "現在完了している分析": [
        "5文型フルセットDB完全分析 (final_rephrase_analysis.py)",
        "サブスロット生成パターン特定 (9種類)",
        "clause型処理ルール抽出 (44パターン)",
        "関係詞節分解構造の解明"
    ],
    "すぐに実装開始できるファイル": [
        "rephrase_rules_v2.0.json - 新ルール辞書",
        "SpacyRephraseParser.py - 構造解析エンジン",
        "subslot_generator.py - サブスロット自動生成"
    ],
    "参照必須ファイル": [
        "final_rephrase_analysis.py - 完全分析結果",
        "（小文字化した最初の5文型フルセット）例文入力元.xlsx - 正解データ",
        "quality_checker.py - 品質検証ツール",
        "test_time_adverbs.py - 重複問題テスト"
    ],
    "重要な発見": {
        "関係詞節パターン": "sub-s: 'the manager who', sub-aux: 'had', sub-v: 'taken'",
        "複文処理パターン": "sub-m1: 'even though', sub-s: 'he', sub-v: 'was'",
        "clause型分布": "S:9, M2:9, M3:9, O1:8, M1:4, O2:3, C1:2"
    }
}

if __name__ == "__main__":
    print("=== Rephrase Rule Dictionary v2.0 実装計画書 ===")
    print(f"作成日: {CONTINUATION_INFO}")
    print("\n【実装優先順位】")
    for item in IMPLEMENTATION_PRIORITY:
        print(f"{item['順位']}. {item['フェーズ']}")
        print(f"   理由: {item['理由']}")
        print(f"   継続性: {item['継続性']}\n")
    
    print("この実装計画書により、次のチャットでも作業を継続できます。")
