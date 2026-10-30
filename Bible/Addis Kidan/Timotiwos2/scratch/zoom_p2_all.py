import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"

doc = pymupdf.open(pdf_path)
page = doc[1] # Page 2

zoom = 6.0
mat = pymupdf.Matrix(zoom, zoom)

crops = [
    ("p02_v15_v18.png", pymupdf.Rect(30, 80, 310, 220)),
    ("p02_heading_sec2.png", pymupdf.Rect(30, 205, 310, 275)),
    ("p02_v1_v3.png", pymupdf.Rect(30, 265, 310, 395)),
    ("p02_v4_v7.png", pymupdf.Rect(30, 385, 310, 495)),
    ("p02_v8_v10.png", pymupdf.Rect(30, 485, 310, 600)),
    ("p02_v11_v13.png", pymupdf.Rect(30, 590, 310, 690)),
    ("p02_sec3_v14.png", pymupdf.Rect(30, 680, 310, 775)),
]

for name, r in crops:
    pix = page.get_pixmap(matrix=mat, clip=r)
    pix.save(os.path.join(out_dir, name))

print("All p02 zoomed crops generated!")
