"""
特定パターンの検出改善を行う
特に gerund_pattern と noun_clause の精度向上
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def analyze_specific_failures():
    """失敗しているパターンを詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    print("🔍 Specific Pattern Failure Analysis")
    print("=" * 50)
    
    # Case 3: by encouraging him constantly (gerund_pattern期待)
    print("\n📝 Case 3 Analysis:")
    sentence = "She made him happy by encouraging him constantly."
    result = detector.detect_hierarchical_grammar(sentence)
    
    print(f"Sentence: {sentence}")
    print(f"Expected: gerund_pattern (by encouraging)")
    print(f"Detected: {[clause.grammatical_pattern.value for clause in result.subordinate_clauses]}")
    
    # 詳細分析
    print("\n🔍 Detailed Analysis:")
    print(f"Main clause pattern: {result.main_clause.grammatical_pattern.value}")
    print(f"Main clause confidence: {result.main_clause.confidence}")
    
    for i, clause in enumerate(result.subordinate_clauses):
        print(f"Subordinate {i+1}: {clause.grammatical_pattern.value} (conf: {clause.confidence})")
        print(f"  Text: '{clause.text}'")
        print(f"  Root: '{clause.root_word}' ({clause.root_pos})")
        print(f"  Subjects: {clause.subjects}, Objects: {clause.objects}")
    
    # Case 4: what you think (noun_clause期待) 
    print("\n" + "=" * 50)
    print("\n📝 Case 4 Analysis:")
    sentence = "Please tell me what you think about this idea."
    result = detector.detect_hierarchical_grammar(sentence)
    
    print(f"Sentence: {sentence}")
    print(f"Expected: imperative_pattern + noun_clause (what you think)")
    print(f"Detected main: {result.main_clause.grammatical_pattern.value}")
    print(f"Detected sub: {[clause.grammatical_pattern.value for clause in result.subordinate_clauses]}")
    
    # 詳細分析
    print("\n🔍 Detailed Analysis:")
    for i, clause in enumerate(result.subordinate_clauses):
        print(f"Subordinate {i+1}: {clause.grammatical_pattern.value} (conf: {clause.confidence})")
        print(f"  Text: '{clause.text}'")
        print(f"  Root: '{clause.root_word}' ({clause.root_pos})")
        print(f"  Subjects: {clause.subjects}, Objects: {clause.objects}")
    
    print("\n🎯 Issues Identified:")
    print("1. 'by encouraging' not detected as gerund_pattern")
    print("2. 'what you think' detected as relative_pattern instead of noun_clause") 
    print("3. Main clause (imperative) not being properly separated from subordinate")

if __name__ == "__main__":
    analyze_specific_failures()
