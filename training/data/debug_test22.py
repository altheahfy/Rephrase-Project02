#!/usr/bin/env python3
"""Test22 詳細デバッグ"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_test22():
    print("Test22 detailed debug - missing main clause")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The person you mentioned is here."
    print(f"Sentence: {sentence}")
    print("="*50)
    
    # Stanza解析結果も確認
    stanza_result = mapper.nlp(sentence)
    print("Stanza dependency parsing:")
    for word in stanza_result.sentences[0].words:
        print(f"  {word.id}: '{word.text}' <- {word.head} ({word.deprel})")
    print("="*50)
    
    result = mapper.process(sentence)
    
    print("="*50)
    print("Final result:")
    print("Main slots:")
    for k, v in result['slots'].items():
        if v:
            print(f"  {k:3}: '{v}'")
        else:
            print(f"  {k:3}: (empty)")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        print(f"  {k}: '{v}'")
    
    print("\nExpected:")
    print("  V  : 'is'")
    print("  M2 : 'here'")
    print("  sub-s  : 'you'")
    print("  sub-v  : 'mentioned'")
    print("  sub-o1 : 'The person [omitted]'")
    print("\nProblem: Main clause 'is here' is completely missing!")

if __name__ == "__main__":
    debug_test22()
