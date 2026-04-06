import streamlit as st
import os
import pandas as pd
import plotly.express as px
from difflib import SequenceMatcher

from utils.extractor import extract_pdf, extract_html
from utils.cleaner import clean_text
from utils.splitter import split_sentences
from utils.comparator import classify_strict, highlight_diff
from utils.visual_utils import pdf_to_image, html_to_image, compare_images
from utils.reporter import generate_excel_report
from utils.pdf_report import generate_pdf_report

# ---------------- AI ---------------- #
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def classify_ai(pdf_s, html_s):
    missing, extra, mismatch = [], [], []
    used = set()

    for p in pdf_s:
        best_score, best_match = 0, None
        for h in html_s:
            score = similarity(p, h)
            if score > best_score:
                best_score, best_match = score, h

        if best_score > 0.9:
            used.add(best_match)
        elif best_score > 0.6:
            mismatch.append((p, best_match))
            used.add(best_match)
        else:
            missing.append(p)

    for h in html_s:
        if h not in used:
            extra.append(h)

    return missing, extra, mismatch

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="QA Studio SaaS", layout="wide")

# ---------------- SIDEBAR ---------------- #
st.sidebar.markdown("## 🅰️ QA Studio SaaS")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🔍 Analysis", "📊 Reports"]
)

pdf_file = st.sidebar.file_uploader("Upload PDF", type="pdf")
html_file = st.sidebar.file_uploader("Upload HTML", type=["html", "htm"])

mode = st.sidebar.radio("Comparison Mode", ["Strict", "AI Smart"])

run = st.sidebar.button("🚀 Run Audit", width="stretch")

# ---------------- PROCESS ---------------- #
if run and pdf_file and html_file:

    os.makedirs("temp", exist_ok=True)

    pdf_path = "temp/input.pdf"
    html_path = "temp/input.html"

    with open(pdf_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    with open(html_path, "wb") as f:
        f.write(html_file.getbuffer())

    with st.spinner("Running QA Engine..."):
        pdf_text = clean_text(extract_pdf(pdf_path))
        html_text = clean_text(extract_html(html_path))

        pdf_s = split_sentences(pdf_text)
        html_s = split_sentences(html_text)

        if mode == "AI Smart":
            missing, extra, mismatch = classify_ai(pdf_s, html_s)
        else:
            missing, extra, mismatch = classify_strict(pdf_s, html_s)

    total = len(pdf_s)
    penalty = len(missing) + (len(mismatch) * 0.5)
    score = round(max(0, (1 - penalty / max(total, 1)) * 100), 2)

    st.session_state.data = {
        "missing": missing,
        "extra": extra,
        "mismatch": mismatch,
        "score": score,
        "total": total
    }

# ---------------- LOAD ---------------- #
data = st.session_state.get("data", None)

# ---------------- DASHBOARD ---------------- #
if page == "🏠 Dashboard":
    st.title("💎 QA Dashboard")

    if data:
        score = data["score"]

        st.markdown(f"""
        <div style="background:#4f46e5;color:white;padding:30px;
        border-radius:16px;text-align:center;">
        <h3>Match Score</h3>
        <h1>{score}%</h1>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score/100)

        c1, c2, c3 = st.columns(3)
        c1.metric("Missing", len(data["missing"]))
        c2.metric("Extra", len(data["extra"]))
        c3.metric("Mismatch", len(data["mismatch"]))

        df = pd.DataFrame({
            "Type": ["Missing", "Extra", "Mismatch"],
            "Count": [len(data["missing"]), len(data["extra"]), len(data["mismatch"])]
        })

        fig = px.bar(df, x="Type", y="Count")
        st.plotly_chart(fig, width="stretch")

    else:
        st.info("Run an audit to see dashboard")

# ---------------- ANALYSIS ---------------- #
elif page == "🔍 Analysis":
    st.title("🔍 Content Analysis")

    if data:

        total_issues = len(data["mismatch"])

        selected_issue = None
        if total_issues > 0:
            selected_issue = st.selectbox(
                "📌 Jump to Issue",
                list(range(1, total_issues + 1))
            )

        tab1, tab2 = st.tabs(["Text", "Visual"])

        # ---------- TEXT ----------
        with tab1:
            st.markdown("### 🔍 Text Differences")

            if not data["mismatch"]:
                st.success("✅ No mismatches found")

            for idx, (p, h) in enumerate(data["mismatch"], start=1):
                p_h, h_h = highlight_diff(p, h)

                border = "3px solid #4f46e5" if selected_issue == idx else "1px solid #eee"

                st.markdown(f"""
                <div style="background:white;padding:20px;
                border-radius:12px;border:{border};
                margin-bottom:15px;">
                <b>Issue #{idx}</b><br><br>
                <b>PDF:</b><br>{p_h}<br><br>
                <b>HTML:</b><br>{h_h}
                </div>
                """, unsafe_allow_html=True)

        # ---------- VISUAL ----------
        with tab2:
            pdf_path = "temp/input.pdf"
            html_path = "temp/input.html"

            p_img = pdf_to_image(pdf_path)
            h_img = html_to_image(html_path)

            diff_path, visual_errors = compare_images(p_img, h_img)

            st.image(diff_path, width="stretch")

            for i, desc in enumerate(visual_errors, start=1):
                st.error(f"Issue {i}: {desc}")

    else:
        st.info("Run audit first")

# ---------------- REPORTS ---------------- #
elif page == "📊 Reports":
    st.title("📊 Reports")

    if data:
        excel = generate_excel_report(
            data["missing"],
            data["extra"],
            data["mismatch"]
        )

        pdf = generate_pdf_report(
            data["missing"],
            data["extra"],
            data["mismatch"],
            []
        )

        st.download_button("📥 Excel Report", excel, "report.xlsx", width="stretch")
        st.download_button("📄 PDF Report", pdf, "report.pdf", width="stretch")

    else:
        st.info("Run audit first")