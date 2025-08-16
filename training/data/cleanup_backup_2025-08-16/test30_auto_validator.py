#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test30自動検証スクリプト
階層的解析アプローチ（Stanza → spaCy → Rephrase独自ルール）の結果を自動チェック
"""

import json
from unified_stanza_rephrase_mapper import UnifiedMapper

def test30_auto_validation():
    """Test30の自動検証"""
    
    # 期待結果定義
    expected = {
        "main_slots": {
            "S": "",  # 関係節により空
            "V": "is",
            "C2": "in Tokyo"
        },
        "sub_slots": {
            "sub-m3": "The house where",
            "sub-s": "I", 
            "sub-aux": "was",
            "sub-v": "born"
        }
    }
    
    # テスト実行
    sentence = "The house where I was born is in Tokyo."
    
    print(f"🧪 Test30自動検証開始")
    print(f"📝 文章: {sentence}")
    print(f"🎯 期待結果:")
    print(f"   Main slots: {expected['main_slots']}")
    print(f"   Sub slots: {expected['sub_slots']}")
    print("="*50)
    
    try:
        # Unified Mapper実行
        mapper = UnifiedMapper()
        mapper.add_handler('basic_five_pattern')
        mapper.add_handler('relative_clause')
        mapper.add_handler('adverbial_modifier')
        
        result = mapper.process(sentence)
        
        # 結果抽出
        actual_main = result.get('slots', {})
        actual_sub = result.get('sub_slots', {})
        
        print(f"🔍 実際の結果:")
        print(f"   Main slots: {actual_main}")
        print(f"   Sub slots: {actual_sub}")
        print("="*50)
        
        # 検証実行
        validation_results = []
        
        # メインスロット検証
        for slot, expected_value in expected['main_slots'].items():
            actual_value = actual_main.get(slot, "MISSING")
            is_correct = actual_value == expected_value
            validation_results.append({
                'type': 'main_slot',
                'slot': slot,
                'expected': expected_value,
                'actual': actual_value,
                'correct': is_correct
            })
            
        # サブスロット検証
        for slot, expected_value in expected['sub_slots'].items():
            actual_value = actual_sub.get(slot, "MISSING")
            is_correct = actual_value == expected_value
            validation_results.append({
                'type': 'sub_slot', 
                'slot': slot,
                'expected': expected_value,
                'actual': actual_value,
                'correct': is_correct
            })
        
        # 結果レポート
        print(f"📊 検証結果:")
        total_tests = len(validation_results)
        passed_tests = sum(1 for r in validation_results if r['correct'])
        
        for result in validation_results:
            status = "✅ PASS" if result['correct'] else "❌ FAIL"
            print(f"   {status} {result['type']} '{result['slot']}': '{result['actual']}' (期待: '{result['expected']}')")
        
        print("="*50)
        print(f"🏆 総合結果: {passed_tests}/{total_tests} テスト通過")
        
        if passed_tests == total_tests:
            print("🎉 All tests PASSED! 階層的解析アプローチ完璧！")
            return True
        else:
            print(f"⚠️  {total_tests - passed_tests} tests FAILED. 修正が必要です。")
            
            # 失敗詳細
            print("\n🔧 修正が必要な項目:")
            for result in validation_results:
                if not result['correct']:
                    print(f"   - {result['slot']}: '{result['actual']}' → '{result['expected']}'")
            
            return False
            
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test30_auto_validation()
    exit(0 if success else 1)
