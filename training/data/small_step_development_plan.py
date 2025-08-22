#!/usr/bin/env python3
"""
Order機能スモールステップ開発計画
Phase 1.1: GrammarElement拡張（最小限の変更）
"""

def define_small_steps():
    """スモールステップ開発計画の定義"""
    
    print("=== Order機能スモールステップ開発計画 ===\n")
    
    steps = {
        "Phase 1.1": {
            "title": "GrammarElement拡張（最小限）",
            "duration": "1-2日",
            "risk": "極低",
            "description": "既存のGrammarElementクラスにorder関連フィールドを追加",
            "tasks": [
                "GrammarElementクラスにorder関連フィールド追加",
                "既存コードの動作確認",
                "回帰テスト実行"
            ],
            "success_criteria": [
                "既存の69.7%認識精度維持",
                "新フィールドが正常に初期化される",
                "既存テストが全て通過"
            ]
        },
        "Phase 1.2": {
            "title": "文型認識エンジン（基本版）",
            "duration": "2-3日", 
            "risk": "低",
            "description": "基本的な文型判定機能（肯定文/疑問文）を追加",
            "tasks": [
                "SentenceTypeDetectorクラス実装",
                "基本的な文型判定ロジック",
                "文型判定テスト"
            ],
            "success_criteria": [
                "肯定文と疑問文の区別ができる",
                "既存機能への影響なし",
                "文型判定精度80%以上"
            ]
        },
        "Phase 1.3": {
            "title": "V_group_key基本管理",
            "duration": "2-3日",
            "risk": "低",
            "description": "動詞ベースのV_group_key生成機能",
            "tasks": [
                "VGroupKeyManagerクラス実装",
                "動詞からV_group_key生成",
                "V_group_key統合テスト"
            ],
            "success_criteria": [
                "動詞からV_group_keyが正常生成",
                "既存の文法認識精度維持",
                "V_group_key生成精度90%以上"
            ]
        },
        "Phase 1.4": {
            "title": "基本order計算",
            "duration": "3-4日",
            "risk": "中",
            "description": "基本的なSlot_display_order計算機能",
            "tasks": [
                "基本order計算ロジック実装",
                "既存システムとの統合",
                "order情報出力機能"
            ],
            "success_criteria": [
                "基本的なorder情報が生成される",
                "既存の文法認識機能と並行動作",
                "order計算精度70%以上"
            ]
        }
    }
    
    # 各ステップの詳細表示
    for phase, details in steps.items():
        print(f"🔹 {phase}: {details['title']}")
        print(f"   期間: {details['duration']}")
        print(f"   リスク: {details['risk']}")
        print(f"   概要: {details['description']}")
        print(f"   タスク:")
        for task in details['tasks']:
            print(f"     - {task}")
        print(f"   成功基準:")
        for criteria in details['success_criteria']:
            print(f"     ✓ {criteria}")
        print()
    
    print("🎯 推奨開始ステップ: Phase 1.1")
    print("📋 各ステップ完了後に必ず回帰テスト実行")
    print("⚠️ 問題発生時は即座に前のステップに戻る")

if __name__ == "__main__":
    define_small_steps()
