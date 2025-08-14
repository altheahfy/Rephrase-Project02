#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使役動詞 + 関係詞節テスト
システムがいつ正常動作するかを特定する
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

def test_causative_relative_combinations():
    """使役動詞と関係詞節の組み合わせテスト"""
    print("🧪 使役動詞 + 関係詞節組み合わせテスト")
    print("="*60)
    
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    decomposer = SubSlotDecomposer()
    
    # テスト例文（使役動詞の有無で比較）
    test_sentences = [
        # 1. 使役動詞なし + 関係詞節（失敗例）
        "The book that I read is interesting.",
        
        # 2. 使役動詞あり + 関係詞節（成功の可能性）
        "I made the student who was late study harder.",
        
        # 3. 使役動詞あり + 単純文（成功例）
        "I made him study hard.",
        
        # 4. 使役動詞なし + 単純文（比較用）
        "He studies hard.",
        
        # 5. 使役動詞あり + 複雑関係詞節
        "The teacher made the student who had missed class complete the assignment that was given yesterday.",
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{'='*60}")
        print(f"🔍 テスト {i}: {sentence}")
        print("="*60)
        
        try:
            # メインスロット分解
            main_result = integrator.process(sentence)
            if not main_result or 'slots' not in main_result:
                print(f"❌ メインスロット分解失敗")
                continue
                
            main_slots = main_result['slots']
            print(f"\n📌 メインスロット結果:")
            for slot, value in main_slots.items():
                if value and value.strip():
                    print(f"  {slot}: '{value}'")
            
            # 使役動詞検出状況
            has_causative = any(verb in sentence.lower() for verb in ['make', 'made', 'let', 'have', 'had', 'help', 'get'])
            print(f"🎯 使役動詞検出: {'✅ あり' if has_causative else '❌ なし'}")
            
            # サブスロット分解
            sub_slot_results = decomposer.decompose_complex_slots(main_slots)
            
            # サブスロット結果確認
            has_meaningful_subslots = False
            if sub_slot_results:
                for main_slot, sub_results in sub_slot_results.items():
                    for sub_result in sub_results:
                        if sub_result.original_text and sub_result.original_text.strip():
                            meaningful_subs = {k: v for k, v in sub_result.sub_slots.items() if v and v.strip()}
                            if meaningful_subs:
                                has_meaningful_subslots = True
                                break
            
            print(f"🎯 サブスロット生成: {'✅ 成功' if has_meaningful_subslots else '❌ 失敗'}")
            
            # 詳細サブスロット表示（成功した場合のみ）
            if has_meaningful_subslots:
                print(f"\n🎯 サブスロット詳細:")
                for main_slot, sub_results in sub_slot_results.items():
                    for j, sub_result in enumerate(sub_results, 1):
                        if sub_result.original_text and sub_result.original_text.strip():
                            print(f"  📂 {main_slot} スロット:")
                            print(f"    原文: '{sub_result.original_text}'")
                            for sub_slot, value in sub_result.sub_slots.items():
                                if value and value.strip():
                                    print(f"      {sub_slot}: '{value}'")
                    
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_causative_relative_combinations()
