
import json
import openpyxl
import re
import sys

# ✅ JSONファイル指定（コマンド引数対応）
json_file = sys.argv[1] if len(sys.argv) > 1 else "example_3.json"
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

with open("slottext.json", "r", encoding="utf-8") as f:
    slottext_rules = json.load(f)["rules"]

# ✅ 補助テキスト自動補完（動的補助判定を追加）
def infer_slot_text(phrase, subslots=None, idx=None):
    phrase_lc = phrase.lower()
    texts = []

    for rule in slottext_rules:
        condition = rule["condition"]
        guidance = rule["guidance"]
        if re.search(condition, phrase_lc, re.IGNORECASE):
            texts.append(guidance)

    if "be動詞過去" in texts and re.search(r"^was\s+\w+ing", phrase_lc):
        texts = [t for t in texts if t != "be動詞過去"]

    # 🌟 動的補助判定（aux に基づく過去形抑制 + 完了形付与）
    if subslots is not None and idx is not None:
        if idx > 1:
            prev_sub = subslots[idx - 2]  # idx は1始まり
            prev_phrase = prev_sub.get("phrase", "").lower()
            if prev_phrase in ["have", "has"]:
                texts = [t for t in texts if t != "過去形"]
                texts.append("現在完了")
            elif prev_phrase == "had":
                texts = [t for t in texts if t != "過去形"]
                texts.append("過去完了")

    return "、".join(sorted(set(texts)))

# ✅ Excelロード
wb = openpyxl.load_workbook("DB_know_ex001.xlsx")
master_sheet = wb["example_master"]
phrase_sheet = wb["slot_phrase_pool"]
type_sheet = wb["phrase_type_rules"]
text_sheet = wb["slottext_rules"]
structure_sheet = wb["slot_structure"]
mapping_sheet = wb["subslot_mapping"]
substructure_sheet = wb["subslot_structure"]

# ✅ master_sheet 出力
構文ID = data.get("構文ID", "")
V_group_key = data.get("V_group_key", "")
example_id = data.get("例文ID", "")
original = data.get("原文", "")
values = [構文ID or "", V_group_key or "", example_id or "", original or ""]
master_sheet.append(values)

# ✅ phrase_pool 重複防止付き出力
existing_pairs = set(((row[1].value or "").strip(), (row[2].value or "").strip()) for row in phrase_sheet.iter_rows(min_row=2))
for slot in data["slot_data"]:
    key = (slot["slot"].strip(), slot["phrase"].strip())
    if key not in existing_pairs:
        phrase_sheet.append([V_group_key, slot["slot"], slot["phrase"]])
        existing_pairs.add(key)

# ✅ type_sheet 出力
for slot in data["slot_data"]:
    type_sheet.append([slot["phrase"], slot["type"]])

# ✅ text_sheet 出力
for slot in data["slot_data"]:
    if slot["type"] == "word":
        slot_text = slot.get("slot_text", "") or infer_slot_text(slot["phrase"])
        text_sheet.append([slot["phrase"], slot_text])

# ✅ structure_sheet 出力
for slot in data["slot_data"]:
    structure_sheet.append([
        slot["phrase"],
        slot["slot"],
        slot["type"],
        slot.get("slot_text", "") or (infer_slot_text(slot["phrase"]) if slot["type"] == "word" else "")
    ])

# ✅ mapping_sheet と substructure_sheet 出力
for slot in data["slot_data"]:
    if slot.get("type") == "clause" and "subslots" in slot:
        for idx, sub in enumerate(slot["subslots"], start=1):
            mapping_sheet.append([
                slot.get("phrase", ""),
                sub.get("slot", ""),
                sub.get("phrase", "")
            ])

            substructure_sheet.append([
                V_group_key,
                slot.get("phrase", ""),
                sub.get("slot", ""),
                sub.get("phrase", ""),
                infer_slot_text(sub.get("phrase", ""), slot["subslots"], idx),
                idx
            ])

# ✅ 保存
output_path = "DB_know_ex001_updated.xlsx"
wb.save(output_path)

with open("log_output.txt", "w", encoding="utf-8") as log:
    log.write(f"✅ DB updated and saved to: {output_path}\n")
    log.write(f"Written master row: {values}\n")
