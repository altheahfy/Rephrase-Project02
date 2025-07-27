
import pandas as pd
import re
import sys

def generate_subslots(slotphrase):
    if not isinstance(slotphrase, str):
        return []
    subslots = []
    tokens = slotphrase.split()
    used = set()
    for i, token in enumerate(tokens):
        if token.lower() in ["who", "which", "that"] and "sub-s" not in used:
            subslots.append(("sub-s", " ".join(tokens[:i+1])))
            used.add("sub-s")
        elif token.lower() in ["had", "has", "have"] and "sub-aux" not in used:
            subslots.append(("sub-aux", token))
            used.add("sub-aux")
        elif re.match(r".*ly$", token.lower()) and "sub-m2" not in used:
            subslots.append(("sub-m2", token))
            used.add("sub-m2")
        elif re.match(r".*ed$|.*en$|.*ing$", token.lower()) and "sub-v" not in used:
            subslots.append(("sub-v", token))
            used.add("sub-v")
    if not any(s[0] == "sub-s" for s in subslots) and tokens:
        subslots.append(("sub-s", tokens[0]))
    ordered_subs = ["sub-m1", "sub-s", "sub-aux", "sub-m2", "sub-v",
                    "sub-c1", "sub-o1", "sub-o2", "sub-c2", "sub-m3"]
    result = []
    for sub_id in ordered_subs:
        elem = ""
        for s_id, s_elem in subslots:
            if s_id == sub_id:
                elem = s_elem
                break
        result.append((sub_id, elem))
    return result

def safe_str(val):
    if pd.isna(val):
        return ""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "例文入力元.xlsx"
    new_example_id = sys.argv[2] if len(sys.argv) > 2 else ""
    output_file = "例文入力_自動展開_改良_idcopy_force.xlsx"

    wb = pd.read_excel(input_file)
    rows = []
    slot_order_counter = {}

    for _, row in wb.iterrows():
        current_example_id = safe_str(row.get("例文ID")).strip()
        if new_example_id and current_example_id != new_example_id:
            continue

        slot = safe_str(row.get("Slot")).strip()
        if slot not in slot_order_counter:
            slot_order_counter[slot] = len(slot_order_counter) + 1
        slot_display_order = slot_order_counter[slot]

        base = {
            "構文ID": safe_str(row.get("構文ID")),
            "例文ID": current_example_id,
            "V_group_key": safe_str(row.get("V_group_key")),
            "原文": safe_str(row.get("原文")),
            "Slot": slot,
            "SlotPhrase": safe_str(row.get("SlotPhrase")),
            "PhraseType": safe_str(row.get("PhraseType")),
            "Slot_display_order": slot_display_order
        }

        rows.append({
            **base,
            "SubslotID": "",
            "SubslotElement": "",
            "display_order": 0
        })

        subslots = generate_subslots(base["SlotPhrase"])
        display_order = 1
        for sub_id, sub_elem in subslots:
            rows.append({
                "構文ID": safe_str(row.get("構文ID")),
                "例文ID": safe_str(row.get("例文ID")),
                "V_group_key": safe_str(row.get("V_group_key")),
                "原文": "",
                "Slot": base["Slot"],
                "SlotPhrase": base["SlotPhrase"],
                "PhraseType": base["PhraseType"],
                "Slot_display_order": base["Slot_display_order"],
                "SubslotID": sub_id,
                "SubslotElement": sub_elem,
                "display_order": display_order
            })
            display_order += 1

    df_out = pd.DataFrame(rows)
    df_out.to_excel(output_file, index=False)
    print(f"✅ 自動展開ファイルを出力しました: {output_file}")

if __name__ == "__main__":
    main()
