#!/usr/bin/env python3
"""
仮定法・条件法エンジンのスロット分解デモンストレーション

各パターンがどのようにスロット分解されるかを詳細に表示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.subjunctive_conditional_engine import SubjunctiveConditionalEngine

def demonstrate_slot_decomposition():
    """仮定法・条件法エンジンのスロット分解を詳細デモ"""
    engine = SubjunctiveConditionalEngine()
    
    # 詳細な分析対象例文
    test_sentences = [
        "If it rains, I will stay home.",
        "If I were rich, I would travel the world.",
        "If I had studied harder, I would have passed the exam.",
        "Were I rich, I would buy a house.",
        "Had she known the truth, she would have acted differently.",
        "I wish I were taller.",
        "She wishes she had more money.",
        "Unless you hurry, you will be late.",
        "It's important that he be on time.",
    ]
    
    print("🔍 仮定法・条件法エンジン - 詳細スロット分解デモンストレーション")
    print("=" * 80)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【例文 {i}】: {sentence}")
        print("-" * 60)
        
        if not engine.is_applicable(sentence):
            print("❌ このエンジンでは処理不可")
            continue
            
        result = engine.process(sentence)
        
        if not result['success']:
            print(f"❌ 処理エラー: {result['error']}")
            continue
        
        # 条件法タイプを表示
        conditional_type = result['metadata']['conditional_type']
        print(f"📋 分類: {conditional_type}")
        
        # 構造分析を表示
        structure = result['metadata'].get('structure', {})
        main_clause = structure.get('main_clause', '')
        sub_clause = structure.get('subordinate_clause', '')
        
        if main_clause:
            print(f"🏛️  主節: '{main_clause}'")
        if sub_clause:
            print(f"🔗 従属節: '{sub_clause}'")
        
        print("\n📊 スロット配分結果:")
        
        # Upper Slots (主節)
        upper_slots = result['slots']
        print("  【Upper Slots - 主節成分】:")
        for slot_name in ['S', 'V', 'O1', 'C1', 'M1', 'M2', 'M3', 'Aux']:
            value = upper_slots.get(slot_name, '').strip()
            if value:
                slot_desc = {
                    'S': '主語',
                    'V': '動詞', 
                    'O1': '目的語1',
                    'C1': '補語1',
                    'M1': '修飾語1',
                    'M2': '修飾語2', 
                    'M3': '修飾語3',
                    'Aux': '助動詞'
                }[slot_name]
                print(f"    {slot_name} ({slot_desc}): '{value}'")
        
        # Sub-slots (従属節)
        print("  【Sub-slots - 従属節成分】:")
        for slot_name in ['sub-s', 'sub-v', 'sub-o1', 'sub-c1', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux']:
            value = upper_slots.get(slot_name, '').strip()
            if value:
                slot_desc = {
                    'sub-s': '従属主語',
                    'sub-v': '従属動詞',
                    'sub-o1': '従属目的語1',
                    'sub-c1': '従属補語1', 
                    'sub-m1': '従属修飾語1',
                    'sub-m2': '従属修飾語2',
                    'sub-m3': '従属修飾語3',
                    'sub-aux': '従属助動詞'
                }[slot_name]
                print(f"    {slot_name} ({slot_desc}): '{value}'")
        
        # 特別な分析ポイントがあれば表示
        print(f"\n🔬 分析ポイント:")
        if conditional_type == "conditional_type1":
            print("    • 実在条件法: 現実的に起こりうる条件と結果")
            print("    • if節(従属節)の動詞は現在形、主節は未来形")
        elif conditional_type == "conditional_type2":
            print("    • 非実在現在条件法: 現在の非現実的仮定")
            print("    • if節はwere/過去形、主節はwould/could/might")
        elif conditional_type == "conditional_type3":
            print("    • 非実在過去条件法: 過去の非現実的仮定")  
            print("    • if節はhad+過去分詞、主節はwould have+過去分詞")
        elif conditional_type == "inverted_conditional":
            print("    • 倒置条件法: if省略で助動詞が文頭に")
            print("    • Were/Had/Should + 主語の語順")
        elif conditional_type == "wish_subjunctive":
            print("    • wish仮定法: 願望を表す非現実的内容")
            print("    • wish + (that) + 仮定法過去/過去完了")
        
        print("\n" + "─" * 60)

if __name__ == "__main__":
    demonstrate_slot_decomposition()
