"""
Dependency Analysis Debug Tool
依存関係の詳細分析でパターン検出の問題を特定
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_dependency_analysis():
    """依存関係を詳細分析してパターン検出の問題を特定"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    test_sentences = [
        "She is a teacher.",
        "The book is very good.", 
        "The cat sleeps.",
        "Please tell me."
    ]
    
    print("🔍 Dependency Analysis Debug")
    print("=" * 50)
    
    for sentence in test_sentences:
        print(f"\n📝 Sentence: \"{sentence}\"")
        print("-" * 40)
        
        # Get Stanza analysis
        stanza_analysis = detector._analyze_with_stanza(sentence)
        dependencies = stanza_analysis.get('dependencies', [])
        pos_tags = dict(stanza_analysis.get('pos_tags', []))
        lemmas = dict(stanza_analysis.get('lemmas', []))
        
        print("📊 Dependencies:")
        for dep in dependencies:
            print(f"   {dep.head} --{dep.relation}-> {dep.dependent}")
            
        print("🏷️ POS Tags:")
        for word, pos in pos_tags.items():
            lemma = lemmas.get(word, word)
            print(f"   {word} ({lemma}): {pos}")
        
        # Get clause decomposition
        clauses = detector._decompose_into_clauses_v4(stanza_analysis, sentence)
        
        print("🏗️ Clause Analysis:")
        for clause in clauses:
            print(f"   Type: {clause.clause_type}")
            print(f"   Root: {clause.root_word} ({clause.root_pos}, {clause.root_lemma})")
            print(f"   Text: {clause.text}")
            print(f"   Subjects: {clause.subjects}")
            print(f"   Objects: {clause.objects}")
            print(f"   Complements: {clause.complements}")
            print(f"   Is Linking: {clause.is_linking_verb()}")
            print(f"   Has Subject: {clause.has_subject()}")
            print(f"   Has Object: {clause.has_object()}")
            print(f"   Has Complement: {clause.has_complement()}")

if __name__ == "__main__":
    debug_dependency_analysis()
