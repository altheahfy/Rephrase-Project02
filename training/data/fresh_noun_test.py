#!/usr/bin/env python3
import sys
import importlib
import spacy

# モジュールキャッシュをクリア
if 'noun_clause_handler' in sys.modules:
    importlib.reload(sys.modules['noun_clause_handler'])

from noun_clause_handler import NounClauseHandler

def fresh_test():
    print("=== Fresh Module Test ===")
    
    nlp = spacy.load('en_core_web_sm')
    sentence = 'It depends on if you agree.'
    doc = nlp(sentence)
    
    print(f"Target: '{sentence}'")
    print(f"spaCy tokens:")
    for i, token in enumerate(doc):
        print(f"   {i}: '{token.text}' (pos={token.pos_}, dep={token.dep_})")
    
    handler = NounClauseHandler()
    
    print(f"\n🧪 Testing _detect_by_pos_analysis:")
    result = handler._detect_by_pos_analysis(doc, sentence)
    print(f"Final Result: {result}")
    
    return result

if __name__ == "__main__":
    fresh_test()
