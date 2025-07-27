
import json
from openpyxl import load_workbook

def add_example_to_db(template_path, json_path, output_path):
    wb = load_workbook(template_path)

    # テンプレート列定義（参照用、チェックロジックに発展可能）
    template_columns = {
        "slot_phrase_pool": ['V_group_key', 'Slot', 'SlotPhrase'],
        "phrase_type_rules": ['SlotPhrase', 'PhraseType'],
        "slottext_rules": ['SlotPhrase', 'SlotText'],
        "slot_structure": ['SlotPhrase', 'Slot', 'PhraseType', 'SlotText'],
        "subslot_mapping": ['SlotPhrase', 'Subslot', 'Subphrase'],
        "subslot_structure": ['V_group_key', 'Slot', 'SubslotID', 'SubslotElement', 'SubslotText']
    }

    # JSONファイル読み込み
    with open(json_path, "r", encoding="utf-8") as f:
        example = json.load(f)

    v_key = example["V_group_key"]
    slots = example["Slots"]
    subslots = example["Subslots"]

    for slot, data in slots.items():
        wb["slot_phrase_pool"].append([v_key, slot, data["SlotPhrase"]])

    for slot, data in slots.items():
        wb["phrase_type_rules"].append([f"{v_key}_{slot}", data["PhraseType"]])

    for slot, data in slots.items():
        if "SlotText" in data and data["SlotText"]:
            wb["slottext_rules"].append([f"{v_key}_{slot}", data["SlotText"]])

    for slot, data in slots.items():
        wb["slot_structure"].append([f"{v_key}_{slot}", slot, data["PhraseType"], data.get("SlotText", "")])

    for slot, subs in subslots.items():
        for sub in subs:
            phrase_key = f"{v_key}_{slot}"
            wb["subslot_mapping"].append([phrase_key, sub["SubslotID"], sub["SubslotElement"]])
            wb["subslot_structure"].append([v_key, slot, sub["SubslotID"], sub["SubslotElement"], sub["SubslotText"]])

    wb.save(output_path)

# 使用例
if __name__ == "__main__":
    template_path = "DB_know_ex001.xlsx"
    json_path = "example_5001.json"
    output_path = "DB_know_ex001_with_5001_from_json.xlsx"
    add_example_to_db(template_path, json_path, output_path)
