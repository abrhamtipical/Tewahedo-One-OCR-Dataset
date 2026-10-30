import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Let's crop:
# 1. v20 full (y: 440 to 520)
# 2. v21-v23 (y: 510 to 600)
# 3. v24-v26 (y: 590 to 720)

def crop(ymin, ymax, name):
    box = (int(25 * scale), int(ymin * scale), int(290 * scale), int(ymax * scale))
    img.crop(box).save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

crop(440, 520, "p08_v20_detailed")
crop(515, 600, "p08_v21_v23_detailed")
crop(595, 715, "p08_v24_v26_detailed")
print("Detailed crops saved!")
