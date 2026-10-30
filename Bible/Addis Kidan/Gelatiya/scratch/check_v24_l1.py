import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p7 = doc[6]

mat = fitz.Matrix(25, 25)
pix = p7.get_pixmap(matrix=mat, clip=fitz.Rect(55, 140, 290, 165))
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p07_v24_line1_exact.png")
print("Saved.")
