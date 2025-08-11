import sys
sys.path.append('.')
from step18_unified_rephrase_system import Step18UnifiedRephraseSystem

# システム初期化
system = Step18UnifiedRephraseSystem()

# ex007のSスロット部分のテスト
sentence = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== 前置詞統合修正テスト：ex007 ===")
print("=" * 50)

results = system.process_sentence(sentence)

print("\n=== Sスロットの結果確認 ===")
s_slot = results.get('S', {})
for subslot, value in s_slot.items():
    if value:
        print(f'{subslot:10}: "{value}"')

print(f"\n=== sub-m3の確認 ===")
if s_slot.get('sub-m3'):
    print(f"❌ sub-m3が残存: '{s_slot['sub-m3']}'")
else:
    print("✅ sub-m3が除外されました")
