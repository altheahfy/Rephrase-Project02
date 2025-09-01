#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テストデータの連番整理スクリプト
欠番を埋めて1から連番になるように修正
"""

import json
import os

def renumber_test_data():
    """テストデータを1から連番で整理"""
    
    # 元ファイル読み込み
    input_file = 'final_54_test_data_with_absolute_order_corrected.json'
    
    print(f"📖 {input_file} を読み込み中...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 既存のキーを取得してソート
    old_keys = sorted([int(k) for k in data['data'].keys()])
    print(f"📊 現在: {len(old_keys)}個のケース (範囲: {min(old_keys)}-{max(old_keys)})")
    
    # 欠番確認
    all_range = set(range(min(old_keys), max(old_keys) + 1))
    existing = set(old_keys)
    missing = sorted(all_range - existing)
    if missing:
        print(f"⚠️  欠番: {missing}")
    
    # 新しいデータ構造作成
    new_data = {
        'meta': data['meta'].copy(),
        'data': {}
    }
    
    # 連番で再割り当て
    new_number = 1
    old_to_new_mapping = {}
    
    for old_key in old_keys:
        old_str_key = str(old_key)
        new_str_key = str(new_number)
        
        # データをコピー
        new_data['data'][new_str_key] = data['data'][old_str_key].copy()
        
        # マッピング記録
        old_to_new_mapping[old_key] = new_number
        
        new_number += 1
    
    # メタデータ更新
    new_data['meta']['total_count'] = len(old_keys)
    new_data['meta']['valid_count'] = len(old_keys)
    new_data['meta']['total_reorganized'] = len(old_keys)
    new_data['meta']['renumbered'] = True
    new_data['meta']['note'] = f"連番整理済み（1-{len(old_keys)}）- 新文法ハンドラー開発準備完了"
    
    # バックアップ作成
    backup_file = input_file.replace('.json', '_backup.json')
    print(f"💾 バックアップ作成: {backup_file}")
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 新ファイル保存
    print(f"✨ 連番整理完了: 1-{len(old_keys)} ({len(old_keys)}ケース)")
    
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    # マッピング情報表示
    print("\n📋 番号変更マッピング (最初の10個):")
    for i, (old, new) in enumerate(old_to_new_mapping.items()):
        if i < 10:
            print(f"  {old} → {new}")
        elif i == 10:
            print("  ...")
            break
    
    print(f"\n🎉 完了! 新しい範囲: 1-{len(old_keys)}")
    return len(old_keys), old_to_new_mapping

if __name__ == "__main__":
    total_cases, mapping = renumber_test_data()
