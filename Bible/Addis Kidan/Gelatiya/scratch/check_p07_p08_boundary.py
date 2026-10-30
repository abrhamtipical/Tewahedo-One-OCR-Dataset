import fitz
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)

# Let's inspect page 7 bottom with larger y2
p7 = doc[6]
mat6 = fitz.Matrix(6, 6)
clip_bottom = fitz.Rect(45, 740, 295, 830)
pix = p7.get_pixmap(matrix=mat6, clip=clip_bottom)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p07_bottom_check.png")

# Also render top of page 8 (index 7)
p8 = doc[7]
clip_p8_top = fitz.Rect(45, 65, 295, 300)
pix_p8_top = p8.get_pixmap(matrix=mat6, clip=clip_p8_top)
pix_p8_top.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_top_check.png")

# Also Amharic bottom of page 7 to see where verse 8 ends
clip_amh_bot = fitz.Rect(295, 740, 550, 830)
pix_amh = p7.get_pixmap(matrix=mat6, clip=clip_amh_bot)
pix_amh.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p07_amh_bot_check.png")

print("Checks saved.")
