"""
"The students study hard for exams." の分析
hardがM1期待の理由を調査
"""

import sys
sys.path.append('.')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def analyze_hard_placement():
    """hardの配置理由分析"""
    print("🔍 'The students study hard for exams.' 分析開始")
    
    mapper = UnifiedStanzaRephraseMapper()
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The students study hard for exams."
    
    # Stanza解析結果を詳細表示
    doc = mapper.stanza_pipeline(sentence)
    
    print("\n📋 Stanza解析結果:")
    for sent in doc.sentences:
        for word in sent.words:
            print(f"  {word.id}: '{word.text}' - POS:{word.upos}, deprel:{word.deprel}, head:{word.head}")
    
    # 動詞位置特定
    verb_position = None
    for sent in doc.sentences:
        for word in sent.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                verb_position = word.id
                print(f"\n🎯 動詞: '{word.text}' (位置: {word.id})")
                break
    
    # hardとfor examsの位置分析
    hard_position = None
    for_exams_start = None
    
    for sent in doc.sentences:
        for word in sent.words:
            if word.text.lower() == 'hard':
                hard_position = word.id
                print(f"📍 'hard' 位置: {word.id}")
            elif word.text.lower() == 'for':
                for_exams_start = word.id
                print(f"📍 'for exams' 開始位置: {word.id}")
    
    # 距離計算
    if verb_position and hard_position:
        hard_distance = abs(verb_position - hard_position)
        print(f"📏 hard距離: |{verb_position} - {hard_position}| = {hard_distance}")
    
    if verb_position and for_exams_start:
        for_distance = abs(verb_position - for_exams_start)
        print(f"📏 for exams距離: |{verb_position} - {for_exams_start}| = {for_distance}")
    
    # 文の構造分析
    total_words = len([w for sent in doc.sentences for w in sent.words])
    print(f"\n📊 文の長さ: {total_words}語")
    
    if hard_position:
        hard_ratio = hard_position / total_words
        print(f"📊 hard位置比率: {hard_position}/{total_words} = {hard_ratio:.2f}")
    
    if for_exams_start:
        for_ratio = for_exams_start / total_words
        print(f"📊 for exams位置比率: {for_exams_start}/{total_words} = {for_ratio:.2f}")
    
    # 期待値の理由推測
    print("\n🤔 M1期待の理由推測:")
    print("   1. 語順: study → hard → for exams")
    print("   2. 意味: hardは動作の様態（どのように勉強するか）")
    print("   3. 距離: studyの直後なので最も近い修飾語")
    print("   4. 文法: 副詞hardは動詞を直接修飾")
    
    # 実際の処理結果
    print("\n🔧 実際の処理結果:")
    result = mapper.process(sentence)
    slots = result.get('slots', {})
    print(f"   システム出力: {slots}")
    
    # M-slot分析
    m_slots = {k: v for k, v in slots.items() if k.startswith('M')}
    print(f"   M-slots: {m_slots}")

if __name__ == "__main__":
    analyze_hard_placement()
