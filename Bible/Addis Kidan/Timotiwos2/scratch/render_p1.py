import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
page = doc[0] # Page 1 (index 0)

# Ge'ez column is on the left
rect = page.rect
print("Page rect:", rect)

# Left column box roughly: x0=30, y0=40, x1=rect.width*0.53, y1=rect.height-30
clip_left = pymupdf.Rect(20, 30, rect.width * 0.52, rect.height - 30)

zoom = 4.0 # High resolution
mat = pymupdf.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, clip=clip_left)
pix.save(os.path.join(out_dir, "p01_crop_full.png"))
print("Saved p01_crop_full.png")
