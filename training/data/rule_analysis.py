print("=== Rephrase Engine の実装内容分析 ===")
print()

rule_categories = {
    "基本ルール辞書": {
        "内容": ["cognitive_verbs", "modal_verbs", "be_verbs", "have_verbs", "copular_verbs", "ditransitive_verbs"],
        "例": "think, believe, know, will, can, am, is, have, become, give",
        "行数": 30
    },
    "疑問文ルール": {
        "内容": ["wh疑問文", "do疑問文", "be疑問文", "modal疑問文", "yes/no疑問文"],
        "例": "What do you think? / Do you know? / Are you ready?",
        "行数": 250
    },
    "文型パターン": {
        "内容": ["SVO", "SVC", "受動態", "完了形", "Modal+動詞", "複文"],
        "例": "I love you / I am happy / I have done / I can go",
        "行数": 200
    },
    "修飾語ルール": {
        "内容": ["句動詞", "前置詞句", "副詞", "時間表現", "場所表現", "方法表現"],
        "例": "turn on / from home / quickly / every day / at school",
        "行数": 180
    },
    "複文処理": {
        "内容": ["that節", "認知動詞+節", "関係詞", "疑問詞節"],
        "例": "I think that he is smart / I know what he wants",
        "行数": 150
    },
    "命令文ルール": {
        "内容": ["呼びかけ", "please処理", "命令動詞", "目的語分離"],
        "例": "You, give it to me please / John, sit down",
        "行数": 150
    },
    "語彙認識": {
        "内容": ["spaCy統合", "品詞判定", "語幹抽出", "未知語処理"],
        "例": "recovered → recover (VERB) / entrepreneurship → 認識済み",
        "行数": 50
    }
}

total_rules = 0
total_lines = 0

for category, info in rule_categories.items():
    rule_count = len(info["内容"])
    lines = info["行数"]
    total_rules += rule_count
    total_lines += lines
    
    print(f"{category:12} : {rule_count:2}種類のルール ({lines:3}行)")
    print(f"             例: {info['例']}")
    print()

print("=" * 50)
print(f"総実装ルール数: {total_rules}種類")
print(f"総実装行数  : {total_lines}行 (推定)")
print(f"実際の行数  : 1069行")
print()
print("🎯 結論: エンジン自体が巨大なルール辞書になっている！")
