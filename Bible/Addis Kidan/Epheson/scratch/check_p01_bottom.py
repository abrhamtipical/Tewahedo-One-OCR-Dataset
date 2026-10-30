import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Bottom of page 1 (y: 700 to 765)
img.crop((int(25 * scale), int(700 * scale), int(295 * scale), int(765 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p01_bottom_zoom.png"
)

# Also let's check top of page 2 (index 1) left column (y: 40 to 120) to see the transition
page2 = doc[1]
bitmap2 = page2.render(scale=scale)
img2 = bitmap2.to_pil()
img2.crop((int(25 * scale), int(40 * scale), int(295 * scale), int(130 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p02_top_zoom.png"
)

print("Page 1 bottom and Page 2 top saved.")
