"""
最終的な成功率確認ツール
15例文の仮定法例文で100%成功達成確認
"""

from central_controller import CentralController

def test_final_conditional_success():
    controller = CentralController()
    
    # 仮定法15例文（Cases 141-155）
    conditional_cases = {
        141: "Should you need help, please call me.",
        142: "Were I you, I would say yes.",
        143: "If you give me more time, I will finish the project.",
        144: "Had she known the truth, she would have acted differently.",
        145: "If I were rich, I would travel the world.",
        146: "Should anyone ask, tell them I'm busy.",
        147: "Unless you study hard, you won't pass the exam.",
        148: "As if I didn't know that already.",
        149: "If only I could fly like a bird.",
        150: "Provided that you agree, we can proceed.",
        151: "But for your help, I would have failed.",
        152: "Without your support, we couldn't have succeeded.",
        153: "Had it not been for your advice, I would have made a mistake.",
        154: "Were it not for the rain, we would go out.",
        155: "If I had known you were coming, I would have prepared dinner."
    }
    
    success_count = 0
    total_count = len(conditional_cases)
    
    print(f"\n🎯 条件文テスト - 15例文での成功率確認")
    print(f"{'='*60}")
    
    for case_num, sentence in conditional_cases.items():
        try:
            result = controller.process_sentence(sentence)
            success = result.get('success', False)
            
            if success:
                success_count += 1
                status = "✅ SUCCESS"
            else:
                status = f"❌ FAILED: {result.get('error', 'Unknown error')}"
            
            print(f"Case {case_num:3d}: {status}")
            
        except Exception as e:
            print(f"Case {case_num:3d}: ❌ EXCEPTION: {str(e)}")
    
    success_rate = (success_count / total_count) * 100
    
    print(f"\n{'='*60}")
    print(f"🎯 最終結果:")
    print(f"   成功: {success_count}/{total_count} 例文")
    print(f"   成功率: {success_rate:.1f}%")
    
    if success_rate == 100.0:
        print(f"🎉 ★★★ 100% SUCCESS ACHIEVED! ★★★")
        print(f"🎯 ユーザー目標「エラーをゼロにするぞ」達成！")
    else:
        print(f"⚠️ 目標未達成 - 残り{total_count - success_count}例文要修正")
    
    return success_rate == 100.0

if __name__ == "__main__":
    test_final_conditional_success()
