#!/usr/bin/env python3
"""
人間的判断による語順マッピングシステム
元の例文語順を尊重し、視覚的異常を検出して調整
"""

import json
from pathlib import Path
from collections import defaultdict

class HumanLikeOrderMapper:
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
    
    def create_initial_grid(self):
        """初期グリッド作成：各例文の実際の語順で配置"""
        print("🚀 人間的判断による語順マッピング開始")
        print("=" * 60)
        
        # 最大位置数を確認
        max_positions = 0
        sentence_positions = []
        
        for sentence_data in self.action_data:
            sentence = sentence_data["sentence"]
            slots = sentence_data["slots"]
            
            positions = {}
            for slot_type, element in slots.items():
                pos = self.get_word_position_in_sentence(sentence, element)
                if pos:
                    positions[pos] = element
                    max_positions = max(max_positions, pos)
            
            sentence_positions.append({
                "sentence": sentence,
                "positions": positions,
                "slots": slots
            })
        
        print(f"📊 最大位置数: {max_positions}")
        
        # グリッド表示
        print("\n📋 初期グリッド（実際の語順）:")
        print("=" * 60)
        
        # ヘッダー
        header = "例文\t\t\t"
        for i in range(1, max_positions + 1):
            header += f"{i}\t"
        print(header)
        print("-" * 80)
        
        # 各例文の位置を表示
        grid_data = []
        for i, sp in enumerate(sentence_positions):
            row_data = {"sentence_num": i+1, "sentence": sp["sentence"], "positions": {}}
            
            row = f"{i+1}. {sp['sentence'][:20]}...\t"
            for pos in range(1, max_positions + 1):
                element = sp["positions"].get(pos, "")
                row += f"{element}\t"
                if element:
                    row_data["positions"][pos] = element
            
            print(row)
            grid_data.append(row_data)
        
        return grid_data, max_positions
    
    def analyze_column_conflicts(self, grid_data, max_positions):
        """列内の衝突・異常を分析"""
        print("\n🔍 列分析：同じ位置の要素を確認")
        print("=" * 60)
        
        column_analysis = {}
        conflict_elements = []
        
        for pos in range(1, max_positions + 1):
            elements_in_column = []
            for row in grid_data:
                element = row["positions"].get(pos)
                if element:
                    elements_in_column.append({
                        "element": element,
                        "sentence_num": row["sentence_num"],
                        "sentence": row["sentence"]
                    })
            
            column_analysis[pos] = elements_in_column
            
            print(f"\n位置{pos}:")
            if not elements_in_column:
                print("  (空)")
            else:
                for item in elements_in_column:
                    print(f"  - {item['element']} (例文{item['sentence_num']})")
                
                # 衝突検出：同じ位置に複数の異なる要素
                if len(elements_in_column) > 1:
                    print(f"  ⚠️ 衝突検出！同じ位置に{len(elements_in_column)}個の要素")
                    
                    # 特殊位置の要素を特定（移動候補）
                    for item in elements_in_column:
                        if item['element'] in ['together', 'carefully']:
                            conflict_elements.append({
                                'element': item['element'],
                                'current_pos': pos,
                                'sentence_num': item['sentence_num'],
                                'sentence': item['sentence']
                            })
                            print(f"    🎯 移動候補: {item['element']}")
        
        return column_analysis, conflict_elements
    
    def apply_human_adjustments(self, grid_data, conflict_elements, max_positions):
        """人間的判断による調整を適用"""
        print("\n🎯 人間的判断による調整適用")
        print("=" * 60)
        
        # 調整ルール
        adjustments = {
            'together': 7,    # 7列目に移動（文末位置）
            'carefully': 3,   # 3列目に移動（動詞直前）
            'in the park': 8  # 8列目に移動
        }
        
        # 調整を適用
        adjusted_grid = []
        for row in grid_data:
            new_row = {
                "sentence_num": row["sentence_num"],
                "sentence": row["sentence"],
                "positions": row["positions"].copy()
            }
            
            # 移動が必要な要素をチェック
            elements_to_move = []
            for pos, element in list(new_row["positions"].items()):
                if element in adjustments:
                    elements_to_move.append((pos, element, adjustments[element]))
            
            # 移動実行
            for old_pos, element, new_pos in elements_to_move:
                del new_row["positions"][old_pos]
                new_row["positions"][new_pos] = element
                print(f"  📝 例文{new_row['sentence_num']}: {element} を位置{old_pos}→{new_pos}に移動")
            
            # 空きスロットを詰める処理
            self._fill_gaps(new_row)
            
            adjusted_grid.append(new_row)
        
        return adjusted_grid
    
    def _fill_gaps(self, row):
        """空きスロットを詰める"""
        positions = row["positions"]
        if not positions:
            return
        
        # 現在の位置をソート
        sorted_positions = sorted(positions.keys())
        
        # 連続した位置に再配置
        new_positions = {}
        new_pos = 1
        
        for old_pos in sorted_positions:
            element = positions[old_pos]
            new_positions[new_pos] = element
            
            # 位置が変わった場合のログ
            if new_pos != old_pos:
                print(f"    🔧 例文{row['sentence_num']}: {element} を位置{old_pos}→{new_pos}に詰める")
            
            new_pos += 1
        
        row["positions"] = new_positions
    
    def display_final_grid(self, adjusted_grid):
        """最終調整済みグリッドを表示"""
        print("\n📊 最終調整済みグリッド:")
        print("=" * 60)
        
        # 最大位置を再計算
        max_pos = 0
        for row in adjusted_grid:
            if row["positions"]:
                max_pos = max(max_pos, max(row["positions"].keys()))
        
        # ヘッダー
        header = "例文\t\t\t"
        for i in range(1, max_pos + 1):
            header += f"{i}\t"
        print(header)
        print("-" * 80)
        
        # 各例文の調整後位置を表示
        results = []
        for row in adjusted_grid:
            display_row = f"{row['sentence_num']}. {row['sentence'][:20]}...\t"
            ordered_slots = {}
            
            for pos in range(1, max_pos + 1):
                element = row["positions"].get(pos, "")
                display_row += f"{element}\t"
                if element:
                    ordered_slots[str(pos)] = element
            
            print(display_row)
            
            results.append({
                "sentence": row["sentence"],
                "adjusted_ordered_slots": ordered_slots
            })
        
        return results
    
    def generate_final_mapping(self):
        """完全な人間的判断マッピングを生成"""
        # Step 1: 初期グリッド作成
        grid_data, max_positions = self.create_initial_grid()
        
        # Step 2: 衝突分析
        column_analysis, conflict_elements = self.analyze_column_conflicts(grid_data, max_positions)
        
        # Step 3: 人間的調整適用
        adjusted_grid = self.apply_human_adjustments(grid_data, conflict_elements, max_positions)
        
        # Step 4: 最終グリッド表示
        results = self.display_final_grid(adjusted_grid)
        
        # 結果をファイルに保存
        output_file = Path("human_like_order_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 人間的判断結果を {output_file} に保存しました")
        
        return results

def main():
    mapper = HumanLikeOrderMapper()
    results = mapper.generate_final_mapping()
    
    print("\n🎯 最終結果:")
    for i, result in enumerate(results, 1):
        print(f"例文{i}: {result['sentence']}")
        print(f"調整済み順序: {result['adjusted_ordered_slots']}")
        print()

if __name__ == "__main__":
    main()
