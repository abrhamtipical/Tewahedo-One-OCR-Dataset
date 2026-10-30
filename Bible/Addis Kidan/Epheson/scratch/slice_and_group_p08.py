import fitz, cv2, os
import numpy as np

pdf_path = r'C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf'
scratch_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch'
lines_dir = os.path.join(scratch_dir, 'p08_lines')
groups_dir = os.path.join(scratch_dir, 'p08_groups')
os.makedirs(lines_dir, exist_ok=True)
os.makedirs(groups_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages in epheson.pdf: {len(doc)}")
page = doc[7] # index 7 is page 8
mat = fitz.Matrix(6, 6) # high DPI 6x
pix = page.get_pixmap(matrix=mat)
img_path = os.path.join(scratch_dir, 'p08_render.png')
pix.save(img_path)

img = cv2.imread(img_path)
h, w = img.shape[:2]

# Save top check and bottom check
cv2.imwrite(os.path.join(scratch_dir, 'p08_top_check.png'), img[:int(h*0.25), :])
cv2.imwrite(os.path.join(scratch_dir, 'p08_bottom_check.png'), img[int(h*0.75):, :])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

x_start = int(w * 0.06)
x_end = int(w * 0.47)
y_start = int(h * 0.06)
y_end = int(h * 0.95)

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

print(f"Found {len(lines)} line bands in Page 8.")

line_idx = 1
for sy, ey in lines:
    pad = 6
    actual_sy = max(0, y_start + sy - pad)
    actual_ey = min(h, y_start + ey + pad)
    line_crop = img[actual_sy:actual_ey, x_start:x_end]
    line_gray = cv2.cvtColor(line_crop, cv2.COLOR_BGR2GRAY)
    if np.sum(line_gray < 180) > 100:
        cv2.imwrite(os.path.join(lines_dir, f'line_{line_idx:02d}.png'), line_crop)
        line_idx += 1

print(f"Saved {line_idx - 1} lines to {lines_dir}")

# Group into 5-line chunks
all_lines = sorted([f for f in os.listdir(lines_dir) if f.startswith('line_') and f.endswith('.png')])
group_size = 5
for i in range(0, len(all_lines), group_size):
    chunk = all_lines[i:i+group_size]
    imgs = [cv2.imread(os.path.join(lines_dir, f)) for f in chunk]
    max_w = max(im.shape[1] for im in imgs)
    padded = []
    for idx_c, im in enumerate(imgs):
        ih, iw = im.shape[:2]
        pad_img = np.full((ih, max_w, 3), 255, dtype=np.uint8)
        pad_img[:, :iw] = im
        padded.append(pad_img)
        padded.append(np.full((10, max_w, 3), 230, dtype=np.uint8))
    stacked = np.vstack(padded[:-1])
    group_name = f"group_{i//group_size + 1}_{chunk[0][:7]}_to_{chunk[-1][:7]}.png"
    cv2.imwrite(os.path.join(groups_dir, group_name), stacked)
    print(f"Saved {group_name}")
