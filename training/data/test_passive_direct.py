#!/usr/bin/env python3
"""
受動態検出テスト（直接実装）
"""

import spacy

def test_passive_detection():
    """受動態パターンの直接検出"""
    
    # spaCy初期化
    nlp = spacy.load("en_core_web_sm")
    
    test_sentences = [
        'The book was written.',
        'The book was written by John.',
        'The car is repaired.',
        'She was surprised by the news.',
        'The project will be completed.'
    ]
    
    print('🔥 受動態検出テスト')
    print('='*50)
    
    for sentence in test_sentences:
        print(f'\n📝 テスト文: {sentence}')
        doc = nlp(sentence)
        
        # 基本的な受動態検出
        passive_found = False
        be_verb = ""
        past_participle = ""
        
        tokens = list(doc)
        for i in range(len(tokens) - 1):
            current = tokens[i]
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            
            # be動詞 + 過去分詞パターン
            if (current.lemma_.lower() == 'be' and 
                current.pos_ in ['AUX', 'VERB'] and
                next_token and next_token.tag_ == 'VBN'):
                
                passive_found = True
                be_verb = current.text
                past_participle = next_token.text
                break
            
            # modal + be + 過去分詞パターン
            if (current.pos_ == 'AUX' and 
                current.text.lower() in ['will', 'would', 'can', 'could', 'should'] and
                i + 2 < len(tokens)):
                
                be_token = tokens[i + 1]
                pp_token = tokens[i + 2]
                
                if (be_token.lemma_.lower() == 'be' and 
                    pp_token.tag_ == 'VBN'):
                    
                    passive_found = True
                    be_verb = f"{current.text} {be_token.text}"
                    past_participle = pp_token.text
                    break
        
        # by句の検出
        by_phrase = ""
        for token in tokens:
            if token.text.lower() == 'by' and token.pos_ == 'ADP':
                # by以降の名詞句を簡単に抽出
                idx = token.i
                phrase_parts = ['by']
                for j in range(idx + 1, min(idx + 4, len(tokens))):
                    next_tok = tokens[j]
                    if next_tok.pos_ in ['NOUN', 'PROPN', 'DET']:
                        phrase_parts.append(next_tok.text)
                    else:
                        break
                if len(phrase_parts) > 1:
                    by_phrase = ' '.join(phrase_parts)
                break
        
        # 結果表示
        if passive_found:
            print(f'✅ 受動態検出: {be_verb} + {past_participle}')
            if by_phrase:
                print(f'📍 by句: {by_phrase}')
            print(f'🎯 V スロット候補: {be_verb} {past_participle}')
        else:
            print('❌ 受動態未検出')
        
        print('-' * 30)

if __name__ == '__main__':
    test_passive_detection()
