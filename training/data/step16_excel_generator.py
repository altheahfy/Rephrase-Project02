#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step16ベース完全版Excel生成システム

10サブスロット完全対応 + 5文型フルセット構造出力
MaximalSubslotGeneratorを活用した最新Excel生成機能
"""

import pandas as pd
import json
import os
from datetime import datetime
from step16_maximal_subslot import MaximalSubslotGenerator

class Step16ExcelGenerator:
    """Step16ベース完全版Excel生成システム"""
    
    def __init__(self):
        """初期化"""
        print("🚀 Step16 Excel Generator 起動開始...")
        
        # Step16システム初期化
        self.subslot_generator = MaximalSubslotGenerator()
        
        # ID管理
        self.current_construction_id = 5001  # 5文型フルセットに合わせる
        self.current_example_id = 1
        
        # 結果データ保存用
        self.excel_rows = []
        
        # スロット表示順序定義（5文型フルセットと同じ順序）
        self.main_slot_order = {
            'M1': 1, 'S': 2, 'Aux': 3, 'V': 4, 'O1': 5, 
            'O2': 6, 'C1': 7, 'C2': 8, 'M2': 9, 'M3': 10
        }
        
        # サブスロット表示順序
        self.subslot_order = {
            'sub-s': 1, 'sub-aux': 2, 'sub-m2': 3, 'sub-v': 4, 
            'sub-o1': 5, 'sub-o2': 6, 'sub-c1': 7, 'sub-c2': 8,
            'sub-m1': 9, 'sub-m3': 10
        }
        
        print("✅ Step16 Excel Generator 初期化完了")
        
    def analyze_and_generate_excel(self, sentences, v_group_key_base="analyze", output_filename=None):
        """文リストを解析してExcel形式で出力"""
        print(f"\n🎯 Excel生成開始: {len(sentences)}文を処理")
        
        for sentence in sentences:
            if not sentence or not sentence.strip():
                continue
                
            sentence = sentence.strip()
            print(f"\n📝 解析中: {sentence}")
            
            # Step16で全スロット解析
            all_slot_results = self._analyze_all_slots(sentence)
            
            # V_group_key生成
            v_group_key = self._extract_main_verb(all_slot_results) or f"{v_group_key_base}_{self.current_example_id}"
            
            # Excel行データ生成
            excel_rows = self._convert_to_excel_format(sentence, all_slot_results, v_group_key)
            self.excel_rows.extend(excel_rows)
            
            self.current_example_id += 1
        
        # Excel出力
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"step16_excel_output_{timestamp}.xlsx"
        
        self._save_to_excel(output_filename)
        return output_filename
    
    def _analyze_all_slots(self, sentence):
        """Step16で全スロットを解析"""
        all_results = {}
        
        # 各上位スロットでStep16解析実行
        for slot_name in self.subslot_generator.target_slots:
            subslots = self.subslot_generator.generate_maximal_subslots(slot_name, sentence)
            if subslots:
                all_results[slot_name] = subslots
        
        return all_results
    
    def _extract_main_verb(self, all_slot_results):
        """メイン動詞をV_group_keyとして抽出"""
        # 各スロット結果から動詞を探す
        for slot_name, subslots in all_slot_results.items():
            if 'sub-v' in subslots:
                verb = subslots['sub-v']['text']
                # 基本形に変換（簡易版）
                return self._get_verb_base_form(verb)
        return None
    
    def _get_verb_base_form(self, verb):
        """動詞の基本形取得（簡易版）"""
        # spaCyを使った正確な基本形取得
        if self.subslot_generator.nlp:
            doc = self.subslot_generator.nlp(verb)
            for token in doc:
                if token.pos_ == "VERB":
                    return token.lemma_
        return verb.lower()
    
    def _convert_to_excel_format(self, sentence, all_slot_results, v_group_key):
        """Step16解析結果を5文型フルセット形式のExcel行に変換"""
        excel_rows = []
        example_id = f"ex{self.current_example_id:03d}"
        
        # 各上位スロットを処理
        for slot_name in self.main_slot_order.keys():
            if slot_name in all_slot_results:
                subslots = all_slot_results[slot_name]
                slot_display_order = self.main_slot_order[slot_name]
                
                # 上位スロットの統合フレーズを生成
                main_phrase = self._generate_main_slot_phrase(subslots)
                phrase_type = self._determine_phrase_type(main_phrase)
                
                # 上位スロット行を追加
                excel_rows.append({
                    '構文ID': self.current_construction_id,
                    '例文ID': example_id,
                    'V_group_key': v_group_key,
                    '原文': sentence,
                    'Slot': slot_name,
                    'SlotPhrase': main_phrase,
                    'PhraseType': phrase_type,
                    'SubslotID': None,
                    'SubslotElement': None,
                    'Slot_display_order': slot_display_order,
                    'display_order': 0
                })
                
                # サブスロット行を追加
                subslot_rows = self._generate_subslot_rows(
                    sentence, slot_name, subslots, example_id, 
                    v_group_key, slot_display_order
                )
                excel_rows.extend(subslot_rows)
        
        self.current_construction_id += 1
        return excel_rows
    
    def _generate_main_slot_phrase(self, subslots):
        """サブスロットから上位スロットの統合フレーズを生成"""
        # サブスロットを順序でソートして結合
        sorted_subslots = sorted(
            subslots.items(), 
            key=lambda x: self.subslot_order.get(x[0], 999)
        )
        
        phrase_parts = []
        for subslot_name, subslot_data in sorted_subslots:
            if subslot_data and subslot_data.get('text'):
                phrase_parts.append(subslot_data['text'])
        
        return ' '.join(phrase_parts)
    
    def _determine_phrase_type(self, phrase):
        """フレーズタイプ判定（word/clause）"""
        if not phrase:
            return 'word'
        
        # 簡易判定: 複数単語かつ動詞を含む場合はclause
        words = phrase.split()
        if len(words) > 2:
            # spaCyで動詞チェック
            if self.subslot_generator.nlp:
                doc = self.subslot_generator.nlp(phrase)
                for token in doc:
                    if token.pos_ in ["VERB", "AUX"]:
                        return 'clause'
        
        return 'word'
    
    def _generate_subslot_rows(self, sentence, main_slot, subslots, example_id, v_group_key, slot_display_order):
        """サブスロット行データ生成"""
        rows = []
        
        # 表示順序でソート（原文の語順）
        sorted_subslots = sorted(
            subslots.items(),
            key=lambda x: x[1].get('display_order', 999) if x[1] else 999
        )
        
        for subslot_id, subslot_data in sorted_subslots:
            if subslot_data and subslot_data.get('text'):
                display_order = subslot_data.get('display_order', 999)
                rows.append({
                    '構文ID': self.current_construction_id,
                    '例文ID': example_id,
                    'V_group_key': v_group_key,
                    '原文': None,  # サブスロット行では空
                    'Slot': main_slot,
                    'SlotPhrase': None,  # サブスロット行では空
                    'PhraseType': None,  # サブスロット行では空
                    'SubslotID': subslot_id,
                    'SubslotElement': subslot_data['text'],
                    'Slot_display_order': slot_display_order,
                    'display_order': display_order
                })
        
        return rows
    
    def _save_to_excel(self, output_filename):
        """Excel形式で保存"""
        if not self.excel_rows:
            print("❌ 保存するデータがありません")
            return
        
        try:
            # DataFrame作成
            df = pd.DataFrame(self.excel_rows)
            
            # カラム順序を5文型フルセットと同じにする
            column_order = [
                '構文ID', '例文ID', 'V_group_key', '原文', 'Slot', 
                'SlotPhrase', 'PhraseType', 'SubslotID', 'SubslotElement',
                'Slot_display_order', 'display_order'
            ]
            df = df[column_order]
            
            # Excel保存
            df.to_excel(output_filename, index=False, engine='openpyxl')
            
            print(f"✅ Excel保存完了: {output_filename}")
            print(f"📊 総行数: {len(df)}行")
            print(f"📝 例文数: {self.current_example_id - 1}文")
            print(f"🎯 構文ID範囲: {5001} - {self.current_construction_id - 1}")
            
            # 統計情報表示
            self._show_statistics(df)
            
        except Exception as e:
            print(f"❌ Excel保存エラー: {e}")
            raise
    
    def _show_statistics(self, df):
        """生成統計表示"""
        print(f"\n📊 生成統計:")
        print(f"   上位スロット行: {len(df[df['SubslotID'].isna()])}行")
        print(f"   サブスロット行: {len(df[df['SubslotID'].notna()])}行")
        
        # スロット別統計
        main_slots = df[df['SubslotID'].isna()]['Slot'].value_counts()
        print(f"   上位スロット別:")
        for slot, count in main_slots.items():
            print(f"     {slot}: {count}文")
        
        # V_group_key別統計
        v_groups = df['V_group_key'].value_counts()
        print(f"   V_group_key数: {len(v_groups)}個")

def test_step16_excel_generator():
    """Step16 Excel Generator のテスト"""
    print("🧪 Step16 Excel Generator テスト開始")
    print("=" * 60)
    
    generator = Step16ExcelGenerator()
    
    # テスト用例文（複雑な5文型構造）
    test_sentences = [
        "The intelligent student was studying English very hard in the library.",
        "I gave him a beautiful book yesterday.",
        "She made me extremely happy with her wonderful surprise.",
        "They were working diligently on the important project together.",
        "The teacher explained the difficult concept clearly to all students."
    ]
    
    print(f"📝 テスト例文: {len(test_sentences)}文")
    for i, sentence in enumerate(test_sentences, 1):
        print(f"   {i}. {sentence}")
    
    # Excel生成実行
    output_file = generator.analyze_and_generate_excel(
        test_sentences, 
        v_group_key_base="test",
        output_filename="step16_test_output.xlsx"
    )
    
    print(f"\n🎉 テスト完了!")
    print(f"📁 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    test_step16_excel_generator()
