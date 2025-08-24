#!/usr/bin/env python3
"""
受動態ハンドラーテスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper

def test_passive_voice_handler():
    """受動態ハンドラーのテスト"""
    mapper = DynamicGrammarMapper()

    # 受動態テスト文
    test_sentences = [
        'The book was written by John.',
        'The car is repaired in the garage.',
        'She was surprised by the news.',
        'The project will be completed soon.'
    ]

    print('🔥 受動態ハンドラーテスト開始')
    print('='*50)

    for sentence in test_sentences:
        print(f'\n📝 テスト文: {sentence}')
        result = mapper.analyze_sentence(sentence)
        
        print(f'🎯 V スロット: {result.get("slots", {}).get("V", "(empty)")}')
        
        # M スロットの確認
        for m_slot in ['M1', 'M2', 'M3']:
            m_value = result.get('slots', {}).get(m_slot, '')
            if m_value:
                print(f'📍 {m_slot} スロット: {m_value}')
        
        # 文法情報の確認
        grammar_info = result.get('grammar_info', {})
        if 'handler_contributions' in grammar_info:
            passive_info = grammar_info['handler_contributions'].get('passive_voice')
            if passive_info:
                print(f'✅ 受動態ハンドラー成功: {passive_info.get("processing_notes", "")}')
        
        print('-' * 30)

if __name__ == '__main__':
    test_passive_voice_handler()
