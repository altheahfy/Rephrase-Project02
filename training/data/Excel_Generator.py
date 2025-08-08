# ===== Rephrase Excel Generator =====
# 英文を解析してExcel形式で出力（batch.py用）

import pandas as pd
import os
from Rephrase_Parsing_Engine import RephraseParsingEngine

class ExcelGenerator:
    """Rephrase解析結果をExcel形式で出力"""
    
    def __init__(self):
        self.engine = RephraseParsingEngine()
        self.results = []
        self.current_sentence_id = 1
        self.current_construction_id = 1000
        self.slot_display_orders = {
            'M1': 1, 'M2': 2, 'M3': 3,
            'S': 5, 'Aux': 6, 'V': 7, 
            'O1': 8, 'O2': 9, 'O3': 10,
            'C': 11, 'M4': 12
        }
    
    def analyze_and_add_sentence(self, sentence, v_group_key=None):
        """文を解析してExcelデータに追加"""
        sentence = sentence.strip()
        if not sentence:
            return
            
        print(f"\n=== 解析中: {sentence} ===")
        
        # 品詞分解実行
        slots = self.engine.analyze_sentence(sentence)
        
        if not slots:
            print(f"❌ 解析失敗: {sentence}")
            return
            
        # 例文IDとV_group_key生成
        example_id = f"ex{self.current_sentence_id:03d}"
        if not v_group_key:
            # 動詞から推測
            verb = self.extract_main_verb(slots)
            v_group_key = verb if verb else "unknown"
            
        # 各スロットをExcel行に変換
        row_count = 0
        for slot, candidates in slots.items():
            if not candidates:
                continue
                
            candidate = candidates[0]
            slot_phrase = candidate['value']
            phrase_type = self.determine_phrase_type(candidate)
            
            # メインスロット行
            main_row = {
                '構文ID': self.current_construction_id,
                '例文ID': example_id,
                'V_group_key': v_group_key,
                '原文': sentence if row_count == 0 else None,
                'Slot': slot,
                'SlotPhrase': slot_phrase,
                'PhraseType': phrase_type,
                'SubslotID': None,
                'SubslotElement': None,
                'Slot_display_order': self.slot_display_orders.get(slot, 10),
                'display_order': 0,
                'QuestionType': self.get_question_type(slot_phrase)
            }
            
            self.results.append(main_row)
            row_count += 1
            
            # サブスロット処理（複文の場合）
            if 'subslots' in candidate and candidate['subslots']:
                for sub_slot, sub_value in candidate['subslots'].items():
                    sub_row = {
                        '構文ID': self.current_construction_id,
                        '例文ID': example_id,
                        'V_group_key': v_group_key,
                        '原文': None,
                        'Slot': slot,  # 親スロットと同じ
                        'SlotPhrase': slot_phrase,  # 親と同じ
                        'PhraseType': 'clause',
                        'SubslotID': sub_slot,
                        'SubslotElement': sub_value,
                        'Slot_display_order': self.slot_display_orders.get(slot, 10),
                        'display_order': 0,
                        'QuestionType': None
                    }
                    
                    self.results.append(sub_row)
                    row_count += 1
        
        # 結果表示
        print(f"✅ 解析完了: {row_count}行追加")
        for slot, candidates in slots.items():
            if candidates:
                candidate = candidates[0]
                print(f"  {slot}: {candidate['value']}")
                if 'subslots' in candidate and candidate['subslots']:
                    for sub_slot, sub_value in candidate['subslots'].items():
                        print(f"    └─ {sub_slot}: {sub_value}")
        
        self.current_sentence_id += 1
        self.current_construction_id += 1
    
    def extract_main_verb(self, slots):
        """メイン動詞を抽出"""
        if 'V' in slots and slots['V']:
            return slots['V'][0]['value']
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
    
    def save_to_excel(self, output_filename="新規例文入力元.xlsx"):
        """Excel形式で保存"""
        if not self.results:
            print("❌ 保存するデータがありません")
            return
            
        # DataFrameに変換
        df = pd.DataFrame(self.results)
        
        # 列順序を調整（既存フォーマットに合わせる）
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
        except Exception as e:
            print(f"❌ Excel保存エラー: {e}")
    
    def show_summary(self):
        """解析結果サマリー表示"""
        if not self.results:
            print("解析データがありません")
            return
            
        df = pd.DataFrame(self.results)
        
        print("\n=== 解析結果サマリー ===")
        print(f"総行数: {len(df)}行")
        print(f"例文数: {self.current_sentence_id - 1}文")
        print(f"スロット種類: {df['Slot'].nunique()}種類")
        print("スロット分布:")
        print(df['Slot'].value_counts().to_string())


def interactive_mode():
    """対話式モード"""
    print("=== Rephrase Excel Generator ===")
    print("英文を入力すると品詞分解してExcel形式で蓄積します")
    print("'save'でExcel保存、'quit'で終了")
    
    generator = ExcelGenerator()
    
    while True:
        user_input = input("\n英文を入力: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'save':
            generator.save_to_excel()
        elif user_input.lower() == 'summary':
            generator.show_summary()
        elif user_input:
            generator.analyze_and_add_sentence(user_input)
        else:
            print("英文を入力してください")
    
    # 終了時に自動保存確認
    if generator.results:
        save_confirm = input("\n終了前にExcelファイルを保存しますか？ (y/N): ")
        if save_confirm.lower() == 'y':
            generator.save_to_excel()


def bulk_file_mode():
    """一括ファイル処理モード"""
    print("=== 一括ファイル処理モード ===")
    print("テキストファイルから英文を一括読み込みして処理します")
    
    # ファイル名入力
    while True:
        filename = input("\n英文リストファイル名を入力 (例: sentences.txt): ").strip()
        if not filename:
            print("ファイル名を入力してください")
            continue
            
        if not os.path.exists(filename):
            print(f"❌ ファイルが見つかりません: {filename}")
            
            # 新規作成確認
            create_confirm = input(f"新規ファイル '{filename}' を作成しますか？ (y/N): ")
            if create_confirm.lower() == 'y':
                sample_content = """# 英文リスト（1行1文）
# '#'で始まる行はコメントとして無視されます
# 空行も無視されます

I run fast.
She is happy.
I will go tomorrow.
I could have done it better.
The book is written by John.
I think that he is smart.
She believes that we are ready.
What did you buy yesterday?
Where did she go?
Who wrote this book?"""
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(sample_content)
                    print(f"✅ サンプルファイルを作成しました: {filename}")
                    print("ファイルを編集してから再実行してください")
                    return
                except Exception as e:
                    print(f"❌ ファイル作成エラー: {e}")
                    return
            continue
        else:
            break
    
    # ファイル読み込み・処理
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 英文抽出（コメントと空行を除外）
        sentences = []
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                sentences.append((line_num, line))
        
        if not sentences:
            print(f"❌ {filename} に有効な英文が見つかりません")
            return
            
        print(f"\n📖 {len(sentences)}個の英文を発見しました:")
        for i, (line_num, sentence) in enumerate(sentences[:5], 1):
            print(f"  {i}. {sentence}")
        if len(sentences) > 5:
            print(f"  ... 他{len(sentences) - 5}個")
        
        # 処理確認
        process_confirm = input(f"\n{len(sentences)}個の英文を一括処理しますか？ (y/N): ")
        if process_confirm.lower() != 'y':
            print("処理をキャンセルしました")
            return
        
        # 一括処理実行
        generator = ExcelGenerator()
        
        print(f"\n=== 一括処理開始 ===")
        success_count = 0
        error_count = 0
        
        for line_num, sentence in sentences:
            try:
                print(f"\n[{success_count + error_count + 1}/{len(sentences)}] Line {line_num}: {sentence}")
                generator.analyze_and_add_sentence(sentence)
                success_count += 1
            except Exception as e:
                print(f"❌ エラー (Line {line_num}): {e}")
                error_count += 1
        
        # 結果サマリー
        print(f"\n=== 処理完了 ===")
        print(f"✅ 成功: {success_count}個")
        print(f"❌ エラー: {error_count}個")
        
        if success_count > 0:
            generator.show_summary()
            
            # 自動保存
            output_filename = f"一括処理_{filename.replace('.txt', '')}_結果.xlsx"
            generator.save_to_excel(output_filename)
        
    except Exception as e:
        print(f"❌ ファイル処理エラー: {e}")


def batch_mode():
    """バッチ処理モード（テスト用）"""
    test_sentences = [
        "I run fast",
        "She is happy", 
        "I will go",
        "I could have done it",
        "The book is written by John",
        "I think that he is smart",
        "She believes that we are ready",
        "I know what he thinks",
        "What did you buy?",
        "Where did she go?"
    ]
    
    generator = ExcelGenerator()
    
    print("=== バッチ処理モード ===")
    for sentence in test_sentences:
        generator.analyze_and_add_sentence(sentence)
    
    generator.show_summary()
    generator.save_to_excel("テスト用例文入力元.xlsx")


if __name__ == "__main__":
    print("モードを選択してください:")
    print("1: 対話式モード（英文を手動入力）")
    print("2: バッチ処理モード（テストデータで自動実行）")
    print("3: 一括ファイル処理モード（txtファイルから84個でも一気に処理）★推奨")
    
    mode = input("モード番号 (1, 2, or 3): ").strip()
    
    if mode == "2":
        batch_mode()
    elif mode == "3":
        bulk_file_mode()
    else:
        interactive_mode()
