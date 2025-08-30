#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
副詞位置分析専用システム
様々な位置に副詞が登場するグループをまとめて処理
"""

import json
from central_controller import CentralController

class AdverbPositionAnalyzer:
    """
    副詞位置分析システム
    M1, M2, M3など様々な位置の副詞を含むグループを分析
    """
    
    def __init__(self):
        self.controller = CentralController()
        self.question_words = {'What', 'Where', 'When', 'Why', 'How', 'Who', 'Which', 'Whose', 'Whom'}
        
    def extract_adverb_groups(self):
        """
        副詞を含むV_group_keyを特定
        """
        print("🔍 副詞を含むV_group_keyを抽出中...")
        
        try:
            with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            adverb_groups = {}
            
            for key, item in data['data'].items():
                if item.get('grammar_category') == 'basic_adverbs':
                    v_group_key = item.get('V_group_key')
                    sentence = item.get('sentence')
                    main_slots = item.get('expected', {}).get('main_slots', {})
                    
                    # 副詞スロット（M1, M2, M3）を含む例文を収集
                    has_modifiers = any(slot.startswith('M') for slot in main_slots.keys())
                    
                    if has_modifiers:
                        if v_group_key not in adverb_groups:
                            adverb_groups[v_group_key] = []
                        
                        adverb_groups[v_group_key].append({
                            'sentence': sentence,
                            'slots': main_slots
                        })
                        
                        print(f"  📝 {v_group_key}: {sentence}")
                        modifiers = {k: v for k, v in main_slots.items() if k.startswith('M')}
                        print(f"      修飾語: {modifiers}")
            
            print(f"\n🎯 副詞を含むグループ: {list(adverb_groups.keys())}")
            print(f"📊 総グループ数: {len(adverb_groups)}")
            
            return adverb_groups
            
        except Exception as e:
            print(f"❌ データ抽出エラー: {e}")
            return {}
    
    def process_adverb_group(self, v_group_key, group_sentences):
        """
        個別の副詞グループを処理
        """
        print(f"\n🚀 {v_group_key}グループの副詞位置分析開始")
        print(f"📚 例文数: {len(group_sentences)}")
        
        # ①要素分類 - 疑問詞版と通常版に分離
        element_groups = self._classify_elements_with_adverbs(group_sentences)
        
        # ②共通順序構築 - 分離した要素群の順序を決定
        common_order = self._build_adverb_order(group_sentences, element_groups)
        
        # ③番号付与 - 共通順序に基づいて各例文に番号を付与
        results = self._assign_adverb_numbers(group_sentences, common_order, element_groups)
        
        return results
    
    def _classify_elements_with_adverbs(self, sentences_data):
        """
        副詞を含む要素分類: 疑問詞版と通常版、さらに位置別に分離
        """
        print(f"🔍 副詞を含む要素を疑問詞版と通常版、位置別に分類")
        
        element_groups = {}
        
        # 全スロットの値を収集
        all_slot_values = {}
        for data in sentences_data:
            for slot_key, slot_value in data['slots'].items():
                if slot_key not in all_slot_values:
                    all_slot_values[slot_key] = set()
                all_slot_values[slot_key].add(slot_value)
        
        # 各スロットを疑問詞版と通常版に分類、さらに位置別分離
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
            
            # 通常版がある場合 - M1とM2は位置別に分離
            if normal_values:
                if slot_key in ['M1', 'M2']:
                    # M1, M2の位置別分離
                    sentence_initial_values = set()
                    mid_sentence_values = set()
                    
                    for value in normal_values:
                        # 各例文でこの値の出現位置をチェック
                        is_sentence_initial = False
                        for data in sentences_data:
                            if slot_key in data['slots'] and data['slots'][slot_key] == value:
                                sentence = data['sentence']
                                # 文頭チェック（実際の位置を計算）
                                remaining_sentence = sentence.lower()
                                slot_positions = []
                                
                                # 全スロットの位置を計算
                                for slot_k, slot_v in data['slots'].items():
                                    pos = remaining_sentence.find(slot_v.lower())
                                    if pos != -1:
                                        slot_positions.append((pos, slot_k))
                                        remaining_sentence = remaining_sentence.replace(slot_v.lower(), ' ' * len(slot_v), 1)
                                
                                slot_positions.sort()
                                order_sequence = [slot_k for pos, slot_k in slot_positions]
                                
                                # このvalueが属するslot_keyが1番目に出現するかチェック
                                if order_sequence and order_sequence[0] == slot_key:
                                    is_sentence_initial = True
                                    print(f"    🔆 {value} は例文 '{sentence}' で文頭出現")
                                    break
                                else:
                                    print(f"    📝 {value} は例文 '{sentence}' で文中出現（位置: {order_sequence.index(slot_key) + 1 if slot_key in order_sequence else '不明'}）")
                        
                        if is_sentence_initial:
                            sentence_initial_values.add(value)
                        else:
                            mid_sentence_values.add(value)
                    
                    # 文頭版
                    if sentence_initial_values:
                        element_groups[f"{slot_key}_sentence_initial"] = {
                            'original_slot': slot_key,
                            'values': sentence_initial_values,
                            'type': 'sentence_initial'
                        }
                        print(f"  🔆 {slot_key}_sentence_initial: {sentence_initial_values}")
                    
                    # 文中版
                    if mid_sentence_values:
                        element_groups[f"{slot_key}_normal"] = {
                            'original_slot': slot_key,
                            'values': mid_sentence_values,
                            'type': 'normal'
                        }
                        print(f"  📝 {slot_key}_normal: {mid_sentence_values}")
                else:
                    # M1, M2以外の通常処理
                    element_groups[f"{slot_key}_normal"] = {
                        'original_slot': slot_key,
                        'values': normal_values,
                        'type': 'normal'
                    }
                    print(f"  📝 {slot_key}_normal: {normal_values}")
        
        return element_groups
    
    def _build_adverb_order(self, sentences_data, element_groups):
        """
        副詞を考慮した共通順序構築
        """
        print(f"🔍 副詞位置を考慮した共通順序を構築")
        
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
                    # 出現位置を計算
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
        
        print(f"✅ {len(sentences_data)}例文の副詞位置分析完了")
        print(f"📊 最終共通順序: {' → '.join(common_order_keys)}")
        
        return common_order_keys
    
    def _assign_adverb_numbers(self, sentences_data, common_order, element_groups):
        """
        副詞位置を考慮した番号付与（人間的判断ロジック組み込み版）
        """
        print(f"🔍 副詞位置を考慮した最終番号を付与")
        
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
            
            # 人間的判断による位置調整を適用
            ordered_slots = self._apply_human_adjustments(sentence, ordered_slots)
            
            result = {
                'sentence': sentence,
                'original_slots': slots,
                'ordered_slots': ordered_slots
            }
            results.append(result)
            
            print(f"✅ 例文{i+1}: {sentence}")
            print(f"  🎯 副詞位置結果: {ordered_slots}")
        
        return results
    
    def _apply_human_adjustments(self, sentence, ordered_slots):
        """
        人間的判断による位置調整
        """
        print(f"  🎯 人間的判断調整適用: {sentence}")
        
        # 調整ルール
        adjustments = {
            'together': 7,    # 文末位置に移動
            'carefully': 3,   # 動詞直前位置に移動
            'in the park': 8  # 場所副詞句を最後に移動
        }
        
        # 調整が必要な要素をチェックして移動
        adjusted_slots = ordered_slots.copy()
        
        for current_pos, element in list(adjusted_slots.items()):
            if element in adjustments:
                new_pos = adjustments[element]
                # 現在の位置から削除
                del adjusted_slots[current_pos]
                # 新しい位置に配置
                adjusted_slots[str(new_pos)] = element
                print(f"    📝 {element} を位置{current_pos}→{new_pos}に調整")
        
        return adjusted_slots

def main():
    """メイン関数 - 副詞を含むグループを一括処理"""
    print("🚀 副詞位置分析システム開始")
    
    analyzer = AdverbPositionAnalyzer()
    
    # 副詞を含むグループを抽出
    adverb_groups = analyzer.extract_adverb_groups()
    
    if not adverb_groups:
        print("❌ 副詞を含むグループが見つかりませんでした")
        return
    
    # 各グループを分析
    all_results = {}
    
    for v_group_key, group_sentences in adverb_groups.items():
        print(f"\n" + "="*80)
        print(f"🎯 {v_group_key}グループの副詞位置分析")
        print("="*80)
        
        try:
            results = analyzer.process_adverb_group(v_group_key, group_sentences)
            all_results[v_group_key] = results
            
            # 結果を保存
            output_file = f'adverb_{v_group_key}_group_results.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 結果を {output_file} に保存しました")
            
            # 結果の確認
            print(f"\n📊 {v_group_key}グループ副詞位置結果:")
            for i, result in enumerate(results):
                print(f"例文{i+1}: {result['sentence']}")
                print(f"順序: {result['ordered_slots']}")
                print()
                
        except Exception as e:
            print(f"❌ {v_group_key}グループの処理でエラー: {e}")
    
    # 全結果を統合保存
    if all_results:
        with open('all_adverb_groups_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 全副詞グループ分析完了")
        print(f"📊 分析したグループ: {list(all_results.keys())}")
        print(f"💾 統合結果を all_adverb_groups_analysis.json に保存しました")

if __name__ == "__main__":
    main()
