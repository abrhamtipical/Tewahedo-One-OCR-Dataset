import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(15, 15)

# Verse 9 lines 1 and 2, full width
clip = fitz.Rect(45, 655, 295, 700)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v9_wide.png")
print("Saved v9 wide.")
