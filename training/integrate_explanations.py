#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解説CSVファイルをJSONファイルに統合するスクリプト
"""

import json
import csv
import os
from pathlib import Path

def load_csv_explanations(csv_file_path):
    """CSVファイルから解説データを読み込む"""
    explanations = {}
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                v_group_key = row['V_group_key'].strip()
                explanation_title = row['explanation_title'].strip()
                explanation_content = row['explanation_content'].strip()
                
                explanations[v_group_key] = {
                    'explanation_title': explanation_title,
                    'explanation_content': explanation_content
                }
                
        print(f"✅ CSVから {len(explanations)} 件の解説データを読み込みました")
        return explanations
        
    except Exception as e:
        print(f"❌ CSVファイル読み込みエラー: {e}")
        return {}

def load_json_data(json_file_path):
    """既存のJSONファイルを読み込む"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"✅ JSONファイルから {len(data)} 件のデータを読み込みました")
        return data
    except Exception as e:
        print(f"❌ JSONファイル読み込みエラー: {e}")
        return []

def add_explanation_entries(json_data, explanations):
    """JSONデータに解説エントリを追加"""
    added_count = 0
    
    for v_group_key, explanation in explanations.items():
        # 解説エントリを作成
        explanation_entry = {
            "V_group_key": v_group_key,
            "Slot": "EXPLANATION",
            "SlotPhrase": "",
            "SlotText": "",
            "SlotAuxtext": "",
            "SubslotID": "",
            "ImagePath": "",
            "explanation_title": explanation['explanation_title'],
            "explanation_content": explanation['explanation_content']
        }
        
        # JSONデータに追加
        json_data.append(explanation_entry)
        added_count += 1
        print(f"📝 解説エントリ追加: {v_group_key}")
    
    print(f"✅ 合計 {added_count} 件の解説エントリを追加しました")
    return json_data

def save_json_data(json_data, json_file_path):
    """JSONデータをファイルに保存"""
    try:
        # バックアップファイルを作成
        backup_path = str(json_file_path).replace('.json', '_backup.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"📋 バックアップファイル作成: {backup_path}")
        
        # 新しいJSONファイルを保存
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)
        
        print(f"✅ JSONファイル保存完了: {json_file_path}")
        print(f"📊 総データ件数: {len(json_data)}")
        
    except Exception as e:
        print(f"❌ JSONファイル保存エラー: {e}")

def main():
    """メイン処理"""
    print("🚀 解説データ統合スクリプト開始")
    
    # ファイルパス設定
    current_dir = Path(__file__).parent
    csv_file = current_dir / "解説入力フォーマット.csv"
    json_file = current_dir / "data" / "V自動詞第1文型.json"
    
    # ファイル存在確認
    if not csv_file.exists():
        print(f"❌ CSVファイルが見つかりません: {csv_file}")
        return
    
    if not json_file.exists():
        print(f"❌ JSONファイルが見つかりません: {json_file}")
        return
    
    # 処理実行
    explanations = load_csv_explanations(csv_file)
    if not explanations:
        print("❌ 解説データの読み込みに失敗しました")
        return
    
    json_data = load_json_data(json_file)
    if not json_data:
        print("❌ JSONデータの読み込みに失敗しました")
        return
    
    # 解説エントリ追加
    updated_json_data = add_explanation_entries(json_data, explanations)
    
    # ファイル保存
    save_json_data(updated_json_data, json_file)
    
    print("🎉 解説データ統合完了！")

if __name__ == "__main__":
    main()
