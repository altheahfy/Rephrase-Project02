#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
絶対順序管理システム（グループ内絶対位置固定版）
"""

class AbsoluteOrderManager:
    def __init__(self):
        # V_group_key別相対順序ルール
        self.group_rules = {
            "tell": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "M2_END"]
            },
            "give": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "M2_END"]
            },
            "passive": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "C2", "M2_END"]
            },
            "action": {
                "relative_order": ["M1", "Aux", "S", "V", "O1", "O2", "M2", "C1", "C2", "M2_END"]
            },
            "communication": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "C1", "C2", "M2_END"]
            },
            "default": {
                "relative_order": ["M1", "M2", "Aux", "S", "V", "O1", "O2", "C1", "C2", "M2_END"]
            }
        }
        
        # wh-word→スロットマッピング
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
        絶対順序を適用（グループ内絶対位置固定版）
        
        Args:
            slots (dict): スロット情報
            v_group_key (str): 動詞グループキー
            wh_word (str, optional): 疑問詞
            group_population (set, optional): グループ母集団
            
        Returns:
            list: 絶対位置付きスロット情報
        """
        print("=== AbsoluteOrderManager.apply_absolute_order (Group Fixed Position System) ===")
        print(f"Input slots: {slots}")
        print(f"V_group_key: {v_group_key}")
        print(f"wh_word: {wh_word}")
        print(f"Group population: {group_population}")
        
        # グループ内絶対位置固定システムを使用
        return self._apply_group_fixed_position_system(slots, v_group_key, wh_word, group_population)
    
    def _apply_group_fixed_position_system(self, slots, v_group_key, wh_word, group_population):
        """
        グループ内絶対位置固定システム
        同じV_group_key内では各スロットの絶対位置は常に固定
        """
        print("Using group fixed position system")
        
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
        
        # グループ母集団に基づく固定絶対位置計算
        if group_population:
            present_slots = group_population
            print(f"Using group population: {present_slots}")
        else:
            present_slots = set(mapped_slots.keys())
            print(f"Present slots in sentence: {present_slots}")
        
        # 相対順序から固定絶対位置を計算（wh-wordの有無に関係なく）
        absolute_positions = {}
        current_position = 2  # 位置1はwh-word用に予約
        
        for slot_type in relative_order:
            if slot_type in present_slots:
                absolute_positions[slot_type] = current_position
                print(f"  {slot_type} → fixed position {current_position}")
                current_position += 1
            else:
                print(f"  {slot_type} → skipped (not in group population)")
        
        # スロット別絶対位置マッピング
        slot_positions = []
        
        for slot_name, slot_value in mapped_slots.items():
            original_name = original_slot_names[slot_name]
            
            # wh-word特別処理: wh-wordは位置1に固定、他は通常の固定位置
            if wh_word and slot_value.lower().startswith(wh_word.lower()):
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": 1
                })
                print(f"  Final: {original_name}({slot_value}) → position 1 (wh-word fixed)")
            elif slot_name in absolute_positions:
                absolute_position = absolute_positions[slot_name]
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": absolute_position
                })
                print(f"  Final: {original_name}({slot_value}) → position {absolute_position} (group fixed)")
            else:
                # グループルールにないスロットは最後に追加
                slot_positions.append({
                    "slot": original_name,
                    "value": slot_value,
                    "absolute_position": 999  # 最後に配置
                })
                print(f"  Final: {original_name}({slot_value}) → position 999 (fallback)")
        
        # 絶対位置でソート
        slot_positions.sort(key=lambda x: x["absolute_position"])
        
        print(f"Group fixed position result: {slot_positions}")
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
                    print(f"❌ wh-word consistency: {wh_word} in {slot_name}, expected {expected_slot}")
                    return False
        
        print(f"⚠️ wh-word not found: {wh_word}")
        return False
