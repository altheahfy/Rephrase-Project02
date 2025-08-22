#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立した人間文法認識システムテスト
Stanzaに依存せず、純粋に人間文法認識の動作を検証

目的:
1. 人間文法認識が実際に動作しているかを確認
2. Stanzaフォールバックに隠れていないかを検証
3. 具体的な修正結果を可視化
"""

import json
import re
from typing import Dict, List, Any
import logging

class HumanGrammarRecognitionTest:
    """人間文法認識システム独立テスト"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        
    def test_relative_clause_patterns(self, sentence: str) -> Dict:
        """関係節パターン検出テスト"""
        results = {
            'sentence': sentence,
            'patterns_detected': [],
            'confidence_scores': [],
            'modifications': []
        }
        
        sentence_lower = sentence.lower()
        
        # パターン1: whose + 所有構造
        if 'whose' in sentence_lower:
            pattern = self._test_possessive_relative_pattern(sentence_lower)
            if pattern['found']:
                results['patterns_detected'].append('possessive_relative')
                results['confidence_scores'].append(pattern['confidence'])
                results['modifications'].append(pattern)
        
        # パターン2: who/which/that + 動詞構造
        if any(word in sentence_lower for word in ['who', 'which', 'that']):
            pattern = self._test_standard_relative_pattern(sentence_lower)
            if pattern['found']:
                results['patterns_detected'].append('standard_relative')
                results['confidence_scores'].append(pattern['confidence'])
                results['modifications'].append(pattern)
        
        return results
    
    def _test_possessive_relative_pattern(self, sentence_lower: str) -> Dict:
        """所有格関係代名詞パターン検出（独立）"""
        pattern_result = {'found': False, 'type': 'possessive_relative', 'confidence': 0.0}
        
        # パターン: [先行詞] whose [所有される名詞] + [動詞/形容詞]
        patterns = [
            r'(\w+)\s+whose\s+(\w+)\s+(is|are|was|were)\s+(\w+)',  # whose + be動詞
            r'(\w+)\s+whose\s+(\w+)\s+(\w+)',  # whose + 一般動詞
        ]
        
        for pattern in patterns:
            match = re.search(pattern, sentence_lower)
            if match:
                groups = match.groups()
                pattern_result.update({
                    'found': True,
                    'antecedent': groups[0],
                    'possessed_noun': groups[1],
                    'human_interpretation': f"Human recognizes: '{groups[0]}' owns '{groups[1]}'",
                    'confidence': 0.95
                })
                break
        
        return pattern_result
    
    def _test_standard_relative_pattern(self, sentence_lower: str) -> Dict:
        """標準的関係代名詞パターン検出（独立）"""
        pattern_result = {'found': False, 'type': 'standard_relative', 'confidence': 0.0}
        
        patterns = [
            r'(\w+)\s+(who|which|that)\s+(\w+)',  # 基本パターン
            r'(\w+)\s*,\s*(who|which)\s+(\w+)',   # コンマ区切り
        ]
        
        for pattern in patterns:
            match = re.search(pattern, sentence_lower)
            if match:
                antecedent_text, rel_pronoun_text, verb_text = match.groups()
                pattern_result.update({
                    'found': True,
                    'antecedent': antecedent_text,
                    'relative_pronoun': rel_pronoun_text,
                    'relative_verb': verb_text,
                    'human_interpretation': f"Human recognizes: '{antecedent_text}' is modified by relative clause",
                    'confidence': 0.9
                })
                break
        
        return pattern_result
    
    def test_conjunction_patterns(self, sentence: str) -> Dict:
        """接続詞パターン検出テスト（独立）"""
        results = {
            'sentence': sentence,
            'patterns_detected': [],
            'modifications': []
        }
        
        sentence_lower = sentence.lower()
        
        # 複合接続詞パターンの検出
        conjunction_patterns = [
            r'\bas\s+if\b',       # "as if" 
            r'\beven\s+if\b',     # "even if"
            r'\bas\s+though\b',   # "as though"
            r'\bwhile\b',         # "while"
            r'\bbecause\b',       # "because"
        ]
        
        for pattern in conjunction_patterns:
            matches = re.finditer(pattern, sentence_lower)
            for match in matches:
                conjunction_text = match.group().strip()
                results['patterns_detected'].append(conjunction_text)
                results['modifications'].append({
                    'type': 'compound_conjunction' if ' ' in conjunction_text else 'subordinating_conjunction',
                    'text': conjunction_text,
                    'human_interpretation': f"Human recognizes: '{conjunction_text}' introduces subordinate clause",
                    'confidence': 0.95 if ' ' in conjunction_text else 0.90
                })
        
        return results
    
    def test_passive_voice_patterns(self, sentence: str) -> Dict:
        """受動態パターン検出テスト（独立）"""
        results = {
            'sentence': sentence,
            'patterns_detected': [],
            'modifications': []
        }
        
        # be動詞 + 過去分詞パターン
        be_verbs = ['is', 'are', 'was', 'were', 'be', 'been', 'being']
        words = sentence.lower().split()
        
        for i in range(len(words) - 1):
            if words[i] in be_verbs:
                next_word = words[i + 1]
                
                # 簡単な過去分詞判定（語尾ベース）
                if (next_word.endswith('ed') or 
                    next_word.endswith('en') or 
                    next_word in ['done', 'seen', 'taken', 'given', 'written', 'spoken']):
                    
                    results['patterns_detected'].append('passive_voice')
                    results['modifications'].append({
                        'type': 'passive_voice',
                        'be_verb': words[i],
                        'past_participle': next_word,
                        'human_interpretation': f"Human recognizes: '{words[i]} {next_word}' is passive voice",
                        'confidence': 0.85
                    })
        
        return results

def run_isolated_tests():
    """独立テストの実行"""
    tester = HumanGrammarRecognitionTest()
    
    # テスト用文章
    test_sentences = [
        "The car whose owner is rich lives here.",
        "The woman who works here is my friend.",
        "The book that I read was interesting.",
        "He looks as if he is tired.",
        "The document was reviewed thoroughly.",
        "Children were playing happily.",
    ]
    
    print("🧠 独立した人間文法認識システムテスト開始")
    print("=" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 テスト {i}: {sentence}")
        print("-" * 40)
        
        # 関係節テスト
        rel_results = tester.test_relative_clause_patterns(sentence)
        if rel_results['patterns_detected']:
            print(f"✅ 関係節検出: {rel_results['patterns_detected']}")
            for mod in rel_results['modifications']:
                print(f"   → {mod.get('human_interpretation', 'Unknown')}")
        
        # 接続詞テスト
        conj_results = tester.test_conjunction_patterns(sentence)
        if conj_results['patterns_detected']:
            print(f"✅ 接続詞検出: {conj_results['patterns_detected']}")
            for mod in conj_results['modifications']:
                print(f"   → {mod.get('human_interpretation', 'Unknown')}")
        
        # 受動態テスト
        pass_results = tester.test_passive_voice_patterns(sentence)
        if pass_results['patterns_detected']:
            print(f"✅ 受動態検出: {pass_results['patterns_detected']}")
            for mod in pass_results['modifications']:
                print(f"   → {mod.get('human_interpretation', 'Unknown')}")
        
        if (not rel_results['patterns_detected'] and 
            not conj_results['patterns_detected'] and 
            not pass_results['patterns_detected']):
            print("❌ パターン検出なし")
    
    print("\n" + "=" * 60)
    print("🏁 独立テスト完了")

if __name__ == "__main__":
    run_isolated_tests()
