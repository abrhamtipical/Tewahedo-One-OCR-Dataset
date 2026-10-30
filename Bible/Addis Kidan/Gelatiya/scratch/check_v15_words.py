import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Crop v15 in Ge'ez: y ~ 260 to 320 pt, x: 25 to 290
box_geez = (int(25 * scale), int(260 * scale), int(290 * scale), int(320 * scale))
img.crop(box_geez).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_geez_zoom.png")

# Crop v15 in Amharic (right column): x: 300 to 570, y ~ 260 to 320
box_amh = (int(290 * scale), int(260 * scale), int(580 * scale), int(320 * scale))
img.crop(box_amh).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_amh_zoom.png")

print("v15 crops saved!")
