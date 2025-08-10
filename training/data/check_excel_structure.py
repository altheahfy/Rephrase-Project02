#!/usr/bin/env python3
"""
Excel例文ファイルの構造確認スクリプト
"""

import pandas as pd
import os

# 対象ファイル
files = [
    '例文入力元_分解結果_v2.xlsx',
    '（小文字化した最初の5文型フルセット）例文入力元.xlsx', 
    '例文入力元.xlsx'
]

for filename in files:
    print(f"\n{'='*60}")
    print(f"📁 {filename}")
    print(f"{'='*60}")
    
    if not os.path.exists(filename):
        print(f"❌ ファイルが見つかりません: {filename}")
        continue
        
    try:
        # Excelファイルを読み込み
        excel_file = pd.ExcelFile(filename)
        print(f"📊 シート数: {len(excel_file.sheet_names)}")
        
        for i, sheet_name in enumerate(excel_file.sheet_names):
            print(f"\n📝 シート{i+1}: '{sheet_name}'")
            
            # 各シートの列名を表示
            df = pd.read_excel(filename, sheet_name=sheet_name)
            print(f"  行数: {len(df)}")
            print(f"  列名: {list(df.columns)}")
            
            # 最初の3行のサンプルデータを表示
            if len(df) > 0:
                print(f"\n  サンプルデータ（最初の3行）:")
                for idx, row in df.head(3).iterrows():
                    print(f"    行{idx+1}: {dict(row)}")
                    
                # 例文らしき列を探す
                sentence_columns = []
                for col in df.columns:
                    if any(keyword in str(col).lower() for keyword in ['例文', 'sentence', '文', 'text']):
                        sentence_columns.append(col)
                        
                if sentence_columns:
                    print(f"\n  🎯 例文候補列: {sentence_columns}")
                    for col in sentence_columns[:2]:  # 最初の2列のみ表示
                        print(f"    '{col}' サンプル:")
                        for idx, val in df[col].head(3).items():
                            if pd.notna(val):
                                print(f"      {idx}: {val}")
                else:
                    print(f"\n  ❓ 例文らしき列が見つかりません")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

print(f"\n{'='*60}")
print("✅ 構造確認完了")
