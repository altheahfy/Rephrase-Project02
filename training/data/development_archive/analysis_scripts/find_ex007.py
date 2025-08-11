"""
正解データの特定 - ex007を検索
"""

import pandas as pd

def find_ex007():
    """ex007を特定して正解データを表示"""
    
    try:
        excel_file = "例文入力元_分解結果_v2_20250810_113552.xlsx"
        df = pd.read_excel(excel_file)
        
        print("📋 ex007の正解データを検索中...")
        
        # ex007の行を検索
        ex007_rows = df[df['例文ID'] == 'ex007']
        
        if len(ex007_rows) == 0:
            print("❌ ex007が見つかりません")
            # 代替検索
            print("\n🔍 利用可能な例文IDを確認:")
            unique_ids = df['例文ID'].unique()[:20]  # 最初の20個
            for ex_id in unique_ids:
                if pd.notna(ex_id):
                    print(f"  - {ex_id}")
            return
            
        print(f"✅ ex007発見: {len(ex007_rows)}行")
        
        # 原文を取得
        original_sentence = ex007_rows['原文'].iloc[0] if '原文' in ex007_rows.columns else "不明"
        print(f"\n📝 原文: \"{original_sentence}\"")
        
        print(f"\n🎯 ex007の全スロット分解:")
        
        # スロット順に並べて表示
        sorted_rows = ex007_rows.sort_values('display_order') if 'display_order' in ex007_rows.columns else ex007_rows
        
        for idx, row in sorted_rows.iterrows():
            slot = row['Slot']
            slot_phrase = row['SlotPhrase'] 
            phrase_type = row['PhraseType']
            display_order = row.get('display_order', 'N/A')
            
            print(f"  {slot:<3}: \"{slot_phrase}\" ({phrase_type}) [order:{display_order}]")
            
        # 統計情報
        slots_count = ex007_rows['Slot'].value_counts()
        print(f"\n📊 スロット統計:")
        for slot, count in slots_count.items():
            print(f"  {slot}: {count}個")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    find_ex007()
