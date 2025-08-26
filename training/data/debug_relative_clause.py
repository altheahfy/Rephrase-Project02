#!/usr/bin/env python3
"""関係節処理の詳細デバッグスクリプト"""

import spacy
from relative_clause_handler import RelativeClauseHandler

def debug_relative_clause_processing():
    """関係節処理の各ステップを詳細に確認"""
    handler = RelativeClauseHandler()
    
    test_case = "The man who runs fast is strong."
    
    print(f"=== デバッグ: '{test_case}' ===")
    
    # Step 1: 関係節部分抽出をテスト
    clause_text = handler._extract_relative_clause_text(test_case, 'who')
    print(f"Step 1 - 関係節抽出: '{clause_text}'")
    
    # Step 2: AdverbHandler処理をテスト
    if handler.adverb_handler:
        adverb_result = handler.adverb_handler.process(clause_text)
        print(f"Step 2 - AdverbHandler結果: {adverb_result}")
        
        if adverb_result.get('success'):
            cleaned_clause = adverb_result.get('separated_text', clause_text)
            print(f"Step 2 - 清理されたテキスト: '{cleaned_clause}'")
            
            # 修飾語情報の変換処理をテスト
            raw_modifiers = adverb_result.get('modifiers', {})
            modifiers = {}
            
            if raw_modifiers:
                modifier_texts = []
                for pos_idx, modifier_list in raw_modifiers.items():
                    print(f"位置 {pos_idx}: {modifier_list}")
                    if isinstance(modifier_list, list):
                        for modifier_info in modifier_list:
                            if isinstance(modifier_info, dict) and 'text' in modifier_info:
                                modifier_texts.append(modifier_info['text'])
                                print(f"修飾語テキスト追加: '{modifier_info['text']}'")
                
                if modifier_texts:
                    modifiers['M2'] = ' '.join(modifier_texts)
                    print(f"最終M2値: '{modifiers['M2']}'")
                else:
                    print("修飾語テキストが空")
            else:
                print("raw_modifiersが空")
    
    # Step 3: 完全な_analyze_relative_clause呼び出しをテスト
    analysis = handler._analyze_relative_clause(test_case, 'who')
    print(f"Step 3 - 完全分析結果:")
    print(f"  success: {analysis.get('success')}")
    print(f"  modifiers: {analysis.get('modifiers', 'なし')}")
    
    # Step 4: _process_who呼び出しをテスト
    who_result = handler._process_who(test_case)
    print(f"Step 4 - _process_who結果:")
    print(f"  success: {who_result.get('success')}")
    print(f"  sub_slots: {who_result.get('sub_slots', 'なし')}")

if __name__ == "__main__":
    debug_relative_clause_processing()
