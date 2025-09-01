import spacy
import sys
sys.path.append('.')

from noun_clause_handler import NounClauseHandler

# ===== デバッグ: noun_clause_handlerの実際の動作を確認 =====

def debug_noun_clause_handler():
    nlp = spacy.load("en_core_web_sm")
    
    sentence = "It depends on if you agree."
    doc = nlp(sentence)
    
    # spaCy解析結果を表示
    print(f"\n📝 Target: '{sentence}'")
    print(f"🔍 spaCy tokens:")
    for i, token in enumerate(doc):
        print(f"   {i}: '{token.text}' (pos={token.pos_}, dep={token.dep_})")
    
    # NounClauseHandlerインスタンスを作成
    handler = NounClauseHandler()
    
    # _detect_noun_clausesを直接テスト
    print(f"\n🧪 Testing _detect_noun_clauses():")
    detect_result = handler._detect_noun_clauses(doc, sentence)
    print(f"   _detect_noun_clauses: {detect_result}")
    
    # _detect_by_pos_analysisを直接テスト
    print(f"\n🧪 Testing _detect_by_pos_analysis():")
    pos_analysis_result = handler._detect_by_pos_analysis(doc, sentence)
    print(f"   _detect_by_pos_analysis: {pos_analysis_result}")
    
    # processをテスト（引数を修正）
    print(f"\n🧪 Testing process():")
    try:
        process_result = handler.process(sentence)
        print(f"   process: {process_result}")
    except Exception as e:
        print(f"   process error: {e}")

if __name__ == "__main__":
    debug_noun_clause_handler()
