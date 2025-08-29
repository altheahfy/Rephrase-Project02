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
        group_populationから語順ベースの重複回避要素リストを作成
        例文の語順通りに処理し、バッティングを回避して配置
        """
        print("🔧 語順ベース要素分析開始")
        
        # Step 1: 各文の語順情報を取得
        sentence_word_orders = []
        for sentence_data in group_population:
            case = sentence_data.get("case", "unknown")
            slots = sentence_data.get("slots", {})
            sentence = sentence_data.get("sentence", "")
            
            print(f"📝 語順分析: {case} - {sentence}")
            
            # 文を単語に分割して語順を取得
            word_order = self._extract_word_order_from_sentence(sentence, slots)
            sentence_word_orders.append({
                "case": case,
                "sentence": sentence,
                "slots": slots,
                "word_order": word_order
            })
            
            print(f"  語順: {word_order}")
        
        # Step 2: 語順通りに要素を配置（バッティング回避）
        element_position_map = {}  # element_key -> position
        used_positions = set()
        next_available_position = 1
        
        # 各文を語順通りに処理
        for sentence_info in sentence_word_orders:
            word_order = sentence_info["word_order"]
            case = sentence_info["case"]
            
            print(f"📋 {case} の要素配置:")
            
            for word_pos, (slot_name, slot_value) in enumerate(word_order, 1):
                # 要素タイプを判定
                if self.is_wh_word_content(slot_value):
                    detected_wh = self.detect_wh_word({slot_name: slot_value})
                    if detected_wh:
                        element_key = f"{slot_name}_{detected_wh}"
                    else:
                        element_key = f"{slot_name}_wh_unknown"
                else:
                    element_key = f"{slot_name}_standard"
                
                # 既に配置済みかチェック
                if element_key not in element_position_map:
                    # 新しい要素なので配置
                    target_position = next_available_position
                    element_position_map[element_key] = target_position
                    used_positions.add(target_position)
                    next_available_position += 1
                    
                    print(f"  新規配置: {element_key} → position {target_position}")
                else:
                    print(f"  既存要素: {element_key} → position {element_position_map[element_key]} (スキップ)")
        
        # Step 3: position順でソートして要素リスト作成
        sorted_elements = sorted(element_position_map.items(), key=lambda x: x[1])
        final_element_list = [element_key for element_key, position in sorted_elements]
        
        print(f"📊 最終要素配置:")
        for element_key, position in sorted_elements:
            print(f"  position {position}: {element_key}")
        
        print(f"📋 要素リスト: {final_element_list}")
        return final_element_list
    
    def _extract_word_order_from_sentence(self, sentence, slots):
        """
        例文とスロット情報から語順を抽出
        """
        import re
        
        # 句読点を除去
        clean_sentence = re.sub(r'[?!.,]', '', sentence)
        words = clean_sentence.split()
        
        word_order = []
        used_words = set()
        
        # 各単語がどのスロットに対応するかマッチング
        for word in words:
            best_match = None
            best_slot = None
            
            # 完全一致を優先
            for slot_name, slot_value in slots.items():
                if slot_value and word.lower() == slot_value.lower():
                    if word.lower() not in used_words:
                        best_match = slot_value
                        best_slot = slot_name
                        used_words.add(word.lower())
                        break
            
            # 部分一致をチェック（フレーズの場合）
            if not best_match:
                for slot_name, slot_value in slots.items():
                    if slot_value and word.lower() in slot_value.lower():
                        # フレーズ全体をマッチング
                        phrase_words = slot_value.split()
                        if word == phrase_words[0]:  # フレーズの最初の単語
                            best_match = slot_value
                            best_slot = slot_name
                            # フレーズの全単語を使用済みに
                            for phrase_word in phrase_words:
                                used_words.add(phrase_word.lower())
                            break
            
            if best_match and best_slot:
                word_order.append((best_slot, best_match))
        
        return word_order
    
    def _matches_element_type(self, slot_value, element_type):
        """
        スロット値が要素タイプと一致するかチェック
        新しい要素キー形式に対応: "slot_name_type"
        """
        if "_" in element_type:
            slot_name, type_suffix = element_type.split("_", 1)
            
            if type_suffix == "standard":
                return not self.is_wh_word_content(slot_value)
            else:
                # 疑問詞タイプ (where, what, etc.)
                return (self.is_wh_word_content(slot_value) and 
                       slot_value.lower().startswith(type_suffix.lower()))
        else:
            # 旧形式の互換性
            if element_type == "standard":
                return not self.is_wh_word_content(slot_value)
            else:
                return (self.is_wh_word_content(slot_value) and 
                       slot_value.lower().startswith(element_type.lower()))
    
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
