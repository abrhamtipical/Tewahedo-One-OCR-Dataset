import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(12, 12)

# Verse 9 and line 1 of v10: x from 45 to 300, y from 670 to 760
clip = fitz.Rect(45, 670, 300, 765)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v9_full.png")
print("Saved v9 full.")
