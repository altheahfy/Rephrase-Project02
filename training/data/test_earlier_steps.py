#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
正しいRephrase分解ができていた時点を特定
"""

import sys
sys.path.append('./archive')

def test_earlier_steps():
    """より前のstepで正しい分解があったかテスト"""
    print("🔍 正しいRephrase分解の探査")
    print("=" * 60)
    
    test_phrase = "the woman who seemed indecisive"
    
    # Step13 O1専用システムをテスト
    try:
        from step13_o1_subslot import O1SubslotGenerator
        print("\n📋 Step13 (O1専用) テスト")
        generator = O1SubslotGenerator()
        result = generator.generate_o1_subslots(test_phrase, "phrase")
        print(f"   分解結果数: {len(result)}")
        for sub_type, sub_data in result.items():
            print(f"   ✅ {sub_type}: '{sub_data['text'] if isinstance(sub_data, dict) else sub_data}'")
    except Exception as e:
        print(f"   ❌ Step13 エラー: {str(e)}")
    
    # Step12 S専用システムをテスト
    try:
        from step12_s_subslot import SSubslotGenerator
        print("\n📋 Step12 (S専用) テスト")
        generator = SSubslotGenerator()
        result = generator.generate_s_subslots(test_phrase, "phrase")
        print(f"   分解結果数: {len(result)}")
        for sub_type, sub_data in result.items():
            print(f"   ✅ {sub_type}: '{sub_data['text'] if isinstance(sub_data, dict) else sub_data}'")
    except Exception as e:
        print(f"   ❌ Step12 エラー: {str(e)}")
    
    # Step10 C1専用システムをテスト
    try:
        from step10_c1_subslot import C1SubslotGenerator
        print("\n📋 Step10 (C1専用) テスト")
        generator = C1SubslotGenerator()
        result = generator.generate_c1_subslots("indecisive", "word")
        print(f"   分解結果数: {len(result)}")
        for sub_type, sub_data in result.items():
            print(f"   ✅ {sub_type}: '{sub_data['text'] if isinstance(sub_data, dict) else sub_data}'")
    except Exception as e:
        print(f"   ❌ Step10 エラー: {str(e)}")

if __name__ == "__main__":
    test_earlier_steps()
