#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
be動詞構文の実装テスト
"""

from pure_stanza_engine_v2 import PureStanzaEngine

def test_be_verb_constructions():
    """be動詞の3パターンをテスト"""
    engine = PureStanzaEngine()
    
    # テスト文
    test_sentences = [
        # 形容詞補語
        "He is happy.",
        "She is very intelligent.",
        
        # 名詞補語
        "He is a teacher.",
        "She is a brilliant student.",
        
        # 前置詞句補語
        "He was under intense pressure.",
        "They are in the classroom.",
        "She is at the library."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"テスト文: {sentence}")
        print(f"{'='*60}")
        
        try:
            result = engine.decompose(sentence)
            
            print(f"\n📊 分解結果:")
            for slot_name, slot_data in result.items():
                if isinstance(slot_data, dict) and 'main' in slot_data:
                    print(f"  {slot_name}: '{slot_data['main']}'")
                    
                    # サブスロット情報があれば表示
                    if len(slot_data) > 1:
                        print(f"    サブスロット:")
                        for sub_key, sub_value in slot_data.items():
                            if sub_key != 'main':
                                print(f"      {sub_key}: '{sub_value}'")
                else:
                    print(f"  {slot_name}: {slot_data}")
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_be_verb_constructions()
