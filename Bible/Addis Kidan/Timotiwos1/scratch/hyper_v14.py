import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(25, 25)

clip = fitz.Rect(45, 205, 290, 250)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v14_hyper_real.png")
print("Saved v14 hyper real.")
