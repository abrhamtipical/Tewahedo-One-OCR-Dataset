import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[8]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Amharic v2-v4 on right column: x: 295 to 580, y: 160 to 280
img.crop((int(295 * scale), int(160 * scale), int(580 * scale), int(280 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_amh_v2_v4.png"
)

# Amharic v17 on right column: x: 295 to 580, y: 610 to 670
img.crop((int(295 * scale), int(610 * scale), int(580 * scale), int(670 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_amh_v17.png"
)

print("Amharic crops saved.")
