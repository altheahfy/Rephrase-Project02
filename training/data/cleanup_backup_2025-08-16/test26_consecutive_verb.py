#!/usr/bin/env python3
"""Test26 連続動詞構文テスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_26():
    print("Test26: The door opened slowly creaked loudly.")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The door opened slowly creaked loudly."
    print(f"Sentence: {sentence}")
    
    result = mapper.process(sentence)
    
    print("\n=== CURRENT RESULT ===")
    print("Main slots:")
    for k, v in result['slots'].items():
        # 空文字列も表示（重要：従属節による空化を確認するため）
        print(f"  {k}: '{v}'")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        if v:
            print(f"  {k}: '{v}'")
    
    print("\n=== EXPECTED RESULT ===")
    print("S: '' (empty due to sub-slots)")
    print("V: 'creaked'")  
    print("M2: 'loudly'")
    print("sub-v: 'The door opened'")
    print("sub-m2: 'slowly'")

if __name__ == "__main__":
    test_26()
