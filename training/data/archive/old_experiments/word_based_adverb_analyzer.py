#!/usr/bin/env python3
"""
単語ベース副詞位置分析システム
M要素をスロットIDではなく単語そのものでメタセル配置
"""

import json
from pathlib import Path
import sys

# 既存システムのインポート
from central_controller import CentralController

class WordBasedAdverbAnalyzer:
    def __init__(self):
        self.controller = CentralController()
        
    def analyze_adverb_positions_by_word(self, sentences):
        """単語ベースで副詞位置を分析"""
        print("🚀 単語ベース副詞位置分析開始")
        
        # 1. 全例文から要素を抽出
        all_elements = {}
        word_positions = {}  # 単語別の位置情報
        
        for i, sentence in enumerate(sentences):
            print(f"  📝 例文{i+1}: {sentence}")
            
            # スロット解析
            try:
                slots = self.controller.parse_sentence_to_slots(sentence, "action")
                print(f"     スロット: {slots}")
            except Exception as e:
                print(f"     ❌ 解析エラー: {e}")
                continue
            
            # 実際の単語位置を取得（文中での出現順序）
            words = sentence.replace(',', '').replace('.', '').split()
            
            # 各スロットの単語を位置と共に記録
            for slot_type, slot_value in slots.items():
                slot_words = slot_value.split()
                
                # 単語の文中位置を特定
                for word in slot_words:
                    if word in words:
                        word_position = words.index(word) + 1
                        
                        # M要素は単語ベースで記録
                        if slot_type.startswith('M'):
                            if slot_value not in word_positions:
                                word_positions[slot_value] = []
                            word_positions[slot_value].append({
                                'sentence': sentence,
                                'position': word_position,
                                'context': self._get_word_context(slot_value, sentence)
                            })
                        else:
                            # 非M要素は従来通りスロットベース
                            element_key = f"{slot_type}_normal"
                            if element_key not in all_elements:
                                all_elements[element_key] = []
                            all_elements[element_key].append({
                                'value': slot_value,
                                'sentence': sentence,
                                'position': word_position
                            })
        
        print(f"\n🔍 副詞単語の位置パターン分析:")
        for word, positions in word_positions.items():
            print(f"  📝 '{word}':")
            for pos_info in positions:
                print(f"    → {pos_info['context']} (位置: {pos_info['position']})")
        
        # 2. 副詞の文法的位置パターンを分析
        adverb_patterns = self._analyze_adverb_patterns(word_positions)
        
        # 3. 非M要素の平均位置計算
        element_avg_positions = {}
        for element_type, elements in all_elements.items():
            positions = [elem['position'] for elem in elements]
            avg_pos = sum(positions) / len(positions)
            element_avg_positions[element_type] = avg_pos
            print(f"  ✅ {element_type}: 平均位置={avg_pos:.2f}")
        
        # 4. 統合順序の構築
        final_order = self._build_integrated_order(element_avg_positions, adverb_patterns)
        
        return final_order, word_positions, adverb_patterns
    
    def _get_word_context(self, word_phrase, sentence):
        """単語の文脈情報を取得"""
        words = sentence.replace(',', '').replace('.', '').split()
        phrase_words = word_phrase.split()
        
        try:
            start_idx = words.index(phrase_words[0])
            if start_idx == 0:
                return f"文頭: {sentence}"
            elif start_idx == len(words) - len(phrase_words):
                return f"文末: {sentence}"
            else:
                return f"文中: {sentence}"
        except ValueError:
            return f"不明: {sentence}"
    
    def _analyze_adverb_patterns(self, word_positions):
        """副詞の文法的位置パターンを分析"""
        patterns = {}
        
        for word, positions in word_positions.items():
            # 位置パターンの分析
            position_list = [pos['position'] for pos in positions]
            avg_position = sum(position_list) / len(position_list)
            
            # 文法的役割の推定
            contexts = [pos['context'] for pos in positions]
            
            if any('文頭' in ctx for ctx in contexts):
                role = 'sentence_initial'
                order_position = 1
            elif any('文末' in ctx for ctx in contexts):
                role = 'sentence_final'
                order_position = 10  # 後に調整
            elif avg_position < 3:
                role = 'pre_verb'
                order_position = 3
            else:
                role = 'post_verb'
                order_position = 5
            
            patterns[word] = {
                'role': role,
                'avg_position': avg_position,
                'order_position': order_position,
                'contexts': contexts
            }
            
            print(f"  🎯 '{word}' → {role} (順序位置: {order_position})")
        
        return patterns
    
    def _build_integrated_order(self, element_positions, adverb_patterns):
        """統合順序を構築"""
        all_order_elements = {}
        
        # 非M要素を追加
        for element_type, avg_pos in element_positions.items():
            all_order_elements[element_type] = avg_pos
        
        # M要素（副詞）を単語ベースで追加
        for word, pattern in adverb_patterns.items():
            all_order_elements[f"word_{word}"] = pattern['order_position']
        
        # 順序でソート
        sorted_elements = sorted(all_order_elements.items(), key=lambda x: x[1])
        
        print(f"\n📊 統合最終順序:")
        for i, (element, position) in enumerate(sorted_elements, 1):
            print(f"  {i}. {element} (位置: {position:.2f})")
        
        # 番号マッピングを作成
        order_mapping = {}
        for i, (element, _) in enumerate(sorted_elements, 1):
            order_mapping[element] = i
        
        return order_mapping
    
    def apply_word_based_ordering(self, sentences, order_mapping, adverb_patterns):
        """単語ベース順序を適用"""
        results = []
        
        for sentence in sentences:
            try:
                slots = self.controller.parse_sentence_to_slots(sentence, "action")
                ordered_slots = {}
                
                for slot_type, slot_value in slots.items():
                    if slot_type.startswith('M'):
                        # M要素は単語ベースで処理
                        word_key = f"word_{slot_value}"
                        if word_key in order_mapping:
                            order_num = order_mapping[word_key]
                            ordered_slots[str(order_num)] = slot_value
                    else:
                        # 非M要素は従来通り
                        element_key = f"{slot_type}_normal"
                        if element_key in order_mapping:
                            order_num = order_mapping[element_key]
                            ordered_slots[str(order_num)] = slot_value
                
                results.append({
                    'sentence': sentence,
                    'original_slots': slots,
                    'ordered_slots': ordered_slots
                })
                
                print(f"✅ {sentence}")
                print(f"  🎯 単語ベース結果: {ordered_slots}")
                
            except Exception as e:
                print(f"❌ 処理エラー: {sentence} - {e}")
        
        return results

def test_word_based_approach():
    """単語ベースアプローチのテスト"""
    print("🚀 単語ベース副詞位置分析テスト")
    
    # actionグループのテストデータ
    action_sentences = [
        "She sings beautifully.",
        "We always eat breakfast together.", 
        "The cat quietly sat on the mat.",
        "She carefully reads books.",
        "They run fast.",
        "Actually, she works very hard.",
        "Every morning, he jogs slowly in the park."
    ]
    
    analyzer = WordBasedAdverbAnalyzer()
    
    # 分析実行
    order_mapping, word_positions, adverb_patterns = analyzer.analyze_adverb_positions_by_word(action_sentences)
    
    # 結果適用
    results = analyzer.apply_word_based_ordering(action_sentences, order_mapping, adverb_patterns)
    
    # 結果保存
    output_file = "word_based_action_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 単語ベース結果を {output_file} に保存しました")
    
    return results

if __name__ == "__main__":
    test_word_based_approach()
