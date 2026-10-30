import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)

# Page 8 bottom
p8 = doc[7]
pix8 = p8.get_pixmap(matrix=fitz.Matrix(6, 6), clip=fitz.Rect(45, 740, 295, 830))
pix8.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p08_bottom_check.png")

# Page 9 top
p9 = doc[8]
pix9 = p9.get_pixmap(matrix=fitz.Matrix(6, 6), clip=fitz.Rect(45, 65, 295, 300))
pix9.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p09_top_check.png")

print("Saved p8 bot and p9 top checks.")
