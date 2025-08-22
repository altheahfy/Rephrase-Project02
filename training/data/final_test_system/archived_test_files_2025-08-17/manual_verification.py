#!/usr/bin/env python3
"""
Manual Verification - 手動チェックツール
比較ツールとは独立してシステム出力の正確性を検証
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def manual_check():
    """手動検証"""
    print("🔧 手動検証開始...")
    
    # 期待値データ読み込み
    with open('../final_54_test_data.json', 'r', encoding='utf-8') as f:
        expected_data = json.load(f)
    
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    
    # 手動検証対象（比較ツールで失敗と報告された例文）
    test_ids = ["1", "2", "20", "21"]
    
    for test_id in test_ids:
        print(f"\n{'='*60}")
        print(f"📖 Test[{test_id}]手動検証")
        
        expected_entry = expected_data["data"][test_id]
        sentence = expected_entry["sentence"]
        expected = expected_entry["expected"]
        
        print(f"文: '{sentence}'")
        
        # システム処理
        result = mapper.process(sentence)
        actual_main = result.get('slots', {})
        actual_sub = result.get('sub_slots', {})
        
        expected_main = expected.get('main_slots', {})
        expected_sub = expected.get('sub_slots', {})
        
        print(f"\n期待主節: {expected_main}")
        print(f"実際主節: {actual_main}")
        
        print(f"\n期待従属: {expected_sub}")
        print(f"実際従属: {actual_sub}")
        
        # 手動比較
        main_match = True
        sub_match = True
        
        for key, expected_val in expected_main.items():
            actual_val = actual_main.get(key, '')
            if actual_val != expected_val:
                main_match = False
                print(f"❌ 主節不一致: {key} '{actual_val}' ≠ '{expected_val}'")
        
        for key, expected_val in expected_sub.items():
            actual_val = actual_sub.get(key, '')
            if actual_val != expected_val:
                sub_match = False
                print(f"❌ 従属節不一致: {key} '{actual_val}' ≠ '{expected_val}'")
        
        if main_match and sub_match:
            print("✅ 手動検証: 完全一致")
        elif main_match:
            print("⚠️ 手動検証: 主節のみ一致")
        else:
            print("❌ 手動検証: 不一致あり")

if __name__ == "__main__":
    manual_check()
