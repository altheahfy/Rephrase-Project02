#!/usr/bin/env python3
"""V5の修正をテストするスクリプト"""

from hierarchical_grammar_detector_v5 import HierarchicalGrammarDetectorV5

def test_v5_fix():
    detector = HierarchicalGrammarDetectorV5()
    
    # テスト文
    test_sentence = "I think that he is smart."
    
    print(f"🧪 Testing V5 Fix: {test_sentence}")
    print("=" * 50)
    
    try:
        result = detector.detect_hierarchical_grammar_v5(test_sentence)
        print(f"✅ SUCCESS: V5 processing completed")
        print(f"📋 Main result pattern: {result.main_result.main_clause.grammatical_pattern.value}")
        print(f"📊 Number of subordinate results: {len(result.subordinate_results)}")
        
        if result.subordinate_results:
            for i, sub in enumerate(result.subordinate_results):
                if 'result' in sub:
                    print(f"  📎 Sub result {i+1}: {sub['result'].main_clause.grammatical_pattern.value}")
                else:
                    print(f"  📎 Sub result {i+1}: {sub}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_v5_fix()
    exit(0 if success else 1)
