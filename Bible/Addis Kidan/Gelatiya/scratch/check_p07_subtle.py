import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p7 = doc[6]

def save_zoom(name, rect, zoom=25):
    mat = fitz.Matrix(zoom, zoom)
    pix = p7.get_pixmap(matrix=mat, clip=rect)
    pix.save(rf"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\{name}.png")

save_zoom("p07_check_v24_line1", fitz.Rect(55, 120, 290, 160))
save_zoom("p07_check_v25_betahte_word", fitz.Rect(185, 205, 275, 235))

print("Checks done.")
