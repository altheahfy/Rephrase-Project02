#!/usr/bin/env python3
"""
比較級・最上級ハンドラーテストスクリプト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import json

def test_comparative_superlative():
    """比較級・最上級ハンドラーのテスト"""
    
    # テスト例文
    test_sentences = [
        'This book is bigger than that one.',
        'She is the smartest of all the students.',
        'He runs faster than anyone else.',
        'This is the most beautiful flower.',
        'Today is more interesting than yesterday.',
        'Mount Everest is the highest mountain in the world.'
    ]

    mapper = DynamicGrammarMapper()
    print('🎯 比較級・最上級ハンドラーテスト開始')
    print(f'アクティブハンドラー: {mapper.active_handlers}')
    print()

    results = []
    for i, sentence in enumerate(test_sentences, 1):
        print(f'--- テスト {i}: {sentence} ---')
        try:
            result = mapper.analyze_sentence(sentence)
            
            # 結果表示
            main_slots = result.get('main_slots', {})
            sub_slots = result.get('sub_slots', {})
            
            print(f'メインスロット: {main_slots}')
            print(f'サブスロット: {sub_slots}')
            
            if 'unified_handlers' in result:
                detected = result['unified_handlers'].get('detected_patterns', [])
                print(f'検出パターン: {[p.get("type") for p in detected]}')
                
                # 比較級・最上級が検出されたかチェック
                comparative_detected = any(p.get('type') == 'comparative_superlative' for p in detected)
                print(f'比較級・最上級検出: {"✅" if comparative_detected else "❌"}')
            
            results.append({
                'sentence': sentence,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'success': bool(main_slots)
            })
            
        except Exception as e:
            print(f'❌ エラー: {e}')
            results.append({
                'sentence': sentence,
                'error': str(e),
                'success': False
            })
        
        print()
    
    # サマリー表示
    success_count = sum(1 for r in results if r['success'])
    print(f"🎯 テスト結果サマリー: {success_count}/{len(test_sentences)} 成功")
    
    return results

if __name__ == "__main__":
    test_comparative_superlative()
