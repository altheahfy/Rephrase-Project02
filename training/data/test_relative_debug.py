#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""RelativeClauseHandlerのテスト実行"""

import sys
import os
import json

# パスを追加して相対インポートを可能にする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ハンドラーをインポート
try:
    from relative_clause_handler import RelativeClauseHandler
    print("✅ RelativeClauseHandler インポート成功")
except ImportError as e:
    print(f"❌ RelativeClauseHandler インポートエラー: {e}")
    exit(1)

def test_failing_cases():
    """失敗しているケースをテスト"""
    
    # 協力者なしでテスト
    handler = RelativeClauseHandler()
    
    # 失敗しているケース
    test_cases = [
        "The teacher whose class runs efficiently is respected greatly.",  # case_59
        "The report which was thoroughly reviewed by experts was published successfully."  # case_62
    ]
    
    print("=" * 60)
    print("RelativeClauseHandler 失敗ケーステスト")
    print("=" * 60)
    
    for i, case in enumerate(test_cases, 59):
        print(f"\n🔍 Case {i}: {case}")
        try:
            result = handler.process(case)
            print(f"結果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"❌ 例外発生: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_failing_cases()
