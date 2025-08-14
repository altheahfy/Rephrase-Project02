"""
Noun Clause検出問題をデバッグ
"what you think" がなぜ relative_pattern として検出されるかを分析
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_noun_clause():
    """Noun Clause検出問題の詳細デバッグ"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    sentence = "Please tell me what you think about this idea."
    print("🔍 Debugging Noun Clause Detection")
    print("=" * 50)
    print(f"Sentence: {sentence}")
    print()
    
    result = detector.detect_hierarchical_grammar(sentence)
    
    # 詳細なクラス情報を確認
    for i, clause in enumerate(result.subordinate_clauses):
        print(f"Clause {i+1}:")
        print(f"  Text: '{clause.text}'")
        print(f"  Clause type: {clause.clause_type}")
        print(f"  Root word: '{clause.root_word}' (POS: {clause.root_pos})")
        print(f"  Detected pattern: {clause.grammatical_pattern.value}")
        print(f"  Confidence: {clause.confidence}")
        print(f"  Features: {clause.linguistic_features}")
        print()
        
        # パターン判定の詳細確認
        print(f"  🔍 Pattern Analysis:")
        
        # Relative pattern rules check
        print(f"    Relative pattern conditions:")
        print(f"    - clause_type in ['relative_clause', 'adnominal_clause']: {clause.clause_type in ['relative_clause', 'adnominal_clause']}")
        print(f"    - wh-words present: {any(word in clause.text.lower() for word in ['which', 'that', 'who', 'whom', 'whose', 'where', 'when', 'what'])}")
        
        # Noun clause rules check  
        print(f"    Noun clause conditions:")
        print(f"    - clause_type in ['clausal_complement', 'clausal_subject']: {clause.clause_type in ['clausal_complement', 'clausal_subject']}")
        print(f"    - wh-words present: {any(word in clause.text.lower() for word in ['what', 'who', 'which', 'where', 'when', 'how', 'why', 'that', 'if', 'whether'])}")
        
        # Context analysis
        print(f"    Context analysis:")
        print(f"    - Full sentence: '{sentence}'")
        print(f"    - Clause position in sentence: {sentence.find(clause.text[:10])}")
        print(f"    - Follows mental verb pattern: {'tell' in sentence.lower()}")
        
        print("=" * 50)
    
    print("\n🎯 Issue Analysis:")
    print("1. Clause type might be incorrectly classified")
    print("2. Pattern priority might favor relative over noun clause")
    print("3. Context requirements might not be matching")

if __name__ == "__main__":
    debug_noun_clause()
