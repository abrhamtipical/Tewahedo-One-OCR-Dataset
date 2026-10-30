import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[5]
mat = fitz.Matrix(25, 25)

# Verse 16: y from 300 to 365
clip = fitz.Rect(45, 300, 285, 365)
page.get_pixmap(matrix=mat, clip=clip).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v16_exact.png")
print("Saved v16 exact.")
