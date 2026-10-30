import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 30
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# 1. v20 words: 'ት...ርት ተወሳፍ...'
# y ~ 455 to 495, x: 100 to 285
b1 = (int(110 * scale), int(455 * scale), int(290 * scale), int(480 * scale))
img.crop(b1).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v20_line1_words.png")

# 2. v20 line 2: 'ጐ...ይ'
# y ~ 475 to 500, x: 80 to 180
b2 = (int(80 * scale), int(475 * scale), int(180 * scale), int(500 * scale))
img.crop(b2).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v20_line2_goyey.png")

# 3. v15 line 2 start: 'ል... ተ...'
b3 = (int(30 * scale), int(370 * scale), int(140 * scale), int(405 * scale))
img.crop(b3).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_words_zoom30.png")

print("Saved ultra zoom!")
