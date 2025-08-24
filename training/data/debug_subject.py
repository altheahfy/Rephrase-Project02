#!/usr/bin/env python3
"""
主語認識デバッグテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_grammar_mapper import DynamicGrammarMapper

def debug_subject_recognition():
    """主語認識のデバッグ"""
    
    analyzer = DynamicGrammarMapper()
    
    test_sentence = "She quickly runs to school."
    print(f"テスト文: {test_sentence}")
    
    # spaCy解析
    doc = analyzer.nlp(test_sentence)
    tokens = analyzer._extract_tokens(doc)
    
    print("\n=== トークン情報 ===")
    for i, token in enumerate(tokens):
        print(f"{i}: '{token['text']}' pos={token['pos']} tag={token['tag']} dep={token['dep']}")
    
    # コア要素の特定
    core_elements = analyzer._identify_core_elements(tokens)
    
    print("\n=== コア要素 ===")
    print(f"主語: {core_elements.get('subject')} (indices: {core_elements.get('subject_indices')})")
    print(f"動詞: {core_elements.get('verb')} (indices: {core_elements.get('verb_indices')})")
    print(f"助動詞: {core_elements.get('auxiliary')} (indices: {core_elements.get('auxiliary_indices')})")
    
    # メイン動詞の特定
    main_verb_idx = analyzer._find_main_verb(tokens)
    print(f"\nメイン動詞インデックス: {main_verb_idx}")
    
    # 主語の特定（詳細デバッグ）
    if main_verb_idx is not None:
        print(f"\n=== 主語検出デバッグ ===")
        print(f"動詞位置: {main_verb_idx} ('{tokens[main_verb_idx]['text']}')")
        print("動詞前のトークンを右から左に探索:")
        
        subject_indices = []
        
        for i in range(main_verb_idx - 1, -1, -1):
            token = tokens[i]
            
            print(f"  検討中[{i}]: '{token['text']}' pos={token['pos']} tag={token['tag']}")
            
            # 助動詞チェック
            is_aux = analyzer._is_auxiliary_verb(token)
            print(f"    助動詞?: {is_aux}")
            
            if is_aux:
                print("    → 助動詞のためスキップ")
                continue
            
            # 主語候補チェック
            is_subject_candidate = (token['pos'] in ['NOUN', 'PROPN', 'PRON'] or 
                                   token['tag'] in ['DT', 'PRP', 'PRP$', 'WP'])
            print(f"    主語候補?: {is_subject_candidate}")
            
            if is_subject_candidate:
                subject_indices.insert(0, i)
                print(f"    → 主語に追加: indices={subject_indices}")
            else:
                print(f"    → 主語境界に到達、終了")
                break
        
        print(f"最終主語indices: {subject_indices}")
        
        if subject_indices:
            subject_text = ' '.join([tokens[i]['text'] for i in subject_indices])
            print(f"最終主語テキスト: '{subject_text}'")
        else:
            print("主語が検出されませんでした")

if __name__ == "__main__":
    debug_subject_recognition()
