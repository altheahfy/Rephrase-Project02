"""
Being a teacher 構文の依存関係詳細分析
なぜ Being がルートとして認識されないかを調査
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def debug_being_a_teacher_dependency():
    """Being a teacher の依存関係を詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    sentence = "Being a teacher, she knows how to explain."
    
    print(f"🔍 Analyzing: \"{sentence}\"")
    print("=" * 50)
    
    # Stanza解析の詳細取得
    stanza_analysis = detector._analyze_with_stanza(sentence)
    
    dependencies = stanza_analysis.get('dependencies', [])
    pos_tags = dict(stanza_analysis.get('pos_tags', []))
    lemmas = dict(stanza_analysis.get('lemmas', []))
    tokens = stanza_analysis.get('tokens', [])
    
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
    
    print("\n🎯 Looking for 'Being' specifically:")
    being_deps = [dep for dep in dependencies if 'being' in dep.head.lower() or 'being' in dep.dependent.lower()]
    for dep in being_deps:
        print(f"   {dep.head} --{dep.relation}-> {dep.dependent}")
    
    # advcl 関係の詳細分析
    print("\n📍 ADVCL Relations (should catch participial constructions):")
    advcl_deps = [dep for dep in dependencies if dep.relation == 'advcl']
    for dep in advcl_deps:
        print(f"   {dep.head} --advcl-> {dep.dependent}")
        
        # この構文で分詞構文のルートを探索
        print(f"   Checking for participial root around '{dep.dependent}'...")
        
        # depのdependentに関連する全ての依存関係
        related_deps = [d for d in dependencies if d.head == dep.dependent or d.dependent == dep.dependent]
        print(f"   Related dependencies to '{dep.dependent}':")
        for rd in related_deps:
            print(f"      {rd.head} --{rd.relation}-> {rd.dependent}")
            
            # 'Being'を含む関係をチェック
            if 'being' in rd.head.lower() or 'being' in rd.dependent.lower():
                print(f"      *** FOUND 'Being' relation: {rd.head} --{rd.relation}-> {rd.dependent} ***")
    
    print("\n🔍 Tokens Analysis:")
    print(f"   Tokens: {tokens}")
    
    # 文の最初の単語をチェック
    sentence_words = sentence.split()
    if sentence_words:
        first_word = sentence_words[0]
        print(f"   First word: '{first_word}'")
        first_clean = first_word.replace(',', '').replace('.', '')
        print(f"   First word clean: '{first_clean}'")
        first_pos = pos_tags.get(first_clean, pos_tags.get(first_clean.lower(), pos_tags.get(first_clean.capitalize(), 'NOT_FOUND')))
        print(f"   First word POS: {first_pos}")

if __name__ == "__main__":
    debug_being_a_teacher_dependency()
