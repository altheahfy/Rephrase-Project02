import json
import os

def find_m2_slots_corrected(filename):
    """正しいフィールド名でM2スロットを検索"""
    print(f"\n=== {filename} ===")
    
    if not os.path.exists(filename):
        print(f"ファイルが見つかりません: {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    m2_records = []
    
    for record in data:
        if record.get('Slot') == 'M2':  # 'slot_name'ではなく'Slot'
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
        for i, record in enumerate(records[:2]):  # 最初の2個だけ表示
            print(f"  例文{i+1}: 例文ID={record.get('例文ID')}")
            print(f"  SlotPhrase: {record.get('SlotPhrase', '')}")
            print(f"  SubslotElement: {record.get('SubslotElement', '')}")
            print(f"  PhraseType: {record.get('PhraseType', '')}")
            print(f"  詳細: {json.dumps(record, ensure_ascii=False, indent=4)}")
            print()
    
    return m2_records

def find_do_group_with_m2(filename):
    """V_group_key:doでM2スロットのある例文を検索"""
    print(f"\n=== {filename} のV_group_key:doでM2検索 ===")
    
    if not os.path.exists(filename):
        print(f"ファイルが見つかりません: {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    do_m2_records = []
    for record in data:
        if record.get('V_group_key') == 'do' and record.get('Slot') == 'M2':
            do_m2_records.append(record)
    
    print(f"V_group_key:doのM2レコード数: {len(do_m2_records)}")
    
    for i, record in enumerate(do_m2_records):
        print(f"\nレコード{i+1}:")
        print(f"  例文ID: {record.get('例文ID')}")
        print(f"  SlotPhrase: {record.get('SlotPhrase')}")
        print(f"  SubslotElement: {record.get('SubslotElement')}")
        print(f"  PhraseType: {record.get('PhraseType')}")
        print(f"  詳細: {json.dumps(record, ensure_ascii=False, indent=2)}")
    
    return do_m2_records

def main():
    file1 = "V自動詞第1文型.json"
    file2 = "slot_order_data_第4文型と極性.json"
    
    print("=== 修正版M2スロット検索 ===")
    m2_1 = find_m2_slots_corrected(file1)
    m2_2 = find_m2_slots_corrected(file2)
    
    print("\n=== V_group_key:doのM2検索 ===")
    do_m2_1 = find_do_group_with_m2(file1)
    do_m2_2 = find_do_group_with_m2(file2)
    
    print(f"\n=== 比較結果 ===")
    print(f"{file1}: M2={len(m2_1)}個, do+M2={len(do_m2_1)}個")
    print(f"{file2}: M2={len(m2_2)}個, do+M2={len(do_m2_2)}個")

if __name__ == "__main__":
    main()
