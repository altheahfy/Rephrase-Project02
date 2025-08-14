"""
"She made him happy." の不要な従属節検出問題分析
なぜ imperative_pattern が従属節として検出されるかを調査
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_she_made_him_happy():
    """She made him happy構文の不要従属節検出問題を詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    sentence = "She made him happy."
    
    print(f"🔍 Analyzing: \"{sentence}\"")
    print("=" * 50)
    
    # 完全な分析結果を取得
    result = detector.detect_grammar_pattern(sentence)
    
    print("🏗️ Full Detection Result:")
    print(f"   Primary Pattern: {result.primary_pattern}")
    print(f"   Confidence: {result.confidence:.3f}")
    print(f"   Secondary Patterns: {result.secondary_patterns}")
    
    # Stanza解析の詳細取得
    stanza_analysis = detector._analyze_with_stanza(sentence)
    dependencies = stanza_analysis.get('dependencies', [])
    pos_tags = dict(stanza_analysis.get('pos_tags', []))
    
    print("\n📊 All Dependencies:")
    for dep in dependencies:
        print(f"   {dep.head} --{dep.relation}-> {dep.dependent}")
        head_pos = pos_tags.get(dep.head, 'N/A')
        dep_pos = pos_tags.get(dep.dependent, 'N/A')
        print(f"      {dep.head}({head_pos}) → {dep.dependent}({dep_pos})")
    
    print("\n🏗️ Clause Decomposition:")
    clauses = detector._decompose_into_clauses_v4(stanza_analysis, sentence)
    
    print(f"   Total Clauses: {len(clauses)}")
    print(f"   Expected: 1 (main clause only)")
    
    for i, clause in enumerate(clauses, 1):
        print(f"\n   Clause {i}:")
        print(f"      Type: {clause.clause_type}")
        print(f"      Root: {clause.root_word} ({clause.root_pos})")
        print(f"      Text: \"{clause.text}\"")
        print(f"      Subjects: {clause.subjects}")
        print(f"      Objects: {clause.objects}")
        
        # パターン分析
        pattern_result = detector._analyze_clause_pattern_v4(clause, stanza_analysis, sentence)
        print(f"      Pattern: {pattern_result['pattern']}")
        print(f"      Confidence: {pattern_result['confidence']:.3f}")
        
        if clause.clause_type != 'main':
            print(f"      *** UNEXPECTED SUBORDINATE CLAUSE ***")
            print(f"      This clause should not exist in simple 'She made him happy' sentence")

if __name__ == "__main__":
    debug_she_made_him_happy()
