#!/usr/bin/env python3
"""
正解データベースの内容を詳細確認
"""

import json

def analyze_expected_results():
    """正解データベースの構造を詳細分析"""
    print("🔍 正解データベースの詳細分析")
    
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("📊 全体構造:")
        print(f"  トップレベルキー: {list(data.keys())}")
        
        correct_answers = data.get('correct_answers', {})
        print(f"  correct_answers内の項目数: {len(correct_answers)}")
        print(f"  correct_answers内のキー: {list(correct_answers.keys())[:10]}...")
        
        print("\n📝 最初の5項目の詳細:")
        for i, (key, value) in enumerate(list(correct_answers.items())[:5], 1):
            print(f"\n--- 項目{i} (キー: {key}) ---")
            print(f"sentence: {value.get('sentence', 'なし')}")
            expected = value.get('expected', {})
            if expected:
                print(f"expected構造: {list(expected.keys())}")
                main_slots = expected.get('main_slots', {})
                sub_slots = expected.get('sub_slots', {})
                print(f"main_slots: {main_slots}")
                print(f"sub_slots: {sub_slots}")
            else:
                print("expectedデータなし")
                
        # キーと例文の対応を確認
        print("\n📋 キー番号と例文の対応関係:")
        for key in sorted(correct_answers.keys(), key=lambda x: int(x) if x.isdigit() else 999):
            sentence = correct_answers[key].get('sentence', '')
            print(f"  {key}: {sentence}")
            
    except FileNotFoundError:
        print("❌ expected_results_progress.json が見つかりません")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    analyze_expected_results()
