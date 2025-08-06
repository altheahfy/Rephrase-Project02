
import pandas as pd
import spacy
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
import joblib

nlp = spacy.load("en_core_web_sm")

def extract_features(row):
    # SlotPhrase と SubslotElement の両方を特徴に組み込む
    phrase = str(row["SlotPhrase"]).strip()
    subslot = str(row["SubslotElement"]).strip()
    doc_phrase = nlp(phrase)
    doc_subslot = nlp(subslot)
    
    features = {}
    for i, token in enumerate(doc_phrase):
        features.update({f"phrase_{i}_{k}": getattr(token, k) for k in ["text", "lemma_", "pos_", "dep_"]})
    for i, token in enumerate(doc_subslot):
        features.update({f"subslot_{i}_{k}": getattr(token, k) for k in ["text", "lemma_", "pos_", "dep_"]})
    return features

def train_model(file_path="例文入力元.xlsx", model_path="ml_model.pkl"):
    df = pd.read_excel(file_path, sheet_name=0)
    
    X = [extract_features(row) for _, row in df.iterrows()]
    y_upper = df["上位スロットID"]
    y_sub = df["SubslotID"]
    
    vec = DictVectorizer(sparse=False)
    X_vec = vec.fit_transform(X)
    
    clf_upper = DecisionTreeClassifier()
    clf_sub = DecisionTreeClassifier()
    
    clf_upper.fit(X_vec, y_upper)
    clf_sub.fit(X_vec, y_sub)
    
    joblib.dump((vec, clf_upper, clf_sub), model_path)
    print(f"✅ モデルを保存しました: {model_path}")

def predict(file_path="例文入力元.xlsx", model_path="ml_model.pkl"):
    vec, clf_upper, clf_sub = joblib.load(model_path)
    df = pd.read_excel(file_path, sheet_name=0)
    
    predictions = []
    for _, row in df.iterrows():
        feat = extract_features(row)
        X_vec = vec.transform([feat])
        pred_upper = clf_upper.predict(X_vec)[0]
        pred_sub = clf_sub.predict(X_vec)[0]
        predictions.append({
            "SlotPhrase": row["SlotPhrase"],
            "SubslotElement": row["SubslotElement"],
            "Predicted_上位スロットID": pred_upper,
            "Predicted_SubslotID": pred_sub
        })
    
    df_pred = pd.DataFrame(predictions)
    output_path = "予測結果.xlsx"
    df_pred.to_excel(output_path, index=False)
    print(f"✅ 予測結果ファイルを出力しました: {output_path}")

# 利用例:
# train_model()
# predict()
