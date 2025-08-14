#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係詞節サブスロット分解の最終テスト
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

def final_relative_clause_test():
    """関係詞節の最終テスト"""
    print("🎯 関係詞節サブスロット分解 - 最終テスト")
    print("="*60)
    
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    decomposer = SubSlotDecomposer()
    
    # 関係詞節に特化したテスト
    test_sentences = [
        "The book that I bought is interesting.",
        "The person who knows me is here.",
        "The students who were studying passed the exam.",
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{'='*40}")
        print(f"🔍 テスト {i}: {sentence}")
        print("="*40)
        
        try:
            # メインスロット分解
            main_result = integrator.process(sentence)
            main_slots = main_result['slots']
            
            print(f"📌 主語: '{main_slots.get('S', '')}' ")
            print(f"📌 動詞: '{main_slots.get('V', '')}' ")
            
            # サブスロット分解
            sub_slot_results = decomposer.decompose_complex_slots(main_slots)
            
            # 関係詞節のサブスロット確認
            if 'S' in sub_slot_results:
                s_result = sub_slot_results['S'][0]
                print(f"🎯 関係詞節: '{s_result.original_text}'")
                print(f"🎯 サブスロット:")
                for sub_slot, value in s_result.sub_slots.items():
                    if value and value.strip():
                        print(f"   {sub_slot}: '{value}'")
            else:
                print("❌ 関係詞節サブスロット生成失敗")
                    
        except Exception as e:
            print(f"❌ エラー: {e}")

if __name__ == "__main__":
    final_relative_clause_test()
