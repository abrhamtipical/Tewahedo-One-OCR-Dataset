import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[2] # Page 3 (0-indexed is 2)

scale = 8
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# Top of Page 3 left col: y from 90 to 200 pt, x from 25 to 295 pt
crop1 = img.crop((int(25 * scale), int(90 * scale), int(295 * scale), int(220 * scale)))
crop1.save(os.path.join(scratch_dir, "p03_top_lines.png"))

print("Top lines saved at 8x scale")
