import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[1] # Page 2 (index 1)

scale = 6
bitmap = page.render(scale=scale)
img = bitmap.to_pil()
w, h = img.size

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# Left col
left_box = (int(25 * scale), int(40 * scale), int(295 * scale), int(765 * scale))
img.crop(left_box).save(os.path.join(scratch_dir, "p02_left_full.png"))

# Right col
right_box = (int(295 * scale), int(40 * scale), int(580 * scale), int(765 * scale))
img.crop(right_box).save(os.path.join(scratch_dir, "p02_right_full.png"))

# 4 sections
img.crop((int(25 * scale), int(40 * scale), int(295 * scale), int(240 * scale))).save(os.path.join(scratch_dir, "p02_sec1.png"))
img.crop((int(25 * scale), int(220 * scale), int(295 * scale), int(420 * scale))).save(os.path.join(scratch_dir, "p02_sec2.png"))
img.crop((int(25 * scale), int(400 * scale), int(295 * scale), int(600 * scale))).save(os.path.join(scratch_dir, "p02_sec3.png"))
img.crop((int(25 * scale), int(580 * scale), int(295 * scale), int(765 * scale))).save(os.path.join(scratch_dir, "p02_sec4.png"))

print(f"Page 2 rendered: {w}x{h}")
