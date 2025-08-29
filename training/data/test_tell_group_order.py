#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tellグループのorder付けテストスクリプト
分解結果を使ってAbsoluteOrderManagerでorder付けを実行
"""

import json
import sys
from pathlib import Path

# パス設定
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from absolute_order_manager_group_fixed import AbsoluteOrderManager

def load_decomposition_results(filename):
    """分解結果ファイルを読み込み"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON読み込みエラー: {e}")
        return None

def prepare_group_population(decomposition_data):
    """
    分解結果からgroup_population形式のデータを準備
    """
    group_population = []
    
    for case_key, case_data in decomposition_data.items():
        if case_data.get('match', False):  # 成功したケースのみ
            actual_data = case_data.get('actual', {})
            main_slots = actual_data.get('main_slots', {})
            
            # group_population形式に変換
            sentence_data = {
                "case": case_key,
                "sentence": case_data.get('sentence', ''),
                "slots": main_slots
            }
            group_population.append(sentence_data)
            
    return group_population

def test_tell_group_ordering():
    """tellグループのorder付けテスト"""
    print("🎯 tellグループ order付けテスト開始")
    print("=" * 60)
    
    # 1. 分解結果読み込み
    decomposition_data = load_decomposition_results("tell_group_decomposition.json")
    if not decomposition_data:
        return
    
    print(f"📊 読み込み完了: {len(decomposition_data)} ケース")
    
    # 2. group_population形式に変換
    group_population = prepare_group_population(decomposition_data)
    print(f"📋 group_population準備完了: {len(group_population)} 有効ケース")
    
    # 3. AbsoluteOrderManagerインスタンス作成
    order_manager = AbsoluteOrderManager()
    
    # 4. 各ケースでorder付けテスト
    print("\n🔄 individual order付けテスト:")
    print("-" * 40)
    
    for i, sentence_data in enumerate(group_population, 1):
        case = sentence_data['case']
        sentence = sentence_data['sentence']
        slots = sentence_data['slots']
        
        print(f"\n📝 Case {i}: {case}")
        print(f"   例文: {sentence}")
        print(f"   スロット: {slots}")
        
        # group_populationを使ってorder付け
        try:
            slot_positions = order_manager.apply_absolute_order(
                slots=slots,
                v_group_key="tell_group",
                group_population=group_population
            )
            
            print(f"   🎯 Order結果:")
            for pos_data in slot_positions:
                slot_name = pos_data['slot']
                value = pos_data['value']
                position = pos_data['absolute_position']
                print(f"      {slot_name}({value}) → position {position}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 5. グループ統一order付けテスト
    print(f"\n🌟 グループ統一order付けテスト:")
    print("-" * 40)
    
    # 最初のケースを代表として使用
    if group_population:
        representative_case = group_population[0]
        slots = representative_case['slots']
        
        print(f"📝 代表ケース: {representative_case['case']}")
        print(f"   例文: {representative_case['sentence']}")
        
        try:
            slot_positions = order_manager.apply_absolute_order(
                slots=slots,
                v_group_key="tell_group",
                group_population=group_population
            )
            
            print(f"🎯 統一Order結果:")
            sorted_positions = sorted(slot_positions, key=lambda x: x['absolute_position'])
            
            for pos_data in sorted_positions:
                slot_name = pos_data['slot']
                value = pos_data['value']
                position = pos_data['absolute_position']
                print(f"   position {position}: {slot_name}({value})")
                
            # tellグループの標準順序を表示
            print(f"\n📊 tellグループ標準順序:")
            positions_only = [pos_data['absolute_position'] for pos_data in sorted_positions]
            slots_only = [pos_data['slot'] for pos_data in sorted_positions]
            print(f"   positions: {positions_only}")
            print(f"   slots: {slots_only}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ tellグループ order付けテスト完了")

if __name__ == "__main__":
    test_tell_group_ordering()
