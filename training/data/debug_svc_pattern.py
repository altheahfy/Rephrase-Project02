#!/usr/bin/env python3
"""
SVC文型（be動詞＋形容詞補語）問題の詳細調査
「The car is red.」でC1補語が認識されない原因分析
"""
from dynamic_grammar_mapper import DynamicGrammarMapper

def debug_svc_pattern():
    """SVC文型の詳細デバッグ"""
    
    mapper = DynamicGrammarMapper()
    sentence = "The car is red."
    
    print("=== SVC文型デバッグ分析 ===")
    print(f"対象文: {sentence}\n")
    
    # 詳細解析
    result = mapper.analyze_sentence(sentence)
    
    print("📊 現在の認識結果:")
    print(f"   パターン: {result.get('pattern_detected', 'unknown')}")
    print(f"   文型: {result.get('sentence_type', 'unknown')}")
    print(f"   スロット: {result.get('Slot', [])}")
    
    # 内部処理の詳細を確認するため、低レベル解析
    doc = mapper.nlp(sentence)
    tokens = mapper._extract_tokens(doc)
    
    print(f"\n🔍 Token分析:")
    for i, token in enumerate(tokens):
        print(f"   {i}: '{token['text']}' - POS:{token['pos']}, TAG:{token['tag']}, DEP:{token['dep']}")
    
    # コア要素分析
    core = mapper._identify_core_elements(tokens)
    print(f"\n🎯 コア要素認識:")
    print(f"   主語: {core.get('subject', 'なし')}")
    print(f"   動詞: {core.get('verb', {}).get('text', 'なし') if core.get('verb') else 'なし'}")
    print(f"   助動詞: {core.get('auxiliary', {}).get('text', 'なし') if core.get('auxiliary') else 'なし'}")
    
    # 文型判定
    pattern = mapper._determine_sentence_pattern(core, tokens)
    print(f"\n📋 文型判定:")
    print(f"   判定結果: {pattern}")
    
    # 文法要素割り当て
    elements = mapper._assign_grammar_roles(tokens, pattern, core)
    print(f"\n⚙️ 文法要素割り当て:")
    for element in elements:
        print(f"   {element.role}: '{element.text}' (信頼度: {element.confidence:.2f})")
    
    print(f"\n❌ 問題分析:")
    print("   期待: C1補語 'red' が認識される")
    print("   実際: C1補語が認識されていない")
    
    # 'red'トークンの詳細分析
    red_token = None
    for token in tokens:
        if token['text'].lower() == 'red':
            red_token = token
            break
    
    if red_token:
        print(f"\n🔍 'red'トークン詳細:")
        print(f"   POS: {red_token['pos']}")
        print(f"   TAG: {red_token['tag']}")
        print(f"   DEP: {red_token['dep']}")
        print(f"   HEAD: {red_token.get('head', 'unknown')}")
    
    # be動詞の詳細分析
    is_token = None
    for token in tokens:
        if token['text'].lower() == 'is':
            is_token = token
            break
    
    if is_token:
        print(f"\n🔍 'is'トークン詳細:")
        print(f"   POS: {is_token['pos']}")
        print(f"   TAG: {is_token['tag']}")
        print(f"   DEP: {is_token['dep']}")

if __name__ == "__main__":
    debug_svc_pattern()
