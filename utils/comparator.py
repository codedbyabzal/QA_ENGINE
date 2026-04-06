import re
from difflib import ndiff

# -------------------------------
# NORMALIZE TEXT
# -------------------------------
def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower())


# -------------------------------
# REMOVE SYMBOLS
# -------------------------------
def remove_symbols(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)


# -------------------------------
# SYMBOL DIFFERENCE
# -------------------------------
def get_special_diff(p, h):

    sp_p = re.findall(r'[^a-zA-Z0-9\s]', p)
    sp_h = re.findall(r'[^a-zA-Z0-9\s]', h)

    missing = [c for c in sp_p if c not in sp_h]
    extra = [c for c in sp_h if c not in sp_p]

    return f"Missing symbols: {missing} | Extra symbols: {extra}"


# -------------------------------
# STRICT MATCHING
# -------------------------------
def classify_strict(pdf_s, html_s):

    used_html = set()

    missing = []
    extra = []
    mismatch = []

    for p in pdf_s:

        found_match = False
        p_norm = normalize(p)
        p_clean = remove_symbols(p_norm)

        for i, h in enumerate(html_s):

            if i in used_html:
                continue

            h_norm = normalize(h)
            h_clean = remove_symbols(h_norm)

            # PERFECT MATCH
            if p_norm == h_norm:
                used_html.add(i)
                found_match = True
                break

            # SYMBOL DIFFERENCE
            if p_clean == h_clean:
                used_html.add(i)
                mismatch.append((p, h))
                found_match = True
                break

            # PARTIAL MATCH
            if p_clean in h_clean or h_clean in p_clean:
                used_html.add(i)
                mismatch.append((p, h))
                found_match = True
                break

        if not found_match:
            missing.append(p)

    for i, h in enumerate(html_s):
        if i not in used_html:
            extra.append(h)

    return missing, extra, mismatch


# -------------------------------
# 🔥 HIGHLIGHT DIFFERENCE (KEY FEATURE)
# -------------------------------
def highlight_diff(pdf, html):

    diff = list(ndiff(pdf.split(), html.split()))

    pdf_out = []
    html_out = []

    for d in diff:
        if d.startswith("- "):
            pdf_out.append(f"<span style='background:#ff4d4d;color:white;padding:2px 4px;border-radius:4px'>{d[2:]}</span>")
        elif d.startswith("+ "):
            html_out.append(f"<span style='background:#28a745;color:white;padding:2px 4px;border-radius:4px'>{d[2:]}</span>")
        elif d.startswith("  "):
            word = d[2:]
            pdf_out.append(word)
            html_out.append(word)

    return " ".join(pdf_out), " ".join(html_out)