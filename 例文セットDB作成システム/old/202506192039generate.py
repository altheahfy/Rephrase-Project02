
import pandas as pd
import sys
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def extract_features(slotphrase):
    doc = nlp(slotphrase)
    features = []
    for token in doc:
        features.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "dep": token.dep_,
            "head_text": token.head.text,
            "head_pos": token.head.pos_,
        })
    return features

def predict_slot(features):
    # ダミー予測：全トークン text を結合し O1 スロットと仮定
    slot_predictions = [("O1", " ".join([f["text"] for f in features]))]
    return slot_predictions

def assign_order(rows):
    result = []
    grouped = defaultdict(list)
    for row in rows:
        key = row["例文ID"]
        grouped[key].append(row)

    slot_priority = {
        "S": 1, "V": 2, "O1": 3, "O2": 4, "C1": 5, "C2": 6,
        "M1": 7, "M2": 8, "M3": 9, "Aux": 10
    }

    for key, group in grouped.items():
        group.sort(key=lambda x: slot_priority.get(x["PredictedSlotID"], 99))
        for order, row in enumerate(group, 1):
            row["Slot_display_order"] = order
            result.append(row)
    return result

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "例文入力元.xlsx"
    output_file = "例文入力_ML予測結果_with_order.xlsx"

    wb = pd.read_excel(input_file)
    rows = []

    for _, row in wb.iterrows():
        slotphrase = str(row.get("SlotPhrase", "")).strip()
        if not slotphrase:
            continue

        features = extract_features(slotphrase)
        predictions = predict_slot(features)

        for slot_id, slot_elem in predictions:
            rows.append({
                "構文ID": row.get("構文ID", ""),
                "例文ID": row.get("例文ID", ""),
                "Slot": row.get("Slot", ""),
                "SlotPhrase": slotphrase,
                "PredictedSlotID": slot_id,
                "PredictedSlotElement": slot_elem
            })

    rows_with_order = assign_order(rows)
    df_out = pd.DataFrame(rows_with_order)
    df_out.to_excel(output_file, index=False)
    print(f"✅ ML予測結果（順序付与済）ファイルを出力しました: {output_file}")

if __name__ == "__main__":
    main()
