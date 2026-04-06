import pandas as pd
import io

def generate_excel_report(missing, extra, mismatch, visual_errors=[]):
    output = io.BytesIO()

    summary = pd.DataFrame({
        "Metric": ["Missing", "Extra", "Mismatch", "Visual Issues"],
        "Count": [len(missing), len(extra), len(mismatch), len(visual_errors)]
    })

    text_issues = []

    for m in missing:
        text_issues.append(["Missing", m, "", "Critical"])

    for e in extra:
        text_issues.append(["Extra", "", e, "Low"])

    for p, h in mismatch:
        text_issues.append(["Mismatch", p, h, "Medium"])

    df_text = pd.DataFrame(text_issues, columns=["Type", "PDF", "HTML", "Severity"])

    df_visual = pd.DataFrame({
        "Visual Issues": visual_errors
    })

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        df_text.to_excel(writer, sheet_name="Text Issues", index=False)
        df_visual.to_excel(writer, sheet_name="Visual Issues", index=False)

    output.seek(0)
    return output