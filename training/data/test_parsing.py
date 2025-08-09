from Rephrase_Parsing_Engine import RephraseParsingEngine

engine = RephraseParsingEngine()
result = engine.analyze_sentence('He has recovered quickly from a serious injury.')

print("=== 解析結果 ===")
for slot, values in result.items():
    for v in values:
        print(f"{v['value']}_{slot}_{v.get('order', '?')}")
