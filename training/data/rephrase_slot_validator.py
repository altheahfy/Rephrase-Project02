"""
Rephrase Slot Structure Validator
絶対的スロット構造バリデーション機能

このモジュールは、RephraseプロジェクトでAIアシスタントが
間違ったスロット構造を生成することを防止します。

使用方法:
from rephrase_slot_validator import validate_slots, get_valid_slots

# スロット分解前に必ず実行
if not validate_slots(your_slots_dict):
    print("エラー: 無効なスロット構造です")
"""

# 正式Rephraseスロット定義（2025-08-13 ユーザー確認済み）
VALID_UPPER_SLOTS = {
    'M1', 'S', 'Aux', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3'
}

VALID_SUB_SLOTS = {
    'sub-m1', 'sub-s', 'sub-aux', 'sub-m2', 'sub-v', 
    'sub-c1', 'sub-o1', 'sub-o2', 'sub-c2', 'sub-m3'
}

# サブスロットを持つ上位スロット
SLOTS_WITH_SUBSLOTS = {
    'M1', 'S', 'M2', 'C1', 'O1', 'O2', 'C2', 'M3'
}

# サブスロットを持たない上位スロット
SLOTS_WITHOUT_SUBSLOTS = {'Aux', 'V'}

def validate_slots(slots_dict: dict) -> bool:
    """
    Rephraseスロット構造の強制バリデーション
    
    Args:
        slots_dict: スロット名をキーとする辞書
        
    Returns:
        bool: 全スロットが有効な場合True
    """
    invalid_slots = []
    
    for slot_name in slots_dict.keys():
        if slot_name not in VALID_UPPER_SLOTS and slot_name not in VALID_SUB_SLOTS:
            invalid_slots.append(slot_name)
    
    if invalid_slots:
        print(f"❌ 無効なRephraseスロット検出: {invalid_slots}")
        print(f"✅ 有効な上位スロット: {sorted(VALID_UPPER_SLOTS)}")
        print(f"✅ 有効なサブスロット: {sorted(VALID_SUB_SLOTS)}")
        return False
    
    return True

def get_valid_slots():
    """有効なスロット一覧を取得"""
    return {
        'upper_slots': VALID_UPPER_SLOTS,
        'sub_slots': VALID_SUB_SLOTS,
        'slots_with_subslots': SLOTS_WITH_SUBSLOTS,
        'slots_without_subslots': SLOTS_WITHOUT_SUBSLOTS
    }

def show_slot_structure():
    """Rephraseスロット構造の表示"""
    print("=== Rephrase正式スロット構造 ===")
    print("上位スロット:", sorted(VALID_UPPER_SLOTS))
    print("サブスロット:", sorted(VALID_SUB_SLOTS))
    print()
    
    print("各上位スロットのサブスロット:")
    for slot in sorted(SLOTS_WITH_SUBSLOTS):
        print(f"  {slot}: {sorted(VALID_SUB_SLOTS)}")
    
    print("サブスロットなし:")
    for slot in sorted(SLOTS_WITHOUT_SUBSLOTS):
        print(f"  {slot}: (サブスロットなし)")

def create_type_clause_template(upper_slot: str):
    """Type Clause用テンプレート作成"""
    if upper_slot not in SLOTS_WITH_SUBSLOTS:
        return None
    
    template = {upper_slot: ""}  # Type Clauseは上位スロット空
    # 必要に応じてサブスロット追加
    return template

if __name__ == "__main__":
    # テスト実行
    show_slot_structure()
    
    # テスト例
    test_slots = {
        'S': 'I', 'Aux': 'must', 'V': 'go',
        'M1': '', 'sub-m1': 'because', 'sub-s': 'he', 
        'sub-aux': 'was', 'sub-v': 'captured'
    }
    
    print(f"\nテスト結果: {validate_slots(test_slots)}")
