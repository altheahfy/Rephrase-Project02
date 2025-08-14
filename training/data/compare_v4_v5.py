#!/usr/bin/env python3
"""V4とV5の比較テスト"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
from hierarchical_grammar_detector_v5 import HierarchicalGrammarDetectorV5

def compare_v4_v5():
    detector_v4 = HierarchicalGrammarDetectorV4()
    detector_v5 = HierarchicalGrammarDetectorV5()
    
    test_cases = [
        "I think that he is smart.",
        "Being a teacher, she knows students well.",
        "The book that I read yesterday was interesting.",
        "She said that she would come.",
        "I believe he is right."
    ]
    
    print("🔍 V4 vs V5 Comparison Test")
    print("=" * 60)
    
    for test_sentence in test_cases:
        print(f"\n📝 Test: \"{test_sentence}\"")
        print("-" * 40)
        
        # V4テスト
        try:
            v4_result = detector_v4.detect_hierarchical_grammar(test_sentence)
            v4_pattern = v4_result.main_clause.grammatical_pattern.value if v4_result.main_clause else "Unknown"
            print(f"🔵 V4 Result: {v4_pattern}")
        except Exception as e:
            print(f"🔵 V4 Error: {e}")
        
        # V5テスト
        try:
            v5_result = detector_v5.detect_hierarchical_grammar_v5(test_sentence)
            v5_main = v5_result.main_result.main_clause.grammatical_pattern.value if v5_result.main_result.main_clause else "Unknown"
            v5_subs = [sub['result'].main_clause.grammatical_pattern.value for sub in v5_result.subordinate_results if 'result' in sub and sub['result'].main_clause]
            print(f"🔴 V5 Main: {v5_main}")
            if v5_subs:
                print(f"🔴 V5 Subs: {', '.join(v5_subs)}")
        except Exception as e:
            print(f"🔴 V5 Error: {e}")

if __name__ == "__main__":
    compare_v4_v5()
