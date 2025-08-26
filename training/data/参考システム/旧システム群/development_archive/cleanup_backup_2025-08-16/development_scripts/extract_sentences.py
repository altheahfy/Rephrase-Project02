#!/usr/bin/env python3
"""
正解データベースから例文リストを抽出
"""

import json

def extract_sentences_from_expected_data():
    """正解データベースから例文リストを抽出"""
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sentences = []
        results = data.get('results', [])
        
        # 番号順にソート
        sorted_results = sorted(results, key=lambda x: int(x['id']))
        
        for result in sorted_results:
            sentence = result.get('sentence', '')
            sentences.append(sentence)
            print(f"例文{result['id']}: {sentence}")
        
        print(f"\n合計例文数: {len(sentences)}")
        
        # Pythonリスト形式で出力
        print("\n=== Python形式リスト ===")
        print("your_test_sentences = [")
        for sentence in sentences:
            print(f'    "{sentence}",')
        print("]")
        
        return sentences
        
    except Exception as e:
        print(f"エラー: {e}")
        return []

if __name__ == "__main__":
    extract_sentences_from_expected_data()
