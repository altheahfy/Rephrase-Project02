#!/usr/bin/env python3
"""名詞句置換ロジックの問題を詳細分析"""

import spacy

def analyze_noun_phrase_problem():
    """名詞句の範囲特定問題を分析"""
    
    nlp_spacy = spacy.load("en_core_web_sm")
    
    test_sentence = "The book that I read yesterday was interesting."
    
    print(f"🔍 分析文: {test_sentence}")
    print("=" * 50)
    
    doc = nlp_spacy(test_sentence)
    
    print("🔍 名詞句 (noun_chunks):")
    for chunk in doc.noun_chunks:
        print(f"  📎 '{chunk.text}' (root: {chunk.root.text}, start: {chunk.start}, end: {chunk.end})")
    
    print("\n🔍 関係節 (relcl):")
    for token in doc:
        if token.dep_ == 'relcl':
            clause_tokens = list(token.subtree)
            clause_text = ' '.join([t.text for t in clause_tokens])
            print(f"  📎 relcl: '{clause_text}' (head: {token.head.text})")
            
            # 修飾される名詞の範囲
            head_token = token.head
            print(f"  📎 修飾される語: '{head_token.text}' (idx: {head_token.i})")
            
            # 名詞句全体の範囲を特定
            noun_phrase_start = None
            noun_phrase_end = None
            
            for chunk in doc.noun_chunks:
                if head_token.i >= chunk.start and head_token.i < chunk.end:
                    noun_phrase_start = chunk.start
                    noun_phrase_end = chunk.end
                    print(f"  📎 名詞句範囲: tokens {noun_phrase_start}-{noun_phrase_end}")
                    print(f"  📎 名詞句全体: '{chunk.text}'")
                    break
    
    print("\n🔍 正しい置換:")
    print("  ❌ 間違い: 'The book something was interesting.'")
    print("  ✅ 正解: 'Something was interesting.'")
    
    # 正しい置換の実装例
    correct_replacement = implement_correct_replacement(doc)
    print(f"  🎯 実装結果: '{correct_replacement}'")

def implement_correct_replacement(doc):
    """正しい名詞句全体置換の実装"""
    
    # 関係節を含む名詞句を特定
    noun_phrases_to_replace = []
    
    for token in doc:
        if token.dep_ == 'relcl':
            # 修飾される名詞を特定
            head_token = token.head
            
            # その名詞を含む名詞句全体を特定
            for chunk in doc.noun_chunks:
                if head_token.i >= chunk.start and head_token.i < chunk.end:
                    noun_phrases_to_replace.append({
                        'start': chunk.start,
                        'end': chunk.end,
                        'text': chunk.text,
                        'replacement': 'Something'
                    })
                    break
    
    # 置換実行
    if noun_phrases_to_replace:
        # 最初の名詞句のみ処理（この例では1つだけ）
        replacement = noun_phrases_to_replace[0]
        
        # トークン再構成
        result_tokens = []
        i = 0
        while i < len(doc):
            if i == replacement['start']:
                result_tokens.append(replacement['replacement'])
                i = replacement['end']  # 名詞句全体をスキップ
            else:
                result_tokens.append(doc[i].text)
                i += 1
        
        return ' '.join(result_tokens)
    
    return str(doc)

if __name__ == "__main__":
    analyze_noun_phrase_problem()
