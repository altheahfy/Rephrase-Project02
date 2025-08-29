#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CentralControllerでtellグループ分解テスト
"""

from central_controller import CentralController
import json

def test_tell_group_decomposition():
    """
    tellグループの例文をCentralControllerで分解
    """
    print("🎯 CentralController tellグループ分解テスト")
    print("=" * 60)
    
    controller = CentralController()
    
    # tellグループのテスト文
    test_sentences = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Did I tell him a truth in the kitchen?",
        "Where did you tell me a story?"
    ]
    
    decomposed_results = []
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📋 Case {i}: {sentence}")
        
        try:
            # CentralControllerで分解
            result = controller.decompose(sentence)
            
            print(f"✅ 分解成功:")
            print(f"   slots: {result.get('slots', {})}")
            print(f"   grammar_info: {result.get('grammar_info', {})}")
            print(f"   其他情報: {[(k, v) for k, v in result.items() if k not in ['slots', 'grammar_info']]}")
            
            decomposed_results.append({
                "sentence": sentence,
                "result": result
            })
            
        except Exception as e:
            print(f"❌ 分解エラー: {e}")
    
    # 結果をJSONで保存
    output_file = "tell_group_decomposed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(decomposed_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 結果を {output_file} に保存しました")
    return decomposed_results

if __name__ == "__main__":
    results = test_tell_group_decomposition()
