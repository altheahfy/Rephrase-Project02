#!/usr/bin/env python3
"""
統一入れ子構造 複雑文テスト
"""

from pure_stanza_engine_v3_1_unified import PureStanzaEngineV31
import json

def test_complex_nesting():
    """複雑な入れ子構造のテスト"""
    engine = PureStanzaEngineV31()
    
    complex_sentences = [
        # 基本確認
        "The beautiful woman runs quickly.",
        # 複文テスト
        "The man who came yesterday knows the answer.",
        # 複雑修飾句
        "The book on the table is very interesting.",
        # 第4文型詳細
        "She gave the tall boy a new book.",
        # 第5文型
        "They made him very happy.",
    ]
    
    for sentence in complex_sentences:
        print(f"\n{'='*70}")
        print(f"複雑文テスト: {sentence}")
        print('='*70)
        
        try:
            result = engine.decompose_unified(sentence)
            
            print(f"\n📊 **最終結果構造:**")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_complex_nesting()
