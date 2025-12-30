import streamlit as st

from backend.predict import predict_news
from backend.patterns import detect_patterns
from backend.risk import calculate_risk
from backend.history import save_history
from backend.fetch_url import extract_text_from_url
from backend.source_check import check_source
from backend.category import detect_category, category_warning

# ----------------------------------
# Page setup
# ----------------------------------
st.header("🔍 Analyze News Article")

# ----------------------------------
# Session state initialization
# ----------------------------------
if "article_text" not in st.session_state:
    st.session_state.article_text = ""

if "article_source" not in st.session_state:
    st.session_state.article_source = ""

if "fetched" not in st.session_state:
    st.session_state.fetched = False

# ----------------------------------
# Input type selection
# ----------------------------------
input_type = st.radio(
    "Choose input type",
    ["Paste Text", "Paste URL"],
    horizontal=True
)

# ----------------------------------
# INPUT HANDLING
# ----------------------------------
if input_type == "Paste URL":
    url = st.text_input("Paste news URL")

    if st.button("Fetch Article"):
        extracted = extract_text_from_url(url)

        if extracted and len(extracted.split()) > 80:
            st.session_state.article_text = extracted
            st.session_state.article_source = url
            st.session_state.fetched = True
            st.success("✅ Article content extracted successfully.")
        else:
            st.session_state.fetched = False
            st.error(
                "❌ Unable to extract sufficient article content. "
                "Some websites restrict scraping."
            )

else:
    text_input = st.text_area(
        "Paste news article text",
        height=300
    )
    st.session_state.article_text = text_input
    st.session_state.article_source = ""
    st.session_state.fetched = True if len(text_input.split()) > 30 else False

# ----------------------------------
# ANALYSIS
# ----------------------------------
if st.button("Analyze"):
    article = st.session_state.article_text

    if not st.session_state.fetched or len(article.split()) < 30:
        st.warning("Please provide valid article text or fetch a URL first.")
    else:
        # -------------------------------
        # Model prediction
        # -------------------------------
        prediction, confidence = predict_news(article)
        patterns = detect_patterns(article)
        risk_level, trust_score = calculate_risk(
            prediction, confidence, patterns
        )

        # -------------------------------
        # Source credibility (URL only)
        # -------------------------------
        trusted_override = False
        domain = None

        if st.session_state.article_source:
            status, domain = check_source(st.session_state.article_source)

            st.subheader("🌐 Source Credibility")
            st.write(f"Source: **{domain}**")
            st.write(f"Credibility: **{status}**")

            if status == "KNOWN / TRUSTED":
                trusted_override = True

        # -------------------------------
        # Decision label logic (IMPORTANT)
        # -------------------------------
        if prediction == 0 and trusted_override:
            final_label = "POTENTIALLY MISCLASSIFIED"
        else:
            final_label = "FAKE" if prediction == 0 else "REAL"

        # -------------------------------
        # Final decision display
        # -------------------------------
        if risk_level == "HIGH" and not trusted_override:
            st.error(f"❌ {final_label} — HIGH MISINFORMATION RISK")
        elif risk_level == "MEDIUM":
            st.warning(f"⚠ {final_label} — MEDIUM RISK")
        else:
            st.success(f"✅ {final_label} — LOW RISK")

        # -------------------------------
        # Trust meter
        # -------------------------------
        st.metric("Model Confidence (%)", round(confidence, 2))
        st.progress(trust_score / 100)
        st.caption(f"Trust Score: {trust_score}/100")

        # -------------------------------
        # Category awareness (weighted)
        # -------------------------------
        category = detect_category(article)
        st.subheader("🗂 News Category")
        st.write(category)
        st.info(category_warning(category))

        # -------------------------------
        # Pattern detection
        # -------------------------------
        st.subheader("⚠ Detected Misinformation Patterns")
        if patterns:
            for p in patterns:
                st.write("•", p)
        else:
            st.write("No major misinformation patterns detected.")

        # -------------------------------
        # Dataset limitation notice
        # -------------------------------
        if trusted_override and prediction == 0:
            st.info(
                "ℹ This article is from a trusted news source. "
                "The classification may be affected by dataset bias or regional differences."
            )

        # -------------------------------
        # Save history
        # -------------------------------
        save_history(final_label, confidence, risk_level, trust_score)
