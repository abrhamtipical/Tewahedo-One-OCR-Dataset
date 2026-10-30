import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(30, 30)

clip = fitz.Rect(55, 300, 280, 345)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v16_detail.png")
print("Saved v16 detail.")
