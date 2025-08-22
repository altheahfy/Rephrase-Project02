#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
純粋人間文法認識システムテスト
===============================

Stanzaを完全に排除し、人間文法認識のみでスロット分割を実行するテスト

目的:
1. 人間文法認識だけでどこまで正解できるかを測定
2. Stanzaに一切依存せずに動作することを証明
3. 人間文法認識の純粋な性能評価

制約:
- Stanza pipeline使用禁止
- 依存関係解析使用禁止
- 純粋な正規表現＋ルールベースのみ
"""

import json
import re
from typing import Dict, List, Any, Tuple

class PureHumanGrammarSystem:
    """純粋人間文法認識システム（Stanza完全排除）"""
    
    def __init__(self):
        # 人間文法認識ルール定義
        self.grammar_rules = {
            'svc_patterns': [
                r'^(.*?)\s+(is|are|was|were)\s+(.*?)\.?$',  # S + be動詞 + C
            ],
            'svo_patterns': [
                r'^(.*?)\s+(.*?)\s+(.*?)\.?$',  # 基本SVO
            ],
            'svoo_patterns': [
                r'^(.*?)\s+(give|gave|send|sent|tell|told)\s+(.*?)\s+(.*?)\.?$',  # 典型的第4文型
            ],
            'passive_patterns': [
                r'^(.*?)\s+(was|were)\s+(.*?ed|.*?en)\s+by\s+(.*?)\.?$',  # 受動態 + by
                r'^(.*?)\s+(was|were)\s+(.*?ed|.*?en)\.?$',  # 受動態（by句なし）
            ],
            'perfect_patterns': [
                r'^(.*?)\s+(has|have|had)\s+(.*?ed|.*?en)\s+(.*?)\.?$',  # 完了形 + 目的語
            ],
            'adverb_patterns': [
                r'^(.*?)\s+(.*?)\s+(.*?ly)\.?$',  # 副詞(-ly)
            ]
        }
    
    def process_sentence_pure_human(self, sentence: str) -> Dict:
        """純粋人間文法認識でスロット分割"""
        result = {
            'sentence': sentence,
            'slots': {},
            'sub_slots': {},
            'recognition_method': 'pure_human_grammar',
            'patterns_used': []
        }
        
        # パターンマッチング順序（優先度順）
        
        # 1. 受動態パターン
        passive_result = self._detect_passive_pattern(sentence)
        if passive_result['detected']:
            result['slots'] = passive_result['slots']
            result['patterns_used'].append('passive_voice')
            return result
        
        # 2. 完了形パターン
        perfect_result = self._detect_perfect_pattern(sentence)
        if perfect_result['detected']:
            result['slots'] = perfect_result['slots']
            result['patterns_used'].append('perfect_tense')
            return result
            
        # 3. SVOO パターン（第4文型）
        svoo_result = self._detect_svoo_pattern(sentence)
        if svoo_result['detected']:
            result['slots'] = svoo_result['slots']
            result['patterns_used'].append('svoo_pattern')
            return result
        
        # 4. SVC パターン
        svc_result = self._detect_svc_pattern(sentence)
        if svc_result['detected']:
            result['slots'] = svc_result['slots']
            result['patterns_used'].append('svc_pattern')
            return result
        
        # 5. 副詞パターン
        adverb_result = self._detect_adverb_pattern(sentence)
        if adverb_result['detected']:
            result['slots'] = adverb_result['slots']
            result['patterns_used'].append('adverb_pattern')
            return result
        
        # 6. 基本SVO（最後の手段）
        svo_result = self._detect_basic_svo_pattern(sentence)
        result['slots'] = svo_result['slots']
        result['patterns_used'].append('basic_svo')
        
        return result
    
    def _detect_passive_pattern(self, sentence: str) -> Dict:
        """受動態パターン検出"""
        # パターン1: S + was/were + Vpp + by + Agent
        pattern1 = r'^(.*?)\s+(was|were)\s+(.*?)\s+by\s+(.*?)\.?$'
        match = re.match(pattern1, sentence, re.IGNORECASE)
        if match:
            subject, aux, verb, agent = match.groups()
            return {
                'detected': True,
                'slots': {
                    'S': subject.strip(),
                    'Aux': aux.strip(),
                    'V': verb.strip(),
                    'M1': f"by {agent.strip()}"
                }
            }
        
        # パターン2: S + was/were + Vpp
        pattern2 = r'^(.*?)\s+(was|were)\s+(.*?)\.?$'
        match = re.match(pattern2, sentence, re.IGNORECASE)
        if match:
            subject, aux, verb = match.groups()
            return {
                'detected': True,
                'slots': {
                    'S': subject.strip(),
                    'Aux': aux.strip(),
                    'V': verb.strip()
                }
            }
        
        return {'detected': False, 'slots': {}}
    
    def _detect_perfect_pattern(self, sentence: str) -> Dict:
        """完了形パターン検出"""
        pattern = r'^(.*?)\s+(has|have|had)\s+(.*?)\s+(.*?)\.?$'
        match = re.match(pattern, sentence, re.IGNORECASE)
        if match:
            subject, aux, verb, object_part = match.groups()
            return {
                'detected': True,
                'slots': {
                    'S': subject.strip(),
                    'Aux': aux.strip(),
                    'V': verb.strip(),
                    'O1': object_part.strip()
                }
            }
        return {'detected': False, 'slots': {}}
    
    def _detect_svoo_pattern(self, sentence: str) -> Dict:
        """SVOO（第4文型）パターン検出"""
        pattern = r'^(.*?)\s+(give|gave|send|sent|tell|told)\s+(.*?)\s+(.*?)\.?$'
        match = re.match(pattern, sentence, re.IGNORECASE)
        if match:
            subject, verb, obj1, obj2 = match.groups()
            return {
                'detected': True,
                'slots': {
                    'S': subject.strip(),
                    'V': verb.strip(),
                    'O1': obj1.strip(),
                    'O2': obj2.strip()
                }
            }
        return {'detected': False, 'slots': {}}
    
    def _detect_svc_pattern(self, sentence: str) -> Dict:
        """SVC パターン検出"""
        pattern = r'^(.*?)\s+(is|are|was|were)\s+(.*?)\.?$'
        match = re.match(pattern, sentence, re.IGNORECASE)
        if match:
            subject, verb, complement = match.groups()
            return {
                'detected': True,
                'slots': {
                    'S': subject.strip(),
                    'V': verb.strip(),
                    'C1': complement.strip()
                }
            }
        return {'detected': False, 'slots': {}}
    
    def _detect_adverb_pattern(self, sentence: str) -> Dict:
        """副詞パターン検出"""
        pattern = r'^(.*?)\s+(.*?)\s+(.*?ly)\.?$'
        match = re.match(pattern, sentence, re.IGNORECASE)
        if match:
            subject, verb, adverb = match.groups()
            return {
                'detected': True,
                'slots': {
                    'S': subject.strip(),
                    'V': verb.strip(),
                    'M2': adverb.strip()
                }
            }
        return {'detected': False, 'slots': {}}
    
    def _detect_basic_svo_pattern(self, sentence: str) -> Dict:
        """基本SVO パターン検出（最後の手段）"""
        # 単純な3分割
        words = sentence.replace('.', '').split()
        if len(words) >= 2:
            return {
                'detected': True,
                'slots': {
                    'S': words[0],
                    'V': words[1],
                    'O1': ' '.join(words[2:]) if len(words) > 2 else ''
                }
            }
        return {'detected': False, 'slots': {}}

class PureHumanGrammarTester:
    """純粋人間文法認識テスター"""
    
    def __init__(self):
        self.system = PureHumanGrammarSystem()
        self.stats = {
            'total_tests': 0,
            'perfect_matches': 0,
            'main_slot_matches': 0,
            'errors': []
        }
    
    def load_test_data(self, filename: str = "my_test_sentences.json") -> Dict:
        """テストデータ読み込み"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ テストファイル {filename} が見つかりません")
            return {"data": {}}
    
    def normalize_slots(self, data: Any) -> Dict:
        """スロットデータ正規化"""
        if isinstance(data, dict):
            if "main_slots" in data:
                return data["main_slots"]
            elif "slots" in data:
                return data["slots"]
            else:
                return data
        return {}
    
    def compare_slots(self, actual: Dict, expected: Dict) -> Tuple[bool, float, List]:
        """スロット比較"""
        if not expected:
            return len(actual) == 0, 1.0 if len(actual) == 0 else 0.0, []
        
        total_expected = len(expected)
        matches = 0
        differences = []
        
        for key, expected_value in expected.items():
            actual_value = actual.get(key, "")
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
        
        # 余分なスロットチェック
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
    
    def run_pure_human_test(self) -> Dict:
        """純粋人間文法認識テスト実行"""
        print("🧠 純粋人間文法認識テスト開始（Stanza完全排除）")
        print("=" * 60)
        
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
                # 純粋人間文法認識実行
                result = self.system.process_sentence_pure_human(sentence)
                
                # 結果正規化
                actual_slots = self.normalize_slots(result)
                expected_slots = self.normalize_slots(expected)
                
                # 比較
                perfect, accuracy, differences = self.compare_slots(actual_slots, expected_slots)
                
                # 統計更新
                if perfect:
                    self.stats['perfect_matches'] += 1
                    self.stats['main_slot_matches'] += 1
                
                # 結果表示
                print(f"🧠 純粋人間文法認識結果: {result}")
                print(f"🎯 期待値: {expected}")
                print(f"📊 一致: {'✅' if perfect else '❌'}")
                print(f"📊 精度: {accuracy:.2%}")
                print(f"🔍 使用パターン: {result.get('patterns_used', [])}")
                
                # 差分表示
                if differences:
                    print("❌ 差分:")
                    for diff in differences:
                        print(f"   {diff['slot']}: 期待='{diff['expected']}' 実際='{diff['actual']}'")
                
            except Exception as e:
                error_msg = f"テスト {test_id} でエラー: {str(e)}"
                print(f"❌ {error_msg}")
                self.stats['errors'].append(error_msg)
        
        # 最終統計
        self._print_final_statistics()
        return self.stats
    
    def _print_final_statistics(self):
        """最終統計表示"""
        print("\n" + "=" * 60)
        print("📊 純粋人間文法認識 最終統計")
        print("=" * 60)
        
        total = self.stats['total_tests']
        if total == 0:
            print("❌ テストが実行されませんでした")
            return
        
        perfect_rate = self.stats['perfect_matches'] / total * 100
        
        print(f"🧠 純粋人間文法認識正解率: {perfect_rate:.1f}% ({self.stats['perfect_matches']}/{total})")
        print("🚫 Stanza使用: 0% (完全排除)")
        print("✅ 独立性: 100% (外部依存なし)")
        
        if self.stats['errors']:
            print(f"❌ エラー数: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"   - {error}")
        
        # 評価
        print("\n🎖️ 純粋人間文法認識評価:")
        if perfect_rate >= 80:
            print("🥇 優秀: 人間文法認識だけで高精度達成")
        elif perfect_rate >= 60:
            print("🥈 良好: 人間文法認識の基本機能確認")
        elif perfect_rate >= 40:
            print("🥉 合格: 人間文法認識の部分的動作確認")
        else:
            print("❌ 要改善: 人間文法認識ルールの見直しが必要")

if __name__ == "__main__":
    tester = PureHumanGrammarTester()
    tester.run_pure_human_test()
