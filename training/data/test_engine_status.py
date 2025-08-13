#!/usr/bin/env python3
"""
Grammar Master Controller v2 のエンジン登録状況確認テスト
"""

try:
    from grammar_master_controller_v2 import GrammarMasterControllerV2
    
    print("=== Grammar Master Controller v2 エンジン登録状況 ===")
    controller = GrammarMasterControllerV2()
    
    print(f"総エンジン数: {len(controller.engine_registry)}")
    print()
    
    for engine_type, info in controller.engine_registry.items():
        print(f"Priority {info.priority:2d}: {engine_type.value:15s} - {info.description}")
    
    print("\n=== 簡単な処理テスト ===")
    
    # テスト例文
    test_sentences = [
        "I can see.",
        "She is running.",
        "The cat sits on the table."
    ]
    
    for sentence in test_sentences:
        print(f"\nテスト文: {sentence}")
        try:
            result = controller.process_sentence(sentence, debug=False)
            print(f"成功: {result.success}")
            print(f"エンジン: {result.engine_type.value}")
            print(f"スロット: {result.slots}")
        except Exception as e:
            print(f"エラー: {e}")
            
except ImportError as e:
    print(f"インポートエラー: {e}")
except Exception as e:
    print(f"予期しないエラー: {e}")
