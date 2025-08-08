"""
JSONファイル活用度の検証
1000行のルール辞書をどれだけ使えているかチェック
"""

import json
import os

def analyze_json_usage():
    """JSONファイルの活用度分析"""
    
    print("🔍 rephrase_rules_v1.0.json 活用度分析")
    print("=" * 50)
    
    # JSONファイル読み込み
    with open('rephrase_rules_v1.0.json', 'r', encoding='utf-8') as f:
        rules_data = json.load(f)
    
    # ファイル情報
    file_size = os.path.getsize('rephrase_rules_v1.0.json')
    with open('rephrase_rules_v1.0.json', 'r', encoding='utf-8') as f:
        lines = len(f.readlines())
    
    print(f"📊 JSONファイル情報:")
    print(f"   - 行数: {lines}行")
    print(f"   - ファイルサイズ: {file_size:,}バイト ({file_size/1024:.1f}KB)")
    print(f"   - ルール数: {len(rules_data.get('rules', []))}")
    
    # ルール詳細分析
    rules = rules_data.get('rules', [])
    
    print(f"\n📚 ルール詳細分析:")
    
    # ルールカテゴリ分析
    categories = {}
    total_trigger_conditions = 0
    total_examples = 0
    
    for rule in rules:
        rule_id = rule.get('id', '')
        category = rule_id.split('-')[0] if '-' in rule_id else 'other'
        
        if category not in categories:
            categories[category] = []
        categories[category].append(rule_id)
        
        # トリガー条件数をカウント
        trigger = rule.get('trigger', {})
        if 'form' in trigger:
            total_trigger_conditions += len(trigger['form'])
        if 'lemma' in trigger:
            total_trigger_conditions += len(trigger['lemma'])
        if 'examples' in rule:
            total_examples += len(rule['examples'])
    
    print(f"   - ルールカテゴリ: {len(categories)}種類")
    for category, rule_ids in categories.items():
        print(f"     {category}: {len(rule_ids)}個")
    
    print(f"   - 総トリガー条件数: {total_trigger_conditions}")
    print(f"   - 総例文数: {total_examples}")
    
    # 現在のPythonコードでの活用度
    print(f"\n❌ 現在の活用状況:")
    print(f"   - JSONファイル読み込み: ✅")
    print(f"   - ルール数取得: ✅ (21個)")
    print(f"   - カテゴリ分類: ✅ (6種類)")
    print(f"   - 実際の分解での活用: ❌❌❌")
    print(f"   - パターンマッチング: ❌❌❌")
    print(f"   - 例文データ活用: ❌❌❌")
    
    print(f"\n🤦‍♀️ 無駄な現状:")
    print(f"   - 1018行の詳細ルール → 使用率約1%")
    print(f"   - 21,586バイトのデータ → ほぼ無視")
    print(f"   - 数百のトリガー条件 → 未活用")
    
    return rules_data

def show_unused_potential():
    """未活用ポテンシャルの表示"""
    
    rules_data = analyze_json_usage()
    
    print(f"\n🔥 未活用の宝の山:")
    print("-" * 40)
    
    rules = rules_data.get('rules', [])
    
    # サンプルルールの詳細表示
    for i, rule in enumerate(rules[:3]):
        print(f"\n例{i+1}: {rule.get('id', 'unknown')}")
        print(f"  トリガー: {rule.get('trigger', {})}")
        print(f"  割り当て: {rule.get('assign', {})}")
        if 'examples' in rule:
            print(f"  例文数: {len(rule['examples'])}")
        if 'notes' in rule:
            print(f"  注記: {rule['notes']}")
    
    print(f"\n💡 これらの詳細ルールが全て未活用！")

def propose_real_integration():
    """真の統合プランを提案"""
    
    print(f"\n🚀 真の統合プラン:")
    print("-" * 40)
    
    print("Phase 1: 全ルールの完全解析")
    print("   - 1018行の全ルールをPythonで解釈")
    print("   - トリガー条件の実装")
    print("   - パターンマッチングエンジン構築")
    
    print("\nPhase 2: 例文データの活用")
    print("   - JSON内の全例文を学習データ化")
    print("   - パターン認識アルゴリズム実装")
    print("   - 自動分類精度の向上")
    
    print("\nPhase 3: 真の汎用エンジン")
    print("   - 1000行ルール → 完全活用")
    print("   - 88例文 → 無限例文対応")
    print("   - 手動修正 → 自動学習")
    
    print(f"\n🎯 効果予想:")
    print("現在: JSONファイル活用率 1%")
    print("統合後: JSONファイル活用率 95%+")
    print("= 真の大幅バージョンアップ！")

if __name__ == "__main__":
    show_unused_potential()
    propose_real_integration()
    
    print(f"\n😅 現状の正直な告白:")
    print("1000行のJSONファイルは完全に宝の持ち腐れです！")
    print("真の統合システムを構築すべきでした！")
