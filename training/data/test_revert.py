from Rephrase_Parsing_Engine import RephraseParsingEngine

engine = RephraseParsingEngine()

# 問題の例文1
print("=== He has recovered quickly from a serious injury. ===")
result1 = engine.analyze_sentence('He has recovered quickly from a serious injury.')
for slot, values in result1.items():
    for v in values:
        print(f"{v['value']}_{slot}_{v.get('order', '?')}")

print("\n=== I lie on the bed. ===")
result2 = engine.analyze_sentence('I lie on the bed.')
for slot, values in result2.items():
    for v in values:
        print(f"{v['value']}_{slot}_{v.get('order', '?')}")
