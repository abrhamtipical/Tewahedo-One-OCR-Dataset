import fitz, cv2, os
import numpy as np

pdf_path = r'C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf'
out_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p07_lines'
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
page = doc[6] # index 6 is page 7
mat = fitz.Matrix(6, 6)
pix = page.get_pixmap(matrix=mat)
img_path = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p07_render.png'
pix.save(img_path)

img = cv2.imread(img_path)
h, w = img.shape[:2]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

x_start = int(w * 0.06)
x_end = int(w * 0.47)
y_start = int(h * 0.06)
y_end = int(h * 0.95) # Make sure we don't cut off bottom lines!

crop_area = gray[y_start:y_end, x_start:x_end]
_, bin_img = cv2.threshold(crop_area, 200, 255, cv2.THRESH_BINARY_INV)

h_proj = np.sum(bin_img, axis=1)

lines = []
in_line = False
start_y = 0
min_ink = np.max(h_proj) * 0.02

for idx, val in enumerate(h_proj):
    if val > min_ink and not in_line:
        in_line = True
        start_y = idx
    elif val <= min_ink and in_line:
        in_line = False
        if (idx - start_y) > 15:
            lines.append((start_y, idx))
if in_line and (len(h_proj) - start_y) > 15:
    lines.append((start_y, len(h_proj)))

print(f"Found {len(lines)} line bands in Page 7.")

line_idx = 1
for sy, ey in lines:
    pad = 6
    actual_sy = max(0, y_start + sy - pad)
    actual_ey = min(h, y_start + ey + pad)
    line_crop = img[actual_sy:actual_ey, x_start:x_end]
    line_gray = cv2.cvtColor(line_crop, cv2.COLOR_BGR2GRAY)
    if np.sum(line_gray < 180) > 100:
        cv2.imwrite(os.path.join(out_dir, f'line_{line_idx:02d}.png'), line_crop)
        line_idx += 1

print(f"Saved {line_idx - 1} lines to {out_dir}")
