"""
Imperative Pattern Detection Test
命令文検出の修正効果をテスト
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def test_imperative_improvements():
    """修正された命令文検出をテスト"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    test_cases = [
        "Go to school now.",
        "Please tell me if there are any problems.",
        "Come here quickly.",
        "Stop talking.",
        "Help me with this.",
    ]
    
    print("🧪 Testing Improved Imperative Detection")
    print("=" * 50)
    
    for sentence in test_cases:
        print(f"\n📝 Sentence: \"{sentence}\"")
        print("-" * 40)
        
        result = detector.detect_grammar_pattern(sentence)
        
        print(f"🏗️ Primary Pattern: {result.primary_pattern}")
        print(f"⚡ Confidence: {result.confidence:.3f}")
        print(f"� Recommended Engines: {result.recommended_engines}")
        
        # Expected for imperatives
        pattern_name = result.primary_pattern.name if hasattr(result.primary_pattern, 'name') else str(result.primary_pattern)
        is_imperative = 'IMPERATIVE' in pattern_name
        status = "✅" if is_imperative else "❌"
        print(f"🎯 Imperative Detection: {status} (Pattern: {pattern_name})")

if __name__ == "__main__":
    test_imperative_improvements()
