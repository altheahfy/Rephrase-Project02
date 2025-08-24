#!/usr/bin/env python3
"""
シンプル副詞テスト - Unicode問題なし版
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_grammar_mapper import DynamicGrammarMapper

def test_simple_sentence():
    """シンプルな文のテスト"""
    
    analyzer = DynamicGrammarMapper()
    
    test_sentence = "She quickly runs to school."
    print(f"テスト文: {test_sentence}")
    
    result = analyzer.analyze_sentence(test_sentence)
    
    print(f"main_slots: {result.get('main_slots', {})}")
    print(f"sub_slots: {result.get('sub_slots', {})}")
    
    # 期待値との比較
    expected_main = {'S': 'She', 'M1': 'quickly', 'V': 'runs', 'M2': 'to school'}
    actual_main = result.get('main_slots', {})
    
    print(f"期待: {expected_main}")
    print(f"実際: {actual_main}")
    
    # 副詞配置のチェック
    m1_match = actual_main.get('M1') == expected_main.get('M1')
    m2_match = actual_main.get('M2') == expected_main.get('M2')
    
    print(f"M1正解: {m1_match} (期待: {expected_main.get('M1')}, 実際: {actual_main.get('M1')})")
    print(f"M2正解: {m2_match} (期待: {expected_main.get('M2')}, 実際: {actual_main.get('M2')})")
    
    return m1_match and m2_match

if __name__ == "__main__":
    print("=== シンプル副詞テスト ===")
    result = test_simple_sentence()
    print(f"結果: {'成功' if result else '失敗'}")
