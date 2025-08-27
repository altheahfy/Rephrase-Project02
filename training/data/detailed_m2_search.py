import json
import os

def find_all_m2_slots(filename):
    """全てのM2スロットを検索"""
    print(f"\n=== {filename} ===")
    
    if not os.path.exists(filename):
        print(f"ファイルが見つかりません: {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    m2_records = []
    
    for record in data:
        if record.get('slot_name') == 'M2':
            m2_records.append(record)
    
    print(f"M2スロット総数: {len(m2_records)}")
    
    # V_group_keyごとにまとめて表示
    by_v_group = {}
    for record in m2_records:
        v_group = record.get('V_group_key', 'unknown')
        if v_group not in by_v_group:
            by_v_group[v_group] = []
        by_v_group[v_group].append(record)
    
    for v_group, records in by_v_group.items():
        print(f"\nV_group_key: {v_group} ({len(records)}個)")
        for i, record in enumerate(records[:3]):  # 最初の3個だけ表示
            print(f"  例文{i+1}: {record.get('example_text', '')}")
            print(f"  M2値: {record.get('slot_value', '')}")
            print(f"  Example ID: {record.get('example_id')}")
            if i == 0:  # 最初の1個だけ詳細表示
                print(f"  詳細: {json.dumps(record, ensure_ascii=False, indent=4)}")
            print()
        if len(records) > 3:
            print(f"  ... その他{len(records)-3}個")
    
    return m2_records

def find_do_group_records(filename):
    """V_group_key:doの全レコードを検索"""
    print(f"\n=== {filename} のV_group_key:do ===")
    
    if not os.path.exists(filename):
        print(f"ファイルが見つかりません: {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    do_records = []
    for record in data:
        if record.get('V_group_key') == 'do':
            do_records.append(record)
    
    print(f"V_group_key:doのレコード総数: {len(do_records)}")
    
    # スロット名ごとにカウント
    slot_counts = {}
    for record in do_records:
        slot_name = record.get('slot_name', 'unknown')
        slot_counts[slot_name] = slot_counts.get(slot_name, 0) + 1
    
    print("スロット別カウント:")
    for slot_name, count in sorted(slot_counts.items()):
        print(f"  {slot_name}: {count}個")
    
    return do_records

def main():
    file1 = "V自動詞第1文型.json"
    file2 = "slot_order_data_第4文型と極性.json"
    
    print("=== 全M2スロット検索 ===")
    m2_1 = find_all_m2_slots(file1)
    m2_2 = find_all_m2_slots(file2)
    
    print("\n=== V_group_key:do検索 ===")
    do_1 = find_do_group_records(file1)
    do_2 = find_do_group_records(file2)

if __name__ == "__main__":
    main()
