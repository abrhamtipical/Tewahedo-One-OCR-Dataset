import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 30
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Let's crop:
# v20: y: 490 to 550, x: 25 to 290
b_v20 = (int(25 * scale), int(495 * scale), int(290 * scale), int(555 * scale))
img.crop(b_v20).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v20_precise_30x.png")

print("v20 precise saved!")
