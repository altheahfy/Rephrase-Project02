#!/usr/bin/env python3
"""
DB比較分析スクリプト
正常なDBと問題のDBの構造を詳細比較
"""

import json
import os

def analyze_db_structure(filename, db_name):
    """DBの構造を詳細分析"""
    
    print(f"\n📊 {db_name} ({filename}) 分析")
    print("-" * 60)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 読み込みエラー: {e}")
        return None
    
    # 基本統計
    total_records = len(data)
    print(f"総レコード数: {total_records}")
    
    # 例文IDの分析
    example_ids = set()
    empty_example_ids = 0
    
    for record in data:
        ex_id = record.get("例文ID", "")
        if ex_id:
            example_ids.add(ex_id)
        else:
            empty_example_ids += 1
    
    print(f"ユニーク例文ID数: {len(example_ids)}")
    print(f"空の例文ID: {empty_example_ids}件")
    print(f"例文ID範囲: {sorted(list(example_ids))[:3]}...{sorted(list(example_ids))[-3:]}")
    
    # 最初の例文の詳細分析
    first_example_id = None
    for record in data:
        if record.get("例文ID"):
            first_example_id = record["例文ID"]
            break
    
    if first_example_id:
        first_example_data = [r for r in data if r.get("例文ID") == first_example_id]
        print(f"\n🔍 最初の例文 {first_example_id}:")
        print(f"  スロット数: {len(first_example_data)}")
        
        slots_info = []
        for record in first_example_data:
            slot_name = record.get("Slot", "")
            phrase = record.get("SlotPhrase", "")
            phrase_type = record.get("PhraseType", "")
            display_order = record.get("Slot_display_order", 0)
            
            slots_info.append({
                'slot': slot_name,
                'phrase': phrase,
                'type': phrase_type,
                'order': display_order
            })
        
        # 表示順でソート
        slots_info.sort(key=lambda x: x['order'])
        
        for slot_info in slots_info:
            print(f"  {slot_info['order']:2d}. {slot_info['slot']:4s} | '{slot_info['phrase'][:30]}' | {slot_info['type']}")
    
    # フィールド構造の確認
    if data:
        sample_record = data[0]
        print(f"\n📋 フィールド構造:")
        for key, value in sample_record.items():
            value_type = type(value).__name__
            value_str = str(value)[:50]
            print(f"  {key}: {value_type} = '{value_str}'")
    
    return {
        'total_records': total_records,
        'example_ids': example_ids,
        'empty_example_ids': empty_example_ids,
        'first_example': first_example_data if first_example_id else [],
        'sample_record': data[0] if data else {}
    }

def compare_databases():
    """複数のDBを比較"""
    
    print("🔍 データベース構造比較分析")
    print("=" * 80)
    
    # 比較対象のDBファイル
    databases = [
        ("slot_order_data.json", "フルセット（正常）"),
        ("slot_order_data_第4文型と極性.json", "第4文型と極性（問題）"),
        ("V自動詞第1文型.json", "V自動詞第1文型"),
    ]
    
    db_results = {}
    
    for filename, db_name in databases:
        if os.path.exists(filename):
            result = analyze_db_structure(filename, db_name)
            db_results[db_name] = result
        else:
            print(f"\n⚠️ {filename} が見つかりません")
    
    # 比較結果
    print("\n" + "=" * 80)
    print("🔍 比較結果サマリー")
    print("=" * 80)
    
    for db_name, result in db_results.items():
        if result:
            print(f"\n📊 {db_name}:")
            print(f"  総レコード: {result['total_records']}")
            print(f"  例文数: {len(result['example_ids'])}")
            print(f"  空例文ID: {result['empty_example_ids']}")
            print(f"  最初例文のスロット数: {len(result['first_example'])}")
    
    # 詳細な差異を探す
    print("\n🔍 詳細差異分析:")
    
    if "フルセット（正常）" in db_results and "第4文型と極性（問題）" in db_results:
        normal_db = db_results["フルセット（正常）"]
        problem_db = db_results["第4文型と極性（問題）"]
        
        # フィールド構造比較
        normal_fields = set(normal_db['sample_record'].keys())
        problem_fields = set(problem_db['sample_record'].keys())
        
        if normal_fields == problem_fields:
            print("  ✅ フィールド構造は同一")
        else:
            print("  ❌ フィールド構造に差異あり")
            print(f"    正常DBのみ: {normal_fields - problem_fields}")
            print(f"    問題DBのみ: {problem_fields - normal_fields}")
        
        # 値の型比較
        print("  📝 フィールド値の型比較:")
        for field in normal_fields & problem_fields:
            normal_val = normal_db['sample_record'][field]
            problem_val = problem_db['sample_record'][field]
            normal_type = type(normal_val).__name__
            problem_type = type(problem_val).__name__
            
            if normal_type != problem_type:
                print(f"    ❌ {field}: {normal_type} vs {problem_type}")
            elif str(normal_val) != str(problem_val):
                print(f"    ⚠️ {field}: '{normal_val}' vs '{problem_val}'")

if __name__ == "__main__":
    compare_databases()
