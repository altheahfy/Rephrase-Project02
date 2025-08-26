#!/usr/bin/env python3
"""
Stanza依存関係パターン体系調査
基本5文型とその修飾語パターンを網羅的に分析
"""

import stanza

def analyze_sentence_patterns():
    """基本文型のStanza解析パターンを体系的に調査"""
    nlp = stanza.Pipeline('en', verbose=False)
    
    # 基本5文型の代表例
    test_patterns = {
        "第1文型 (SV)": [
            "Birds fly.",
            "Children play.",
            "The sun rises.",
        ],
        "第2文型 (SVC)": [
            "He is happy.",
            "She is a teacher.", 
            "They are in the room.",
            "The sky looks blue.",
        ],
        "第3文型 (SVO)": [
            "I like you.",
            "She reads books.",
            "We see the mountain.",
        ],
        "第4文型 (SVOO)": [
            "I gave him a book.",
            "She told me the truth.",
            "They showed us the way.",
        ],
        "第5文型 (SVOC)": [
            "We made him happy.",
            "I found it interesting.",
            "They elected her president.",
        ]
    }
    
    # 修飾語パターン
    modifier_patterns = {
        "形容詞修飾": [
            "The tall man walks.",
            "She likes red apples.",
        ],
        "副詞修飾": [
            "He runs quickly.",
            "She is very intelligent.",
        ],
        "前置詞句修飾": [
            "The book on the table is mine.",
            "He lives in Tokyo.",
        ]
    }
    
    all_patterns = {**test_patterns, **modifier_patterns}
    
    pattern_rules = {}
    
    for category, sentences in all_patterns.items():
        print(f"\n{'='*80}")
        print(f"📋 {category}")
        print(f"{'='*80}")
        
        category_patterns = []
        
        for sentence in sentences:
            print(f"\n🎯 文: {sentence}")
            print(f"-" * 60)
            
            doc = nlp(sentence)
            sent = doc.sentences[0]
            
            # ROOT探索
            root_word = None
            for word in sent.words:
                if word.deprel == 'root':
                    root_word = word
                    break
            
            if not root_word:
                print("❌ ROOT が見つかりません")
                continue
                
            print(f"📌 ROOT: '{root_word.text}' (POS: {root_word.upos})")
            
            # 基本構造抽出
            structure = {}
            structure['root'] = {'word': root_word.text, 'pos': root_word.upos, 'id': root_word.id}
            
            # 各依存関係を分析
            relations = {}
            for word in sent.words:
                if word.deprel not in relations:
                    relations[word.deprel] = []
                relations[word.deprel].append({
                    'word': word.text,
                    'pos': word.upos,
                    'head': word.head,
                    'id': word.id
                })
            
            # 重要な関係を表示
            important_relations = ['nsubj', 'obj', 'iobj', 'cop', 'xcomp', 'amod', 'advmod', 'det', 'case', 'nmod']
            
            print("📋 重要な依存関係:")
            for rel in important_relations:
                if rel in relations:
                    for item in relations[rel]:
                        head_word = sent.words[item['head']-1].text if item['head'] > 0 else 'ROOT'
                        print(f"  {rel:12}: {item['word']:15} -> {head_word:15} (POS: {item['pos']})")
            
            # パターンを記録
            pattern_signature = []
            for word in sent.words:
                if word.deprel in important_relations:
                    pattern_signature.append(f"{word.deprel}({word.upos})")
            
            structure['pattern'] = '+'.join(sorted(pattern_signature))
            category_patterns.append(structure)
            
            print(f"🔍 パターン: {structure['pattern']}")
        
        pattern_rules[category] = category_patterns
    
    # パターン統計
    print(f"\n{'='*80}")
    print("📊 パターン統計")
    print(f"{'='*80}")
    
    all_patterns_seen = {}
    for category, patterns in pattern_rules.items():
        print(f"\n📋 {category}:")
        for pattern in patterns:
            signature = pattern['pattern']
            if signature not in all_patterns_seen:
                all_patterns_seen[signature] = []
            all_patterns_seen[signature].append(category)
            print(f"  - {signature}")
    
    print(f"\n📋 共通パターン:")
    for pattern, categories in all_patterns_seen.items():
        if len(categories) > 1:
            print(f"  {pattern} -> {categories}")

if __name__ == "__main__":
    analyze_sentence_patterns()
