#!/usr/bin/env python3
"""
学習型54例文バリデーションシステム（例文4-6）
正しいRephrase構造理解に基づく継続実行
"""

from real_custom_learning_validator import RealCustomLearningValidator

def continue_learning_validation():
    """学習型バリデーションの継続実行"""
    
    validator = RealCustomLearningValidator()
    
    print("🚀 学習型54例文バリデーション継続（例文4-6）")
    print("="*60)
    print("✅ Rephraseスロット構造の核心原理を確認済み:")
    print("   - スロット内容を並べて例文再構築表示")
    print("   - 重複排除・欠落防止・文法保持")
    print("   - 関係節では先行詞+関係代名詞をサブスロットに格納")
    print("="*60)
    
    # 例文4-6の処理
    results = validator.batch_process_with_learning(4, 6)
    
    return validator

if __name__ == "__main__":
    continue_learning_validation()
