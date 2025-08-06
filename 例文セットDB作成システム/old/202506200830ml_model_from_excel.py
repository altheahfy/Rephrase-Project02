
import pandas as pd
import spacy
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
import joblib

nlp = spacy.load("en_core_web_sm")

def extract_features(row):
    phrase = str(row["SlotPhrase"]).strip() if pd.notna(row["SlotPhrase"]) else ""
    subslot = str(row["SubslotElement"]).strip()
    doc_phrase = nlp(phrase)
    doc_subslot = nlp(subslot)

    features = {}
    for i, token in enumerate(doc_phrase):
        features.update({f"phrase_{i}_{k}": getattr(token, k) for k in ["text", "lemma_", "pos_", "dep_"]})
    for i, token in enumerate(doc_subslot):
        features.update({f"subslot_{i}_{k}": getattr(token, k) for k in ["text", "lemma_", "pos_", "dep_"]})
    return features

def train_and_predict():
    df = pd.read_excel("例文入力元.xlsx")
    df = df.dropna(subset=["Slot", "SubslotID"])
    df = df[df["SubslotID"] != ""]

    X = [extract_features(row) for _, row in df.iterrows()]
    y_upper = df["Slot"]
    y_sub = df["SubslotID"]

    vec = DictVectorizer(sparse=False)
    X_vec = vec.fit_transform(X)

    clf_upper = DecisionTreeClassifier()
    clf_sub = DecisionTreeClassifier()

    clf_upper.fit(X_vec, y_upper)
    clf_sub.fit(X_vec, y_sub)

    joblib.dump((vec, clf_upper, clf_sub), "ml_model.pkl")

    predictions = []
    for _, row in df.iterrows():
        feat = extract_features(row)
        X_vec_row = vec.transform([feat])
        pred_upper = clf_upper.predict(X_vec_row)[0]
        pred_sub = clf_sub.predict(X_vec_row)[0]

        predictions.append({
            "構文ID": row.get("構文ID", ""),
            "例文ID": row.get("例文ID", ""),
            "V_group_key": row.get("V_group_key", ""),
            "原文": row.get("原文", ""),
            "Slot": pred_upper,
            "SlotPhrase": row.get("SlotPhrase", ""),
            "PhraseType": row.get("PhraseType", ""),
            "SubslotID": pred_sub,
            "SubslotElement": row.get("SubslotElement", ""),
            "Slot_display_order": row.get("Slot_display_order", ""),
            "display_order": row.get("display_order", "")
        })

    df_out = pd.DataFrame(predictions, columns=[
        "構文ID", "例文ID", "V_group_key", "原文", "Slot",
        "SlotPhrase", "PhraseType", "SubslotID", "SubslotElement",
        "Slot_display_order", "display_order"
    ])
    df_out.to_excel("予測結果_例文入力元形式.xlsx", index=False)
    print("✅ 例文入力元形式で予測結果を出力しました。")

if __name__ == "__main__":
    train_and_predict()
