"""
修正後のBasic Five Patternエンジン詳細検証テスト
Rephrase的スロット分解が正確かどうかの詳細チェック
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grammar_master_controller_v2 import GrammarMasterControllerV2

def detailed_slot_verification():
    """修正後のBasic Five Patternエンジンの詳細スロット分解検証"""
    print("🔍 Basic Five Pattern エンジン詳細スロット分解検証\n")
    
    controller = GrammarMasterControllerV2()
    
    # 理論的矛盾が発生していた問題例文 + 期待されるスロット分解
    test_cases = [
        {
            "sentence": "The cat sits.",
            "description": "SV文型 - 修正前は協調システムで失敗",
            "expected_slots": {"S": "The cat", "V": "sits"},
            "expected_pattern": "SV"
        },
        {
            "sentence": "They made him captain.",
            "description": "SVOC文型 - 修正前は協調システムで失敗", 
            "expected_slots": {"S": "They", "V": "made", "O1": "him", "C1": "captain"},
            "expected_pattern": "SVOC"
        },
        {
            "sentence": "She is beautiful.",
            "description": "SVC文型",
            "expected_slots": {"S": "She", "V": "is", "C1": "beautiful"},
            "expected_pattern": "SVC"
        },
        {
            "sentence": "I love you.",
            "description": "SVO文型",
            "expected_slots": {"S": "I", "V": "love", "O1": "you"},
            "expected_pattern": "SVO"
        },
        {
            "sentence": "He gave me a book.",
            "description": "SVOO文型",
            "expected_slots": {"S": "He", "V": "gave", "O1": "me", "O2": "a book"},
            "expected_pattern": "SVOO"
        }
    ]
    
    correct_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        description = test_case["description"]
        expected = test_case["expected_slots"]
        pattern = test_case["expected_pattern"]
        
        print(f"{'='*70}")
        print(f"テスト {i}: {description}")
        print(f"例文: '{sentence}'")
        print(f"期待文型: {pattern}")
        print(f"期待スロット: {expected}")
        print("-" * 50)
        
        try:
            # 協調システムで処理
            result = controller.process_sentence(sentence, debug=True)
            
            if result and result.slots:
                print(f"✅ 処理成功")
                print(f"📋 実際のスロット分解:")
                
                # 全スロット表示
                for slot_name, slot_value in result.slots.items():
                    if slot_value.strip():  # 空でないスロットのみ
                        print(f"   {slot_name}: '{slot_value}'")
                
                # 主要スロット（大文字）のみ抽出
                main_slots = {k: v.strip() for k, v in result.slots.items() 
                             if k.upper() == k and v.strip()}
                
                print(f"🎯 主要スロット: {main_slots}")
                
                # 期待値との比較
                print(f"🔍 期待値との比較:")
                is_correct = True
                
                for exp_slot, exp_value in expected.items():
                    actual_value = main_slots.get(exp_slot, "").strip()
                    
                    if actual_value == exp_value:
                        print(f"   ✅ {exp_slot}: '{actual_value}' == '{exp_value}' (正解)")
                    else:
                        print(f"   ❌ {exp_slot}: '{actual_value}' != '{exp_value}' (不正解)")
                        is_correct = False
                
                # 余分なスロットチェック
                extra_slots = {k: v for k, v in main_slots.items() 
                              if k not in expected}
                if extra_slots:
                    print(f"   ⚠️ 余分なスロット: {extra_slots}")
                
                # 欠けているスロットチェック
                missing_slots = {k: v for k, v in expected.items() 
                               if k not in main_slots or not main_slots[k].strip()}
                if missing_slots:
                    print(f"   ❌ 欠けているスロット: {missing_slots}")
                    is_correct = False
                
                if is_correct:
                    print(f"🎉 完全正解！期待通りの{pattern}文型分解")
                    correct_count += 1
                else:
                    print(f"⚠️ 部分的不正解 - 調整が必要")
                
                # エンジン情報
                if hasattr(result, 'metadata') and result.metadata:
                    engine_info = result.metadata.get('engine_used', 'unknown')
                    strategy = result.metadata.get('coordination_strategy', 'unknown')
                    print(f"🔧 使用エンジン: {engine_info}")
                    print(f"🔧 協調戦略: {strategy}")
                    
            else:
                print("❌ 処理失敗 - 結果が空")
                
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("")
        
    # 最終結果
    total_tests = len(test_cases)
    accuracy = (correct_count / total_tests) * 100
    
    print(f"{'='*70}")
    print(f"📊 詳細検証結果:")
    print(f"   総テスト数: {total_tests}")
    print(f"   完全正解数: {correct_count}")
    print(f"   正確率: {accuracy:.1f}%")
    
    if correct_count == total_tests:
        print("🏆 全て完璧！Rephrase的スロット分解が理論通り")
    elif correct_count > 0:
        print("⚠️ 部分的成功 - 一部調整が必要")
    else:
        print("❌ 重大問題 - スロット分解が不正確")
        
    return accuracy

if __name__ == "__main__":
    detailed_slot_verification()
