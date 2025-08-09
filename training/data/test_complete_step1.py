#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Engine Step 1 テスト
基本抽出メソッドの動作確認
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_basic_extraction():
    """基本抽出機能のテスト"""
    print("🧪 Complete Engine Step 1: 基本抽出テスト\n")
    
    # エンジン初期化
    try:
        engine = CompleteRephraseParsingEngine()
        print("✅ Complete Engine初期化完了\n")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return
    
    # 段階的テストケース
    test_cases = [
        {
            "sentence": "I love you.",
            "level": "基本SVO",
            "focus": "主語・動詞の正確な抽出"
        },
        {
            "sentence": "I can't afford it.",
            "level": "助動詞縮約形",
            "focus": "can't -> cannotの変換"
        },
        {
            "sentence": "He left New York a few days ago.",
            "level": "時間表現",
            "focus": "'a few days ago'の完全抽出"
        },
        {
            "sentence": "That afternoon, she gave him a book.",
            "level": "SVOO+時間",
            "focus": "複数要素の正確な分離"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        level = test_case["level"]
        focus = test_case["focus"]
        
        print(f"=== Step 1 テスト {i}: {level} ===")
        print(f"例文: {sentence}")
        print(f"焦点: {focus}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            if 'error' in result:
                print(f"❌ エラー: {result['error']}")
                continue
            
            # 結果の詳細表示
            print("📊 解析結果:")
            
            main_slots = result.get('main_slots', {})
            for slot in ['S', 'Aux', 'V', 'O1', 'O2', 'M3']:
                if slot in main_slots and main_slots[slot]:
                    values = []
                    for item in main_slots[slot]:
                        if isinstance(item, dict):
                            value = item.get('value', 'N/A')
                            rule = item.get('rule_id', 'unknown')
                            values.append(f"'{value}' ({rule})")
                        else:
                            values.append(f"'{str(item)}'")
                    print(f"  {slot}: {', '.join(values)}")
            
            # メタデータ表示
            metadata = result.get('metadata', {})
            sentence_type = result.get('sentence_type', '不明')
            print(f"  文型: {sentence_type}")
            print(f"  適用ルール数: {metadata.get('rules_applied', 0)}")
            print(f"  複雑度: {metadata.get('complexity_score', 0)}")
            
            # Sub構造があれば表示
            sub_structures = result.get('sub_structures', [])
            if sub_structures:
                print(f"  Sub構造: {len(sub_structures)}個")
                for sub in sub_structures:
                    print(f"    {sub.get('type', '不明')}節: {sub.get('verb', 'N/A')}")
            
        except Exception as e:
            print(f"❌ 解析エラー: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_basic_extraction()
