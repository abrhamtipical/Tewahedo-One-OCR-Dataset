import cv2
import numpy as np

def zoom_and_save(img_path, out_path, crop_box=None, zoom=3):
    img = cv2.imread(img_path)
    if crop_box:
        x1, y1, x2, y2 = crop_box
        img = img[y1:y2, x1:x2]
    h, w = img.shape[:2]
    zoomed = cv2.resize(img, (w * zoom, h * zoom), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(out_path, zoomed)

# Zoom specific words
zoom_and_save("scratch/p04_lines/line_24.png", "scratch/p04_z_line24.png", zoom=2)
zoom_and_save("scratch/p04_lines/line_36.png", "scratch/p04_z_line36.png", zoom=2)
zoom_and_save("scratch/p04_lines/line_42.png", "scratch/p04_z_line42.png", zoom=2)
zoom_and_save("scratch/p04_lines/line_46.png", "scratch/p04_z_line46.png", zoom=2)

print("Zooms created.")
