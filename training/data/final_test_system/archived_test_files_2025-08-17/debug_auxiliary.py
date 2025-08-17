#!/usr/bin/env python3
"""助動詞ハンドラーデバッグスクリプト"""

import sys
sys.path.append('../')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_auxiliary_handler():
    print("🔧 助動詞ハンドラーデバッグ開始")
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('auxiliary_complex')  # 助動詞ハンドラー追加
    
    print(f"📋 Active handlers: {mapper.list_active_handlers()}")
    
    # Test 20: "He has finished his homework."
    test_sentence = "He has finished his homework."
    print(f"\n🧪 テスト文: {test_sentence}")
    
    result = mapper.process(test_sentence)
    print(f"📊 結果: {result}")
    
    # 期待値との比較
    expected = {"S": "He", "Aux": "has", "V": "finished", "O1": "his homework"}
    print(f"🎯 期待値: {expected}")
    
    # 比較
    missing_keys = []
    for key in expected:
        if key not in result:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ 欠損キー: {missing_keys}")
    else:
        print("✅ キー完全一致")

if __name__ == "__main__":
    debug_auxiliary_handler()
