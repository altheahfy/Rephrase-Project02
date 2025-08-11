#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 既存のStep18統一システムを5文型フルセット全例文処理用に修正

import pandas as pd
import sys
import os

# Step18システムをインポートするため、同じディレクトリからインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 一時的にStep18システムのクラスをコピーして修正版を作成
exec(open('step18_unified_rephrase_system.py').read().replace(
    'if __name__ == "__main__":', 
    'if False:  # メイン実行を無効化'
))

class Step18FullsetProcessor:
    """5文型フルセット全例文をStep18完全版で処理"""
    
    def __init__(self):
        print("🎯 Step18完全版 - 5文型フルセット処理システム初期化...")
        self.system = Step18UnifiedRephraseSystem()
        print("✅ Step18統一システム初期化完了")

    def load_fullset_sentences(self):
        """5文型フルセットから全例文を読み込み"""
        try:
            df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
            
            # 例文ID別に原文を取得
            sentences = {}
            for _, row in df.iterrows():
                if pd.notna(row['例文ID']) and pd.notna(row['原文']):
                    if row['例文ID'] not in sentences:
                        sentences[row['例文ID']] = row['原文']
            
            print(f"📂 5文型フルセットから{len(sentences)}個の例文を読み込み")
            return df, sentences
            
        except Exception as e:
            print(f"❌ ファイル読み込みエラー: {e}")
            return None, None

    def process_all_sentences(self):
        """全例文をStep18完全版で処理"""
        print("\n🎯 5文型フルセット全例文処理開始")
        print("=" * 80)
        
        # データ読み込み
        correct_df, sentences = self.load_fullset_sentences()
        if not sentences:
            return
        
        all_results = []
        
        # 各例文を処理
        for i, (ex_id, sentence) in enumerate(sentences.items(), 1):
            print(f"\n📋 [{i}/{len(sentences)}] 処理中: {ex_id}")
            print(f"原文: {sentence}")
            print("-" * 60)
            
            try:
                # Step18完全版で処理
                results = self.system.process_sentence(sentence)
                
                # 結果を一覧表示
                print("🔍 Step18処理結果:")
                for slot_name, slot_data in results.items():
                    if slot_data:  # データが存在する場合のみ表示
                        print(f"  {slot_name}スロット:")
                        if isinstance(slot_data, dict):
                            for key, value in slot_data.items():
                                if value:
                                    print(f"    {key:10}: \"{value}\"")
                
                # 結果を蓄積
                for slot_name, slot_data in results.items():
                    if isinstance(slot_data, dict):
                        for subslot_id, element in slot_data.items():
                            if element:
                                all_results.append({
                                    '例文ID': ex_id,
                                    'Slot': slot_name,
                                    'SubslotID': subslot_id,
                                    'SubslotElement': element,
                                    '原文': sentence
                                })
                    else:
                        # 単一要素スロット(V, Aux)の場合
                        all_results.append({
                            '例文ID': ex_id,
                            'Slot': slot_name,
                            'SubslotID': '',
                            'SubslotElement': str(slot_data),
                            '原文': sentence
                        })
                        
            except Exception as e:
                print(f"❌ {ex_id} 処理エラー: {e}")
                continue
        
        # 結果をDataFrameに変換
        result_df = pd.DataFrame(all_results)
        
        print(f"\n✅ 全処理完了: {len(all_results)}行の結果生成")
        
        # 正解データと比較
        self.compare_with_correct_data(result_df, correct_df)
        
        return result_df

    def compare_with_correct_data(self, result_df, correct_df):
        """正解データとの詳細比較"""
        print("\n" + "=" * 80)
        print("🔍 正解データとの詳細比較")
        print("=" * 80)
        
        # サブスロット分解がある正解データのみ抽出
        correct_subslots = correct_df[correct_df['SubslotID'].notna()]
        
        print(f"📊 比較統計:")
        print(f"  正解サブスロット行数: {len(correct_subslots)}")
        print(f"  Step18結果行数: {len(result_df)}")
        print(f"  正解例文数: {len(correct_subslots['例文ID'].unique())}")
        print(f"  Step18処理例文数: {len(result_df['例文ID'].unique())}")
        
        # 例文別詳細比較（最初の3例文）
        for ex_id in correct_subslots['例文ID'].unique()[:3]:
            print(f"\n" + "=" * 60)
            print(f"📋 {ex_id} 詳細比較:")
            print("=" * 60)
            
            # 該当データ抽出
            correct_ex = correct_subslots[correct_subslots['例文ID'] == ex_id]
            result_ex = result_df[result_df['例文ID'] == ex_id]
            
            # 原文表示
            if len(correct_ex) > 0:
                original = correct_ex['原文'].iloc[0] if '原文' in correct_ex.columns else "原文不明"
                print(f"原文: {original}")
                print()
            
            # スロット別比較
            all_slots = set(correct_ex['Slot'].unique()) | set(result_ex['Slot'].unique())
            
            for slot in sorted(all_slots):
                correct_slot = correct_ex[correct_ex['Slot'] == slot]
                result_slot = result_ex[result_ex['Slot'] == slot]
                
                if len(correct_slot) > 0 or len(result_slot) > 0:
                    print(f"【{slot}スロット】")
                    
                    # 正解データ
                    print("  正解:")
                    if len(correct_slot) > 0:
                        for _, row in correct_slot.iterrows():
                            print(f"    {row['SubslotID']:10}: \"{row['SubslotElement']}\"")
                    else:
                        print("    (データなし)")
                    
                    # Step18結果
                    print("  Step18:")
                    if len(result_slot) > 0:
                        for _, row in result_slot.iterrows():
                            print(f"    {row['SubslotID']:10}: \"{row['SubslotElement']}\"")
                    else:
                        print("    (データなし)")
                    
                    print()

if __name__ == "__main__":
    processor = Step18FullsetProcessor()
    results = processor.process_all_sentences()
