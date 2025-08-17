"""
2つのテストファイルの例文一致確認
"""

import json
import codecs

def compare_test_sentences():
    """例文の完全一致確認"""
    print("🔍 例文一致確認開始")
    
    # test_53_complete.py が使用する例文（final_54_test_data.json から）
    with codecs.open('final_test_system/final_54_test_data.json', 'r', 'utf-8') as f:
        json_data = json.load(f)
    
    json_sentences = []
    for key, value in json_data['data'].items():
        if key.isdigit() and int(key) <= 53:  # 53例文まで
            json_sentences.append(value['sentence'])
    
    # test_final_53.py が使用する例文（ハードコード）
    hardcoded_sentences = [
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
        "The artist whose paintings were exhibited internationally became famous rapidly."
    ]
    
    print(f"📊 JSON例文数: {len(json_sentences)}")
    print(f"📊 ハードコード例文数: {len(hardcoded_sentences)}")
    
    # 完全一致確認
    if len(json_sentences) != len(hardcoded_sentences):
        print("❌ 例文数が異なります")
        return False
    
    mismatches = []
    for i, (json_sent, hard_sent) in enumerate(zip(json_sentences, hardcoded_sentences), 1):
        if json_sent != hard_sent:
            mismatches.append({
                'index': i,
                'json': json_sent,
                'hardcoded': hard_sent
            })
    
    if mismatches:
        print(f"❌ {len(mismatches)}個の例文が不一致:")
        for mismatch in mismatches:
            print(f"  例文{mismatch['index']}:")
            print(f"    JSON:       '{mismatch['json']}'")
            print(f"    ハードコード: '{mismatch['hardcoded']}'")
    else:
        print("✅ 全53例文が完全に一致しています")
        return True
    
    return False

if __name__ == "__main__":
    compare_test_sentences()
