#!/usr/bin/env python3
"""
システム出力形式確認用スクリプト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def check_output_format():
    """システムの出力形式を詳細確認"""
    print("🔍 システム出力形式確認")
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='WARNING')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    test_sentences = [
        "I love you.",
        "The person that works here is kind.",
        "The letter was written by John."
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 テスト例文: {sentence}")
        print("-" * 50)
        
        # process()メソッドの結果
        try:
            result1 = mapper.process(sentence)
            print(f"process()の出力:")
            print(f"  型: {type(result1)}")
            print(f"  内容: {result1}")
            if isinstance(result1, dict):
                print(f"  キー: {list(result1.keys())}")
        except Exception as e:
            print(f"process()エラー: {e}")
        
        # process_sentence()メソッドの結果（もしあれば）
        try:
            result2 = mapper.process_sentence(sentence)
            print(f"\nprocess_sentence()の出力:")
            print(f"  型: {type(result2)}")
            print(f"  内容: {result2}")
            if isinstance(result2, dict):
                print(f"  キー: {list(result2.keys())}")
        except AttributeError:
            print(f"\nprocess_sentence()メソッドは存在しません")
        except Exception as e:
            print(f"process_sentence()エラー: {e}")

if __name__ == "__main__":
    check_output_format()
