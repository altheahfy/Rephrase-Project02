#!/usr/bin/env python3
"""
Grammar Master Controller Slot Debug Test
Grammar Master Controllerのスロット抽出内容とサブレベル処理の詳細デバッグ

Phase 2統合でサブレベルパターン検出が失敗している原因を特定します。
"""

import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from grammar_master_controller_v2 import GrammarMasterControllerV2
    from sublevel_pattern_lib import SublevelPatternLib
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def debug_slot_processing():
    """Grammar Master Controllerのスロット処理詳細デバッグ"""
    print("🔧 Grammar Master Controller Slot Debug Test")
    print("=" * 65)
    
    controller = GrammarMasterControllerV2()
    
    # テストケース: I think that he is smart
    test_sentence = "I think that he is smart."
    
    print(f"\n🧪 Test Sentence: '{test_sentence}'")
    print("-" * 50)
    
    # 処理実行
    result = controller.process_sentence(test_sentence, debug=True)
    
    print(f"\n📊 Processing Results:")
    print(f"   Engine: {result.engine_type.value}")
    print(f"   Success: {result.success}")
    print(f"   Processing Time: {result.processing_time:.4f}s")
    
    if result.slots:
        print(f"\n🎯 Extracted Slots:")
        for slot, value in result.slots.items():
            if value and value.strip():
                print(f"   {slot}: '{value}'")
                
                # 各スロット値でサブレベルパターン検出テスト
                print(f"      → Sublevel Pattern Test...")
                lib = SublevelPatternLib()
                pattern_result = lib.analyze_sublevel_pattern(value)
                
                if pattern_result:
                    pattern_name = pattern_result[0]
                    print(f"         ✅ Pattern Detected: {pattern_name}")
                    
                    # スロット抽出テスト
                    sublevel_slots = lib.extract_sublevel_slots(value, pattern_name)
                    if sublevel_slots:
                        print(f"         📋 Sublevel Slots: {sublevel_slots}")
                    else:
                        print("         ⚠️  No sublevel slots extracted")
                else:
                    print("         ❌ No pattern detected")
                    
                    # Stanza解析詳細表示
                    try:
                        doc = lib.nlp(value)
                        sent = doc.sentences[0]
                        print("         🔍 Stanza Analysis:")
                        for word in sent.words:
                            print(f"            {word.text}: {word.pos} ({word.deprel})")
                    except Exception as parse_error:
                        print(f"         ❌ Stanza parse error: {parse_error}")
            else:
                print(f"   {slot}: (empty)")
    
    # サブレベルパターン処理結果確認
    if 'sublevel_patterns' in result.metadata:
        sublevel_data = result.metadata['sublevel_patterns']
        print(f"\n🔬 Sublevel Pattern Processing Results:")
        print(f"   Applied: {sublevel_data.get('applied', False)}")
        
        enhancement_details = sublevel_data.get('enhancement_details', {})
        processing_stats = sublevel_data.get('processing_stats', {})
        
        print(f"   Processing Stats: {processing_stats}")
        
        if enhancement_details:
            print(f"   Enhancement Details:")
            for slot, details in enhancement_details.items():
                print(f"      {slot}: enhanced={details.get('enhanced', False)}, pattern={details.get('pattern_type', 'N/A')}")
    else:
        print(f"\n⚠️  No sublevel pattern metadata found")

if __name__ == "__main__":
    debug_slot_processing()
