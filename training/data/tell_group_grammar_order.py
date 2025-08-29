#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループの文法的役割別order付け
"""

def analyze_tell_group_grammar_order():
    """tellグループの文法的役割別order分析"""
    
    # tellグループの例文と既存のabsolute_order
    sentences_data = [
        {
            "sentence": "What did he tell her at the store?",
            "absolute_order": {"O2": 2, "Aux": 3, "S": 4, "V": 5, "O1": 6, "M2": 8},
            "words": ["What", "did", "he", "tell", "her", "at", "the", "store"]
        },
        {
            "sentence": "Did he tell her a secret there?", 
            "absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M2": 8},
            "words": ["Did", "he", "tell", "her", "a", "secret", "there"]
        },
        {
            "sentence": "Did I tell him a truth in the kitchen?",
            "absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M2": 8},
            "words": ["Did", "I", "tell", "him", "a", "truth", "in", "the", "kitchen"]
        },
        {
            "sentence": "Where did you tell me a story?",
            "absolute_order": {"M2": 1, "Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7},
            "words": ["Where", "did", "you", "tell", "me", "a", "story"]
        }
    ]
    
    print("=== tellグループ 文法的役割別order分析 ===")
    
    # 全ての文法的役割を収集
    all_grammar_roles = set()
    for data in sentences_data:
        all_grammar_roles.update(data["absolute_order"].keys())
    
    print(f"登場する文法的役割: {sorted(all_grammar_roles)}")
    print()
    
    # 各文法的役割の出現位置を分析
    role_positions = {}
    for role in all_grammar_roles:
        positions = []
        for data in sentences_data:
            if role in data["absolute_order"]:
                positions.append(data["absolute_order"][role])
        role_positions[role] = positions
    
    print("=== 文法的役割別出現位置 ===")
    for role in sorted(all_grammar_roles):
        positions = role_positions[role]
        avg_pos = sum(positions) / len(positions)
        print(f"{role:3} → 位置: {positions} (平均: {avg_pos:.1f})")
    
    # 平均位置でソートして固定order作成
    sorted_roles = sorted(all_grammar_roles, key=lambda x: sum(role_positions[x]) / len(role_positions[x]))
    
    print("\n=== tellグループ 固定order ===")
    for i, role in enumerate(sorted_roles, 1):
        avg_pos = sum(role_positions[role]) / len(role_positions[role])
        print(f"{role}_{i} (平均位置: {avg_pos:.1f})")
    
    print("\n=== 各例文での実際の配置確認 ===")
    for i, data in enumerate(sentences_data, 1):
        print(f"\n例文{i}: {data['sentence']}")
        print(f"単語: {data['words']}")
        print("配置:")
        
        # 固定orderでの配置を示す
        for j, role in enumerate(sorted_roles, 1):
            if role in data["absolute_order"]:
                actual_pos = data["absolute_order"][role]
                # 実際の単語を特定
                if role == "O2" and data["words"][0] in ["What"]:
                    word = data["words"][0] 
                elif role == "M2" and data["words"][0] in ["Where"]:
                    word = data["words"][0]
                elif role == "Aux":
                    word = next(w for w in data["words"] if w.lower() in ["did"])
                elif role == "S":
                    word = next(w for w in data["words"] if w.lower() in ["he", "i", "you"])
                elif role == "V":
                    word = "tell"
                elif role == "O1":
                    word = next(w for w in data["words"] if w.lower() in ["her", "him", "me"])
                elif role == "M2" and role != "M2" or data["words"][0] not in ["Where"]:
                    # M2が場所句の場合
                    if "there" in data["words"]:
                        word = "there"
                    elif "at" in data["words"]:
                        word = "at the store"
                    elif "in" in data["words"]:
                        word = "in the kitchen"
                    else:
                        word = "?"
                else:
                    word = "?"
                    
                print(f"  {role}_{j}: {word} (実際位置: {actual_pos})")
            else:
                print(f"  {role}_{j}: --- (なし)")
    
    return sorted_roles

if __name__ == "__main__":
    result = analyze_tell_group_grammar_order()
