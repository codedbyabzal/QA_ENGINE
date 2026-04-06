import streamlit as st
from utils.extractor import extract_pdf, extract_html
from utils.cleaner import clean_text
from utils.splitter import split_sentences, split_html_sentences
from utils.matcher import match_sentences
from utils.comparator import classify

st.set_page_config(layout="wide")
st.title("📊 Email QA Automation Tool")

# -------------------------------
# INPUT
# -------------------------------
pdf_path = st.text_input("📄 PDF Path", "samples/sample.pdf")
html_path = st.text_input("📧 HTML Path", "samples/sample.html")

if st.button("Run QA Check"):

    # PROCESS
    pdf_text = clean_text(extract_pdf(pdf_path))
    html_text = clean_text(extract_html(html_path))

    pdf_s = split_sentences(pdf_text)
    html_s = split_html_sentences(split_sentences(html_text))

    matched, missing, extra = match_sentences(pdf_s, html_s)
    differences, spacing, line_issues, special = classify(matched)

    # -------------------------------
    # SUMMARY
    # -------------------------------
    st.markdown("### 📊 Summary")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🔄 Differences", len(differences))
    c2.metric("❌ Missing", len(missing))
    c3.metric("➕ Extra", len(extra))
    c4.metric("⚠️ Spacing", len(spacing))
    c5.metric("🔤 Special Char", len(special))

    st.markdown("---")

    # -------------------------------
    # HIGHLIGHT FUNCTION
    # -------------------------------
    def highlight(p, h):
        pw = p.split()
        hw = h.split()

        rp = []
        rh = []

        for i in range(max(len(pw), len(hw))):
            wp = pw[i] if i < len(pw) else ""
            wh = hw[i] if i < len(hw) else ""

            if wp == wh:
                rp.append(wp)
                rh.append(wh)
            else:
                rp.append(f"<span style='background:#ffcccc'>{wp}</span>")
                rh.append(f"<span style='background:#ccffcc'>{wh}</span>")

        return " ".join(rp), " ".join(rh)

    # -------------------------------
    # DIFFERENCES
    # -------------------------------
    st.subheader("🔄 Compared Differences")

    for p, h in differences:
        p_h, h_h = highlight(p, h)

        st.markdown(f"""
        <div style="background:#e7f3ff;padding:12px;border-radius:8px;margin-bottom:10px;">
        <b>PDF:</b><br>{p_h}<br><br>
        <b>HTML:</b><br>{h_h}
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------
    # SPECIAL CHAR
    # -------------------------------
    st.subheader("🔤 Special Character Issues")

    for p, h, diff in special:
        st.markdown(f"""
        <div style="background:#ffeeba;padding:12px;border-radius:8px;margin-bottom:10px;">
        <b>PDF:</b> {p}<br>
        <b>HTML:</b> {h}<br>
        <b>{diff}</b>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------
    # MISSING
    # -------------------------------
    st.subheader("❌ Missing")

    for m in missing:
        st.markdown(f"<div style='background:#f8d7da;padding:8px;margin-bottom:5px'>{m}</div>", unsafe_allow_html=True)

    # -------------------------------
    # EXTRA
    # -------------------------------
    st.subheader("➕ Extra")

    for e in extra:
        st.markdown(f"<div style='background:#d4edda;padding:8px;margin-bottom:5px'>{e}</div>", unsafe_allow_html=True)

    # -------------------------------
    # SPACING
    # -------------------------------
    st.subheader("⚠️ Spacing Issues")

    for p, h in spacing:
        st.markdown(f"""
        <div style="background:#fff3cd;padding:10px;">
        <b>PDF:</b> {p}<br>
        <b>HTML:</b> {h}
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------
    # LINE
    # -------------------------------
    st.subheader("📏 Line Issues")

    for p, h in line_issues:
        st.markdown(f"""
        <div style="background:#f5c6cb;padding:10px;">
        <b>PDF:</b> {p}<br>
        <b>HTML:</b> {h}
        </div>
        """, unsafe_allow_html=True)