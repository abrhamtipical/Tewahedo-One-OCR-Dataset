import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 25
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# v26 is at the bottom of the left column (y: 670 to 750)
box = (int(25 * scale), int(670 * scale), int(290 * scale), int(750 * scale))
img.crop(box).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_v26_extreme.png")
print("v26 saved!")
