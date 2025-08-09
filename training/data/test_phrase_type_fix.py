#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Excel_Generator import ExcelGeneratorV2

def test_phrase_type_fix():
    """修正後のPhraseType判定テスト"""
    
    # ジェネレーター初期化
    try:
        generator = ExcelGeneratorV2()
        print("✅ Excel Generator 初期化完了")
    except Exception as e:
        print(f"❌ ジェネレーター初期化失敗: {e}")
        return

    # 問題の例文をテスト
    test_sentences = [
        "I lie on the bed.",      # on the bed → should be word
        "I see the building.",    # the building → should be word  
        "I talk to a bald man.",  # to a bald man → should be word
        "I want to play tennis."  # to play tennis → should be phrase
    ]
    
    print(f"\n=== PhraseType判定テスト ===")
    
    for sentence in test_sentences:
        print(f"\n--- テスト文: {sentence} ---")
        
        try:
            # 解析実行
            success = generator.analyze_and_add_sentence(sentence, f"test_verb_{sentence.split()[1]}")
            
            if success:
                # 解析結果から候補を取得
                v_group_key = f"test_verb_{sentence.split()[1]}"
                if v_group_key in generator.vgroup_data:
                    sentence_data = generator.vgroup_data[v_group_key][-1]  # 最新データ
                    slots_data = sentence_data['slots']
                    
                    # スロットごとにPhraseType確認
                    if 'slots' in slots_data:
                        main_slots = slots_data['slots']
                        for slot, candidates in main_slots.items():
                            if not candidates:
                                continue
                                
                            print(f"\n  {slot}:")
                            for candidate in candidates:
                                if isinstance(candidate, dict):
                                    value = candidate.get('value', '')
                                    phrase_type = generator.determine_phrase_type(candidate)
                                    candidate_type = candidate.get('type', 'unknown')
                                    
                                    print(f"    Value: '{value}'")
                                    print(f"    Type: {candidate_type}")  
                                    print(f"    PhraseType: {phrase_type}")
                                    
                                    # 期待値チェック
                                    if value == 'on the bed':
                                        expected = 'word'
                                        status = "✅" if phrase_type == expected else "❌"
                                        print(f"    {status} 期待値: {expected}")
                                    elif value == 'the building':
                                        expected = 'word'
                                        status = "✅" if phrase_type == expected else "❌"
                                        print(f"    {status} 期待値: {expected}")
                                    elif value == 'to a bald man':
                                        expected = 'word'
                                        status = "✅" if phrase_type == expected else "❌"
                                        print(f"    {status} 期待値: {expected}")
                                    elif value == 'to play tennis':
                                        expected = 'phrase'
                                        status = "✅" if phrase_type == expected else "❌"
                                        print(f"    {status} 期待値: {expected}")
                                        
        except Exception as e:
            print(f"❌ テストエラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_phrase_type_fix()
