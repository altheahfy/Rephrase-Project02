"""
Rephrase 88例文の文要素分解結果
rephrase_rules_v1.0.json に基づく分解
"""

import pandas as pd

def create_parsed_data():
    """88例文の文要素分解データを作成"""
    
    # 文要素分解結果
    parsed_data = [
        # セット1: I lie on the bed/couch
        {"set_id": "set_01", "sentence_id": "set_01_01", "original": "I lie on the bed.", "S": "I", "Aux": "", "V": "lie", "O1": "", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "on the bed"},
        {"set_id": "set_01", "sentence_id": "set_01_02", "original": "You lie on the sofa.", "S": "You", "Aux": "", "V": "lie", "O1": "", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "on the sofa"},
        {"set_id": "set_01", "sentence_id": "set_01_03", "original": "We lie on the floor.", "S": "We", "Aux": "", "V": "lie", "O1": "", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "on the floor"},
        {"set_id": "set_01", "sentence_id": "set_01_04", "original": "They lie on the couch.", "S": "They", "Aux": "", "V": "lie", "O1": "", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "on the couch"},
        
        # セット2: You got me!
        {"set_id": "set_02", "sentence_id": "set_02_01", "original": "You got me!", "S": "You", "Aux": "", "V": "got", "O1": "me", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_02", "sentence_id": "set_02_02", "original": "I got him!", "S": "I", "Aux": "", "V": "got", "O1": "him", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_02", "sentence_id": "set_02_03", "original": "He got them!", "S": "He", "Aux": "", "V": "got", "O1": "them", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_02", "sentence_id": "set_02_04", "original": "We got Mark!", "S": "We", "Aux": "", "V": "got", "O1": "Mark", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット3: Where did you get it?
        {"set_id": "set_03", "sentence_id": "set_03_01", "original": "Where did you get it?", "S": "you", "Aux": "did", "V": "get", "O1": "it", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "Where"},
        {"set_id": "set_03", "sentence_id": "set_03_02", "original": "Where did I get the device?", "S": "I", "Aux": "did", "V": "get", "O1": "the device", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "Where"},
        {"set_id": "set_03", "sentence_id": "set_03_03", "original": "Where did she get the book?", "S": "she", "Aux": "did", "V": "get", "O1": "the book", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "Where"},
        {"set_id": "set_03", "sentence_id": "set_03_04", "original": "Where did they get the information?", "S": "they", "Aux": "did", "V": "get", "O1": "the information", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "Where"},
        
        # セット4: You, give it to me straight. (命令文)
        {"set_id": "set_04", "sentence_id": "set_04_01", "original": "You, give it to me straight.", "S": "You", "Aux": "", "V": "give", "O1": "it", "O2": "me", "C1": "", "C2": "", "M1": "", "M2": "straight", "M3": ""},
        {"set_id": "set_04", "sentence_id": "set_04_02", "original": "You, give that to him clearly.", "S": "You", "Aux": "", "V": "give", "O1": "that", "O2": "him", "C1": "", "C2": "", "M1": "", "M2": "clearly", "M3": ""},
        {"set_id": "set_04", "sentence_id": "set_04_03", "original": "You, give this to her honestly.", "S": "You", "Aux": "", "V": "give", "O1": "this", "O2": "her", "C1": "", "C2": "", "M1": "", "M2": "honestly", "M3": ""},
        {"set_id": "set_04", "sentence_id": "set_04_04", "original": "You, give them to us directly.", "S": "You", "Aux": "", "V": "give", "O1": "them", "O2": "us", "C1": "", "C2": "", "M1": "", "M2": "directly", "M3": ""},
        
        # セット5: That reminds me.
        {"set_id": "set_05", "sentence_id": "set_05_01", "original": "That reminds me.", "S": "That", "Aux": "", "V": "reminds", "O1": "me", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_05", "sentence_id": "set_05_02", "original": "This reminds you.", "S": "This", "Aux": "", "V": "reminds", "O1": "you", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_05", "sentence_id": "set_05_03", "original": "It reminds her.", "S": "It", "Aux": "", "V": "reminds", "O1": "her", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_05", "sentence_id": "set_05_04", "original": "Everything reminds them.", "S": "Everything", "Aux": "", "V": "reminds", "O1": "them", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット6: Would you hold the line, please?
        {"set_id": "set_06", "sentence_id": "set_06_01", "original": "Would you hold the line, please?", "S": "you", "Aux": "Would", "V": "hold", "O1": "the line", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "please", "M3": ""},
        {"set_id": "set_06", "sentence_id": "set_06_02", "original": "Would I hold the call, please?", "S": "I", "Aux": "Would", "V": "hold", "O1": "the call", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "please", "M3": ""},
        {"set_id": "set_06", "sentence_id": "set_06_03", "original": "Would she hold the phone, please?", "S": "she", "Aux": "Would", "V": "hold", "O1": "the phone", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "please", "M3": ""},
        {"set_id": "set_06", "sentence_id": "set_06_04", "original": "Would they hold the connection, please?", "S": "they", "Aux": "Would", "V": "hold", "O1": "the connection", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "please", "M3": ""},
        
        # セット7: I haven't seen you for a long time.
        {"set_id": "set_07", "sentence_id": "set_07_01", "original": "I haven't seen you for a long time.", "S": "I", "Aux": "haven't", "V": "seen", "O1": "you", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for a long time"},
        {"set_id": "set_07", "sentence_id": "set_07_02", "original": "You haven't seen me for ages.", "S": "You", "Aux": "haven't", "V": "seen", "O1": "me", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for ages"},
        {"set_id": "set_07", "sentence_id": "set_07_03", "original": "We haven't seen Ken for months.", "S": "We", "Aux": "haven't", "V": "seen", "O1": "Ken", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for months"},
        {"set_id": "set_07", "sentence_id": "set_07_04", "original": "They haven't seen him for years.", "S": "They", "Aux": "haven't", "V": "seen", "O1": "him", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for years"},
        
        # セット8: I want something hot.
        {"set_id": "set_08", "sentence_id": "set_08_01", "original": "I want something hot.", "S": "I", "Aux": "", "V": "want", "O1": "something hot", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_08", "sentence_id": "set_08_02", "original": "You want something spicy.", "S": "You", "Aux": "", "V": "want", "O1": "something spicy", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_08", "sentence_id": "set_08_03", "original": "We want something sweet.", "S": "We", "Aux": "", "V": "want", "O1": "something sweet", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_08", "sentence_id": "set_08_04", "original": "They want something fresh.", "S": "They", "Aux": "", "V": "want", "O1": "something fresh", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット9: Could you write it down, please?
        {"set_id": "set_09", "sentence_id": "set_09_01", "original": "Could you write it down, please?", "S": "you", "Aux": "Could", "V": "write", "O1": "it", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "down", "M3": "please"},
        {"set_id": "set_09", "sentence_id": "set_09_02", "original": "Could I write the sentence down, please?", "S": "I", "Aux": "Could", "V": "write", "O1": "the sentence", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "down", "M3": "please"},
        {"set_id": "set_09", "sentence_id": "set_09_03", "original": "Could she write the address down, please?", "S": "she", "Aux": "Could", "V": "write", "O1": "the address", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "down", "M3": "please"},
        {"set_id": "set_09", "sentence_id": "set_09_04", "original": "Could they write the number down, please?", "S": "they", "Aux": "Could", "V": "write", "O1": "the number", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "down", "M3": "please"},
        
        # セット10: I can't afford it.
        {"set_id": "set_10", "sentence_id": "set_10_01", "original": "I can't afford it.", "S": "I", "Aux": "can't", "V": "afford", "O1": "it", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_10", "sentence_id": "set_10_02", "original": "You can't afford the jacket.", "S": "You", "Aux": "can't", "V": "afford", "O1": "the jacket", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_10", "sentence_id": "set_10_03", "original": "She can't afford the car.", "S": "She", "Aux": "can't", "V": "afford", "O1": "the car", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_10", "sentence_id": "set_10_04", "original": "They can't afford the house.", "S": "They", "Aux": "can't", "V": "afford", "O1": "the house", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット11: I believe you.
        {"set_id": "set_11", "sentence_id": "set_11_01", "original": "I believe you.", "S": "I", "Aux": "", "V": "believe", "O1": "you", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_11", "sentence_id": "set_11_02", "original": "You believe Tom.", "S": "You", "Aux": "", "V": "believe", "O1": "Tom", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_11", "sentence_id": "set_11_03", "original": "We believe her.", "S": "We", "Aux": "", "V": "believe", "O1": "her", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_11", "sentence_id": "set_11_04", "original": "They believe him.", "S": "They", "Aux": "", "V": "believe", "O1": "him", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット12: Henry mentioned the fact.
        {"set_id": "set_12", "sentence_id": "set_12_01", "original": "Henry mentioned the fact.", "S": "Henry", "Aux": "", "V": "mentioned", "O1": "the fact", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_12", "sentence_id": "set_12_02", "original": "Sarah mentioned the issue.", "S": "Sarah", "Aux": "", "V": "mentioned", "O1": "the issue", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_12", "sentence_id": "set_12_03", "original": "Tom mentioned the problem.", "S": "Tom", "Aux": "", "V": "mentioned", "O1": "the problem", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_12", "sentence_id": "set_12_04", "original": "They mentioned the concern.", "S": "They", "Aux": "", "V": "mentioned", "O1": "the concern", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット13: He entered her room.
        {"set_id": "set_13", "sentence_id": "set_13_01", "original": "He entered her room.", "S": "He", "Aux": "", "V": "entered", "O1": "her room", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_13", "sentence_id": "set_13_02", "original": "She entered his office.", "S": "She", "Aux": "", "V": "entered", "O1": "his office", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_13", "sentence_id": "set_13_03", "original": "Tom entered Sarah's house.", "S": "Tom", "Aux": "", "V": "entered", "O1": "Sarah's house", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_13", "sentence_id": "set_13_04", "original": "They entered the building.", "S": "They", "Aux": "", "V": "entered", "O1": "the building", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット14: He left New York a few days ago.
        {"set_id": "set_14", "sentence_id": "set_14_01", "original": "He left New York a few days ago.", "S": "He", "Aux": "", "V": "left", "O1": "New York", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "a few days ago"},
        {"set_id": "set_14", "sentence_id": "set_14_02", "original": "She left Rome last week.", "S": "She", "Aux": "", "V": "left", "O1": "Rome", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "last week"},
        {"set_id": "set_14", "sentence_id": "set_14_03", "original": "Tom left Paris yesterday.", "S": "Tom", "Aux": "", "V": "left", "O1": "Paris", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "yesterday"},
        {"set_id": "set_14", "sentence_id": "set_14_04", "original": "They left London this morning.", "S": "They", "Aux": "", "V": "left", "O1": "London", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "this morning"},
        
        # セット15: He reached Boston the next morning.
        {"set_id": "set_15", "sentence_id": "set_15_01", "original": "He reached Boston the next morning.", "S": "He", "Aux": "", "V": "reached", "O1": "Boston", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "the next morning"},
        {"set_id": "set_15", "sentence_id": "set_15_02", "original": "She reached Milan that evening.", "S": "She", "Aux": "", "V": "reached", "O1": "Milan", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "that evening"},
        {"set_id": "set_15", "sentence_id": "set_15_03", "original": "Tom reached Tokyo at noon.", "S": "Tom", "Aux": "", "V": "reached", "O1": "Tokyo", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "at noon"},
        {"set_id": "set_15", "sentence_id": "set_15_04", "original": "They reached Berlin at midnight.", "S": "They", "Aux": "", "V": "reached", "O1": "Berlin", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "at midnight"},
        
        # セット16: I approach Tokyo.
        {"set_id": "set_16", "sentence_id": "set_16_01", "original": "I approach Tokyo.", "S": "I", "Aux": "", "V": "approach", "O1": "Tokyo", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_16", "sentence_id": "set_16_02", "original": "You approach the station.", "S": "You", "Aux": "", "V": "approach", "O1": "the station", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_16", "sentence_id": "set_16_03", "original": "We approach the building.", "S": "We", "Aux": "", "V": "approach", "O1": "the building", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_16", "sentence_id": "set_16_04", "original": "They approach the destination.", "S": "They", "Aux": "", "V": "approach", "O1": "the destination", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット17: He resembles his mother.
        {"set_id": "set_17", "sentence_id": "set_17_01", "original": "He resembles his mother.", "S": "He", "Aux": "", "V": "resembles", "O1": "his mother", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_17", "sentence_id": "set_17_02", "original": "She resembles her father.", "S": "She", "Aux": "", "V": "resembles", "O1": "her father", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_17", "sentence_id": "set_17_03", "original": "Tom resembles his uncle.", "S": "Tom", "Aux": "", "V": "resembles", "O1": "his uncle", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_17", "sentence_id": "set_17_04", "original": "They resemble their parents.", "S": "They", "Aux": "", "V": "resemble", "O1": "their parents", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット18: She married a bald man.
        {"set_id": "set_18", "sentence_id": "set_18_01", "original": "She married a bald man.", "S": "She", "Aux": "", "V": "married", "O1": "a bald man", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_18", "sentence_id": "set_18_02", "original": "He married a quiet woman.", "S": "He", "Aux": "", "V": "married", "O1": "a quiet woman", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_18", "sentence_id": "set_18_03", "original": "Sarah married a kind person.", "S": "Sarah", "Aux": "", "V": "married", "O1": "a kind person", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_18", "sentence_id": "set_18_04", "original": "They married their partners.", "S": "They", "Aux": "", "V": "married", "O1": "their partners", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット19: She got married with a bald man.
        {"set_id": "set_19", "sentence_id": "set_19_01", "original": "She got married with a bald man.", "S": "She", "Aux": "", "V": "got married with", "O1": "a bald man", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_19", "sentence_id": "set_19_02", "original": "He got married with a kind woman.", "S": "He", "Aux": "", "V": "got married with", "O1": "a kind woman", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_19", "sentence_id": "set_19_03", "original": "Sarah got married with a nice person.", "S": "Sarah", "Aux": "", "V": "got married with", "O1": "a nice person", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_19", "sentence_id": "set_19_04", "original": "Tom got married with a lovely partner.", "S": "Tom", "Aux": "", "V": "got married with", "O1": "a lovely partner", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        
        # セット20: She's been married to a bald man for 5 years.
        {"set_id": "set_20", "sentence_id": "set_20_01", "original": "She's been married to a bald man for 5 years.", "S": "She", "Aux": "has been", "V": "married to", "O1": "a bald man", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for 5 years"},
        {"set_id": "set_20", "sentence_id": "set_20_02", "original": "He's been married to a kind woman for 3 years.", "S": "He", "Aux": "has been", "V": "married to", "O1": "a kind woman", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for 3 years"},
        {"set_id": "set_20", "sentence_id": "set_20_03", "original": "Sarah's been married to a nice person for 2 years.", "S": "Sarah", "Aux": "has been", "V": "married to", "O1": "a nice person", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for 2 years"},
        {"set_id": "set_20", "sentence_id": "set_20_04", "original": "Tom's been married to a lovely partner for 10 years.", "S": "Tom", "Aux": "has been", "V": "married to", "O1": "a lovely partner", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "for 10 years"},
        
        # セット21: He'll answer your letter soon.
        {"set_id": "set_21", "sentence_id": "set_21_01", "original": "He'll answer your letter soon.", "S": "He", "Aux": "will", "V": "answer", "O1": "your letter", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "soon"},
        {"set_id": "set_21", "sentence_id": "set_21_02", "original": "She'll answer his message tomorrow.", "S": "She", "Aux": "will", "V": "answer", "O1": "his message", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "tomorrow"},
        {"set_id": "set_21", "sentence_id": "set_21_03", "original": "Tom'll answer the email later.", "S": "Tom", "Aux": "will", "V": "answer", "O1": "the email", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "later"},
        {"set_id": "set_21", "sentence_id": "set_21_04", "original": "They'll answer our call tonight.", "S": "They", "Aux": "will", "V": "answer", "O1": "our call", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": "tonight"},
        
        # セット22: We discuss our schedule.
        {"set_id": "set_22", "sentence_id": "set_22_01", "original": "We discuss our schedule.", "S": "We", "Aux": "", "V": "discuss", "O1": "our schedule", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_22", "sentence_id": "set_22_02", "original": "You discuss your project.", "S": "You", "Aux": "", "V": "discuss", "O1": "your project", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_22", "sentence_id": "set_22_03", "original": "They discuss their plan.", "S": "They", "Aux": "", "V": "discuss", "O1": "their plan", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
        {"set_id": "set_22", "sentence_id": "set_22_04", "original": "I discuss my proposal.", "S": "I", "Aux": "", "V": "discuss", "O1": "my proposal", "O2": "", "C1": "", "C2": "", "M1": "", "M2": "", "M3": ""},
    ]
    
    return parsed_data

def export_to_excel():
    """Excel形式で出力"""
    data = create_parsed_data()
    df = pd.DataFrame(data)
    
    # 列順序
    columns = ["set_id", "sentence_id", "original", "S", "Aux", "V", "O1", "O2", "C1", "C2", "M1", "M2", "M3"]
    df = df[columns]
    
    # Excel出力
    output_file = "rephrase_88_sentences_parsed.xlsx"
    df.to_excel(output_file, index=False, sheet_name="Rephrase文要素分解")
    
    print(f"✅ 完了: {len(data)}文を文要素分解")
    print(f"📊 出力ファイル: {output_file}")
    
    # 統計情報
    print(f"\n📈 統計:")
    print(f"- 総例文数: {len(data)}")
    print(f"- セット数: {df['set_id'].nunique()}")
    print(f"- 平均語彙数: {df['original'].str.split().str.len().mean():.1f}語")
    
    # サンプル表示
    print(f"\n🔍 分解例:")
    for i in range(3):
        row = data[i]
        print(f"\n例文: {row['original']}")
        for slot in ["S", "Aux", "V", "O1", "O2", "M1", "M2", "M3"]:
            if row[slot]:
                print(f"  {slot}: {row[slot]}")
    
    return df

if __name__ == "__main__":
    df = export_to_excel()
