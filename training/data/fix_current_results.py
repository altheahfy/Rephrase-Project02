#!/usr/bin/env python3
"""
現在のaction_group_fixed_results.jsonを人間的判断で修正
"""

import json
from pathlib import Path

def fix_current_results():
    """現在の結果を人間的判断で修正"""
    print("🚀 現在の結果を人間的判断で修正開始")
    print("=" * 60)
    
    # 現在の結果をロード
    input_file = Path("action_group_fixed_results.json")
    with open(input_file, 'r', encoding='utf-8') as f:
        current_results = json.load(f)
    
    print("📋 修正前の結果:")
    for i, result in enumerate(current_results, 1):
        print(f"例文{i}: {result['sentence']}")
        print(f"現在の順序: {result['ordered_slots']}")
        
        # 現在の順序で語順を再構成
        ordered_words = []
        for pos in sorted(result['ordered_slots'].keys(), key=int):
            ordered_words.append(result['ordered_slots'][pos])
        print(f"現在の語順: {' '.join(ordered_words)}")
        print()
    
    # 修正ルールを適用
    fixed_results = []
    
    for result in current_results:
        sentence = result['sentence']
        current_slots = result['ordered_slots'].copy()
        
        print(f"🔧 修正中: {sentence}")
        
        # 修正ルール適用
        if sentence == "We always eat breakfast together.":
            # together を位置5→7に移動
            together_value = current_slots.pop('5')  # togetherを削除
            current_slots['7'] = together_value       # 位置7に移動
            print(f"  📝 together を位置5→7に移動")
            
        elif sentence == "She carefully reads books.":
            # carefully を位置5→3に移動
            carefully_value = current_slots.pop('5')  # carefullyを削除
            current_slots['3'] = carefully_value      # 位置3に移動
            print(f"  📝 carefully を位置5→3に移動")
            
        elif sentence == "Every morning, he jogs slowly in the park.":
            # in the park を位置7→8に移動
            park_value = current_slots.pop('7')       # in the parkを削除
            current_slots['8'] = park_value           # 位置8に移動
            print(f"  📝 in the park を位置7→8に移動")
        
        # 修正後の語順を確認
        ordered_words = []
        for pos in sorted(current_slots.keys(), key=int):
            ordered_words.append(current_slots[pos])
        print(f"  ✅ 修正後語順: {' '.join(ordered_words)}")
        
        fixed_result = {
            "sentence": sentence,
            "original_slots": result['original_slots'],
            "ordered_slots": current_slots
        }
        fixed_results.append(fixed_result)
        print()
    
    # 修正結果を保存
    output_file = Path("action_group_human_fixed_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_results, f, ensure_ascii=False, indent=2)
    
    print(f"💾 修正結果を {output_file} に保存しました")
    
    # 最終結果表示
    print("\n📊 最終修正結果:")
    print("=" * 60)
    for i, result in enumerate(fixed_results, 1):
        print(f"例文{i}: {result['sentence']}")
        
        # 順序通りの語順を表示
        ordered_words = []
        for pos in sorted(result['ordered_slots'].keys(), key=int):
            ordered_words.append(result['ordered_slots'][pos])
        
        print(f"修正後順序: {result['ordered_slots']}")
        print(f"修正後語順: {' '.join(ordered_words)}")
        print()
    
    return fixed_results

def main():
    fix_current_results()

if __name__ == "__main__":
    main()
