#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループの正しい要素列挙（文法的役割ベース）
"""

def enumerate_tell_group_correct():
    """tellグループの正しい要素列挙"""
    
    # tellグループの例文
    sentences = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Did I tell him a truth in the kitchen?",
        "Where did you tell me a story?"
    ]
    
    print("=== tellグループ例文 ===")
    for i, sentence in enumerate(sentences, 1):
        print(f"例文{i}: {sentence}")
    
    # 文法的役割による分析
    print("\n=== 文法的役割による要素分析 ===")
    
    # 各例文の文法的役割
    grammar_analysis = [
        # 例文1: What did he tell her at the store?
        {
            "sentence": "What did he tell her at the store?",
            "roles": {
                "M2_wh": "What",      # 疑問詞位置のM2 (実際はO2だが)
                "O2_wh": "What",      # 疑問詞位置のO2
                "Aux": "did",
                "S": "he", 
                "V": "tell",
                "O1": "her",
                "M2_normal": "at the store"
            }
        },
        # 例文2: Did he tell her a secret there?
        {
            "sentence": "Did he tell her a secret there?",
            "roles": {
                "Aux": "Did",
                "S": "he",
                "V": "tell", 
                "O1": "her",
                "O2_normal": "a secret",
                "M2_normal": "there"
            }
        },
        # 例文3: Did I tell him a truth in the kitchen?
        {
            "sentence": "Did I tell him a truth in the kitchen?", 
            "roles": {
                "Aux": "Did",
                "S": "I",
                "V": "tell",
                "O1": "him", 
                "O2_normal": "a truth",
                "M2_normal": "in the kitchen"
            }
        },
        # 例文4: Where did you tell me a story?
        {
            "sentence": "Where did you tell me a story?",
            "roles": {
                "M2_wh": "Where",     # 疑問副詞位置のM2
                "Aux": "did",
                "S": "you",
                "V": "tell", 
                "O1": "me",
                "O2_normal": "a story"
            }
        }
    ]
    
    # 全ての文法的役割を収集
    all_grammar_roles = set()
    for analysis in grammar_analysis:
        all_grammar_roles.update(analysis["roles"].keys())
    
    sorted_roles = sorted(list(all_grammar_roles))
    
    print(f"抽出された文法的役割（要素）: {len(sorted_roles)}個")
    for i, role in enumerate(sorted_roles, 1):
        print(f"{i}. {role}")
    
    # 各要素の出現を確認
    print(f"\n=== 各要素の出現確認 ===")
    for role in sorted_roles:
        print(f"\n{role}:")
        for i, analysis in enumerate(grammar_analysis, 1):
            if role in analysis["roles"]:
                value = analysis["roles"][role]
                print(f"  例文{i}: {value}")
            else:
                print(f"  例文{i}: ---")
    
    return sorted_roles

if __name__ == "__main__":
    result = enumerate_tell_group_correct()
