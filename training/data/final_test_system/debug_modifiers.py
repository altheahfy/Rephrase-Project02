#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M1/M2/M3配置問題をデバッグするための専用テストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_modifier_positions():
    """M1/M2/M3配置の問題を詳細デバッグ"""
    
    # デバッグレベルでシステム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # 問題のある例文をテスト
    test_cases = [
        {
            'sentence': 'The student who studies diligently always succeeds academically.',
            'expected_main': {'M1': 'always', 'M2': 'academically'},
            'description': 'Test34: M1/M2の位置が逆転'
        },
        {
            'sentence': 'The message was sent yesterday.',
            'expected_main': {'M2': 'yesterday'},
            'description': 'Test27: M2が検出されない'
        },
        {
            'sentence': 'The car that was quickly repaired yesterday runs smoothly.',
            'expected_main': {'M1': 'smoothly'},
            'description': 'Test32: M1とM2が逆転'
        }
    ]
    
    print("M1/M2/M3配置デバッグテスト")
    print("="*60)
    
    for i, test in enumerate(test_cases, 1):
        sentence = test['sentence']
        expected = test['expected_main']
        description = test['description']
        
        print(f"\n{description}")
        print(f"例文: {sentence}")
        print(f"期待値: {expected}")
        
        try:
            result = mapper.process(sentence)
            system_main = result.get('slots', {})
            
            # M1/M2/M3のみ抽出
            system_modifiers = {k: v for k, v in system_main.items() if k.startswith('M')}
            
            print(f"システム: {system_modifiers}")
            
            # 比較
            match = system_modifiers == expected
            print(f"結果: {'✅ 一致' if match else '❌ 不一致'}")
            
            if not match:
                print("詳細分析:")
                for key in expected:
                    if key not in system_modifiers:
                        print(f"  - {key}: 欠落 (期待='{expected[key]}')")
                    elif system_modifiers[key] != expected[key]:
                        print(f"  - {key}: 不一致 (期待='{expected[key]}', 実際='{system_modifiers[key]}')")
                
                for key in system_modifiers:
                    if key not in expected:
                        print(f"  - {key}: 余分 (実際='{system_modifiers[key]}')")
        
        except Exception as e:
            print(f"エラー: {str(e)}")
        
        print("-" * 60)

if __name__ == "__main__":
    debug_modifier_positions()
