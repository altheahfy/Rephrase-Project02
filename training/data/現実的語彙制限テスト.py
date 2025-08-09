# 実際の語彙制限テスト - 厳しい現実版

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

# エンジン初期化
engine = RephraseParsingEngine()

print("=== 動詞の語彙制限テスト ===\n")

# 動詞のテスト（現在形・過去形・過去分詞）
verb_tests = [
    # 現在形（辞書にない）
    ("I complete the task.", "complete"),
    ("She investigates the case.", "investigates"), 
    ("They analyze the data.", "analyze"),
    
    # 過去形（-edじゃない不規則）
    ("I ran to school.", "ran"),
    ("She sang a song.", "sang"),
    ("They bought a car.", "bought"),
    
    # 過去分詞（-edじゃない不規則で辞書にない）
    ("I have run five miles.", "run"),
    ("She has sung beautifully.", "sung"), 
    ("They have bought it.", "bought"),
    
    # 現在分詞（-ing）
    ("I am running now.", "running"),
    ("She is analyzing data.", "analyzing"),
]

for sentence, target_word in verb_tests:
    print(f"文: {sentence}")
    print(f"問題語: {target_word}")
    
    # 語の種類判定テスト
    if target_word.endswith('ed'):
        recognition = "✅ -edルールで認識"
    elif engine.looks_like_past_participle(target_word):
        recognition = "✅ 不規則辞書で認識"
    else:
        recognition = "❌ 認識不可（語彙制限）"
    
    print(f"認識状況: {recognition}")
    
    try:
        result = engine.analyze_sentence(sentence)
        if result:
            print("解析: 成功")
        else:
            print("解析: 失敗")
    except Exception as e:
        print(f"解析: エラー - {e}")
    
    print("-" * 40)

print("\n=== 名詞・形容詞・副詞の語彙制限テスト ===\n")

# 名詞・形容詞・副詞のテスト
other_tests = [
    ("The sophisticated analysis is complete.", ["sophisticated", "analysis"]),
    ("She works efficiently every day.", ["efficiently"]),
    ("The comprehensive investigation concluded.", ["comprehensive", "investigation"]),
    ("He speaks fluently in three languages.", ["fluently"]),
    ("The preliminary results are encouraging.", ["preliminary", "encouraging"]),
]

for sentence, problem_words in other_tests:
    print(f"文: {sentence}")
    print(f"問題語: {', '.join(problem_words)}")
    print("認識状況: ❌ 現在のシステムでは品詞判定不可")
    print("-" * 40)

print("\n=== 実際の16,000例文想定テスト ===\n")

# 実際の英語教材でよく出る複雑な文
realistic_tests = [
    "The environmental scientist conducted a comprehensive investigation.",
    "Students frequently encounter challenging mathematical equations.",  
    "The pharmaceutical company developed innovative therapeutic solutions.",
    "Technological advancement significantly influences contemporary society.",
    "Archaeological discoveries provide valuable historical insights.",
]

for sentence in realistic_tests:
    print(f"文: {sentence}")
    words = sentence.replace('.', '').replace(',', '').split()
    
    recognized_words = 0
    total_words = len(words)
    
    for word in words:
        word_lower = word.lower()
        # 超基本語彙（仮定）
        basic_vocab = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 
                      'do', 'does', 'did', 'will', 'would', 'can', 'could', 'should',
                      'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her']
        
        if word_lower in basic_vocab:
            recognized_words += 1
        elif word.endswith('ed'):
            recognized_words += 1
        elif engine.looks_like_past_participle(word):
            recognized_words += 1
    
    coverage = (recognized_words / total_words) * 100
    print(f"語彙カバー率: {coverage:.1f}% ({recognized_words}/{total_words}語)")
    
    if coverage < 60:
        print("❌ 解析困難レベル")
    elif coverage < 80:
        print("⚠️ 解析不完全")
    else:
        print("✅ 解析可能")
    
    print("-" * 50)
