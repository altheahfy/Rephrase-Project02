#!/usr/bin/env python3
"""
副詞配置精密化プロジェクト
========================

目的: 中央制御機構100%精度達成を受け、より複雑な文での副詞配置（M1, M2, M3）の精度向上
対象: 実際の語学学習文でのM1(50%), M2(62.5%), M3(37.5%)の精度向上

戦略:
1. 動詞からの距離ベース位置決定の精密化
2. 意味的修飾関係の考慮 
3. 前置詞句vs副詞の正確な分類

作成日: 2025年8月24日
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_grammar_mapper import DynamicGrammarMapper

# 副詞配置テストケース（実際の語学学習文から）
ADVERB_TEST_CASES = {
    # M1テスト: 動詞前副詞
    11: {
        'sentence': 'She quickly runs to school.',
        'expected_main': {'S': 'She', 'M1': 'quickly', 'V': 'runs', 'M2': 'to school'},
        'expected_sub': {}
    },
    12: {
        'sentence': 'He carefully opened the door.',
        'expected_main': {'S': 'He', 'M1': 'carefully', 'V': 'opened', 'O1': 'the door'},
        'expected_sub': {}
    },
    
    # M2テスト: 動詞直後副詞
    13: {
        'sentence': 'They work hard every day.',
        'expected_main': {'S': 'They', 'V': 'work', 'M2': 'hard', 'M3': 'every day'},
        'expected_sub': {}
    },
    14: {
        'sentence': 'The team played well yesterday.',
        'expected_main': {'S': 'The team', 'V': 'played', 'M2': 'well', 'M3': 'yesterday'},
        'expected_sub': {}
    },
    
    # M3テスト: 文末副詞・時間・場所
    15: {
        'sentence': 'We will meet at the station tomorrow.',
        'expected_main': {'S': 'We', 'Aux': 'will', 'V': 'meet', 'M2': 'at the station', 'M3': 'tomorrow'},
        'expected_sub': {}
    },
    16: {
        'sentence': 'The students studied in the library quietly.',
        'expected_main': {'S': 'The students', 'V': 'studied', 'M2': 'in the library', 'M3': 'quietly'},
        'expected_sub': {}
    },
    
    # 複合副詞テスト
    17: {
        'sentence': 'She very carefully examined the document thoroughly.',
        'expected_main': {'S': 'She', 'M1': 'very carefully', 'V': 'examined', 'O1': 'the document', 'M3': 'thoroughly'},
        'expected_sub': {}
    },
    18: {
        'sentence': 'The workers built the house quite slowly but efficiently.',
        'expected_main': {'S': 'The workers', 'V': 'built', 'O1': 'the house', 'M2': 'quite slowly but efficiently'},
        'expected_sub': {}
    }
}

def test_adverb_placement():
    """副詞配置テスト実行"""
    print("=== 副詞配置精密化テスト ===")
    print("中央制御機構での副詞配置精度検証")
    
    analyzer = DynamicGrammarMapper()
    
    total_tests = len(ADVERB_TEST_CASES)
    success_count = 0
    
    for test_num, test_case in ADVERB_TEST_CASES.items():
        sentence = test_case['sentence']
        expected_main = test_case['expected_main']
        expected_sub = test_case['expected_sub']
        
        print(f"\n=== Test {test_num}: {sentence} ===")
        
        try:
            result = analyzer.analyze_sentence(sentence)
            
            main_slots = result.get('main_slots', result.get('slots', {}))
            sub_slots = result.get('sub_slots', {})
            
            print(f"実際: main={main_slots}")
            print(f"期待: main={expected_main}")
            
            # 副詞配置の詳細分析
            m1_match = main_slots.get('M1') == expected_main.get('M1')
            m2_match = main_slots.get('M2') == expected_main.get('M2')
            m3_match = main_slots.get('M3') == expected_main.get('M3')
            
            other_slots_match = True
            for key in ['S', 'V', 'Aux', 'O1', 'O2', 'C1', 'C2']:
                if main_slots.get(key) != expected_main.get(key):
                    other_slots_match = False
                    break
            
            if m1_match and m2_match and m3_match and other_slots_match:
                print("✅ 副詞配置正解！")
                success_count += 1
            else:
                print("❌ 副詞配置不正解")
                if not m1_match:
                    print(f"  M1不一致: 実際='{main_slots.get('M1')}', 期待='{expected_main.get('M1')}'")
                if not m2_match:
                    print(f"  M2不一致: 実際='{main_slots.get('M2')}', 期待='{expected_main.get('M2')}'")
                if not m3_match:
                    print(f"  M3不一致: 実際='{main_slots.get('M3')}', 期待='{expected_main.get('M3')}'")
                if not other_slots_match:
                    print(f"  その他スロット不一致")
            
        except Exception as e:
            print(f"❌ エラー発生: {e}")
    
    print(f"\n=== 副詞配置テスト結果 ===")
    print(f"総テスト数: {total_tests}")
    print(f"成功: {success_count}/{total_tests}")
    print(f"副詞配置精度: {success_count/total_tests*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 副詞配置も完璧！")
    else:
        print(f"🔧 改善余地あり: 副詞配置ロジックの精密化が必要")
        return success_count / total_tests

if __name__ == "__main__":
    test_adverb_placement()
