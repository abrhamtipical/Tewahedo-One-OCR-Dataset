import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

scale = 25
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# v12: y: 490 to 540
img.crop((int(25 * scale), int(490 * scale), int(295 * scale), int(540 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p01_v12_zoom.png"
)

# v14: y: 560 to 605
img.crop((int(25 * scale), int(560 * scale), int(295 * scale), int(605 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p01_v14_zoom.png"
)

# v16: y: 640 to 685
img.crop((int(25 * scale), int(640 * scale), int(295 * scale), int(685 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p01_v16_zoom.png"
)

print("Targeted zoom crops saved.")
