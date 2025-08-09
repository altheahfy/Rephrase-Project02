#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rephrase_Parsing_Engineの実際の処理フローを調査
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine

def investigate_processing_flow():
    """処理フローの調査"""
    engine = RephraseParsingEngine()
    
    print("=== Rephrase Parsing Engine 調査 ===")
    
    # ルールデータの確認
    print("\n--- ルールデータの内容 ---")
    if hasattr(engine, 'rules_data') and engine.rules_data:
        print(f"ルールファイル読み込み: ✅")
        print(f"ルールデータのキー: {list(engine.rules_data.keys())}")
        
        if 'rules' in engine.rules_data:
            rules = engine.rules_data['rules']
            print(f"定義されたルール数: {len(rules)}")
            
            # 時間修飾語ルールを探す
            time_rules = []
            for r in rules:
                if isinstance(r, dict):
                    rule_id = r.get('id', '')
                    assign_info = r.get('assign', {})
                    
                    if 'time' in rule_id.lower() or (isinstance(assign_info, dict) and assign_info.get('slot') == 'M3'):
                        time_rules.append(r)
                    elif isinstance(assign_info, list):
                        # assignが配列の場合もチェック
                        for assign_item in assign_info:
                            if isinstance(assign_item, dict) and assign_item.get('slot') == 'M3':
                                time_rules.append(r)
                                break
                                
            print(f"時間修飾語関連ルール数: {len(time_rules)}")
            
            for rule in time_rules[:3]:  # 最初の3つを表示
                rule_id = rule.get('id', 'ID不明')
                trigger = rule.get('trigger', {})
                pattern = trigger.get('pattern', 'パターンなし')
                print(f"  - {rule_id}: {str(pattern)[:50]}...")
                
    else:
        print(f"ルールファイル読み込み: ❌ フォールバックルール使用")
    
    # 実際の処理方法を確認するために、テスト文を解析
    test_sentence = "He left New York a few days ago."
    print(f"\n--- テスト文の処理フロー ---")
    print(f"テスト文: {test_sentence}")
    
    # spaCyなしでの処理を試してみる
    original_nlp = engine.nlp
    engine.nlp = None  # spaCyを一時的に無効化
    
    print("\n🔍 spaCy無効時の処理:")
    result_without_spacy = engine.analyze_sentence(test_sentence)
    print(f"結果: {result_without_spacy}")
    
    # spaCyありでの処理
    engine.nlp = original_nlp
    print("\n🔍 spaCy有効時の処理:")
    result_with_spacy = engine.analyze_sentence(test_sentence)
    print(f"結果: {result_with_spacy}")
    
    # 処理パスの確認
    print(f"\n--- 処理パス確認 ---")
    print(f"is_question('{test_sentence}'): {engine.is_question(test_sentence)}")
    print(f"is_imperative_with_vocative('{test_sentence}'): {engine.is_imperative_with_vocative(test_sentence)}")
    print(f"contains_subclause('{test_sentence}'): {engine.contains_subclause(test_sentence)}")

if __name__ == "__main__":
    investigate_processing_flow()
