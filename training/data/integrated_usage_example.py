#!/usr/bin/env python3
"""
統合されたCentralControllerの使用例
UIから直接ロードできる形での使用方法
"""

from central_controller import CentralController

def demonstrate_integrated_usage():
    """統合CentralControllerの使用デモ"""
    print("🚀 統合CentralController使用デモ")
    print("=" * 60)
    
    # 1. CentralControllerを初期化
    controller = CentralController()
    
    # 2. テスト例文
    test_sentences = [
        "We always eat breakfast together.",           # action群（副詞付き）
        "What did he tell her at the store?",          # tell群（疑問文）
        "She carefully reads books.",                  # action群（副詞）
        "Did he tell her a secret there?",             # tell群
        "Actually, she works very hard.",              # action群（文頭副詞）
    ]
    
    print("📚 テスト例文:")
    for i, sentence in enumerate(test_sentences, 1):
        print(f"  {i}. {sentence}")
    
    print("\n" + "=" * 60)
    print("🔍 処理結果:")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 例文{i}: {sentence}")
        print("-" * 40)
        
        # 3. 統合処理（一回の呼び出しですべて完了）
        result = controller.process_sentence(sentence)
        
        # 4. 結果表示
        if result.get('success'):
            main_slots = result.get('main_slots', {})
            ordered_slots = result.get('ordered_slots', {})
            
            print(f"✅ 処理成功:")
            print(f"   📊 スロット構造: {main_slots}")
            print(f"   🔢 順序情報: {ordered_slots}")
            
            # 順序通りの語順を再構成
            if ordered_slots:
                ordered_words = []
                for pos in sorted(ordered_slots.keys(), key=int):
                    ordered_words.append(ordered_slots[pos])
                print(f"   📝 語順: {' '.join(ordered_words)}")
            
            # メタデータ
            metadata = result.get('metadata', {})
            if metadata:
                print(f"   📋 メタデータ: {metadata}")
        else:
            print(f"❌ 処理失敗: {result.get('error', '不明なエラー')}")

def ui_integration_example():
    """UI統合用の簡潔な使用例"""
    print("\n" + "=" * 60)
    print("🖥️ UI統合用シンプル使用例")
    print("=" * 60)
    
    controller = CentralController()
    
    # UI想定：ユーザー入力文
    user_input = "We always eat breakfast together."
    
    # 一行で処理完了
    result = controller.process_sentence(user_input)
    
    # UIが必要な情報を取得
    slots = result.get('main_slots', {})           # スロット構造
    order = result.get('ordered_slots', {})        # 順序情報
    success = result.get('success', False)         # 成功/失敗
    
    print(f"入力: {user_input}")
    print(f"成功: {success}")
    print(f"スロット: {slots}")
    print(f"順序: {order}")
    
    return {
        'input': user_input,
        'success': success,
        'slots': slots,
        'order': order
    }

def api_style_usage():
    """API風の使用例"""
    print("\n" + "=" * 60)
    print("🌐 API風使用例")
    print("=" * 60)
    
    def process_rephrase_sentence(sentence: str) -> dict:
        """
        Rephrase文処理API風関数
        
        Args:
            sentence: 処理する英語文
            
        Returns:
            dict: 処理結果（スロット+順序）
        """
        controller = CentralController()
        return controller.process_sentence(sentence)
    
    # API使用例
    sentences = [
        "She sings beautifully.",
        "What did you tell me yesterday?",
        "They run fast."
    ]
    
    results = []
    for sentence in sentences:
        result = process_rephrase_sentence(sentence)
        results.append(result)
        
        print(f"📝 '{sentence}'")
        print(f"   → スロット: {result.get('main_slots', {})}")
        print(f"   → 順序: {result.get('ordered_slots', {})}")
    
    return results

if __name__ == "__main__":
    # デモ実行
    demonstrate_integrated_usage()
    ui_integration_example()
    api_style_usage()
