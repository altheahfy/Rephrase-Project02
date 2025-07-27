
import json
import openpyxl
import sys
import re

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)


# Load slottext rules
with open("slottext_regex.json", "r", encoding="utf-8") as f:
    slottext_rules = json.load(f)["rules"]

def infer_slot_text(phrase):
    phrase_lc = phrase.lower()
    for rule in slottext_rules:
        condition = rule["condition"]
        guidance = rule["guidance"]
                if rule.get("condition_type") == "regex":
            if re.search(condition, phrase_lc):
                return guidance
        elif condition in phrase_lc:
            return guidance
    return ""

wb = openpyxl.load_workbook(sys.argv[2])

# example_master
master_sheet = wb["example_master"]
master_sheet.append([
    data.get("構文ID", ""),
    data.get("V_group_key", ""),
    data.get("V_display", ""),
    data.get("example_id", "ex000"),
    data.get("original", "").replace("\n", " "),
    data.get("original_translated", "") if "original_translated" in data else ""
])

# slot_phrase_pool
phrase_sheet = wb["slot_phrase_pool"]
for slot in data["slot_data"]:
    phrase_sheet.append([data["V_group_key"], slot["slot"], slot["phrase"]])

# phrase_type_rules
type_sheet = wb["phrase_type_rules"]
for slot in data["slot_data"]:
    type_sheet.append([slot["phrase"], slot["type"]])

# slottext_rules (typeがwordのもののみ)
text_sheet = wb["slottext_rules"]
for slot in data["slot_data"]:
    if slot["type"] == "word":
        slot_text = slot.get("slot_text", "") or infer_slot_text(slot["phrase"])
        text_sheet.append([slot["phrase"], slot_text])

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
            mapping_sheet.append(["", sub.get("slot", ""), sub.get("phrase", ""), sub.get("type", "")])
            if sub.get("type") == "word":
                subtext_sheet.append([sub["phrase"], sub.get("slot_text", "")])

# 保存とログ出力
output_path = sys.argv[2].replace(".xlsx", "_updated.xlsx")
wb.save(output_path)
with open("log_output.txt", "w", encoding="utf-8") as log:
    log.write(f"✅ DB updated and saved to: {output_path}\n")