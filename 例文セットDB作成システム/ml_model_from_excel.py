
import pandas as pd
import spacy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# spaCyモデルロード
nlp = spacy.load("en_core_web_sm")

# データ読み込み
data = pd.read_excel("example_data.xlsx")  # 必要に応じてファイル名変更

# 特徴抽出
def extract_features(text):
    doc = nlp(str(text))
    if len(doc) == 0:
        return pd.Series(["", "", ""])
    token = doc[0]
    return pd.Series([
        token.text,
        token.pos_,
        token.dep_
    ])

features = data["SlotPhrase"].apply(extract_features)
features.columns = ["token", "pos", "dep"]
features = pd.get_dummies(features)

# ラベル定義
labels = {
    "Slot": data["Slot"],
    "SlotPhrase": data["SlotPhrase"],
    "PhraseType": data["PhraseType"],
    "SubslotID": data["SubslotID"],
    "SubslotElement": data["SubslotElement"]
}

# 学習・評価関数
def train_and_evaluate(X, y, label_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\n--- {label_name} ---")
    print(classification_report(y_test, y_pred))
    joblib.dump(clf, f"model_{label_name}.pkl")
    return clf

# 各ラベルで学習・保存
models = {}
for label_name, y in labels.items():
    models[label_name] = train_and_evaluate(features, y, label_name)

# 全予測結果を出力
data["Predicted_Slot"] = models["Slot"].predict(features)
data["Predicted_SlotPhrase"] = models["SlotPhrase"].predict(features)
data["Predicted_PhraseType"] = models["PhraseType"].predict(features)
data["Predicted_SubslotID"] = models["SubslotID"].predict(features)
data["Predicted_SubslotElement"] = models["SubslotElement"].predict(features)

data.to_excel("example_data_predicted.xlsx", index=False)

print("✅ 5ラベルのモデル学習・保存・出力完了")
