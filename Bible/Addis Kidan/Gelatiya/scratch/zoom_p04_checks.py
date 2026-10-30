import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p4 = doc[3]

mat = fitz.Matrix(16, 16)

# Let's crop:
# 1. v2 and v3
pix1 = p4.get_pixmap(matrix=mat, clip=fitz.Rect(45, 65, 295, 205))
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_v2_v3.png")

# 2. v4, v5, v6
pix2 = p4.get_pixmap(matrix=mat, clip=fitz.Rect(45, 200, 295, 335))
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_v4_v6.png")

# 3. v7, v8, v9
pix3 = p4.get_pixmap(matrix=mat, clip=fitz.Rect(45, 330, 295, 470))
pix3.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_v7_v9.png")

# 4. v10, v11, v12
pix4 = p4.get_pixmap(matrix=mat, clip=fitz.Rect(45, 465, 295, 610))
pix4.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_v10_v12.png")

# 5. v13, v14
pix5 = p4.get_pixmap(matrix=mat, clip=fitz.Rect(45, 605, 295, 715))
pix5.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_v13_v14.png")

# 6. Section 4, v15, v16, v17
pix6 = p4.get_pixmap(matrix=mat, clip=fitz.Rect(45, 710, 295, 790))
pix6.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p04_sec4_v15_v17.png")

print("Page 4 detailed sections rendered successfully")
