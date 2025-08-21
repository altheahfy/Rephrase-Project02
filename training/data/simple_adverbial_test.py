"""
AdverbialPattern統合テスト
ParticiplePatternと同じ構造での統合動作確認
"""

import sys
import os

# パス設定
sys.path.append(os.path.abspath('.'))

# 統合システムのインポート
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_adverbial_pattern_integration():
    """AdverbialPatternの統合テスト"""
    
    print("=== AdverbialPattern統合テスト開始 ===")
    
    # 統合システム初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    # テストケース: 複合副詞句
    test_cases = [
        "He spoke very carefully.",        # very + carefully (ADV + ADV)
        "She worked quite slowly.",        # quite + slowly (ADV + ADV)  
        "They moved extremely fast.",      # extremely + fast (ADV + ADV)
        "The dog barked very loudly.",     # very + loudly (複合副詞 + 他要素)
    ]
    
    print("\n--- 複合副詞句テスト ---")
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{sentence}'")
        
        try:
            # 統合処理実行
            result = mapper.process(sentence)
            
            # 結果表示
            if result and 'slots' in result:
                slots = result['slots']
                sub_slots = result.get('sub_slots', {})
                
                print(f"  スロット: {slots}")
                if sub_slots:
                    print(f"  サブスロット: {sub_slots}")
                    
                # AdverbialPattern検出確認
                grammar_info = result.get('grammar_info', {})
                detected = grammar_info.get('detected_patterns', [])
                if 'adverbial_construction' in detected:
                    print(f"  ✓ AdverbialPattern検出成功")
                    control_flags = grammar_info.get('control_flags', {})
                    if control_flags.get('adverbial_detected'):
                        print(f"  ✓ 副詞構文フラグ設定済み")
                        print(f"  副詞タイプ: {control_flags.get('adverb_type', 'unknown')}")
                else:
                    print(f"  ✗ AdverbialPattern未検出")
            else:
                print(f"  ✗ 処理失敗: {result}")
                
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            import traceback
            traceback.print_exc()

def test_direct_adverbial_pattern():
    """AdverbialPattern直接テスト - スキップ（統合テスト優先）"""
    
    print("\n\n=== AdverbialPattern直接テスト ===")
    print("統合テスト優先のため一時スキップ")

if __name__ == "__main__":
    test_adverbial_pattern_integration()
    # test_direct_adverbial_pattern()  # 統合テスト成功後に実行
