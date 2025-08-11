"""
正解データの正確な読み取り - ex007
"""

import pandas as pd

def read_correct_data():
    """正解データをExcelから読み取り"""
    
    try:
        # 正解データファイル
        excel_file = "例文入力元_分解結果_v2_20250810_113552.xlsx"
        df = pd.read_excel(excel_file)
        
        print("📋 Excelファイルから正解データを読み取り中...")
        print(f"ファイル: {excel_file}")
        print(f"行数: {len(df)}")
        
        # ex007を探す（行番号7または文章内容で特定）
        if len(df) > 7:
            ex007_row = df.iloc[6]  # 0-based indexなので6
            print(f"\n🎯 ex007の正解データ:")
            
            # 各列の内容を表示
            for col in df.columns:
                value = ex007_row[col]
                if pd.notna(value) and str(value).strip():
                    print(f"  {col:<15}: \"{value}\"")
        
        print(f"\n📋 全列名:")
        for col in df.columns:
            print(f"  - {col}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        print("代替ファイルを試します...")
        
        try:
            alt_file = "（小文字化した最初の5文型フルセット）例文入力元.xlsx"
            df = pd.read_excel(alt_file)
            print(f"\n代替ファイル: {alt_file}")
            print(f"行数: {len(df)}")
            
            if len(df) > 7:
                ex007_row = df.iloc[6]
                print(f"\n🎯 ex007の正解データ (代替):")
                
                for col in df.columns:
                    value = ex007_row[col]
                    if pd.notna(value) and str(value).strip():
                        print(f"  {col:<15}: \"{value}\"")
                        
        except Exception as e2:
            print(f"❌ 代替ファイルもエラー: {e2}")

if __name__ == "__main__":
    read_correct_data()
