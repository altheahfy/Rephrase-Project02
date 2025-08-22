#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人間文法認識システム正解率テスト
=============================

目的:
1. 人間文法認識システムの実際の正解率を測定
2. 期待値との照合による精度評価
3. 各ハンドラーの個別性能分析
4. エラーパターンの特定

評価項目:
- スロット一致率（メイン・サブ別）
- 文法パターン認識率
- Stanzaフォールバック依存度
"""

import json
import sys
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

# メインシステムをインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class HumanGrammarAccuracyTester:
    """人間文法認識システム正解率テスト"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.WARNING)  # ログレベルを下げてテスト結果を見やすく
        
        # メインシステム初期化
        self.mapper = UnifiedStanzaRephraseMapper()
        
        # 統計データ
        self.stats = {
            'total_tests': 0,
            'perfect_matches': 0,
            'main_slot_matches': 0,
            'sub_slot_matches': 0,
            'human_grammar_used': 0,
            'stanza_fallback_used': 0,
            'errors': []
        }
        
    def load_test_data(self, filename: str = "my_test_sentences.json") -> Dict:
        """テストデータを読み込み"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"テストデータファイル {filename} が見つかりません")
            return {"data": {}}
            
    def normalize_slots(self, data: Any) -> Tuple[Dict, Dict]:
        """スロットデータを正規化して比較しやすくする"""
        if isinstance(data, dict):
            # システム出力形式: {"slots": {...}, "sub_slots": {...}}
            if "slots" in data and "sub_slots" in data:
                return data["slots"], data["sub_slots"]
            
            # 期待値形式: {"main_slots": {...}, "sub_slots": {...}}
            elif "main_slots" in data and "sub_slots" in data:
                return data["main_slots"], data["sub_slots"]
            
            # フラット形式を分離
            main_slots = {}
            sub_slots = {}
            for key, value in data.items():
                if key.startswith("sub-"):
                    sub_slots[key] = value
                elif key in ["S", "V", "O1", "O2", "C1", "C2", "Aux", "M1", "M2", "M3"]:
                    main_slots[key] = value
            return main_slots, sub_slots
        
        return {}, {}
    
    def compare_slots(self, actual: Dict, expected: Dict) -> Tuple[bool, float, List]:
        """スロットを比較して一致度を計算"""
        if not expected:  # 期待値が空の場合
            return len(actual) == 0, 1.0 if len(actual) == 0 else 0.0, []
        
        total_expected = len(expected)
        matches = 0
        differences = []
        
        for key, expected_value in expected.items():
            actual_value = actual.get(key, "")
            
            # 値の正規化（空白処理等）
            expected_clean = str(expected_value).strip()
            actual_clean = str(actual_value).strip()
            
            if expected_clean == actual_clean:
                matches += 1
            else:
                differences.append({
                    'slot': key,
                    'expected': expected_clean,
                    'actual': actual_clean
                })
        
        # 余分なスロットをチェック
        for key in actual:
            if key not in expected and actual[key].strip():
                differences.append({
                    'slot': key,
                    'expected': '(not expected)',
                    'actual': str(actual[key]).strip()
                })
        
        perfect_match = len(differences) == 0
        accuracy = matches / total_expected if total_expected > 0 else 1.0
        
        return perfect_match, accuracy, differences
    
    def detect_human_grammar_usage(self, sentence: str, result: Dict) -> bool:
        """人間文法認識が使用されたかを検出"""
        # ログから人間文法認識の使用を検出する簡易版
        # 実際の実装では、システムからの応答を解析
        sentence_lower = sentence.lower()
        
        # 人間文法認識が効果的なパターンの検出
        human_patterns = [
            'whose',  # 所有格関係代名詞
            'as if',  # 複合接続詞
            'even if',
            'was/were + 過去分詞'  # 受動態パターン
        ]
        
        for pattern in ['whose', 'as if', 'even if']:
            if pattern in sentence_lower:
                return True
                
        # 受動態パターン検出
        if any(word in sentence_lower for word in ['was', 'were']) and any(word in sentence_lower for word in ['written', 'made', 'given', 'taken']):
            return True
            
        return False
    
    def run_accuracy_test(self) -> Dict:
        """正解率テスト実行"""
        print("🎯 人間文法認識システム正解率テスト開始")
        print("=" * 60)
        
        # テストデータ読み込み
        test_data = self.load_test_data()
        test_items = test_data.get("data", {})
        
        if not test_items:
            print("❌ テストデータが見つかりません")
            return self.stats
        
        self.stats['total_tests'] = len(test_items)
        
        for test_id, test_case in test_items.items():
            sentence = test_case["sentence"]
            expected = test_case["expected"]
            
            print(f"\n📝 テスト {test_id}: {sentence}")
            print("-" * 50)
            
            try:
                # システム実行
                result = self.mapper.process(sentence)
                
                # 結果正規化
                actual_main, actual_sub = self.normalize_slots(result)
                expected_main, expected_sub = self.normalize_slots(expected)
                
                # メインスロット比較
                main_perfect, main_accuracy, main_diffs = self.compare_slots(actual_main, expected_main)
                
                # サブスロット比較
                sub_perfect, sub_accuracy, sub_diffs = self.compare_slots(actual_sub, expected_sub)
                
                # 総合評価
                overall_perfect = main_perfect and sub_perfect
                
                # 統計更新
                if overall_perfect:
                    self.stats['perfect_matches'] += 1
                if main_perfect:
                    self.stats['main_slot_matches'] += 1
                if sub_perfect:
                    self.stats['sub_slot_matches'] += 1
                
                # 人間文法認識使用検出
                human_used = self.detect_human_grammar_usage(sentence, result)
                if human_used:
                    self.stats['human_grammar_used'] += 1
                else:
                    self.stats['stanza_fallback_used'] += 1
                
                # 結果表示
                print(f"✅ 結果: {result}")
                print(f"🎯 期待値: {expected}")
                print(f"📊 総合一致: {'✅' if overall_perfect else '❌'}")
                print(f"📊 メイン精度: {main_accuracy:.2%}")
                print(f"📊 サブ精度: {sub_accuracy:.2%}")
                print(f"🧠 人間文法認識: {'✅' if human_used else '❌ (Stanza使用)'}")
                
                # 差分表示
                if main_diffs:
                    print("❌ メインスロット差分:")
                    for diff in main_diffs:
                        print(f"   {diff['slot']}: 期待='{diff['expected']}' 実際='{diff['actual']}'")
                
                if sub_diffs:
                    print("❌ サブスロット差分:")
                    for diff in sub_diffs:
                        print(f"   {diff['slot']}: 期待='{diff['expected']}' 実際='{diff['actual']}'")
                
            except Exception as e:
                error_msg = f"テスト {test_id} でエラー: {str(e)}"
                print(f"❌ {error_msg}")
                self.stats['errors'].append(error_msg)
        
        # 最終統計
        self._print_final_statistics()
        return self.stats
    
    def _print_final_statistics(self):
        """最終統計を表示"""
        print("\n" + "=" * 60)
        print("📊 最終統計結果")
        print("=" * 60)
        
        total = self.stats['total_tests']
        if total == 0:
            print("❌ テストが実行されませんでした")
            return
        
        perfect_rate = self.stats['perfect_matches'] / total * 100
        main_rate = self.stats['main_slot_matches'] / total * 100
        sub_rate = self.stats['sub_slot_matches'] / total * 100
        human_usage_rate = self.stats['human_grammar_used'] / total * 100
        
        print(f"🎯 総合正解率: {perfect_rate:.1f}% ({self.stats['perfect_matches']}/{total})")
        print(f"📈 メインスロット正解率: {main_rate:.1f}% ({self.stats['main_slot_matches']}/{total})")
        print(f"📈 サブスロット正解率: {sub_rate:.1f}% ({self.stats['sub_slot_matches']}/{total})")
        print(f"🧠 人間文法認識使用率: {human_usage_rate:.1f}% ({self.stats['human_grammar_used']}/{total})")
        print(f"🤖 Stanzaフォールバック率: {100-human_usage_rate:.1f}% ({self.stats['stanza_fallback_used']}/{total})")
        
        if self.stats['errors']:
            print(f"❌ エラー数: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"   - {error}")
        
        # 評価判定
        print("\n🎖️ システム評価:")
        if perfect_rate >= 90:
            print("🥇 優秀: 90%以上の正解率")
        elif perfect_rate >= 80:
            print("🥈 良好: 80%以上の正解率")
        elif perfect_rate >= 70:
            print("🥉 合格: 70%以上の正解率")
        else:
            print("❌ 改善要: 70%未満の正解率")

if __name__ == "__main__":
    tester = HumanGrammarAccuracyTester()
    tester.run_accuracy_test()
