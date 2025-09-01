"""
ConditionalHandler テスト用スクリプト
"""

from central_controller import CentralController

def test_conditional_sentences():
    """仮定法例文のテスト"""
    controller = CentralController()
    
    # 仮定法例文（131-155から抜粋）
    test_sentences = [
        "If I were rich, I would buy a car.",  # 131番
        "If she had studied harder, she would have passed the exam.",  # 132番
        "I wish I were taller.",  # 133番
        "She acts as if she knew everything.",  # 134番
        "Without your help, I would fail.",  # 135番
        "Were I rich, I would travel the world.",  # 倒置仮定法
        "Had she arrived earlier, she would have seen him.",  # 倒置仮定法
    ]
    
    print("=== 仮定法ハンドラーテスト ===\n")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"テスト{i}: {sentence}")
        print("-" * 50)
        
        # 仮定法パターン検出テスト
        conditional_handler = controller.handlers['conditional']
        patterns = conditional_handler.detect_conditional_patterns(sentence)
        print(f"🔍 検出パターン: {patterns}")
        
        # 全体処理テスト
        result = controller.process_sentence(sentence)
        
        if result['success']:
            print(f"✅ 処理成功")
            print(f"📝 main_slots: {result.get('main_slots', {})}")
            if 'sub_slots' in result:
                print(f"📝 sub_slots: {result['sub_slots']}")
            if 'metadata' in result:
                meta = result['metadata']
                print(f"🔧 primary_handler: {meta.get('primary_handler')}")
                print(f"🔧 conditional_info: {meta.get('conditional_info', {})}")
        else:
            print(f"❌ 処理失敗: {result.get('error', 'Unknown error')}")
        
        print("\n")

if __name__ == "__main__":
    test_conditional_sentences()
