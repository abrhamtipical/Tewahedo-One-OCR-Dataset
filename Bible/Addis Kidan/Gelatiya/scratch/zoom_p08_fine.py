import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[7]

scale = 12
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Left column box roughly x: 25 to 290 pt
# Total page height 792 pt
# Band 1: v8 to v12 (y: 60 to 220)
# Band 2: v13 to v16 (y: 200 to 360)
# Band 3: v16 to v20 (y: 350 to 510)
# Band 4: v20 to v23 (y: 500 to 640)
# Band 5: v23 to v26 (y: 630 to 760)

def crop_band(ymin, ymax, name):
    box = (int(25 * scale), int(ymin * scale), int(290 * scale), int(ymax * scale))
    cropped = img.crop(box)
    cropped.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

crop_band(60, 220, "band1_v8_v12")
crop_band(210, 360, "band2_v13_v16")
crop_band(350, 500, "band3_v16_v20")
crop_band(490, 630, "band4_v20_v23")
crop_band(620, 750, "band5_v23_v26")
print("Bands saved successfully!")
