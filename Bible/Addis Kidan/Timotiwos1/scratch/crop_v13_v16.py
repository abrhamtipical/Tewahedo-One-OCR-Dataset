import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(12, 12)

# Verses 13, 14, 15, 16: full width
clip = fitz.Rect(45, 180, 290, 340)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v13_v16_wide.png")
print("Saved v13-v16 wide.")
