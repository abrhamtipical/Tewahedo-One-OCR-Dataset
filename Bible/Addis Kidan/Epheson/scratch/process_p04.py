import pypdfium2 as pdfium
from PIL import Image
import numpy as np
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
p4 = doc[3] # Page 4 (0-indexed is 3)

scale = 6
bitmap = p4.render(scale=scale)
img = bitmap.to_pil()

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"
page4_dir = os.path.join(scratch_dir, "p04_lines")
os.makedirs(page4_dir, exist_ok=True)

# Left col: x from 25 to 295 pt, y from 40 to 765 pt
left_box = (int(25 * scale), int(40 * scale), int(295 * scale), int(765 * scale))
col = img.crop(left_box)
col.save(os.path.join(scratch_dir, "p04_left_full.png"))

# Also save 4 sections for overview
img.crop((int(25 * scale), int(40 * scale), int(295 * scale), int(240 * scale))).save(os.path.join(scratch_dir, "p04_sec1.png"))
img.crop((int(25 * scale), int(220 * scale), int(295 * scale), int(420 * scale))).save(os.path.join(scratch_dir, "p04_sec2.png"))
img.crop((int(25 * scale), int(400 * scale), int(295 * scale), int(600 * scale))).save(os.path.join(scratch_dir, "p04_sec3.png"))
img.crop((int(25 * scale), int(580 * scale), int(295 * scale), int(765 * scale))).save(os.path.join(scratch_dir, "p04_sec4.png"))

# Now let's slice lines starting below the header line (y > 90 pt)
text_box = (int(25 * scale), int(90 * scale), int(295 * scale), int(760 * scale))
text_col = img.crop(text_box)
text_col.save(os.path.join(page4_dir, "p04_text_area.png"))

arr = np.array(text_col.convert("L"))
ink = (arr < 180).astype(np.int32)
row_sums = np.sum(ink, axis=1)

lines = []
in_line = False
start_y = 0

for y, s in enumerate(row_sums):
    if s > 15:
        if not in_line:
            in_line = True
            start_y = max(0, y - 4)
    else:
        if in_line:
            in_line = False
            end_y = min(arr.shape[0], y + 4)
            if end_y - start_y > 15:
                lines.append((start_y, end_y))

print(f"Page 4: detected {len(lines)} lines")
for i, (sy, ey) in enumerate(lines):
    line_crop = text_col.crop((0, sy, text_col.width, ey))
    line_crop.save(os.path.join(page4_dir, f"line_{i+1:02d}.png"))

print("Page 4 rendered and all lines sliced successfully!")
