#!/usr/bin/env python3
"""
例文照合による正しい語順抽出システム
元の例文と照合して正しい順序を決定
"""

import json
from pathlib import Path

class SentenceOrderValidator:
    def __init__(self):
        # actionグループのスロットデータ
        self.action_data = [
            {
                "sentence": "She sings beautifully.",
                "slots": {"S": "She", "V": "sings", "M2": "beautifully"}
            },
            {
                "sentence": "We always eat breakfast together.",
                "slots": {"S": "We", "V": "eat", "O1": "breakfast", "M1": "always", "M2": "together"}
            },
            {
                "sentence": "The cat quietly sat on the mat.",
                "slots": {"S": "The cat", "V": "sat", "M1": "quietly", "M2": "on the mat"}
            },
            {
                "sentence": "She carefully reads books.",
                "slots": {"S": "She", "V": "reads", "O1": "books", "M2": "carefully"}
            },
            {
                "sentence": "They run fast.",
                "slots": {"S": "They", "V": "run", "M2": "fast"}
            },
            {
                "sentence": "Actually, she works very hard.",
                "slots": {"S": "she", "V": "works", "M1": "Actually", "M2": "very hard"}
            },
            {
                "sentence": "Every morning, he jogs slowly in the park.",
                "slots": {"S": "he", "V": "jogs", "M1": "Every morning", "M2": "slowly", "M3": "in the park"}
            }
        ]
    
    def get_word_position_in_sentence(self, sentence, word_or_phrase):
        """元の例文中での単語/句の実際の位置を取得"""
        # カンマと句読点を除去して正規化
        normalized_sentence = sentence.replace(",", "").replace(".", "")
        words = normalized_sentence.split()
        
        # 句の場合（複数単語）
        if " " in word_or_phrase:
            phrase_words = word_or_phrase.split()
            for i in range(len(words) - len(phrase_words) + 1):
                if words[i:i+len(phrase_words)] == phrase_words:
                    return i + 1  # 1-based indexing
        else:
            # 単語の場合
            for i, word in enumerate(words):
                if word == word_or_phrase:
                    return i + 1  # 1-based indexing
        
        return None
    
    def extract_correct_order_from_sentence(self, sentence_data):
        """元の例文から正しい語順を抽出"""
        sentence = sentence_data["sentence"]
        slots = sentence_data["slots"]
        
        print(f"📝 例文: {sentence}")
        print(f"   スロット: {slots}")
        
        # 各要素の実際の位置を取得
        element_positions = {}
        for slot_type, element in slots.items():
            position = self.get_word_position_in_sentence(sentence, element)
            if position:
                element_positions[element] = position
                print(f"   📍 {element} → 位置{position}")
        
        # 位置順にソート
        sorted_elements = sorted(element_positions.items(), key=lambda x: x[1])
        
        # 順序番号を付与
        ordered_slots = {}
        for order, (element, position) in enumerate(sorted_elements, 1):
            ordered_slots[str(order)] = element
        
        print(f"   ✅ 正しい順序: {ordered_slots}")
        return ordered_slots
    
    def analyze_all_sentences(self):
        """全例文の正しい語順を分析"""
        print("🚀 例文照合による正しい語順抽出開始")
        print("=" * 60)
        
        results = []
        
        for i, sentence_data in enumerate(self.action_data, 1):
            print(f"\n例文{i}:")
            ordered_slots = self.extract_correct_order_from_sentence(sentence_data)
            
            result = {
                "sentence": sentence_data["sentence"],
                "original_slots": sentence_data["slots"],
                "correct_ordered_slots": ordered_slots
            }
            results.append(result)
        
        # 結果をファイルに保存
        output_file = Path("correct_order_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 正しい順序結果を {output_file} に保存しました")
        
        # 結果表示
        print("\n📊 正しい語順結果:")
        print("=" * 60)
        for i, result in enumerate(results, 1):
            print(f"例文{i}: {result['sentence']}")
            print(f"正しい順序: {result['correct_ordered_slots']}")
            print()
        
        return results
    
    def compare_with_current_results(self):
        """現在の結果と比較"""
        print("\n🔍 現在の結果との比較:")
        print("=" * 60)
        
        # 現在の結果をロード
        current_file = Path("action_group_fixed_results.json")
        if not current_file.exists():
            print("❌ 現在の結果ファイルが見つかりません")
            return
        
        with open(current_file, 'r', encoding='utf-8') as f:
            current_results = json.load(f)
        
        correct_results = self.analyze_all_sentences()
        
        print("\n🔍 比較結果:")
        for i, (current, correct) in enumerate(zip(current_results, correct_results)):
            print(f"\n例文{i+1}: {current['sentence']}")
            print(f"現在の順序: {current['ordered_slots']}")
            print(f"正しい順序: {correct['correct_ordered_slots']}")
            
            # 違いをチェック
            if current['ordered_slots'] != correct['correct_ordered_slots']:
                print("❌ 順序が違います！")
            else:
                print("✅ 順序が正しいです")

def main():
    validator = SentenceOrderValidator()
    validator.compare_with_current_results()

if __name__ == "__main__":
    main()
