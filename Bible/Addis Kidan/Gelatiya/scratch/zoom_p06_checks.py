import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p6 = doc[5]

mat = fitz.Matrix(20, 20)

# 1. v9 lines 2-3
pix1 = p6.get_pixmap(matrix=mat, clip=fitz.Rect(45, 185, 295, 250))
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p06_z_v9_line2.png")

# 2. v13, v14
pix2 = p6.get_pixmap(matrix=mat, clip=fitz.Rect(45, 335, 295, 410))
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p06_z_v13_v14.png")

# 3. v15, v16
pix3 = p6.get_pixmap(matrix=mat, clip=fitz.Rect(45, 400, 295, 475))
pix3.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p06_z_v15_v16.png")

# 4. v17, v18
pix4 = p6.get_pixmap(matrix=mat, clip=fitz.Rect(45, 465, 295, 545))
pix4.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p06_z_v17_v18.png")

# 5. v20, Section 7, v21, v22
pix5 = p6.get_pixmap(matrix=mat, clip=fitz.Rect(45, 590, 295, 785))
pix5.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p06_z_v20_v22.png")

print("Page 6 high zoom crops saved successfully")
