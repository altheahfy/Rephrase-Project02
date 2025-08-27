import json

def debug_m2_subslot_ids():
    """M2サブスロットのSubslotID値を詳しく調べる"""
    
    files = ["V自動詞第1文型.json", "slot_order_data_第4文型と極性.json"]
    
    for filename in files:
        print(f"\n=== {filename} ===")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filename}")
            continue
        
        # V_group_key:doのM2サブスロットを検索
        m2_subslots = []
        for record in data:
            if (record.get('V_group_key') == 'do' and 
                record.get('Slot') == 'M2' and 
                record.get('SubslotID')):
                m2_subslots.append(record)
        
        print(f"V_group_key:doのM2サブスロット数: {len(m2_subslots)}")
        
        for i, sub in enumerate(m2_subslots):
            print(f"\nサブスロット{i+1}:")
            print(f"  SubslotID: '{sub.get('SubslotID')}'")
            print(f"  SubslotElement: '{sub.get('SubslotElement')}'")
            print(f"  例文ID: {sub.get('例文ID')}")
            print(f"  display_order: {sub.get('display_order')}")
            
            # 予想されるHTML ID
            subslot_id = sub.get('SubslotID', '').lower()
            expected_html_id = f"slot-m2-sub-{subslot_id}"
            print(f"  予想HTML ID: '{expected_html_id}'")

if __name__ == "__main__":
    debug_m2_subslot_ids()
