from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_pdf_report(missing, extra, mismatch, visual_errors):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("QA Audit Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Missing: {len(missing)}", styles['Normal']))
    elements.append(Paragraph(f"Extra: {len(extra)}", styles['Normal']))
    elements.append(Paragraph(f"Mismatch: {len(mismatch)}", styles['Normal']))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Text Issues", styles['Heading2']))

    for p, h in mismatch:
        elements.append(Paragraph(f"PDF: {p}", styles['Normal']))
        elements.append(Paragraph(f"HTML: {h}", styles['Normal']))
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("Visual Issues", styles['Heading2']))

    for v in visual_errors:
        elements.append(Paragraph(v, styles['Normal']))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)

    return buffer