#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_phrase_classification():
    engine = CompleteRephraseParsingEngine()
    
    test_sentences = [
        'I sleep on the bed.',
        'I go to a bald man.',
        'I saw the building.',
        'I want to play tennis.'  # 動詞を含む真のphrase
    ]
    
    for sentence in test_sentences:
        print(f'\n=== テスト: {sentence} ===')
        result = engine.analyze_sentence(sentence)
        if result:
            # main_slotsをチェック
            main_slots = result.get('main_slots', {})
            phrase_found = False
            
            for slot_name, slot_candidates in main_slots.items():
                for candidate in slot_candidates:
                    if candidate.get('label') == 'phrase' or candidate.get('is_phrase'):
                        phrase_found = True
                        text = candidate.get('value', candidate.get('text', ''))
                        print(f'⚠️ phrase検出 [{slot_name}]: "{text}"')
            
            if not phrase_found:
                print('✅ phrase検出なし（期待通り）')
        else:
            print('❌ 解析失敗')

if __name__ == "__main__":
    test_phrase_classification()
