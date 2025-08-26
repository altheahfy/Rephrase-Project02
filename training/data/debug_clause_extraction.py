#!/usr/bin/env python3
"""デバッグ：関係節テキスト抽出確認"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def debug_clause_extraction():
    """関係節テキスト抽出をデバッグ"""
    
    adverb_handler = AdverbHandler()
    collaborators = {
        'AdverbHandler': adverb_handler
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # オリジナルテキストを設定
    full_text = "The book which lies there"
    rel_handler.original_text = full_text
    
    # 関係節テキスト抽出をテスト
    print("🔍 関係節テキスト抽出テスト:")
    print(f"フルテキスト: '{full_text}'")
    
    clause_text = rel_handler._extract_relative_clause_text_original(full_text, 'which')
    print(f"抽出結果: '{clause_text}'")
    
    # AdverbHandlerに渡されるテキストを確認
    print(f"\n🔍 AdverbHandlerに渡されるテキスト: '{clause_text}'")
    
    if clause_text:
        adverb_result = adverb_handler.process(clause_text)
        print("AdverbHandler結果:")
        print(json.dumps(adverb_result, indent=2, ensure_ascii=False))
        
        # 修飾語変換ロジックを手動テスト
        raw_modifiers = adverb_result.get('modifiers', {})
        modifiers = {}
        
        if raw_modifiers:
            modifier_texts = []
            for pos_idx, modifier_list in raw_modifiers.items():
                print(f"インデックス {pos_idx}: {modifier_list}")
                if isinstance(modifier_list, list):
                    for modifier_info in modifier_list:
                        if isinstance(modifier_info, dict) and 'text' in modifier_info:
                            modifier_texts.append(modifier_info['text'])
                            print(f"修飾語追加: '{modifier_info['text']}'")
            
            if modifier_texts:
                modifiers['M2'] = ' '.join(modifier_texts)
                print(f"最終M2: '{modifiers['M2']}'")

if __name__ == "__main__":
    debug_clause_extraction()
