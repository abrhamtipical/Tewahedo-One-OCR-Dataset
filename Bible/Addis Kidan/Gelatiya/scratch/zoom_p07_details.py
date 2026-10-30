import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p7 = doc[6]

def save_zoom(name, rect, zoom=25):
    mat = fitz.Matrix(zoom, zoom)
    pix = p7.get_pixmap(matrix=mat, clip=rect)
    pix.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

# v24 line 1 & line 2
save_zoom("p07_detail_v24", fitz.Rect(55, 128, 290, 175))

# v25 line 1, 2, 3
save_zoom("p07_detail_v25", fitz.Rect(55, 180, 290, 245))

# v27 all lines
save_zoom("p07_detail_v27", fitz.Rect(55, 270, 290, 335))

# v28 - v31
save_zoom("p07_detail_v28_v31", fitz.Rect(55, 330, 290, 420))

# ch5 head & section 8 head & v1
save_zoom("p07_detail_ch5_head_s8_v1", fitz.Rect(55, 415, 290, 500))

# v4, v5, v6
save_zoom("p07_detail_v4_v5_v6", fitz.Rect(55, 580, 290, 680))

# v7, v8
save_zoom("p07_detail_v7_v8", fitz.Rect(55, 680, 290, 770))

print("Detailed 25x zooms saved.")
