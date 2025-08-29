#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
絶対順序管理システム（汎用版）
シンプルで明確な実装
"""

class AbsoluteOrderManagerUniversal:
    def __init__(self):
        """
        汎用絶対順序管理システム
        """
        pass
    
    def analyze_group_population(self, group_sentences):
        """
        グループ母集団を分析して要素リストを作成
        
        Args:
            group_sentences (list): グループ内の全例文リスト
            
        Returns:
            list: 要素リスト（登場順序付き）
        """
        print(f"🔍 Analyzing {len(group_sentences)} sentences in group...")
        
        # Step 1: 全例文から要素を収集（文中語順で）
        all_elements = []
        
        for i, sentence_data in enumerate(group_sentences):
            slots = sentence_data.get("slots", {})
            sentence_text = sentence_data.get("sentence", f"sentence_{i+1}")
            
            print(f"  📝 {sentence_text}")
            
            # 各文の語順で要素を収集
            sentence_elements = []
            for slot_name, slot_value in slots.items():
                if slot_value:
                    # 疑問詞判定
                    if self.is_wh_word(slot_value):
                        wh_word = self.detect_wh_word(slot_value)
                        element_id = f"{slot_name}_{wh_word}_wh"
                        sentence_elements.append(element_id)
                        print(f"    🔹 {slot_name}({slot_value}) → {element_id}")
                    else:
                        element_id = f"{slot_name}_standard"
                        sentence_elements.append(element_id)
                        print(f"    🔹 {slot_name}({slot_value}) → {element_id}")
            
            all_elements.extend(sentence_elements)
        
        # Step 2: 登場順序で重複を除去
        seen = set()
        element_order = []
        for element in all_elements:
            if element not in seen:
                element_order.append(element)
                seen.add(element)
        
        print(f"📋 Group element order: {element_order}")
        return element_order
    
    def assign_absolute_order(self, target_slots, element_order):
        """
        個別文に絶対順序を割り当て
        
        Args:
            target_slots (dict): 対象文のスロット
            element_order (list): グループ要素順序
            
        Returns:
            dict: 絶対順序辞書
        """
        absolute_order = {}
        
        print(f"🎯 Assigning order to: {target_slots}")
        
        for position, element_id in enumerate(element_order, 1):
            # 要素IDを解析
            parts = element_id.split('_')
            slot_name = parts[0]
            element_type = parts[1]
            is_wh = len(parts) > 2 and parts[2] == 'wh'
            
            slot_value = target_slots.get(slot_name)
            
            if slot_value:
                # マッチング判定
                if is_wh and self.is_wh_word(slot_value):
                    detected_wh = self.detect_wh_word(slot_value)
                    if detected_wh == element_type:
                        absolute_order[slot_name] = position
                        print(f"  ✅ {slot_name}({slot_value}) → position {position} (wh-word: {detected_wh})")
                elif not is_wh and not self.is_wh_word(slot_value):
                    absolute_order[slot_name] = position
                    print(f"  ✅ {slot_name}({slot_value}) → position {position} (standard)")
                else:
                    print(f"  ⏭️ {slot_name}({slot_value}) → skipped (type mismatch)")
            else:
                print(f"  ⭕ position {position} → empty (reserved for {element_id})")
        
        return absolute_order
    
    def is_wh_word(self, text):
        """
        疑問詞判定
        """
        if not text:
            return False
        
        wh_words = ["what", "where", "when", "why", "how", "who", "whom", "whose", "which"]
        text_lower = text.lower().strip()
        
        for wh in wh_words:
            if text_lower.startswith(wh):
                return True
        return False
    
    def detect_wh_word(self, text):
        """
        疑問詞を検出
        """
        if not text:
            return None
            
        wh_words = ["what", "where", "when", "why", "how", "who", "whom", "whose", "which"]
        text_lower = text.lower().strip()
        
        for wh in wh_words:
            if text_lower.startswith(wh):
                return wh
        return None
    
    def process_group(self, group_sentences, target_sentence_slots):
        """
        グループ処理のメイン関数
        
        Args:
            group_sentences (list): グループ母集団
            target_sentence_slots (dict): 対象文のスロット
            
        Returns:
            dict: 絶対順序辞書
        """
        print("=" * 60)
        print("🎯 Universal Absolute Order Manager")
        print("=" * 60)
        
        # Step 1: グループ分析
        element_order = self.analyze_group_population(group_sentences)
        
        # Step 2: 順序割り当て
        absolute_order = self.assign_absolute_order(target_sentence_slots, element_order)
        
        print(f"🎉 Final result: {absolute_order}")
        return absolute_order
