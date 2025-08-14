#!/usr/bin/env python3
"""V4の実際のメソッドを確認"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def check_v4_methods():
    detector = HierarchicalGrammarDetectorV4()
    
    print("🔍 V4 Available Methods:")
    methods = [method for method in dir(detector) if callable(getattr(detector, method)) and not method.startswith('_')]
    
    for method in methods:
        print(f"  ✅ {method}")
    
    # 実際のメソッドをテスト
    test_sentence = "I think something."
    try:
        result = detector.detect_hierarchical_grammar(test_sentence)
        print(f"\n🎯 detect_hierarchical_grammar works: {result.main_clause.grammatical_pattern.value if result.main_clause else 'None'}")
    except Exception as e:
        print(f"\n❌ detect_hierarchical_grammar failed: {e}")

if __name__ == "__main__":
    check_v4_methods()
