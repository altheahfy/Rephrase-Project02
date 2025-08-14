"""
Subordinate Clause Detection Debug Tool
従属節検出の問題を詳細分析

現在の問題:
1. "Being a teacher" → gerund_pattern が検出されない
2. "Having finished" → participle_pattern が検出されない
3. 分詞構文と動名詞の区別が不正確
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_subordinate_clause_detection():
    """従属節検出の問題を詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # 問題のある従属節パターンに焦点
    test_sentences = [
        "Being a teacher, she knows how to explain.",
        "Having finished the work, she went home.", 
        "Walking in the park, I saw a bird.",
        "Excited about the news, he called his friend.",
        "Written by Shakespeare, the play is famous."
    ]
    
    print("🔍 Subordinate Clause Detection Debug")
    print("=" * 50)
    
    for sentence in test_sentences:
        print(f"\n📝 Sentence: \"{sentence}\"")
        print("=" * 40)
        
        # 詳細な依存関係分析
        stanza_analysis = detector._analyze_with_stanza(sentence)
        dependencies = stanza_analysis.get('dependencies', [])
        pos_tags = dict(stanza_analysis.get('pos_tags', []))
        lemmas = dict(stanza_analysis.get('lemmas', []))
        
        print("📊 Key Dependencies (adverbial clauses):")
        for dep in dependencies:
            if dep.relation in ['advcl', 'acl', 'acl:relcl', 'xcomp', 'ccomp']:
                print(f"   {dep.head} --{dep.relation}-> {dep.dependent}")
                print(f"      {dep.dependent}: {pos_tags.get(dep.dependent, 'N/A')} ({lemmas.get(dep.dependent, 'N/A')})")
        
        # 節の分解結果
        clauses = detector._decompose_into_clauses_v4(stanza_analysis, sentence)
        
        print(f"\n🏗️ Clause Decomposition ({len(clauses)} clauses):")
        for i, clause in enumerate(clauses, 1):
            print(f"   {i}. Type: {clause.clause_type}")
            print(f"      Root: {clause.root_word} ({clause.root_pos}, {clause.root_lemma})")
            print(f"      Text: {clause.text}")
            
            # パターン分析結果
            pattern_result = detector._analyze_clause_pattern_v4(clause, stanza_analysis, sentence)
            print(f"      Pattern: {pattern_result['pattern']}")
            print(f"      Confidence: {pattern_result['confidence']:.3f}")
            print(f"      Features: {pattern_result['features']}")
            
            # 特定パターンの詳細チェック
            print(f"      ---- Detailed Analysis ----")
            print(f"      Is linking: {clause.is_linking_verb()}")
            print(f"      Is copular: {clause.is_copular_construction()}")
            print(f"      Has subjects: {clause.has_subject()} ({clause.subjects})")
            print(f"      Has objects: {clause.has_object()} ({clause.objects})")
            print(f"      Has complements: {clause.has_complement()} ({clause.complements})")
            
            # 分詞構文・動名詞の特徴チェック
            is_vbg = clause.root_pos in ['VBG', 'VERB'] and clause.root_word.endswith('ing')
            is_vbn = clause.root_pos in ['VBN', 'VERB'] and (clause.root_word.endswith('ed') or clause.root_word.endswith('en'))
            is_advcl = clause.clause_type == 'adverbial_clause'
            
            print(f"      VBG (ing-form): {is_vbg}")
            print(f"      VBN (past participle): {is_vbn}")  
            print(f"      Adverbial clause: {is_advcl}")
            
            # 文の位置チェック (分詞構文は通常文頭)
            words = sentence.split()
            first_word = words[0] if words else ""
            is_sentence_initial = clause.root_word.lower() == first_word.lower()
            print(f"      Sentence initial: {is_sentence_initial}")

if __name__ == "__main__":
    debug_subordinate_clause_detection()
