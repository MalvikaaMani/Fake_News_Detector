def calculate_risk(prediction, confidence, patterns):
    risk_score = 0

    if prediction == 0:  # Fake
        risk_score += 40

    if confidence > 85:
        risk_score += 20

    risk_score += len(patterns) * 10

    if risk_score >= 60:
        return "HIGH", 100 - risk_score
    elif risk_score >= 30:
        return "MEDIUM", 100 - risk_score
    else:
        return "LOW", 100 - risk_score
