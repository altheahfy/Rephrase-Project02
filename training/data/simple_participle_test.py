#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple ParticiplePattern Test
修正されたParticiplePatternの動作確認
"""

import sys
import stanza
sys.path.append('.')

from universal_slot_system.patterns.participle_pattern import ParticiplePattern
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_participle_integration():
    """分詞構文統合テスト"""
    
    print("=== ParticiplePattern 統合テスト ===")
    
    # Stanza初期化
    print("Stanza初期化中...")
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', use_gpu=False)
    
    # システム初期化
    print("システム初期化中...")
    unified_mapper = UnifiedStanzaRephraseMapper()
    participle_pattern = ParticiplePattern()
    
    # テスト文
    test_sentences = [
        "The man working overtime finished late",
        "The dog barking loudly disturbed neighbors", 
        "Walking slowly through the park she enjoyed nature"
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n--- テスト {i}: {sentence} ---")
        
        # Stanza解析
        doc = nlp(sentence)
        
        # ParticiplePattern直接テスト
        pattern_detected = participle_pattern.detect(doc, sentence)
        print(f"ParticiplePattern検出: {pattern_detected}")
        
        # 統合システムテスト
        try:
            result = unified_mapper.process(sentence)
            if result and 'slots' in result:
                slots = result['slots']
                confidence = result.get('confidence', 0.0)
                print(f"統合システム結果: {len(slots)} スロット, 信頼度: {confidence:.3f}")
                
                # 分詞関連スロット確認
                all_result_keys = list(result.keys())
                print(f"結果キー: {all_result_keys}")
                
                participle_slots = {k: v for k, v in slots.items() if 'sub-' in k}
                if participle_slots:
                    print(f"分詞サブスロット: {participle_slots}")
                else:
                    print("分詞サブスロット: なし")
                    
                # 主要スロット表示
                main_slots = {k: v for k, v in slots.items() if not k.startswith('sub-')}
                print(f"メインスロット: {main_slots}")
                
                # メタ情報確認
                meta = result.get('meta', {})
                processing_time = meta.get('processing_time', 0)
                print(f"処理時間: {processing_time:.3f}s")
                
            else:
                print("統合システム結果: なし")
                if result:
                    print(f"受信した結果構造: {list(result.keys())}")
                
        except Exception as e:
            print(f"統合システムエラー: {e}")
    
    print("\n=== テスト完了 ===")

if __name__ == "__main__":
    test_participle_integration()
