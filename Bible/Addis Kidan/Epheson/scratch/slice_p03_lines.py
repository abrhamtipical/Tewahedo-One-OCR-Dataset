import pypdfium2 as pdfium
from PIL import Image
import numpy as np
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
p3 = doc[2] # Page 3

scale = 6
bitmap = p3.render(scale=scale)
img = bitmap.to_pil()

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"
page3_dir = os.path.join(scratch_dir, "p03_lines")
os.makedirs(page3_dir, exist_ok=True)

# Left column: x from 25 to 295 pt, y from 90 to 760 pt
left_box = (int(25 * scale), int(90 * scale), int(295 * scale), int(760 * scale))
col = img.crop(left_box)
col.save(os.path.join(page3_dir, "p03_left_text_area.png"))

# Convert to grayscale numpy array
arr = np.array(col.convert("L"))
# ink is dark (< 180)
ink = (arr < 180).astype(np.int32)
row_sums = np.sum(ink, axis=1)

# Find line bands
lines = []
in_line = False
start_y = 0

for y, s in enumerate(row_sums):
    if s > 15: # ink present
        if not in_line:
            in_line = True
            start_y = max(0, y - 4)
    else:
        if in_line:
            in_line = False
            end_y = min(arr.shape[0], y + 4)
            if end_y - start_y > 15: # minimum height for a line
                lines.append((start_y, end_y))

print(f"Detected {len(lines)} lines on Page 3!")

for i, (sy, ey) in enumerate(lines):
    line_crop = col.crop((0, sy, col.width, ey))
    line_crop.save(os.path.join(page3_dir, f"line_{i+1:02d}.png"))

print("All lines saved successfully!")
