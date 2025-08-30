#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PassiveVoiceHandlerのテスト実行"""

import sys
import os
import json

# パスを追加して相対インポートを可能にする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ハンドラーをインポート
try:
    from passive_voice_handler import PassiveVoiceHandler
    print("✅ PassiveVoiceHandler インポート成功")
except ImportError as e:
    print(f"❌ PassiveVoiceHandler インポートエラー: {e}")
    exit(1)

def test_passive_handler():
    """受動態ハンドラーをテスト"""
    
    handler = PassiveVoiceHandler()
    
    # 問題が起きている簡略文をテスト
    test_cases = [
        "The teacher is respected greatly .",
        "The report was published successfully .",
    ]
    
    print("=" * 60)
    print("PassiveVoiceHandler テスト")
    print("=" * 60)
    
    for i, case in enumerate(test_cases):
        print(f"\n🔍 Test {i+1}: {case}")
        try:
            result = handler.process(case)
            print(f"結果タイプ: {type(result)}")
            print(f"結果: {result}")
        except Exception as e:
            print(f"❌ 例外発生: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_passive_handler()
