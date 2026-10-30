import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p7 = doc[6]

mat = fitz.Matrix(25, 25)
pix = p7.get_pixmap(matrix=mat, clip=fitz.Rect(230, 715, 295, 750))
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p07_v8_end.png")
print("Saved v8 end.")
