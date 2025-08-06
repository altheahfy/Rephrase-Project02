
import pandas as pd
import spacy
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
import joblib

nlp = spacy.load("en_core_web_sm")

def extract_features(slotphrase):
    doc = nlp(slotphrase)
    features = []
    for token in doc:
        features.append({
            "text": token.text.lower(),
            "lemma": token.lemma_.lower(),
            "pos": token.pos_,
            "dep": token.dep_,
            "head_text": token.head.text.lower(),
            "head_pos": token.head.pos_,
        })
    combined = {f"{i}_{k}": v for i, token_feat in enumerate(features) for k, v in token_feat.items()}
    return combined

def train_model(train_file, model_file="ml_slot_model.pkl"):
    df = pd.read_excel(train_file)
    X = [extract_features(phrase) for phrase in df["SlotPhrase"]]
    
    vec = DictVectorizer(sparse=False)
    X_vec = vec.fit_transform(X)
    
    y_upper = df["正解上位スロットID"]
    y_sub = df["正解サブスロットID"]
    
    clf_upper = DecisionTreeClassifier()
    clf_sub = DecisionTreeClassifier()
    
    clf_upper.fit(X_vec, y_upper)
    clf_sub.fit(X_vec, y_sub)
    
    joblib.dump((vec, clf_upper, clf_sub), model_file)
    print(f"✅ 上位・サブスロットモデルを保存しました: {model_file}")

def predict_slot(model_file, slotphrase):
    vec, clf_upper, clf_sub = joblib.load(model_file)
    feat = extract_features(slotphrase)
    X_vec = vec.transform([feat])
    pred_upper = clf_upper.predict(X_vec)[0]
    pred_sub = clf_sub.predict(X_vec)[0]
    return pred_upper, pred_sub

# 利用例:
# train_model("正解データテンプレート_上位サブ対応.xlsx")
# print(predict_slot("ml_slot_model.pkl", "the thoughtful woman"))
