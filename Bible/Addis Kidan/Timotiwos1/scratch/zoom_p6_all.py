import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[5]
mat = fitz.Matrix(8, 8)

# 1. Verses 11-13 (top)
clip1 = fitz.Rect(45, 100, 290, 240)
pix1 = page.get_pixmap(matrix=mat, clip=clip1)
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_v11_v13_zoom.png")

# 2. Verses 14-16 (mid-top)
clip2 = fitz.Rect(45, 230, 290, 360)
pix2 = page.get_pixmap(matrix=mat, clip=clip2)
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_v14_v16_zoom.png")

# 3. Verses 17-19 (mid)
clip3 = fitz.Rect(45, 350, 290, 480)
pix3 = page.get_pixmap(matrix=mat, clip=clip3)
pix3.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_v17_v19_zoom.png")

# 4. Verses 20-22 (mid-bot)
clip4 = fitz.Rect(45, 470, 290, 590)
pix4 = page.get_pixmap(matrix=mat, clip=clip4)
pix4.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_v20_v22_zoom.png")

# 5. Verses 23-25, Ch 6, Sec 6, 6:1 (bot)
clip5 = fitz.Rect(45, 580, 290, 750)
pix5 = page.get_pixmap(matrix=mat, clip=clip5)
pix5.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_v23_ch6_zoom.png")

print("Saved all 5 zoom segments of Page 6.")
