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
        汎用的絶対位置システム（母集団要素リストベース）
        group_populationから要素リストを作成し、各文でマッチング
        """
        print("🎯 Using Group Population Element List System")
        
        # group_populationが提供されていない場合のフォールバック
        if not group_population:
            print("⚠️ No group_population provided, using fallback system")
            return self._apply_fallback_system(slots)
        
        # Step 1: group_populationから要素リストを作成
        element_list = self._create_element_list_from_population(group_population, v_group_key)
        print(f"📋 Group element list: {element_list}")
        
        # Step 2: 各文のスロットを要素リストとマッチング
        slot_positions = []
        for position, element_key in enumerate(element_list, 1):
            # 要素キーを解析 (例: "M1_where", "O2_what", "Aux_standard")
            if "_" in element_key:
                slot_name, element_type = element_key.split("_", 1)
            else:
                slot_name = element_key
                element_type = "standard"
            
            slot_value = slots.get(slot_name)
            
            # スロットが存在し、要素タイプが一致する場合のみ位置を割り当て
            if slot_value and self._matches_element_type(slot_value, element_type):
                slot_positions.append({
                    "slot": slot_name,
                    "value": slot_value,
                    "absolute_position": position
                })
                print(f"  ✅ {slot_name}({slot_value}) → position {position} (element: {element_key})")
            elif slot_value:
                print(f"  ⏭️ {slot_name}({slot_value}) → skipped (element type mismatch: {element_type})")
            else:
                print(f"  ⭕ {slot_name} → empty (position {position} reserved for {element_key})")
        
        print(f"📋 Final slot positions: {[(sp['slot'], sp['absolute_position']) for sp in slot_positions]}")
        return slot_positions
    
    def _create_element_list_from_population(self, group_population, v_group_key):
        """
        group_populationからグループの要素リストを作成
        """
        element_set = set()
        
        # 母集団の全文を調査して要素を抽出
        for sentence_data in group_population:
            slots = sentence_data.get("slots", {})
            
            for slot_name, slot_value in slots.items():
                if slot_value:
                    # 疑問詞の判定
                    if self.is_wh_word_content(slot_value):
                        detected_wh = self.detect_wh_word({slot_name: slot_value})
                        if detected_wh:
                            element_set.add(f"{slot_name}_{detected_wh}")
                        else:
                            element_set.add(f"{slot_name}_standard")
                    else:
                        element_set.add(f"{slot_name}_standard")
        
        # 要素を順序付け（疑問詞優先、その後標準順序）
        element_list = []
        wh_elements = []
        standard_elements = []
        
        for element in sorted(element_set):
            if "_where" in element or "_what" in element or "_when" in element or "_why" in element or "_how" in element:
                wh_elements.append(element)
            else:
                standard_elements.append(element)
        
        # where系疑問詞とwhat疑問詞を先頭に配置
        wh_elements.sort(key=lambda x: (0 if "where" in x else 1 if "what" in x else 2))
        
        element_list.extend(wh_elements)
        element_list.extend(standard_elements)
        
        return element_list
    
    def _matches_element_type(self, slot_value, element_type):
        """
        スロット値が要素タイプと一致するかチェック
        """
        if element_type == "standard":
            return not self.is_wh_word_content(slot_value)
        else:
            # 疑問詞タイプ (where, what, etc.)
            return self.is_wh_word_content(slot_value) and slot_value.lower().startswith(element_type.lower())
    
    def _apply_fallback_system(self, slots):
        """
        group_populationがない場合のフォールバックシステム
        tellグループ要素リストを暫定的に使用（正しいMスロット配置ルール適用）
        """
        print("🔧 Using fallback system with known element lists")
        
        # tellグループの正しい要素リスト（Mスロット配置ルール準拠）
        tell_elements = [
            "M2_where",     # 1_M2_where (修飾語1個なのでM2に配置)
            "O2_what",      # 2_O2_what (O2のwhat疑問詞)  
            "Aux_standard", # 3_Aux_standard
            "S_standard",   # 4_S_standard
            "V_standard",   # 5_V_standard
            "O1_standard",  # 6_O1_standard
            "O2_standard",  # 7_O2_standard (標準)
            "M2_standard"   # 8_M2_standard (標準)
        ]
        
        slot_positions = []
        for position, element_key in enumerate(tell_elements, 1):
            slot_name, element_type = element_key.split("_", 1)
            slot_value = slots.get(slot_name)
            
            # スロットが存在し、要素タイプが一致する場合のみ位置を割り当て
            if slot_value and self._matches_element_type(slot_value, element_type):
                slot_positions.append({
                    "slot": slot_name,
                    "value": slot_value,
                    "absolute_position": position
                })
                print(f"  ✅ {slot_name}({slot_value}) → position {position} (element: {element_key})")
            elif slot_value:
                print(f"  ⏭️ {slot_name}({slot_value}) → skipped (element type mismatch: {element_type})")
            else:
                print(f"  ⭕ {slot_name} → empty (position {position} reserved for {element_key})")
        
        return slot_positions
    
    def is_wh_word_content(self, slot_value, expected_wh=None):
        """
        スロット内容が指定された疑問詞かどうか判定
        """
        if not slot_value:
            return False
        
        value_lower = slot_value.lower().strip()
        
        if expected_wh:
            return value_lower.startswith(expected_wh.lower())
        else:
            wh_words = ["what", "where", "when", "why", "how", "who", "whom", "whose", "which"]
            for wh_word in wh_words:
                if value_lower.startswith(wh_word):
                    return True
            return False

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
