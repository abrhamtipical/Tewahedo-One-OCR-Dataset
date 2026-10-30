import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page7 = doc[6]
mat = fitz.Matrix(4, 4)

clip = fitz.Rect(45, 700, 290, 790)
pix = page7.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_bottom_exact.png")
print("Saved p7 bottom exact.")
