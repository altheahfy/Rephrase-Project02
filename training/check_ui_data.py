import json

with open('data/slot_order_data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('置き換え後のslot_order_data2.jsonでwhatグループのdidとwhereを確認:')
for entry in data:
    if entry.get('V_group_key') == 'what' and entry.get('SlotPhrase') in ['did', 'Where']:
        print(f"Phrase: {entry.get('SlotPhrase')}, Slot: {entry.get('Slot')}, Order: {entry.get('Slot_display_order')}")
