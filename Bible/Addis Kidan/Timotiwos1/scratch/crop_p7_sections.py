import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page7 = doc[6]
mat = fitz.Matrix(15, 15)

# v4-v7
clip_v4_v7 = fitz.Rect(45, 230, 285, 380)
page7.get_pixmap(matrix=mat, clip=clip_v4_v7).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v4_v7.png")

# v8-v10
clip_v8_v10 = fitz.Rect(45, 370, 285, 500)
page7.get_pixmap(matrix=mat, clip=clip_v8_v10).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v8_v10_clean.png")

# v11-v13
clip_v11_v13 = fitz.Rect(45, 490, 285, 620)
page7.get_pixmap(matrix=mat, clip=clip_v11_v13).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v11_v13_clean.png")

# v14-v16
clip_v14_v16 = fitz.Rect(45, 610, 285, 740)
page7.get_pixmap(matrix=mat, clip=clip_v14_v16).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_hyper_v14_v16_clean.png")

print("Saved all clean crops.")
