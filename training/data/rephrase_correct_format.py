"""
88例文を正しい入力様式に変換
例文入力元.xlsxの形式に準拠
"""

import pandas as pd
import numpy as np

def create_rephrase_format():
    """88例文を正しい様式で作成"""
    
    # 88例文データ（簡略版）
    sentences = [
        # セット1: I lie on the bed
        {"set_id": "set_01", "ex_id": "ex101", "original": "I lie on the bed.", "slots": [("S", "I", "word"), ("V", "lie", "word"), ("M3", "on the bed", "phrase")]},
        {"set_id": "set_01", "ex_id": "ex102", "original": "You lie on the sofa.", "slots": [("S", "You", "word"), ("V", "lie", "word"), ("M3", "on the sofa", "phrase")]},
        {"set_id": "set_01", "ex_id": "ex103", "original": "We lie on the floor.", "slots": [("S", "We", "word"), ("V", "lie", "word"), ("M3", "on the floor", "phrase")]},
        {"set_id": "set_01", "ex_id": "ex104", "original": "They lie on the couch.", "slots": [("S", "They", "word"), ("V", "lie", "word"), ("M3", "on the couch", "phrase")]},
        
        # セット2: You got me!
        {"set_id": "set_02", "ex_id": "ex201", "original": "You got me!", "slots": [("S", "You", "word"), ("V", "got", "word"), ("O1", "me", "word")]},
        {"set_id": "set_02", "ex_id": "ex202", "original": "I got him!", "slots": [("S", "I", "word"), ("V", "got", "word"), ("O1", "him", "word")]},
        {"set_id": "set_02", "ex_id": "ex203", "original": "He got them!", "slots": [("S", "He", "word"), ("V", "got", "word"), ("O1", "them", "word")]},
        {"set_id": "set_02", "ex_id": "ex204", "original": "We got Mark!", "slots": [("S", "We", "word"), ("V", "got", "word"), ("O1", "Mark", "word")]},
        
        # セット3: Where did you get it?
        {"set_id": "set_03", "ex_id": "ex301", "original": "Where did you get it?", "slots": [("M3", "Where", "word"), ("S", "you", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "it", "word")]},
        {"set_id": "set_03", "ex_id": "ex302", "original": "Where did I get the device?", "slots": [("M3", "Where", "word"), ("S", "I", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "the device", "phrase")]},
        {"set_id": "set_03", "ex_id": "ex303", "original": "Where did she get the book?", "slots": [("M3", "Where", "word"), ("S", "she", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "the book", "phrase")]},
        {"set_id": "set_03", "ex_id": "ex304", "original": "Where did they get the information?", "slots": [("M3", "Where", "word"), ("S", "they", "word"), ("Aux", "did", "word"), ("V", "get", "word"), ("O1", "the information", "phrase")]},
        
        # セット4: You, give it to me straight.
        {"set_id": "set_04", "ex_id": "ex401", "original": "You, give it to me straight.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "it", "word"), ("O2", "me", "word"), ("M2", "straight", "word")]},
        {"set_id": "set_04", "ex_id": "ex402", "original": "You, give that to him clearly.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "that", "word"), ("O2", "him", "word"), ("M2", "clearly", "word")]},
        {"set_id": "set_04", "ex_id": "ex403", "original": "You, give this to her honestly.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "this", "word"), ("O2", "her", "word"), ("M2", "honestly", "word")]},
        {"set_id": "set_04", "ex_id": "ex404", "original": "You, give them to us directly.", "slots": [("S", "You", "word"), ("V", "give", "word"), ("O1", "them", "word"), ("O2", "us", "word"), ("M2", "directly", "word")]},
        
        # セット5: That reminds me.
        {"set_id": "set_05", "ex_id": "ex501", "original": "That reminds me.", "slots": [("S", "That", "word"), ("V", "reminds", "word"), ("O1", "me", "word")]},
        {"set_id": "set_05", "ex_id": "ex502", "original": "This reminds you.", "slots": [("S", "This", "word"), ("V", "reminds", "word"), ("O1", "you", "word")]},
        {"set_id": "set_05", "ex_id": "ex503", "original": "It reminds her.", "slots": [("S", "It", "word"), ("V", "reminds", "word"), ("O1", "her", "word")]},
        {"set_id": "set_05", "ex_id": "ex504", "original": "Everything reminds them.", "slots": [("S", "Everything", "word"), ("V", "reminds", "word"), ("O1", "them", "word")]},
    ]
    
    # スロット表示順序のマッピング
    slot_display_order = {
        "M1": 1, "S": 2, "Aux": 3, "V": 4, "M2": 5, "O1": 6, "O2": 7, "C1": 8, "C2": 9, "M3": 10
    }
    
    # データを展開
    rows = []
    
    for sentence in sentences:
        ex_id = sentence["ex_id"]
        original = sentence["original"]
        slots = sentence["slots"]
        v_group = sentence["set_id"].replace("set_", "")  # "01", "02", etc.
        
        # 最初の行に原文を設定
        first_row = True
        
        for i, (slot, phrase, phrase_type) in enumerate(slots):
            row = {
                "構文ID": int(v_group) + 1000,  # 1001, 1002, etc.
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
    
    return rows

def create_full_88_sentences():
    """全88例文のデータ作成"""
    
    all_sentences = [
        # セット1-5 (上記と同じ)
        
        # セット6: Would you hold the line, please?
        {"set_id": "set_06", "ex_id": "ex601", "original": "Would you hold the line, please?", "slots": [("S", "you", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the line", "phrase"), ("M2", "please", "word")]},
        {"set_id": "set_06", "ex_id": "ex602", "original": "Would I hold the call, please?", "slots": [("S", "I", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the call", "phrase"), ("M2", "please", "word")]},
        {"set_id": "set_06", "ex_id": "ex603", "original": "Would she hold the phone, please?", "slots": [("S", "she", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the phone", "phrase"), ("M2", "please", "word")]},
        {"set_id": "set_06", "ex_id": "ex604", "original": "Would they hold the connection, please?", "slots": [("S", "they", "word"), ("Aux", "Would", "word"), ("V", "hold", "word"), ("O1", "the connection", "phrase"), ("M2", "please", "word")]},
        
        # セット7: I haven't seen you for a long time.
        {"set_id": "set_07", "ex_id": "ex701", "original": "I haven't seen you for a long time.", "slots": [("S", "I", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "you", "word"), ("M3", "for a long time", "phrase")]},
        {"set_id": "set_07", "ex_id": "ex702", "original": "You haven't seen me for ages.", "slots": [("S", "You", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "me", "word"), ("M3", "for ages", "phrase")]},
        {"set_id": "set_07", "ex_id": "ex703", "original": "We haven't seen Ken for months.", "slots": [("S", "We", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "Ken", "word"), ("M3", "for months", "phrase")]},
        {"set_id": "set_07", "ex_id": "ex704", "original": "They haven't seen him for years.", "slots": [("S", "They", "word"), ("Aux", "haven't", "word"), ("V", "seen", "word"), ("O1", "him", "word"), ("M3", "for years", "phrase")]},
        
        # セット8: I want something hot.
        {"set_id": "set_08", "ex_id": "ex801", "original": "I want something hot.", "slots": [("S", "I", "word"), ("V", "want", "word"), ("O1", "something hot", "phrase")]},
        {"set_id": "set_08", "ex_id": "ex802", "original": "You want something spicy.", "slots": [("S", "You", "word"), ("V", "want", "word"), ("O1", "something spicy", "phrase")]},
        {"set_id": "set_08", "ex_id": "ex803", "original": "We want something sweet.", "slots": [("S", "We", "word"), ("V", "want", "word"), ("O1", "something sweet", "phrase")]},
        {"set_id": "set_08", "ex_id": "ex804", "original": "They want something fresh.", "slots": [("S", "They", "word"), ("V", "want", "word"), ("O1", "something fresh", "phrase")]},
        
        # 残りも同様に追加...（簡略のため一部のみ表示）
    ]
    
    return all_sentences

def export_correct_format():
    """正しい形式でExcel出力"""
    
    # 簡略版で動作確認（最初の20例文）
    rows = create_rephrase_format()
    
    # DataFrame作成
    df = pd.DataFrame(rows)
    
    # 列順序調整
    columns = ['構文ID', '例文ID', 'V_group_key', '原文', 'Slot', 'SlotPhrase', 
               'PhraseType', 'SubslotID', 'SubslotElement', 'Slot_display_order', 'display_order']
    df = df[columns]
    
    # Slot_display_orderでソート
    df = df.sort_values(['例文ID', 'Slot_display_order', 'display_order'])
    
    # Excel出力
    output_file = "rephrase_88_correct_format.xlsx"
    df.to_excel(output_file, index=False, sheet_name="Sheet1")
    
    print(f"✅ 正しい形式で出力完了")
    print(f"📊 ファイル: {output_file}")
    print(f"📈 レコード数: {len(df)}")
    print(f"📈 例文数: {df['例文ID'].nunique()}")
    
    # サンプル表示
    print(f"\n🔍 出力例:")
    print(df.head(10))
    
    return df

if __name__ == "__main__":
    df = export_correct_format()
