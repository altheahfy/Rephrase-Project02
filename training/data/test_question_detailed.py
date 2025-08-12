#!/usr/bin/env python3
"""
Question Formation Engine 個別動作検証テスト
各質問タイプの詳細なスロット分解を検証
"""

import sys
import os
sys.path.append('c:/Users/yurit/Downloads/Rephraseプロジェクト20250529/完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training\data')

from engines.question_formation_engine import QuestionFormationEngine

def detailed_test():
    """詳細なスロット分解テスト"""
    engine = QuestionFormationEngine()
    
    # テストケース
    test_cases = [
        # WH疑問文
        ("What are you doing?", "WH疑問文(標準)"),
        ("Where did you go?", "WH疑問文(過去)"), 
        ("Who called you?", "WH疑問文(主語)"),
        ("Which book do you want?", "WH疑問文(which+名詞)"),
        ("How many books did you read?", "WH疑問文(複合)"),
        
        # Yes/No疑問文
        ("Are you coming?", "Yes/No疑問文(be動詞)"),
        ("Do you like coffee?", "Yes/No疑問文(do)"),
        ("Can you help me?", "Yes/No疑問文(modal)"),
        ("Have you finished?", "Yes/No疑問文(完了)"),
        
        # Tag疑問文
        ("You like coffee, don't you?", "Tag疑問文(肯定→否定)"),
        ("She can't swim, can she?", "Tag疑問文(否定→肯定)"),
        ("They are coming, aren't they?", "Tag疑問文(be動詞)"),
        
        # 選択疑問文
        ("Do you prefer tea or coffee?", "選択疑問文"),
        ("Is it red or blue?", "選択疑問文(be動詞)"),
        
        # 埋め込み疑問文
        ("I wonder what time it is.", "埋め込み疑問文"),
        ("Tell me where you live.", "埋め込み疑問文(命令)"),
        ("Do you know who called?", "埋め込み疑問文(Yes/No+WH)"),
        
        # 特殊ケース
        ("Isn't this amazing?", "否定疑問文"),
        ("What a beautiful day!", "感嘆文"),
        ("You're coming, right?", "確認疑問(right)"),
    ]
    
    print("🔍 Question Formation Engine 詳細動作検証")
    print("=" * 80)
    
    for sentence, description in test_cases:
        print(f"\n📝 テスト: {description}")
        print(f"入力: '{sentence}'")
        print("-" * 60)
        
        # is_applicable チェック
        is_applicable = engine.is_applicable(sentence)
        print(f"適用可能: {'✅ Yes' if is_applicable else '❌ No'}")
        
        if is_applicable:
            # 質問情報抽出
            question_info = engine.extract_question_info(sentence)
            print(f"質問発見: {'✅ Yes' if question_info['question_found'] else '❌ No'}")
            print(f"質問タイプ: {question_info.get('question_type', 'Unknown')}")
            print(f"疑問詞: {question_info.get('question_word', 'None')}")
            print(f"助動詞: {question_info.get('auxiliary', 'None')}")
            
            # スロット抽出
            slots = engine.process_sentence(sentence)
            print(f"抽出スロット数: {len(slots)}")
            
            if slots:
                print("📊 スロット詳細:")
                for key, value in slots.items():
                    print(f"  ├─ {key}: '{value}'")
            else:
                print("📊 スロット: なし")
                
            # 標準インターフェーステスト
            standard_result = engine.process(sentence)
            success = standard_result.get('success', False)
            confidence = standard_result.get('metadata', {}).get('confidence_raw', 0)
            print(f"標準IF結果: {'✅ 成功' if success else '❌ 失敗'}")
            print(f"信頼度: {confidence:.2f}")
        
        print("-" * 60)

if __name__ == "__main__":
    detailed_test()
