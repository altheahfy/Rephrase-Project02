#!/usr/bin/env python3
"""
システム出力と正解データベースの詳細比較
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def load_expected_results():
    """正解データベース読み込み"""
    with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    expected_results = {}
    for key, value in data['correct_answers'].items():
        expected_results[int(key)] = {
            'sentence': value['sentence'],
            'expected': value.get('expected', {}),
            'main_slots': value.get('expected', {}).get('main_slots', {}),
            'sub_slots': value.get('expected', {}).get('sub_slots', {})
        }
    
    return expected_results

def compare_results():
    """システム出力と正解の詳細比較"""
    print("🔍 システム出力と正解データベースの詳細比較")
    print("="*60)
    
    # 正解データ読み込み
    expected_results = load_expected_results()
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='WARNING')  # ログを抑制
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    total_tests = 0
    perfect_matches = 0
    main_slot_matches = 0
    sub_slot_matches = 0
    
    for test_id in sorted(expected_results.keys()):
        expected = expected_results[test_id]
        sentence = expected['sentence']
        expected_main = expected['main_slots']
        expected_sub = expected['sub_slots']
        
        # システム実行
        result = mapper.process(sentence)
        actual_main = result.get('slots', {})
        actual_sub = result.get('sub_slots', {})
        
        total_tests += 1
        
        # メインスロット比較
        main_match = (actual_main == expected_main)
        if main_match:
            main_slot_matches += 1
        
        # サブスロット比較
        sub_match = (actual_sub == expected_sub)
        if sub_match:
            sub_slot_matches += 1
        
        # 完全一致チェック
        perfect_match = main_match and sub_match
        if perfect_match:
            perfect_matches += 1
        
        # 不一致の場合は詳細表示
        if not perfect_match:
            print(f"\n❌ テスト{test_id}: {sentence}")
            print("  【メインスロット】")
            print(f"    期待: {expected_main}")
            print(f"    実際: {actual_main}")
            print(f"    一致: {'✅' if main_match else '❌'}")
            
            print("  【サブスロット】")
            print(f"    期待: {expected_sub}")
            print(f"    実際: {actual_sub}")
            print(f"    一致: {'✅' if sub_match else '❌'}")
        else:
            print(f"✅ テスト{test_id}: 完全一致")
    
    # 統計表示
    print(f"\n📊 最終統計:")
    print(f"  総テスト数: {total_tests}")
    print(f"  完全一致: {perfect_matches}/{total_tests} ({perfect_matches/total_tests*100:.1f}%)")
    print(f"  メインスロット一致: {main_slot_matches}/{total_tests} ({main_slot_matches/total_tests*100:.1f}%)")
    print(f"  サブスロット一致: {sub_slot_matches}/{total_tests} ({sub_slot_matches/total_tests*100:.1f}%)")
    
    if perfect_matches == total_tests:
        print("\n🎉 全テスト完全一致！システム完成です！")
    else:
        print(f"\n🔧 {total_tests - perfect_matches}件の不一致があります。修正が必要です。")

if __name__ == "__main__":
    compare_results()
