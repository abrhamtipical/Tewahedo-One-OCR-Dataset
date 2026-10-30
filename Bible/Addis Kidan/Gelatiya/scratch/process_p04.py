import fitz
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)

# Page 4 is index 3
p4 = doc[3]

mat6 = fitz.Matrix(6, 6)
clip_left = fitz.Rect(45, 65, 295, 785)
pix_left = p4.get_pixmap(matrix=mat6, clip=clip_left)
left_path = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_left_full.png"
pix_left.save(left_path)

# Slice into 4 overlapping parts
im = Image.open(left_path)
W, H = im.size

im.crop((0, 0, W, int(H * 0.30))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_sec1.png")
im.crop((0, int(H * 0.25), W, int(H * 0.55))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_sec2.png")
im.crop((0, int(H * 0.50), W, int(H * 0.80))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_sec3.png")
im.crop((0, int(H * 0.75), W, H)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_sec4.png")

print(f"Page 4 rendered successfully: {W}x{H}")
