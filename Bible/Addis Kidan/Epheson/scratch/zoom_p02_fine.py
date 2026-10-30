import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[1] # Page 2

scale = 25
bitmap = page.render(scale=scale)
img = bitmap.to_pil()

# Chapter 2 heading & Section 3: y: 350 to 420
img.crop((int(25 * scale), int(350 * scale), int(295 * scale), int(420 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p02_ch2_sec3_zoom.png"
)

# Ch 2 v2 - v3: y: 440 to 520
img.crop((int(25 * scale), int(440 * scale), int(295 * scale), int(520 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p02_v2_v3_zoom.png"
)

# Ch 2 v7 - v9: y: 580 to 670
img.crop((int(25 * scale), int(580 * scale), int(295 * scale), int(670 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p02_v7_v9_zoom.png"
)

# Ch 2 v10 - v11: y: 660 to 765
img.crop((int(25 * scale), int(660 * scale), int(295 * scale), int(765 * scale))).save(
    r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch\p02_v10_v11_zoom.png"
)

print("Page 2 fine zoom crops saved.")
