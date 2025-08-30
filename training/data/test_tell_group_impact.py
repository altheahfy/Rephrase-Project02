#!/usr/bin/env python3
"""
tellグループへの影響確認テスト
人間的判断ロジック適用後のtellグループ処理をテスト
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adverb_position_analyzer import AdverbPositionAnalyzer

def test_tell_group_impact():
    """tellグループへの影響をテスト"""
    print("🚀 tellグループへの影響確認テスト")
    print("=" * 60)
    
    # tellグループのテストデータ
    tell_data = [
        {
            "sentence": "What did he tell her at the store?",
            "slots": {"S": "he", "V": "tell", "O1": "her", "O2": "What", "M2": "at the store"}
        },
        {
            "sentence": "Did he tell her a secret there?",
            "slots": {"S": "he", "V": "tell", "O1": "her", "O2": "a secret", "M2": "there"}
        },
        {
            "sentence": "Did I tell him a truth in the kitchen?",
            "slots": {"S": "I", "V": "tell", "O1": "him", "O2": "a truth", "M2": "in the kitchen"}
        },
        {
            "sentence": "Where did you tell me a story?",
            "slots": {"S": "you", "V": "tell", "O1": "me", "O2": "a story", "M2": "Where"}
        }
    ]
    
    print("📚 tellグループテストデータ:")
    for i, data in enumerate(tell_data, 1):
        print(f"  {i}. {data['sentence']}")
        print(f"     スロット: {data['slots']}")
    
    # AdverbPositionAnalyzerで処理
    analyzer = AdverbPositionAnalyzer()
    
    # tellグループを処理
    print(f"\n🔍 tellグループの副詞位置分析開始")
    results = analyzer.process_adverb_group("tell", tell_data)
    
    print(f"\n📊 tellグループ結果:")
    print("=" * 60)
    for i, result in enumerate(results, 1):
        print(f"例文{i}: {result['sentence']}")
        print(f"順序: {result['ordered_slots']}")
        
        # 順序通りの語順を表示
        ordered_words = []
        for pos in sorted(result['ordered_slots'].keys(), key=int):
            ordered_words.append(result['ordered_slots'][pos])
        print(f"語順: {' '.join(ordered_words)}")
        print()
    
    # 人間的判断ロジックの適用確認
    print("🔍 人間的判断ロジック適用確認:")
    print("=" * 60)
    
    adjustment_words = ['together', 'carefully', 'in the park']
    found_adjustments = False
    
    for result in results:
        for word in adjustment_words:
            if word in result['ordered_slots'].values():
                print(f"⚠️ 調整対象 '{word}' がtellグループに含まれています")
                found_adjustments = True
    
    if not found_adjustments:
        print("✅ tellグループには調整対象の副詞は含まれていません")
        print("✅ 人間的判断ロジックの影響なし")
    
    return results

def main():
    test_tell_group_impact()

if __name__ == "__main__":
    main()
