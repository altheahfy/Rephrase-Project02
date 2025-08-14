#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サブスロット分解デバッグテスト
正しい例文でサブスロット分解を確認
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

def test_sub_slot_decomposition():
    """サブスロット分解をテスト"""
    print("🧪 サブスロット分解デバッグテスト開始")
    print("="*60)
    
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    decomposer = SubSlotDecomposer()
    
    # テスト例文（複文）
    test_sentences = [
        "The book that I bought yesterday is interesting.",  # 関係詞節
        "The person who knows someone is here.",  # 関係詞節（主語内）
        "Because she was tired, she went to bed early.",  # 副詞節
        "While studying hard, she worked part-time.",  # 副詞節
        "The students who were studying have been working.",  # 複合関係詞節
        "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."  # 超複雑文（完璧テストと同じ）
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{'='*60}")
        print(f"🔍 テスト {i}: {sentence}")
        print("="*60)
        
        try:
            # Step 1: メインスロット分解
            main_result = integrator.process(sentence)
            if not main_result or 'slots' not in main_result:
                print(f"❌ メインスロット分解失敗")
                continue
                
            main_slots = main_result['slots']
            print(f"\n📌 メインスロット結果:")
            for slot, value in main_slots.items():
                if value and value.strip():
                    print(f"  {slot}: '{value}'")
            
            # Step 2: サブスロット分解
            sub_slot_results = decomposer.decompose_complex_slots(main_slots)
            
            # Step 3: 結果表示
            print(f"\n🎯 サブスロット分解結果:")
            if sub_slot_results:
                for main_slot, sub_results in sub_slot_results.items():
                    print(f"\n  📂 {main_slot} スロット:")
                    for j, sub_result in enumerate(sub_results, 1):
                        print(f"    {j}. タイプ: {sub_result.clause_type}")
                        print(f"       原文: '{sub_result.original_text}'")
                        print(f"       信頼度: {sub_result.confidence:.1%}")
                        print(f"       サブスロット:")
                        for sub_slot, value in sub_result.sub_slots.items():
                            if value and value.strip():
                                print(f"         {sub_slot}: '{value}'")
            else:
                print("  ❌ サブスロット結果なし")
            
            # Step 4: クリアされたメインスロット確認
            print(f"\n🧹 クリア後メインスロット:")
            for slot, value in main_slots.items():
                if slot in ['S', 'M2', 'M3', 'C2']:  # サブスロット対象スロット
                    status = "✅ クリア済み" if not value or not value.strip() else f"⚠️ 残存: '{value}'"
                    print(f"  {slot}: {status}")
                    
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_sub_slot_decomposition()
