#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
絶対順序管理システム（グループ内絶対位置固定版）
"""

class AbsoluteOrderManager:
    def __init__(self):
        # V_group_key別固定位置テーブル（期待値データに基づく正確な実装）
        self.FIXED_POSITIONS = {
            "tell": {
                # tellグループの固定位置（Cases 83-86より）
                # wh-word特別位置
                "M2_wh": 1,     # where, when疑問詞専用
                "O2_wh": 2,     # what疑問詞専用
                # 標準位置（飛び番号）
                "Aux": 3,       # 助動詞
                "S": 4,         # 主語
                "V": 5,         # 動詞
                "O1": 6,        # 間接目的語
                "O2": 7,        # 直接目的語（標準位置）
                "M2": 8         # 場所・時間（標準位置）
            },
            "give": {
                # giveグループ（tellと同様の授受動詞）
                "M2_wh": 1, "O2_wh": 2, "Aux": 3, "S": 4, 
                "V": 5, "O1": 6, "O2": 7, "M2": 8
            },
            "action": {
                # actionグループ
                "M1": 1, "Aux": 2, "S": 3, "V": 4, 
                "O1": 5, "O2": 6, "M2": 7, "C1": 8, "C2": 9, "M3": 10
            },
            "passive": {
                # passiveグループ
                "M1": 1, "M2": 2, "Aux": 3, "S": 4, 
                "V": 5, "C2": 6, "M2_END": 7
            },
            "communication": {
                # communicationグループ
                "M1": 1, "M2": 2, "Aux": 3, "S": 4, 
                "V": 5, "O1": 6, "O2": 7, "C1": 8, "C2": 9, "M2_END": 10
            },
            "default": {
                # デフォルトグループ
                "M1": 1, "M2": 2, "Aux": 3, "S": 4, 
                "V": 5, "O1": 6, "O2": 7, "C1": 8, "C2": 9, "M2_END": 10
            }
        }
        
        # レガシー互換性のための旧ルール（廃止予定）
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
        固定位置テーブルシステム（期待値データに厳密準拠）
        """
        print("🎯 Using Fixed Position Table System (corrected implementation)")
        
        # wh-word自動検出（引数より優先）
        detected_wh_word = self.detect_wh_word(slots)
        if detected_wh_word:
            wh_word = detected_wh_word
            print(f"📍 Using detected wh-word: {wh_word}")
        
        # 固定位置テーブル取得
        if v_group_key in self.FIXED_POSITIONS:
            position_table = self.FIXED_POSITIONS[v_group_key]
            print(f"📋 Using position table for '{v_group_key}': {position_table}")
        else:
            position_table = self.FIXED_POSITIONS["default"]
            print(f"📋 Using default position table: {position_table}")
        
        # スロット別絶対位置決定
        slot_positions = []
        
        for slot_name, slot_value in slots.items():
            if not slot_value:  # 空の値をスキップ
                continue
                
            absolute_position = None
            position_reason = ""
            
            # Step 1: wh-word特別処理チェック
            if wh_word:
                wh_override_position = self.get_wh_position_override(wh_word, slot_name)
                if wh_override_position and slot_value.lower().startswith(wh_word.lower()):
                    absolute_position = wh_override_position
                    position_reason = f"wh-word({wh_word}) override"
            
            # Step 2: 固定位置テーブル参照
            if absolute_position is None:
                # スロット名マッピング（M3 → M2等の調整）
                mapped_slot_name = slot_name
                if slot_name == "M3":
                    mapped_slot_name = "M2"  # M3はM2として扱う
                
                if mapped_slot_name in position_table:
                    absolute_position = position_table[mapped_slot_name]
                    position_reason = f"fixed table({v_group_key}.{mapped_slot_name})"
                else:
                    absolute_position = 999  # フォールバック
                    position_reason = "fallback"
            
            slot_positions.append({
                "slot": slot_name,
                "value": slot_value,
                "absolute_position": absolute_position
            })
            
            print(f"  🎯 {slot_name}({slot_value}) → position {absolute_position} ({position_reason})")
        
        # 絶対位置でソート
        slot_positions.sort(key=lambda x: x["absolute_position"])
        
        # 結果表示を簡潔に
        result_summary = []
        for item in slot_positions:
            result_summary.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
        print(f"✅ Fixed position result: {result_summary}")
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
