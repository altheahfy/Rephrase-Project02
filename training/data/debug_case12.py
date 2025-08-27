#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spaCy誤判定対処法テスト：ケース12専用
"""

import json
from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
from basic_five_pattern_handler import BasicFivePatternHandler

# spaCy誤判定ケース
test_case = {
    "id": 12,
    "text": "The man whose car is red lives here.",
    "expected": "spaCy誤判定対処要"
}

# ハンドラーの初期化
adverb_handler = AdverbHandler()
five_pattern_handler = BasicFivePatternHandler()

collaborators = {
    'adverb': adverb_handler,
    'five_pattern': five_pattern_handler
}

rel_handler = RelativeClauseHandler(collaborators)

print(f"🔧 spaCy誤判定対処テスト: ケース {test_case['id']}")
print("=" * 60)
print(f"📝 例文: {test_case['text']}")
print(f"期待: {test_case['expected']}")

try:
    result = rel_handler.process(test_case['text'])
    print("✅ 処理成功")
    print(f"📊 結果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 特に main_continuation を確認
    main_continuation = result.get('main_continuation', '')
    if 'here' in main_continuation:
        print(f"✅ main_continuation に 'here' が含まれている: '{main_continuation}'")
    else:
        print(f"❌ main_continuation に 'here' が含まれていない: '{main_continuation}'")
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()
