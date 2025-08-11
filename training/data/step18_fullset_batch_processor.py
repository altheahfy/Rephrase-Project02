#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spacy
import pandas as pd
from collections import defaultdict

class Step18FullsetBatchProcessor:
    """5文型フルセット全例文の一括処理システム"""
    
    def __init__(self):
        print("🎯 Step18 5文型フルセット一括処理システム初期化...")
        self.nlp = spacy.load("en_core_web_sm")
        
        # 既存のStep18統一システムのマッピングをインポート
        self.dependency_mapping = {
            # 主語関連
            'nsubj': ['sub-s'],           # 主語
            'nsubjpass': ['sub-s'],       # 受動態主語
            'csubj': ['sub-s'],           # 節主語
            'csubjpass': ['sub-s'],       # 受動態節主語
            
            # 動詞関連  
            'aux': ['sub-aux'],           # 助動詞
            'auxpass': ['sub-aux'],       # 受動助動詞
            'cop': ['sub-v'],             # コピュラ動詞
            'ROOT': ['sub-v'],            # メイン動詞
            
            # 目的語関連
            'dobj': ['sub-o1'],           # 直接目的語
            'iobj': ['sub-o2'],           # 間接目的語
            'pobj': ['sub-o1'],           # 前置詞目的語
            
            # 補語関連
            'attr': ['sub-c1'],           # 属性補語
            'acomp': ['sub-c1'],          # 形容詞補語
            'xcomp': ['sub-c2'],          # 開放補語
            'ccomp': ['sub-c2'],          # 節補語
            
            # 修飾語関連
            'amod': ['sub-m2'],           # 形容詞修飾語
            'advmod': ['sub-m2'],         # 副詞修飾語
            'det': ['sub-m2'],            # 限定詞
            'prep': ['sub-m1'],           # 前置詞
            'mark': ['sub-m1'],           # 従属接続詞
            'cc': ['sub-m1'],             # 等位接続詞
            
            # 関係節関連
            'relcl': ['sub-v'],           # 関係節動詞（優先度高）
            'rcmod': ['sub-v'],           # 関係節修飾語
            
            # その他
            'compound': ['sub-m2'],       # 複合語
            'poss': ['sub-m2'],           # 所有格
            'nummod': ['sub-m2'],         # 数詞修飾語
            'npadvmod': ['sub-m3'],       # 名詞句副詞
            'pcomp': ['sub-c2'],          # 前置詞補語
            'agent': ['sub-m3'],          # 能格
        }
        
        print("✅ Step18システム初期化完了")

    def load_fullset_data(self):
        """5文型フルセットデータを読み込み"""
        print("📂 5文型フルセットデータ読み込み...")
        
        try:
            # 5文型フルセットExcelを読み込み
            df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
            
            # 例文ID別に原文を取得
            sentences = {}
            for _, row in df.iterrows():
                if pd.notna(row['例文ID']) and pd.notna(row['原文']):
                    sentences[row['例文ID']] = row['原文']
            
            print(f"✅ {len(sentences)}個の例文を読み込み完了")
            return df, sentences
            
        except Exception as e:
            print(f"❌ ファイル読み込みエラー: {e}")
            return None, None

    def process_sentence(self, sentence):
        """単一文をStep18方式で処理"""
        doc = self.nlp(sentence)
        
        # スロット抽出（簡略版）
        slots = defaultdict(dict)
        
        for token in doc:
            if token.dep_ in self.dependency_mapping:
                subslots = self.dependency_mapping[token.dep_]
                for subslot in subslots:
                    # 基本的なマッピング（実際のStep18より簡素化）
                    if 'sub-s' in subslot and token.pos_ in ['PRON', 'NOUN', 'PROPN']:
                        slots['S'][subslot] = token.text
                    elif 'sub-v' in subslot and token.pos_ in ['VERB', 'AUX']:
                        slots['S'][subslot] = token.text
                    elif 'sub-m' in subslot:
                        slots['S'][subslot] = token.text
                    elif 'sub-c' in subslot:
                        slots['S'][subslot] = token.text
                    elif 'sub-o' in subslot:
                        slots['S'][subslot] = token.text
        
        return dict(slots)

    def batch_process_all(self):
        """全例文を一括処理"""
        print("\n🎯 5文型フルセット全例文一括処理開始")
        print("=" * 80)
        
        # データ読み込み
        correct_df, sentences = self.load_fullset_data()
        if not sentences:
            return
        
        # 処理結果格納
        results = []
        
        # 各例文を処理
        for ex_id, sentence in sentences.items():
            print(f"\n📋 処理中: {ex_id}")
            print(f"原文: {sentence[:100]}..." if len(sentence) > 100 else f"原文: {sentence}")
            
            # Step18エンジンで処理
            slots = self.process_sentence(sentence)
            
            # 結果を格納
            for slot_name, subslots in slots.items():
                for subslot_id, element in subslots.items():
                    results.append({
                        '例文ID': ex_id,
                        'Slot': slot_name,
                        'SubslotID': subslot_id,
                        'SubslotElement': element,
                        '原文': sentence
                    })
        
        # 結果をDataFrameに変換
        result_df = pd.DataFrame(results)
        
        print(f"\n✅ 処理完了: {len(results)}行の結果を生成")
        
        # 正解データと比較
        self.compare_with_correct(result_df, correct_df)
        
        return result_df

    def compare_with_correct(self, result_df, correct_df):
        """正解データとの比較"""
        print("\n🔍 正解データとの比較開始")
        print("=" * 50)
        
        # サブスロット分解がある正解データのみ抽出
        correct_subslots = correct_df[correct_df['SubslotID'].notna()]
        
        print(f"📊 比較対象:")
        print(f"  正解サブスロット数: {len(correct_subslots)}")
        print(f"  Step18結果数: {len(result_df)}")
        
        # 例文ID別に比較
        for ex_id in correct_subslots['例文ID'].unique()[:3]:  # 最初の3例文のみ
            print(f"\n📋 {ex_id} 比較結果:")
            
            # 正解データ
            correct_ex = correct_subslots[correct_subslots['例文ID'] == ex_id]
            result_ex = result_df[result_df['例文ID'] == ex_id]
            
            print("  【正解】")
            for _, row in correct_ex.iterrows():
                print(f"    {row['Slot']} | {row['SubslotID']} | {row['SubslotElement']}")
            
            print("  【Step18結果】")
            for _, row in result_ex.iterrows():
                print(f"    {row['Slot']} | {row['SubslotID']} | {row['SubslotElement']}")

if __name__ == "__main__":
    processor = Step18FullsetBatchProcessor()
    results = processor.batch_process_all()
