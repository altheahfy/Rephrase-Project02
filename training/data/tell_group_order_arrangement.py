#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループの8要素を例文の語順で重複しないように配置
"""

def arrange_tell_group_elements():
    """tellグループの8要素を語順で配置"""
    
    # tellグループの8要素
    elements = ["Aux", "M2_normal", "M2_wh", "O1", "O2_normal", "O2_wh", "S", "V"]
    
    # 各例文での要素の位置を分析
    sentence_analysis = [
        {
            "sentence": "What did he tell her at the store?",
            "element_positions": {
                "O2_wh": 0,      # What
                "M2_wh": 0,      # What (同じ単語だが別解釈)  
                "Aux": 1,        # did
                "S": 2,          # he
                "V": 3,          # tell
                "O1": 4,         # her
                "M2_normal": 5   # at the store (atの位置)
            }
        },
        {
            "sentence": "Did he tell her a secret there?",
            "element_positions": {
                "Aux": 0,        # Did
                "S": 1,          # he
                "V": 2,          # tell
                "O1": 3,         # her
                "O2_normal": 4,  # a secret (aの位置)
                "M2_normal": 6   # there
            }
        },
        {
            "sentence": "Did I tell him a truth in the kitchen?",
            "element_positions": {
                "Aux": 0,        # Did
                "S": 1,          # I
                "V": 2,          # tell
                "O1": 3,         # him
                "O2_normal": 4,  # a truth (aの位置)
                "M2_normal": 6   # in the kitchen (inの位置)
            }
        },
        {
            "sentence": "Where did you tell me a story?",
            "element_positions": {
                "M2_wh": 0,      # Where
                "Aux": 1,        # did
                "S": 2,          # you
                "V": 3,          # tell
                "O1": 4,         # me
                "O2_normal": 5   # a story (aの位置)
            }
        }
    ]
    
    print("=== tellグループ要素の語順分析 ===")
    
    # 各要素の平均位置を計算
    element_avg_positions = {}
    
    for element in elements:
        positions = []
        for analysis in sentence_analysis:
            if element in analysis["element_positions"]:
                positions.append(analysis["element_positions"][element])
        
        if positions:
            avg_pos = sum(positions) / len(positions)
            element_avg_positions[element] = avg_pos
            print(f"{element:12} → 位置: {positions} (平均: {avg_pos:.1f})")
        else:
            element_avg_positions[element] = 999  # 出現しない要素は最後
            print(f"{element:12} → 位置: [] (平均: なし)")
    
    # 平均位置でソート
    sorted_elements = sorted(elements, key=lambda x: element_avg_positions[x])
    
    print(f"\n=== tellグループ固定order ===")
    for i, element in enumerate(sorted_elements, 1):
        avg_pos = element_avg_positions[element]
        if avg_pos != 999:
            print(f"{element}_{i} (平均位置: {avg_pos:.1f})")
        else:
            print(f"{element}_{i} (出現なし)")
    
    print(f"\n=== 各例文での配置確認 ===")
    for i, analysis in enumerate(sentence_analysis, 1):
        print(f"\n例文{i}: {analysis['sentence']}")
        print("固定orderでの配置:")
        
        for j, element in enumerate(sorted_elements, 1):
            if element in analysis["element_positions"]:
                actual_pos = analysis["element_positions"][element]
                print(f"  {element}_{j}: 位置{actual_pos} ✓")
            else:
                print(f"  {element}_{j}: --- (なし)")
    
    return sorted_elements

if __name__ == "__main__":
    result = arrange_tell_group_elements()
