import pandas as pd
import sys
sys.path.append('.')
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

class DebugExcelGenerator:
    def __init__(self):
        self.engine = CompleteRephraseParsingEngine()
        self.results = []

    def analyze_and_add_sentence(self, sentence):
        """例文解析とデータ追加"""
        print(f"\n=== 解析開始: {sentence} ===")
        try:
            # 解析実行
            analysis_result = self.engine.analyze_sentence(sentence)
            print(f"✅ 解析成功: {type(analysis_result)}")
            return True
        except Exception as e:
            print(f"❌ 解析エラー: {e}")
            return False

    def test_excel_loading(self):
        """Excel読み込みテスト"""
        try:
            df = pd.read_excel('例文入力元.xlsx')
            print(f"Excel読み込み成功: {len(df)}行")
            
            # 例文カラム特定
            sentence_column = '原文'
            print(f"例文カラム: {sentence_column}")
            
            # 各行をテスト
            loaded_count = 0
            processed_sentences = set()
            
            for index, row in df.iterrows():
                sentence = str(row[sentence_column]).strip()
                
                if sentence and sentence != 'nan' and len(sentence) > 1:
                    if sentence not in processed_sentences:
                        print(f"\n--- 処理中（行{index+1}): '{sentence}' ---")
                        success = self.analyze_and_add_sentence(sentence)
                        if success:
                            processed_sentences.add(sentence)
                            loaded_count += 1
                        else:
                            print(f"❌ 解析失敗: {sentence}")
                            break
                        
                        # 最初の3文だけテスト
                        if loaded_count >= 3:
                            print("\n=== 最初の3文テスト完了 ===")
                            break
                            
            print(f"\n✅ テスト完了: {loaded_count}文を処理")
            
        except Exception as e:
            print(f"❌ Excel処理エラー: {e}")
            import traceback
            traceback.print_exc()

# テスト実行
if __name__ == "__main__":
    debug_gen = DebugExcelGenerator()
    debug_gen.test_excel_loading()
