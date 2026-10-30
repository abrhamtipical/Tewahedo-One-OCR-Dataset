import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page7 = doc[6]
mat = fitz.Matrix(20, 20)

# 1. Verse 2 & 3
clip1 = fitz.Rect(45, 105, 285, 190)
page7.get_pixmap(matrix=mat, clip=clip1).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v2_v3.png")

# 2. Verse 4 & 5
clip2 = fitz.Rect(45, 190, 285, 290)
page7.get_pixmap(matrix=mat, clip=clip2).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v4_v5.png")

# 3. Verse 8, 9, 10
clip3 = fitz.Rect(45, 360, 285, 500)
page7.get_pixmap(matrix=mat, clip=clip3).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v8_v10.png")

# 4. Verse 11, 12, 13
clip4 = fitz.Rect(45, 490, 285, 630)
page7.get_pixmap(matrix=mat, clip=clip4).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v11_v13.png")

# 5. Verse 14, 15, 16
clip5 = fitz.Rect(45, 620, 285, 750)
page7.get_pixmap(matrix=mat, clip=clip5).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v14_v16.png")

print("Saved all Page 7 hyper zooms.")
