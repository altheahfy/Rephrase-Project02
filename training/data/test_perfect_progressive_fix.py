#!/usr/bin/env python3
"""
完了進行形エンジン修正テスト - 時間節問題の検証
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.perfect_progressive_engine import PerfectProgressiveEngine

def test_time_clause_fix():
    """時間節の配置修正テスト"""
    print("🔥 完了進行形エンジン 修正テスト開始")
    print("🚀 完了進行形構文エンジン初期化中...")
    
    # より軽量な初期化
    try:
        engine = PerfectProgressiveEngine()
        print("✅ 初期化完了")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return
    
    print("\n📝 時間節配置修正テスト")
    print("=" * 50)
    
    # テストケース1: when節の正しい配置
    test_cases = [
        {
            'name': '過去完了進行形 + when節',
            'sentence': 'She had been waiting for an hour when I arrived.',
            'expected_upper': ['S', 'Aux', 'V', 'M1'],  # when節は上位に含まれない
            'expected_sub': ['sub-s', 'sub-aux', 'sub-v', 'sub-m1', 'sub-m2']  # when節はサブに含まれる
        },
        {
            'name': '複文の完了進行形分離',
            'sentence': 'He was tired because he had been running all morning.',
            'expected_upper': ['S', 'Aux', 'V'],  # 完了進行形の主要素のみ
            'expected_sub': ['sub-s', 'sub-aux', 'sub-v']  # 完了進行形部分のみ
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 テスト{i}: {test_case['name']}")
        print(f"入力: {test_case['sentence']}")
        
        try:
            result = engine.process(test_case['sentence'])
            print(f"✅ 処理成功")
            
            print(f"  📋 上位スロット:")
            upper_slots = []
            for key, value in result.items():
                if not key.startswith('sub-') and key not in ['metadata']:
                    print(f"    {key}: '{value}'")
                    upper_slots.append(key)
            
            print(f"  📋 サブスロット:")
            sub_slots = []
            for key, value in result.items():
                if key.startswith('sub-'):
                    print(f"    {key}: '{value}'")
                    sub_slots.append(key)
            
            # 上位スロット検証
            print(f"\n  🔍 上位スロット検証:")
            print(f"    期待: {test_case['expected_upper']}")
            print(f"    実際: {upper_slots}")
            
            # when節が上位に入っていないかチェック
            if 'M2' in upper_slots and ('when' in str(result.get('M2', '')) or 'because' in str(result.get('M2', ''))):
                print(f"    ❌ 時間節/理由節が上位スロットに配置されています")
            else:
                print(f"    ✅ 時間節/理由節は上位スロットに配置されていません")
                
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 修正テスト完了")

if __name__ == "__main__":
    test_time_clause_fix()
