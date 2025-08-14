#!/usr/bin/env python3
"""
Complex Grammar Structure Test
==============================

Test the current system's ability to handle:
1. Complex sentences with multiple clauses
2. Multiple grammar patterns in one sentence
3. Embedded constructions
4. Compound and complex sentence structures
"""

from high_precision_grammar_detector import HighPrecisionGrammarDetector
from advanced_grammar_detector import GrammarPattern

def test_complex_structures():
    """Test complex and compound sentence structures."""
    detector = HighPrecisionGrammarDetector(log_level="INFO")
    
    complex_sentences = [
        # 複文構造 (Complex sentences)
        ("The book that was written by John is very good.", "相対節 + 受動態 + SVC構文"),
        ("If you study hard, you will succeed.", "条件節 + 単純未来"),
        ("When she was young, she seemed very happy.", "時間節 + SVC構文"),
        ("Although it looks difficult, I think it's easy.", "譲歩節 + SVO + SVC構文"),
        
        # 重文構造 (Compound sentences)  
        ("She reads books, and he writes stories.", "SVO + SVO (並列)"),
        ("The door was closed, but the window was open.", "受動態 + 受動態"),
        ("There are many problems, so we need solutions.", "存在文 + SVO"),
        
        # 複合文法要素 (Multiple grammar elements)
        ("Being tired, he decided to rest.", "分詞構文 + SVO"),
        ("To succeed, you must work hard.", "不定詞句 + 助動詞 + SVO"),
        ("Having finished the work, she went home.", "完了分詞 + SVO"),
        
        # 埋め込み構造 (Embedded structures)
        ("I know that she seems happy today.", "SVO + that節 + SVC構文"),
        ("The man who is standing there looks familiar.", "関係節 + 進行形 + SVC構文"),
        ("What he said was completely wrong.", "関係節 + SVC構文"),
        
        # 複雑な命令文
        ("Please tell him that the meeting was cancelled.", "命令文 + that節 + 受動態"),
        ("Don't forget to bring what you promised.", "否定命令文 + 不定詞 + 関係節"),
        
        # 存在文の複雑形
        ("There were many people who seemed unhappy.", "存在文 + 関係節 + SVC構文"),
        ("There's something that needs to be done.", "存在文 + 関係節 + 受動不定詞"),
    ]
    
    print("🔍 Complex Grammar Structure Analysis")
    print("=" * 60)
    
    results = []
    for sentence, description in complex_sentences:
        print(f"\n📝 Sentence: \"{sentence}\"")
        print(f"📋 Description: {description}")
        
        try:
            result = detector.detect_grammar_pattern(sentence)
            
            print(f"🎯 Primary Pattern: {result.primary_pattern.value}")
            print(f"📊 Confidence: {result.confidence:.3f}")
            print(f"🔄 Secondary Patterns: {[p.value for p in result.secondary_patterns[:3]]}")
            print(f"🤖 Recommended Engines: {result.recommended_engines}")
            print(f"⚡ Coordination Strategy: {result.coordination_strategy}")
            print(f"🧩 Complexity Score: {result.complexity_score:.3f}")
            
            # 複雑度分析
            complexity_level = "Simple" if result.complexity_score < 0.5 else \
                              "Moderate" if result.complexity_score < 0.8 else "Complex"
            print(f"📈 Complexity Level: {complexity_level}")
            
            # 複数パターンの検出状況
            total_patterns = len([p for p in result.secondary_patterns if p != result.primary_pattern]) + 1
            print(f"🔢 Detected Patterns: {total_patterns}")
            
            results.append({
                'sentence': sentence,
                'description': description,
                'primary': result.primary_pattern,
                'secondary_count': len(result.secondary_patterns),
                'complexity': result.complexity_score,
                'engines': len(result.recommended_engines)
            })
            
        except Exception as e:
            print(f"❌ Error analyzing: {e}")
            results.append({
                'sentence': sentence,
                'description': description,
                'primary': None,
                'error': str(e)
            })
    
    # 統計分析
    print(f"\n📊 Complex Structure Analysis Summary")
    print("=" * 60)
    
    successful_analyses = [r for r in results if 'error' not in r]
    if successful_analyses:
        avg_complexity = sum(r['complexity'] for r in successful_analyses) / len(successful_analyses)
        avg_secondary = sum(r['secondary_count'] for r in successful_analyses) / len(successful_analyses)
        avg_engines = sum(r['engines'] for r in successful_analyses) / len(successful_analyses)
        
        print(f"Successfully analyzed: {len(successful_analyses)}/{len(results)} sentences")
        print(f"Average complexity score: {avg_complexity:.3f}")
        print(f"Average secondary patterns: {avg_secondary:.1f}")
        print(f"Average recommended engines: {avg_engines:.1f}")
        
        # 複雑度分布
        simple_count = len([r for r in successful_analyses if r['complexity'] < 0.5])
        moderate_count = len([r for r in successful_analyses if 0.5 <= r['complexity'] < 0.8])
        complex_count = len([r for r in successful_analyses if r['complexity'] >= 0.8])
        
        print(f"\nComplexity Distribution:")
        print(f"  Simple (< 0.5): {simple_count}")
        print(f"  Moderate (0.5-0.8): {moderate_count}")
        print(f"  Complex (≥ 0.8): {complex_count}")
        
        # 最も複雑な文の分析
        most_complex = max(successful_analyses, key=lambda x: x['complexity'])
        print(f"\nMost Complex Sentence:")
        print(f"  \"{most_complex['sentence']}\"")
        print(f"  Complexity: {most_complex['complexity']:.3f}")
        print(f"  Secondary patterns: {most_complex['secondary_count']}")
    
    return results

def analyze_multi_pattern_detection():
    """Analyze how well the system detects multiple patterns in complex sentences."""
    detector = HighPrecisionGrammarDetector()
    
    # 既知の複数パターンを含む文
    multi_pattern_sentences = [
        ("The book that was written by John seems interesting.", 
         ["relative_pattern", "passive_pattern", "svc_pattern"]),
        
        ("Please tell me if there are any problems.",
         ["imperative_pattern", "existential_there"]),
         
        ("Being a teacher, she knows how to explain difficult concepts.",
         ["gerund_pattern", "svo_pattern", "infinitive_pattern"]),
    ]
    
    print(f"\n🔬 Multi-Pattern Detection Analysis")
    print("=" * 60)
    
    for sentence, expected_patterns in multi_pattern_sentences:
        result = detector.detect_grammar_pattern(sentence)
        detected_patterns = [result.primary_pattern.value] + [p.value for p in result.secondary_patterns]
        
        print(f"\nSentence: \"{sentence}\"")
        print(f"Expected patterns: {expected_patterns}")
        print(f"Detected patterns: {detected_patterns[:5]}")  # Top 5
        
        # 検出率の計算
        matches = len(set(expected_patterns) & set(detected_patterns))
        coverage = matches / len(expected_patterns) * 100
        
        print(f"Pattern coverage: {matches}/{len(expected_patterns)} ({coverage:.1f}%)")

if __name__ == "__main__":
    complex_results = test_complex_structures()
    analyze_multi_pattern_detection()
