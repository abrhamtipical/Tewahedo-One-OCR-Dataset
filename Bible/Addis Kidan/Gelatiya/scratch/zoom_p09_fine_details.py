import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[8]

scale = 25
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# v6: y 270 to 310
img.crop((int(25 * scale), int(270 * scale), int(290 * scale), int(310 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v6_detail.png"
)

# v14: y 510 to 560
img.crop((int(25 * scale), int(510 * scale), int(290 * scale), int(560 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v14_detail.png"
)

# v16: y 580 to 620
img.crop((int(25 * scale), int(580 * scale), int(290 * scale), int(620 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v16_detail.png"
)

print("Detail crops saved.")
