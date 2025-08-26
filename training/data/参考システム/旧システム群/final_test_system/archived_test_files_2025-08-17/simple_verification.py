#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプルなシステム動作確認
unified_stanza_rephrase_mapper.pyが正しく動作するかだけをチェック
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def simple_verification():
    """シンプルなシステム動作確認"""
    print("🔧 システム動作確認")
    print("="*50)
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    # テスト例文
    test_sentences = [
        "The car is red.",
        "I love you.",
        "The man who runs fast is strong.",
        "The book was written by John.",
        "The students study hard for exams."
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 例文: {sentence}")
        
        # システム実行
        result = mapper.process(sentence)
        
        # 結果表示
        slots = result.get('slots', {})
        sub_slots = result.get('sub_slots', {})
        
        print("結果:")
        if slots:
            for k, v in slots.items():
                if v.strip():
                    print(f"  {k}: {v}")
        
        if sub_slots:
            for k, v in sub_slots.items():
                if v.strip():
                    print(f"  {k}: {v}")
        
        if not slots and not sub_slots:
            print("  スロット検出なし")
    
    print("\n✅ システム動作確認完了")

if __name__ == "__main__":
    simple_verification()
