#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
54例文正解データ蓄積ファイル
ユーザー判定による正解想定の記録・管理
"""

import json
from datetime import datetime

# 54例文リスト（custom_test.pyより）
SENTENCES = [
    "I love you.",
    "She reads books.",
    "The cat sleeps.",
    "He gives me a book.",
    "I find it interesting.",
    "The book is good.",
    "The person that works here is kind.",
    "The car which was parked outside is mine.",
    "The house where I was born is old.",
    "The day when we met was sunny.",
    "The reason why he left is unclear.",
    "The man whose car was stolen called the police.",
    "I know the person that you mentioned.",
    "The book which I read was fascinating.",
    "The place where we lived was peaceful.",
    "The time when you called was perfect.",
    "The woman whose idea won the contest is my sister.",
    "I like the movie that you recommended.",
    "The restaurant where we ate was expensive.",
    "The moment when I realized the truth was shocking.",
    "I am running quickly to catch the bus.",
    "She sings beautifully at the concert.",
    "The dog barks loudly in the yard.",
    "He works diligently on his project.",
    "They dance gracefully at the party.",
    "I eat breakfast every morning.",
    "She studies English twice a week.",
    "He visits his grandmother on Sundays.",
    "We go to the beach in summer.",
    "They play tennis after school.",
    "The window was broken.",
    "She is going to visit Paris next month.",
    "He has finished his homework.",
    "The letter was written by John.",
    "The house was built in 1990.",
    "The book was written by a famous author.",
    "The cake is being baked by my mother.",
    "The cake was eaten by the children.",
    "The door was opened by the key.",
    "The message was sent yesterday.",
    "If it rains, I stay home.",
    "She acts as if she knows everything.",
    "The students study hard for exams.",
    "The car was repaired last week.",
    "The book was published in 2020.",
    "I went to the store and bought some milk.",
    "She was tired, but she continued working.",
    "Although it was raining, we went for a walk.",
    "Because he was late, he missed the train.",
    "The room was cleaned this morning.",
    "The man who is standing there is my father.",
    "The girl whom I met yesterday is very smart.",
    "The house that we visited last week is for sale.",
    "The teacher whose class I attended was excellent."
]

# 正解データ構造
EXPECTED_RESULTS = {
    # 進捗管理
    "meta": {
        "last_updated": "",
        "current_sentence": 1,
        "total_sentences": len(SENTENCES),
        "completion_status": "in_progress",
        "session_notes": []
    },
    
    # 正解想定データ
    "correct_answers": {
        # 例: 
        # "1": {
        #     "sentence": "I love you.",
        #     "expected": {
        #         "main_slots": {"S": "I", "V": "love", "O1": "you"},
        #         "sub_slots": {}
        #     },
        #     "ai_prediction": {...},
        #     "user_judgment": "correct" | "incorrect",
        #     "corrections": {...},
        #     "notes": "..."
        # }
    },
    
    # 学習パターン
    "learned_patterns": {
        "basic_sentence_types": {},
        "relative_clauses": {},
        "slot_emptying_rules": {},
        "sub_slot_patterns": {}
    }
}

def save_progress(data):
    """進捗をファイルに保存"""
    data["meta"]["last_updated"] = datetime.now().isoformat()
    
    with open("expected_results_progress.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 進捗保存完了: {data['meta']['current_sentence']}/{data['meta']['total_sentences']}")

def load_progress():
    """保存された進捗を読み込み"""
    try:
        with open("expected_results_progress.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return EXPECTED_RESULTS.copy()

def add_result(sentence_num, ai_prediction, user_judgment, corrections=None, notes=""):
    """正解データを追加"""
    data = load_progress()
    
    sentence_key = str(sentence_num)
    data["correct_answers"][sentence_key] = {
        "sentence": SENTENCES[sentence_num - 1],
        "ai_prediction": ai_prediction,
        "user_judgment": user_judgment,
        "corrections": corrections or {},
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }
    
    # 正解版を確定
    if user_judgment == "correct":
        data["correct_answers"][sentence_key]["expected"] = ai_prediction
    else:
        data["correct_answers"][sentence_key]["expected"] = corrections
    
    # 進捗更新
    data["meta"]["current_sentence"] = max(data["meta"]["current_sentence"], sentence_num + 1)
    
    save_progress(data)
    return data

def get_current_sentence():
    """現在処理すべき例文を取得"""
    data = load_progress()
    current = data["meta"]["current_sentence"]
    
    if current <= len(SENTENCES):
        return current, SENTENCES[current - 1]
    else:
        return None, "全例文完了"

def display_progress():
    """進捗状況を表示"""
    data = load_progress()
    current = data["meta"]["current_sentence"]
    total = data["meta"]["total_sentences"]
    
    print(f"🔢 進捗状況: {current-1}/{total} 例文完了")
    print(f"📝 次の例文: {current}. {SENTENCES[current-1] if current <= total else '完了'}")
    
    # 完了済み例文一覧
    completed = [int(k) for k in data["correct_answers"].keys()]
    if completed:
        print(f"✅ 完了済み: {sorted(completed)}")

if __name__ == "__main__":
    print("📋 54例文正解データ蓄積システム")
    print("=" * 50)
    display_progress()
