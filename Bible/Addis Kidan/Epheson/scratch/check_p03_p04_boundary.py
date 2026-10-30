import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# Check page 3 bottom at 8x scale: y from 680 to 770 pt
scale = 8
p3 = doc[2]
bm3 = p3.render(scale=scale)
img3 = bm3.to_pil()
p3_bottom = img3.crop((int(25 * scale), int(670 * scale), int(295 * scale), int(770 * scale)))
p3_bottom.save(os.path.join(scratch_dir, "p03_bottom_fine.png"))

# Check page 4 top at 8x scale: y from 90 to 220 pt
p4 = doc[3]
bm4 = p4.render(scale=scale)
img4 = bm4.to_pil()
p4_top = img4.crop((int(25 * scale), int(90 * scale), int(295 * scale), int(220 * scale)))
p4_top.save(os.path.join(scratch_dir, "p04_top_fine.png"))

print("Page 3 bottom and Page 4 top fine crops saved.")
