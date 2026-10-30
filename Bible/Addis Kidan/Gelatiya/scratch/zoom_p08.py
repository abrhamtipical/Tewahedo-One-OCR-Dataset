import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p8 = doc[7]

def save_zoom(name, rect, zoom=12):
    mat = fitz.Matrix(zoom, zoom)
    pix = p8.get_pixmap(matrix=mat, clip=rect)
    pix.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

# v8 line 2, v9, v10
save_zoom("p08_z_v8_v10", fitz.Rect(55, 95, 290, 210))
# v11, v12, section 9 head
save_zoom("p08_z_v11_sec9", fitz.Rect(55, 200, 290, 310))
# v13, v14, v15
save_zoom("p08_z_v13_v15", fitz.Rect(55, 300, 290, 430))
# v16, v17, v18
save_zoom("p08_z_v16_v18", fitz.Rect(55, 420, 290, 550))
# v19, v20, v21
save_zoom("p08_z_v19_v21", fitz.Rect(55, 540, 290, 670))
# v22, v23, v24, v25, v26
save_zoom("p08_z_v22_v26", fitz.Rect(55, 660, 290, 785))

print("Page 8 zooms saved.")
