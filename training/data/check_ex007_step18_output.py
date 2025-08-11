import sys
sys.path.append('.')
from step18_unified_rephrase_system import Step18UnifiedRephraseSystem

# システム初期化
system = Step18UnifiedRephraseSystem()

# ex007の完全処理
sentence = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== ex007の全スロット出力確認 ===")
print("=" * 50)

results = system.process_sentence(sentence)

print("\n=== Step18の全スロット出力 ===")
for slot_name in ['M1', 'S', 'Aux', 'V', 'O1', 'C1', 'C2', 'M2', 'M3']:
    slot_data = results.get(slot_name, {})
    if slot_data and any(slot_data.values()):
        print(f'\n📋 {slot_name}スロット:')
        for subslot, value in slot_data.items():
            if value:
                print(f'  {subslot:10}: "{value}"')
    else:
        print(f'\n📋 {slot_name}スロット: (なし)')

print('\n' + '='*50)
