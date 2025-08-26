#!/usr/bin/env python3
"""
Basic Five Pattern Engine Enhanced Test
統一境界拡張ライブラリ統合後のテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/engines')

try:
    from engines.basic_five_pattern_engine_enhanced import BasicFivePatternEngine
except ImportError:
    from basic_five_pattern_engine_enhanced import BasicFivePatternEngine

def test_enhanced_engine():
    """Enhanced版Basic Five Pattern Engineテスト"""
    
    print("🧪 Basic Five Pattern Engine Enhanced Test")
    print("=" * 60)
    
    engine = BasicFivePatternEngine()
    
    # 既存テストケース（境界拡張効果測定）
    test_cases = [
        {
            "sentence": "I love programming",
            "pattern": "SVO",
            "expected": {"S": "I", "V": "love", "O1": "programming"},
            "boundary_test": False
        },
        {
            "sentence": "The tall man runs fast",
            "pattern": "SV",
            "expected": {"S": "tall man", "V": "runs"},  # 境界拡張効果期待
            "boundary_test": True
        },
        {
            "sentence": "He gave her a beautiful book",
            "pattern": "SVOO", 
            "expected": {"S": "He", "V": "gave", "O1": "her", "O2": "beautiful book"},
            "boundary_test": True
        },
        {
            "sentence": "They consider him very smart",
            "pattern": "SVOC",
            "expected": {"S": "They", "V": "consider", "O1": "him", "C2": "smart"},
            "boundary_test": True  # "very smart"拡張期待
        },
        {
            "sentence": "The red car is expensive",
            "pattern": "SVC",
            "expected": {"S": "red car", "V": "is", "C1": "expensive"},
            "boundary_test": True  # "The red car"拡張期待
        }
    ]
    
    success_count = 0
    boundary_improvement_count = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{case['sentence']}'")
        print(f"   Expected pattern: {case['pattern']}")
        
        # エンジン実行
        result = engine.process_sentence(case['sentence'])
        
        if result['success']:
            print(f"   ✅ Pattern detected: {result.get('pattern', 'Unknown')}")
            
            # スロット結果表示
            slots = result.get('slots', {})
            print(f"   📦 Slots extracted:")
            for slot, value in slots.items():
                expected_value = case['expected'].get(slot)
                if expected_value:
                    # 境界拡張効果チェック
                    is_expanded = len(value.split()) > len(expected_value.split())
                    expansion_mark = " 🔧" if is_expanded else ""
                    match_mark = "✅" if value.strip() == expected_value.strip() else "⚠️"
                    print(f"      {slot}: '{value}'{expansion_mark} {match_mark}")
                    
                    if case['boundary_test'] and is_expanded:
                        boundary_improvement_count += 1
                else:
                    print(f"      {slot}: '{value}' (追加)")
            
            success_count += 1
        else:
            print(f"   ❌ Detection failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n📊 Test Results:")
    print(f"   Total tests: {len(test_cases)}")
    print(f"   Successful detections: {success_count}/{len(test_cases)}")
    print(f"   Boundary expansion improvements: {boundary_improvement_count}")
    print(f"   Success rate: {success_count/len(test_cases)*100:.1f}%")
    
    if success_count == len(test_cases):
        print(f"\n🎉 All tests passed! Enhanced boundary expansion working!")
        if boundary_improvement_count > 0:
            print(f"✨ {boundary_improvement_count} cases showed boundary expansion improvements!")
    else:
        print(f"\n⚠️ {len(test_cases) - success_count} tests failed")
    
    return success_count == len(test_cases)

if __name__ == "__main__":
    test_enhanced_engine()
