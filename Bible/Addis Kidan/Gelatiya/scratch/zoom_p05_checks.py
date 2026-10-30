import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p5 = doc[4] # page 5

mat = fitz.Matrix(16, 16)

# 1. v19 & v20 (hruy / hiruys)
pix1 = p5.get_pixmap(matrix=mat, clip=fitz.Rect(45, 150, 295, 255))
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p05_z_v19_v20.png")

# 2. v21 & v22 (sobehu, zegese / ze'agete)
pix2 = p5.get_pixmap(matrix=mat, clip=fitz.Rect(45, 230, 295, 360))
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p05_z_v21_v22.png")

# 3. v23, v24, v25 (akbetene, merha/mogzit)
pix3 = p5.get_pixmap(matrix=mat, clip=fitz.Rect(45, 345, 295, 470))
pix3.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p05_z_v23_v25.png")

# 4. v27, v28, v29
pix4 = p5.get_pixmap(matrix=mat, clip=fitz.Rect(45, 460, 295, 570))
pix4.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p05_z_v27_v29.png")

# 5. Ch 4 heading, Section 5 heading, v1
pix5 = p5.get_pixmap(matrix=mat, clip=fitz.Rect(45, 550, 295, 680))
pix5.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p05_z_ch4_head_v1.png")

# 6. v2, v3, v4, v5
pix6 = p5.get_pixmap(matrix=mat, clip=fitz.Rect(45, 660, 295, 785))
pix6.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p05_z_v2_v5.png")

print("Page 5 high-zoom crops saved")
