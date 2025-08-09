#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def debug_engine_output():
    """CompleteRephraseParsingEngineの出力内容詳細確認"""
    
    engine = CompleteRephraseParsingEngine()
    
    test_sentence = "I want to play tennis."
    print(f"=== エンジン出力詳細確認: {test_sentence} ===")
    
    result = engine.analyze_sentence(test_sentence)
    
    print(f"\n📋 完全な結果構造:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # slotsデータの詳細確認
    if 'slots' in result:
        print(f"\n🔍 スロットデータ詳細:")
        for slot, candidates in result['slots'].items():
            if not candidates:
                continue
            print(f"\n  {slot}:")
            for i, candidate in enumerate(candidates):
                print(f"    候補 {i}:")
                for key, value in candidate.items():
                    print(f"      {key}: {value}")

if __name__ == "__main__":
    debug_engine_output()
