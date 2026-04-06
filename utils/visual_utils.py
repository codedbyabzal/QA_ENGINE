import os
import time
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pdf2image import convert_from_path

def html_to_image(html_path, output_path="temp/html_out.png"):
    abs_path = os.path.abspath(html_path)
    file_url = "file:///" + abs_path.replace("\\", "/")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1200,4000") 
    chrome_options.add_argument("--force-device-scale-factor=2") 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(file_url)
    time.sleep(3) 
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    driver.save_screenshot(output_path)
    driver.quit()
    return output_path

def pdf_to_image(pdf_path, output_path="temp/pdf_out.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Higher DPI (300) for sharpest possible comparison baseline
    images = convert_from_path(pdf_path, dpi=300)
    images[0].save(output_path, "PNG")
    return output_path

def compare_images(pdf_img_path, html_img_path, output_path="temp/side_by_side_audit.png"):
    img_pdf = cv2.imread(pdf_img_path)
    img_html = cv2.imread(html_img_path)

    if img_pdf is None or img_html is None:
        raise ValueError("Assets not found.")

    h1, w1 = img_pdf.shape[:2]
    h2, w2 = img_html.shape[:2]
    max_h, max_w = max(h1, h2), max(w1, w2)

    def get_centered(img, th, tw):
        canvas = np.full((th, tw, 3), 255, dtype=np.uint8)
        y, x = (th - img.shape[0]) // 2, (tw - img.shape[1]) // 2
        canvas[y:y+img.shape[0], x:x+img.shape[1]] = img
        return canvas

    p_norm = get_centered(img_pdf, max_h, max_w)
    h_norm = get_centered(img_html, max_h, max_w)

    diff = cv2.absdiff(p_norm, h_norm)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150)

    _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)
    combined = cv2.bitwise_and(thresh, edges)

    kernel = np.ones((15, 15), np.uint8)
    dilated = cv2.dilate(combined, kernel, iterations=1)

    diff_view = h_norm.copy()
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    visual_errors = []

    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area > 300:
            x, y, w, h = cv2.boundingRect(c)

            section = int((y / max_h) * 3)
            section_name = ["Header", "Body", "Footer"][min(section, 2)]

            confidence = min(100, int((area / 5000) * 100))

            description = f"Issue in {section_name} | Area: {int(area)}px | Confidence: {confidence}%"
            visual_errors.append(description)

            overlay = diff_view.copy()
            cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.25, diff_view, 0.75, 0, diff_view)

            cv2.rectangle(diff_view, (x, y), (x+w, y+h), (0, 0, 255), 3)
            cv2.putText(diff_view, str(i+1), (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

    def style_view(img, title, color=(255,0,0)):
        canvas = cv2.copyMakeBorder(img, 200, 0, 0, 0,
                                    cv2.BORDER_CONSTANT,
                                    value=[248, 250, 252])
        cv2.putText(canvas, title, (60, 130),
                    cv2.FONT_HERSHEY_DUPLEX, 3, color, 6)
        return canvas

    v1 = style_view(p_norm, "DESIGN (PDF)")
    v2 = style_view(h_norm, "BUILD (HTML)")
    v3 = style_view(diff_view, f"AUDIT ({len(visual_errors)} ISSUES)", (0,0,255))

    spacer = np.full((v1.shape[0], 80, 3), 248, dtype=np.uint8)
    montage = np.hstack((v1, spacer, v2, spacer, v3))

    cv2.imwrite(output_path, montage)

    return output_path, visual_errors