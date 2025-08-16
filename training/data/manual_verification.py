#!/usr/bin/env python3
"""
正解データベース検証スクリプト - システム出力との比較
"""
import json
from typing import Dict, Any

def load_expected_results() -> Dict[str, Any]:
    """正解データベース読み込み"""
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('correct_answers', {})
    except Exception as e:
        print(f"❌ 正解データベース読み込みエラー: {e}")
        return {}

def compare_results(system_output: Dict, expected: Dict, sentence_num: int, sentence: str) -> bool:
    """結果比較"""
    print(f"\n📝 例文{sentence_num}: {sentence}")
    
    # システム出力のスロット取得
    system_slots = system_output.get('slots', {})
    system_sub_slots = system_output.get('sub_slots', {})
    
    # 正解データのスロット取得  
    expected_main = expected.get('main_slots', {})
    expected_sub = expected.get('sub_slots', {})
    
    print(f"🤖 システム出力:")
    print(f"   メイン: {system_slots}")
    print(f"   サブ  : {system_sub_slots}")
    
    print(f"✅ 正解データ:")
    print(f"   メイン: {expected_main}")
    print(f"   サブ  : {expected_sub}")
    
    # 比較
    main_match = system_slots == expected_main
    sub_match = system_sub_slots == expected_sub
    
    overall_match = main_match and sub_match
    
    if overall_match:
        print("🎉 完全一致！")
    else:
        print("⚠️ 不一致:")
        if not main_match:
            print(f"   メインスロット不一致")
        if not sub_match:
            print(f"   サブスロット不一致")
    
    return overall_match

def manual_verification():
    """手動検証用データ入力"""
    expected_results = load_expected_results()
    
    if not expected_results:
        print("❌ 正解データが見つかりません")
        return
    
    print("🔍 手動検証モード")
    print("システムの出力結果を入力して正解データと比較します\n")
    
    # 例文1のテスト
    sentence_num = 1
    if str(sentence_num) in expected_results:
        expected_data = expected_results[str(sentence_num)]['expected']
        sentence = expected_results[str(sentence_num)]['sentence']
        
        print(f"例文{sentence_num}: {sentence}")
        print("システム出力のメインスロットを入力してください（JSON形式）:")
        
        # 手動入力例（実際のシステム出力で置き換え）
        # 例: {"S": "I", "V": "love", "O1": "you"}
        system_example = {"S": "I", "V": "love", "O1": "you"}
        
        mock_system_output = {
            'slots': system_example,
            'sub_slots': {}
        }
        
        compare_results(mock_system_output, expected_data, sentence_num, sentence)

if __name__ == "__main__":
    manual_verification()
