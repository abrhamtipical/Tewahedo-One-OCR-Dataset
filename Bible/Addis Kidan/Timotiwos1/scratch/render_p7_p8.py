import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
print("Total pages in timotiwos1.pdf:", len(doc))

page7 = doc[6] # index 6 (page 7)
page8 = doc[7] # index 7 (page 8)
print("Page 7 Rect:", page7.rect)
print("Page 8 Rect:", page8.rect)

mat = fitz.Matrix(4, 4)

# Page 7 crops (top, mid, bot)
clip_p7_top = fitz.Rect(45, 100, 290, 330)
page7.get_pixmap(matrix=mat, clip=clip_p7_top).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_crop1_top.png")

clip_p7_mid = fitz.Rect(45, 320, 290, 540)
page7.get_pixmap(matrix=mat, clip=clip_p7_mid).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_crop2_mid.png")

clip_p7_bot = fitz.Rect(45, 530, 290, 760)
page7.get_pixmap(matrix=mat, clip=clip_p7_bot).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p07_crop3_bot.png")

# Page 8 full left column
clip_p8 = fitz.Rect(45, 100, 290, 760)
page8.get_pixmap(matrix=mat, clip=clip_p8).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p08_crop_all.png")

print("Saved Page 7 and Page 8 crops.")
