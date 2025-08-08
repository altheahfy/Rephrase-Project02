# ===== Rephrase Excel Generator v2.0 =====
# 動的Slot_display_order対応版

import pandas as pd
import os
from Rephrase_Parsing_Engine import RephraseParsingEngine

class ExcelGeneratorV2:
    """Rephrase解析結果をExcel形式で出力（動的絶対順序対応）"""
    
    def __init__(self):
        self.engine = RephraseParsingEngine()
        self.results = []
        self.current_sentence_id = 1
        self.current_construction_id = 1000
        
        # V_group_keyごとの例文データを保持
        self.vgroup_data = {}  # {v_group_key: [sentence_data, ...]}
    
    def analyze_and_add_sentence(self, sentence, v_group_key=None):
        """文を解析してV_group_keyデータに蓄積（Step 1）"""
        sentence = sentence.strip()
        if not sentence:
            return
            
        print(f"\n=== Step 1 解析中: {sentence} ===")
        
        # 品詞分解実行
        slots = self.engine.analyze_sentence(sentence)
        
        if not slots:
            print(f"❌ 解析失敗: {sentence}")
            return
            
        # V_group_key生成
        if not v_group_key:
            verb = self.extract_main_verb(slots)
            v_group_key = verb if verb else f"unknown_{self.current_sentence_id}"
            
        # V_group_keyデータに蓄積
        if v_group_key not in self.vgroup_data:
            self.vgroup_data[v_group_key] = []
            
        sentence_data = {
            'sentence': sentence,
            'slots': slots,
            'example_id': f"ex{self.current_sentence_id:03d}",
            'construction_id': self.current_construction_id
        }
        
        self.vgroup_data[v_group_key].append(sentence_data)
        
        print(f"✅ Step 1完了: V_group_key='{v_group_key}' に蓄積")
        for slot, candidates in slots.items():
            if candidates:
                candidate = candidates[0]
                print(f"  {slot}: {candidate['value']}")
        
        self.current_sentence_id += 1
        self.current_construction_id += 1
    
    def generate_excel_data(self):
        """V_group_keyデータからExcelデータを生成（Step 2）"""
        print(f"\n=== Step 2: Excel データ生成開始 ===")
        
        for v_group_key, sentences in self.vgroup_data.items():
            print(f"\n--- V_group_key: '{v_group_key}' 処理中 ---")
            
            # この V_group_key の絶対順序を計算
            slot_orders = self.calculate_slot_display_orders(v_group_key)
            print(f"絶対順序: {slot_orders}")
            
            # 各例文をExcelデータに変換
            for sentence_data in sentences:
                self.convert_to_excel_rows(sentence_data, v_group_key, slot_orders)
        
        print(f"\n✅ Step 2完了: 総 {len(self.results)} 行生成")
    
    def calculate_slot_display_orders(self, v_group_key):
        """V_group_key内の全例文からSlot_display_orderを動的計算"""
        if v_group_key not in self.vgroup_data:
            return {}
            
        vgroup_sentences = self.vgroup_data[v_group_key]
        
        # Step 1: 全例文から語順を収集
        word_positions = []  # [(position, slot, word), ...]
        
        for sentence_data in vgroup_sentences:
            sentence = sentence_data['sentence']
            slots = sentence_data['slots']
            words = sentence.split()
            
            current_pos = 0
            for slot, candidates in slots.items():
                if not candidates:
                    continue
                    
                candidate = candidates[0]
                slot_phrase = candidate['value']
                
                # 文中での語句の位置を特定
                phrase_words = slot_phrase.split()
                
                # 文中での開始位置を探索
                found_pos = self.find_phrase_position(words, phrase_words, current_pos)
                if found_pos >= 0:
                    word_positions.append((found_pos, slot, slot_phrase))
                    current_pos = found_pos + len(phrase_words)
        
        # Step 2: 語順でソートしてSlot種類を整理
        word_positions.sort(key=lambda x: x[0])  # 位置順でソート
        
        # Step 3: Slot種類ごとに連番を割り当て
        seen_slots = []
        slot_orders = {}
        order = 1
        
        for pos, slot, phrase in word_positions:
            if slot not in seen_slots:
                seen_slots.append(slot)
                slot_orders[slot] = order
                order += 1
        
        return slot_orders
    
    def find_phrase_position(self, words, phrase_words, start_pos=0):
        """文中でのフレーズの位置を検索"""
        if not phrase_words:
            return -1
            
        for i in range(start_pos, len(words) - len(phrase_words) + 1):
            # 完全一致チェック
            if words[i:i+len(phrase_words)] == phrase_words:
                return i
            
            # 部分一致チェック（大文字小文字無視）
            if all(w1.lower() == w2.lower() for w1, w2 in zip(words[i:i+len(phrase_words)], phrase_words)):
                return i
        
        return -1  # 見つからない場合
    
    def convert_to_excel_rows(self, sentence_data, v_group_key, slot_orders):
        """1つの例文をExcel行データに変換"""
        sentence = sentence_data['sentence']
        slots = sentence_data['slots']
        example_id = sentence_data['example_id']
        construction_id = sentence_data['construction_id']
        
        row_count = 0
        for slot, candidates in slots.items():
            if not candidates:
                continue
                
            candidate = candidates[0]
            slot_phrase = candidate['value']
            phrase_type = self.determine_phrase_type(candidate)
            
            # 絶対順序を取得
            slot_display_order = slot_orders.get(slot, 99)  # 見つからない場合は99
            
            # メインスロット行
            main_row = {
                '構文ID': construction_id,
                '例文ID': example_id,
                'V_group_key': v_group_key,
                '原文': sentence if row_count == 0 else None,
                'Slot': slot,
                'SlotPhrase': slot_phrase,
                'PhraseType': phrase_type,
                'SubslotID': None,
                'SubslotElement': None,
                'Slot_display_order': slot_display_order,
                'display_order': 0,
                'QuestionType': self.get_question_type(slot_phrase)
            }
            
            self.results.append(main_row)
            row_count += 1
            
            # サブスロット処理
            if 'subslots' in candidate and candidate['subslots']:
                for sub_slot, sub_value in candidate['subslots'].items():
                    sub_row = {
                        '構文ID': construction_id,
                        '例文ID': example_id,
                        'V_group_key': v_group_key,
                        '原文': None,
                        'Slot': slot,
                        'SlotPhrase': slot_phrase,
                        'PhraseType': 'clause',
                        'SubslotID': sub_slot,
                        'SubslotElement': sub_value,
                        'Slot_display_order': slot_display_order,
                        'display_order': 0,
                        'QuestionType': None
                    }
                    
                    self.results.append(sub_row)
                    row_count += 1
    
    def extract_main_verb(self, slots):
        """メイン動詞を抽出（改良版）"""
        
        # 1. まず通常のVスロットをチェック
        if 'V' in slots and slots['V']:
            verb_candidate = slots['V'][0]['value']
            
            # 動詞らしい単語かチェック
            if self.looks_like_verb(verb_candidate):
                return verb_candidate
        
        # 2. Auxスロットもチェック（助動詞の後に動詞がある可能性）
        if 'Aux' in slots and slots['Aux']:
            aux_candidate = slots['Aux'][0]['value']
            if self.looks_like_verb(aux_candidate):
                return aux_candidate
        
        # 3. O1から動詞を探す（解析ミスの場合）
        if 'O1' in slots and slots['O1']:
            o1_text = slots['O1'][0]['value']
            verb_from_o1 = self.extract_verb_from_text(o1_text)
            if verb_from_o1:
                return verb_from_o1
        
        # 4. 全文から動詞を探す（最後の手段）
        return None
    
    def looks_like_verb(self, word):
        """動詞らしい単語かチェック"""
        # 明らかに動詞でない単語を除外
        non_verbs = ['do', 'you', 'i', 'he', 'she', 'they', 'we', 'what', 'where', 'when', 'why', 'how', 'who']
        if word.lower() in non_verbs:
            return False
            
        # 一般的な動詞パターン
        common_verbs = ['run', 'walk', 'think', 'believe', 'know', 'go', 'come', 'give', 'take', 'make', 'see', 'hear']
        if word.lower() in common_verbs:
            return True
            
        # その他は基本的にTrueとする（保守的アプローチ）
        return True
    
    def extract_verb_from_text(self, text):
        """テキストから動詞を抽出"""
        words = text.split()
        for word in words:
            if self.looks_like_verb(word):
                return word
        return None
    
    def determine_phrase_type(self, candidate):
        """PhraseTypeを判定"""
        value = candidate['value'].strip()
        word_count = len(value.split())
        
        if word_count == 1:
            return 'word'
        elif 'subslots' in candidate and candidate['subslots']:
            return 'clause'
        else:
            return 'phrase'
    
    def get_question_type(self, phrase):
        """QuestionTypeを判定（wh-word識別）"""
        wh_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which']
        phrase_lower = phrase.lower().strip()
        
        if phrase_lower in wh_words:
            return 'wh-word'
        return None
    
    def save_to_excel(self, output_filename="新規例文入力元_v2.xlsx"):
        """Excel形式で保存"""
        if not self.results:
            print("❌ 保存するデータがありません")
            return
            
        # DataFrameに変換
        df = pd.DataFrame(self.results)
        
        # 列順序を調整
        column_order = [
            '構文ID', '例文ID', 'V_group_key', '原文', 'Slot', 'SlotPhrase', 
            'PhraseType', 'SubslotID', 'SubslotElement', 'Slot_display_order', 
            'display_order', 'QuestionType'
        ]
        
        # 不足している列を追加
        for col in column_order:
            if col not in df.columns:
                df[col] = None
                
        # 列順序を適用
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
    
    def show_summary(self):
        """解析結果サマリー表示"""
        print("\n=== 解析結果サマリー ===")
        print(f"V_group数: {len(self.vgroup_data)}個")
        for v_key, sentences in self.vgroup_data.items():
            print(f"  {v_key}: {len(sentences)}文")
            
        if self.results:
            df = pd.DataFrame(self.results)
            print(f"総行数: {len(df)}行")
            print(f"例文数: {self.current_sentence_id - 1}文")


def test_v2():
    """バージョン2テスト"""
    print("=== Excel Generator v2.0 テスト ===")
    
    generator = ExcelGeneratorV2()
    
    # テストデータ
    test_sentences = [
        "I run fast",
        "Do you run every day?",
        "I think that he is smart",
        "What did you buy?"
    ]
    
    # Step 1: 全例文を解析・蓄積
    for sentence in test_sentences:
        generator.analyze_and_add_sentence(sentence)
    
    # Step 2: Excel データ生成
    generator.generate_excel_data()
    
    # サマリー表示
    generator.show_summary()
    
    # Excel保存
    generator.save_to_excel("テスト_v2_絶対順序対応.xlsx")


if __name__ == "__main__":
    test_v2()
