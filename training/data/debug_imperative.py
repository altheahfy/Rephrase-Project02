"""
命令文の基本分解デバッグツール
"please call me."のような簡単な命令文が分解できない問題を解析
"""

from central_controller import CentralController
import spacy

def test_imperative_sentences():
    controller = CentralController()
    nlp = spacy.load("en_core_web_sm")
    
    # 失敗する主節のテスト
    test_sentences = [
        "please call me.",
        "call me.",
        "didn't know that already.",
        "But for your help",
        "Without your support"
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*50}")
        print(f"🔍 テスト: '{sentence}'")
        print(f"{'='*50}")
        
        # spaCy解析
        doc = nlp(sentence)
        print(f"\n📋 spaCy解析:")
        for token in doc:
            print(f"   {token.i:2d}: '{token.text:10s}' dep={token.dep_:10s} pos={token.pos_:5s} tag={token.tag_:6s}")
        
        # 副詞分離テスト
        adverb_handler = controller.handlers['adverb']
        adverb_result = adverb_handler.process(sentence)
        print(f"\n📝 副詞分離結果:")
        print(f"   成功: {adverb_result['success']}")
        print(f"   分離後テキスト: '{adverb_result.get('separated_text', sentence)}'")
        print(f"   修飾語スロット: {adverb_result.get('modifier_slots', {})}")
        
        # 5文型分解テスト
        processing_text = adverb_result.get('separated_text', sentence)
        five_pattern_handler = controller.handlers['basic_five_pattern']
        five_result = five_pattern_handler.process(processing_text)
        print(f"\n⚙️ 5文型分解結果:")
        print(f"   成功: {five_result['success']}")
        if five_result['success']:
            print(f"   スロット: {five_result.get('slots', {})}")
        else:
            print(f"   エラー: {five_result.get('error', 'Unknown error')}")
        
        # 基本分解全体テスト
        basic_result = controller._process_basic_decomposition(sentence)
        print(f"\n🔧 基本分解全体結果:")
        print(f"   成功: {basic_result['success']}")
        if basic_result['success']:
            print(f"   メインスロット: {basic_result.get('main_slots', {})}")
        else:
            print(f"   エラー: {basic_result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_imperative_sentences()
