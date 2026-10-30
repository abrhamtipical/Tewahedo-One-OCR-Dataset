import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[8]

scale = 35
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# v3: y 220 to 245
img.crop((int(25 * scale), int(220 * scale), int(200 * scale), int(245 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v3_zoom35.png"
)

# v17 word 'ዘየነትየኒ' and surrounding: y 625 to 650
img.crop((int(25 * scale), int(625 * scale), int(290 * scale), int(655 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v17_zoom35.png"
)

# Colophon / Subscription: y 680 to 760
img.crop((int(25 * scale), int(680 * scale), int(290 * scale), int(760 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_colophon_zoom35.png"
)

print("Zoom 35x crops saved successfully.")
