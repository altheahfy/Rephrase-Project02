#!/usr/bin/env python3
"""
文法ハンドラー修正優先順位分析
現在の69.7%精度向上のための戦略的修正計画
"""

def analyze_grammar_handler_priorities():
    """文法ハンドラー修正の優先順位分析"""
    
    print("=== 文法ハンドラー修正優先順位分析 ===\n")
    
    # 現在の具体的問題
    issues = [
        {
            "sentence": "The car is red.",
            "issue": "C1補語「red」が認識されない",
            "expected": "C1: red",
            "actual": "C1: なし",
            "pattern": "SVC文型（be動詞＋形容詞補語）",
            "priority": "高",
            "fix_complexity": "低"
        },
        {
            "sentence": "He has finished his homework.",
            "issue": "O1目的語の境界が不正確",
            "expected": "O1: his homework",
            "actual": "O1: his",
            "pattern": "修飾語つき目的語の境界認識",
            "priority": "高",
            "fix_complexity": "中"
        },
        {
            "sentence": "The students study hard for exams.",
            "issue": "修飾語M2, M3の分類・境界エラー",
            "expected": "M2: hard, M3: for exams",
            "actual": "M2: for, M3: なし",
            "pattern": "副詞＋前置詞句の修飾語分類",
            "priority": "中",
            "fix_complexity": "中"
        },
        {
            "sentence": "The teacher explains grammar clearly to confused students daily.",
            "issue": "複数修飾語の境界・分類エラー",
            "expected": "M2: to confused students, M3: daily",
            "actual": "M2: to, M3: confused",
            "pattern": "複数修飾語の正確な境界認識",
            "priority": "中",
            "fix_complexity": "高"
        },
        {
            "sentence": "The student writes essays carefully for better grades.",
            "issue": "副詞と前置詞句修飾語の分類エラー",
            "expected": "M2: carefully, M3: for better grades",
            "actual": "M2: for, M3: better",
            "pattern": "副詞＋前置詞句の修飾語分類",
            "priority": "中",
            "fix_complexity": "中"
        }
    ]
    
    # 優先順位順に表示
    high_priority = [issue for issue in issues if issue["priority"] == "高"]
    medium_priority = [issue for issue in issues if issue["priority"] == "中"]
    
    print("🔥 **高優先度修正項目** (即座修正推奨)")
    for i, issue in enumerate(high_priority, 1):
        print(f"\n{i}. {issue['pattern']}")
        print(f"   例文: \"{issue['sentence']}\"")
        print(f"   問題: {issue['issue']}")
        print(f"   期待: {issue['expected']}")
        print(f"   実際: {issue['actual']}")
        print(f"   修正難易度: {issue['fix_complexity']}")
    
    print(f"\n⚡ **中優先度修正項目** (順次修正)")
    for i, issue in enumerate(medium_priority, 1):
        print(f"\n{i}. {issue['pattern']}")
        print(f"   例文: \"{issue['sentence']}\"")
        print(f"   問題: {issue['issue']}")
        print(f"   修正難易度: {issue['fix_complexity']}")
    
    # 修正戦略の提案
    print(f"\n📋 **修正戦略提案**")
    
    strategies = [
        {
            "phase": "フェーズ1: SVC文型修正",
            "target": "「The car is red.」C1補語認識", 
            "expected_gain": "+16.6%精度向上",
            "effort": "低",
            "description": "be動詞＋形容詞パターンのC1補語認識修正"
        },
        {
            "phase": "フェーズ2: 目的語境界修正", 
            "target": "「his homework」完全認識",
            "expected_gain": "+8.3%精度向上",
            "effort": "中",
            "description": "修飾語つき目的語の境界認識アルゴリズム改善"
        },
        {
            "phase": "フェーズ3: 修飾語分類改善",
            "target": "M2, M3修飾語の正確な分類",
            "expected_gain": "+15-20%精度向上",
            "effort": "中～高",
            "description": "副詞・前置詞句修飾語の境界認識と分類ロジック改善"
        }
    ]
    
    for strategy in strategies:
        print(f"\n🎯 {strategy['phase']}")
        print(f"   対象: {strategy['target']}")
        print(f"   期待効果: {strategy['expected_gain']}")
        print(f"   作業量: {strategy['effort']}")
        print(f"   概要: {strategy['description']}")
    
    print(f"\n🚀 **推奨開始順序**")
    print("1. フェーズ1から開始（最大効果・最小リスク）")
    print("2. 各フェーズ完了後に回帰テスト実行")
    print("3. 精度が85%を超えたらPhase 1.3 (V_group_key管理)に移行検討")

if __name__ == "__main__":
    analyze_grammar_handler_priorities()
