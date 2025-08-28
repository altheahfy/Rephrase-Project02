#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
絶対順序管理システム（グループ内絶対位置固定版）
"""

class AbsoluteOrderManager:
    def __init__(self):
        # wh-word→スロットマッピング（変更なし）
        self.wh_word_slots = {
            "what": "O2",
            "where": "M2", 
            "when": "M2",
            "why": "M2",
            "how": "M2",
            "who": "S",
            "whom": "O1"
        }
        
        # 標準スロット順序（汎用システム用）
        self.STANDARD_SLOT_ORDER = [
            "M1", "M2", "Aux", "S", "V", "C1", "O1", "O2", "C2", "M3"
        ]
    
    def detect_wh_word(self, slots):
        """
        スロット内のwh-wordを検出
        
        Args:
            slots (dict): スロット情報
            
        Returns:
            str or None: 検出されたwh-word
        """
        wh_words = ["what", "where", "when", "why", "how", "who", "whom", "whose", "which"]
        
        for slot_name, slot_value in slots.items():
            if slot_value:
                value_lower = slot_value.lower().strip()
                for wh_word in wh_words:
                    if value_lower.startswith(wh_word):
                        print(f"🔍 Detected wh-word: '{wh_word}' in {slot_name}='{slot_value}'")
                        return wh_word
        
        return None
    
    def get_wh_position_override(self, wh_word, slot_name):
        """
        wh-wordに基づく特別位置を取得
        
        Args:
            wh_word (str): 疑問詞
            slot_name (str): スロット名
            
        Returns:
            int or None: 特別位置（1 or 2）またはNone
        """
        if wh_word in ["where", "when", "why", "how"]:
            # 場所・時間・理由・方法疑問詞 → position 1
            return 1
        elif wh_word == "what":
            # what疑問詞 → position 2
            return 2
        elif wh_word in ["who", "whom"]:
            # 人物疑問詞は通常位置を使用（特別位置なし）
            return None
        
        return None
    
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
        汎用的絶対位置システム（登場順序ベース）
        ①グループ内全要素を登場順に並べてorder付与
        ②異なる要素が同じorderを持たない  
        ③同一スロットが疑問詞なら早い位置、標準なら後の位置
        """
        print("🎯 Using Universal Order System (登場順序ベース)")
        
        # wh-word自動検出
        detected_wh_word = self.detect_wh_word(slots)
        if detected_wh_word:
            wh_word = detected_wh_word
            print(f"📍 Detected wh-word: {wh_word}")
        
        # Step 1: 疑問詞の特別位置を先に決定
        wh_positions = {}
        if wh_word:
            # where系疑問詞は位置1
            if wh_word in ["where", "when", "why", "how"]:
                for slot_name, slot_value in slots.items():
                    if slot_value and slot_value.lower().startswith(wh_word.lower()):
                        wh_positions[slot_name] = 1
                        print(f"📍 {slot_name}({slot_value}) → position 1 (where系疑問詞)")
                        break
            
            # what疑問詞は位置2
            elif wh_word == "what":
                for slot_name, slot_value in slots.items():
                    if slot_value and slot_value.lower().startswith("what"):
                        wh_positions[slot_name] = 2
                        print(f"📍 {slot_name}({slot_value}) → position 2 (what疑問詞)")
                        break
        
        # Step 2: 標準順序での存在スロット収集
        present_slots = []
        for slot_name in self.STANDARD_SLOT_ORDER:
            if slot_name in slots and slots[slot_name]:
                present_slots.append(slot_name)
        
        # M3がある場合は追加
        if "M3" in slots and slots["M3"]:
            present_slots.append("M3")
        
        print(f"📋 Present slots in standard order: {present_slots}")
        
        # Step 3: 登場順序に基づく連続位置付与
        slot_positions = []
        current_position = 1
        
        for slot_name in present_slots:
            slot_value = slots[slot_name]
            
            # 疑問詞として既に位置が決まっている場合
            if slot_name in wh_positions:
                slot_positions.append({
                    "slot": slot_name,
                    "value": slot_value,
                    "absolute_position": wh_positions[slot_name]
                })
                print(f"  ✅ {slot_name}({slot_value}) → position {wh_positions[slot_name]} (疑問詞)")
            else:
                # 疑問詞位置（1,2）をスキップして連続番号付与
                while current_position in wh_positions.values():
                    current_position += 1
                
                slot_positions.append({
                    "slot": slot_name,
                    "value": slot_value,
                    "absolute_position": current_position
                })
                print(f"  ✅ {slot_name}({slot_value}) → position {current_position} (標準順序)")
                current_position += 1
        
        print(f"📋 Final slot positions: {[(sp['slot'], sp['absolute_position']) for sp in slot_positions]}")
        return slot_positions

    def assign_absolute_order(self, decomposed_list):
        """
        各文のスロットに絶対順序を割り当て
        
        Args:
            decomposed_list (list): 分解された文のリスト
            
        Returns:
            list: 絶対順序が追加された分解済み文リスト
        """
        print("\n=== AbsoluteOrderManager.assign_absolute_order ===")
        
        for i, sentence_data in enumerate(decomposed_list):
            print(f"\n📝 Processing sentence {i+1}:")
            
            slots = sentence_data.get("slots", {})
            group_info = sentence_data.get("group_info", {})
            v_group_key = group_info.get("V_group_key", "unknown")
            
            print(f"  📂 V_group_key: {v_group_key}")
            print(f"  📋 Slots: {slots}")
            
            # apply_absolute_orderを呼び出して位置情報を取得
            slot_positions = self.apply_absolute_order(slots, v_group_key)
            
            # absolute_order辞書を作成
            absolute_order = {}
            for position_info in slot_positions:
                slot_name = position_info["slot"]
                absolute_position = position_info["absolute_position"]
                absolute_order[slot_name] = absolute_position
            
            sentence_data["absolute_order"] = absolute_order
            print(f"  🎯 Final absolute_order: {absolute_order}")
        
        return decomposed_list
    
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
