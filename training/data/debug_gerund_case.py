#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
動名詞ケース専用デバッグテスト
どのハンドラーが先に処理しているかを詳細分析
"""

import json
import sys
sys.path.append('.')

from true_central_controller import TrueCentralController

def test_specific_gerund_case():
    """特定の動名詞ケースのデバッグ"""
    
    # 中央管理システム初期化
    controller = TrueCentralController()
    
    # テストケース: 171番 (主語動名詞)
    sentence = "Swimming is fun."
    v_group_key = "gerund_subject"
    
    print(f"=== デバッグテスト: '{sentence}' ===")
    print(f"V_group_key: {v_group_key}")
    
    # ハンドラー段階別に処理を追跡
    try:
        result = controller.process_sentence(sentence, v_group_key)
        print(f"最終結果: {result}")
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_specific_gerund_case()
