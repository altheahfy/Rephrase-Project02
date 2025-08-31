#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
副詞位置分析専用システム
Pure Data-Driven Absolute Order Manager
完全にデータ駆動型の汎用語順分析システム
"""

import json

class PureDataDrivenOrderManager:
    """
    副詞位置分析システム
    Pure Data-Driven: 実際の例文データから語順パターンを学習
    汎用性: 任意のスロット構造と例文群に対応
    """
    
    def __init__(self):
        # 汎用疑問詞セット（拡張可能）
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
                if slot_key == 'M1':
                    # M1の位置別分離（既存ロジック）
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
                    
                    # 文中版 - M2_pre_verbと統合するため、pre_verb_generalとして扱う
                    if mid_sentence_values:
                        element_groups[f"M_pre_verb"] = element_groups.get(f"M_pre_verb", {
                            'original_slot': 'M_pre_verb',
                            'values': set(),
                            'type': 'pre_verb'
                        })
                        element_groups[f"M_pre_verb"]['values'].update(mid_sentence_values)
                        print(f"  📝 M_pre_verb (M1): {mid_sentence_values}")
                
                elif slot_key == 'M2':
                    # M2の動詞前後分離
                    sentence_initial_values = set()
                    pre_verb_values = set()
                    post_verb_values = set()
                    
                    for value in normal_values:
                        # 各例文でこの値の出現位置をチェック
                        is_sentence_initial = False
                        is_pre_verb = False
                        
                        for data in sentences_data:
                            if slot_key in data['slots'] and data['slots'][slot_key] == value:
                                sentence = data['sentence']
                                # 位置を計算
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
                                
                                # M2の位置を特定
                                if slot_key in order_sequence:
                                    m2_position = order_sequence.index(slot_key)
                                    
                                    # 文頭チェック
                                    if m2_position == 0:
                                        is_sentence_initial = True
                                        print(f"    🔆 {value} は例文 '{sentence}' で文頭出現")
                                        break
                                    
                                    # 動詞（V）との位置関係をチェック
                                    v_position = -1
                                    for i, slot in enumerate(order_sequence):
                                        if slot == 'V':
                                            v_position = i
                                            break
                                    
                                    if v_position >= 0:
                                        if m2_position < v_position:
                                            is_pre_verb = True
                                            print(f"    📝 {value} は例文 '{sentence}' で動詞前出現（位置: {m2_position + 1}, V位置: {v_position + 1}）")
                                        else:
                                            print(f"    📝 {value} は例文 '{sentence}' で動詞後出現（位置: {m2_position + 1}, V位置: {v_position + 1}）")
                                    else:
                                        print(f"    📝 {value} は例文 '{sentence}' で文中出現（位置: {m2_position + 1}）")
                                break
                        
                        if is_sentence_initial:
                            sentence_initial_values.add(value)
                        elif is_pre_verb:
                            pre_verb_values.add(value)
                        else:
                            post_verb_values.add(value)
                    
                    # 文頭版
                    if sentence_initial_values:
                        element_groups[f"{slot_key}_sentence_initial"] = {
                            'original_slot': slot_key,
                            'values': sentence_initial_values,
                            'type': 'sentence_initial'
                        }
                        print(f"  🔆 {slot_key}_sentence_initial: {sentence_initial_values}")
                    
                    # 動詞前版 - M1_normalと統合するため、pre_verb_generalとして扱う
                    if pre_verb_values:
                        element_groups[f"M_pre_verb"] = element_groups.get(f"M_pre_verb", {
                            'original_slot': 'M_pre_verb',
                            'values': set(),
                            'type': 'pre_verb'
                        })
                        element_groups[f"M_pre_verb"]['values'].update(pre_verb_values)
                        print(f"  📝 M_pre_verb (M2): {pre_verb_values}")
                    
                    # 動詞後版（通常版）
                    if post_verb_values:
                        element_groups[f"{slot_key}_normal"] = {
                            'original_slot': slot_key,
                            'values': post_verb_values,
                            'type': 'normal'
                        }
                        print(f"  📝 {slot_key}_normal: {post_verb_values}")
                else:
                    # M1, M2以外の通常処理
                    element_groups[f"{slot_key}_normal"] = {
                        'original_slot': slot_key,
                        'values': normal_values,
                        'type': 'normal'
                    }
                    print(f"  📝 {slot_key}_normal: {normal_values}")
        
        # 統合グループの最終表示
        if "M_pre_verb" in element_groups:
            print(f"  🔧 M_pre_verb (統合): {element_groups['M_pre_verb']['values']}")
        
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
            
            if group_name == 'M_pre_verb':
                # 統合グループM_pre_verbの特別処理
                for data in sentences_data:
                    sentence = data['sentence']
                    slots = data['slots']
                    
                    # このグループの値が含まれているかチェック
                    for slot_k, slot_v in slots.items():
                        if slot_v in values:
                            # 出現位置を計算
                            slot_positions = []
                            remaining_sentence = sentence.lower()
                            
                            for s_k, s_v in slots.items():
                                pos = remaining_sentence.find(s_v.lower())
                                if pos != -1:
                                    slot_positions.append((pos, s_k))
                                    remaining_sentence = remaining_sentence.replace(s_v.lower(), ' ' * len(s_v), 1)
                            
                            slot_positions.sort()
                            order_sequence = [s_k for pos, s_k in slot_positions]
                            
                            if slot_k in order_sequence:
                                position = order_sequence.index(slot_k) + 1
                                positions.append(position)
                                print(f"    📍 {group_name}: 例文 '{sentence}' で位置{position} (要素: {slot_v})")
                            break
            else:
                # 通常のグループ処理
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
        
        # 同一例文内での相対制約をチェックして調整
        common_order_keys = self._adjust_for_sentence_constraints(sentences_data, element_groups, common_order_keys)
        
        print(f"✅ {len(sentences_data)}例文の副詞位置分析完了")
        print(f"📊 最終共通順序: {' → '.join(common_order_keys)}")
        
        return common_order_keys
    
    def _adjust_for_sentence_constraints(self, sentences_data, element_groups, initial_order):
        """
        同一例文内での相対制約に基づいて順序を調整
        """
        print("🔍 同一例文内の相対制約をチェック")
        
        # 各例文での要素グループ間の制約を収集
        constraints = []
        
        for data in sentences_data:
            sentence = data['sentence']
            slots = data['slots']
            
            # この例文に含まれるグループとその位置を特定
            sentence_groups = {}
            
            slot_positions = []
            remaining_sentence = sentence.lower()
            
            for slot_k, slot_v in slots.items():
                pos = remaining_sentence.find(slot_v.lower())
                if pos != -1:
                    slot_positions.append((pos, slot_k))
                    remaining_sentence = remaining_sentence.replace(slot_v.lower(), ' ' * len(slot_v), 1)
            
            slot_positions.sort()
            order_sequence = [slot_k for pos, slot_k in slot_positions]
            
            # 各スロットがどのグループに属するかを特定
            for i, slot_key in enumerate(order_sequence):
                slot_value = slots[slot_key]
                for group_name, group_info in element_groups.items():
                    if (group_info['original_slot'] == slot_key and 
                        slot_value in group_info['values']):
                        sentence_groups[group_name] = i + 1
                        break
            
            # この例文内でのグループ間制約を生成
            group_list = sorted(sentence_groups.items(), key=lambda x: x[1])
            for i in range(len(group_list) - 1):
                before_group = group_list[i][0]
                after_group = group_list[i + 1][0]
                constraints.append((before_group, after_group))
                print(f"    📏 制約: {before_group} < {after_group} (例文: '{sentence}')")
        
        # 制約を満たすように順序を調整
        adjusted_order = initial_order.copy()
        
        # 制約違反をチェックして修正（無限ループ防止）
        made_changes = True
        max_iterations = 50  # 最大試行回数
        iteration_count = 0
        
        while made_changes and iteration_count < max_iterations:
            made_changes = False
            iteration_count += 1
            
            for before_group, after_group in constraints:
                if before_group in adjusted_order and after_group in adjusted_order:
                    before_idx = adjusted_order.index(before_group)
                    after_idx = adjusted_order.index(after_group)
                    
                    if before_idx > after_idx:
                        # 制約違反を修正
                        print(f"    🔧 制約違反修正 (試行{iteration_count}): {before_group} と {after_group} の順序を調整")
                        adjusted_order.remove(before_group)
                        adjusted_order.insert(after_idx, before_group)
                        made_changes = True
                        
        if iteration_count >= max_iterations:
            print(f"⚠️ 制約調整が最大試行回数({max_iterations})に達しました。循環参照の可能性があります。")
            print(f"📋 現在の順序: {adjusted_order}")
            print(f"📋 制約一覧: {constraints}")
        
        return adjusted_order
    
    def _assign_adverb_numbers(self, sentences_data, common_order, element_groups):
        """
        副詞位置を考慮した番号付与
        """
        print(f"🔍 副詞位置を考慮した最終番号を付与")
        
        # グループ名から順序番号へのマッピングを作成
        group_to_order = {}
        for i, group_name in enumerate(common_order):
            group_to_order[group_name] = i + 1
        
        print(f"📊 グループ→順序マッピング: {group_to_order}")
        
        # 順序マッピングを保存（CentralControllerから参照用）
        self._group_order_mapping = group_to_order
        
        results = []
        for i, data in enumerate(sentences_data):
            sentence = data['sentence']
            slots = data['slots']
            
            ordered_slots = {}
            for slot_key, slot_value in slots.items():
                # このスロット値がどのグループに属するかを特定
                matched_group = None
                
                # 統合グループM_pre_verbを優先的にチェック
                if 'M_pre_verb' in element_groups and slot_value in element_groups['M_pre_verb']['values']:
                    matched_group = 'M_pre_verb'
                else:
                    # 通常のグループ検索
                    for group_name, group_info in element_groups.items():
                        if group_name != 'M_pre_verb' and (group_info['original_slot'] == slot_key and 
                            slot_value in group_info['values']):
                            matched_group = group_name
                            break
                
                if matched_group and matched_group in group_to_order:
                    order_num = group_to_order[matched_group]
                    ordered_slots[str(order_num)] = slot_value
                    print(f"  📝 {slot_key}={slot_value} → {matched_group} → 順序{order_num}")
                else:
                    print(f"  ❓ {slot_key}={slot_value} → マッチするグループが見つかりません")
            
            result = {
                'sentence': sentence,
                'original_slots': slots,
                'ordered_slots': ordered_slots
            }
            results.append(result)
            
            print(f"✅ 例文{i+1}: {sentence}")
            print(f"  🎯 副詞位置結果: {ordered_slots}")
        
        return results
    
    def apply_sub_slot_order(self, sub_slots: dict) -> dict:
        """
        サブスロットに文法的語順でdisplay_orderを付与
        
        Args:
            sub_slots: サブスロット辞書 {'sub-s': 'value', 'sub-v': 'value', ...}
            
        Returns:
            dict: ordered_sub_slots形式 {'sub-s': {'value': 'text', 'display_order': 1}, ...}
        """
        if not sub_slots:
            return {}
        
        print(f"🔧 サブスロット順序付け開始: {len(sub_slots)}要素")
        
        ordered_sub_slots = {}
        display_order = 1
        
        # _parent_slotを除外してサブスロット要素のみ処理
        for key, value in sub_slots.items():
            if not key.startswith('_') and value:  # メタ情報と空値を除外
                ordered_sub_slots[key] = {
                    'value': value,
                    'display_order': display_order
                }
                display_order += 1
        
        print(f"🔧 サブスロット順序付け完了: {len(ordered_sub_slots)}要素")
        return ordered_sub_slots

def main():
    """メイン関数 - 副詞を含むグループを一括処理"""
    print("🚀 副詞位置分析システム開始")
    
    analyzer = PureDataDrivenOrderManager()
    
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
            output_file = f'results/adverb_{v_group_key}_group_results.json'
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
    
def main():
    """実行メイン関数"""
    order_manager = PureDataDrivenOrderManager()
    
    all_results = {}
    
    # 副詞グループを取得
    groups = order_manager.extract_adverb_groups()
    
    for v_group_key, examples in groups.items():
        print(f"\n{'='*50}")
        print(f"🎯 グループ: {v_group_key}")
        print(f"{'='*50}")
        
        try:
            results = order_manager.process_adverb_group(v_group_key, examples)
            
            if results:
                all_results[v_group_key] = results
                
                print(f"\n🎉 分析完了: {v_group_key}グループ ({len(examples)}例文)")
                for i, result in enumerate(results):
                    print(f"例文{i+1}: {result['sentence']}")
                    print(f"順序: {result['ordered_slots']}")
                    print()
                    
        except Exception as e:
            print(f"❌ {v_group_key}グループの処理でエラー: {e}")
    
    # 全結果を統合保存
    if all_results:
        with open('results/all_adverb_groups_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
            
        print(f"\n🎉 全副詞グループ分析完了")
        print(f"📊 分析したグループ: {list(all_results.keys())}")
        print(f"💾 統合結果を results/all_adverb_groups_analysis.json に保存しました")

if __name__ == "__main__":
    main()
