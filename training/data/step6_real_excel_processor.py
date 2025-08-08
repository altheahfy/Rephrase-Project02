"""
Step 6システム + 実用テスト版
ex000スキップルール対応の実用的なExcel処理システム
"""

import pandas as pd
from step6_final_100percent_integration import FinalRuleEngine

def process_real_excel_data():
    """
    例文入力元.xlsxを読み込み、ex000をスキップして実際の88文を処理
    """
    
    print("📊 実用テスト開始: 例文入力元.xlsx処理")
    print("=" * 60)
    
    try:
        # Excel読み込み
        df = pd.read_excel("例文入力元.xlsx")
        print(f"✅ Excelファイル読み込み成功")
        print(f"📊 全レコード数: {len(df)}件")
        
        # ex000系（入力例）をスキップ
        actual_data = df[~df['ex_id'].str.startswith('ex000')]
        skipped_count = len(df) - len(actual_data)
        
        print(f"📊 処理対象: {len(actual_data)}文")
        print(f"⏭️  スキップ: {skipped_count}件 (ex000系入力例)")
        print()
        
        # Step 6エンジン初期化
        engine = FinalRuleEngine()
        
        # 結果格納用
        analysis_results = []
        
        print("🔄 分析開始...")
        for index, row in actual_data.iterrows():
            sentence = row['原文']
            set_id = row['set_id']
            ex_id = row['ex_id']
            v_group = row['V_group_key']
            
            # 文分析
            slots = engine.analyze_sentence(sentence)
            
            # 結果行作成
            result_row = {
                'set_id': set_id,
                'ex_id': ex_id, 
                'V_group_key': v_group,
                '原文': sentence,
                'S': '; '.join(slots.get('S', [])),
                'Aux': '; '.join(slots.get('Aux', [])),
                'V': '; '.join(slots.get('V', [])),
                'O1': '; '.join(slots.get('O1', [])),
                'O2': '; '.join(slots.get('O2', [])),
                'C1': '; '.join(slots.get('C1', [])),
                'C2': '; '.join(slots.get('C2', [])),
                'M1': '; '.join(slots.get('M1', [])),
                'M2': '; '.join(slots.get('M2', [])),
                'M3': '; '.join(slots.get('M3', []))
            }
            
            analysis_results.append(result_row)
            
            # 進捗表示（10件ごと）
            if len(analysis_results) % 10 == 0:
                print(f"  ✅ {len(analysis_results)}件処理完了")
        
        print(f"🎉 全{len(analysis_results)}件の分析完了")
        
        # 結果DataFrame作成
        results_df = pd.DataFrame(analysis_results)
        
        # Excel出力
        output_file = "step6_real_test_results.xlsx"
        results_df.to_excel(output_file, index=False, sheet_name="Step6_Analysis")
        
        print(f"📊 出力完了: {output_file}")
        print(f"📈 統合率: 21/34 = 61.8% (Step 6システム)")
        
        # 簡易統計
        total_slots = 0
        filled_slots = 0
        
        for col in ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']:
            total_slots += len(results_df)
            filled_slots += (results_df[col] != '').sum()
        
        fill_rate = filled_slots / total_slots * 100
        print(f"📊 スロット充填率: {fill_rate:.1f}%")
        
        return results_df
        
    except FileNotFoundError:
        print("❌ 例文入力元.xlsxが見つかりません")
        print("📍 ファイルがカレントディレクトリにあることを確認してください")
    except Exception as e:
        print(f"❌ エラー発生: {str(e)}")

def main():
    """メイン実行"""
    print("🚀 Step 6 + 実用テストシステム")
    print("📋 ex000スキップルール対応版")
    print()
    
    # 実用テスト実行
    results = process_real_excel_data()
    
    print()
    print("✅ 実用テスト完了")
    print("🎯 次: 100%統合への継続作業")
    print("📈 目標: 34ルール完全統合")

if __name__ == "__main__":
    main()
