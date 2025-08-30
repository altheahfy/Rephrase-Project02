#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終版Pure Data-Driven Absolute Order Manager
疑問詞と通常位置を分離して処理するアプローチ
"""

import json
from central_controller import CentralController

class FinalPureDataDrivenAbsoluteOrderManager:
    """
    最終版Pure Data-Driven絶対順序マネージャー
    疑問詞と通常位置の要素を分離して適切な順序を決定
    """
    
    def __init__(self):
        self.controller = CentralController()
        self.question_words = {'What', 'Where', 'When', 'Why', 'How', 'Who', 'Which', 'Whose', 'Whom'}
        
    def process_v_group(self, v_group_key):
        """
        V_group_keyの例文群を処理して絶対順序を決定
        """
        print(f"\n🚀 {v_group_key}グループの処理開始（疑問詞分離版）")
        
        # ①全要素抽出 - CentralControllerで例文を分解
        sentences_data = self._extract_all_elements(v_group_key)
        
        # ②要素分類 - 疑問詞版と通常版に分離
        element_groups = self._classify_elements(sentences_data)
        
        # ③共通順序構築 - 分離した要素群の順序を決定
        common_order = self._build_final_order(sentences_data, element_groups)
        
        # ④番号付与 - 共通順序に基づいて各例文に番号を付与
        results = self._assign_final_numbers(sentences_data, common_order, element_groups)
        
        return results
    
    def _extract_all_elements(self, v_group_key):
        """
        ①全要素抽出: CentralControllerで例文を分解してスロット要素を取得
        """
        print(f"🔍 ステップ①: {v_group_key}グループから全要素を抽出")
        
        sentences = self.controller._extract_real_group_data(v_group_key)
        print(f"📚 例文数: {len(sentences)}")
        
        sentences_data = []
        for i, sentence in enumerate(sentences):
            print(f"  📝 例文{i+1}: {sentence}")
            
            result = self.controller.process_sentence(sentence)
            slots = result.get('main_slots', {})
            print(f"  🔧 分解結果: {slots}")
            
            sentences_data.append({
                'sentence': sentence,
                'slots': slots
            })
        
        return sentences_data
    
    def _classify_elements(self, sentences_data):
        """
        ②要素分類: 疑問詞版と通常版に分離
        """
        print(f"\n🔍 ステップ②: 要素を疑問詞版と通常版に分類")
        
        element_groups = {}
        
        # 全スロットの値を収集
        all_slot_values = {}
        for data in sentences_data:
            for slot_key, slot_value in data['slots'].items():
                if slot_key not in all_slot_values:
                    all_slot_values[slot_key] = set()
                all_slot_values[slot_key].add(slot_value)
        
        # 各スロットを疑問詞版と通常版に分類
        for slot_key, values in all_slot_values.items():
            question_values = set()
            normal_values = set()
            
            for value in values:
                if value in self.question_words:
                    question_values.add(value)
                else:
                    normal_values.add(value)
            
            # 疑問詞版がある場合
            if question_values:
                element_groups[f"{slot_key}_question"] = {
                    'original_slot': slot_key,
                    'values': question_values,
                    'type': 'question'
                }
                print(f"  🔍 {slot_key}_question: {question_values}")
            
            # 通常版がある場合
            if normal_values:
                element_groups[f"{slot_key}_normal"] = {
                    'original_slot': slot_key,
                    'values': normal_values,
                    'type': 'normal'
                }
                print(f"  📝 {slot_key}_normal: {normal_values}")
        
        return element_groups
    
    def _build_final_order(self, sentences_data, element_groups):
        """
        ③共通順序構築: 分離した要素群の平均位置を計算
        """
        print(f"\n🔍 ステップ③: 分離要素の共通順序を構築")
        
        # 各要素グループの平均出現位置を計算
        group_avg_positions = {}
        
        for group_name, group_info in element_groups.items():
            original_slot = group_info['original_slot']
            values = group_info['values']
            positions = []
            
            for data in sentences_data:
                sentence = data['sentence']
                slots = data['slots']
                
                # このグループの値が含まれているかチェック
                if original_slot in slots and slots[original_slot] in values:
                    # 出現位置を計算（シンプルに文字位置から順序を計算）
                    slot_positions = []
                    remaining_sentence = sentence.lower()
                    
                    for slot_k, slot_v in slots.items():
                        pos = remaining_sentence.find(slot_v.lower())
                        if pos != -1:
                            slot_positions.append((pos, slot_k))
                            remaining_sentence = remaining_sentence.replace(slot_v.lower(), ' ' * len(slot_v), 1)
                    
                    slot_positions.sort()
                    order_sequence = [slot_k for pos, slot_k in slot_positions]
                    
                    if original_slot in order_sequence:
                        position = order_sequence.index(original_slot) + 1
                        positions.append(position)
                        print(f"    📍 {group_name}: 例文 '{sentence}' で位置{position}")
            
            if positions:
                avg_position = sum(positions) / len(positions)
                group_avg_positions[group_name] = avg_position
                print(f"  ✅ {group_name}: 平均位置={avg_position:.2f}")
        
        # 平均位置でソートして共通順序を決定
        common_order = sorted(group_avg_positions.items(), key=lambda x: x[1])
        common_order_keys = [group_name for group_name, avg_pos in common_order]
        
        print(f"✅ 最終共通順序: {' → '.join(common_order_keys)}")
        
        return common_order_keys
    
    def _assign_final_numbers(self, sentences_data, common_order, element_groups):
        """
        ④番号付与: 共通順序に基づいて各例文に番号を付与
        """
        print(f"\n🔍 ステップ④: 最終番号を付与")
        
        # グループ名から順序番号へのマッピングを作成
        group_to_order = {}
        for i, group_name in enumerate(common_order):
            group_to_order[group_name] = i + 1
        
        print(f"📊 グループ→順序マッピング: {group_to_order}")
        
        results = []
        for i, data in enumerate(sentences_data):
            sentence = data['sentence']
            slots = data['slots']
            
            ordered_slots = {}
            for slot_key, slot_value in slots.items():
                # このスロット値がどのグループに属するかを特定
                matched_group = None
                for group_name, group_info in element_groups.items():
                    if (group_info['original_slot'] == slot_key and 
                        slot_value in group_info['values']):
                        matched_group = group_name
                        break
                
                if matched_group and matched_group in group_to_order:
                    order_num = group_to_order[matched_group]
                    ordered_slots[str(order_num)] = slot_value
                    print(f"  📝 {slot_key}={slot_value} → {matched_group} → 順序{order_num}")
            
            result = {
                'sentence': sentence,
                'original_slots': slots,
                'ordered_slots': ordered_slots
            }
            results.append(result)
            
            print(f"✅ 例文{i+1}: {sentence}")
            print(f"  🎯 最終結果: {ordered_slots}")
        
        return results

def main():
    """メイン関数 - tellグループでテスト"""
    print("🚀 最終版Pure Data-Driven Absolute Order Manager テスト開始")
    
    manager = FinalPureDataDrivenAbsoluteOrderManager()
    
    # tellグループをテスト
    results = manager.process_v_group('tell')
    
    # 結果を保存
    output_file = 'final_tell_group_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 結果を {output_file} に保存しました")
    
    # 結果の確認
    print(f"\n📊 最終結果サマリー:")
    for i, result in enumerate(results):
        print(f"例文{i+1}: {result['sentence']}")
        print(f"順序: {result['ordered_slots']}")
        print()

if __name__ == "__main__":
    main()
