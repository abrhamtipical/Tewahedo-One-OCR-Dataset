import fitz
from PIL import Image

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p7 = doc[6]

def save_zoom(name, rect, zoom=12):
    mat = fitz.Matrix(zoom, zoom)
    pix = p7.get_pixmap(matrix=mat, clip=rect)
    pix.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

# v23 to v25
save_zoom("p07_z_v23_v24", fitz.Rect(55, 95, 290, 195))
# v25 to v27
save_zoom("p07_z_v25_v27", fitz.Rect(55, 185, 290, 295))
# v28 to v31
save_zoom("p07_z_v28_v31", fitz.Rect(55, 290, 290, 420))
# Chapter 5 head, section 8 head, v1-v3
save_zoom("p07_z_ch5_head_v3", fitz.Rect(55, 410, 290, 560))
# v4 to v6
save_zoom("p07_z_v4_v6", fitz.Rect(55, 550, 290, 680))
# v7 to v8
save_zoom("p07_z_v7_v8", fitz.Rect(55, 670, 290, 770))

print("Zooms saved.")
