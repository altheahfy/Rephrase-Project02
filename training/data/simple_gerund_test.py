#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
動名詞ハンドラー単体テスト - 単純版
"""

import sys
sys.path.append('.')

from gerund_handler import GerundHandler

def test_single_gerund():
    """動名詞ハンドラーの基本テスト"""
    
    print("=== 動名詞ハンドラー単体テスト ===")
    
    # ハンドラー初期化
    handler = GerundHandler()
    
    # シンプルなテストケース
    test_cases = [
        "Swimming is fun.",  # 主語動名詞
        "I enjoy reading.",  # 目的語動名詞
        "I'm interested in learning.",  # 前置詞+動名詞
    ]
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n--- テスト {i}: {sentence} ---")
        
        # can_handle テスト
        can_handle = handler.can_handle(sentence)
        print(f"can_handle: {can_handle}")
        
        if can_handle:
            # handle テスト
            try:
                result = handler.handle(sentence, "test_gerund")
                print(f"handle結果:")
                print(f"  main_slots: {result.get('main_slots', {})}")
                print(f"  sub_slots: {result.get('sub_slots', {})}")
            except Exception as e:
                print(f"handle エラー: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ can_handleでFalse判定")

if __name__ == "__main__":
    test_single_gerund()
