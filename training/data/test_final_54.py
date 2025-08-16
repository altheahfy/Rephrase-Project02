#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
54例文完全テスト（有効31例文 + 新規23例文）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
import codecs

def test_final_54_sentences():
    """54例文完全テスト実行"""
    print("🧪 54例文完全テスト開始")
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    
    # 全ハンドラーを追加
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    print("✅ システム準備完了")
    
    # 54例文完全セット（有効31例文 + 新規23例文）
    test_sentences = [
        "The car is red.",
        "I love you.",
        "The man who runs fast is strong.",
        "The book which lies there is mine.",
        "The person that works here is kind.",
        "The book which I bought is expensive.",
        "The man whom I met is tall.",
        "The car that he drives is new.",
        "The car which was crashed is red.",
        "The book that was written is famous.",
        "The letter which was sent arrived.",
        "The man whose car is red lives here.",
        "The student whose book I borrowed is smart.",
        "The woman whose dog barks is my neighbor.",
        "The place where we met is beautiful.",
        "The time when he arrived was late.",
        "The reason why she left is unclear.",
        "The way how he solved it was clever.",
        "The book I read yesterday was boring.",
        "He has finished his homework.",
        "The letter was written by John.",
        "The house was built in 1990.",
        "The book was written by a famous author.",
        "The cake is being baked by my mother.",
        "The cake was eaten by the children.",
        "The door was opened by the key.",
        "The message was sent yesterday.",
        "She acts as if she knows everything.",
        "The students study hard for exams.",
        "The car was repaired last week.",
        "The book which was carefully written by Shakespeare is famous.",
        "The car that was quickly repaired yesterday runs smoothly.",
        "The letter which was slowly typed by the secretary arrived today.",
        "The student who studies diligently always succeeds academically.",
        "The teacher whose class runs efficiently is respected greatly.",
        "The doctor who works carefully saves lives successfully.",
        "The window was gently opened by the morning breeze.",
        "The message is being carefully written by the manager.",
        "The problem was quickly solved by the expert team.",
        "The house whose roof was damaged badly needs immediate repair.",
        "The place where we met accidentally became our favorite spot.",
        "The time when everything changed dramatically was unexpected.",
        "The building is being constructed very carefully by skilled workers.",
        "The teacher explains grammar clearly to confused students daily.",
        "The student writes essays carefully for better grades.",
        "The report which was thoroughly reviewed by experts was published successfully.",
        "The student whose essay was carefully corrected improved dramatically.",
        "The machine that was properly maintained works efficiently every day.",
        "The team working overtime completed the project successfully yesterday.",
        "The woman standing quietly near the door was waiting patiently.",
        "The children playing happily in the garden were supervised carefully.",
        "The documents being reviewed thoroughly will be approved soon.",
        "The artist whose paintings were exhibited internationally became famous rapidly.",
        "The book was published in 2020."
    ]
    
    print(f"\n📖 テスト例文数: {len(test_sentences)}")
    print("="*60)
    
    success_count = 0
    processing_times = []
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n🧪 テスト{i:2d}: {sentence}")
        print("-" * 50)
        
        try:
            result = mapper.process(sentence)
            processing_time = result['meta']['processing_time']
            processing_times.append(processing_time)
            
            print(f"⏱️  処理時間: {processing_time:.3f}秒")
            
            # 結果詳細表示
            slots = result.get('slots', {})
            sub_slots = result.get('sub_slots', {})
            
            if slots or sub_slots:
                print("📊 分解結果:")
                
                # メインスロット
                if slots:
                    for slot, value in slots.items():
                        if value.strip():  # 空でない場合
                            print(f"  {slot:4s}: {value}")
                
                # サブスロット
                if sub_slots:
                    print("  サブスロット:")
                    for slot, value in sub_slots.items():
                        if value.strip():
                            print(f"    {slot}: {value}")
                
                success_count += 1
                print("✅ 分解成功")
            else:
                print("📊 分解結果: スロット検出なし")
                print("❌ 分解失敗")
                
        except Exception as e:
            print(f"💥 エラー: {e}")
            print("❌ 処理失敗")
    
    # 統計表示
    print(f"\n{'='*60}")
    print(f"📊 テスト結果統計:")
    print(f"  総テスト数: {len(test_sentences)}")
    print(f"  分解成功数: {success_count}")
    print(f"  成功率: {success_count/len(test_sentences)*100:.1f}%")
    if processing_times:
        print(f"  平均処理時間: {sum(processing_times)/len(processing_times):.3f}秒")
    
    print("\n🎉 54例文完全テスト完了！")

if __name__ == "__main__":
    test_final_54_sentences()
