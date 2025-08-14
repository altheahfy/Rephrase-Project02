#!/usr/bin/env python3
"""正しい名詞句全体置換の実装"""

import spacy

def correct_noun_phrase_replacement():
    """関係節を含む名詞句全体の正しい置換"""
    
    nlp_spacy = spacy.load("en_core_web_sm")
    
    test_sentence = "The book that I read yesterday was interesting."
    
    print(f"🔍 分析文: {test_sentence}")
    print("=" * 50)
    
    doc = nlp_spacy(test_sentence)
    
    # 関係節とその修飾対象を特定
    relcl_info = None
    for token in doc:
        if token.dep_ == 'relcl':
            # 関係節の範囲
            relcl_tokens = list(token.subtree)
            relcl_start = min(t.i for t in relcl_tokens)
            relcl_end = max(t.i for t in relcl_tokens) + 1
            
            # 修飾される名詞の位置
            head_token = token.head
            
            # 名詞句の開始位置を特定（冠詞等を含む）
            noun_phrase_start = head_token.i
            for chunk in doc.noun_chunks:
                if head_token.i >= chunk.start and head_token.i < chunk.end:
                    noun_phrase_start = chunk.start
                    break
            
            relcl_info = {
                'noun_start': noun_phrase_start,
                'noun_head_idx': head_token.i,
                'relcl_start': relcl_start, 
                'relcl_end': relcl_end,
                'full_start': noun_phrase_start,
                'full_end': relcl_end
            }
            
            print(f"📎 修飾される名詞位置: {head_token.i} ('{head_token.text}')")
            print(f"📎 名詞句開始: {noun_phrase_start}")
            print(f"📎 関係節範囲: {relcl_start}-{relcl_end}")
            print(f"📎 全体置換範囲: {noun_phrase_start}-{relcl_end}")
            
            break
    
    if relcl_info:
        # 正しい置換実行
        result_tokens = []
        i = 0
        while i < len(doc):
            if i == relcl_info['full_start']:
                result_tokens.append('Something')
                i = relcl_info['full_end']  # 名詞句+関係節全体をスキップ
            else:
                result_tokens.append(doc[i].text)
                i += 1
        
        result = ' '.join(result_tokens)
        print(f"\n✅ 正しい置換結果: '{result}'")
        
        # V4でテスト
        from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
        detector = HierarchicalGrammarDetectorV4()
        
        try:
            grammar_result = detector.detect_hierarchical_grammar(result)
            pattern = grammar_result.main_clause.grammatical_pattern.value if grammar_result.main_clause else 'Unknown'
            print(f"🎯 文法パターン: {pattern}")
        except Exception as e:
            print(f"❌ 文法解析エラー: {e}")
    
    else:
        print("❌ 関係節が見つかりませんでした")

if __name__ == "__main__":
    correct_noun_phrase_replacement()
