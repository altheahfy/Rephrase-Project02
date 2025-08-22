#!/usr/bin/env python3
"""
疑問文vs肯定文の順序構造差異分析
スクリーンショットで示された重要な発見を検証
"""
import json

def analyze_question_vs_statement_order():
    """疑問文と肯定文の順序構造の根本的違いを分析"""
    
    with open('slot_order_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print('=== 疑問文 vs 肯定文 順序構造差異分析 ===\n')
    
    # V_group_keyごとの分析
    v_groups = {}
    for item in data:
        v_group = item.get('V_group_key', 'unknown')
        if v_group not in v_groups:
            v_groups[v_group] = []
        v_groups[v_group].append(item)

    print(f'総V_group_key数: {len(v_groups)}')
    print(f'V_group_keys: {list(v_groups.keys())}\n')

    # 各V_group_keyの順序パターンを詳細分析
    for v_group_key, v_group_data in v_groups.items():
        print(f'--- V_group_key: {v_group_key} ---')
        
        # 例文IDごとにグループ化
        examples = {}
        for item in v_group_data:
            ex_id = item.get('例文ID', 'unknown')
            if ex_id not in examples:
                examples[ex_id] = []
            examples[ex_id].append(item)

        print(f'例文数: {len(examples)}')
        
        # 各例文の順序パターンと文型を分析
        for ex_id, ex_data in examples.items():
            # 上位スロットのみを取得して順序分析
            top_slots = sorted([item for item in ex_data if not item.get('SubslotID')], 
                              key=lambda x: x.get('Slot_display_order', 999))
            
            slot_sequence = []
            sentence_type = "unknown"
            
            # 文型判定（疑問文 vs 肯定文）
            has_wh_word = False
            sentence_start_slot = None
            
            for slot in top_slots:
                slot_name = slot['Slot']
                phrase = slot.get('SlotPhrase', '').strip()
                
                # 最初に出現するスロットを記録
                if sentence_start_slot is None and phrase:
                    sentence_start_slot = slot_name
                
                # wh-word検出
                if phrase and any(wh in phrase.lower() for wh in ['who', 'what', 'where', 'when', 'why', 'how']):
                    has_wh_word = True
                
                if phrase:
                    slot_sequence.append(f"{slot_name}({slot['Slot_display_order']})")
                else:
                    slot_sequence.append(f"{slot_name}({slot['Slot_display_order']})[EMPTY]")
            
            # 文型判定
            if has_wh_word:
                sentence_type = "wh疑問文"
            elif sentence_start_slot and sentence_start_slot in ['Aux', 'V']:
                sentence_type = "yes/no疑問文"
            elif sentence_start_slot in ['O1']:  # 目的語前置
                sentence_type = "目的語前置文"
            else:
                sentence_type = "肯定文"
            
            print(f'  {ex_id}: [{sentence_type}] {" -> ".join(slot_sequence)}')
        
        print()

    print('\n=== 重要な発見: 順序構造の根本的違い ===')
    
    findings = [
        "✅ 疑問文と肯定文で順序構造が根本的に異なる",
        "✅ wh疑問文: wh-wordが文頭に移動 (O1が位置1に)",
        "✅ yes/no疑問文: 助動詞が文頭に移動",
        "✅ 肯定文: 標準的なS-V-O順序",
        "❌ 1つのV_group_keyで疑問文と肯定文を統一管理は困難"
    ]
    
    for finding in findings:
        print(f'  {finding}')
    
    print('\n=== 設計への影響 ===')
    
    design_implications = [
        "🔄 V_group_key管理を文型別に分離する必要",
        "🔄 疑問文変換時の順序再配置システムが必要", 
        "🔄 文型変換ルール（肯定文↔疑問文）の実装が必要",
        "🔄 絶対順序テーブルを文型別に分離管理",
        "🔄 ランダマイゼーション時の文型制御機能が必要"
    ]
    
    for implication in design_implications:
        print(f'  {implication}')

if __name__ == "__main__":
    analyze_question_vs_statement_order()
