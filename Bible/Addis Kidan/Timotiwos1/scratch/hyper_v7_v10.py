import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[4]
mat = fitz.Matrix(15, 15)

# Verse 7 words
clip_v7 = fitz.Rect(110, 615, 275, 638)
pix_v7 = page.get_pixmap(matrix=mat, clip=clip_v7)
pix_v7.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v7_words.png")

# Verse 8 line 1 end & line 2 & line 3
clip_v8 = fitz.Rect(45, 635, 280, 695)
pix_v8 = page.get_pixmap(matrix=mat, clip=clip_v8)
pix_v8.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v8_words.png")

# Verse 9
clip_v9 = fitz.Rect(45, 690, 280, 740)
pix_v9 = page.get_pixmap(matrix=mat, clip=clip_v9)
pix_v9.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v9_words.png")

# Verse 10
clip_v10 = fitz.Rect(45, 730, 280, 790)
pix_v10 = page.get_pixmap(matrix=mat, clip=clip_v10)
pix_v10.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p05_v10_words.png")

print("Saved hyper-zooms.")
