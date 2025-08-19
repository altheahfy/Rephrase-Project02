#!/usr/bin/env python3
"""
超シンプルルール検証スクリプト
期待値ファイルが超シンプルルールに準拠しているかチェック
"""

import json
import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def validate_simple_rule():
    print("🔍 超シンプルルール検証")
    print("=" * 60)
    
    # 期待値ファイル読み込み
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    data = test_data.get('data', {})
    mapper = UnifiedStanzaRephraseMapper()
    
    violations = []
    
    for case_id, case_data in data.items():
        sentence = case_data['sentence']
        expected_main = case_data['expected']['main_slots']
        expected_sub = case_data.get('expected', {}).get('sub_slots', {})
        
        # 実際の処理結果を取得
        result = mapper.process(sentence)
        actual_main = result.get('slots', {})
        actual_sub = result.get('sub_slots', {})
        
        # 主節Mスロットの個数チェック
        expected_m_slots = [slot for slot in ['M1', 'M2', 'M3'] if expected_main.get(slot)]
        actual_m_slots = [slot for slot in ['M1', 'M2', 'M3'] if actual_main.get(slot)]
        
        # 従属節Mスロットの個数チェック
        expected_sub_m_slots = [slot for slot in ['sub-m1', 'sub-m2', 'sub-m3'] if expected_sub.get(slot)]
        actual_sub_m_slots = [slot for slot in ['sub-m1', 'sub-m2', 'sub-m3'] if actual_sub.get(slot)]
        
        # 超シンプルルール検証
        def validate_slot_assignment(slots_dict, prefix=""):
            slot_names = [f"{prefix}M1", f"{prefix}M2", f"{prefix}M3"] if prefix else ['M1', 'M2', 'M3']
            used_slots = [slot for slot in slot_names if slots_dict.get(slot)]
            count = len(used_slots)
            
            if count == 0:
                return True, ""
            elif count == 1:
                # 1個 → M2のみ
                expected_slot = f"{prefix}M2" if prefix else "M2"
                if used_slots == [expected_slot]:
                    return True, ""
                else:
                    return False, f"1個ルール違反: {used_slots} ≠ [{expected_slot}]"
            elif count == 2:
                # 2個 → M2, M3
                expected_slots = [f"{prefix}M2", f"{prefix}M3"] if prefix else ["M2", "M3"]
                if used_slots == expected_slots:
                    return True, ""
                else:
                    return False, f"2個ルール違反: {used_slots} ≠ {expected_slots}"
            elif count == 3:
                # 3個 → M1, M2, M3
                expected_slots = [f"{prefix}M1", f"{prefix}M2", f"{prefix}M3"] if prefix else ["M1", "M2", "M3"]
                if used_slots == expected_slots:
                    return True, ""
                else:
                    return False, f"3個ルール違反: {used_slots} ≠ {expected_slots}"
            else:
                return False, f"4個以上エラー: {used_slots}"
        
        # 期待値の検証
        expected_valid, expected_error = validate_slot_assignment(expected_main)
        actual_valid, actual_error = validate_slot_assignment(actual_main)
        
        # 従属節の検証
        expected_sub_valid, expected_sub_error = validate_slot_assignment(expected_sub, "sub-")
        actual_sub_valid, actual_sub_error = validate_slot_assignment(actual_sub, "sub-")
        
        # 違反をチェック
        case_violations = []
        
        if not expected_valid:
            case_violations.append(f"期待値Main: {expected_error}")
        
        if not actual_valid:
            case_violations.append(f"実際Main: {actual_error}")
            
        if not expected_sub_valid:
            case_violations.append(f"期待値Sub: {expected_sub_error}")
            
        if not actual_sub_valid:
            case_violations.append(f"実際Sub: {actual_sub_error}")
        
        # Mスロット内容の違いも確認
        if expected_valid and actual_valid:
            main_diff = False
            for slot in ['M1', 'M2', 'M3']:
                if expected_main.get(slot, '') != actual_main.get(slot, ''):
                    main_diff = True
                    case_violations.append(f"Main {slot}: '{actual_main.get(slot, '')}' ≠ '{expected_main.get(slot, '')}'")
        
        if case_violations:
            violations.append({
                'case_id': case_id,
                'sentence': sentence,
                'violations': case_violations,
                'expected_main': expected_main,
                'actual_main': actual_main,
                'expected_sub': expected_sub,
                'actual_sub': actual_sub
            })
    
    # 結果出力
    print(f"\n📊 検証結果:")
    print(f"総ケース数: {len(data)}")
    print(f"ルール違反: {len(violations)}")
    
    if violations:
        print(f"\n❌ 超シンプルルール違反ケース:")
        for v in violations:
            print(f"\nCase {v['case_id']}: {v['sentence']}")
            for violation in v['violations']:
                print(f"  ⚠️ {violation}")
            
            # 推奨修正案
            if 'Main' in str(v['violations']):
                actual_m_count = len([s for s in ['M1', 'M2', 'M3'] if v['actual_main'].get(s)])
                print(f"  💡 修正案: 実際の出力({actual_m_count}個)が超シンプルルール準拠の可能性")
    else:
        print("✅ 全ケースが超シンプルルールに準拠")

if __name__ == "__main__":
    validate_simple_rule()
