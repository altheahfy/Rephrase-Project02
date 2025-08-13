#!/usr/bin/env python3
"""
Detailed slot extraction debugging for existential there sentences
"""

from grammar_master_controller_v2 import GrammarMasterControllerV2

def test_specific_sentences():
    """Test specific sentences to debug slot extraction."""
    controller = GrammarMasterControllerV2()
    
    sentences = [
        'There are three beautiful cats sleeping peacefully in the sunny garden.',
        'There will be many important decisions made during the upcoming meeting.',  
        'There have been numerous significant changes implemented since last year.'
    ]
    
    print("🔍 Detailed Slot Extraction Debug")
    print("=" * 60)
    
    for i, sentence in enumerate(sentences, 19):
        print(f'\n🧪 Test {i}: "{sentence}"')
        result = controller.process_sentence(sentence)
        
        print(f"   Engine: {result.engine_type}")
        print(f"   All Slots: {result.slots}")
        print(f"   Confidence: {result.confidence:.3f}")
        
        # Show individual slots
        for slot_name in ['S', 'V', 'Aux', 'C1', 'M1', 'M2', 'M3', 'C2']:
            if slot_name in result.slots:
                print(f"   {slot_name}: '{result.slots[slot_name]}'")
        print("-" * 50)

if __name__ == "__main__":
    test_specific_sentences()
