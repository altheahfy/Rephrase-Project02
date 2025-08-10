#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Order整合性チェック - 原文とSlotPhrase再構築の比較
"""

import pandas as pd

def check_order_integrity():
    """原文とOrder順SlotPhrase再構築の整合性をチェック"""
    
    df = pd.read_excel('例文入力元_分解結果_v2_20250810_113552.xlsx')
    print('=== Order整合性チェック ===')
    
    # V_group_keyごとにグループ化
    v_groups = df.groupby('V_group_key')
    issues = []
    
    for v_key, group in v_groups:
        if pd.isna(group['原文'].iloc[0]):  # 原文がNaNならスキップ
            continue
            
        original = group['原文'].iloc[0]
        
        # Order順にソートして文を再構築
        sorted_group = group.sort_values('Slot_display_order')
        reconstructed_parts = []
        
        for _, row in sorted_group.iterrows():
            if pd.notna(row['SlotPhrase']):
                reconstructed_parts.append(str(row['SlotPhrase']))
        
        reconstructed = ' '.join(reconstructed_parts)
        
        # 比較（大文字小文字、句読点を正規化）
        orig_normalized = original.replace('.', '').replace(',', '').replace('?', '').replace('!', '').lower().strip()
        recon_normalized = reconstructed.replace('.', '').replace(',', '').replace('?', '').replace('!', '').lower().strip()
        
        if orig_normalized != recon_normalized:
            issues.append({
                'v_key': v_key,
                'original': original,
                'reconstructed': reconstructed,
                'orig_norm': orig_normalized,
                'recon_norm': recon_normalized
            })
    
    print(f'検証したV_group数: {len(v_groups)}')
    print(f'Order不整合: {len(issues)}件')
    
    for i, issue in enumerate(issues[:5]):  # 最初の5件を表示
        print(f'\n【不整合 {i+1}】')
        print(f'V_group: {issue["v_key"]}')
        print(f'原文: {issue["original"]}')  
        print(f'再構築: {issue["reconstructed"]}')
        print(f'正規化原文: {issue["orig_norm"]}')
        print(f'正規化再構築: {issue["recon_norm"]}')
    
    return issues

if __name__ == "__main__":
    issues = check_order_integrity()
