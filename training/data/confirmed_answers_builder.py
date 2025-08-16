#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
確認済み正解データベース構築
4ハンドラー完全性テスト用
"""

import json
import codecs
from datetime import datetime

class ConfirmedAnswerDatabase:
    def __init__(self):
        self.confirmed_data = {}
        
    def add_confirmed_answer(self, test_id, sentence, expected_result, notes=""):
        """確認済み正解データを追加"""
        self.confirmed_data[str(test_id)] = {
            "sentence": sentence,
            "expected": expected_result,
            "notes": notes,
            "confirmed_at": datetime.now().isoformat(),
            "user_judgment": "correct"
        }
        print(f"✅ {test_id}番 保存完了: {sentence}")
    
    def save_to_file(self):
        """ファイルに保存"""
        output_data = {
            "meta": {
                "created_at": datetime.now().isoformat(),
                "total_entries": len(self.confirmed_data),
                "purpose": "4ハンドラー完全性テスト用確認済み正解データ"
            },
            "correct_answers": self.confirmed_data
        }
        
        with codecs.open('confirmed_correct_answers.json', 'w', 'utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 確認済みデータ保存完了: {len(self.confirmed_data)}件")

# グローバルデータベースインスタンス
db = ConfirmedAnswerDatabase()

# 20番: 承認済み
db.add_confirmed_answer(
    20,
    "The book which was carefully written by Shakespeare is famous.",
    {
        "main_slots": {
            "S": "",
            "V": "is", 
            "C1": "famous"
        },
        "sub_slots": {
            "sub-s": "The book which",
            "sub-v": "written",
            "sub-aux": "was",
            "sub-m1": "carefully",
            "sub-m2": "by Shakespeare"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 21番: 承認済み
db.add_confirmed_answer(
    21,
    "The car that was quickly repaired yesterday runs smoothly.",
    {
        "main_slots": {
            "S": "",
            "V": "runs", 
            "M1": "smoothly"
        },
        "sub_slots": {
            "sub-s": "The car that",
            "sub-v": "repaired",
            "sub-aux": "was",
            "sub-m1": "quickly",
            "sub-m2": "yesterday"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 32番: 承認済み
db.add_confirmed_answer(
    32,
    "The letter which was slowly typed by the secretary arrived today.",
    {
        "main_slots": {
            "S": "",
            "V": "arrived", 
            "M2": "today"
        },
        "sub_slots": {
            "sub-s": "The letter which",
            "sub-v": "typed",
            "sub-aux": "was",
            "sub-m1": "slowly",
            "sub-m2": "by the secretary"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 23番: 承認済み
db.add_confirmed_answer(
    23,
    "The student who studies diligently always succeeds academically.",
    {
        "main_slots": {
            "S": "",
            "V": "succeeds", 
            "M1": "always",
            "M2": "academically"
        },
        "sub_slots": {
            "sub-s": "The student who",
            "sub-v": "studies",
            "sub-m1": "diligently"
        }
    },
    "relative_clause + adverbial_modifier (2ハンドラー連携)"
)

# 24番: 承認済み
db.add_confirmed_answer(
    24,
    "The teacher whose class runs efficiently is respected greatly.",
    {
        "main_slots": {
            "S": "",
            "Aux": "is",
            "V": "respected",
            "M2": "greatly"
        },
        "sub_slots": {
            "sub-s": "The teacher whose",
            "sub-c1": "class",
            "sub-v": "runs",
            "sub-m2": "efficiently"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 25番: 承認済み
db.add_confirmed_answer(
    25,
    "The doctor who works carefully saves lives successfully.",
    {
        "main_slots": {
            "S": "",
            "V": "saves",
            "O1": "lives",
            "M2": "successfully"
        },
        "sub_slots": {
            "sub-s": "The doctor who",
            "sub-v": "works",
            "sub-m2": "carefully"
        }
    },
    "relative_clause + adverbial_modifier (2ハンドラー連携)"
)

# 26番: 承認済み
db.add_confirmed_answer(
    26,
    "The window was gently opened by the morning breeze.",
    {
        "main_slots": {
            "S": "The window",
            "Aux": "was",
            "V": "opened",
            "M1": "gently",
            "M2": "by the morning breeze"
        },
        "sub_slots": {}
    },
    "passive_voice + adverbial_modifier (2ハンドラー連携)"
)

# 27番: 承認済み
db.add_confirmed_answer(
    27,
    "The message is being carefully written by the manager.",
    {
        "main_slots": {
            "S": "The message",
            "Aux": "is being",
            "V": "written",
            "M1": "carefully",
            "M2": "by the manager"
        },
        "sub_slots": {}
    },
    "passive_voice + adverbial_modifier (2ハンドラー連携)"
)

# 保存
db.save_to_file()

print("\n🎯 次の確認: 28番")
print("28番: 'The problem was quickly solved by the expert team.'")
