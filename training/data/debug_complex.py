"""
🔍 複文問題の詳細調査
"""

import spacy

def debug_complex_sentence():
    """複文の詳細デバッグ"""
    print("🔍 複文問題デバッグセッション")
    print("=" * 50)
    
    nlp = spacy.load("en_core_web_sm")
    sentence = "I think that he is right."
    doc = nlp(sentence)
    
    print(f"📝 分析文: {sentence}")
    print("🔧 spaCy詳細解析:")
    for i, token in enumerate(doc):
        print(f"   [{i}] {token.text:<8} | {token.pos_:<8} | {token.dep_:<15} | {token.head.text} | {token.tag_}")
    
    print()
    print("🎯 that節の詳細:")
    that_index = -1
    for i, token in enumerate(doc):
        if token.text.lower() == 'that':
            that_index = i
            print(f"   'that' found at index {i}")
            break
    
    if that_index >= 0:
        print(f"   that節以降の語句:")
        for token in doc[that_index:]:
            print(f"     [{token.i}] {token.text} ({token.dep_}, {token.pos_})")
            if token.dep_ == 'cop':
                print(f"       ★ copula found: {token.text}")

if __name__ == "__main__":
    debug_complex_sentence()
