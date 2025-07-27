
import json
import openpyxl
import re

# ✅ JSON読込
with open("example_2_ver2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("slottext.json", "r", encoding="utf-8") as f:
    slottext_rules = json.load(f)["rules"]

# ✅ 補助テキスト自動補完
def infer_slot_text(phrase):
    phrase_lc = phrase.lower()
    if phrase_lc.strip() == "at the very last second":
        return "最後の瞬間に"
    for rule in slottext_rules:
        condition = rule["condition"]
        guidance = rule["guidance"]
        if rule.get("condition_type") == "regex":
            if re.search(condition, phrase_lc):
                return guidance
        elif condition in phrase_lc:
            return guidance
    return ""

# ✅ Excelロード
wb = openpyxl.load_workbook("DB_know_ex001.xlsx")

# ✅ masterシート書き込み（改良版: 列ずれ防止・確認ログ）
master_sheet = wb["example_master"]
構文ID = data.get("構文ID", "")
V_group_key = data.get("V_group_key", "")
V_display = data.get("V_display", "")
example_id = data.get("example_id", "")
original = data.get("original", "")
translated = data.get("original_translated", "")

values = [
    構文ID or "",
    V_group_key or "",
    V_display or "",
    example_id or "",
    original or "",
    translated or ""
]

print(f"✅ 確認: {values}")
master_sheet.append(values)

# ✅ slot_phrase_pool（重複防止あり）
phrase_sheet = wb["slot_phrase_pool"]
existing_pairs = set((row[0].value, row[1].value) for row in phrase_sheet.iter_rows(min_row=2))
for slot in data["slot_data"]:
    key = (slot["slot"], slot["phrase"])
    if key not in existing_pairs:
        phrase_sheet.append(list(key))
        existing_pairs.add(key)

# ✅ phrase_type_rules
type_sheet = wb["phrase_type_rules"]
for slot in data["slot_data"]:
    type_sheet.append([slot["phrase"], slot["type"]])

# ✅ slottext_rules（typeがword限定）
text_sheet = wb["slottext_rules"]
for slot in data["slot_data"]:
    if slot["type"] == "word":
        slot_text = slot.get("slot_text", "") or infer_slot_text(slot["phrase"])
        text_sheet.append([slot["phrase"], slot_text])

# ✅ slot_structure
structure_sheet = wb["slot_structure"]
used_slots = [slot["slot"] for slot in data["slot_data"]]
structure_sheet.append([",".join(used_slots)])

# ✅ subslot処理
mapping_sheet = wb["subslot_mapping"]
subtext_sheet = wb["subslot_structure"]
for slot in data["slot_data"]:
    if slot["type"] == "clause" and "subslots" in slot:
        mapping_sheet.append([slot["slot"]])
        for sub in slot["subslots"]:
            mapping_sheet.append(["", sub.get("slot", ""), sub.get("phrase", ""), sub.get("type", "")])
            if sub.get("type") == "word":
                subtext_sheet.append([sub["phrase"], sub.get("slot_text", "")])

#LOCK: output_path = "DB_know_ex001_updated.xlsx"
output_path = "DB_know_ex001_updated.xlsx"
wb.save(output_path)

with open("log_output.txt", "w", encoding="utf-8") as log:
    log.write(f"✅ DB updated and saved to: {output_path}\n")
    log.write(f"Written master row: {values}\n")
