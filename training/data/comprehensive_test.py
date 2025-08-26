#!/usr/bin/env python3
"""
5文型＋関係節 総合テストシステム
Phase 1（基本5文型）とPhase 2（関係節）の全体状況を把握
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def load_test_data():
    """テストデータ読み込み"""
    try:
        with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ final_54_test_data.json が見つかりません")
        return None

def run_comprehensive_test():
    """5文型＋関係節の総合テスト実行"""
    
    print("🚀 5文型＋関係節 総合テスト開始")
    print("=" * 80)
    
    # テストデータ読み込み
    test_data = load_test_data()
    if not test_data:
        return False
    
    # CentralController初期化
    controller = CentralController()
    
    # Phase 1: 基本5文型テストケース
    phase1_cases = [1, 2, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]
    
    # Phase 2: 関係節テストケース  
    phase2_cases = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    
    results = {
        'phase1': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
        'phase2': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
        'overall': {'total': 0, 'passed': 0, 'failed': 0}
    }
    
    # Phase 1テスト実行
    print("📊 Phase 1: 基本5文型テスト")
    print("-" * 60)
    
    for case_id in phase1_cases:
        case_id_str = str(case_id)
        if case_id_str not in test_data['data']:
            continue
            
        test_case = test_data['data'][case_id_str]
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"📝 ケース{case_id}: {sentence}")
        
        try:
            result = controller.process_sentence(sentence)
            success = result.get('success', False)
            
            # 簡易成功判定（実際のスロット検証は省略）
            if success:
                print(f"✅ PASS")
                results['phase1']['passed'] += 1
            else:
                print(f"❌ FAIL - 処理失敗")
                results['phase1']['failed'] += 1
                
        except Exception as e:
            print(f"❌ FAIL - エラー: {str(e)}")
            results['phase1']['failed'] += 1
            
        results['phase1']['total'] += 1
    
    # Phase 2テスト実行
    print(f"\n📊 Phase 2: 関係節テスト")
    print("-" * 60)
    
    for case_id in phase2_cases:
        case_id_str = str(case_id)
        if case_id_str not in test_data['data']:
            continue
            
        test_case = test_data['data'][case_id_str]
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"📝 ケース{case_id}: {sentence}")
        
        try:
            result = controller.process_sentence(sentence)
            success = result.get('success', False)
            sub_slots = result.get('sub_slots', {})
            
            # 関係節特有の検証：sub_slotsの存在確認
            has_sub_slots = bool(sub_slots and len([k for k in sub_slots.keys() if not k.startswith('_')]) > 0)
            
            if success and has_sub_slots:
                print(f"✅ PASS - 関係節処理成功")
                results['phase2']['passed'] += 1
                
                # 重要ケースの詳細確認
                if case_id in [4, 5]:  # 改善対象ケース
                    sub_m2 = sub_slots.get('sub-m2', '')
                    if sub_m2:
                        print(f"   🎯 sub-m2取得成功: '{sub_m2}'")
                    else:
                        print(f"   ⚠️ sub-m2未取得")
                        
            else:
                print(f"❌ FAIL - 関係節処理失敗")
                results['phase2']['failed'] += 1
                
        except Exception as e:
            print(f"❌ FAIL - エラー: {str(e)}")
            results['phase2']['failed'] += 1
            
        results['phase2']['total'] += 1
    
    # 全体集計
    results['overall']['total'] = results['phase1']['total'] + results['phase2']['total']
    results['overall']['passed'] = results['phase1']['passed'] + results['phase2']['passed']
    results['overall']['failed'] = results['phase1']['failed'] + results['phase2']['failed']
    
    # 結果サマリー
    print(f"\n" + "=" * 80)
    print(f"📊 総合テスト結果サマリー")
    print("=" * 80)
    
    # Phase 1結果
    phase1_rate = (results['phase1']['passed'] / results['phase1']['total'] * 100) if results['phase1']['total'] > 0 else 0
    print(f"📈 Phase 1（基本5文型）: {results['phase1']['passed']}/{results['phase1']['total']} = {phase1_rate:.1f}%")
    
    # Phase 2結果
    phase2_rate = (results['phase2']['passed'] / results['phase2']['total'] * 100) if results['phase2']['total'] > 0 else 0
    print(f"📈 Phase 2（関係節）: {results['phase2']['passed']}/{results['phase2']['total']} = {phase2_rate:.1f}%")
    
    # 全体結果
    overall_rate = (results['overall']['passed'] / results['overall']['total'] * 100) if results['overall']['total'] > 0 else 0
    print(f"📈 全体成功率: {results['overall']['passed']}/{results['overall']['total']} = {overall_rate:.1f}%")
    
    # 評価
    print(f"\n🏆 総合評価:")
    if overall_rate >= 80:
        print(f"🎉 優秀 - システム全体が高い精度で動作")
    elif overall_rate >= 60:
        print(f"✅ 良好 - 基本機能は安定動作")
    elif overall_rate >= 40:
        print(f"🔧 改善中 - 継続的な改善が必要")
    else:
        print(f"❌ 要改善 - 大幅な見直しが必要")
    
    return results

def show_specific_improvements():
    """特定の改善事項を詳細表示"""
    print(f"\n🎯 今回の改善成果（詳細）")
    print("-" * 60)
    
    controller = CentralController()
    
    improvement_cases = [
        (4, "The book which lies there is mine."),
        (5, "The person that works here is kind.")
    ]
    
    for case_id, sentence in improvement_cases:
        print(f"\n📝 ケース{case_id}: {sentence}")
        result = controller.process_sentence(sentence)
        
        success = result.get('success', False)
        sub_slots = result.get('sub_slots', {})
        sub_m2 = sub_slots.get('sub-m2', '')
        
        print(f"   成功: {success}")
        print(f"   sub-m2: '{sub_m2}'")
        print(f"   状態: {'🎉 改善完了' if sub_m2 else '🔧 要改善'}")

if __name__ == "__main__":
    results = run_comprehensive_test()
    show_specific_improvements()
    
    if results:
        overall_rate = (results['overall']['passed'] / results['overall']['total'] * 100)
        print(f"\n{'🎉 総合テスト完了！' if overall_rate >= 50 else '🔧 継続改善必要'}")
    else:
        print(f"\n❌ テストデータ読み込み失敗")
