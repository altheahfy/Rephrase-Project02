
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
    output_file = "例文入力_自動展開_改良_gkh_trigger_final_clean_fixed.xlsx"

    wb = pd.read_excel(input_file)
    rows = []
    last_kid = ""
    last_eid = ""
    last_vkey = ""

    for _, row in wb.iterrows():
        values = {col: safe_str(row.get(col)).strip() for col in ["PhraseType", "SubslotID", "SubslotElement", "Slot_display_order"]}
        if not all(v in ["", "0"] for v in values.values()):
            continue

        kid = safe_str(row.get("構文ID")).strip()
        eid = safe_str(row.get("例文ID")).strip()
        vkey = safe_str(row.get("V_group_key")).strip()

        if kid: last_kid = kid
        if eid: last_eid = eid
        if vkey: last_vkey = vkey

        slot = safe_str(row.get("Slot")).strip()

        base = {
            "構文ID": kid,
            "例文ID": eid,
            "V_group_key": vkey,
            "原文": safe_str(row.get("原文")),
            "Slot": slot,
            "SlotPhrase": safe_str(row.get("SlotPhrase")),
            "PhraseType": safe_str(row.get("PhraseType")),
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
                **base,
                "原文": "",
                "SubslotID": sub_id,
                "SubslotElement": sub_elem,
                "display_order": display_order
            })
            display_order += 1

    for r in rows:
        if not r["構文ID"]:
            r["構文ID"] = last_kid
        if not r["例文ID"]:
            r["例文ID"] = last_eid
        if not r["V_group_key"]:
            r["V_group_key"] = last_vkey

    df_out = pd.DataFrame(rows)
    slot_order = ["M1", "S", "Aux", "M2", "V", "C1", "O1", "O2", "C2", "M3"]
    df_out["Slot_display_order"] = 0
    for eid, group in df_out[df_out["SubslotID"] == ""].groupby("例文ID"):
        ordered = group.copy()
        ordered["order_idx"] = ordered["Slot"].apply(lambda s: slot_order.index(s) if s in slot_order else 99)
        ordered = ordered.sort_values("order_idx").reset_index()
        for i, idx in enumerate(ordered["index"]):
            order_val = i + 1
            df_out.at[idx, "Slot_display_order"] = order_val
            sid = df_out.at[idx, "Slot"]
            mask = (df_out["例文ID"] == eid) & (df_out["Slot"] == sid) & (df_out["SubslotID"] != "")
            df_out.loc[mask, "Slot_display_order"] = order_val

    cols = list(df_out.columns)
    cols.remove("Slot_display_order")
    cols = cols[:-1] + ["Slot_display_order", cols[-1]]
    df_out = df_out[cols]

    df_out.to_excel(output_file, index=False)
    print(f"✅ 自動展開ファイルを出力しました: {output_file}")

if __name__ == "__main__":
    main()
