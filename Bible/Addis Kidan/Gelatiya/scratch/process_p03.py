import fitz
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)

# Page 3 is index 2
p3 = doc[2]

# Left column
mat6 = fitz.Matrix(6, 6)
clip_left = fitz.Rect(45, 65, 295, 740)
pix_left = p3.get_pixmap(matrix=mat6, clip=clip_left)
left_path = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_left_full.png"
pix_left.save(left_path)

# Right column (Amharic)
mat4 = fitz.Matrix(4, 4)
clip_right = fitz.Rect(300, 65, 575, 740)
pix_right = p3.get_pixmap(matrix=mat4, clip=clip_right)
right_path = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_right_full.png"
pix_right.save(right_path)

# Slice left column
im = Image.open(left_path)
W, H = im.size

# 4 overlapping slices: 0-30%, 25-55%, 50-80%, 75-100%
im.crop((0, 0, W, int(H * 0.30))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec1.png")
im.crop((0, int(H * 0.25), W, int(H * 0.55))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec2.png")
im.crop((0, int(H * 0.50), W, int(H * 0.80))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec3.png")
im.crop((0, int(H * 0.75), W, H)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec4.png")

print(f"Page 3 rendered successfully: {W}x{H}")
