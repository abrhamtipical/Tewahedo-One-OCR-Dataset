import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[5] # page 6 (0-indexed: 5)
print("Page 6 Rect:", page.rect)

# Render 3 crops: top, middle, bottom
mat = fitz.Matrix(4, 4)

# Left column is approx x: 40 to 290
clip_top = fitz.Rect(45, 100, 290, 320)
pix_top = page.get_pixmap(matrix=mat, clip=clip_top)
pix_top.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_crop1_top.png")

clip_mid = fitz.Rect(45, 310, 290, 530)
pix_mid = page.get_pixmap(matrix=mat, clip=clip_mid)
pix_mid.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_crop2_mid.png")

clip_bot = fitz.Rect(45, 520, 290, 750)
pix_bot = page.get_pixmap(matrix=mat, clip=clip_bot)
pix_bot.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_crop3_bot.png")

print("Saved page 6 crops.")
