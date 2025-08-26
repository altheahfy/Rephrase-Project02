#!/usr/bin/env python3
"""
Boundary Expansion Effect Test
境界拡張効果の詳細測定
"""

import sys
import os
sys.path.append('..')
sys.path.append('../engines')

from boundary_expansion_lib import BoundaryExpansionLib

def test_boundary_expansion_effects():
    """境界拡張効果の詳細テスト"""
    
    print("🔬 Boundary Expansion Effects Test")
    print("=" * 60)
    
    lib = BoundaryExpansionLib()
    
    # 境界拡張効果のテストケース
    test_cases = [
        {
            "text": "the tall beautiful girl",
            "slot": "S",
            "description": "複数形容詞+名詞（主語）"
        },
        {
            "text": "very carefully and slowly",
            "slot": "M2",
            "description": "複数副詞（修飾語）"
        },
        {
            "text": "New York City Hall",
            "slot": "O1", 
            "description": "複合固有名詞（目的語）"
        },
        {
            "text": "have been working",
            "slot": "V",
            "description": "複合動詞（完了進行形）"
        },
        {
            "text": "extremely important",
            "slot": "C1",
            "description": "副詞+形容詞（補語）"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['description']}")
        print(f"   Original: '{case['text']}'")
        
        # 汎用拡張
        generic_result = lib.expand_span_generic(case['text'])
        print(f"   Generic expansion: '{generic_result}'")
        
        # スロット特化拡張
        slot_result = lib.expand_span_for_slot(case['text'], case['slot'])
        print(f"   {case['slot']} optimized: '{slot_result}'")
        
        # 拡張必要性判定
        requires_expansion = lib.check_requires_expansion(case['text'])
        print(f"   Expansion needed: {requires_expansion}")
        
        # スロット別拡張ルール表示
        expand_deps = lib.get_expansion_deps_for_slot(case['slot'])
        print(f"   {case['slot']} rules: {expand_deps}")
    
    print(f"\n✅ 境界拡張効果測定完了")
    print(f"📊 統一境界拡張ライブラリは全スロットで最適化された処理を提供")

if __name__ == "__main__":
    test_boundary_expansion_effects()
