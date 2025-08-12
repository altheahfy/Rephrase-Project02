#!/usr/bin/env python3
"""
倒置構文エンジン 統合テスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.inversion_engine import InversionEngine

def test_inversion_engine():
    """倒置構文エンジンの包括的テスト"""
    print("🔥 倒置構文エンジン 統合テスト開始")
    print("🚀 倒置構文エンジン初期化中...")
    
    try:
        engine = InversionEngine()
        print("✅ 初期化完了")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return
    
    print("\n📝 独立文処理テスト")
    print("=" * 50)
    
    test_cases = [
        # 否定の倒置
        {
            'name': '否定の倒置 (Never)',
            'sentence': 'Never have I seen such beauty.',
            'expected_pattern': 'negative_inversion'
        },
        {
            'name': '否定の倒置 (Not only)',
            'sentence': 'Not only did he win the race.',
            'expected_pattern': 'negative_inversion'
        },
        {
            'name': '否定の倒置 (Hardly)',
            'sentence': 'Hardly had I arrived when it started raining.',
            'expected_pattern': 'negative_inversion'
        },
        
        # 副詞句の倒置
        {
            'name': '副詞句の倒置 (場所)',
            'sentence': 'On the table lay a book.',
            'expected_pattern': 'adverbial_inversion'
        },
        {
            'name': '副詞句の倒置 (in句)',
            'sentence': 'In the garden stood a beautiful tree.',
            'expected_pattern': 'adverbial_inversion'
        },
        
        # 条件文の倒置
        {
            'name': '条件倒置 (Had)',
            'sentence': 'Had I known, I would have come.',
            'expected_pattern': 'conditional_inversion'
        },
        {
            'name': '条件倒置 (Were)',
            'sentence': 'Were I you, I would accept the offer.',
            'expected_pattern': 'conditional_inversion'
        },
        {
            'name': '条件倒置 (Should)',
            'sentence': 'Should you need help, please call me.',
            'expected_pattern': 'conditional_inversion'
        },
        
        # 比較の倒置
        {
            'name': '比較倒置 (So)',
            'sentence': 'So beautiful was she that everyone stared.',
            'expected_pattern': 'comparative_inversion'
        },
        {
            'name': '比較倒置 (Such)',
            'sentence': 'Such was his anger that he couldn\'t speak.',
            'expected_pattern': 'comparative_inversion'
        },
        
        # 場所の倒置
        {
            'name': '場所倒置 (Down)',
            'sentence': 'Down the hill ran the children.',
            'expected_pattern': 'locative_inversion'
        },
        {
            'name': '場所倒置 (Away)',
            'sentence': 'Away flew the bird.',
            'expected_pattern': 'locative_inversion'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 テスト{i}: {test_case['name']}")
        print(f"入力: {test_case['sentence']}")
        
        try:
            result = engine.process(test_case['sentence'])
            
            if result:
                print(f"✅ 処理成功: {result.get('tense_type', 'unknown')}")
                
                print(f"  📋 上位スロット:")
                for key, value in result.items():
                    if not key.startswith('sub-') and key not in ['metadata', 'tense_type']:
                        print(f"    {key}: '{value}'")
                
                print(f"  📋 サブスロット:")
                for key, value in result.items():
                    if key.startswith('sub-'):
                        print(f"    {key}: '{value}'")
                
                print(f"  📋 メタ情報: {result.get('metadata', {})}")
                
                # パターン確認
                expected = test_case['expected_pattern']
                actual = result.get('tense_type')
                if expected == actual:
                    print(f"  ✅ パターン確認: {actual}")
                else:
                    print(f"  ❌ パターン不一致: 期待={expected}, 実際={actual}")
            
            else:
                print("❌ 処理失敗: 結果が空です")
                
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n📝 サブスロット専用処理テスト")
    print("=" * 50)
    
    subslot_tests = [
        {
            'name': 'サブスロット倒置1',
            'sentence': 'Never have I seen such beauty'
        },
        {
            'name': 'サブスロット倒置2', 
            'sentence': 'On the table lay a book'
        },
        {
            'name': 'サブスロット倒置3',
            'sentence': 'Had I known'
        }
    ]
    
    for i, test_case in enumerate(subslot_tests, 1):
        print(f"\n🔧 サブスロットテスト{i}: {test_case['name']}")
        print(f"入力: {test_case['sentence']}")
        
        try:
            result = engine.process_as_subslot(test_case['sentence'])
            print("✅ サブスロット処理成功:")
            for key, value in result.items():
                print(f"    {key}: '{value}'")
        except Exception as e:
            print(f"❌ サブスロット処理エラー: {e}")
    
    print("\n📝 統合例テスト: 接続詞 + 倒置")
    print("=" * 50)
    
    # 統合例のシミュレーション
    complex_sentence = "Because never had he seen such beauty, he was amazed."
    subordinate_clause = "never had he seen such beauty"
    
    print(f"完全文: {complex_sentence}")
    print(f"従属節: {subordinate_clause}")
    
    try:
        subslot_result = engine.process_as_subslot(subordinate_clause)
        print("🎯 接続詞節内倒置のサブスロット分解:")
        for key, value in subslot_result.items():
            print(f"  {key}: '{value}'")
        
        print(f"\n📊 統合結果想定:")
        print(f"  上位: M1='Because never had he seen such beauty'")
        print(f"  上位: S='he', V='was', C1='amazed'")
        print(f"  サブ: sub-s='{subslot_result.get('sub-s', '')}', sub-aux='{subslot_result.get('sub-aux', '')}', sub-v='{subslot_result.get('sub-v', '')}', sub-m1='{subslot_result.get('sub-m1', '')}'")
        
    except Exception as e:
        print(f"❌ 統合テストエラー: {e}")
    
    print(f"\n🎉 倒置構文エンジン テスト完了")

if __name__ == "__main__":
    test_inversion_engine()
