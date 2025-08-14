#!/usr/bin/env python3
"""
Stanza Complex Structure Analysis
================================

Verify that Stanza correctly analyzes complex grammatical structures
that our current system is missing.
"""

from advanced_grammar_detector import AdvancedGrammarDetector

def analyze_stanza_complex_parsing():
    """Analyze how well Stanza parses complex structures."""
    detector = AdvancedGrammarDetector()
    
    complex_sentences = [
        "Being a teacher, she knows how to explain difficult concepts.",
        "The book that was written by John is very good.",
        "Please tell me if there are any problems.",
        "Having finished the work, she went home.",
        "If you study hard, you will succeed.",
        "When she was young, she seemed very happy.",
    ]
    
    print("🔍 Stanza Complex Structure Analysis")
    print("=" * 60)
    
    for sentence in complex_sentences:
        print(f"\n📝 Sentence: \"{sentence}\"")
        print("-" * 50)
        
        # Get Stanza analysis
        stanza_analysis = detector._analyze_with_stanza(sentence)
        dependencies = stanza_analysis.get('dependencies', [])
        pos_tags = stanza_analysis.get('pos_tags', [])
        
        print("🔗 Dependencies:")
        for dep in dependencies:
            print(f"  {dep.dependent} --{dep.relation}--> {dep.head}")
        
        print("\n🏷️ POS Tags:")
        for word, pos in pos_tags:
            print(f"  {word}: {pos}")
        
        # Analyze specific grammatical constructions
        print("\n🧩 Grammatical Constructions Found:")
        
        # Check for specific patterns
        constructions = []
        
        # Gerund/Participle constructions
        for dep in dependencies:
            if dep.relation in ['advcl', 'amod', 'acl'] and any(pos[1] == 'VBG' for pos in pos_tags if pos[0] == dep.dependent):
                constructions.append(f"Participle/Gerund: {dep.dependent} ({dep.relation})")
        
        # Relative clauses
        for dep in dependencies:
            if dep.relation in ['acl:relcl', 'relcl']:
                constructions.append(f"Relative clause: {dep.dependent}")
        
        # Subordinate clauses
        for dep in dependencies:
            if dep.relation in ['advcl', 'ccomp', 'xcomp']:
                constructions.append(f"Subordinate clause: {dep.dependent} ({dep.relation})")
        
        # Passive constructions
        passive_indicators = [dep for dep in dependencies if dep.relation in ['nsubj:pass', 'nsubjpass', 'aux:pass', 'auxpass']]
        if passive_indicators:
            constructions.append(f"Passive voice: {', '.join([d.dependent for d in passive_indicators])}")
        
        # Copula constructions
        copula_indicators = [dep for dep in dependencies if dep.relation == 'cop']
        if copula_indicators:
            constructions.append(f"Copula construction: {', '.join([d.dependent for d in copula_indicators])}")
        
        # Existential there
        expl_indicators = [dep for dep in dependencies if dep.relation == 'expl']
        if expl_indicators:
            constructions.append(f"Existential there: {', '.join([d.dependent for d in expl_indicators])}")
        
        if constructions:
            for construction in constructions:
                print(f"  ✓ {construction}")
        else:
            print("  (No complex constructions detected)")
        
        # Check if our system would miss multiple patterns
        print("\n⚠️ Potential Multi-Pattern Detection Issues:")
        
        # Count different types of clauses/constructions
        clause_types = set()
        for dep in dependencies:
            if dep.relation in ['advcl', 'ccomp', 'xcomp', 'acl:relcl', 'relcl']:
                clause_types.add(dep.relation)
        
        construction_types = set()
        if any(dep.relation in ['nsubj:pass', 'nsubjpass', 'aux:pass', 'auxpass'] for dep in dependencies):
            construction_types.add('passive')
        if any(dep.relation == 'cop' for dep in dependencies):
            construction_types.add('copula')
        if any(dep.relation == 'expl' for dep in dependencies):
            construction_types.add('existential')
        
        total_constructions = len(clause_types) + len(construction_types)
        if total_constructions > 1:
            print(f"  📊 {total_constructions} distinct grammatical constructions found")
            print(f"  🎯 Our system would likely focus on only 1 primary pattern")
        else:
            print("  ✅ Single primary construction - our system should handle well")

def deep_dive_problematic_sentence():
    """Deep dive into the most problematic sentence."""
    detector = AdvancedGrammarDetector()
    
    sentence = "Being a teacher, she knows how to explain difficult concepts."
    print(f"\n🔬 Deep Analysis: \"{sentence}\"")
    print("=" * 60)
    
    stanza_analysis = detector._analyze_with_stanza(sentence)
    spacy_analysis = detector._analyze_with_spacy(sentence)
    
    print("📊 Stanza Detailed Analysis:")
    dependencies = stanza_analysis.get('dependencies', [])
    
    # Group dependencies by clause/construction
    main_clause_deps = []
    participle_clause_deps = []
    infinitive_deps = []
    
    for dep in dependencies:
        if dep.relation == 'advcl':
            participle_clause_deps.append(dep)
        elif dep.relation in ['xcomp', 'ccomp']:
            infinitive_deps.append(dep)
        else:
            main_clause_deps.append(dep)
    
    print(f"\n🎯 Main clause dependencies ({len(main_clause_deps)}):")
    for dep in main_clause_deps:
        print(f"  {dep.dependent} --{dep.relation}--> {dep.head}")
    
    print(f"\n🔄 Participle clause dependencies ({len(participle_clause_deps)}):")
    for dep in participle_clause_deps:
        print(f"  {dep.dependent} --{dep.relation}--> {dep.head}")
    
    print(f"\n➡️ Infinitive dependencies ({len(infinitive_deps)}):")
    for dep in infinitive_deps:
        print(f"  {dep.dependent} --{dep.relation}--> {dep.head}")
    
    print("\n💡 What our system should ideally detect:")
    print("  1. Gerund/Participle: 'Being a teacher' (adverbial clause)")
    print("  2. Main SVO: 'she knows [something]'")
    print("  3. Infinitive: 'how to explain' (embedded question + infinitive)")
    
    # Show why our current system fails
    pattern_scores = detector._calculate_pattern_scores(sentence, stanza_analysis, spacy_analysis)
    print("\n❌ Why our current system fails:")
    print("Current pattern scores:")
    sorted_scores = sorted(pattern_scores.items(), key=lambda x: x[1], reverse=True)
    for pattern, score in sorted_scores[:5]:
        if score > 0:
            print(f"  {pattern.value}: {score:.3f}")
    
    print("\n🎯 The issue: Our system treats the entire sentence as one unit,")
    print("   but Stanza correctly identifies 3 separate grammatical constructions!")

if __name__ == "__main__":
    analyze_stanza_complex_parsing()
    deep_dive_problematic_sentence()
