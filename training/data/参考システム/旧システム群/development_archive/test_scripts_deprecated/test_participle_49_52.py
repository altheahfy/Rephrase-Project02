#!/usr/bin/env python3
"""
分詞構文Cases 49-52 の個別確認テスト
一括テストに問題があるかもしれないので、個別にテスト
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_participle_cases():
    """Cases 49-52の個別テスト"""
    
    # テストデータ読み込み
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    results = {}
    success_count = 0
    total_count = 0
    
    # Mapper初期化（一度だけ）
    mapper = UnifiedStanzaRephraseMapper()
    
    # Cases 49-52をテスト
    for case_id in ['49', '50', '51', '52']:
        if case_id not in test_data['data']:
            print(f"❌ Case {case_id} がデータに見つかりません")
            continue
            
        case_data = test_data['data'][case_id]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        print(f"\n=== Case {case_id} ===")
        print(f"入力: {sentence}")
        
        # 処理実行
        result = mapper.process(sentence)
        
        # 比較
        main_match = result.get('main_slots', {}) == expected['main_slots']
        sub_match = result.get('sub_slots', {}) == expected['sub_slots']
        overall_match = main_match and sub_match
        
        total_count += 1
        if overall_match:
            success_count += 1
            results[case_id] = "✅ 成功"
            print(f"✅ 完全一致！")
        else:
            results[case_id] = "❌ 失敗"
            print(f"❌ 不一致")
            print(f"  期待 main: {expected['main_slots']}")
            print(f"  実際 main: {result.get('main_slots', {})}")
            print(f"  期待 sub:  {expected['sub_slots']}")
            print(f"  実際 sub:  {result.get('sub_slots', {})}")
    
    # 結果サマリー
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    print(f"\n=== 分詞構文テスト結果 ===")
    print(f"成功率: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    for case_id, status in results.items():
        print(f"  Case {case_id}: {status}")
    
    return success_rate

if __name__ == "__main__":
    test_participle_cases()
