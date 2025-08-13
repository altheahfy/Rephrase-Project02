"""
修正後の基本5文型エンジン検証テスト
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grammar_master_controller_v2 import GrammarMasterControllerV2

def test_basic_five_pattern_fix():
    """修正後のBasic Five Patternエンジンの動作確認"""
    print("🔧 修正後のBasic Five Patternエンジンテスト開始\n")
    
    controller = GrammarMasterControllerV2()
    
    # 理論的矛盾が発生していた問題例文
    test_cases = [
        ("The cat sits.", "SV文型 - 修正前は協調システムで失敗"),
        ("They made him captain.", "SVOC文型 - 修正前は協調システムで失敗"),
        ("She is beautiful.", "SVC文型"),
        ("I love you.", "SVO文型"),
        ("He gave me a book.", "SVOO文型"),
    ]
    
    success_count = 0
    
    for i, (sentence, description) in enumerate(test_cases, 1):
        print(f"テスト {i}: {description}")
        print(f"例文: '{sentence}'")
        
        try:
            # 協調システムで処理
            result = controller.process_sentence(sentence)
            
            if result and result.slots and len(result.slots) > 0:
                print("✅ 成功 - 協調システムで正常処理")
                print(f"   結果スロット数: {len(result.slots)}")
                
                # 主要スロット表示
                main_slots = {k: v for k, v in result.slots.items() if k.upper() == k and v.strip()}
                print(f"   主要スロット: {main_slots}")
                
                success_count += 1
            else:
                print("❌ 失敗 - 結果が空")
                
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
        
        print("-" * 60)
        
    # 結果サマリー
    total_tests = len(test_cases)
    success_rate = (success_count / total_tests) * 100
    
    print(f"\n📊 テスト結果サマリー:")
    print(f"   総テスト数: {total_tests}")
    print(f"   成功数: {success_count}")
    print(f"   成功率: {success_rate:.1f}%")
    
    if success_count == total_tests:
        print("🎉 修正完了！全ての基本5文型が協調システムで正常動作")
    elif success_count > 0:
        print("⚠️ 部分的改善 - さらなる調整が必要")
    else:
        print("❌ 修正効果なし - 追加調査が必要")
        
    return success_rate

if __name__ == "__main__":
    test_basic_five_pattern_fix()
