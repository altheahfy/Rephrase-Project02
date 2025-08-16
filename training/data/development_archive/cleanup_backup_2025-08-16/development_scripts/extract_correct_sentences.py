#!/usr/bin/env python3
"""
正解データベースから正しい例文リストを抽出
"""
import json

def extract_sentences():
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("正解データベースの例文リスト:")
        sentences = []
        
        # correct_answersから番号順にソートして取得
        correct_answers = data.get('correct_answers', {})
        for i in range(1, 55):  # 1-54
            key = str(i)
            if key in correct_answers:
                sentence = correct_answers[key].get('sentence', '')
                sentences.append(sentence)
                print(f"{i:2d}: {sentence}")
            else:
                print(f"{i:2d}: [データなし]")
        
        return sentences
        
    except Exception as e:
        print(f"エラー: {e}")
        return []

if __name__ == "__main__":
    sentences = extract_sentences()
    print(f"\n総数: {len(sentences)}例文")
