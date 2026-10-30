import cv2

def crop_zoom(img_path, out_path, x_pct, zoom=3):
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    x1 = int(w * x_pct[0])
    x2 = int(w * x_pct[1])
    crop = img[:, x1:x2]
    cv2.imwrite(out_path, cv2.resize(crop, (0,0), fx=zoom, fy=zoom))

# 1. Line 15: start
crop_zoom("scratch/p05_lines/line_15.png", "scratch/p05_z_line15.png", (0.0, 0.6))

# 2. Line 16: middle
crop_zoom("scratch/p05_lines/line_16.png", "scratch/p05_z_line16.png", (0.55, 0.85))

# 3. Line 23: middle (shepherds)
crop_zoom("scratch/p05_lines/line_23.png", "scratch/p05_z_line23.png", (0.1, 0.55))

# 4. Line 28: middle
crop_zoom("scratch/p05_lines/line_28.png", "scratch/p05_z_line28.png", (0.3, 0.75))

# 5. Line 30: start
crop_zoom("scratch/p05_lines/line_30.png", "scratch/p05_z_line30.png", (0.1, 0.4))

# 6. Line 37: end
crop_zoom("scratch/p05_lines/line_37.png", "scratch/p05_z_line37.png", (0.6, 1.0))

# 7. Line 39: start
crop_zoom("scratch/p05_lines/line_39.png", "scratch/p05_z_line39.png", (0.0, 0.4))

# 8. Line 44: start
crop_zoom("scratch/p05_lines/line_44.png", "scratch/p05_z_line44.png", (0.0, 0.5))

# 9. Line 45: start
crop_zoom("scratch/p05_lines/line_45.png", "scratch/p05_z_line45.png", (0.0, 0.4))

print("P05 spots zoomed.")
