from Rephrase_Parsing_Engine import RephraseParsingEngine

# 従来の解析テスト（spaCyは警告を出すが動作する）
print("=== 従来解析テスト（spaCy統合版）===")
engine = RephraseParsingEngine()
result = engine.analyze_sentence('He has recovered quickly from a serious injury.')

for slot, values in result.items():
    for v in values:
        print(f"{v['value']}_{slot}_{v.get('order', '?')}")

print(f"\nエンジン名: {engine.engine_name}")
print(f"spaCy利用可能: {engine.nlp is not None}")
