import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[5]
mat = fitz.Matrix(25, 25)

# 1. Verse 11
clip1 = fitz.Rect(45, 105, 285, 155)
page.get_pixmap(matrix=mat, clip=clip1).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v11.png")

# 2. Verse 13
clip2 = fitz.Rect(45, 170, 285, 235)
page.get_pixmap(matrix=mat, clip=clip2).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v13.png")

# 3. Verse 14
clip3 = fitz.Rect(45, 235, 285, 305)
page.get_pixmap(matrix=mat, clip=clip3).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v14.png")

# 4. Verse 16
clip4 = fitz.Rect(45, 330, 285, 395)
page.get_pixmap(matrix=mat, clip=clip4).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v16.png")

# 5. Verse 17
clip5 = fitz.Rect(45, 385, 285, 435)
page.get_pixmap(matrix=mat, clip=clip5).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v17.png")

# 6. Verse 21 line 4 & Verse 22
clip6 = fitz.Rect(45, 520, 285, 590)
page.get_pixmap(matrix=mat, clip=clip6).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v21_22.png")

# 7. Verse 23
clip7 = fitz.Rect(45, 585, 285, 640)
page.get_pixmap(matrix=mat, clip=clip7).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_v23.png")

print("Saved all Page 6 hyper-zooms.")
