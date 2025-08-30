#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CentralControllerで関係節処理の統合テスト"""

import sys
import os
import json

# パスを追加して相対インポートを可能にする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ハンドラーをインポート
try:
    from central_controller import CentralController
    print("✅ CentralController インポート成功")
except ImportError as e:
    print(f"❌ CentralController インポートエラー: {e}")
    exit(1)

def test_failing_cases():
    """失敗しているケースを中央コントローラーでテスト"""
    
    controller = CentralController()
    
    # 失敗しているケース
    test_cases = [
        "The teacher whose class runs efficiently is respected greatly.",  # case_59
        "The report which was thoroughly reviewed by experts was published successfully."  # case_62
    ]
    
    print("=" * 60)
    print("CentralController 関係節統合テスト")
    print("=" * 60)
    
    for i, case in enumerate([59, 62]):
        text = test_cases[i]
        print(f"\n🔍 Case {case}: {text}")
        try:
            result = controller.process_sentence(text)
            
            # 結果の詳細チェック
            if result.get('success') == True:
                print(f"✅ 成功")
                print(f"📊 main_slots: {result.get('main_slots', {})}")
                print(f"📊 sub_slots: {result.get('sub_slots', {})}")
            elif result.get('success') == False:
                print(f"❌ 失敗: {result.get('error', 'Unknown error')}")
            else:
                print(f"⚠️ 異常な結果タイプ: {type(result.get('success'))}")
                print(f"結果全体: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
        except Exception as e:
            print(f"❌ 例外発生: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_failing_cases()
