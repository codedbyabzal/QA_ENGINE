import re
from difflib import SequenceMatcher


# -------------------------------
# NORMALIZATION
# -------------------------------
def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


# -------------------------------
# SIMILARITY SCORE
# -------------------------------
def similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


# -------------------------------
# SMART MATCHING ENGINE
# -------------------------------
def match_sentences(pdf_s, html_s, threshold=0.75, partial_boost=0.15):

    used_html = set()

    results = {
        "matched": [],
        "mismatched": [],
        "missing": [],
        "extra": []
    }

    for p in pdf_s:

        best_score = 0
        best_match = None
        best_index = -1

        for i, h in enumerate(html_s):

            if i in used_html:
                continue

            score = similarity(p, h)

            # 🔥 partial match boost
            if normalize(p) in normalize(h) or normalize(h) in normalize(p):
                score += partial_boost

            if score > best_score:
                best_score = score
                best_match = h
                best_index = i

        # -------------------------------
        # CLASSIFICATION
        # -------------------------------

        if best_score >= threshold:
            used_html.add(best_index)
            results["matched"].append({
                "pdf": p,
                "html": best_match,
                "score": round(best_score, 2)
            })

        elif best_score >= 0.5:
            used_html.add(best_index)
            results["mismatched"].append({
                "pdf": p,
                "html": best_match,
                "score": round(best_score, 2)
            })

        else:
            results["missing"].append(p)

    # Remaining HTML = extra
    for i, h in enumerate(html_s):
        if i not in used_html:
            results["extra"].append(h)

    return results