"""
ユーザー指摘事項の確認テスト
182-188番ケースの修正内容を検証
"""

import json
from gerund_handler import GerundHandler

def test_user_corrections():
    """
    ユーザーの修正指示に従った182-188番ケースのテスト
    """
    # ハンドラーを初期化
    handler = GerundHandler()

    # 修正対象ケース
    test_cases = [
        ("I'm interested in learning French.", "182"),
        ("She is good at playing piano.", "183"),
        ("They are afraid of flying.", "184"),
        ("After finishing homework, I watch TV.", "186"),
        ("Before leaving home, she checked the weather.", "187"),
        ("Without saying anything, he left.", "188")
    ]

    print('🧪 ユーザー指摘事項の確認テスト')
    print('=' * 60)

    for sentence, case_num in test_cases:
        print(f'\n📝 ケース{case_num}: "{sentence}"')
        
        if handler.can_handle(sentence):
            result = handler.handle(sentence, f"gerund_prepositional")
            if result.get('success'):
                print(f'   ✅ 処理成功')
                main_slots = result.get("main_slots", {})
                sub_slots = result.get("sub_slots", {})
                
                print(f'   メインスロット: {main_slots}')
                print(f'   サブスロット: {sub_slots}')
                
                # 修正点の確認
                if case_num in ["182", "183"]:
                    if "sub-m2" in sub_slots and "sub-v" in sub_slots:
                        print(f'   ✅ 前置詞とV要素が正しく分離: sub-m2:"{sub_slots.get("sub-m2")}", sub-v:"{sub_slots.get("sub-v")}"')
                    else:
                        print(f'   ❌ 前置詞とV要素の分離に問題')
                        
                elif case_num == "184":
                    if main_slots.get("C1") == "afraid" and "sub-v" in sub_slots:
                        print(f'   ✅ C1:"afraid"とsub-v:"{sub_slots.get("sub-v")}"の分離OK')
                    else:
                        print(f'   ❌ C1とsub-vの分離に問題')
                        
                elif case_num in ["186", "187", "188"]:
                    if main_slots.get("M1") == "" and "sub-m1" in sub_slots:
                        print(f'   ✅ M1空でsub-m1:"{sub_slots.get("sub-m1")}"分離OK')
                    else:
                        print(f'   ❌ M1とsub-m1の分離に問題')
                        
            else:
                print(f'   ❌ 処理失敗: {result.get("error", "不明")}')
        else:
            print(f'   ❌ 動名詞として認識されず')

if __name__ == "__main__":
    test_user_corrections()
