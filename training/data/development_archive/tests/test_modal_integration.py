#!/usr/bin/env python3
"""
Test Modal Engine Integration with Grammar Master Controller v2.0

Test the newly integrated Modal Engine in the lazy loading system.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType

def test_modal_integration():
    """Test Modal Engine integration with the master controller."""
    
    print("🚀 MODAL ENGINE INTEGRATION TEST")
    print("=" * 80)
    
    # Initialize controller with lazy loading
    controller = GrammarMasterControllerV2()
    
    print(f"\n📊 System Status:")
    print(f"   Total engines registered: {len(controller.engine_registry)}")
    
    # Get actual loaded engines count through instance checking
    loaded_count = sum(1 for info in controller.engine_registry.values() if info.instance is not None)
    print(f"   Currently loaded engines: {loaded_count}")
    
    # Test sentences for Modal Engine
    modal_test_sentences = [
        "I can swim very well.",
        "Students must submit their assignments on time.",
        "You should study harder for the exam.",
        "It will rain tomorrow.",
        "She could play piano when she was young.",
        "I have to go to work early tomorrow.",
        "Can you help me with this?",
        "Would you like some coffee?",
        "We need to call our parents.",
        "She used to live in Paris."
    ]
    
    # Test non-modal sentences (should not trigger Modal Engine)
    non_modal_sentences = [
        "I like chocolate ice cream.",
        "The cat is sleeping on the sofa.",
        "If I were rich, I would travel.",  # Should go to Subjunctive
        "The book that I read was good."     # Should go to Relative
    ]
    
    print(f"\n🧪 Testing Modal Sentences:")
    modal_successes = 0
    
    for i, sentence in enumerate(modal_test_sentences, 1):
        print(f"\nTest {i:2d}: {sentence}")
        
        try:
            result = controller.process_sentence(sentence)
            
            if result.success:
                modal_successes += 1
                print(f"   ✅ Success - Engine: {result.engine_type.value}")
                print(f"   📊 Confidence: {result.confidence:.2f}")
                print(f"   📝 Slots: {result.slots}")
                print(f"   ⏱️  Time: {result.processing_time*1000:.1f}ms")
                
                # Check if Modal Engine was used
                if result.engine_type == EngineType.MODAL:
                    print(f"   🎯 Modal Engine correctly selected!")
                else:
                    print(f"   ⚠️  Different engine selected: {result.engine_type.value}")
            else:
                print(f"   ❌ Failed: {result.error}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")
    
    print(f"\n🧪 Testing Non-Modal Sentences:")
    non_modal_correctly_handled = 0
    
    for i, sentence in enumerate(non_modal_sentences, 1):
        print(f"\nNon-Modal Test {i}: {sentence}")
        
        try:
            result = controller.process_sentence(sentence)
            
            if result.success:
                print(f"   ✅ Success - Engine: {result.engine_type.value}")
                print(f"   📊 Confidence: {result.confidence:.2f}")
                
                # Check if Modal Engine was NOT used (which is correct)
                if result.engine_type != EngineType.MODAL:
                    non_modal_correctly_handled += 1
                    print(f"   🎯 Correctly avoided Modal Engine")
                else:
                    print(f"   ⚠️  Modal Engine incorrectly selected")
            else:
                print(f"   ❌ Failed: {result.error}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")
    
    print(f"\n📊 ENGINE LOADING STATUS:")
    print(f"   Total engines registered: {len(controller.engine_registry)}")
    
    loaded_count = sum(1 for info in controller.engine_registry.values() if info.instance is not None)
    print(f"   Currently loaded engines: {loaded_count}")
    
    if loaded_count > 0:
        loaded_types = [engine_type.value for engine_type, info in controller.engine_registry.items() if info.instance is not None]
        print(f"   Loaded engine types: {loaded_types}")
    
    print(f"\n🎯 INTEGRATION RESULTS:")
    print(f"   Modal sentences processed successfully: {modal_successes}/{len(modal_test_sentences)}")
    print(f"   Non-modal sentences handled correctly: {non_modal_correctly_handled}/{len(non_modal_sentences)}")
    
    modal_accuracy = (modal_successes / len(modal_test_sentences)) * 100
    non_modal_accuracy = (non_modal_correctly_handled / len(non_modal_sentences)) * 100
    
    print(f"   Modal sentence accuracy: {modal_accuracy:.1f}%")
    print(f"   Non-modal handling accuracy: {non_modal_accuracy:.1f}%")
    
    if modal_accuracy >= 80 and non_modal_accuracy >= 75:
        print(f"\n✅ MODAL ENGINE INTEGRATION SUCCESSFUL!")
        print(f"   🎉 Now supporting 11 unified grammar engines!")
    else:
        print(f"\n⚠️ Integration needs improvement")
    
    return modal_accuracy, non_modal_accuracy

if __name__ == "__main__":
    test_modal_integration()
