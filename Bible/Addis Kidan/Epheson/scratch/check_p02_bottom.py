import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)

scale = 20
# Bottom of page 2 (index 1): y: 700 to 765
page2 = doc[1]
bitmap2 = page2.render(scale=scale)
img2 = bitmap2.to_pil()
img2.crop((int(25 * scale), int(700 * scale), int(295 * scale), int(765 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p02_bottom_zoom.png"
)

# Top of page 3 (index 2): y: 40 to 120
page3 = doc[2]
bitmap3 = page3.render(scale=scale)
img3 = bitmap3.to_pil()
img3.crop((int(25 * scale), int(40 * scale), int(295 * scale), int(120 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p03_top_zoom.png"
)

print("Page 2 bottom and Page 3 top saved.")
