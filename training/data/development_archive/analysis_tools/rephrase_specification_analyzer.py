"""
Rephrase 5文型フルセット分析スクリプト
5文型フルセットデータを体系的に分析し、正しいRephraseエンジンの仕様を抽出する
"""
import json
from collections import defaultdict, Counter

def analyze_slot_order_data(file_path):
    """slot_order_data.jsonを分析してRephraseの仕様を抽出"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== 5文型フルセット分析結果 ===\n")
    
    # 1. 全例文数を集計
    examples = set()
    for item in data:
        if item.get('例文ID'):
            examples.add(item['例文ID'])
    print(f"総例文数: {len(examples)}")
    
    # 2. clause構造の例文を抽出
    clause_examples = defaultdict(list)
    for item in data:
        if item.get('PhraseType') == 'clause':
            example_id = item['例文ID']
            slot = item['Slot']
            phrase = item['SlotPhrase']
            clause_examples[example_id].append({
                'slot': slot,
                'phrase': phrase,
                'item': item
            })
    
    print(f"複文構造を含む例文数: {len(clause_examples)}")
    
    # 3. 上位スロット空化パターンを分析
    upper_slot_patterns = {
        'empty_upper_with_subslots': [],  # 上位空+サブスロット有り
        'filled_upper_with_subslots': [], # 上位あり+サブスロット有り
        'only_upper_no_subslots': []      # 上位のみ、サブスロット無し
    }
    
    for example_id in clause_examples:
        # この例文の全データを取得
        example_data = [item for item in data if item['例文ID'] == example_id]
        
        # 各clauseスロットを分析
        for clause_info in clause_examples[example_id]:
            slot = clause_info['slot']
            upper_phrase = clause_info['phrase']
            
            # このスロットにサブスロットがあるか確認
            subslots = [item for item in example_data 
                       if item['Slot'] == slot and item.get('SubslotID')]
            
            if subslots:
                # サブスロットがある場合、上位が空かどうか確認
                # 上位スロットを再度検索（空の場合SlotPhraseが""になっている可能性）
                upper_slots_for_this = [item for item in example_data 
                                      if item['Slot'] == slot and not item.get('SubslotID')]
                
                # 実際の空かどうかは後続のemptyエントリを確認
                empty_upper_found = any(item for item in example_data 
                                      if item['Slot'] == slot and 
                                      not item.get('SubslotID') and
                                      item.get('SlotPhrase', '').strip() == '')
                
                if empty_upper_found or len(upper_slots_for_this) > 1:
                    upper_slot_patterns['empty_upper_with_subslots'].append({
                        'example_id': example_id,
                        'slot': slot,
                        'original_phrase': upper_phrase,
                        'subslot_count': len(subslots)
                    })
                else:
                    upper_slot_patterns['filled_upper_with_subslots'].append({
                        'example_id': example_id,
                        'slot': slot,
                        'original_phrase': upper_phrase,
                        'subslot_count': len(subslots)
                    })
            else:
                upper_slot_patterns['only_upper_no_subslots'].append({
                    'example_id': example_id,
                    'slot': slot,
                    'phrase': upper_phrase
                })
    
    # 4. 分析結果を出力
    print("\n=== 上位スロット動作パターン分析 ===")
    
    print(f"\n1. 上位空化+サブスロット分解パターン: {len(upper_slot_patterns['empty_upper_with_subslots'])}件")
    for item in upper_slot_patterns['empty_upper_with_subslots'][:5]:
        print(f"   例文{item['example_id']} {item['slot']}スロット: \"{item['original_phrase']}\" → {item['subslot_count']}個のサブスロット")
    
    print(f"\n2. 上位保持+サブスロット追加パターン: {len(upper_slot_patterns['filled_upper_with_subslots'])}件")
    for item in upper_slot_patterns['filled_upper_with_subslots'][:5]:
        print(f"   例文{item['example_id']} {item['slot']}スロット: \"{item['original_phrase']}\" + {item['subslot_count']}個のサブスロット")
    
    print(f"\n3. 上位のみパターン: {len(upper_slot_patterns['only_upper_no_subslots'])}件")
    
    # 5. サブスロットタイプ統計
    subslot_types = Counter()
    for item in data:
        if item.get('SubslotID'):
            subslot_types[item['SubslotID']] += 1
    
    print(f"\n=== サブスロットタイプ使用統計 ===")
    for subslot_type, count in subslot_types.most_common(10):
        print(f"{subslot_type}: {count}回")
    
    # 6. 具体的な例文パターンを詳細出力
    print(f"\n=== 詳細分析: 関係詞節 vs 従属節パターン ===")
    
    # 関係詞パターンを特定
    relative_patterns = []
    subordinate_patterns = []
    
    for example_id in clause_examples:
        example_data = [item for item in data if item['例文ID'] == example_id]
        
        for clause_info in clause_examples[example_id]:
            slot = clause_info['slot']
            phrase = clause_info['phrase']
            
            if 'who' in phrase or 'which' in phrase or 'that' in phrase:
                relative_patterns.append({
                    'example_id': example_id,
                    'slot': slot, 
                    'phrase': phrase,
                    'pattern_type': 'relative_clause'
                })
            elif 'because' in phrase or 'when' in phrase or 'if' in phrase:
                subordinate_patterns.append({
                    'example_id': example_id,
                    'slot': slot,
                    'phrase': phrase, 
                    'pattern_type': 'subordinate_clause'
                })
    
    print(f"関係詞節パターン: {len(relative_patterns)}件")
    for item in relative_patterns[:3]:
        print(f"   例文{item['example_id']} {item['slot']}: \"{item['phrase']}\"")
        
    print(f"従属節パターン: {len(subordinate_patterns)}件")  
    for item in subordinate_patterns[:3]:
        print(f"   例文{item['example_id']} {item['slot']}: \"{item['phrase']}\"")
    
    return {
        'upper_slot_patterns': upper_slot_patterns,
        'subslot_types': subslot_types,
        'relative_patterns': relative_patterns,
        'subordinate_patterns': subordinate_patterns
    }

if __name__ == "__main__":
    # ファイルパスを指定
    file_path = "training/data/slot_order_data.json"
    
    try:
        results = analyze_slot_order_data(file_path)
        print("\n=== 分析完了 ===")
        print("この結果を元に、正しいRephraseエンジンの仕様を確定します。")
        
    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません")
        print("このスクリプトをtraining/dataディレクトリで実行してください")
    except Exception as e:
        print(f"分析中にエラーが発生しました: {e}")
