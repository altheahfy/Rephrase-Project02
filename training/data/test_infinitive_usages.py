#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_infinitive_usages():
    engine = CompleteRephraseParsingEngine()
    
    test_sentences = [
        # 名詞的用法（既にテスト済み）
        'I want to play tennis.',
        
        # 副詞的用法（目的）
        'I went to the store to buy milk.',
        'She came here to help me.',
        
        # 形容詞的用法（名詞修飾）
        'I have something to do.',
        'He needs time to think.',
        'There is nothing to eat.',
        
        # 比較用：通常の前置詞句
        'I went to the store.',
    ]
    
    for sentence in test_sentences:
        print(f'\n{"="*60}')
        print(f'テスト文: {sentence}')
        print("="*60)
        
        # spaCy分析
        doc = engine.nlp(sentence)
        print("\n🔍 spaCy 依存関係分析:")
        for token in doc:
            print(f"  {token.text:10} [{token.pos_:4}] ({token.dep_:10}) <- {token.head.text}")
        
        # 不定詞句の分析
        infinitive_phrases = []
        for token in doc:
            if token.pos_ == 'PART' and token.text.lower() == 'to' and token.head.pos_ == 'VERB':
                # 不定詞句を構築
                inf_verb = token.head
                phrase_tokens = [token.text, inf_verb.text]
                
                # 動詞の目的語や修飾語を追加
                for child in inf_verb.children:
                    if child != token and child.dep_ in ['dobj', 'pobj', 'prep']:
                        if child.dep_ == 'prep':
                            for prep_child in child.children:
                                if prep_child.dep_ == 'pobj':
                                    phrase_tokens.extend([child.text, prep_child.text])
                        else:
                            phrase_tokens.append(child.text)
                
                infinitive_phrase = ' '.join(phrase_tokens)
                infinitive_phrases.append({
                    'phrase': infinitive_phrase,
                    'dep': inf_verb.dep_,
                    'head': inf_verb.head.text,
                    'usage': classify_infinitive_usage(inf_verb)
                })
        
        print(f"\n🔍 検出された不定詞句:")
        for inf_info in infinitive_phrases:
            print(f"  - '{inf_info['phrase']}' [{inf_info['dep']}] <- {inf_info['head']} ({inf_info['usage']})")
        
        # 完全解析結果
        result = engine.analyze_sentence(sentence)
        if result and 'main_slots' in result:
            main_slots = result['main_slots']
            
            print(f"\n📊 スロット分析:")
            phrase_found = False
            for slot_name, candidates in main_slots.items():
                if candidates:  # 空でない場合のみ表示
                    print(f"  {slot_name}:")
                    for candidate in candidates:
                        label = candidate.get('label', 'word')
                        text = candidate.get('value', candidate.get('text', ''))
                        is_phrase_flag = candidate.get('is_phrase', False)
                        if is_phrase_flag or label == 'phrase':
                            phrase_found = True
                            print(f"    - '{text}' [PHRASE] ✨")
                        else:
                            print(f"    - '{text}' [{label}]")
            
            if not phrase_found:
                print("  (phraseなし)")

def classify_infinitive_usage(verb_token):
    """不定詞の用法を分類"""
    dep = verb_token.dep_
    
    # 名詞的用法
    if dep in ['dobj', 'nsubj', 'pcomp', 'ccomp', 'csubj']:
        return "名詞的用法"
    elif dep == 'xcomp' and verb_token.head.lemma_ in ['want', 'like', 'need', 'plan', 'try', 'decide']:
        return "名詞的用法"
    
    # 副詞的用法（目的・結果）
    elif dep in ['advcl', 'purpcl']:
        return "副詞的用法"
    elif dep == 'xcomp' and verb_token.head.lemma_ in ['go', 'come', 'run', 'walk']:
        return "副詞的用法（目的）"
    
    # 形容詞的用法（名詞修飾）
    elif dep in ['acl', 'relcl']:
        return "形容詞的用法"
    
    # その他
    else:
        return f"その他 ({dep})"

if __name__ == "__main__":
    test_infinitive_usages()
