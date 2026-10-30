import cv2, os
import numpy as np

lines_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p06_lines'
out_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p06_groups'
os.makedirs(out_dir, exist_ok=True)

all_lines = sorted([f for f in os.listdir(lines_dir) if f.startswith('line_') and f.endswith('.png')])
# First let's check lines 01 to 04 to identify where body begins
for f in all_lines[:4]:
    print(f, cv2.imread(os.path.join(lines_dir, f)).shape)

# Let's see what each of the first 4 lines looks like
group_size = 5
for i in range(0, len(all_lines), group_size):
    chunk = all_lines[i:i+group_size]
    imgs = [cv2.imread(os.path.join(lines_dir, f)) for f in chunk]
    max_w = max(img.shape[1] for img in imgs)
    padded = []
    for idx_c, img in enumerate(imgs):
        h, w = img.shape[:2]
        pad_img = np.full((h, max_w, 3), 255, dtype=np.uint8)
        pad_img[:, :w] = img
        padded.append(pad_img)
        padded.append(np.full((10, max_w, 3), 230, dtype=np.uint8))
    stacked = np.vstack(padded[:-1])
    group_name = f"group_{i//group_size + 1}_{chunk[0][:7]}_to_{chunk[-1][:7]}.png"
    cv2.imwrite(os.path.join(out_dir, group_name), stacked)
    print(f"Saved {group_name}")
