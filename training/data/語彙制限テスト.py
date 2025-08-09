# 語彙制限テスト - シンプル版

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

# エンジン初期化
engine = RephraseParsingEngine()

# 様々な語彙でテスト
test_sentences = [
    "I have seen you.",                    # seen = 不規則過去分詞（辞書にある）
    "She has completed the task.",         # completed = 規則過去分詞（-edで判定）
    "They have accomplished the mission.", # accomplished = 規則過去分詞（-edで判定）
    "He has broken the record.",           # broken = 不規則過去分詞（辞書にある）
    "We have investigated the problem.",   # investigated = 規則過去分詞（-edで判定）
]

print("=== 語彙制限解決テスト ===\n")

for sentence in test_sentences:
    print(f"文: {sentence}")
    
    # 解析実行
    try:
        result = engine.analyze_sentence(sentence)
        
        # スロット表示
        if result:
            print("スロット:")
            for slot, value_list in result.items():
                if slot != 'Slot_display_order':
                    if isinstance(value_list, list) and value_list:
                        print(f"  {slot}: {value_list[0]['value']}")
                    else:
                        print(f"  {slot}: {value_list}")
        else:
            print("  解析失敗")
            
    except Exception as e:
        print(f"  エラー: {e}")
    
    print("-" * 40)

print("\n=== 語尾判定テスト ===")
test_words = ["completed", "accomplished", "investigated", "studied", "worked"]

for word in test_words:
    is_pp = engine.is_past_participle(word)
    print(f"{word}: {'✅ 過去分詞' if is_pp else '❌ 認識失敗'}")
