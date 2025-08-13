#!/usr/bin/env python3
"""
Question Formation Engine 完全版テスト
全ての微調整を含むテスト
"""

import sys
import os
sys.path.append('c:/Users/yurit/Downloads/Rephraseプロジェクト20250529/完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/data')

from engines.question_formation_engine import QuestionFormationEngine

def test_complete_version():
    """完全版テスト"""
    engine = QuestionFormationEngine()
    
    test_cases = [
        # WH疑問文
        ("What are you doing?", "O1: What (目的語疑問)"),
        ("Where did you go?", "M3: Where (場所修飾)"),
        ("Who called you?", "S: Who (主語疑問)"),
        
        # Yes/No疑問文 (語分割確認)
        ("Do you like coffee?", "完全語分割: Do + you + like + coffee"),
        ("Can you help me?", "Modal分離: Can + you + help + me"),
        
        # Tag疑問文 (助動詞分離確認)
        ("You like coffee, don't you?", "基本構造"),
        ("She can swim, can't she?", "助動詞分離: She + can + swim + M3"),
        ("They are coming, aren't they?", "Be動詞: They + are + coming + M3"),
        
        # 選択疑問文
        ("Do you prefer tea or coffee?", "O1: tea or coffee (一体)"),
        
        # 埋め込み疑問文 (改善版)
        ("I wonder what time it is.", "サブスロット: what time, it, is"),
        ("Tell me where you live.", "命令文: Tell + me + where you live"),
        
        # 否定疑問文 (新機能)
        ("Isn't this amazing?", "否定疑問: Isn't + this + amazing"),
        ("Don't you like it?", "否定疑問: Don't + you + like + it"),
        ("Can't you do it?", "Modal否定: Can't + you + do + it"),
    ]
    
    print("🚀 Question Formation Engine 完全版テスト")
    print("=" * 80)
    
    success_count = 0
    
    for sentence, expected in test_cases:
        print(f"\n📝 テスト: {sentence}")
        print(f"期待: {expected}")
        print("-" * 60)
        
        # スロット抽出
        result = engine.process(sentence)
        
        if result.get('success', False):
            success_count += 1
            slots = result.get('slots', {})
            print("✅ 成功")
            
            # 実際のスロット表示
            main_slots = {k: v for k, v in slots.items() if not k.startswith('_meta_') and not k.startswith('sub-')}
            sub_slots = {k: v for k, v in slots.items() if k.startswith('sub-')}
            
            print("📊 主要スロット:")
            for key, value in main_slots.items():
                print(f"  ├─ {key}: '{value}'")
            
            if sub_slots:
                print("🔗 サブスロット:")
                for key, value in sub_slots.items():
                    print(f"  ├─ {key}: '{value}'")
                    
            # 品質評価
            quality_score = len(main_slots) + (0.5 * len(sub_slots))
            print(f"🎯 品質スコア: {quality_score:.1f}")
            
        else:
            print("❌ 失敗")
            print(f"エラー: {result.get('error', 'Unknown')}")
        
        print("-" * 60)
    
    print(f"\n📈 最終結果")
    print("=" * 80)
    print(f"成功数: {success_count}/{len(test_cases)}")
    print(f"成功率: {(success_count/len(test_cases))*100:.1f}%")
    
    if success_count == len(test_cases):
        print("🎉 完全成功！Question Formation Engine は完璧に動作します！")
    elif success_count >= len(test_cases) * 0.9:
        print("🚀 優秀！Question Formation Engine はほぼ完璧です！")
    elif success_count >= len(test_cases) * 0.8:
        print("✅ 良好！Question Formation Engine は良く動作します！")
    else:
        print("⚠️ 要改善！さらなる調整が必要です。")

if __name__ == "__main__":
    test_complete_version()
