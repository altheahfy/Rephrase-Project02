#!/usr/bin/env python3
"""
Phase A3-1: PureCentralController 初期テスト
=========================================

新しく実装した純粋管理機能のテスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper, PureCentralController

def test_pure_central_controller():
    """PureCentralControllerの基本動作テスト"""
    print("🎯 Phase A3-1: PureCentralController 初期テスト開始")
    print("=" * 60)
    
    # Step 1: DynamicGrammarMapperインスタンス作成
    print("Step 1: DynamicGrammarMapper初期化...")
    mapper = DynamicGrammarMapper()
    print("✅ DynamicGrammarMapper初期化完了")
    
    # Step 2: PureCentralControllerインスタンス作成
    print("\nStep 2: PureCentralController初期化...")
    controller = PureCentralController(mapper)
    print("✅ PureCentralController初期化完了")
    
    # Step 3: テストケース実行
    test_cases = [
        "The doctor who works carefully saves lives successfully.",  # Phase A2の成功例
        "The book was written by John.",  # 受動態テスト
        "The cat sits on the mat."  # シンプルなSVO
    ]
    
    print(f"\nStep 3: {len(test_cases)}件のテストケース実行...")
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n--- テスト {i}: {sentence} ---")
        
        try:
            # 純粋管理機能でのテスト
            result = controller.analyze_sentence_pure_management(sentence)
            
            # 基本チェック
            main_verb = result.get('slots', {}).get('V', 'NOT_FOUND')
            slots_count = len(result.get('slots', {}))
            has_management_info = 'management_info' in result
            
            print(f"✅ 実行成功:")
            print(f"   主動詞: {main_verb}")
            print(f"   スロット数: {slots_count}")
            print(f"   管理情報: {'あり' if has_management_info else 'なし'}")
            
            if 'error' in result:
                print(f"⚠️  エラー情報: {result['error']}")
            
        except Exception as e:
            print(f"❌ 実行エラー: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 PureCentralController 初期テスト完了")
    
    # Step 4: 従来の方法との比較
    print("\nStep 4: 従来方法との比較テスト...")
    test_sentence = "The doctor who works carefully saves lives successfully."
    
    print(f"比較対象: {test_sentence}")
    
    # 従来の方法
    print("\n【従来のDynamicGrammarMapper】")
    try:
        old_result = mapper.analyze_sentence(test_sentence)
        old_verb = old_result.get('slots', {}).get('V', 'NOT_FOUND')
        print(f"主動詞: {old_verb}")
        print(f"スロット数: {len(old_result.get('slots', {}))}")
    except Exception as e:
        print(f"エラー: {str(e)}")
    
    # 新しい純粋管理方法
    print("\n【新しいPureCentralController】")
    try:
        new_result = controller.analyze_sentence_pure_management(test_sentence)
        new_verb = new_result.get('slots', {}).get('V', 'NOT_FOUND')
        print(f"主動詞: {new_verb}")
        print(f"スロット数: {len(new_result.get('slots', {}))}")
        print(f"管理情報: {'あり' if 'management_info' in new_result else 'なし'}")
    except Exception as e:
        print(f"エラー: {str(e)}")
    
    print("\n🎉 Phase A3-1 初期実装テスト完了!")

if __name__ == "__main__":
    test_pure_central_controller()
