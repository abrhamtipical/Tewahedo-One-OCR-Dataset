import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4] # page 5

# Let's see the height and width of page
rect = page.rect
print("Page rect:", rect)

# Let's crop the bottom half of the left column
# Left column is approximately x0=40 to x1=280 (or 50 to 300)
# Let's render y from 400 to 750 at 4x zoom
mat = fitz.Matrix(4, 4)

clip1 = fitz.Rect(45, 450, 285, 620)
pix1 = page.get_pixmap(matrix=mat, clip=clip1)
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v6_v8.png")

clip2 = fitz.Rect(45, 600, 285, 750)
pix2 = page.get_pixmap(matrix=mat, clip=clip2)
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v9_v10.png")

print("Saved crops successfully.")
