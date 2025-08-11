"""
Excelファイル構造確認とex007データ検索
"""

import pandas as pd

def analyze_excel_structure():
    """Excelファイルの構造を詳細に分析"""
    
    try:
        # ファイル読み込み
        excel_file = pd.ExcelFile('例文入力元_分解結果_v2_20250810_113552.xlsx')
        print(f"=== Excelシート一覧 ===")
        for sheet_name in excel_file.sheet_names:
            print(f"- {sheet_name}")
        
        # 最初のシートを詳細分析
        df = pd.read_excel('例文入力元_分解結果_v2_20250810_113552.xlsx', sheet_name=0)
        print(f"\n=== 最初のシート構造 ===")
        print(f"行数: {len(df)}")
        print(f"列数: {len(df.columns)}")
        
        print("\n=== 列名一覧 ===")
        for i, col in enumerate(df.columns):
            print(f"{i:3d}: {col}")
        
        print("\n=== 最初の10行のデータサンプル ===")
        # 文章や例文を含む可能性のある列を探す
        for idx in range(min(10, len(df))):
            row = df.iloc[idx]
            print(f"\n行{idx+1}:")
            for col in df.columns:
                value = row[col]
                if pd.notna(value) and str(value).strip():
                    # 長い値は省略して表示
                    val_str = str(value).strip()
                    if len(val_str) > 30:
                        val_str = val_str[:30] + "..."
                    print(f"  {col}: {val_str}")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    analyze_excel_structure()
