#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def process_fullset_with_step18():
    """5文型フルセットを直接Step18で処理する簡単な方法"""
    
    print("🎯 5文型フルセット vs Step18完全版 直接比較開始")
    print("=" * 80)
    
    # まず5文型フルセットの構造を確認
    try:
        df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
        
        # 例文ID別に原文を取得
        sentences = {}
        for _, row in df.iterrows():
            if pd.notna(row['例文ID']) and pd.notna(row['原文']):
                if row['例文ID'] not in sentences:
                    sentences[row['例文ID']] = row['原文']
        
        print(f"📂 5文型フルセットから{len(sentences)}個の例文を読み込み")
        
        # 複雑な例文（サブスロット分解があるもの）を特定
        complex_examples = df[df['SubslotID'].notna()]['例文ID'].unique()
        print(f"📋 サブスロット分解を持つ複雑な例文: {len(complex_examples)}個")
        print(f"例文ID: {list(complex_examples)}")
        
        # 最初の複雑な例文を詳しく確認
        if len(complex_examples) > 0:
            first_complex = complex_examples[0]
            print(f"\n🔍 {first_complex}の詳細分析:")
            print("-" * 50)
            
            # 原文
            original_text = sentences.get(first_complex, "不明")
            print(f"原文: {original_text}")
            
            # 正解データ（サブスロット分解）
            correct_data = df[(df['例文ID'] == first_complex) & (df['SubslotID'].notna())]
            print(f"\n📋 正解サブスロット構造:")
            
            for slot in correct_data['Slot'].unique():
                slot_data = correct_data[correct_data['Slot'] == slot]
                print(f"\n  【{slot}スロット】")
                for _, row in slot_data.iterrows():
                    print(f"    {row['SubslotID']:10}: \"{row['SubslotElement']}\"")
                    
        return sentences, df
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None, None

def show_step18_manual_test():
    """Step18システムの手動テスト用設定を表示"""
    
    print("\n" + "=" * 80)
    print("🎯 Step18システム手動テスト推奨手順")
    print("=" * 80)
    
    print("""
1. step18_unified_rephrase_system.py のテスト文を以下に変更:
   
   ex007: "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
   
2. python step18_unified_rephrase_system.py を実行
   
3. 出力結果と正解データを手動比較

【ex007正解サブスロット】:
  Sスロット:
    sub-s     : "the manager who"
    sub-aux   : "had"  
    sub-m2    : "recently"
    sub-v     : "taken"
    sub-o1    : "charge of the project"
    
  C2スロット:
    sub-v     : "deliver"
    sub-o1    : "the final proposal"  
    sub-m3    : "flawlessly"
    
  M2スロット:
    sub-m1    : "even though"
    sub-s     : "he"
    sub-v     : "was"
    sub-m2    : "under intense pressure"
    
  M3スロット:
    sub-m1    : "so"
    sub-s     : "the outcome"
    sub-aux   : "would"
    sub-v     : "reflect"
    sub-o1    : "the full potential"
""")

if __name__ == "__main__":
    sentences, df = process_fullset_with_step18()
    show_step18_manual_test()
