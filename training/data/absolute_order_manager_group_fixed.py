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
        汎用的絶対位置システム
        V_group_key内の全要素を登場順序でソートし、連続したorder番号を付与
        """
        print("🎯 Using Universal Order System (登場順序ベース)")
        
        # wh-word自動検出
        detected_wh_word = self.detect_wh_word(slots)
        if detected_wh_word:
            wh_word = detected_wh_word
            print(f"📍 Detected wh-word: {wh_word}")
        
        # Step 1: 存在するスロットを標準順序でソート
        present_slots = []
        for slot_name in self.STANDARD_SLOT_ORDER:
            if slot_name in slots and slots[slot_name]:
                present_slots.append(slot_name)
        
        # M3がある場合はM3も追加（標準順序の最後）
        if "M3" in slots and slots["M3"]:
            present_slots.append("M3")
        
        print(f"📋 Present slots in standard order: {present_slots}")
        
        # Step 2: wh-word特別処理の位置決定
        wh_word_positions = {}
        if wh_word:
            for slot_name, slot_value in slots.items():
                if slot_value and slot_value.lower().startswith(wh_word.lower()):
                    wh_override_position = self.get_wh_position_override(wh_word, slot_name)
                    if wh_override_position:
                        wh_word_positions[slot_name] = wh_override_position
                        print(f"📍 wh-word override: {slot_name}({slot_value}) → position {wh_override_position}")
        
        # Step 3: 連続位置番号付与（wh-word以外）
        slot_positions = []
        current_position = 1
        
        # wh-word特別位置をスキップしながら連続番号付与
        for slot_name in present_slots:
            slot_value = slots[slot_name]
            
            if slot_name in wh_word_positions:
                # wh-word特別位置を使用
                absolute_position = wh_word_positions[slot_name]
                position_reason = f"wh-word({wh_word}) override"
            else:
                # wh-word特別位置（1,2）をスキップして連続番号付与
                while current_position in [1, 2] and any(pos == current_position for pos in wh_word_positions.values()):
                    current_position += 1
                
                absolute_position = current_position
                position_reason = f"standard order position"
                current_position += 1
            
            slot_positions.append({
                "slot": slot_name,
                "value": slot_value,
                "absolute_position": absolute_position
            })
            
            print(f"  🎯 {slot_name}({slot_value}) → position {absolute_position} ({position_reason})")
        
        # 絶対位置でソート
        slot_positions.sort(key=lambda x: x["absolute_position"])
        
        # 結果表示
        result_summary = []
        for item in slot_positions:
            result_summary.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
        print(f"✅ Universal order result: {result_summary}")
        
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
