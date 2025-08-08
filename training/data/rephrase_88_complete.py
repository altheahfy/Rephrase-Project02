"""
全88例文を正しい入力様式に変換（完全版）
例文入力元.xlsxの形式に完全準拠
"""

import pandas as pd
import numpy as np

def create_all_88_sentences():
    """全88例文のデータ作成"""
    
    all_sentences = [
        # セット1: I lie on the bed (4例文)
        {"set_id": "set_01", "ex_id": "ex101", "original": "I lie on the bed.", "slots": [("S", "I", "word"), ("V", "lie", "word"), ("M3", "on the bed", "phrase")]},
        {"set_id": "set_01", "ex_id": "ex102", "original": "You lie on the sofa.", "slots": [("S", "You", "word"), ("V", "lie", "word"), ("M3", "on the sofa", "phrase")]},
        {"set_id": "set_01", "ex_id": "ex103", "original": "We lie on the floor.", "slots": [("S", "We", "word"), ("V", "lie", "word"), ("M3", "on the floor", "phrase")]},
        {"set_id": "set_01", "ex_id": "ex104", "original": "They lie on the couch.", "slots": [("S", "They", "word"), ("V", "lie", "word"), ("M3", "on the couch", "phrase")]},
        
        # セット2: You got me! (4例文)
        {"set_id": "set_02", "ex_id": "ex201", "original": "You got me!", "slots": [("S", "You", "word"), ("V", "got", "word"), ("O1", "me", "word")]},
        {"set_id": "set_02", "ex_id": "ex202", "original": "I got him!", "slots": [("S", "I", "word"), ("V", "got", "word"), ("O1", "him", "word")]},
        {"set_id": "set_02", "ex_id": "ex203", "original": "He got them!", "slots": [("S", "He", "word"), ("V", "got", "word"), ("O1", "them", "word")]},
        {"set_id": "set_02", "ex_id": "ex204", "original": "We got Mark!", "slots": [("S", "We", "word"), ("V", "got", "word"), ("O1", "Mark", "word")]},
        
        # セット3: Where did you get it? (4例文)
        {"set_id": "set_03", "ex_id": "ex301", "original": "Where did you get it?", "slots": [("M3", "Where", "word"), ("S", "you", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "it", "word")]},
        {"set_id": "set_03", "ex_id": "ex302", "original": "Where did I get the device?", "slots": [("M3", "Where", "word"), ("S", "I", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "the device", "phrase")]},
        {"set_id": "set_03", "ex_id": "ex303", "original": "Where did she get the book?", "slots": [("M3", "Where", "word"), ("S", "she", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "the book", "phrase")]},
        {"set_id": "set_03", "ex_id": "ex304", "original": "Where did they get the information?", "slots": [("M3", "Where", "word"), ("S", "they", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "the information", "phrase")]},
        
        # セット4: You, give it to me straight. (4例文)
        {"set_id": "set_04", "ex_id": "ex401", "original": "You, give it to me straight.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "it", "word"), ("O2", "me", "word"), ("M2", "straight", "word")]},
        {"set_id": "set_04", "ex_id": "ex402", "original": "You, give that to him clearly.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "that", "word"), ("O2", "him", "word"), ("M2", "clearly", "word")]},
        {"set_id": "set_04", "ex_id": "ex403", "original": "You, give this to her honestly.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "this", "word"), ("O2", "her", "word"), ("M2", "honestly", "word")]},
        {"set_id": "set_04", "ex_id": "ex404", "original": "You, give them to us directly.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "them", "word"), ("O2", "us", "word"), ("M2", "directly", "word")]},
        
        # セット5: That reminds me. (4例文)
        {"set_id": "set_05", "ex_id": "ex501", "original": "That reminds me.", "slots": [("S", "That", "word"), ("V", "reminds", "word"), ("O1", "me", "word")]},
        {"set_id": "set_05", "ex_id": "ex502", "original": "This reminds you.", "slots": [("S", "This", "word"), ("V", "reminds", "word"), ("O1", "you", "word")]},
        {"set_id": "set_05", "ex_id": "ex503", "original": "It reminds her.", "slots": [("S", "It", "word"), ("V", "reminds", "word"), ("O1", "her", "word")]},
        {"set_id": "set_05", "ex_id": "ex504", "original": "Everything reminds them.", "slots": [("S", "Everything", "word"), ("V", "reminds", "word"), ("O1", "them", "word")]},
        
        # セット6: Would you hold the line, please? (4例文)
        {"set_id": "set_06", "ex_id": "ex601", "original": "Would you hold the line, please?", "slots": [("S", "you", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the line", "phrase"), ("M2", "please", "word")]},
        {"set_id": "set_06", "ex_id": "ex602", "original": "Would I hold the call, please?", "slots": [("S", "I", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the call", "phrase"), ("M2", "please", "word")]},
        {"set_id": "set_06", "ex_id": "ex603", "original": "Would she hold the phone, please?", "slots": [("S", "she", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the phone", "phrase"), ("M2", "please", "word")]},
        {"set_id": "set_06", "ex_id": "ex604", "original": "Would they hold the connection, please?", "slots": [("S", "they", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the connection", "phrase"), ("M2", "please", "word")]},
        
        # セット7: I haven't seen you for a long time. (4例文)
        {"set_id": "set_07", "ex_id": "ex701", "original": "I haven't seen you for a long time.", "slots": [("S", "I", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "you", "word"), ("M3", "for a long time", "phrase")]},
        {"set_id": "set_07", "ex_id": "ex702", "original": "You haven't seen me for ages.", "slots": [("S", "You", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "me", "word"), ("M3", "for ages", "phrase")]},
        {"set_id": "set_07", "ex_id": "ex703", "original": "We haven't seen Ken for months.", "slots": [("S", "We", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "Ken", "word"), ("M3", "for months", "phrase")]},
        {"set_id": "set_07", "ex_id": "ex704", "original": "They haven't seen him for years.", "slots": [("S", "They", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "him", "word"), ("M3", "for years", "phrase")]},
        
        # セット8: I want something hot. (4例文)
        {"set_id": "set_08", "ex_id": "ex801", "original": "I want something hot.", "slots": [("S", "I", "word"), ("V", "want", "word"), ("O1", "something hot", "phrase")]},
        {"set_id": "set_08", "ex_id": "ex802", "original": "You want something spicy.", "slots": [("S", "You", "word"), ("V", "want", "word"), ("O1", "something spicy", "phrase")]},
        {"set_id": "set_08", "ex_id": "ex803", "original": "We want something sweet.", "slots": [("S", "We", "word"), ("V", "want", "word"), ("O1", "something sweet", "phrase")]},
        {"set_id": "set_08", "ex_id": "ex804", "original": "They want something fresh.", "slots": [("S", "They", "word"), ("V", "want", "word"), ("O1", "something fresh", "phrase")]},
        
        # セット9: Could you write it down, please? (4例文)
        {"set_id": "set_09", "ex_id": "ex901", "original": "Could you write it down, please?", "slots": [("S", "you", "word"), ("Aux", "Could", "word"), ("V", "write", "word"), ("O1", "it", "word"), ("M2", "down", "word"), ("M3", "please", "word")]},
        {"set_id": "set_09", "ex_id": "ex902", "original": "Could I write the sentence down, please?", "slots": [("S", "I", "word"), ("Aux", "Could", "word"), ("V", "write", "word"), ("O1", "the sentence", "phrase"), ("M2", "down", "word"), ("M3", "please", "word")]},
        {"set_id": "set_09", "ex_id": "ex903", "original": "Could she write the address down, please?", "slots": [("S", "she", "word"), ("Aux", "Could", "word"), ("V", "write", "word"), ("O1", "the address", "phrase"), ("M2", "down", "word"), ("M3", "please", "word")]},
        {"set_id": "set_09", "ex_id": "ex904", "original": "Could they write the number down, please?", "slots": [("S", "they", "word"), ("Aux", "Could", "word"), ("V", "write", "word"), ("O1", "the number", "phrase"), ("M2", "down", "word"), ("M3", "please", "word")]},
        
        # セット10: I can't afford it. (4例文)
        {"set_id": "set_10", "ex_id": "ex1001", "original": "I can't afford it.", "slots": [("S", "I", "word"), ("Aux", "can't", "word"), ("V", "afford", "word"), ("O1", "it", "word")]},
        {"set_id": "set_10", "ex_id": "ex1002", "original": "You can't afford the jacket.", "slots": [("S", "You", "word"), ("Aux", "can't", "word"), ("V", "afford", "word"), ("O1", "the jacket", "phrase")]},
        {"set_id": "set_10", "ex_id": "ex1003", "original": "She can't afford the car.", "slots": [("S", "She", "word"), ("Aux", "can't", "word"), ("V", "afford", "word"), ("O1", "the car", "phrase")]},
        {"set_id": "set_10", "ex_id": "ex1004", "original": "They can't afford the house.", "slots": [("S", "They", "word"), ("Aux", "can't", "word"), ("V", "afford", "word"), ("O1", "the house", "phrase")]},
        
        # セット11: I believe you. (4例文)
        {"set_id": "set_11", "ex_id": "ex1101", "original": "I believe you.", "slots": [("S", "I", "word"), ("V", "believe", "word"), ("O1", "you", "word")]},
        {"set_id": "set_11", "ex_id": "ex1102", "original": "You believe Tom.", "slots": [("S", "You", "word"), ("V", "believe", "word"), ("O1", "Tom", "word")]},
        {"set_id": "set_11", "ex_id": "ex1103", "original": "We believe her.", "slots": [("S", "We", "word"), ("V", "believe", "word"), ("O1", "her", "word")]},
        {"set_id": "set_11", "ex_id": "ex1104", "original": "They believe him.", "slots": [("S", "They", "word"), ("V", "believe", "word"), ("O1", "him", "word")]},
        
        # セット12: Henry mentioned the fact. (4例文)
        {"set_id": "set_12", "ex_id": "ex1201", "original": "Henry mentioned the fact.", "slots": [("S", "Henry", "word"), ("V", "mentioned", "word"), ("O1", "the fact", "phrase")]},
        {"set_id": "set_12", "ex_id": "ex1202", "original": "Sarah mentioned the issue.", "slots": [("S", "Sarah", "word"), ("V", "mentioned", "word"), ("O1", "the issue", "phrase")]},
        {"set_id": "set_12", "ex_id": "ex1203", "original": "Tom mentioned the problem.", "slots": [("S", "Tom", "word"), ("V", "mentioned", "word"), ("O1", "the problem", "phrase")]},
        {"set_id": "set_12", "ex_id": "ex1204", "original": "They mentioned the concern.", "slots": [("S", "They", "word"), ("V", "mentioned", "word"), ("O1", "the concern", "phrase")]},
        
        # セット13: He entered her room. (4例文)
        {"set_id": "set_13", "ex_id": "ex1301", "original": "He entered her room.", "slots": [("S", "He", "word"), ("V", "entered", "word"), ("O1", "her room", "phrase")]},
        {"set_id": "set_13", "ex_id": "ex1302", "original": "She entered his office.", "slots": [("S", "She", "word"), ("V", "entered", "word"), ("O1", "his office", "phrase")]},
        {"set_id": "set_13", "ex_id": "ex1303", "original": "Tom entered Sarah's house.", "slots": [("S", "Tom", "word"), ("V", "entered", "word"), ("O1", "Sarah's house", "phrase")]},
        {"set_id": "set_13", "ex_id": "ex1304", "original": "They entered the building.", "slots": [("S", "They", "word"), ("V", "entered", "word"), ("O1", "the building", "phrase")]},
        
        # セット14: He left New York a few days ago. (4例文)
        {"set_id": "set_14", "ex_id": "ex1401", "original": "He left New York a few days ago.", "slots": [("S", "He", "word"), ("V", "left", "word"), ("O1", "New York", "phrase"), ("M3", "a few days ago", "phrase")]},
        {"set_id": "set_14", "ex_id": "ex1402", "original": "She left Rome last week.", "slots": [("S", "She", "word"), ("V", "left", "word"), ("O1", "Rome", "word"), ("M3", "last week", "phrase")]},
        {"set_id": "set_14", "ex_id": "ex1403", "original": "Tom left Paris yesterday.", "slots": [("S", "Tom", "word"), ("V", "left", "word"), ("O1", "Paris", "word"), ("M3", "yesterday", "word")]},
        {"set_id": "set_14", "ex_id": "ex1404", "original": "They left London this morning.", "slots": [("S", "They", "word"), ("V", "left", "word"), ("O1", "London", "word"), ("M3", "this morning", "phrase")]},
        
        # セット15: He reached Boston the next morning. (4例文)
        {"set_id": "set_15", "ex_id": "ex1501", "original": "He reached Boston the next morning.", "slots": [("S", "He", "word"), ("V", "reached", "word"), ("O1", "Boston", "word"), ("M3", "the next morning", "phrase")]},
        {"set_id": "set_15", "ex_id": "ex1502", "original": "She reached Milan that evening.", "slots": [("S", "She", "word"), ("V", "reached", "word"), ("O1", "Milan", "word"), ("M3", "that evening", "phrase")]},
        {"set_id": "set_15", "ex_id": "ex1503", "original": "Tom reached Tokyo at noon.", "slots": [("S", "Tom", "word"), ("V", "reached", "word"), ("O1", "Tokyo", "word"), ("M3", "at noon", "phrase")]},
        {"set_id": "set_15", "ex_id": "ex1504", "original": "They reached Berlin at midnight.", "slots": [("S", "They", "word"), ("V", "reached", "word"), ("O1", "Berlin", "word"), ("M3", "at midnight", "phrase")]},
        
        # セット16: I approach Tokyo. (4例文)
        {"set_id": "set_16", "ex_id": "ex1601", "original": "I approach Tokyo.", "slots": [("S", "I", "word"), ("V", "approach", "word"), ("O1", "Tokyo", "word")]},
        {"set_id": "set_16", "ex_id": "ex1602", "original": "You approach the station.", "slots": [("S", "You", "word"), ("V", "approach", "word"), ("O1", "the station", "phrase")]},
        {"set_id": "set_16", "ex_id": "ex1603", "original": "We approach the building.", "slots": [("S", "We", "word"), ("V", "approach", "word"), ("O1", "the building", "phrase")]},
        {"set_id": "set_16", "ex_id": "ex1604", "original": "They approach the destination.", "slots": [("S", "They", "word"), ("V", "approach", "word"), ("O1", "the destination", "phrase")]},
        
        # セット17: He resembles his mother. (4例文)
        {"set_id": "set_17", "ex_id": "ex1701", "original": "He resembles his mother.", "slots": [("S", "He", "word"), ("V", "resembles", "word"), ("O1", "his mother", "phrase")]},
        {"set_id": "set_17", "ex_id": "ex1702", "original": "She resembles her father.", "slots": [("S", "She", "word"), ("V", "resembles", "word"), ("O1", "her father", "phrase")]},
        {"set_id": "set_17", "ex_id": "ex1703", "original": "Tom resembles his uncle.", "slots": [("S", "Tom", "word"), ("V", "resembles", "word"), ("O1", "his uncle", "phrase")]},
        {"set_id": "set_17", "ex_id": "ex1704", "original": "They resemble their parents.", "slots": [("S", "They", "word"), ("V", "resemble", "word"), ("O1", "their parents", "phrase")]},
        
        # セット18: She married a bald man. (4例文)
        {"set_id": "set_18", "ex_id": "ex1801", "original": "She married a bald man.", "slots": [("S", "She", "word"), ("V", "married", "word"), ("O1", "a bald man", "phrase")]},
        {"set_id": "set_18", "ex_id": "ex1802", "original": "He married a quiet woman.", "slots": [("S", "He", "word"), ("V", "married", "word"), ("O1", "a quiet woman", "phrase")]},
        {"set_id": "set_18", "ex_id": "ex1803", "original": "Sarah married a kind person.", "slots": [("S", "Sarah", "word"), ("V", "married", "word"), ("O1", "a kind person", "phrase")]},
        {"set_id": "set_18", "ex_id": "ex1804", "original": "They married their partners.", "slots": [("S", "They", "word"), ("V", "married", "word"), ("O1", "their partners", "phrase")]},
        
        # セット19: She got married with a bald man. (4例文)
        {"set_id": "set_19", "ex_id": "ex1901", "original": "She got married with a bald man.", "slots": [("S", "She", "word"), ("V", "got married with", "phrase"), ("O1", "a bald man", "phrase")]},
        {"set_id": "set_19", "ex_id": "ex1902", "original": "He got married with a kind woman.", "slots": [("S", "He", "word"), ("V", "got married with", "phrase"), ("O1", "a kind woman", "phrase")]},
        {"set_id": "set_19", "ex_id": "ex1903", "original": "Sarah got married with a nice person.", "slots": [("S", "Sarah", "word"), ("V", "got married with", "phrase"), ("O1", "a nice person", "phrase")]},
        {"set_id": "set_19", "ex_id": "ex1904", "original": "Tom got married with a lovely partner.", "slots": [("S", "Tom", "word"), ("V", "got married with", "phrase"), ("O1", "a lovely partner", "phrase")]},
        
        # セット20: She's been married to a bald man for 5 years. (4例文)
        {"set_id": "set_20", "ex_id": "ex2001", "original": "She's been married to a bald man for 5 years.", "slots": [("S", "She", "word"), ("Aux", "has been", "phrase"), ("V", "married to", "phrase"), ("O1", "a bald man", "phrase"), ("M3", "for 5 years", "phrase")]},
        {"set_id": "set_20", "ex_id": "ex2002", "original": "He's been married to a kind woman for 3 years.", "slots": [("S", "He", "word"), ("Aux", "has been", "phrase"), ("V", "married to", "phrase"), ("O1", "a kind woman", "phrase"), ("M3", "for 3 years", "phrase")]},
        {"set_id": "set_20", "ex_id": "ex2003", "original": "Sarah's been married to a nice person for 2 years.", "slots": [("S", "Sarah", "word"), ("Aux", "has been", "phrase"), ("V", "married to", "phrase"), ("O1", "a nice person", "phrase"), ("M3", "for 2 years", "phrase")]},
        {"set_id": "set_20", "ex_id": "ex2004", "original": "Tom's been married to a lovely partner for 10 years.", "slots": [("S", "Tom", "word"), ("Aux", "has been", "phrase"), ("V", "married to", "phrase"), ("O1", "a lovely partner", "phrase"), ("M3", "for 10 years", "phrase")]},
        
        # セット21: He'll answer your letter soon. (4例文)
        {"set_id": "set_21", "ex_id": "ex2101", "original": "He'll answer your letter soon.", "slots": [("S", "He", "word"), ("Aux", "will", "word"), ("V", "answer", "word"), ("O1", "your letter", "phrase"), ("M3", "soon", "word")]},
        {"set_id": "set_21", "ex_id": "ex2102", "original": "She'll answer his message tomorrow.", "slots": [("S", "She", "word"), ("Aux", "will", "word"), ("V", "answer", "word"), ("O1", "his message", "phrase"), ("M3", "tomorrow", "word")]},
        {"set_id": "set_21", "ex_id": "ex2103", "original": "Tom'll answer the email later.", "slots": [("S", "Tom", "word"), ("Aux", "will", "word"), ("V", "answer", "word"), ("O1", "the email", "phrase"), ("M3", "later", "word")]},
        {"set_id": "set_21", "ex_id": "ex2104", "original": "They'll answer our call tonight.", "slots": [("S", "They", "word"), ("Aux", "will", "word"), ("V", "answer", "word"), ("O1", "our call", "phrase"), ("M3", "tonight", "word")]},
        
        # セット22: We discuss our schedule. (4例文)
        {"set_id": "set_22", "ex_id": "ex2201", "original": "We discuss our schedule.", "slots": [("S", "We", "word"), ("V", "discuss", "word"), ("O1", "our schedule", "phrase")]},
        {"set_id": "set_22", "ex_id": "ex2202", "original": "You discuss your project.", "slots": [("S", "You", "word"), ("V", "discuss", "word"), ("O1", "your project", "phrase")]},
        {"set_id": "set_22", "ex_id": "ex2203", "original": "They discuss their plan.", "slots": [("S", "They", "word"), ("V", "discuss", "word"), ("O1", "their plan", "phrase")]},
        {"set_id": "set_22", "ex_id": "ex2204", "original": "I discuss my proposal.", "slots": [("S", "I", "word"), ("V", "discuss", "word"), ("O1", "my proposal", "phrase")]},
    ]
    
    return all_sentences

def export_full_format():
    """完全版の正しい形式でExcel出力"""
    
    # 全88例文取得
    all_sentences = create_all_88_sentences()
    
    # スロット表示順序のマッピング
    slot_display_order = {
        "M1": 1, "S": 2, "Aux": 3, "V": 4, "M2": 5, "O1": 6, "O2": 7, "C1": 8, "C2": 9, "M3": 10
    }
    
    # データを展開
    rows = []
    
    for sentence in all_sentences:
        ex_id = sentence["ex_id"]
        original = sentence["original"]
        slots = sentence["slots"]
        set_num = int(sentence["set_id"].replace("set_", ""))
        v_group = f"{set_num:02d}"  # "01", "02", etc.
        
        # 最初の行に原文を設定
        first_row = True
        
        for i, (slot, phrase, phrase_type) in enumerate(slots):
            row = {
                "構文ID": 1000 + set_num,  # 1001, 1002, etc.
                "例文ID": ex_id,
                "V_group_key": v_group,
                "原文": original if first_row else np.nan,
                "Slot": slot,
                "SlotPhrase": phrase,
                "PhraseType": phrase_type,
                "SubslotID": np.nan,
                "SubslotElement": np.nan,
                "Slot_display_order": slot_display_order.get(slot, 99),
                "display_order": 0
            }
            rows.append(row)
            first_row = False
    
    # DataFrame作成
    df = pd.DataFrame(rows)
    
    # 列順序調整
    columns = ['構文ID', '例文ID', 'V_group_key', '原文', 'Slot', 'SlotPhrase', 
               'PhraseType', 'SubslotID', 'SubslotElement', 'Slot_display_order', 'display_order']
    df = df[columns]
    
    # ソート
    df = df.sort_values(['例文ID', 'Slot_display_order', 'display_order'])
    
    # Excel出力
    output_file = "rephrase_88_complete_format.xlsx"
    df.to_excel(output_file, index=False, sheet_name="Sheet1")
    
    print(f"✅ 全88例文の完全版出力完了")
    print(f"📊 ファイル: {output_file}")
    print(f"📈 レコード数: {len(df)}")
    print(f"📈 例文数: {df['例文ID'].nunique()}")
    
    # 統計情報
    print(f"\n📊 統計:")
    print(f"- セット数: {len(set([s['set_id'] for s in all_sentences]))}")
    print(f"- 平均スロット数/例文: {len(df) / df['例文ID'].nunique():.1f}")
    
    # 各セットの例文数確認
    set_counts = {}
    for s in all_sentences:
        set_id = s['set_id']
        if set_id not in set_counts:
            set_counts[set_id] = 0
        set_counts[set_id] += 1
    
    print(f"- 各セットの例文数: {list(set_counts.values())} (全て4例文であることを確認)")
    
    return df

if __name__ == "__main__":
    df = export_full_format()
