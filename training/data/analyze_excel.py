import pandas as pd
import numpy as np

def analyze_excel_format():
    """例文入力元.xlsxの様式を分析"""
    
    # Excelファイル読み込み
    file_path = "（小文字化した最初の5文型フルセット）例文入力元.xlsx"
    
    try:
        # 全シートを読み込み
        excel_file = pd.ExcelFile(file_path)
        print(f"📊 シート一覧: {excel_file.sheet_names}")
        
        for sheet_name in excel_file.sheet_names:
            print(f"\n🔍 シート: {sheet_name}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            
            # 最初の5行を表示
            print("\n最初の5行:")
            print(df.head())
            
            # データ型確認
            print(f"\nデータ型:")
            for col in df.columns:
                print(f"  {col}: {df[col].dtype}")
            
            # 空白セル確認
            print(f"\n空白セル数:")
            for col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    print(f"  {col}: {null_count}")
                    
            print("="*50)
            
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    analyze_excel_format()
