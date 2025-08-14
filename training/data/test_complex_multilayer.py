"""
Complex Sentence Analysis Test
複雑文の階層的文法検出テスト

テスト文: "There is a book which seems to be bought by my mother on the desk."

期待される検出:
1. Main Clause: existential_there (There is)
2. Relative Clause: relative_pattern (which seems...)
3. Infinitive Construction: infinitive_pattern (to be bought)
4. Passive Voice: passive_pattern (be bought by)
5. Prepositional Phrase: 前置詞句 (by my mother, on the desk)
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def test_complex_multilayer_sentence():
    """複雑な重層文法構造の検出テスト"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # 段階的に複雑度を上げたテスト文
    test_sentences = [
        # レベル1: 基本的な存在文
        "There is a book on the desk.",
        
        # レベル2: 関係代名詞を含む存在文
        "There is a book which is on the desk.",
        
        # レベル3: seems toを含む関係代名詞
        "There is a book which seems to be good.",
        
        # レベル4: 受動態を含む関係代名詞
        "There is a book which was bought by my mother.",
        
        # レベル5: 最終複雑文
        "There is a book which seems to be bought by my mother on the desk."
    ]
    
    print("🔍 Complex Multilayer Grammar Analysis")
    print("=" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 Level {i}: \"{sentence}\"")
        print("=" * 50)
        
        # 詳細な依存関係分析
        stanza_analysis = detector._analyze_with_stanza(sentence)
        dependencies = stanza_analysis.get('dependencies', [])
        pos_tags = dict(stanza_analysis.get('pos_tags', []))
        lemmas = dict(stanza_analysis.get('lemmas', []))
        
        print("📊 Dependency Structure:")
        for dep in dependencies:
            print(f"   {dep.head} --{dep.relation}-> {dep.dependent}")
        
        print("\n🏷️ POS & Lemma Analysis:")
        for word, pos in pos_tags.items():
            lemma = lemmas.get(word, word)
            print(f"   {word} ({lemma}): {pos}")
        
        # 階層的文法検出
        result = detector.detect_hierarchical_grammar(sentence)
        
        print(f"\n🏗️ Hierarchical Grammar Analysis:")
        print(f"   📍 Main Clause: {result.main_clause.grammatical_pattern if result.main_clause else 'None'}")
        if result.main_clause:
            print(f"      - Text: {result.main_clause.text}")
            print(f"      - Confidence: {result.main_clause.confidence:.3f}")
            print(f"      - Root: {result.main_clause.root_word} ({result.main_clause.root_pos})")
            print(f"      - Subjects: {result.main_clause.subjects}")
            print(f"      - Objects: {result.main_clause.objects}")
            print(f"      - Complements: {result.main_clause.complements}")
        
        if result.subordinate_clauses:
            print(f"\n   📋 Subordinate Clauses ({len(result.subordinate_clauses)}):")
            for j, clause in enumerate(result.subordinate_clauses, 1):
                print(f"      {j}. {clause.grammatical_pattern} (conf: {clause.confidence:.3f})")
                print(f"         - Type: {clause.clause_type}")
                print(f"         - Text: {clause.text}")
                print(f"         - Root: {clause.root_word} ({clause.root_pos})")
        
        if result.embedded_constructions:
            print(f"\n   🔧 Embedded Constructions ({len(result.embedded_constructions)}):")
            for j, const in enumerate(result.embedded_constructions, 1):
                print(f"      {j}. {const.grammatical_pattern} (conf: {const.confidence:.3f})")
                print(f"         - Type: {const.clause_type}")
                print(f"         - Text: {const.text}")
        
        print(f"\n   📊 Analysis Summary:")
        print(f"      - Complexity: {result.overall_complexity:.3f}")
        print(f"      - Engines: {result.recommended_engines}")
        print(f"      - Strategy: {result.coordination_strategy}")
        print(f"      - Processing Time: {result.processing_time:.3f}s")
        
        # 特定の文法要素の検出確認
        print(f"\n   ✅ Grammar Elements Detection:")
        
        # existential there検出
        has_existential = any(
            clause.grammatical_pattern.value == 'existential_there' 
            for clause in [result.main_clause] + result.subordinate_clauses + result.embedded_constructions
            if clause and clause.grammatical_pattern
        )
        print(f"      - Existential 'There': {'✅ Detected' if has_existential else '❌ Not detected'}")
        
        # 関係代名詞検出
        has_relative = any(
            clause.grammatical_pattern.value == 'relative_pattern'
            for clause in [result.main_clause] + result.subordinate_clauses + result.embedded_constructions
            if clause and clause.grammatical_pattern
        )
        print(f"      - Relative Clause: {'✅ Detected' if has_relative else '❌ Not detected'}")
        
        # 不定詞検出
        has_infinitive = any(
            clause.grammatical_pattern.value == 'infinitive_pattern'
            for clause in [result.main_clause] + result.subordinate_clauses + result.embedded_constructions
            if clause and clause.grammatical_pattern
        )
        print(f"      - Infinitive (to): {'✅ Detected' if has_infinitive else '❌ Not detected'}")
        
        # 受動態検出
        has_passive = any(
            clause.grammatical_pattern.value == 'passive_pattern'
            for clause in [result.main_clause] + result.subordinate_clauses + result.embedded_constructions
            if clause and clause.grammatical_pattern
        )
        print(f"      - Passive Voice: {'✅ Detected' if has_passive else '❌ Not detected'}")
        
        # seems to 検出
        has_seems = 'seems' in sentence.lower()
        seems_detected = any(
            'seems' in clause.text.lower()
            for clause in [result.main_clause] + result.subordinate_clauses + result.embedded_constructions
            if clause
        )
        if has_seems:
            print(f"      - 'Seems to' construction: {'✅ Detected' if seems_detected else '❌ Not detected'}")
        
        # by句（agent）検出
        has_by_agent = 'by' in sentence.lower() and any(word in sentence.lower() for word in ['mother', 'father', 'teacher'])
        by_detected = any(
            'by' in clause.text.lower()
            for clause in [result.main_clause] + result.subordinate_clauses + result.embedded_constructions
            if clause
        )
        if has_by_agent:
            print(f"      - By-agent phrase: {'✅ Detected' if by_detected else '❌ Not detected'}")

if __name__ == "__main__":
    test_complex_multilayer_sentence()
