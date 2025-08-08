import pandas as pd
import numpy as np

def detailed_analysis():
    """詳細分析"""
    
    file_path = "（小文字化した最初の5文型フルセット）例文入力元.xlsx"
    df = pd.read_excel(file_path)
    
    print("📋 入力様式の詳細分析")
    print("="*50)
    
    # 例文IDごとのグループ化
    examples = df['例文ID'].unique()
    print(f"例文数: {len(examples)}")
    
    # 最初の例文の構造を詳細に見る
    for i, ex_id in enumerate(examples[:3]):
        print(f"\n🔍 例文: {ex_id}")
        ex_data = df[df['例文ID'] == ex_id]
        
        # 原文（最初のレコードから取得）
        original = ex_data[ex_data['原文'].notna()]['原文'].iloc[0] if len(ex_data[ex_data['原文'].notna()]) > 0 else "N/A"
        print(f"原文: {original}")
        
        # 構造
        print(f"レコード数: {len(ex_data)}")
        
        # スロット構造
        print("スロット構造:")
        for _, row in ex_data.iterrows():
            slot = row['Slot']
            phrase = row['SlotPhrase']
            phrase_type = row['PhraseType']
            subslot_id = row['SubslotID']
            subslot_elem = row['SubslotElement']
            slot_order = row['Slot_display_order']
            display_order = row['display_order']
            
            if pd.notna(phrase):
                print(f"  {slot} ({slot_order}): '{phrase}' [{phrase_type}]")
            elif pd.notna(subslot_elem):
                print(f"    {subslot_id} ({slot_order}.{display_order}): '{subslot_elem}'")
            else:
                print(f"  {slot} ({slot_order}): [空]")
        
        print("-" * 30)
    
    # スロット種類の確認
    print(f"\n📊 スロット種類:")
    slots = df['Slot'].unique()
    for slot in sorted(slots):
        count = len(df[df['Slot'] == slot])
        print(f"  {slot}: {count}回")
    
    # PhraseTypeの確認
    print(f"\n📊 PhraseType種類:")
    phrase_types = df['PhraseType'].dropna().unique()
    for ptype in sorted(phrase_types):
        count = len(df[df['PhraseType'] == ptype])
        print(f"  {ptype}: {count}回")

if __name__ == "__main__":
    detailed_analysis()
