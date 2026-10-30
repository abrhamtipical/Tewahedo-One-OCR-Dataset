import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(30, 30)

# Verse 10 lines 2, 3, 4
clip = fitz.Rect(45, 715, 275, 765)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v10_detail.png")
print("Saved v10 detail 30x.")
