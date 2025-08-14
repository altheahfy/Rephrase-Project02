"""
Gerund vs Participle 分類問題の分析
"Being a teacher" がなぜ gerund_pattern になるかを調査
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_gerund_vs_participle():
    """Gerund vs Participle分類問題を詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    test_cases = [
        ("Being a teacher, she knows students.", "Should be PARTICIPLE (describes she)"),
        ("Walking in the park, I saw birds.", "Should be PARTICIPLE (describes I)"),
        ("Having finished work, she went home.", "Should be PARTICIPLE (describes she)"),
    ]
    
    print("🔍 Analyzing Gerund vs Participle Classification")
    print("=" * 60)
    
    for sentence, expected in test_cases:
        print(f"\n📝 Sentence: \"{sentence}\"")
        print(f"📋 Expected: {expected}")
        print("-" * 50)
        
        # 詳細分析
        stanza_analysis = detector._analyze_with_stanza(sentence)
        clauses = detector._decompose_into_clauses_v4(stanza_analysis, sentence)
        
        # 従属節のパターンをチェック
        subordinate_clauses = [c for c in clauses if c.clause_type == 'adverbial_clause']
        
        if subordinate_clauses:
            clause = subordinate_clauses[0]
            pattern_result = detector._analyze_clause_pattern_v4(clause, stanza_analysis, sentence)
            
            print(f"🏗️ Subordinate clause:")
            print(f"   Root: {clause.root_word} ({clause.root_pos})")
            print(f"   Text: \"{clause.text}\"")
            print(f"   Pattern: {pattern_result['pattern']}")
            print(f"   Confidence: {pattern_result['confidence']:.3f}")
            
            # 動名詞 vs 分詞の条件チェック
            print(f"\n🔍 Classification Analysis:")
            print(f"   Root is VBG/ing-form: {clause.root_pos in ['VBG', 'VERB'] and (clause.root_word.endswith('ing') or clause.root_lemma.endswith('ing'))}")
            print(f"   Is AUX 'Being': {clause.root_pos == 'AUX' and clause.root_word.lower() == 'being'}")
            print(f"   Clause type: {clause.clause_type}")
            print(f"   Has subjects: {clause.has_subject()}")
            print(f"   Has objects: {clause.has_object()}")
            
            # GERUND vs PARTICIPLE のルール適用チェック
            gerund_rules = detector.pattern_detection_rules.get('gerund_pattern', {})
            participle_rules = detector.pattern_detection_rules.get('participle_pattern', {})
            
            print(f"\n📋 Rule Application:")
            if gerund_rules:
                gerund_confidence, gerund_features = detector._calculate_ultra_precise_score(
                    'gerund_pattern', clause, gerund_rules, sentence
                )
                print(f"   GERUND confidence: {gerund_confidence:.3f}")
                print(f"   GERUND features: {gerund_features}")
            
            if participle_rules:  
                # Need to get the actual GrammarPattern enum
                from advanced_grammar_detector import GrammarPattern
                participle_confidence, participle_features = detector._calculate_ultra_precise_score(
                    GrammarPattern.PARTICIPLE_PATTERN, clause, participle_rules, sentence
                )
                print(f"   PARTICIPLE confidence: {participle_confidence:.3f}")
                print(f"   PARTICIPLE features: {participle_features}")
        else:
            print("   No subordinate clauses found!")

if __name__ == "__main__":
    debug_gerund_vs_participle()
