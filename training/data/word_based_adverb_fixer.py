#!/usr/bin/env python3
"""
単語ベース副詞位置分析システム（既存データ使用版）
M要素をスロットIDではなく単語そのものでメタセル配置
"""

import json
from pathlib import Path

class WordBasedAdverbFixer:
    def __init__(self):
        # actionグループのスロットデータ（既知）
        self.action_data = [
            {
                "sentence": "She sings beautifully.",
                "slots": {"S": "She", "V": "sings", "M2": "beautifully"}
            },
            {
                "sentence": "We always eat breakfast together.",
                "slots": {"S": "We", "V": "eat", "O1": "breakfast", "M1": "always", "M2": "together"}
            },
            {
                "sentence": "The cat quietly sat on the mat.",
                "slots": {"S": "The cat", "V": "sat", "M1": "quietly", "M2": "on the mat"}
            },
            {
                "sentence": "She carefully reads books.",
                "slots": {"S": "She", "V": "reads", "O1": "books", "M2": "carefully"}
            },
            {
                "sentence": "They run fast.",
                "slots": {"S": "They", "V": "run", "M2": "fast"}
            },
            {
                "sentence": "Actually, she works very hard.",
                "slots": {"S": "she", "V": "works", "M1": "Actually", "M2": "very hard"}
            },
            {
                "sentence": "Every morning, he jogs slowly in the park.",
                "slots": {"S": "he", "V": "jogs", "M1": "Every morning", "M2": "slowly", "M3": "in the park"}
            }
        ]
    
    def analyze_word_positions(self):
        """単語の実際の文中位置を分析"""
        print("🚀 単語ベース副詞位置分析開始")
        
        word_positions = {}  # 副詞単語別の位置情報
        non_adverb_elements = {}  # 非副詞要素の位置情報
        
        for data in self.action_data:
            sentence = data["sentence"]
            slots = data["slots"]
            
            print(f"\n📝 分析: {sentence}")
            
            # 単語の実際の位置を取得
            words = sentence.replace(',', '').replace('.', '').split()
            print(f"   単語リスト: {words}")
            
            for slot_type, slot_value in slots.items():
                # 文中での実際の位置を計算
                slot_words = slot_value.split()
                try:
                    # 最初の単語の位置を取得
                    first_word = slot_words[0]
                    word_position = words.index(first_word) + 1
                    
                    if slot_type.startswith('M'):
                        # M要素は単語ベースで記録
                        if slot_value not in word_positions:
                            word_positions[slot_value] = []
                        
                        # 文法的位置の判定
                        if word_position == 1:
                            grammar_role = "sentence_initial"
                        elif word_position == len(words) - len(slot_words) + 1:
                            grammar_role = "sentence_final"
                        else:
                            # S, V, Oとの相対位置で判定
                            s_pos = self._get_element_position(slots.get('S', ''), words)
                            v_pos = self._get_element_position(slots.get('V', ''), words)
                            
                            if word_position < v_pos:
                                if word_position < s_pos or word_position == s_pos + 1:
                                    grammar_role = "pre_subject_or_after_subject"
                                else:
                                    grammar_role = "pre_verb"
                            else:
                                grammar_role = "post_verb"
                        
                        word_positions[slot_value].append({
                            'sentence': sentence,
                            'position': word_position,
                            'grammar_role': grammar_role,
                            'context': f"{slot_type} in '{sentence}'"
                        })
                        
                        print(f"   🎯 '{slot_value}' → 位置{word_position} ({grammar_role})")
                        
                    else:
                        # 非M要素
                        element_key = f"{slot_type}_normal"
                        if element_key not in non_adverb_elements:
                            non_adverb_elements[element_key] = []
                        
                        non_adverb_elements[element_key].append({
                            'value': slot_value,
                            'sentence': sentence,
                            'position': word_position
                        })
                        
                        print(f"   📍 {slot_type}='{slot_value}' → 位置{word_position}")
                        
                except (ValueError, IndexError) as e:
                    print(f"   ❌ 位置特定エラー: {slot_value} - {e}")
        
        return word_positions, non_adverb_elements
    
    def _get_element_position(self, element_value, words):
        """要素の文中位置を取得"""
        if not element_value:
            return 0
        try:
            first_word = element_value.split()[0]
            return words.index(first_word) + 1
        except (ValueError, IndexError):
            return 0
    
    def determine_adverb_order_positions(self, word_positions):
        """副詞の順序位置を決定"""
        print(f"\n🔍 副詞の文法的順序位置決定:")
        
        adverb_order = {}
        
        for word, positions in word_positions.items():
            # 各副詞の文法的役割を分析
            roles = [pos['grammar_role'] for pos in positions]
            most_common_role = max(set(roles), key=roles.count)
            
            # 順序位置を決定
            if most_common_role == "sentence_initial":
                order_pos = 1
            elif most_common_role == "pre_subject_or_after_subject":
                order_pos = 3
            elif most_common_role == "pre_verb":
                order_pos = 3
            elif most_common_role == "post_verb":
                # さらに細分化：直後 vs 文末
                avg_pos = sum(pos['position'] for pos in positions) / len(positions)
                if avg_pos < 5:  # 相対的に早い位置
                    order_pos = 5
                else:  # 文末寄り
                    order_pos = 7
            elif most_common_role == "sentence_final":
                order_pos = 8
            else:
                order_pos = 5  # デフォルト
            
            adverb_order[word] = {
                'order_position': order_pos,
                'grammar_role': most_common_role,
                'positions': positions
            }
            
            print(f"  🎯 '{word}' → 順序{order_pos} ({most_common_role})")
        
        return adverb_order
    
    def build_final_order_mapping(self, non_adverb_elements, adverb_order):
        """最終的な順序マッピングを構築"""
        print(f"\n📊 最終順序マッピング構築:")
        
        # 非副詞要素の平均位置
        element_positions = {}
        for element_type, elements in non_adverb_elements.items():
            positions = [elem['position'] for elem in elements]
            avg_pos = sum(positions) / len(positions)
            element_positions[element_type] = avg_pos
            print(f"  📍 {element_type}: 平均位置={avg_pos:.2f}")
        
        # 全要素を統合
        all_elements = {}
        
        # 非副詞要素を追加
        for element_type, avg_pos in element_positions.items():
            all_elements[element_type] = avg_pos
        
        # 副詞を単語ベースで追加
        for word, info in adverb_order.items():
            all_elements[f"word_{word}"] = info['order_position']
        
        # ソートして番号を付与
        sorted_elements = sorted(all_elements.items(), key=lambda x: x[1])
        
        order_mapping = {}
        for i, (element, position) in enumerate(sorted_elements, 1):
            order_mapping[element] = i
            print(f"  {i}. {element} (位置: {position})")
        
        return order_mapping
    
    def apply_corrected_ordering(self, order_mapping, adverb_order):
        """修正された順序を適用"""
        print(f"\n✅ 修正版順序適用:")
        
        results = []
        
        for data in self.action_data:
            sentence = data["sentence"]
            slots = data["slots"]
            
            ordered_slots = {}
            
            for slot_type, slot_value in slots.items():
                if slot_type.startswith('M'):
                    # M要素は単語ベースで処理
                    word_key = f"word_{slot_value}"
                    if word_key in order_mapping:
                        order_num = order_mapping[word_key]
                        ordered_slots[str(order_num)] = slot_value
                else:
                    # 非M要素
                    element_key = f"{slot_type}_normal"
                    if element_key in order_mapping:
                        order_num = order_mapping[element_key]
                        ordered_slots[str(order_num)] = slot_value
            
            results.append({
                'sentence': sentence,
                'original_slots': slots,
                'ordered_slots': ordered_slots
            })
            
            print(f"  📝 {sentence}")
            print(f"     修正後: {ordered_slots}")
        
        return results

def test_word_based_fix():
    """単語ベース修正のテスト"""
    print("🚀 単語ベース副詞位置修正テスト")
    
    fixer = WordBasedAdverbFixer()
    
    # 1. 単語位置分析
    word_positions, non_adverb_elements = fixer.analyze_word_positions()
    
    # 2. 副詞順序位置決定
    adverb_order = fixer.determine_adverb_order_positions(word_positions)
    
    # 3. 最終順序マッピング構築
    order_mapping = fixer.build_final_order_mapping(non_adverb_elements, adverb_order)
    
    # 4. 修正版適用
    results = fixer.apply_corrected_ordering(order_mapping, adverb_order)
    
    # 5. 結果保存
    output_file = "word_based_corrected_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 修正版結果を {output_file} に保存しました")
    
    # 6. 問題のある例文の確認
    print(f"\n🔍 問題例文の修正確認:")
    for result in results:
        if "together" in result['sentence'] or "carefully" in result['sentence']:
            print(f"  📝 {result['sentence']}")
            print(f"     修正後順序: {result['ordered_slots']}")
            # 修正された語順を構築
            ordered_words = {}
            for pos, word in result['ordered_slots'].items():
                ordered_words[int(pos)] = word
            reconstructed = " ".join([ordered_words[i] for i in sorted(ordered_words.keys())])
            print(f"     修正された語順: {reconstructed}")
    
    return results

if __name__ == "__main__":
    test_word_based_fix()
