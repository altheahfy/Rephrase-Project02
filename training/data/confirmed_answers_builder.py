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

# 28番: 承認済み
db.add_confirmed_answer(
    28,
    "The problem was quickly solved by the expert team.",
    {
        "main_slots": {
            "S": "The problem",
            "Aux": "was",
            "V": "solved",
            "M2": "quickly",
            "M3": "by the expert team"
        },
        "sub_slots": {}
    },
    "passive_voice + adverbial_modifier (2ハンドラー連携)"
)

# 29番: 承認済み
db.add_confirmed_answer(
    29,
    "The house whose roof was damaged badly needs immediate repair.",
    {
        "main_slots": {
            "S": "",
            "V": "needs",
            "O1": "immediate repair"
        },
        "sub_slots": {
            "sub-s": "the house whose roof",
            "sub-aux": "was",
            "sub-v": "damaged",
            "sub-m2": "badly"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 30番: 承認済み（修正版）
db.add_confirmed_answer(
    30,
    "The place where we met accidentally became our favorite spot.",
    {
        "main_slots": {
            "S": "",
            "V": "became",
            "C1": "our favorite spot"
        },
        "sub_slots": {
            "sub-s": "we",
            "sub-v": "met",
            "sub-m1": "The place where",
            "sub-m2": "accidentally"
        }
    },
    "relative_clause + adverbial_modifier (2ハンドラー連携)"
)

# 31番: 承認済み
db.add_confirmed_answer(
    31,
    "The time when everything changed dramatically was unexpected.",
    {
        "main_slots": {
            "S": "",
            "Aux": "was",
            "V": "unexpected"
        },
        "sub_slots": {
            "sub-s": "everything",
            "sub-v": "changed",
            "sub-m1": "The time when",
            "sub-m2": "dramatically"
        }
    },
    "relative_clause + adverbial_modifier (2ハンドラー連携)"
)

# 41番: 承認済み
db.add_confirmed_answer(
    41,
    "The building is being constructed very carefully by skilled workers.",
    {
        "main_slots": {
            "S": "The building",
            "Aux": "is being",
            "V": "constructed",
            "M1": "very carefully",
            "M2": "by skilled workers"
        },
        "sub_slots": {}
    },
    "passive_voice + adverbial_modifier (2ハンドラー連携)"
)

# 45番: 承認済み
db.add_confirmed_answer(
    45,
    "The teacher explains grammar clearly to confused students daily.",
    {
        "main_slots": {
            "S": "The teacher",
            "V": "explains",
            "O1": "grammar",
            "M1": "clearly",
            "M2": "to confused students",
            "M3": "daily"
        },
        "sub_slots": {}
    },
    "basic_five_pattern + adverbial_modifier (2ハンドラー連携)"
)

# 46番: 承認済み（修正版）
db.add_confirmed_answer(
    46,
    "The student writes essays carefully for better grades.",
    {
        "main_slots": {
            "S": "The student",
            "V": "writes",
            "O1": "essays",
            "M2": "carefully",
            "M3": "for better grades"
        },
        "sub_slots": {}
    },
    "basic_five_pattern + adverbial_modifier (2ハンドラー連携)"
)

# 47番: 承認済み
db.add_confirmed_answer(
    47,
    "The report which was thoroughly reviewed by experts was published successfully.",
    {
        "main_slots": {
            "S": "",
            "Aux": "was",
            "V": "published",
            "M2": "successfully"
        },
        "sub_slots": {
            "sub-s": "The report which",
            "sub-aux": "was",
            "sub-v": "reviewed",
            "sub-m1": "thoroughly",
            "sub-m2": "by experts"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 48番: 承認済み
db.add_confirmed_answer(
    48,
    "The student whose essay was carefully corrected improved dramatically.",
    {
        "main_slots": {
            "S": "The student",
            "V": "improved",
            "Adv": "dramatically"
        },
        "sub_slots": {
            "sub-s": "whose essay",
            "sub-aux": "was",
            "sub-v": "corrected",
            "sub-m2": "carefully"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 49番: 承認済み
db.add_confirmed_answer(
    49,
    "The machine that was properly maintained works efficiently every day.",
    {
        "main_slots": {
            "S": "",
            "V": "works",
            "M2": "efficiently",
            "M3": "every day"
        },
        "sub_slots": {
            "sub-s": "the machine that",
            "sub-aux": "was",
            "sub-v": "maintained",
            "sub-m2": "properly"
        }
    },
    "relative_clause + passive_voice + adverbial_modifier (3ハンドラー連携)"
)

# 保存
db.save_to_file()

print("\n📊 進捗確認:")
print("✅ 承認済み: 18件")
print("⏳ 残り確認: 5件")
print("\n🎯 次の確認: 50番")
print("50番: 次の文を確認予定")
