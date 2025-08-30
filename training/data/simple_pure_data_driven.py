#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプルなPure Data-Driven Absolute Order Manager
一から作り直したシンプルで確実なアプローチ
"""

import json
from central_controller import CentralController

class SimplePureDataDrivenAbsoluteOrderManager:
    """
    シンプルなPure Data-Driven絶対順序マネージャー
    4ステップアルゴリズム：
    ①全要素抽出 ②語順観察 ③共通順序構築 ④番号付与
    """
    
    def __init__(self):
        self.controller = CentralController()
        
    def process_v_group(self, v_group_key):
        """
        V_group_keyの例文群を処理して絶対順序を決定
        """
        print(f"\n🚀 {v_group_key}グループの処理開始")
        
        # ①全要素抽出 - CentralControllerで例文を分解
        sentences_data = self._extract_all_elements(v_group_key)
        
        # ②語順観察 - 各例文の要素出現順序を記録
        word_orders = self._observe_word_orders(sentences_data)
        
        # ③共通順序構築 - 全例文から共通の順序パターンを構築
        common_order = self._build_common_order(word_orders)
        
        # ④番号付与 - 共通順序に基づいて各例文に番号を付与
        results = self._assign_order_numbers(sentences_data, common_order)
        
        return results
    
    def _extract_all_elements(self, v_group_key):
        """
        ①全要素抽出: CentralControllerで例文を分解してスロット要素を取得
        """
        print(f"🔍 ステップ①: {v_group_key}グループから全要素を抽出")
        
        # CentralControllerから例文を取得
        sentences = self.controller._extract_real_group_data(v_group_key)
        print(f"📚 例文数: {len(sentences)}")
        
        sentences_data = []
        for i, sentence in enumerate(sentences):
            print(f"  📝 例文{i+1}: {sentence}")
            
            # CentralControllerで分解
            result = self.controller.process_sentence(sentence)
            slots = result.get('main_slots', {})
            print(f"  🔧 分解結果: {slots}")
            
            sentences_data.append({
                'sentence': sentence,
                'slots': slots
            })
        
        return sentences_data
    
    def _observe_word_orders(self, sentences_data):
        """
        ②語順観察: 各例文の要素出現順序を記録（シンプルな出現順カウント）
        """
        print(f"\n🔍 ステップ②: 各例文の語順を観察（シンプル出現順）")
        
        word_orders = []
        for i, data in enumerate(sentences_data):
            sentence = data['sentence']
            slots = data['slots']
            
            # 文中での各スロット要素の出現順序を特定（シンプルにfind順序で）
            slot_positions = []
            remaining_sentence = sentence.lower()
            
            for slot_key, slot_value in slots.items():
                # スロット値が文中のどの位置にあるかを特定
                pos = remaining_sentence.find(slot_value.lower())
                if pos != -1:
                    slot_positions.append((pos, slot_key))
                    # 見つけた部分を置換して重複を避ける
                    remaining_sentence = remaining_sentence.replace(slot_value.lower(), ' ' * len(slot_value), 1)
            
            # 位置順にソートして順序を決定
            slot_positions.sort()
            order_sequence = [slot_key for pos, slot_key in slot_positions]
            
            # 出現順序番号を作成（1番目、2番目、3番目...）
            order_numbers = {}
            for order_num, slot_key in enumerate(order_sequence, 1):
                order_numbers[slot_key] = order_num
            
            print(f"  📝 例文{i+1}: {sentence}")
            print(f"  📊 語順: {' → '.join(order_sequence)}")
            print(f"  🔢 順序: {order_numbers}")
            
            word_orders.append({
                'sentence': sentence,
                'slots': slots,
                'order_sequence': order_sequence,
                'order_numbers': order_numbers
            })
        
        return word_orders
    
    def _build_common_order(self, word_orders):
        """
        ③共通順序構築: 疑問詞を考慮した共通順序パターンを構築
        """
        print(f"\n🔍 ステップ③: 共通順序パターンを構築（疑問詞優先）")
        
    def _build_common_order(self, word_orders):
        """
        ③共通順序構築: 全例文から共通の順序パターンを構築（シンプル平均）
        """
        print(f"\n� ステップ③: 共通順序パターンを構築（シンプル平均）")
        
        # 全スロットキーを収集
        all_slot_keys = set()
        for order_data in word_orders:
            all_slot_keys.update(order_data['slots'].keys())
        
        print(f"� 全スロットキー: {sorted(all_slot_keys)}")
        
        # 各スロットキーの平均出現順序を計算
        slot_avg_orders = {}
        for slot_key in all_slot_keys:
            orders = []
            
            for order_data in word_orders:
                if slot_key in order_data['order_numbers']:
                    orders.append(order_data['order_numbers'][slot_key])
            
            if orders:
                avg_order = sum(orders) / len(orders)
                slot_avg_orders[slot_key] = avg_order
                print(f"  📍 {slot_key}: 平均出現順序={avg_order:.2f}")
        
        # 平均順序でソートして共通順序を決定
        common_order = sorted(slot_avg_orders.items(), key=lambda x: x[1])
        common_order_keys = [slot_key for slot_key, avg_order in common_order]
        
        print(f"✅ 共通順序: {' → '.join(common_order_keys)}")
        
        return common_order_keys
    
    def _assign_order_numbers(self, sentences_data, common_order):
        """
        ④番号付与: 共通順序に基づいて各例文に番号を付与
        """
        print(f"\n🔍 ステップ④: 共通順序に基づいて番号を付与")
        
        # スロットキーから順序番号へのマッピングを作成
        slot_to_order = {}
        for i, slot_key in enumerate(common_order):
            slot_to_order[slot_key] = i + 1  # 1から開始
        
        print(f"📊 スロット→順序マッピング: {slot_to_order}")
        
        results = []
        for i, data in enumerate(sentences_data):
            sentence = data['sentence']
            slots = data['slots']
            
            # 各スロットに順序番号を付与
            ordered_slots = {}
            for slot_key, slot_value in slots.items():
                if slot_key in slot_to_order:
                    order_num = slot_to_order[slot_key]
                    ordered_slots[str(order_num)] = slot_value
                    print(f"  📝 {slot_key}={slot_value} → 順序{order_num}")
            
            result = {
                'sentence': sentence,
                'original_slots': slots,
                'ordered_slots': ordered_slots
            }
            results.append(result)
            
            print(f"✅ 例文{i+1}: {sentence}")
            print(f"  🎯 順序付き結果: {ordered_slots}")
        
        return results

def main():
    """メイン関数 - tellグループでテスト"""
    print("🚀 シンプルPure Data-Driven Absolute Order Manager テスト開始")
    
    manager = SimplePureDataDrivenAbsoluteOrderManager()
    
    # tellグループをテスト
    results = manager.process_v_group('tell')
    
    # 結果を保存
    output_file = 'simple_tell_group_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 結果を {output_file} に保存しました")
    
    # 結果の確認
    print(f"\n📊 結果サマリー:")
    for i, result in enumerate(results):
        print(f"例文{i+1}: {result['sentence']}")
        print(f"順序: {result['ordered_slots']}")
        print()

if __name__ == "__main__":
    main()
