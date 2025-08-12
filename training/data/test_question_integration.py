# Question Formation Engine Integration Test
# Test script to verify the 12th engine integrates properly with the Ultimate Grammar System v1.0

import sys
import os

# Add path for imports
sys.path.append('c:/Users/yurit/Downloads/Rephraseプロジェクト20250529/完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/data')

from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType

def test_question_engine_integration():
    """Test Question Formation Engine integration into the master controller."""
    print("🚀 Testing Question Formation Engine Integration")
    print("=" * 60)
    
    # Initialize the Grammar Master Controller V2 (Ultimate Grammar System v1.0)
    grammar_system = GrammarMasterControllerV2()
    
    # Test sentences with questions
    test_cases = [
        ("What are you doing?", "WH-question test"),
        ("Are you coming to the party?", "Yes/No question test"),
        ("You like coffee, don't you?", "Tag question test"),  
        ("Do you prefer tea or coffee?", "Choice question test"),
        ("I wonder what time it is.", "Embedded question test"),
        ("How many books did you read?", "Complex WH-question test"),
        ("Can you help me with this?", "Modal question test"),
        ("Where have you been?", "Perfect tense question test"),
        ("Isn't this amazing?", "Negative question test")
    ]
    
    successful_tests = 0
    
    for sentence, description in test_cases:
        print(f"\n🔍 Testing: {description}")
        print(f"Input: '{sentence}'")
        
        try:
            # Process the sentence
            result = grammar_system.process_sentence(sentence)
            
            if result and result.success:
                print(f"✅ Engine: {result.engine_type.value}")
                print(f"🎯 Confidence: {result.confidence:.2f}")
                print(f"📊 Slots: {result.slots}")
                print(f"⏱️ Processing Time: {result.processing_time:.4f}s")
                
                # Check if it was processed by Question Formation Engine
                if result.engine_type == EngineType.QUESTION:
                    print(f"🎉 Successfully processed by Question Formation Engine!")
                    successful_tests += 1
                else:
                    print(f"ℹ️ Processed by different engine: {result.engine_type.value}")
            else:
                print(f"❌ Processing failed: {result.error if result else 'No result'}")
                
        except Exception as e:
            print(f"💥 Exception occurred: {str(e)}")
    
    print(f"\n📈 Test Summary")
    print(f"=" * 60)
    print(f"Question Formation Engine Hits: {successful_tests}/{len(test_cases)}")
    print(f"Integration Success Rate: {(successful_tests/len(test_cases))*100:.1f}%")
    
    # Print system stats
    stats = grammar_system.get_processing_stats()
    print(f"\n🏗️ System Statistics")
    print(f"Total Engines Registered: {stats.get('total_engines_registered', 0)}")
    print(f"Engines Loaded: {stats.get('engines_loaded', 0)}")
    
    print(f"\n🎯 Ultimate Grammar System v1.0 now has {stats.get('total_engines_registered', 0)} engines!")

if __name__ == "__main__":
    test_question_engine_integration()
