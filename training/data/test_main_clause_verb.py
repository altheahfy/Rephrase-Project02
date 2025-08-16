#!/usr/bin/env python3
"""
主文動詞検出テスト
関係節の動詞と主文の動詞が正しく区別されるかテスト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_main_clause_verb_detection():
    """主文動詞検出のテスト"""
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')  # 基本5文型ハンドラーを追加
    mapper.add_handler('relative_clause')
    
    # 主文動詞検出のテストケース
    test_cases = [
        ('The book which I bought is expensive.', 'is'),
        ('The man who lives there works hard.', 'works'),
        ('The car that was stolen was found.', 'was'),
        ('I know the person whose dog barks.', 'know')
    ]
    
    print('🧪 主文動詞検出テスト開始')
    print('=' * 60)
    
    success_count = 0
    
    for i, (test_sentence, expected_verb) in enumerate(test_cases, 1):
        print(f'\n📖 テスト{i}: "{test_sentence}"')
        print('-' * 50)
        
        try:
            result = mapper.process(test_sentence)
            slots = result.get('slots', {})
            positional_sub_slots = result.get('positional_sub_slots', {})
            
            print(f'メインスロット:')
            for slot_name in ['S', 'V', 'C1', 'O1', 'O2']:
                if slot_name in slots and slots[slot_name]:
                    print(f'  {slot_name}: "{slots[slot_name]}"')
            
            print(f'位置別サブスロット:')
            for pos_slot_name, sub_slots in positional_sub_slots.items():
                if sub_slots:
                    print(f'  {pos_slot_name}: {sub_slots}')
            
            # 主文動詞が正しく特定されているかチェック
            actual_verb = slots.get('V', '')
            
            if actual_verb.lower() == expected_verb.lower():
                print(f'✅ 主文動詞検出成功: V="{actual_verb}"')
                success_count += 1
            else:
                print(f'❌ 主文動詞検出失敗: V="{actual_verb}" (期待値: "{expected_verb}")')
                
        except Exception as e:
            print(f'❌ エラー: {e}')
            import traceback
            traceback.print_exc()
    
    print(f'\n🏁 主文動詞検出テスト完了')
    print(f'成功: {success_count}/{len(test_cases)} テスト')
    
    if success_count == len(test_cases):
        print('✅ 全テスト成功！主文動詞検出が正常に動作しています。')
    else:
        print('❌ 一部テスト失敗。主文動詞検出ロジックの調整が必要です。')
    
    return success_count == len(test_cases)

if __name__ == '__main__':
    test_main_clause_verb_detection()
