import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[5]
mat = fitz.Matrix(4, 4)

# Bottom check
clip_bot = fitz.Rect(45, 700, 290, 790)
pix_bot = page.get_pixmap(matrix=mat, clip=clip_bot)
pix_bot.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_very_bottom.png")

# Also check top of Page 7 (page index 6)
page7 = doc[6]
clip_p7_top = fitz.Rect(45, 70, 290, 200)
pix_p7_top = page7.get_pixmap(matrix=mat, clip=clip_p7_top)
pix_p7_top.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_top_check.png")

print("Saved boundary checks.")
