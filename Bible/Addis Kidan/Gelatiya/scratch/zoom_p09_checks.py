import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[8]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Let's crop:
# 1. v2-v3 (y: 160 to 240)
b1 = (int(25 * scale), int(160 * scale), int(290 * scale), int(240 * scale))
img.crop(b1).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v2_v3_zoom.png")

# 2. v5-v6 (y: 250 to 330)
b2 = (int(25 * scale), int(250 * scale), int(290 * scale), int(330 * scale))
img.crop(b2).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v5_v6_zoom.png")

# 3. v13 (y: 450 to 520)
b3 = (int(25 * scale), int(25 * scale), int(290 * scale), int(520 * scale)) # wait, y should be 450 to 520
b3 = (int(25 * scale), int(450 * scale), int(290 * scale), int(520 * scale))
img.crop(b3).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v13_zoom.png")

# 4. v14-v15 (y: 500 to 590)
b4 = (int(25 * scale), int(500 * scale), int(290 * scale), int(590 * scale))
img.crop(b4).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v14_v15_zoom.png")

# 5. v17-v18 (y: 600 to 680)
b5 = (int(25 * scale), int(600 * scale), int(290 * scale), int(680 * scale))
img.crop(b5).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_v17_v18_zoom.png")

# 6. Colophon (y: 680 to 765)
b6 = (int(25 * scale), int(680 * scale), int(290 * scale), int(765 * scale))
img.crop(b6).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_colophon_zoom.png")

print("Page 9 zoom checks saved!")
