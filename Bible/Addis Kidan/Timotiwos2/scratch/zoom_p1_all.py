import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"

doc = pymupdf.open(pdf_path)
page = doc[0]

zoom = 6.0
mat = pymupdf.Matrix(zoom, zoom)

crops = [
    ("p01_v0_title_sec1.png", pymupdf.Rect(30, 40, 310, 155)),
    ("p01_v1_v2.png", pymupdf.Rect(30, 150, 310, 240)),
    ("p01_v3_v4.png", pymupdf.Rect(30, 235, 310, 335)),
    ("p01_v5.png", pymupdf.Rect(30, 325, 310, 420)),
    ("p01_v6_v7.png", pymupdf.Rect(30, 415, 310, 495)),
    ("p01_v8.png", pymupdf.Rect(30, 490, 310, 565)),
    ("p01_v9_v10.png", pymupdf.Rect(30, 555, 310, 650)),
    ("p01_v11_v12.png", pymupdf.Rect(30, 640, 310, 725)),
    ("p01_v13_v14.png", pymupdf.Rect(30, 720, 310, 785)),
]

for name, r in crops:
    pix = page.get_pixmap(matrix=mat, clip=r)
    pix.save(os.path.join(out_dir, name))

print("All p01 zoomed crops generated!")
