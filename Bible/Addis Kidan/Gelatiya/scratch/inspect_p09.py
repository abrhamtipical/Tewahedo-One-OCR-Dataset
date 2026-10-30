import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[8]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# v3 - v4 (y: 210 to 280)
img.crop((int(25 * scale), int(205 * scale), int(290 * scale), int(285 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v3_v4.png"
)

# v13 (y: 460 to 525)
img.crop((int(25 * scale), int(460 * scale), int(290 * scale), int(525 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v13_target.png"
)

# v17 - v18 (y: 620 to 695)
img.crop((int(25 * scale), int(620 * scale), int(290 * scale), int(695 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v17_v18_target.png"
)

print("Images generated successfully.")
