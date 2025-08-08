"""
Rephraseルール辞書システムの仕組み解説
ChatGPTが作成したルール辞書をどうやってAIが活用するか
"""

# 1. ルール辞書の構造分析
import json
import re

def analyze_rule_system():
    """ルール辞書システムの仕組み解説"""
    
    print("🔍 Rephraseルール辞書システムの仕組み")
    print("=" * 50)
    
    # ルール辞書読み込み
    with open('rephrase_rules_v1.0.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    print("📋 1. ルール辞書の基本構造:")
    print(f"   - バージョン: {rules['version']}")
    print(f"   - 言語: {rules['language']}")
    print(f"   - スロット順序: {rules['slot_order']}")
    print(f"   - ルール数: {len(rules['rules'])}")
    
    print("\n🎯 2. ルールの種類分析:")
    rule_types = {}
    for rule in rules['rules']:
        rule_id = rule['id']
        category = rule_id.split('-')[0]  # "aux-have" -> "aux"
        if category not in rule_types:
            rule_types[category] = []
        rule_types[category].append(rule_id)
    
    for category, rule_ids in rule_types.items():
        print(f"   - {category.upper()}系: {len(rule_ids)}個 {rule_ids[:3]}{'...' if len(rule_ids) > 3 else ''}")
    
    return rules

def explain_matching_process():
    """ルールマッチングプロセスの説明"""
    
    print("\n⚙️ 3. AIによるルールマッチングプロセス:")
    print("   Step 1: 文を単語に分解")
    print("   Step 2: 各単語に対してルールを優先度順で検索")
    print("   Step 3: マッチしたルールでスロット分類")
    print("   Step 4: PhraseType判定")
    print("   Step 5: 表示順序でソート")
    
    # 実例で説明
    example_sentence = "I can't afford it."
    print(f"\n📝 実例: '{example_sentence}'")
    
    # ステップ1: 分解
    words = example_sentence.replace(".", "").split()
    print(f"   分解: {words}")
    
    # ステップ2-3: 仮想的なマッチング
    matches = [
        ("I", "subject-pronoun", "S", "word"),
        ("can't", "aux-modal-neg", "Aux", "word"),
        ("afford", "verb-transitive", "V", "word"),
        ("it", "object-pronoun", "O1", "word")
    ]
    
    for word, rule_id, slot, phrase_type in matches:
        print(f"   '{word}' → {rule_id} → {slot}({phrase_type})")

def explain_rule_structure():
    """ルール構造の詳細説明"""
    
    print("\n📐 4. ルール構造の詳細:")
    
    # サンプルルールを表示
    with open('rephrase_rules_v1.0.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    # 助動詞ルールの例
    aux_rule = None
    for rule in rules['rules']:
        if rule['id'] == 'aux-have':
            aux_rule = rule
            break
    
    if aux_rule:
        print("   例: 助動詞'have'のルール:")
        print(f"   {{")
        print(f"     'id': '{aux_rule['id']}',")
        print(f"     'priority': {aux_rule['priority']},")
        print(f"     'trigger': {aux_rule['trigger']},")
        print(f"     'assign': {aux_rule['assign']}")
        print(f"   }}")
        
        print("\n   解説:")
        print("   - id: ルールの識別子")
        print("   - priority: マッチング優先度（高い数字が優先）")
        print("   - trigger: どの単語にマッチするかの条件")
        print("   - assign: マッチした時の分類先")

def explain_ai_decision_process():
    """AIの判断プロセス説明"""
    
    print("\n🧠 5. AIの判断プロセス:")
    print("   A. 辞書ルールによる自動分類")
    print("      → 明確なルールがある場合（代名詞、助動詞等）")
    print("   ")
    print("   B. 文脈による推論")
    print("      → ルールが曖昧な場合の文法的判断")
    print("   ")
    print("   C. パターン認識")
    print("      → 類似例文からの学習的分類")
    
    print("\n🔄 6. エラー修正のフィードバックループ:")
    print("   ユーザー指摘 → ルール修正 → 再処理 → 精度向上")
    print("   ")
    print("   例: 'got married with'の修正")
    print("   指摘前: [V: 'got married with']")
    print("   指摘後: [Aux: 'got'] + [V: 'married with']")
    print("   → ルール辞書に新しいパターン追加")

def demonstrate_rule_application():
    """ルール適用の実演"""
    
    print("\n🎬 7. ルール適用の実演:")
    
    test_sentences = [
        "You got me!",
        "Where did you get it?", 
        "Would you hold the line, please?"
    ]
    
    for sentence in test_sentences:
        print(f"\n例文: '{sentence}'")
        
        # 簡易的な分解シミュレーション
        if sentence == "You got me!":
            print("   You → subject-pronoun → S(word)")
            print("   got → verb-past → V(word)")
            print("   me → object-pronoun → O1(word)")
            
        elif sentence == "Where did you get it?":
            print("   Where → question-adverb → M3(word)")
            print("   did → aux-do → Aux(word)")
            print("   you → subject-pronoun → S(word)")
            print("   get → verb-base → V(word)")
            print("   it → object-pronoun → O1(word)")
            
        elif sentence == "Would you hold the line, please?":
            print("   Would → aux-modal → Aux(word)")
            print("   you → subject-pronoun → S(word)")
            print("   hold → verb-base → V(word)")
            print("   the line → noun-phrase → O1(phrase)")
            print("   please → adverb-politeness → M2(word)")

if __name__ == "__main__":
    rules = analyze_rule_system()
    explain_matching_process()
    explain_rule_structure()
    explain_ai_decision_process()
    demonstrate_rule_application()
    
    print("\n✅ まとめ:")
    print("   ChatGPTが作成したルール辞書 →")
    print("   AIが文を分析してルールマッチング →") 
    print("   自動的にスロット分類 →")
    print("   Excel形式で出力")
    print("   ")
    print("   🔧 ユーザーの修正指摘により")
    print("   ルール辞書が進化して精度向上！")
