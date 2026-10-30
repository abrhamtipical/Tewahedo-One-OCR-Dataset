import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p3 = doc[2]

# Matrix 14x for ultra clarity
mat = fitz.Matrix(14, 14)

crops = [
    ("v11_word", fitz.Rect(45, 175, 295, 215)),
    ("v12_line2", fitz.Rect(45, 220, 295, 260)),
    ("v14_all", fitz.Rect(45, 305, 295, 410)),
    ("v15_all", fitz.Rect(45, 400, 295, 455)),
    ("v17_v18", fitz.Rect(45, 495, 295, 580)),
    ("v19_v20", fitz.Rect(45, 570, 295, 665)),
    ("ch3_head", fitz.Rect(45, 680, 295, 755)),
    ("ch3_v1", fitz.Rect(45, 740, 295, 790)),
]

for name, r in crops:
    pix = p3.get_pixmap(matrix=mat, clip=r)
    pix.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_z_{name}.png")

# Also let's get the Amharic right column for verses 11-14 and 17-20 to cross-check textual meaning
pix_amh = p3.get_pixmap(matrix=fitz.Matrix(5, 5), clip=fitz.Rect(300, 160, 575, 550))
pix_amh.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_amh_mid.png")

print("Ultra-zoomed crops rendered successfully")
