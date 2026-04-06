import re


# -------------------------------
# TEXT CLEANING FUNCTION
# -------------------------------
def clean_text(text):
    if not text:
        return ""

    text = text.lower()

    # Remove HTML tags (safety)
    text = re.sub(r"<.*?>", "", text)

    # Split into lines for safer cleaning
    lines = text.split("\n")

    cleaned_lines = []

    remove_patterns = [
        r"^from:",
        r"^subject:",
        r"^sent:",
        r"^to:",
        r"^caution:",
        r"unsubscribe",
        r"view in browser",
        r"\(\d+ characters\)",
        r"character limit"
    ]

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip unwanted patterns
        if any(re.search(p, line) for p in remove_patterns):
            continue

        cleaned_lines.append(line)

    # Join back
    text = " ".join(cleaned_lines)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()