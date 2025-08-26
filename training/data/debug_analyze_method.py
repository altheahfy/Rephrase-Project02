#!/usr/bin/env python3
"""デバッグ：_analyze_relative_clauseでの修飾語取得"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def debug_analyze_method():
    """_analyze_relative_clauseでの修飾語取得をデバッグ"""
    
    adverb_handler = AdverbHandler()
    collaborators = {
        'AdverbHandler': adverb_handler
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # processメソッドを通して実行
    full_text = "The book which lies there"
    
    print("🔍 processメソッド経由テスト:")
    print(f"入力: '{full_text}'")
    
    # processメソッド内での_analyze_relative_clauseの動作を確認
    # 一旦、_analyze_relative_clauseに直接アクセス
    
    # original_textを手動設定してテスト
    rel_handler.original_text = full_text
    
    # Step 1: 関係節テキスト抽出（協力者情報確認）
    original_clause_text = rel_handler._extract_relative_clause_text_original(full_text, 'which')
    print(f"抽出された関係節: '{original_clause_text}'")
    
    # Step 2: AdverbHandler協力
    if rel_handler.adverb_handler and original_clause_text:
        adverb_result = rel_handler.adverb_handler.process(original_clause_text)
        print("AdverbHandler結果:")
        print(json.dumps(adverb_result, indent=2, ensure_ascii=False))
        
        modifiers = {}
        if adverb_result.get('success'):
            raw_modifiers = adverb_result.get('modifiers', {})
            
            if raw_modifiers:
                modifier_texts = []
                for pos_idx, modifier_list in raw_modifiers.items():
                    if isinstance(modifier_list, list):
                        for modifier_info in modifier_list:
                            if isinstance(modifier_info, dict) and 'text' in modifier_info:
                                modifier_texts.append(modifier_info['text'])
                
                if modifier_texts:
                    modifiers['M2'] = ' '.join(modifier_texts)
        
        print(f"変換後modifiers: {modifiers}")
    
    # Step 3: 実際の_analyze_relative_clauseメソッド実行
    print(f"\n🔍 _analyze_relative_clause実行:")
    analysis = rel_handler._analyze_relative_clause(full_text, 'which')
    
    # modifiersキーのみ表示
    print(f"戻り値のmodifiers: {analysis.get('modifiers', {})}")

if __name__ == "__main__":
    debug_analyze_method()
