import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"

doc = pymupdf.open(pdf_path)
page = doc[2] # Page 3

zoom = 6.0
mat = pymupdf.Matrix(zoom, zoom)

crops = [
    ("p03_v15_v17.png", pymupdf.Rect(30, 80, 310, 220)),
    ("p03_v18_v20.png", pymupdf.Rect(30, 210, 310, 340)),
    ("p03_v21_v23.png", pymupdf.Rect(30, 330, 310, 460)),
    ("p03_v24_v26.png", pymupdf.Rect(30, 450, 310, 580)),
    ("p03_ch3_headings_v1_v2.png", pymupdf.Rect(30, 570, 310, 775)),
]

for name, r in crops:
    pix = page.get_pixmap(matrix=mat, clip=r)
    pix.save(os.path.join(out_dir, name))

print("All p03 zoomed crops generated!")
