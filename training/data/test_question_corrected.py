#!/usr/bin/env python3
"""
Question Formation Engine 修正版テスト
正しいRephraseスロット体系での動作確認
"""

import sys
import os
sys.path.append('c:/Users/yurit/Downloads/Rephraseプロジェクト20250529/完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/data')

from engines.question_formation_engine import QuestionFormationEngine

def test_corrected_slots():
    """修正されたスロット分解テスト"""
    engine = QuestionFormationEngine()
    
    test_cases = [
        # WH疑問文
        ("What are you doing?", "O1: What (目的語疑問)"),
        ("Where did you go?", "M3: Where (場所修飾)"),
        ("When will you come?", "M3: When (時間修飾)"), 
        ("Who called you?", "S: Who (主語疑問)"),
        ("Which book do you want?", "O1: Which book (目的語)"),
        
        # Yes/No疑問文
        ("Do you like coffee?", "語分割: like + coffee"),
        ("Can you help me?", "語分割: can + help + me"),
        ("Are you coming?", "be動詞処理"),
        
        # Tag疑問文
        ("You like coffee, don't you?", "M3: don't you (タグ)"),
        ("She can swim, can't she?", "Aux: can + V: swim + M3: can't she"),
        
        # 選択疑問文
        ("Do you prefer tea or coffee?", "O1: tea or coffee (一体)"),
        
        # 埋め込み疑問文
        ("I wonder what time it is.", "sub-c1: what time, sub-s: it, sub-v: is"),
        ("Tell me where you live.", "sub-m3: where, sub-s: you, sub-v: live"),
    ]
    
    print("🔧 Question Formation Engine 修正版テスト")
    print("=" * 70)
    
    for sentence, expected in test_cases:
        print(f"\n📝 テスト: {sentence}")
        print(f"期待: {expected}")
        print("-" * 50)
        
        # スロット抽出
        result = engine.process(sentence)
        
        if result.get('success', False):
            slots = result.get('slots', {})
            print("✅ 成功")
            print("📊 実際のスロット:")
            for key, value in slots.items():
                if not key.startswith('_meta_'):  # メタデータは除外
                    print(f"  ├─ {key}: '{value}'")
            
            # メタデータ表示
            meta_items = {k: v for k, v in slots.items() if k.startswith('_meta_')}
            if meta_items:
                print("🏷️ メタデータ:")
                for key, value in meta_items.items():
                    print(f"  ├─ {key}: '{value}'")
        else:
            print("❌ 失敗")
            print(f"エラー: {result.get('error', 'Unknown')}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_corrected_slots()
