#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
個別システム（Step10-13）の精密ロジック分析
各スロット専用システムから優秀な分解ロジックを抽出
"""

import sys
sys.path.append('./archive')

def analyze_individual_systems():
    """個別システムの分解ロジック分析"""
    print("🔍 個別システム分解ロジック分析")
    print("=" * 80)
    
    # 各個別システムのテストケースと期待結果
    test_cases = {
        "step12_s_subslot": {
            "class": "SSubslotGenerator",
            "method": "generate_s_subslots", 
            "test_data": [
                ("the woman who seemed indecisive", "phrase"),
                ("the intelligent student", "phrase")
            ],
            "expected_patterns": ["主語部分の正確な抽出", "関係代名詞節処理"]
        },
        "step13_o1_subslot": {
            "class": "O1SubslotGenerator", 
            "method": "generate_o1_subslots",
            "test_data": [
                ("that he had been trying to avoid Tom", "clause"),
                ("English very hard", "phrase")
            ],
            "expected_patterns": ["that節処理", "複合目的語処理"]
        },
        "step10_c1_subslot": {
            "class": "C1SubslotGenerator",
            "method": "generate_c1_subslots", 
            "test_data": [
                ("indecisive", "word"),
                ("very experienced", "phrase")
            ],
            "expected_patterns": ["形容詞補語処理", "修飾付き補語処理"]
        },
        "step11_c2_subslot": {
            "class": "C2SubslotGenerator",
            "method": "generate_c2_subslots",
            "test_data": [
                ("confident that he will succeed", "clause"),
            ],
            "expected_patterns": ["that節補語処理"]
        }
    }
    
    individual_results = {}
    
    for module_name, config in test_cases.items():
        print(f"\n{'='*60}")
        print(f"🧪 {module_name} 詳細分析")
        print(f"期待パターン: {', '.join(config['expected_patterns'])}")
        print(f"{'='*60}")
        
        try:
            # 動的インポート
            module = __import__(module_name)
            generator_class = getattr(module, config["class"])
            generator = generator_class()
            method = getattr(generator, config["method"])
            
            module_results = []
            
            for test_phrase, phrase_type in config["test_data"]:
                print(f"\n📋 テスト: '{test_phrase}' ({phrase_type})")
                
                try:
                    result = method(test_phrase, phrase_type)
                    
                    if isinstance(result, dict):
                        print(f"   ✅ 分解結果数: {len(result)}")
                        for sub_type, sub_data in result.items():
                            if isinstance(sub_data, dict):
                                text = sub_data.get('text', str(sub_data)[:30])
                                tokens = sub_data.get('tokens', [])
                                indices = sub_data.get('token_indices', [])
                                print(f"   🎯 {sub_type}: '{text}'")
                                print(f"      tokens: {tokens}")
                                print(f"      indices: {indices}")
                            else:
                                print(f"   🎯 {sub_type}: '{sub_data}'")
                        
                        module_results.append({
                            'input': test_phrase,
                            'type': phrase_type,
                            'output': result,
                            'success': len(result) > 0
                        })
                    else:
                        print(f"   ⚠️ 予期しない結果タイプ: {type(result)}")
                        
                except Exception as e:
                    print(f"   ❌ エラー: {str(e)}")
                    module_results.append({
                        'input': test_phrase,
                        'type': phrase_type,
                        'error': str(e),
                        'success': False
                    })
            
            individual_results[module_name] = {
                'results': module_results,
                'success_count': sum(1 for r in module_results if r.get('success', False))
            }
            
            print(f"\n🎯 {module_name} 成功: {individual_results[module_name]['success_count']}/{len(config['test_data'])}")
            
        except Exception as e:
            print(f"❌ {module_name} モジュールエラー: {str(e)}")
            individual_results[module_name] = {'error': str(e)}
    
    # 優秀なロジック特定
    print(f"\n{'='*80}")
    print("🏆 優秀ロジック特定")
    print(f"{'='*80}")
    
    best_modules = []
    for module_name, results in individual_results.items():
        if 'error' not in results and results.get('success_count', 0) > 0:
            success_rate = results['success_count'] / len(test_cases[module_name]['test_data'])
            print(f"🎯 {module_name}: 成功率 {success_rate:.1%}")
            if success_rate > 0.5:  # 50%以上
                best_modules.append(module_name)
    
    print(f"\n🏆 抽出すべき優秀ロジック: {', '.join(best_modules)}")
    
    return individual_results, best_modules

if __name__ == "__main__":
    analyze_individual_systems()
