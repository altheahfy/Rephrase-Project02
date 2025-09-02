"""
動名詞ハンドラー修正版テスト
Rephrase的スロット分解ルールに従った処理の確認
"""

import json
from gerund_handler import GerundHandler

def test_gerund_handler_corrections():
    """
    ユーザーの修正指示に従った動名詞ハンドラーのテスト
    """
    # ハンドラーを初期化
    handler = GerundHandler()

    # テストケースから修正済みの例文をテスト
    test_cases = [
        ('I am interested in learning English.', 'gerund_prep_complex'),
        ('She keeps talking about movies.', 'gerund_keep_doing'),
        ('My hobby is reading novels.', 'gerund_complement_complex'),
        ('He is good at playing guitar.', 'gerund_good_at'),
        ('I enjoy reading books.', 'gerund_object_complex'),
        ('Reading books is my hobby.', 'gerund_subject_complex')
    ]

    print('🧪 動名詞ハンドラー修正版テスト')
    print('=' * 50)

    for sentence, v_group_key in test_cases:
        print(f'\n📝 テスト: "{sentence}"')
        print(f'   期待パターン: {v_group_key}')
        
        if handler.can_handle(sentence):
            result = handler.handle(sentence, v_group_key)
            if result.get('success'):
                print(f'   ✅ 成功')
                print(f'   メインスロット: {result.get("main_slots", {})}')
                print(f'   サブスロット: {result.get("sub_slots", {})}')
                
                # 修正指示の確認
                sub_slots = result.get("sub_slots", {})
                if sub_slots:
                    if "sub-c2" in sub_slots:
                        print(f'   ⚠️ 注意: sub-c2 が使用されています (sub-m2 に変更推奨)')
            else:
                print(f'   ❌ 処理失敗: {result.get("error", "不明")}')
        else:
            print(f'   ❌ 動名詞として認識されず')

if __name__ == "__main__":
    test_gerund_handler_corrections()
