#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係節ハンドラー単体テスト
"""

import json
from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
from basic_five_pattern_handler import BasicFivePatternHandler

# テストケースの設定
test_cases = [
    {
        "id": 3,
        "text": "The man who runs fast is strong.",
        "expected": "sub-sの関係詞節"
    },
    {
        "id": 4, 
        "text": "The book which lies there is mine.",
        "expected": "sub-sの関係詞節"
    },
    {
        "id": 5,
        "text": "The person that works here is kind.",
        "expected": "sub-sの関係詞節"
    }
]

# ハンドラーの初期化
adverb_handler = AdverbHandler()
five_pattern_handler = BasicFivePatternHandler()

collaborators = {
    'adverb': adverb_handler,
    'five_pattern': five_pattern_handler
}

rel_handler = RelativeClauseHandler(collaborators)

print("🔧 関係節ハンドラー単体テスト")
print("=" * 50)

for case in test_cases:
    print(f"\n📍 ケース {case['id']}: {case['text']}")
    print(f"期待: {case['expected']}")
    
    try:
        result = rel_handler.process(case['text'])
        print("✅ 処理成功")
        print(f"📊 結果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
