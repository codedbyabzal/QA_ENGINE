import os
import cv2
import numpy as np
from pdf2image import convert_from_path

def html_to_image(html_path, output_path="temp/html_out.png"):
    # fallback dummy image (safe for cloud)

    import numpy as np
    import cv2
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img = np.full((1200, 800, 3), 255, dtype=np.uint8)

    cv2.putText(img, "HTML Preview Not Available", (50, 600),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imwrite(output_path, img)

    return output_path


def pdf_to_image(pdf_path, output_path="temp/pdf_out.png"):
    import numpy as np
    import cv2
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img = np.full((1200, 800, 3), 255, dtype=np.uint8)

    cv2.putText(img, "PDF Preview Not Available", (50, 600),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imwrite(output_path, img)

    return output_path

def compare_images(pdf_img_path, html_img_path, output_path="temp/visual_diff.png"):

    img_pdf = cv2.imread(pdf_img_path)
    img_html = cv2.imread(html_img_path)

    if img_pdf is None or img_html is None:
        raise ValueError("Image load failed")

    h1, w1 = img_pdf.shape[:2]
    h2, w2 = img_html.shape[:2]
    max_h, max_w = max(h1, h2), max(w1, w2)

    def center(img, th, tw):
        canvas = np.full((th, tw, 3), 255, dtype=np.uint8)
        y, x = (th - img.shape[0]) // 2, (tw - img.shape[1]) // 2
        canvas[y:y+img.shape[0], x:x+img.shape[1]] = img
        return canvas

    p = center(img_pdf, max_h, max_w)
    h = center(img_html, max_h, max_w)

    diff = cv2.absdiff(p, h)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

    kernel = np.ones((10, 10), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = h.copy()
    errors = []

    for i, c in enumerate(contours):
        area = cv2.contourArea(c)

        if area > 500:
            x, y, w, h_ = cv2.boundingRect(c)

            section = int((y / max_h) * 3)
            section_name = ["Header", "Body", "Footer"][min(section, 2)]

            errors.append({
                "id": i+1,
                "section": section_name,
                "confidence": min(100, int(area / 5000 * 100))
            })

            cv2.rectangle(result, (x, y), (x+w, y+h_), (0, 0, 255), 2)

    cv2.imwrite(output_path, result)

    return output_path, errors
