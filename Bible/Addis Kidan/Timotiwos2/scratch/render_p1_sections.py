import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"

doc = pymupdf.open(pdf_path)
page = doc[0]

# High zoom 5x
zoom = 5.0
mat = pymupdf.Matrix(zoom, zoom)

# Section 1: Top (Banner, Ch 1 heading, verses 1-5)
clip_top = pymupdf.Rect(30, 40, 310, 290)
pix = page.get_pixmap(matrix=mat, clip=clip_top)
pix.save(os.path.join(out_dir, "p01_crop1_top.png"))

# Section 2: Middle (verses 5-11)
clip_mid = pymupdf.Rect(30, 275, 310, 520)
pix = page.get_pixmap(matrix=mat, clip=clip_mid)
pix.save(os.path.join(out_dir, "p01_crop2_mid.png"))

# Section 3: Bottom (verses 11 to end of page)
clip_bot = pymupdf.Rect(30, 505, 310, 770)
pix = page.get_pixmap(matrix=mat, clip=clip_bot)
pix.save(os.path.join(out_dir, "p01_crop3_bot.png"))

print("Saved p01 crops: top, mid, bot")
