import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 20
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Crop v15 Ge'ez: y ~ 330 to 410 pt, x: 25 to 290
box_geez = (int(25 * scale), int(330 * scale), int(290 * scale), int(410 * scale))
img.crop(box_geez).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_real_zoom.png")

# Crop v15 Amharic: y ~ 330 to 410 pt, x: 290 to 580
box_amh = (int(290 * scale), int(330 * scale), int(580 * scale), int(410 * scale))
img.crop(box_amh).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\v15_amh_real_zoom.png")

print("Real v15 saved!")
