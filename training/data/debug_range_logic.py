#!/usr/bin/env python3
"""
範囲論理デバッグ: _find_subject関数の範囲計算を詳細分析
"""

def debug_range_calculation():
    """range()計算の詳細デバッグ"""
    
    # テストケース: "She quickly runs to school."
    # Tokens: 0:'She', 1:'quickly', 2:'runs', 3:'to', 4:'school', 5:'.'
    verb_idx = 2  # 'runs'の位置
    
    print("=== Range Logic Debug ===")
    print(f"verb_idx = {verb_idx}")
    print(f"range({verb_idx - 1}, -1, -1) = range({verb_idx - 1}, -1, -1)")
    
    # 実際の範囲を生成
    actual_range = list(range(verb_idx - 1, -1, -1))
    print(f"実際の範囲: {actual_range}")
    
    # 各インデックスの詳細
    tokens = ['She', 'quickly', 'runs', 'to', 'school', '.']
    print("\n=== Token Analysis ===")
    for i in range(len(tokens)):
        in_range = i in actual_range
        print(f"Index {i}: '{tokens[i]}' - {'✓ 検索対象' if in_range else '✗ スキップ'}")
    
    print("\n=== 期待される範囲 ===")
    expected_range = list(range(verb_idx - 1, -1, -1))
    print(f"期待される範囲: {expected_range}")
    print("問題: Index 0 ('She') が検索対象に含まれていない")
    
    print("\n=== 修正案 ===")
    # 修正されるべき範囲
    correct_range = list(range(verb_idx - 1, -1, -1))
    print(f"修正後の範囲: {correct_range}")
    print("実際は正しく動作するはず... 別の問題があるかも")

if __name__ == "__main__":
    debug_range_calculation()
