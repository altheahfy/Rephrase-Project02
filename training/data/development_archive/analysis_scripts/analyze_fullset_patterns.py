import pandas as pd
from collections import defaultdict

df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

print('🔍 5文型フルセット完全解析：実装すべきパターンリストアップ')
print('=' * 100)

# 全例文IDを取得
example_ids = [eid for eid in df['例文ID'].unique() if pd.notna(eid)]
print(f'📊 総例文数: {len(example_ids)}')
print(f'例文ID一覧: {example_ids}')

# スロット別サブスロット使用パターン分析
slot_patterns = defaultdict(lambda: defaultdict(list))

print('\n🎯 各スロットのサブスロット使用パターン詳細分析')
print('=' * 100)

for slot_name in ['M1', 'S', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3']:
    print(f'\n📋 【{slot_name}スロット】の全パターン:')
    print('-' * 60)
    
    slot_examples = {}
    
    for example_id in example_ids:
        example_data = df[df['例文ID'] == example_id]
        slot_data = example_data[example_data['Slot'] == slot_name]
        
        if len(slot_data) == 0:
            continue
            
        # スロット原句
        slot_phrase = slot_data[slot_data['SubslotID'].isna()]['SlotPhrase'].iloc[0] if len(slot_data[slot_data['SubslotID'].isna()]) > 0 else ''
        
        # サブスロット
        subslots = slot_data[slot_data['SubslotID'].notna()]
        
        if len(subslots) > 0:
            # サブスロット分解あり
            subslot_pattern = []
            subslot_details = {}
            
            for _, row in subslots.iterrows():
                subslot_id = row['SubslotID']
                element = str(row['SubslotElement']) if pd.notna(row['SubslotElement']) else ''
                subslot_pattern.append(subslot_id)
                subslot_details[subslot_id] = element
            
            pattern_key = ' + '.join(sorted(subslot_pattern))
            slot_examples[example_id] = {
                'type': 'subslot',
                'phrase': slot_phrase,
                'pattern': pattern_key,
                'details': subslot_details
            }
        else:
            # 単一要素
            slot_examples[example_id] = {
                'type': 'single',
                'phrase': slot_phrase,
                'pattern': 'SINGLE',
                'details': {}
            }
    
    # パターン別に分類して表示
    pattern_groups = defaultdict(list)
    for eid, info in slot_examples.items():
        pattern_groups[info['pattern']].append((eid, info))
    
    for pattern, examples in pattern_groups.items():
        print(f'  🔸 パターン「{pattern}」({len(examples)}例):')
        for eid, info in examples[:3]:  # 最初の3例のみ表示
            print(f'    {eid}: "{info["phrase"]}"')
            if info['type'] == 'subslot':
                for sub_id, sub_element in info['details'].items():
                    print(f'      {sub_id}: "{sub_element}"')
        if len(examples) > 3:
            print(f'    ... 他{len(examples)-3}例')
        print()

print('\n🔧 実装優先度分析')
print('=' * 100)

# 各スロットで最も頻出のパターンを特定
priority_patterns = {}

for slot_name in ['M1', 'S', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3']:
    slot_pattern_freq = defaultdict(int)
    
    for example_id in example_ids:
        example_data = df[df['例文ID'] == example_id]
        slot_data = example_data[example_data['Slot'] == slot_name]
        
        if len(slot_data) == 0:
            continue
            
        subslots = slot_data[slot_data['SubslotID'].notna()]
        
        if len(subslots) > 0:
            subslot_pattern = ' + '.join(sorted(subslots['SubslotID'].tolist()))
            slot_pattern_freq[subslot_pattern] += 1
        else:
            slot_pattern_freq['SINGLE'] += 1
    
    if slot_pattern_freq:
        most_common = max(slot_pattern_freq.items(), key=lambda x: x[1])
        priority_patterns[slot_name] = {
            'pattern': most_common[0],
            'frequency': most_common[1],
            'total': sum(slot_pattern_freq.values()),
            'all_patterns': dict(slot_pattern_freq)
        }

print('📈 各スロットの実装優先パターン:')
for slot_name, info in priority_patterns.items():
    print(f'  {slot_name}: 「{info["pattern"]}」 ({info["frequency"]}/{info["total"]}例)')
    if len(info['all_patterns']) > 1:
        other_patterns = [(p, f) for p, f in info['all_patterns'].items() if p != info['pattern']]
        print(f'    その他: {other_patterns}')
