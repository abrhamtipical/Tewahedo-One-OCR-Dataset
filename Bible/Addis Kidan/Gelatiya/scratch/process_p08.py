import fitz
from PIL import Image
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)

# Page 8 is index 7
p8 = doc[7]

mat6 = fitz.Matrix(6, 6)
clip_left = fitz.Rect(45, 65, 295, 785)
pix_left = p8.get_pixmap(matrix=mat6, clip=clip_left)
left_path = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_left_full.png"
pix_left.save(left_path)

# Slices
im = Image.open(left_path)
W, H = im.size

im.crop((0, 0, W, int(H * 0.30))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_sec1.png")
im.crop((0, int(H * 0.25), W, int(H * 0.55))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_sec2.png")
im.crop((0, int(H * 0.50), W, int(H * 0.80))).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_sec3.png")
im.crop((0, int(H * 0.75), W, H)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_sec4.png")

# Amharic column
clip_right = fitz.Rect(295, 65, 550, 785)
pix_right = p8.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip_right)
pix_right.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_right_full.png")

print(f"Page 8 rendered: {W}x{H}")
