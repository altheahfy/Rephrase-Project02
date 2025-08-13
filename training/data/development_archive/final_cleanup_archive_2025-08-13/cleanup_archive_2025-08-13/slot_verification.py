#!/usr/bin/env python3
"""
Rephrase Slot Verification Script
Basic Five Pattern Engineの分解結果を検証
"""

from engines.basic_five_pattern_engine import BasicFivePatternEngine

def main():
    engine = BasicFivePatternEngine()
    
    test_sentences = [
        "I love programming.",
        "She is a teacher.", 
        "He gave her a book.",
        "We consider him smart.",
        "The dog runs quickly.",
        "I can speak English.",
        "They are working hard.",
        "The book was written by John."
    ]
    
    print("🔍 Rephraseスロット分解検証")
    print("=" * 50)
    
    for sentence in test_sentences:
        print(f"\n📝 \"{sentence}\"")
        result = engine.process_sentence(sentence)
        
        if result:
            print(f"   パターン: {result['pattern']}")
            for slot, value in sorted(result['slots'].items()):
                print(f"   {slot}: \"{value}\"")
        else:
            print("   ❌ 検出失敗")

if __name__ == "__main__":
    main()
