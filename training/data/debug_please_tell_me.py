"""
"Please tell me" 命令文検出問題の詳細分析
なぜ IMPERATIVE_PATTERN として検出されないかを調査
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_please_tell_me():
    """Please tell me構文の問題を詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    sentence = "Please tell me if there are any problems."
    
    print(f"🔍 Analyzing: \"{sentence}\"")
    print("=" * 50)
    
    # Stanza解析の詳細取得
    stanza_analysis = detector._analyze_with_stanza(sentence)
    
    dependencies = stanza_analysis.get('dependencies', [])
    pos_tags = dict(stanza_analysis.get('pos_tags', []))
    lemmas = dict(stanza_analysis.get('lemmas', []))
    
    print("📊 All Dependencies:")
    for dep in dependencies:
        print(f"   {dep.head} --{dep.relation}-> {dep.dependent}")
        head_pos = pos_tags.get(dep.head, 'N/A')
        dep_pos = pos_tags.get(dep.dependent, 'N/A')
        print(f"      {dep.head}({head_pos}) → {dep.dependent}({dep_pos})")
    
    print("\n🏷️ POS Tags:")
    for word, pos in pos_tags.items():
        lemma = lemmas.get(word, word)
        print(f"   {word}: {pos} (lemma: {lemma})")
    
    print("\n🏗️ Clause Decomposition:")
    clauses = detector._decompose_into_clauses_v4(stanza_analysis, sentence)
    
    for i, clause in enumerate(clauses, 1):
        print(f"\n   Clause {i}:")
        print(f"      Type: {clause.clause_type}")
        print(f"      Root: {clause.root_word} ({clause.root_pos})")
        print(f"      Text: {clause.text}")
        print(f"      Subjects: {clause.subjects}")
        print(f"      Objects: {clause.objects}")
        print(f"      Has subject: {clause.has_subject()}")
        
        # パターン分析
        pattern_result = detector._analyze_clause_pattern_v4(clause, stanza_analysis, sentence)
        print(f"      Pattern: {pattern_result['pattern']}")
        print(f"      Confidence: {pattern_result['confidence']:.3f}")
        print(f"      Features: {pattern_result['features']}")
        
        # 命令文条件チェック
        if clause.clause_type == 'main':
            print(f"      ---- IMPERATIVE CHECK ----")
            print(f"      No subject: {not clause.has_subject()}")
            print(f"      Is VB/VERB: {clause.root_pos in ['VB', 'VERB']}")
            print(f"      Is main clause: {clause.clause_type == 'main'}")
            print(f"      Sentence starts with 'Please': {sentence.strip().lower().startswith('please')}")

if __name__ == "__main__":
    debug_please_tell_me()
