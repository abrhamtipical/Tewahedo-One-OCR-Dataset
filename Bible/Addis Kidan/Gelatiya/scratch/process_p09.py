import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[8] # 0-indexed page 9 (final page)

scale = 6
bitmap = page.render(scale=scale)
img = bitmap.to_pil()
w, h = img.size

# Left col: x approx [25, 290] pt
left_box = (int(25 * scale), int(45 * scale), int(295 * scale), int(765 * scale))
img.crop(left_box).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_left_full.png")

# Right col: x approx [295, 580] pt
right_box = (int(295 * scale), int(45 * scale), int(580 * scale), int(765 * scale))
img.crop(right_box).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_right_full.png")

# Slices of left column (height approx 720 pt)
# sec1: y 45 to 240
# sec2: y 220 to 420
# sec3: y 400 to 600
# sec4: y 580 to 765
img.crop((int(25 * scale), int(45 * scale), int(295 * scale), int(240 * scale))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_sec1.png")
img.crop((int(25 * scale), int(220 * scale), int(295 * scale), int(420 * scale))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_sec2.png")
img.crop((int(25 * scale), int(400 * scale), int(295 * scale), int(600 * scale))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_sec3.png")
img.crop((int(25 * scale), int(580 * scale), int(295 * scale), int(765 * scale))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_sec4.png")

print(f"Page 9 rendered: {w}x{h}")
