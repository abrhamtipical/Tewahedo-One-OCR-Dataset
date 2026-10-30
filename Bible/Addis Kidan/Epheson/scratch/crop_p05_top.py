import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
p5 = doc[4] # Page 5 (0-indexed is 4)

scale = 6
bitmap = p5.render(scale=scale)
img = bitmap.to_pil()

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"
# Top of page 5 left col
crop = img.crop((int(25 * scale), int(90 * scale), int(295 * scale), int(220 * scale)))
crop.save(os.path.join(scratch_dir, "p05_top_fine.png"))
print("Page 5 top fine saved.")
