#!/usr/bin/env python3
"""
Case 53 詳細デバッグスクリプト
関係詞節の処理確認
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_case_53():
    # テストデータ読み込み
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    case_53 = test_data['data']['53']
    sentence = case_53['sentence']
    expected = case_53['expected']
    
    print("=== Case 53 詳細デバッグ ===")
    print(f"入力: {sentence}")
    
    # Mapper初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    # 処理実行
    result = mapper.process(sentence)
    
    print(f"\n結果詳細:")
    print(f"  Main slots: {result.get('main_slots', {})}")
    print(f"  Sub slots: {result.get('sub_slots', {})}")
    print(f"  Patterns: {result.get('patterns_applied', [])}")
    
    # 比較
    print(f"\n比較:")
    print(f"  期待 main: {expected['main_slots']}")
    print(f"  実際 main: {result.get('main_slots', {})}")
    print(f"  期待 sub:  {expected['sub_slots']}")
    print(f"  実際 sub:  {result.get('sub_slots', {})}")
    
    # 差異チェック
    main_match = result.get('main_slots', {}) == expected['main_slots']
    sub_match = result.get('sub_slots', {}) == expected['sub_slots']
    
    if main_match and sub_match:
        print(f"\n✅ 完全一致！")
        return True
    else:
        print(f"\n問題点:")
        if not main_match:
            for key in set(list(expected['main_slots'].keys()) + list(result.get('main_slots', {}).keys())):
                exp_val = expected['main_slots'].get(key)
                act_val = result.get('main_slots', {}).get(key)
                if exp_val != act_val:
                    print(f"  ❌ {key}不一致: 期待'{exp_val}' != 実際'{act_val}'")
        
        if not sub_match:
            for key in set(list(expected['sub_slots'].keys()) + list(result.get('sub_slots', {}).keys())):
                exp_val = expected['sub_slots'].get(key)
                act_val = result.get('sub_slots', {}).get(key)
                if exp_val != act_val:
                    print(f"  ❌ {key}不一致: 期待'{exp_val}' != 実際'{act_val}'")
        
        return False

if __name__ == "__main__":
    debug_case_53()
