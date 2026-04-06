import re

# -------------------------------
# COMMON SPLIT ENGINE (USED FOR BOTH)
# -------------------------------
def split_sentences(text):

    parts = re.split(r'(?<=[.!?])\s+', text)

    merged = []
    buffer = ""

    for p in parts:
        p = p.strip()

        if not p:
            continue

        # 🔥 merge short fragments
        if len(p.split()) < 5:
            buffer += " " + p
        else:
            if buffer:
                merged.append((buffer + " " + p).strip())
                buffer = ""
            else:
                merged.append(p)

    if buffer:
        merged.append(buffer.strip())

    return merged


# -------------------------------
# HTML SPLIT → SAME AS PDF
# -------------------------------
def split_html_sentences(text):
    return split_sentences(text)