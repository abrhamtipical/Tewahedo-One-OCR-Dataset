import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 35
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# v15 lines
box1 = (int(200 * scale), int(345 * scale), int(290 * scale), int(375 * scale))
box2 = (int(25 * scale), int(370 * scale), int(150 * scale), int(405 * scale))

img.crop(box1).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_l1_end.png")
img.crop(box2).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_l2_start.png")

print("v15 extreme zoom saved!")
