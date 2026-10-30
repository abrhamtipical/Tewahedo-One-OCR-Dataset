import cv2, os
import numpy as np

lines_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p05_lines'
out_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p05_groups'
os.makedirs(out_dir, exist_ok=True)

# Group lines into blocks of 5 lines
# line_05 to line_45
all_lines = sorted([f for f in os.listdir(lines_dir) if f.startswith('line_') and f.endswith('.png')])
# filter out lines 01 to 04 (headers/watermarks)
body_lines = [f for f in all_lines if int(f.split('_')[1].split('.')[0]) >= 5]

group_size = 5
for i in range(0, len(body_lines), group_size):
    chunk = body_lines[i:i+group_size]
    imgs = [cv2.imread(os.path.join(lines_dir, f)) for f in chunk]
    # find max width
    max_w = max(img.shape[1] for img in imgs)
    # pad each to max_w and stack vertically with a separator
    padded = []
    for idx_c, img in enumerate(imgs):
        line_num = chunk[idx_c].split('.')[0]
        h, w = img.shape[:2]
        pad_img = np.full((h, max_w, 3), 255, dtype=np.uint8)
        pad_img[:, :w] = img
        # add a small line number label or border
        padded.append(pad_img)
        # 10px white separator
        padded.append(np.full((10, max_w, 3), 230, dtype=np.uint8))
    stacked = np.vstack(padded[:-1])
    group_name = f"group_{i//group_size + 1}_{chunk[0][:7]}_to_{chunk[-1][:7]}.png"
    cv2.imwrite(os.path.join(out_dir, group_name), stacked)
    print(f"Saved {group_name}")
