import joblib
from backend.preprocess import clean_text

model = joblib.load("model/fake_news_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

def predict_news(article):
    cleaned = clean_text(article)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    confidence = max(model.predict_proba(vector)[0])
    return prediction, round(confidence * 100, 2)
