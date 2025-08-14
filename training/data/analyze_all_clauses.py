#!/usr/bin/env python3
"""全節タイプの正しい置換方法を分析"""

import spacy

def analyze_all_clause_types():
    """各節タイプの正しい置換方法を詳細分析"""
    
    nlp_spacy = spacy.load("en_core_web_sm")
    
    test_cases = [
        {
            'sentence': "I think that he is smart.",
            'expected_replacement': "I think something.",
            'description': "補文節(ccomp) - 節のみ置換"
        },
        {
            'sentence': "Being a teacher, she knows students well.",
            'expected_replacement': "somehow, she knows students well.",
            'description': "副詞節(advcl) - 節のみ置換、主節保持"
        },
        {
            'sentence': "The book that I read yesterday was interesting.",
            'expected_replacement': "Something was interesting.",
            'description': "関係節(relcl) - 修飾される名詞句全体置換"
        },
        {
            'sentence': "Having finished the work, she went home.",
            'expected_replacement': "somehow, she went home.",
            'description': "副詞節(advcl) - 節のみ置換、主節保持"
        },
        {
            'sentence': "If I were rich, I would travel around the world.",
            'expected_replacement': "somehow, I would travel around the world.",
            'description': "副詞節(advcl) - 節のみ置換、主節保持"
        }
    ]
    
    print("🔍 全節タイプの置換方法分析")
    print("=" * 70)
    
    for i, case in enumerate(test_cases):
        print(f"\n📝 Case {i+1}: {case['sentence']}")
        print(f"📋 {case['description']}")
        print(f"✅ 期待結果: '{case['expected_replacement']}'")
        
        doc = nlp_spacy(case['sentence'])
        
        # 実際の節構造を分析
        for token in doc:
            if token.dep_ in ['ccomp', 'xcomp', 'advcl', 'acl', 'relcl']:
                clause_tokens = list(token.subtree)
                clause_text = ' '.join([t.text for t in clause_tokens])
                
                print(f"🔍 検出: {token.dep_} = '{clause_text}'")
                print(f"   📍 Head: {token.head.text} (idx: {token.head.i})")
                print(f"   📍 Range: {min(t.i for t in clause_tokens)} - {max(t.i for t in clause_tokens) + 1}")
                
                # 置換方法の判定
                if token.dep_ == 'relcl':
                    # 関係節：修飾される名詞句全体を特定
                    head_token = token.head
                    noun_phrase_start = head_token.i
                    for chunk in doc.noun_chunks:
                        if head_token.i >= chunk.start and head_token.i < chunk.end:
                            noun_phrase_start = chunk.start
                            print(f"   🎯 名詞句全体置換: {noun_phrase_start} - {max(t.i for t in clause_tokens) + 1}")
                            break
                else:
                    # その他：節のみ置換
                    print(f"   🎯 節のみ置換: {min(t.i for t in clause_tokens)} - {max(t.i for t in clause_tokens) + 1}")
        
        print("-" * 50)

def implement_universal_replacement():
    """汎用的置換ロジックの実装"""
    print("\n🛠️ 汎用的置換ロジック実装指針:")
    print("1. relcl → 修飾される名詞句全体 + 関係節 → プレースホルダー")
    print("2. ccomp/xcomp → 節のみ → プレースホルダー") 
    print("3. advcl → 節のみ → プレースホルダー")
    print("4. acl → 節のみ → プレースホルダー")
    print("5. 複数節 → 後ろから順次置換（インデックス維持）")

if __name__ == "__main__":
    analyze_all_clause_types()
    implement_universal_replacement()
