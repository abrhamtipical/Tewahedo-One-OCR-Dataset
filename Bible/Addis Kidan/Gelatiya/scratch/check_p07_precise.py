import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p7 = doc[6]

def save_zoom(name, rect, zoom=25):
    mat = fitz.Matrix(zoom, zoom)
    pix = p7.get_pixmap(matrix=mat, clip=rect)
    pix.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

# 1. ch5 head & section 8 head & v1 & v2
save_zoom("p07_check_ch5_sec8_v1_v2", fitz.Rect(55, 450, 290, 560))

# 2. v6 complete
save_zoom("p07_check_v6_complete", fitz.Rect(55, 630, 290, 700))

# 3. v28 word 5
save_zoom("p07_check_v28_emsale", fitz.Rect(185, 325, 260, 360))

# 4. v30 line 1 word 4 & 5
save_zoom("p07_check_v30_word", fitz.Rect(180, 395, 275, 430))

# 5. v31 line 1 word 4
save_zoom("p07_check_v31_word", fitz.Rect(150, 420, 215, 455))

# 6. v25 line 2 'betahte'
save_zoom("p07_check_v25_betahte", fitz.Rect(160, 205, 210, 235))

print("Checks generated.")
