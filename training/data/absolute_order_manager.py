#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AbsoluteOrderManager - グループ別絶対順序システム
"""

class AbsoluteOrderManager:
    def __init__(self):
        # グループ別相対順序ルール定義（動的絶対位置計算用）
        self.group_rules = {
            "tell": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "M2_END"],
                "description": "tell系動詞: M1冒頭 < M2疑問詞 < Aux < S < V < O1 < O2 < M2文末"
            },
            "give": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "M2_END"],
                "description": "give系動詞: S V O1 O2 の語順"
            },
            "be": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "C1", "C2", "M2_END"],
                "description": "be動詞: Aux S V C1 の語順"
            },
            "action": {
                "relative_order": ["M1", "Aux", "S", "V", "O1", "O2", "M2", "C1", "C2", "M2_END"],
                "description": "一般動詞: M1(時間) S V O1 O2 M2(様態) M2_END(場所)"
            },
            "passive": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "C2", "M2_END"],
                "description": "受動態: S be V C2 の語順"
            },
            # 他のグループは後で追加
            "default": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "C1", "C2", "M2_END"],
                "description": "デフォルト相対順序"
            }
        }
        
        # wh-word識別子による疑問詞制御
        self.wh_word_slots = {
            "what": "O2",
            "where": "M2", 
            "when": "M2",
            "why": "M2",
            "how": "M2",
            "who": "S",
            "whom": "O1"
        }
    
    def apply_absolute_order(self, slots, v_group_key, wh_word=None, group_population=None):
        """
        汎用グループ人口分析による絶対順序計算
        
        Args:
            slots (dict): スロット情報 {"S": "he", "V": "tell", "O1": "her", ...}
            v_group_key (str): 動詞グループキー ("tell", "give", etc.)
            wh_word (str): 疑問詞 ("what", "where", etc.)
            group_population (set): グループ全体に存在する要素セット（省略時は個別分析）
            
        Returns:
            list: 絶対順序でソートされたスロット配列
        """
        print(f"=== AbsoluteOrderManager.apply_absolute_order (Universal Group Population Analysis) ===")
        print(f"Input slots: {slots}")
        print(f"V_group_key: {v_group_key}")
        print(f"wh_word: {wh_word}")
        print(f"Group population: {group_population}")
        
        # 汎用相対順序システムで処理
        return self._apply_universal_relative_order_system(slots, v_group_key, wh_word, group_population)
    
    def _apply_universal_relative_order_system(self, slots, v_group_key, wh_word, group_population):
        """
        汎用相対順序システム（全V_group_key対応）
        """
        print("Using universal relative order system")
        
        # グループルールを取得
        if v_group_key in self.group_rules:
            group_rule = self.group_rules[v_group_key]
            relative_order = group_rule.get("relative_order", [])
        else:
            group_rule = self.group_rules["default"]
            relative_order = group_rule.get("relative_order", [])
        
        print(f"Using relative order: {relative_order}")
        
        # スロット名マッピング（M3 → M2_END等）
        mapped_slots = {}
        original_slot_names = {}
        for slot_name, slot_value in slots.items():
            if slot_name == "M3":
                mapped_slots["M2_END"] = slot_value
                original_slot_names["M2_END"] = slot_name
            else:
                mapped_slots[slot_name] = slot_value
                original_slot_names[slot_name] = slot_name
        
        # グループ人口分析に基づく絶対位置計算
        if group_population:
            # グループ全体に存在する要素を考慮した位置計算
            present_slots = group_population
            print(f"Using group population: {present_slots}")
        else:
            # 個別文の要素のみ考慮
            present_slots = set(mapped_slots.keys())
            print(f"Present slots in sentence: {present_slots}")
        
        # 相対順序から動的絶対位置を計算
        absolute_positions = {}
        current_position = 1
        
        for slot_type in relative_order:
            if slot_type in present_slots or slot_type in mapped_slots:
                absolute_positions[slot_type] = current_position
                print(f"  {slot_type} → position {current_position}")
                current_position += 1
            else:
                print(f"  {slot_type} → skipped (not present)")
        
        # スロット別絶対位置マッピング
        slot_positions = []
        
        for slot_name, slot_value in mapped_slots.items():
            if slot_name in absolute_positions:
                absolute_position = absolute_positions[slot_name]
                original_name = original_slot_names[slot_name]
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": absolute_position
                })
                print(f"  Final: {original_name}({slot_value}) → position {absolute_position}")
            else:
                # グループルールにないスロットは最後に追加
                original_name = original_slot_names[slot_name]
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": 999  # 最後に配置
                })
                print(f"  Final: {original_name}({slot_value}) → position 999 (fallback)")
        
        # 絶対位置でソート
        slot_positions.sort(key=lambda x: x["absolute_position"])
        
        print(f"Universal relative order result: {slot_positions}")
        return slot_positions
    
    def _apply_relative_order_system(self, slots, v_group_key, wh_word, group_population):
        """
        相対順序システム（従来方式）
        """
        print("Using relative order system")
        
        # グループルールを取得
        if v_group_key in self.group_rules:
            group_rule = self.group_rules[v_group_key]
            relative_order = group_rule.get("relative_order", [])
        else:
            group_rule = self.group_rules["default"]
            relative_order = group_rule.get("relative_order", [])
        
        print(f"Using relative order: {relative_order}")
        
        # スロット名マッピング（M3 → M2_END等）
        mapped_slots = {}
        original_slot_names = {}
        for slot_name, slot_value in slots.items():
            if slot_name == "M3":
                mapped_slots["M2_END"] = slot_value
                original_slot_names["M2_END"] = slot_name
            else:
                mapped_slots[slot_name] = slot_value
                original_slot_names[slot_name] = slot_name
        
        # グループ人口分析に基づく絶対位置計算
        if group_population:
            # グループ全体に存在する要素を考慮した位置計算
            present_slots = group_population
            print(f"Using group population: {present_slots}")
        else:
            # 個別文の要素のみ考慮
            present_slots = set(mapped_slots.keys())
            print(f"Present slots in sentence: {present_slots}")
        
        # 相対順序から動的絶対位置を計算
        absolute_positions = {}
        current_position = 1
        
        for slot_type in relative_order:
            if slot_type in present_slots or slot_type in mapped_slots:
                absolute_positions[slot_type] = current_position
                print(f"  {slot_type} → position {current_position}")
                current_position += 1
            else:
                print(f"  {slot_type} → skipped (not present)")
        
        # スロット別絶対位置マッピング
        slot_positions = []
        
        for slot_name, slot_value in mapped_slots.items():
            if slot_name in absolute_positions:
                absolute_position = absolute_positions[slot_name]
                original_name = original_slot_names[slot_name]
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": absolute_position
                })
                print(f"  Final: {original_name}({slot_value}) → position {absolute_position}")
            else:
                # グループルールにないスロットは最後に追加
                original_name = original_slot_names[slot_name]
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": 999  # 最後に配置
                })
                print(f"  Final: {original_name}({slot_value}) → position 999 (fallback)")
        
        # 絶対位置でソート
        slot_positions.sort(key=lambda x: x["absolute_position"])
        
        print(f"Universal relative order result: {slot_positions}")
        return slot_positions
    
    def validate_wh_word_consistency(self, slots, wh_word):
        """
        wh-word一貫性チェック
        
        Args:
            slots (dict): スロット情報
            wh_word (str): 疑問詞
            
        Returns:
            bool: 一貫性チェック結果
        """
        if not wh_word:
            return True
        
        expected_slot = self.wh_word_slots.get(wh_word.lower())
        if not expected_slot:
            return True
        
        # 疑問詞が期待されるスロットに配置されているかチェック
        for slot_name, slot_value in slots.items():
            if slot_value.lower().startswith(wh_word.lower()):
                if slot_name == expected_slot:
                    print(f"✅ wh-word consistency: {wh_word} correctly in {slot_name}")
                    return True
                else:
                    print(f"❌ wh-word inconsistency: {wh_word} in {slot_name}, expected {expected_slot}")
                    return False
        
        return True
    
    def generate_randomization_matrix(self, v_group_key, target_slots):
        """
        ランダム化マトリックス生成（グループ内相対順序を維持）
        
        Args:
            v_group_key (str): 動詞グループキー
            target_slots (list): 対象スロット名リスト
            
        Returns:
            dict: ランダム化可能な組み合わせマトリックス
        """
        if v_group_key not in self.group_rules:
            return {}
        
        group_rule = self.group_rules[v_group_key]
        relative_order = group_rule["relative_order"]
        
        # グループ内要素の相対順序を維持したランダム化
        matrix = {}
        for slot in target_slots:
            if slot in relative_order:
                matrix[slot] = {
                    "relative_position": relative_order.index(slot),
                    "randomizable": False,  # グループ内は相対順序固定
                    "group": v_group_key
                }
            else:
                matrix[slot] = {
                    "relative_position": None,
                    "randomizable": True,   # グループ外は相対的
                    "group": "external"
                }
        
        return matrix


def test_absolute_order_manager():
    """
    tellグループでAbsoluteOrderManager（動的版）をテスト
    """
    print("=== AbsoluteOrderManager 動的テスト開始 ===\n")
    
    manager = AbsoluteOrderManager()
    
    # テストケース1: "What did he tell her at the store?" (M1なし)
    print("【テストケース1】What did he tell her at the store? (M1なし)")
    slots1 = {
        "O2": "What",
        "Aux": "did",
        "S": "he", 
        "V": "tell",
        "O1": "her",
        "M2": "at the store"  # 修正：M3→M2
    }
    result1 = manager.apply_absolute_order(slots1, "tell", "what")
    print()
    
    # テストケース2: "Where did you tell me a story?" (M1なし)
    print("【テストケース2】Where did you tell me a story? (M1なし)")
    slots2 = {
        "M2": "Where",  # 疑問詞のM2
        "Aux": "did",
        "S": "you",
        "V": "tell", 
        "O1": "me",
        "O2": "a story"
    }
    result2 = manager.apply_absolute_order(slots2, "tell", "where")
    print()
    
    # テストケース3: "Yesterday, what did he tell her?" (M1あり - 動的シフト)
    print("【テストケース3】Yesterday, what did he tell her? (M1あり - 動的シフト)")
    slots3 = {
        "M1": "Yesterday",  # 冒頭のM1
        "O2": "what",
        "Aux": "did",
        "S": "he",
        "V": "tell",
        "O1": "her"
    }
    result3 = manager.apply_absolute_order(slots3, "tell", "what")
    print()
    
    # テストケース4: "Last month, where did you tell me a story there?" (M1とM2両方)
    print("【テストケース4】Last month, where did you tell me a story there? (M1とM2両方)")
    slots4 = {
        "M1": "Last month",  # 冒頭のM1
        "M2": "Where",       # 疑問詞のM2（中間）
        "Aux": "did",
        "S": "you",
        "V": "tell",
        "O1": "me", 
        "O2": "a story",
        "M2": "there"        # 最後のM2（位置が重複するが実際は別位置）
    }
    # 注意：M2が2つあるので、実際は別々に処理する必要
    result4 = manager.apply_absolute_order(slots4, "tell", "where")
    print()
    
    # wh-word一貫性テスト
    print("【wh-word一貫性テスト】")
    consistency1 = manager.validate_wh_word_consistency(slots1, "what")
    consistency2 = manager.validate_wh_word_consistency(slots2, "where")
    print()
    
    # ランダム化マトリックステスト
    print("【ランダム化マトリックステスト（動的版）】")
    matrix = manager.generate_randomization_matrix("tell", ["M1", "M2", "O2", "Aux", "S", "V", "O1"])
    print(f"Tell group matrix: {matrix}")
    print()
    
    print("=== 動的絶対順序の説明 ===")
    print("パターン1（M1なし）: M2=1, O2=2, Aux=3, S=4, V=5, O1=6, M2=7")
    print("パターン2（M1あり）: M1=1, M2=2, O2=3, Aux=4, S=5, V=6, O1=7, M2=8")
    print("→ 例文の母集団に応じて絶対位置が動的に決まる")


if __name__ == "__main__":
    test_absolute_order_manager()
