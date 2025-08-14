# ===== 簡易版Excel Generator v3.0 =====
# 現在のシステムに対応したDB生成エンジン

import pandas as pd
import os
from datetime import datetime
from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

class SimpleExcelGeneratorV3:
    """簡易版Excel Generator（現在システム対応版）"""
    
    def __init__(self):
        self.integrator = SimpleUnifiedRephraseSlotIntegrator()
        self.decomposer = SubSlotDecomposer()
        self.results = []
        self.current_sentence_id = 1
        self.current_construction_id = 1000
        self.vgroup_data = {}
        
        print("🚀 簡易版Excel Generator v3.0 初期化完了")
    
    def analyze_and_add_sentence(self, sentence, v_group_key=None):
        """文を解析してデータに追加"""
        sentence = sentence.strip()
        if not sentence:
            return False
            
        try:
            print(f"🔍 解析中: {sentence}")
            
            # Step 1: 統合分解
            main_result = self.integrator.process(sentence)
            if not main_result or 'slots' not in main_result:
                print(f"❌ 統合分解失敗: {sentence}")
                return False
            
            main_slots = main_result['slots']
            
            # Step 2: サブスロット分解
            sub_slot_results = self.decomposer.decompose_complex_slots(main_slots)
            
            # V_group_key生成
            if not v_group_key:
                verb = self.extract_main_verb(main_slots)
                v_group_key = verb if verb else f"unknown_{self.current_sentence_id}"
            
            # データ蓄積
            if v_group_key not in self.vgroup_data:
                self.vgroup_data[v_group_key] = []
            
            sentence_data = {
                'sentence': sentence,
                'main_slots': main_slots,
                'sub_slot_results': sub_slot_results,
                'example_id': f"ex{self.current_sentence_id:03d}",
                'construction_id': self.current_construction_id
            }
            
            self.vgroup_data[v_group_key].append(sentence_data)
            
            print(f"✅ 解析完了: V_group_key='{v_group_key}'")
            self.current_sentence_id += 1
            self.current_construction_id += 1
            return True
            
        except Exception as e:
            print(f"❌ 解析エラー: {sentence} - {e}")
            return False
    
    def extract_main_verb(self, main_slots):
        """メイン動詞を抽出"""
        # V スロットから動詞を抽出
        if 'V' in main_slots and main_slots['V']:
            return main_slots['V']
        
        # Aux スロットから助動詞を抽出
        if 'Aux' in main_slots and main_slots['Aux']:
            return main_slots['Aux']
        
        return 'general'
    
    def generate_excel_data(self):
        """Excel データ生成"""
        print(f"📊 Excel データ生成開始")
        
        for v_group_key, sentences in self.vgroup_data.items():
            print(f"🔧 V_group_key: '{v_group_key}' 処理中 ({len(sentences)}文)")
            
            for sentence_data in sentences:
                self.convert_to_excel_rows(sentence_data, v_group_key)
        
        print(f"✅ Excel データ生成完了: {len(self.results)}行")
    
    def convert_to_excel_rows(self, sentence_data, v_group_key):
        """例文データをExcel行に変換"""
        sentence = sentence_data['sentence']
        main_slots = sentence_data['main_slots']
        sub_slot_results = sentence_data['sub_slot_results']
        example_id = sentence_data['example_id']
        construction_id = sentence_data['construction_id']
        
        row_count = 0
        
        # メインスロット処理
        for slot_name, slot_value in main_slots.items():
            if slot_value and slot_value.strip():
                phrase_type = self.determine_phrase_type(slot_value, sub_slot_results, slot_name)
                
                # メインスロット行
                main_row = {
                    '構文ID': construction_id,
                    '例文ID': example_id,
                    'V_group_key': v_group_key,
                    '原文': sentence if row_count == 0 else None,
                    'Slot': slot_name,
                    'SlotPhrase': slot_value,
                    'PhraseType': phrase_type,
                    'SubslotID': None,
                    'SubslotElement': None,
                    'Slot_display_order': self.get_slot_order(slot_name),
                    'display_order': 0,
                    'QuestionType': self.get_question_type(slot_value)
                }
                
                self.results.append(main_row)
                row_count += 1
                
                # サブスロット処理
                if slot_name in sub_slot_results:
                    for sub_result in sub_slot_results[slot_name]:
                        for sub_slot_id, sub_element in sub_result.sub_slots.items():
                            if sub_element and sub_element.strip():
                                sub_row = {
                                    '構文ID': construction_id,
                                    '例文ID': example_id,
                                    'V_group_key': v_group_key,
                                    '原文': None,
                                    'Slot': slot_name,
                                    'SlotPhrase': slot_value,
                                    'PhraseType': 'clause',
                                    'SubslotID': sub_slot_id,
                                    'SubslotElement': sub_element,
                                    'Slot_display_order': self.get_slot_order(slot_name),
                                    'display_order': 0,
                                    'QuestionType': None
                                }
                                
                                self.results.append(sub_row)
                                row_count += 1
    
    def determine_phrase_type(self, slot_value, sub_slot_results, slot_name):
        """PhraseTypeを判定"""
        word_count = len(slot_value.split())
        
        # サブスロットがある場合はclause
        if slot_name in sub_slot_results:
            for sub_result in sub_slot_results[slot_name]:
                if sub_result.sub_slots:
                    return 'clause'
        
        # 1単語はword
        if word_count == 1:
            return 'word'
        
        # 複数語はphrase
        return 'phrase'
    
    def get_slot_order(self, slot_name):
        """スロット順序を取得"""
        slot_order_map = {
            'M1': 1, 'S': 2, 'Aux': 3, 'M2': 4, 'V': 5,
            'C1': 6, 'O1': 7, 'O2': 8, 'C2': 9, 'M3': 10
        }
        return slot_order_map.get(slot_name, 99)
    
    def get_question_type(self, phrase):
        """QuestionTypeを判定"""
        wh_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which']
        phrase_lower = phrase.lower().strip()
        
        if phrase_lower in wh_words:
            return 'wh-word'
        return None
    
    def save_to_excel(self, output_filename):
        """Excel形式で保存"""
        if not self.results:
            print("❌ 保存するデータがありません")
            return
        
        # DataFrame変換
        df = pd.DataFrame(self.results)
        
        # 列順序調整
        column_order = [
            '構文ID', '例文ID', 'V_group_key', '原文', 'Slot', 'SlotPhrase', 
            'PhraseType', 'SubslotID', 'SubslotElement', 'Slot_display_order', 
            'display_order', 'QuestionType'
        ]
        
        for col in column_order:
            if col not in df.columns:
                df[col] = None
        
        df = df[column_order]
        
        # Excel保存
        try:
            df.to_excel(output_filename, index=False, engine='openpyxl')
            print(f"✅ Excel保存完了: {output_filename}")
            print(f"📊 総行数: {len(df)}行")
            print(f"📝 例文数: {self.current_sentence_id - 1}文")
            print(f"🔗 V_group数: {len(self.vgroup_data)}個")
        except Exception as e:
            print(f"❌ Excel保存エラー: {e}")

def test_simple_excel_generator():
    """簡単なテスト実行"""
    generator = SimpleExcelGeneratorV3()
    
    test_sentences = [
        "I run fast.",
        "She is beautiful.", 
        "He gave me a book.",
        "We made him happy.",
        "There are many students."
    ]
    
    for sentence in test_sentences:
        generator.analyze_and_add_sentence(sentence)
    
    generator.generate_excel_data()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"簡易テストDB_{timestamp}.xlsx"
    generator.save_to_excel(filename)

if __name__ == "__main__":
    test_simple_excel_generator()
