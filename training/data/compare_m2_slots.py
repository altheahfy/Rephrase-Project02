import json
import os

def find_m2_in_do_group(filename):
    """V_group_key:doでM2要素を含む例文を検索"""
    print(f"\n=== {filename} ===")
    
    if not os.path.exists(filename):
        print(f"ファイルが見つかりません: {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    m2_examples = []
    
    for record in data:
        # V_group_key が "do" で slot_name が "M2" のレコードを検索
        if record.get('V_group_key') == 'do' and record.get('slot_name') == 'M2':
            example_id = record.get('example_id')
            example_text = record.get('example_text', '')
            slot_value = record.get('slot_value', '')
            
            print(f"Example ID: {example_id}")
            print(f"Example Text: {example_text}")
            print(f"M2 Slot Value: {slot_value}")
            print(f"Full Record: {json.dumps(record, ensure_ascii=False, indent=2)}")
            print("-" * 50)
            
            m2_examples.append(record)
    
    print(f"見つかったM2例文数: {len(m2_examples)}")
    return m2_examples

def compare_m2_structures():
    """両ファイルのM2構造を比較"""
    file1 = "V自動詞第1文型.json"
    file2 = "slot_order_data_第4文型と極性.json"
    
    print("V_group_key:doのM2要素を比較中...")
    
    m2_examples_1 = find_m2_in_do_group(file1)
    m2_examples_2 = find_m2_in_do_group(file2)
    
    print(f"\n=== 比較結果 ===")
    print(f"{file1}: {len(m2_examples_1)}個のM2例文")
    print(f"{file2}: {len(m2_examples_2)}個のM2例文")
    
    # 同じexample_idがある場合の詳細比較
    if m2_examples_1 and m2_examples_2:
        print(f"\n=== 構造比較 ===")
        print(f"正常動作 ({file1})の構造:")
        if m2_examples_1:
            example = m2_examples_1[0]
            for key, value in example.items():
                print(f"  {key}: {value}")
        
        print(f"\n問題ファイル ({file2})の構造:")
        if m2_examples_2:
            example = m2_examples_2[0]
            for key, value in example.items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    compare_m2_structures()
