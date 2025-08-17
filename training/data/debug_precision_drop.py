#!/usr/bin/env python3
"""
精度低下の詳細分析スクリプト
69.8% → 目標85%への改善戦略
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def analyze_precision_drop():
    """精度低下の原因を詳細分析"""
    
    # テストデータ読み込み
    with open('batch_results_complete.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_results = data['results']
    mapper = UnifiedStanzaRephraseMapper()
    
    # 問題カテゴリ別分析
    adverb_issues = []
    subject_issues = []
    whose_issues = []
    prep_phrase_issues = []
    
    print("🔍 精度低下原因の詳細分析")
    print("=" * 50)
    
    for case_id in sorted(test_results.keys(), key=int)[:53]:
        case = test_results[case_id]
        sentence = case['sentence']
        expected_main = case['expected']['main_slots']
        expected_sub = case['expected']['sub_slots']
        
        # 期待値を統合
        expected = {}
        expected.update(expected_main)
        expected.update(expected_sub)
        
        try:
            result = mapper.process_sentence(sentence)
            
            # 各スロットの比較
            mismatch_details = []
            
            for slot_key in expected:
                if slot_key not in result or result[slot_key] != expected[slot_key]:
                    mismatch_details.append({
                        'slot': slot_key,
                        'expected': expected[slot_key],
                        'actual': result.get(slot_key, '')
                    })
            
            if mismatch_details:
                case_info = {
                    'case': int(case_id),
                    'sentence': sentence,
                    'mismatches': mismatch_details
                }
                
                # カテゴリ分類
                for mismatch in mismatch_details:
                    slot = mismatch['slot']
                    expected_val = str(mismatch['expected']).lower()
                    actual_val = str(mismatch['actual']).lower()
                    
                    if 'M' in slot or 'Adv' in slot:  # 副詞関連
                        adverb_issues.append(case_info)
                        break
                    elif slot == 'S' or 'sub-s' in slot:  # 主語関連
                        subject_issues.append(case_info)
                        break
                    elif 'whose' in expected_val or 'whose' in actual_val:  # whose構文
                        whose_issues.append(case_info)
                        break
                    elif 'by ' in expected_val or 'by ' in actual_val:  # 前置詞句
                        prep_phrase_issues.append(case_info)
                        break
        
        except Exception as e:
            print(f"❌ Case {case_id} エラー: {e}")
    
    # 結果表示
    print(f"\n📊 問題カテゴリ別分析")
    print(f"🔸 副詞配置問題: {len(adverb_issues)} ケース")
    print(f"🔸 主語検出問題: {len(subject_issues)} ケース") 
    print(f"🔸 whose構文問題: {len(whose_issues)} ケース")
    print(f"🔸 前置詞句問題: {len(prep_phrase_issues)} ケース")
    
    # 最も影響の大きい問題を特定
    print(f"\n🎯 優先修正対象（副詞配置問題）:")
    for case in adverb_issues[:5]:  # 上位5ケース
        print(f"Case {case['case']}: {case['sentence']}")
        for mismatch in case['mismatches']:
            print(f"  {mismatch['slot']}: '{mismatch['actual']}' ≠ '{mismatch['expected']}'")
        print()
    
    return {
        'adverb_issues': len(adverb_issues),
        'subject_issues': len(subject_issues),
        'whose_issues': len(whose_issues),
        'prep_phrase_issues': len(prep_phrase_issues),
        'total_issues': len(adverb_issues) + len(subject_issues) + len(whose_issues) + len(prep_phrase_issues)
    }

if __name__ == "__main__":
    try:
        results = analyze_precision_drop()
        print(f"\n📈 改善見込み:")
        print(f"副詞問題解決で +{results['adverb_issues']*1.9:.1f}% 向上期待")
        print(f"全問題解決で +{results['total_issues']*1.9:.1f}% 向上期待")
        print(f"目標精度 85% まで残り: {85 - 69.8:.1f}%")
        
    except Exception as e:
        print(f"❌ 分析エラー: {e}")
        import traceback
        traceback.print_exc()
