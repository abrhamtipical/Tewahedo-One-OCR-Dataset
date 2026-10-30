import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(8, 8)

# Crop verse 7 and 8
clip = fitz.Rect(45, 590, 285, 750)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v7_v10_zoom8x.png")
print("Saved 8x zoom of v7-v10")
