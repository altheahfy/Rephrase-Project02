#!/usr/bin/env python3
"""
強化されたサブレベル5文型対応テスト
関係節・従属節・比較構文などの高次構文テスト
"""

from pure_stanza_engine_v3_1_unified import PureStanzaEngineV31
import json

def test_advanced_sublevel_mapping():
    """強化されたサブレベルマッピングのテスト"""
    
    engine = PureStanzaEngineV31()
    
    # 高次構文テストケース
    advanced_test_cases = [
        # 基本テスト（既存確認）
        "I gave him a book.",
        "The tall man runs fast.",
        
        # 関係代名詞節テスト
        "The book that he bought is expensive.",
        "The man who runs fast won the race.",
        
        # 従属節テスト  
        "He runs because he is late.",
        "She studies while listening to music.",
        
        # 比較構文テスト
        "He is taller than John.",
        "She runs as fast as he can.",
        
        # 複合修飾語テスト
        "The very tall and handsome man runs extremely fast.",
        
        # 前置詞句テスト
        "The book on the table is mine.",
    ]
    
    print("🔍 強化されたサブレベル5文型マッピングテスト開始")
    print("="*70)
    
    for i, sentence in enumerate(advanced_test_cases, 1):
        print(f"\n【テスト{i}】 {sentence}")
        print("-" * 50)
        
        try:
            result = engine.decompose_unified(sentence)
            
            # 結果の詳細分析
            analyze_result_depth(result, sentence)
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            continue
    
    print(f"\n{'='*70}")
    print("🎯 強化されたサブレベルマッピングテスト完了")

def analyze_result_depth(result, sentence):
    """結果の階層深度を分析"""
    
    def count_depth(obj, current_depth=0):
        """再帰的に深度をカウント"""
        max_depth = current_depth
        
        if isinstance(obj, dict):
            if 'subslots' in obj:
                sub_depth = count_depth(obj['subslots'], current_depth + 1)
                max_depth = max(max_depth, sub_depth)
            else:
                for value in obj.values():
                    sub_depth = count_depth(value, current_depth)
                    max_depth = max(max_depth, sub_depth)
        
        return max_depth
    
    max_depth = count_depth(result)
    slot_count = count_total_slots(result)
    
    print(f"📊 分析結果:")
    print(f"   - 最大階層深度: {max_depth}")
    print(f"   - 総スロット数: {slot_count}")
    
    # サブスロット存在箇所の特定
    subslot_locations = find_subslot_locations(result)
    if subslot_locations:
        print(f"   - サブスロット箇所: {', '.join(subslot_locations)}")
    
    # 簡略結果表示
    print(f"📋 結果: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")

def count_total_slots(obj):
    """総スロット数をカウント"""
    if not isinstance(obj, dict):
        return 0
        
    count = 0
    for key, value in obj.items():
        if key in ['M1', 'S', 'O1', 'O2', 'C1', 'C2', 'M2', 'M3', 'Aux', 'V']:
            count += 1
            if isinstance(value, dict) and 'subslots' in value:
                count += count_total_slots(value['subslots'])
        elif key == 'subslots':
            count += count_total_slots(value)
    
    return count

def find_subslot_locations(obj, path=""):
    """サブスロットの位置を特定"""
    locations = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            if key == 'subslots':
                locations.append(path)
            elif isinstance(value, dict):
                locations.extend(find_subslot_locations(value, current_path))
    
    return locations

if __name__ == "__main__":
    test_advanced_sublevel_mapping()
