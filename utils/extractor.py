import pdfplumber
from bs4 import BeautifulSoup
import io

# -------------------------------
# PDF EXTRACT (FIXED)
# -------------------------------
def extract_pdf(pdf_file):
    text = ""
    # pdfplumber can handle the Streamlit UploadedFile object directly
    with pdfplumber.open(pdf_file) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                text += t + "\n"
    return text


# -------------------------------
# HTML EXTRACT (FIXED)
# -------------------------------
def extract_html(html_file):
    # Check if we are dealing with a Streamlit UploadedFile or a path string
    if hasattr(html_file, "getvalue"):
        # Read content from the buffer and decode to string
        content = html_file.getvalue().decode("utf-8", errors="ignore")
    else:
        # Standard logic for local file paths
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    # Pass the string content to BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # remove unwanted tags
    for tag in soup(["script", "style", "head", "title", "meta"]):
        tag.decompose()

    # get clean text
    text = soup.get_text(separator="\n")

    return text