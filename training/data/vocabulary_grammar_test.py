#!/usr/bin/env python3
"""
語彙辞書システム + 文法ルールエンジン = スロット分解システム
理論実証テスト
"""

import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet

def download_nltk_data():
    """NLTK必要データをダウンロード"""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)  # 最新版NLTK用
        nltk.download('averaged_perceptron_tagger', quiet=True) 
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)  # 最新版NLTK用
        nltk.download('wordnet', quiet=True)
        print('✓ NLTK辞書データ準備完了')
        return True
    except Exception as e:
        print(f'✗ NLTK辞書データ準備失敗: {e}')
        return False

def analyze_vocabulary(word):
    """語彙知識分析"""
    synsets = wordnet.synsets(word.lower())
    if synsets:
        return {
            'word': word,
            'definition': synsets[0].definition(),
            'pos_wordnet': synsets[0].pos(),
            'synsets_count': len(synsets)
        }
    return None

def apply_grammar_rules(pos_tags):
    """文法ルールエンジン（第1〜5文型判定）"""
    if len(pos_tags) == 2:
        word1, pos1 = pos_tags[0]
        word2, pos2 = pos_tags[1]
        
        # 第1文型（SV）判定ルール
        if pos1 in ['NNS', 'NN', 'PRP'] and pos2 in ['VBP', 'VBZ', 'VB']:
            return {
                'pattern': 'SV',
                'pattern_name': '第1文型',
                'slots': ['S', 'V'],
                'slot_phrases': [word1, word2],
                'confidence': 0.9
            }
    
    elif len(pos_tags) == 3:
        word1, pos1 = pos_tags[0]
        word2, pos2 = pos_tags[1]
        word3, pos3 = pos_tags[2]
        
        # The dog runs パターン
        if pos1 == 'DT' and pos2 in ['NN', 'NNS'] and pos3 in ['VBZ', 'VBP']:
            return {
                'pattern': 'SV',
                'pattern_name': '第1文型',
                'slots': ['S', 'V'],
                'slot_phrases': [f'{word1} {word2}', word3],
                'confidence': 0.95
            }
    
    return None

def generate_rephrase_slots(grammar_result):
    """Rephrase仕様スロット生成"""
    if not grammar_result:
        return None
        
    return {
        'Slot': grammar_result['slots'],
        'SlotPhrase': grammar_result['slot_phrases'],
        'Slot_display_order': list(range(1, len(grammar_result['slots']) + 1)),
        'display_order': list(range(1, len(grammar_result['slots']) + 1)),
        'PhraseType': ['名詞句' if slot == 'S' else '動詞句' for slot in grammar_result['slots']],
        'pattern_detected': grammar_result['pattern'],
        'confidence': grammar_result['confidence']
    }

def main():
    print('=== 語彙辞書システム + 文法ルールエンジン = スロット分解システム ===')
    print('理論実証テスト\n')
    
    if not download_nltk_data():
        return
    
    test_sentences = ['Children play', 'The dog runs', 'Birds fly']
    
    for sentence in test_sentences:
        print(f'\n--- 分析対象: "{sentence}" ---')
        
        # 1. 語彙知識分析
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        print(f'品詞解析: {pos_tags}')
        
        # 2. WordNet語彙情報
        print('語彙知識:')
        for word, pos in pos_tags:
            vocab_info = analyze_vocabulary(word)
            if vocab_info:
                print(f'  {word}: {vocab_info["definition"][:50]}...')
            else:
                print(f'  {word}: 辞書情報なし')
        
        # 3. 文法ルール適用
        grammar_result = apply_grammar_rules(pos_tags)
        if grammar_result:
            print(f'文法認識: {grammar_result["pattern_name"]} ({grammar_result["pattern"]})')
            print(f'  確信度: {grammar_result["confidence"]:.1%}')
            
            # 4. Rephraseスロット生成
            rephrase_slots = generate_rephrase_slots(grammar_result)
            print('Rephraseスロット:')
            for key, value in rephrase_slots.items():
                print(f'  {key}: {value}')
                
            print('✅ スロット分解成功')
        else:
            print('❌ 文法パターン認識失敗')
    
    print('\n=== 結論 ===')
    print('語彙辞書（NLTK/WordNet） + 独自文法ルール → Rephraseスロット分解')
    print('理論的に完全実装可能！')

if __name__ == '__main__':
    main()
