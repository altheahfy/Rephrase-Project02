#!/usr/bin/env python3
"""
spaCy完全対応Rephraseエンジン拡張 - フェーズ1
高頻度・高価値依存関係の完全統合

対象依存関係:
1. compound (複合語)
2. conj + cc (並列構造)
3. neg (否定)
4. nummod (数詞修飾)
"""

import json
from typing import Dict, List, Any

class SpacyRephraseExtension:
    def __init__(self):
        self.new_rules = []
        self.dependency_mapping = {
            # フェーズ1: 高頻度・高価値依存関係
            'compound': {
                'slot': 'M1',  # 修飾語スロット
                'priority': 25,
                'description': '複合語・複合名詞の統合処理'
            },
            'conj': {
                'slot': 'M2',  # 並列要素スロット
                'priority': 24,
                'description': '並列構造（and, or, but等）の統合処理'
            },
            'cc': {
                'slot': 'M2',  # 等位接続詞
                'priority': 23,
                'description': '等位接続詞（and, or, but等）の処理'
            },
            'neg': {
                'slot': 'M1',  # 否定修飾
                'priority': 26,
                'description': '否定表現（not, never, no等）の処理'
            },
            'nummod': {
                'slot': 'M1',  # 数詞修飾
                'priority': 22,
                'description': '数詞修飾（three books, first time等）の処理'
            }
        }
        
    def generate_compound_rule(self) -> Dict[str, Any]:
        """複合語処理ルール生成"""
        return {
            "id": "compound-noun-phrase-M1",
            "description": "複合語・複合名詞の完全統合（New York, ice cream等）",
            "priority": 25,
            "triggers": {
                "dependency_conditions": ["compound"]
            },
            "conditions": {
                "dependency_pattern": {
                    "target_dep": "compound",
                    "head_pos": ["NOUN", "PROPN"],
                    "child_pos": ["NOUN", "PROPN", "ADJ"]
                }
            },
            "assignments": [
                {
                    "slot": "M1",
                    "extraction_method": "compound_phrase",
                    "value_source": "full_compound_phrase"
                }
            ]
        }
    
    def generate_conjunction_rules(self) -> List[Dict[str, Any]]:
        """並列構造処理ルール生成"""
        rules = []
        
        # 並列要素ルール
        conj_rule = {
            "id": "conjunction-parallel-M2",
            "description": "並列構造の完全統合（cats and dogs, red or blue等）",
            "priority": 24,
            "triggers": {
                "dependency_conditions": ["conj"]
            },
            "conditions": {
                "dependency_pattern": {
                    "target_dep": "conj",
                    "parallel_elements": True
                }
            },
            "assignments": [
                {
                    "slot": "M2",
                    "extraction_method": "conjunction_phrase",
                    "value_source": "full_parallel_structure"
                }
            ]
        }
        
        # 等位接続詞ルール
        cc_rule = {
            "id": "coordinating-conjunction-M2",
            "description": "等位接続詞の統合（and, or, but, so等）",
            "priority": 23,
            "triggers": {
                "dependency_conditions": ["cc"]
            },
            "conditions": {
                "dependency_pattern": {
                    "target_dep": "cc",
                    "conjunction_words": ["and", "or", "but", "so", "yet", "nor"]
                }
            },
            "assignments": [
                {
                    "slot": "M2",
                    "extraction_method": "coordinating_conjunction",
                    "value_source": "conjunction_with_context"
                }
            ]
        }
        
        rules.extend([conj_rule, cc_rule])
        return rules
    
    def generate_negation_rule(self) -> Dict[str, Any]:
        """否定表現処理ルール生成"""
        return {
            "id": "negation-modifier-M1",
            "description": "否定表現の完全統合（not, never, no, none等）",
            "priority": 26,
            "triggers": {
                "dependency_conditions": ["neg"]
            },
            "conditions": {
                "dependency_pattern": {
                    "target_dep": "neg",
                    "negation_words": ["not", "n't", "never", "no", "none", "nothing", "nobody", "nowhere"],
                    "scope_detection": True
                }
            },
            "assignments": [
                {
                    "slot": "M1",
                    "extraction_method": "negation_scope",
                    "value_source": "negation_with_scope"
                }
            ]
        }
    
    def generate_nummod_rule(self) -> Dict[str, Any]:
        """数詞修飾処理ルール生成"""
        return {
            "id": "numeric-modifier-M1",
            "description": "数詞修飾の完全統合（three books, first time, 100 dollars等）",
            "priority": 22,
            "triggers": {
                "dependency_conditions": ["nummod"]
            },
            "conditions": {
                "dependency_pattern": {
                    "target_dep": "nummod",
                    "numeric_types": ["cardinal", "ordinal"],
                    "head_pos": ["NOUN", "PROPN"]
                }
            },
            "assignments": [
                {
                    "slot": "M1",
                    "extraction_method": "numeric_phrase",
                    "value_source": "number_with_noun"
                }
            ]
        }
    
    def generate_all_phase1_rules(self) -> List[Dict[str, Any]]:
        """フェーズ1全ルール生成"""
        rules = []
        
        # 1. 複合語ルール
        rules.append(self.generate_compound_rule())
        
        # 2. 並列構造ルール
        rules.extend(self.generate_conjunction_rules())
        
        # 3. 否定表現ルール
        rules.append(self.generate_negation_rule())
        
        # 4. 数詞修飾ルール
        rules.append(self.generate_nummod_rule())
        
        return rules
    
    def create_enhanced_rules_file(self, output_file: str = "enhanced_rephrase_rules_phase1.json"):
        """拡張ルールファイル生成"""
        
        # 既存ルール読み込み
        try:
            with open("rephrase_rules_v1.0.json", 'r', encoding='utf-8') as f:
                existing_rules = json.load(f)
                print(f"✅ 既存ルール読み込み: {len(existing_rules)}個")
        except FileNotFoundError:
            existing_rules = {}
            print("⚠️ 既存ルールファイルが見つかりません。新規作成します。")
        
        # フェーズ1新ルール生成
        phase1_rules = self.generate_all_phase1_rules()
        
        # ルール統合
        enhanced_rules = existing_rules.copy()
        for rule in phase1_rules:
            enhanced_rules[rule["id"]] = rule
            
        # ファイル出力
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_rules, f, ensure_ascii=False, indent=2)
        
        print(f"🚀 拡張ルールファイル生成完了: {output_file}")
        print(f"  既存ルール: {len(existing_rules)}個")
        print(f"  新規ルール: {len(phase1_rules)}個")
        print(f"  合計ルール: {len(enhanced_rules)}個")
        
        return enhanced_rules
    
    def generate_test_sentences(self) -> List[str]:
        """フェーズ1機能テスト用例文生成"""
        return [
            # compound テスト
            "I live in New York City.",
            "She loves ice cream and chocolate cake.",
            "The software engineer works hard.",
            
            # conj + cc テスト  
            "Cats and dogs are popular pets.",
            "We can go by car or by train.",
            "He is smart but lazy.",
            
            # neg テスト
            "I do not like coffee.",
            "She never goes to parties.",
            "There is no time left.",
            
            # nummod テスト
            "I have three books on the table.",
            "This is my first time here.",
            "The car costs 20000 dollars."
        ]

def main():
    print("🚀 spaCy完全対応Rephraseエンジン拡張 - フェーズ1開始")
    
    # 拡張システム初期化
    extension = SpacyRephraseExtension()
    
    # 拡張ルール生成
    enhanced_rules = extension.create_enhanced_rules_file()
    
    # テスト用例文生成
    test_sentences = extension.generate_test_sentences()
    
    print(f"\n📝 フェーズ1テスト用例文 ({len(test_sentences)}個):")
    for i, sentence in enumerate(test_sentences, 1):
        print(f"  {i:2d}. {sentence}")
    
    print(f"\n🎯 フェーズ1対象依存関係:")
    for dep, info in extension.dependency_mapping.items():
        print(f"  - {dep}: {info['description']}")
    
    print(f"\n✅ フェーズ1準備完了！次は実装とテストです。")

if __name__ == "__main__":
    main()
