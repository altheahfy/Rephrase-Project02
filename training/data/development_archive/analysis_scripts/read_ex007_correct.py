"""
5文型フルセットからex007の正解データを読み取り
"""

import pandas as pd

def read_ex007_correct_data():
    """ex007の正解データを5文型フルセットから読み取り"""
    
    try:
        # 5文型フルセットExcelファイル読み込み
        df = pd.read_excel('例文入力元_分解結果_v2_20250810_113552.xlsx')
        
        print("=== 5文型フルセット ex007 正解データ ===")
        print(f"総行数: {len(df)}")
        
        # ex007を検索
        if len(df) >= 7:
            ex007_row = df.iloc[6]  # 0-indexed なので6番目がex007
            
            print("\nex007 正解データ:")
            print(f"元文: {ex007_row.get('元文', 'N/A')}")
            
            # 各スロットのデータを表示
            slots = ['M1', 'S', 'Aux', 'V', 'O1', 'C1', 'C2', 'M2', 'M3']
            
            for slot in slots:
                slot_data = {}
                for col in df.columns:
                    if col.startswith(slot) and '_' in col:
                        subslot = col.split('_')[1] if '_' in col else col
                        value = ex007_row.get(col, '')
                        if pd.notna(value) and str(value).strip():
                            slot_data[subslot] = str(value).strip()
                
                if slot_data:
                    print(f"\n{slot}スロット:")
                    for key, value in slot_data.items():
                        print(f"  {key:<10}: \"{value}\"")
        else:
            print("❌ ex007のデータが見つかりません")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        print("ファイルが存在しない可能性があります")

if __name__ == "__main__":
    read_ex007_correct_data()
