import pandas as pd
import os
from datetime import datetime

FILE = "data/history.csv"

def save_history(prediction, confidence, risk, trust):
    os.makedirs("data", exist_ok=True)

    entry = {
        "timestamp": datetime.now(),
        "prediction": prediction,
        "confidence": confidence,
        "risk_level": risk,
        "trust_score": trust
    }

    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, pd.DataFrame([entry])])
    else:
        df = pd.DataFrame([entry])

    df.to_csv(FILE, index=False)

def load_history():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame()
