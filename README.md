# 📧 Email QA Automation Platform

<p align="center">
  <b>A SaaS-style QA tool to validate HTML email builds against PDF designs</b>
</p>

<p align="center">
  🚀 Automate QA • 🔍 Detect Differences • 📊 Generate Reports
</p>

---

## 🏆 Highlights

- ⚡ End-to-end QA automation platform  
- 🧠 Smart text comparison engine  
- 🖼️ Visual difference detection  
- 📊 Interactive dashboard (Streamlit)  
- 📥 Excel & PDF reporting  
- 🌐 Fully deployed cloud application  

---

## 🖥️ Demo

👉 **Live App:** *(Add your Streamlit link here)*  
👉 **GitHub Repo:** https://github.com/codedbyabzal/QA_ENGINE

---

## 🎯 Problem Statement

Manual email QA:
- ❌ Time-consuming  
- ❌ Error-prone  
- ❌ Difficult to validate at scale  

👉 This tool automates the entire QA process with accuracy and speed.

---

## ⚙️ Features

### 🔍 Text QA Engine
- Extracts content from PDF & HTML
- Cleans and normalizes text
- Sentence-level comparison
- Detects:
  - ❌ Missing content  
  - ➕ Extra content  
  - ⚠️ Mismatch  
- Word-level highlighting

---

### 🧠 Smart Matching
- Fuzzy matching (`difflib`)
- Substring boosting
- Threshold-based classification
- Weighted match score

---

### 🖼️ Visual QA Engine
- OpenCV-based image comparison
- Detects layout shifts
- Highlights differences
- Section-aware:
  - Header  
  - Body  
  - Footer  

---

### 📊 Dashboard UI
- Upload PDF & HTML
- Run QA instantly
- View:
  - Match Score %
  - Missing / Extra / Mismatch counts
- Charts powered by Plotly

---

### 📥 Reports
- 📊 Excel (multi-sheet)
- 📄 PDF (client-ready)

---

## 🧱 Tech Stack

<p align="center">

| Layer | Tech |
|------|------|
| UI | Streamlit |
| Text Extraction | pdfplumber, BeautifulSoup |
| Matching | difflib |
| Visual QA | OpenCV |
| Charts | Plotly |
| Reports | pandas, reportlab, openpyxl |

</p>

---

## 🧠 Architecture
