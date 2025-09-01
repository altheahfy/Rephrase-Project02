import spacy
import sys
sys.path.append('.')

from noun_clause_handler import NounClauseHandler

# ===== デバッグ: _detect_by_pos_analysisの詳細動作確認 =====

def debug_pos_analysis():
    nlp = spacy.load("en_core_web_sm")
    
    sentence = "It depends on if you agree."
    doc = nlp(sentence)
    
    print(f"\n📝 Target: '{sentence}'")
    print(f"🔍 spaCy tokens:")
    for i, token in enumerate(doc):
        print(f"   {i}: '{token.text}' (pos={token.pos_}, dep={token.dep_})")
    
    # 手動でループを実行
    print(f"\n🔍 Manual loop through _detect_by_pos_analysis logic:")
    
    for i, token in enumerate(doc):
        print(f"\n  Token {i}: '{token.text}'")
        
        if token.text.lower() in ['that', 'whether', 'if']:
            print(f"    ✅ Found connector: '{token.text.lower()}'")
            
            if i > 0:
                print(f"    ✅ i > 0: {i} > 0")
                print(f"    Previous token: '{doc[i-1].text}' (pos={doc[i-1].pos_})")
                
                if doc[i-1].pos_ == 'ADP':
                    print(f"    ✅ Previous is ADP!")
                    print(f"    🎯 Should return result!")
                    result = {
                        'type': 'if_clause_noun',
                        'position': 'prepositional_object',
                        'connector': token.text.lower(),
                        'preposition': doc[i-1].text,
                        'clause_range': (i, len(doc))
                    }
                    print(f"    Result: {result}")
                else:
                    print(f"    ❌ Previous is not ADP: {doc[i-1].pos_}")
            else:
                print(f"    ❌ i is not > 0: {i}")
        else:
            print(f"    - Not a connector: '{token.text.lower()}'")
    
    print(f"\n🧪 Testing actual method:")
    handler = NounClauseHandler()
    result = handler._detect_by_pos_analysis(doc, sentence)
    print(f"    _detect_by_pos_analysis result: {result}")

if __name__ == "__main__":
    debug_pos_analysis()
