from Rephrase_Parsing_Engine import RephraseParsingEngine

engine = RephraseParsingEngine()

# 語彙認識テスト
test_words = ['recovered', 'quickly', 'unknown_word_12345', 'injury', 'lie', 'bed']

print("=== spaCy語彙認識テスト ===")
for word in test_words:
    is_known = engine.is_word_recognized(word)
    print(f"{word}: {'✅認識済み' if is_known else '❌未知語'}")

# 従来の解析も確認
print("\n=== 従来解析（spaCy語彙認識付き）===")
result = engine.analyze_sentence('He has recovered quickly from a serious injury.')
for slot, values in result.items():
    for v in values:
        print(f"{v['value']}_{slot}_{v.get('order', '?')}")
