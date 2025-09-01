#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 119 _detect_by_pos_analysis デバッグスクリプト
"""

import spacy

def debug_pos_analysis():
    """_detect_by_pos_analysis の詳細デバッグ"""
    print("=" * 60)
    print("_detect_by_pos_analysis デバッグ")
    print("=" * 60)
    
    sentence = "It depends on if you agree."
    
    # spaCy解析
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    
    print(f"\n📝 原文: {sentence}")
    
    print(f"\n🔍 トークン分析:")
    for i, token in enumerate(doc):
        print(f"  [{i}] {token.text:12} | pos={token.pos_:8} | text.lower()='{token.text.lower()}'")
        
        # 条件チェック
        if token.text.lower() in ['that', 'whether', 'if']:
            print(f"    → 名詞節接続詞発見: '{token.text.lower()}'")
            
            if i > 0:
                prev_token = doc[i-1]
                print(f"    → 前のトークン: '{prev_token.text}' (pos={prev_token.pos_})")
                
                if prev_token.pos_ == 'ADP':
                    print(f"    ✅ 前置詞+名詞節条件満たす: '{prev_token.text} {token.text}'")
                    
                    result = {
                        'type': 'if_clause_noun',
                        'position': 'prepositional_object',
                        'connector': token.text.lower(),
                        'preposition': prev_token.text,
                        'clause_range': (i, len(doc))
                    }
                    print(f"    → 検出結果: {result}")
                else:
                    print(f"    ❌ 前置詞ではない: pos={prev_token.pos_}")
            else:
                print(f"    ❌ 文頭の接続詞")

if __name__ == "__main__":
    debug_pos_analysis()
