"""
実際の複雑な例文でのHierarchicalGrammarDetectorV4性能評価
- 5つ程度の文法項目を含む
- 従属節の入れ子構造が2つ
- 従属節内にも2つ程度の文法項目を含む
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def create_complex_test_sentences():
    """複雑な例文を作成して実際の解析性能をテスト"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # 複雑な例文セット
    complex_sentences = [
        {
            "sentence": "Having finished the project that was assigned by the teacher, the student who had been working diligently submitted it confidently.",
            "expected_grammar_items": [
                "participle_pattern",      # Having finished (分詞構文)
                "passive_pattern",         # was assigned (受動態) 
                "relative_pattern",        # that was assigned (関係節)
                "relative_pattern",        # who had been working (関係節)
                "perfect_progressive",     # had been working (過去完了進行形)
                "svo_pattern"             # submitted it (主節のSVO)
            ],
            "nested_structures": [
                "the project [that was assigned by the teacher]",  # 入れ子1
                "the student [who had been working diligently]"    # 入れ子2
            ],
            "description": "分詞構文 + 受動関係節 + 能動関係節 + 完了進行形"
        },
        {
            "sentence": "While she was reading the book that her friend had recommended, she discovered what made the story so compelling.",
            "expected_grammar_items": [
                "conjunction_pattern",     # While she was reading (時間の従属節)
                "relative_pattern",        # that her friend had recommended (関係節)
                "perfect_pattern",         # had recommended (過去完了)
                "noun_clause",            # what made the story compelling (名詞節)
                "svoc_pattern",           # made the story compelling (SVOC)
                "svo_pattern"             # she discovered (主節のSVO)
            ],
            "nested_structures": [
                "the book [that her friend had recommended]",      # 入れ子1
                "discovered [what made the story so compelling]"   # 入れ子2
            ],
            "description": "時間節 + 関係節 + 過去完了 + 名詞節 + SVOC"
        },
        {
            "sentence": "Before starting the presentation that he had prepared carefully, Tom asked me what I thought about the topic.",
            "expected_grammar_items": [
                "gerund_pattern",         # starting (動名詞)
                "relative_pattern",       # that he had prepared (関係節)
                "perfect_pattern",        # had prepared (過去完了)
                "svoo_pattern",          # asked me what (SVOO)
                "noun_clause",           # what I thought (名詞節)
                "imperative_pattern"     # 暗黙の命令的要素
            ],
            "nested_structures": [
                "the presentation [that he had prepared carefully]", # 入れ子1
                "asked me [what I thought about the topic]"          # 入れ子2
            ],
            "description": "動名詞 + 関係節 + 過去完了 + SVOO + 名詞節"
        }
    ]
    
    print("🧪 Real Complex Sentence Analysis Test")
    print("=" * 70)
    print("目標: 実際の複雑な例文での解析精度確認")
    print()
    
    total_sentences = len(complex_sentences)
    successful_analyses = 0
    
    for i, test_case in enumerate(complex_sentences, 1):
        print(f"📝 Test Case {i}/{total_sentences}")
        print(f"Description: {test_case['description']}")
        print(f"Sentence: {test_case['sentence']}")
        print()
        
        # 実際の解析実行
        start_time = time.time()
        result = detector.detect_hierarchical_grammar(test_case['sentence'])
        analysis_time = time.time() - start_time
        
        print(f"⏱️ Analysis Time: {analysis_time:.3f}s")
        print()
        
        # 主節解析結果
        print(f"🎯 Main Clause Analysis:")
        print(f"   Pattern: {result.main_clause.grammatical_pattern.value}")
        print(f"   Confidence: {result.main_clause.confidence:.2f}")
        print(f"   Text: '{result.main_clause.text[:60]}...'")
        print()
        
        # 従属節解析結果
        print(f"🔗 Subordinate Clauses Analysis:")
        detected_patterns = []
        for j, clause in enumerate(result.subordinate_clauses, 1):
            pattern = clause.grammatical_pattern.value
            detected_patterns.append(pattern)
            print(f"   Sub {j}: {pattern} (conf: {clause.confidence:.2f})")
            print(f"          Text: '{clause.text[:50]}...'")
        
        print()
        
        # 入れ子構造の確認
        print(f"🏗️ Nested Structure Detection:")
        for structure in test_case['nested_structures']:
            print(f"   Expected: {structure}")
        print()
        
        # 文法項目の検出評価
        expected_patterns = test_case['expected_grammar_items']
        all_detected = [result.main_clause.grammatical_pattern.value] + detected_patterns
        
        print(f"📊 Grammar Pattern Detection:")
        print(f"   Expected: {expected_patterns}")
        print(f"   Detected: {all_detected}")
        
        # パターンマッチング評価
        matches = len(set(expected_patterns) & set(all_detected))
        total_expected = len(expected_patterns)
        accuracy = matches / total_expected * 100 if total_expected > 0 else 0
        
        print(f"   Matches: {matches}/{total_expected} = {accuracy:.1f}%")
        
        if accuracy >= 70:  # 複雑な文では70%以上を良好とする
            print(f"   ✅ GOOD - Complex sentence analysis successful!")
            successful_analyses += 1
        elif accuracy >= 50:
            print(f"   🔶 MODERATE - Partial success")
        else:
            print(f"   ❌ NEEDS IMPROVEMENT")
        
        print()
        print("=" * 70)
        print()
    
    # 総合評価
    overall_success_rate = successful_analyses / total_sentences * 100
    print(f"🏆 OVERALL COMPLEX SENTENCE ANALYSIS RESULTS:")
    print(f"Successful Analyses: {successful_analyses}/{total_sentences} = {overall_success_rate:.1f}%")
    
    if overall_success_rate >= 80:
        print("🎉 EXCELLENT - System handles complex sentences very well!")
    elif overall_success_rate >= 60:
        print("✅ GOOD - System performs well on complex sentences")
    elif overall_success_rate >= 40:
        print("🔶 MODERATE - Some room for improvement")
    else:
        print("❌ NEEDS SIGNIFICANT IMPROVEMENT")
    
    return overall_success_rate >= 60

if __name__ == "__main__":
    import time
    success = create_complex_test_sentences()
