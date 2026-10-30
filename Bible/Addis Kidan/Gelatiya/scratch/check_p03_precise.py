import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p3 = doc[2]

mat30 = fitz.Matrix(24, 24)

# 1. v14 word 1
pix1 = p3.get_pixmap(matrix=mat30, clip=fitz.Rect(50, 310, 110, 335))
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_v14_w1.png")

# 2. v15 fiteretene
pix2 = p3.get_pixmap(matrix=mat30, clip=fitz.Rect(100, 420, 200, 445))
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_v15_fitret.png")

# 3. v17 line 2 end
pix3 = p3.get_pixmap(matrix=mat30, clip=fitz.Rect(180, 520, 270, 545))
pix3.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_v17_end.png")

# 4. v18 line 1
pix4 = p3.get_pixmap(matrix=mat30, clip=fitz.Rect(50, 545, 250, 575))
pix4.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_v18_line1.png")

# 5. v20 full lines
pix5 = p3.get_pixmap(matrix=fitz.Matrix(16, 16), clip=fitz.Rect(45, 620, 290, 715))
pix5.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_v20_full.png")

# 6. v21 full lines
pix6 = p3.get_pixmap(matrix=fitz.Matrix(16, 16), clip=fitz.Rect(45, 710, 290, 765))
pix6.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_v21_full.png")

# 7. Chapter 3 heading
pix7 = p3.get_pixmap(matrix=mat30, clip=fitz.Rect(110, 760, 200, 790))
pix7.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_ch3_head.png")

# Amharic column for v17-v21
pix_amh2 = p3.get_pixmap(matrix=fitz.Matrix(6, 6), clip=fitz.Rect(300, 380, 575, 750))
pix_amh2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_amh_v17_v21.png")

print("Detailed checks rendered")
