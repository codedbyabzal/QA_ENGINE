import os
import cv2
import numpy as np


# -------------------------------
# HTML → IMAGE (Fallback)
# -------------------------------
def html_to_image(html_path, output_path="temp/html_out.png"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img = np.full((1200, 800, 3), 255, dtype=np.uint8)

    cv2.putText(
        img,
        "HTML Preview Not Available (Cloud Mode)",
        (50, 600),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2
    )

    cv2.imwrite(output_path, img)

    return output_path


# -------------------------------
# PDF → IMAGE (Fallback)
# -------------------------------
def pdf_to_image(pdf_path, output_path="temp/pdf_out.png"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img = np.full((1200, 800, 3), 255, dtype=np.uint8)

    cv2.putText(
        img,
        "PDF Preview Not Available (Cloud Mode)",
        (50, 600),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2
    )

    cv2.imwrite(output_path, img)

    return output_path


# -------------------------------
# IMAGE COMPARISON
# -------------------------------
def compare_images(pdf_img_path, html_img_path, output_path="temp/diff.png"):

    img1 = cv2.imread(pdf_img_path)
    img2 = cv2.imread(html_img_path)

    if img1 is None or img2 is None:
        return output_path, []

    h = max(img1.shape[0], img2.shape[0])
    w = max(img1.shape[1], img2.shape[1])

    img1 = cv2.resize(img1, (w, h))
    img2 = cv2.resize(img2, (w, h))

    diff = cv2.absdiff(img1, img2)

    cv2.imwrite(output_path, diff)

    return output_path, []