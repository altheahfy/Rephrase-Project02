
import json
import openpyxl

with open("example_2_ver2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

wb = openpyxl.load_workbook("DB_know_ex001.xlsx")

# example_master
master_sheet = wb["example_master"]
master_sheet.append([
    data.get("構文ID", ""),
    data.get("V_group_key", ""),
    data.get("V_display", ""),
    data.get("example_id", "ex000"),
    data.get("original", ""),
    data.get("original_translated", "")
])

# slot_phrase_pool
phrase_sheet = wb["slot_phrase_pool"]
for slot in data["slot_data"]:
    phrase_sheet.append([slot["slot"], slot["phrase"]])

# phrase_type_rules
type_sheet = wb["phrase_type_rules"]
for slot in data["slot_data"]:
    type_sheet.append([slot["phrase"], slot["type"]])

# slottext_rules (typeがwordのもののみ)
text_sheet = wb["slottext_rules"]
for slot in data["slot_data"]:
    if slot["type"] == "word":
        text_sheet.append([slot["phrase"], slot.get("slot_text", "")])

# slot_structure
structure_sheet = wb["slot_structure"]
used_slots = [slot["slot"] for slot in data["slot_data"]]
structure_sheet.append([",".join(used_slots)])

# subslot_mapping / subslot_text_rules
mapping_sheet = wb["subslot_mapping"]
subtext_sheet = wb["subslot_structure"]
for slot in data["slot_data"]:
    if slot["type"] == "clause" and "subslots" in slot:
        mapping_sheet.append([slot["slot"]])
        for sub in slot["subslots"]:
            mapping_sheet.append(["", sub["slot"], sub["phrase"], sub["type"]])
            if sub["type"] == "word":
                subtext_sheet.append([sub["phrase"], sub.get("slot_text", "")])

# 保存とログ出力
output_path = "DB_know_ex001.xlsx"
wb.save(output_path)
with open("log_output.txt", "w", encoding="utf-8") as log:
    log.write(f"✅ DB updated and saved to: {output_path}\n")
