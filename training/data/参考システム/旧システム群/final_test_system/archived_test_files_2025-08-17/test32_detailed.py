#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os

# 親ディレクトリのパスを追加
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_32_detailed():
    # テストデータの読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Test32のデータを取得
    test_case = test_data['data']['32']  # JSONの構造に合わせて修正
    sentence = test_case['sentence']  # 'text'ではなく'sentence'
    expected = test_case['expected']
    
    print(f"Test32: {sentence}")
    print(f"期待値: {expected}")
    print()
    
    # システムの実行
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process(sentence)  # process_sentence -> process
    
    print(f"システム結果: {result}")
    print()
    
    # 詳細比較
    main_expected = expected['main_slots']
    sub_expected = expected['sub_slots']
    
    # システム結果の構造を理解して抽出
    main_result = result.get('slots', {})  # 主節はslotsキー内
    sub_result = result.get('sub_slots', {})  # 従属節はsub_slotsキー内
    
    print("=== 主節比較 ===")
    print(f"期待値: {main_expected}")
    print(f"システム: {main_result}")
    main_match = (main_result == main_expected)
    print(f"主節一致: {main_match}")
    print()
    
    print("=== 従属節比較 ===")
    print(f"期待値: {sub_expected}")
    print(f"システム: {sub_result}")
    sub_match = (sub_result == sub_expected)
    print(f"従属節一致: {sub_match}")
    
    # 不一致の詳細
    if not sub_match:
        print("\n従属節の不一致詳細:")
        for key in set(list(sub_expected.keys()) + list(sub_result.keys())):
            exp_val = sub_expected.get(key, "MISSING")
            sys_val = sub_result.get(key, "MISSING")
            match_status = "✅" if exp_val == sys_val else "❌"
            print(f"  {key}: 期待値='{exp_val}' システム='{sys_val}' {match_status}")
    
    print()
    
    # 総合判定
    if main_match and sub_match:
        print("結果: PERFECT ✅")
        return True
    elif main_match:
        print("結果: PARTIAL ⚠️ (主節のみ一致)")
        return False
    else:
        print("結果: FAILED ❌")
        return False

if __name__ == "__main__":
    test_32_detailed()
