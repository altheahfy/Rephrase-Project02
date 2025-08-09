# Step 1 テスト: 形態素ルール拡張

from Rephrase_Parsing_Engine import RephraseParsingEngine

print("=== Step 1: 形態素ルール拡張テスト ===\n")

engine = RephraseParsingEngine()

# テスト語彙（様々な難易度）
test_words = [
    "efficiently",      # -ly (副詞)
    "investigation",    # -tion (名詞)
    "beautiful",        # -ful (形容詞)
    "running",          # -ing (動詞)
    "teacher",          # -er (名詞/形容詞)
    "happiness",        # -ness (名詞)
    "scientist",        # -ist (名詞)
    "comprehensive",    # -ive (形容詞)
    "mathematical",     # -al (形容詞)
    "systematic",       # -ic (形容詞)
    "unknown_word"      # 未知語
]

print("📝 単語別解析テスト:")
recognition_count = 0
total_count = len(test_words)

for word in test_words:
    result = engine.analyze_word_morphology(word)
    
    if result['pos'] != 'UNKNOWN':
        recognition_count += 1
        status = "✅"
    else:
        status = "❌"
    
    print(f"  {word:15} -> {result['pos']:20} ({result['confidence']:.2f}) [{result['method']}] {status}")

recognition_rate = (recognition_count / total_count) * 100
print(f"\n📊 認識率: {recognition_count}/{total_count} ({recognition_rate:.1f}%)")

print("\n" + "="*60)

# 実際の文章でテスト
print("\n📖 文章解析テスト:")
test_sentences = [
    "The sophisticated analysis is comprehensive.",
    "She efficiently investigated the mysterious disappearance.", 
    "Students frequently encounter challenging mathematical equations."
]

total_words_in_sentences = 0
recognized_words_in_sentences = 0

for sentence in test_sentences:
    print(f"\n文: {sentence}")
    words = sentence.replace('.', '').replace(',', '').split()
    
    for word in words:
        result = engine.analyze_word_morphology(word)
        total_words_in_sentences += 1
        
        if result['pos'] != 'UNKNOWN':
            recognized_words_in_sentences += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"  {word:15} -> {result['pos']:15} {status}")

sentence_recognition_rate = (recognized_words_in_sentences / total_words_in_sentences) * 100
print(f"\n📊 文章内認識率: {recognized_words_in_sentences}/{total_words_in_sentences} ({sentence_recognition_rate:.1f}%)")

print(f"\n🎯 Step 1 完了:")
print(f"  ✅ 形態素ルール拡張実装完了")
print(f"  📈 語彙認識率: {sentence_recognition_rate:.1f}%")
print(f"  ⏱️ 実装時間: 約20分")
print(f"  💾 追加コード: 約60行")

if sentence_recognition_rate >= 80:
    print(f"  🎉 目標認識率80%以上を達成！")
else:
    print(f"  ⚠️ 認識率改善が必要")
