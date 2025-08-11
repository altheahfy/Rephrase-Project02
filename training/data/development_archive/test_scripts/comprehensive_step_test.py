#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全stepの総合分解精度比較テスト
どのバージョンが最も正しい分解を実現しているかを特定
"""

import sys
sys.path.append('./archive')

def comprehensive_accuracy_test():
    """全stepの総合分解精度テスト"""
    print("🔍 全Step総合分解精度比較テスト")
    print("=" * 80)
    
    # 多様なテストケース
    test_cases = [
        ("S", "the woman who seemed indecisive"),
        ("M1", "this morning"),
        ("O1", "that he had been trying to avoid Tom"),
        ("M3", "because he was afraid of hurting her feelings"),
        ("S", "the intelligent student"),
        ("O1", "English very hard"),
        ("M2", "in the library")
    ]
    
    steps_to_test = [
        ("step7_final_subslot", "FinalSubslotGenerator", "generate_subslots_for_slot_phrase"),
        ("step12_s_subslot", "SSubslotGenerator", "generate_s_subslots"), 
        ("step13_o1_subslot", "O1SubslotGenerator", "generate_o1_subslots"),
        ("step14_universal_subslot", "UniversalSubslotGenerator", "generate_subslots_for_slot"),
        ("step15_enhanced_universal", "EnhancedUniversalSubslotGenerator", "generate_subslots_for_slot")
    ]
    
    results = {}
    
    for module_name, class_name, method_name in steps_to_test:
        print(f"\n{'='*60}")
        print(f"🧪 {module_name} テスト")
        print(f"{'='*60}")
        
        try:
            # 動的インポート
            module = __import__(module_name)
            generator_class = getattr(module, class_name)
            generator = generator_class()
            method = getattr(generator, method_name)
            
            step_results = []
            total_subslots = 0
            
            for slot_name, phrase in test_cases:
                print(f"\n📋 {slot_name}: '{phrase}'")
                
                try:
                    # メソッド呼び出し（パラメータはstepによって異なる）
                    if "step7" in module_name:
                        result = method(phrase, "clause")
                        subslots = result.get('subslots', {}) if isinstance(result, dict) else {}
                    elif "step12" in module_name or "step13" in module_name:
                        if (slot_name == "S" and "step12" in module_name) or (slot_name == "O1" and "step13" in module_name):
                            result = method(phrase, "phrase")
                        else:
                            continue  # このstepでは対象外
                        subslots = result if isinstance(result, dict) else {}
                    else:  # step14, step15
                        result = method(slot_name, phrase)
                        subslots = result if isinstance(result, dict) else {}
                    
                    print(f"   分解結果数: {len(subslots)}")
                    for sub_type, sub_data in subslots.items():
                        if isinstance(sub_data, dict) and 'text' in sub_data:
                            text = sub_data['text']
                        else:
                            text = str(sub_data)[:50]  # 長すぎる場合は切り詰め
                        print(f"   ✅ {sub_type}: '{text}'")
                    
                    step_results.append({
                        'slot': slot_name,
                        'phrase': phrase,
                        'subslot_count': len(subslots),
                        'subslots': subslots
                    })
                    total_subslots += len(subslots)
                    
                except Exception as e:
                    print(f"   ❌ エラー: {str(e)}")
                    step_results.append({
                        'slot': slot_name,
                        'phrase': phrase,
                        'subslot_count': 0,
                        'error': str(e)
                    })
            
            results[module_name] = {
                'total_subslots': total_subslots,
                'test_results': step_results,
                'success_rate': len([r for r in step_results if r['subslot_count'] > 0]) / len(step_results)
            }
            
            print(f"\n🎯 {module_name} 総合結果:")
            print(f"   総サブスロット数: {total_subslots}")
            print(f"   成功率: {results[module_name]['success_rate']:.1%}")
            
        except Exception as e:
            print(f"❌ {module_name} 全体エラー: {str(e)}")
            results[module_name] = {'error': str(e)}
    
    # 最終比較
    print(f"\n{'='*80}")
    print("🏆 最終比較結果")
    print(f"{'='*80}")
    
    best_step = None
    best_score = 0
    
    for step_name, step_result in results.items():
        if 'error' in step_result:
            print(f"❌ {step_name}: エラー")
            continue
            
        score = step_result['total_subslots'] * step_result['success_rate']
        print(f"🎯 {step_name}:")
        print(f"   総サブスロット数: {step_result['total_subslots']}")
        print(f"   成功率: {step_result['success_rate']:.1%}")
        print(f"   総合スコア: {score:.1f}")
        
        if score > best_score:
            best_score = score
            best_step = step_name
    
    if best_step:
        print(f"\n🏆 最優秀: {best_step} (スコア: {best_score:.1f})")
    else:
        print("\n⚠️ 有効な結果が得られませんでした")
    
    return results

if __name__ == "__main__":
    comprehensive_accuracy_test()
