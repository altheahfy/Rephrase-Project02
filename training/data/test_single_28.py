#!/usr/bin/env python3
"""
Test 28 単独実行
接続詞ハンドラーの人間文法認識システムの動作確認
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_single_case():
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    # Test 28: 接続詞構文
    sentence = "She acts as if she knows everything."
    print(f"テスト文: {sentence}")
    
    # 解析実行
    result = mapper.process(sentence)
    
    print(f"解析結果:")
    print(f"  主節: {result.get('slots', {})}")
    print(f"  従属節: {result.get('sub_slots', {})}")
    
    # 期待値
    expected_main = {"S": "She", "V": "acts", "M2": ""}
    expected_sub = {"sub-m2": "as if", "sub-s": "she", "sub-v": "knows", "sub-o1": "everything"}
    
    print(f"期待値:")
    print(f"  主節: {expected_main}")
    print(f"  従属節: {expected_sub}")
    
    # 比較
    actual_main = result.get('slots', {})
    actual_sub = result.get('sub_slots', {})
    
    main_match = actual_main == expected_main
    sub_match = actual_sub == expected_sub
    
    print(f"比較結果:")
    print(f"  主節一致: {main_match}")
    print(f"  従属節一致: {sub_match}")
    print(f"  完全一致: {main_match and sub_match}")
    
    if not sub_match:
        print("従属節不一致詳細:")
        for key in set(expected_sub.keys()) | set(actual_sub.keys()):
            exp_val = expected_sub.get(key, "(not present)")
            act_val = actual_sub.get(key, "(not present)")
            match = "✅" if exp_val == act_val else "❌"
            print(f"  {key}: 期待=\"{exp_val}\" 実際=\"{act_val}\" {match}")

if __name__ == "__main__":
    test_single_case()
