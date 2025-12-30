import streamlit as st
from backend.history import load_history

st.header("📊 Student Activity Insights")

df = load_history()

if df.empty:
    st.info("No articles analyzed yet.")
else:
    total = len(df)
    fake_count = len(df[df["prediction"] == "FAKE"])
    real_count = total - fake_count
    most_common_risk = df["risk_level"].mode()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Articles", total)
    col2.metric("Fake News Detected", fake_count)
    col3.metric("Most Common Risk", most_common_risk)

    st.subheader("📜 Analysis History")
    st.dataframe(df)
